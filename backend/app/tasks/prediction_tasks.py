import asyncio
from datetime import datetime, timedelta

import mlflow
import pandas as pd

from app.core.config import settings
from app.infrastructure.db.session import async_session_factory
from app.tasks import celery_app


async def _generate_forecast(days_ahead: int = 30) -> dict:
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    model = mlflow.xgboost.load_model("models:/xgboost_model/Production")

    from datetime import datetime, timedelta

    from app.infrastructure.repositories.sale_repo import get_sales_by_date_range

    end = datetime.utcnow()
    start = end - timedelta(days=90)

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

    latest = daily.dropna().iloc[-1:]

    if latest.empty:
        return {"message": "Insufficient data for forecast", "forecast": []}

    feature_columns = [c for c in latest.columns if c != "amount"]
    X_latest = latest[feature_columns]

    forecasts = []
    current_features = X_latest.copy()

    for i in range(days_ahead):
        pred = model.predict(current_features)[0]
        forecast_date = (datetime.utcnow() + timedelta(days=i + 1)).date().isoformat()
        forecasts.append({"date": forecast_date, "predicted_amount": round(float(pred), 2)})

    return {
        "message": f"Forecast generated for {days_ahead} days",
        "forecast": forecasts,
        "model_used": "xgboost_model/Production",
    }


@celery_app.task(name="generate_forecast")
def generate_forecast(days_ahead: int = 30) -> dict:
    return asyncio.run(_generate_forecast(days_ahead=days_ahead))
