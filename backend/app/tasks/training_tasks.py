import asyncio
import os
import tempfile

import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score

from app.core.config import settings
from app.infrastructure.db.session import async_session_factory
from app.tasks import celery_app


async def _prepare_features(days_back: int = 365) -> pd.DataFrame:
    from datetime import datetime, timedelta

    from app.infrastructure.repositories.sale_repo import get_sales_by_date_range

    end = datetime.utcnow()
    start = end - timedelta(days=days_back)

    async with async_session_factory() as db:
        sales = await get_sales_by_date_range(db, start, end)

    rows = [
        {
            "sale_date": s.sale_date,
            "product_id": s.product_id,
            "amount": s.amount,
            "quantity": s.quantity,
        }
        for s in sales
    ]

    df = pd.DataFrame(rows)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df = df.set_index("sale_date")

    daily = df.resample("D").agg({"amount": "sum", "quantity": "sum"}).fillna(0)

    for lag in [1, 3, 7, 14, 30]:
        daily[f"amount_lag_{lag}"] = daily["amount"].shift(lag)

    daily["amount_rolling_7"] = daily["amount"].rolling(7).mean()
    daily["amount_rolling_30"] = daily["amount"].rolling(30).mean()
    daily["day_of_week"] = daily.index.dayofweek
    daily["month"] = daily.index.month

    return daily.dropna()


async def _train_model(days_back: int = 365) -> dict:
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    with mlflow.start_run():
        df = await _prepare_features(days_back)

        target = "amount"
        feature_columns = [c for c in df.columns if c != target]
        X = df[feature_columns]
        y = df[target]

        split = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]

        params = {
            "objective": "reg:squarederror",
            "max_depth": 6,
            "learning_rate": 0.05,
            "n_estimators": 200,
            "subsample": 0.8,
        }
        mlflow.log_params(params)

        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metrics({"mae": mae, "r2": r2})
        mlflow.log_param("train_days", days_back)
        mlflow.log_param("feature_count", len(feature_columns))
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, "model.json")
            model.save_model(model_path)
            mlflow.log_artifact(model_path, "model")

        mlflow.xgboost.log_model(model, "xgboost_model")

    return {
        "message": "Training complete",
        "mae": mae,
        "r2": r2,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "features": feature_columns,
    }


@celery_app.task(name="train_sales_model")
def train_sales_model(days_back: int = 365) -> dict:
    return asyncio.run(_train_model(days_back=days_back))
