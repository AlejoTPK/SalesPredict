"""Train an XGBoost model for sales forecasting.

Usage:
    poetry run python -m training.train_xgboost [--rows 500] [--log-to-mlflow]
"""

import argparse
import os
from pathlib import Path

import mlflow
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error

from config.ml_config import get_config
from training.feature_engineering import (
    build_aggregated_features,
    generate_synthetic_sales,
    split_train_test,
)
from training.hyperparameter_tuning import grid_search


def main() -> None:
    parser = argparse.ArgumentParser(description="Train XGBoost sales forecast model")
    parser.add_argument("--rows", type=int, default=500, help="Number of synthetic rows")
    parser.add_argument("--log-to-mlflow", action="store_true", help="Log experiment to MLflow")
    parser.add_argument("--output", type=str, default=None, help="Output model path")
    args = parser.parse_args()

    cfg = get_config()

    print(f"Generating {args.rows} synthetic sales records...")
    df = generate_synthetic_sales(rows=args.rows)
    print(f"  Data shape: {df.shape}")

    print("Building time-series features...")
    features_df = build_aggregated_features(df)
    print(f"  Features shape: {features_df.shape}")

    X_train, y_train, X_test, y_test = split_train_test(features_df)
    print(f"  Train: {len(X_train)} samples, Test: {len(X_test)} samples")
    print(f"  Features: {list(X_train.columns)}")

    print("Running hyperparameter search...")
    search_results = grid_search(X_train, y_train)
    best_params = search_results["best_params"]
    print(f"  Best MAE: {search_results['best_mae']:.2f}")
    print(f"  Best params: {best_params}")

    final_model = xgb.XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
        **best_params,
    )
    final_model.fit(X_train, y_train)

    y_pred = final_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nFinal model on test set ({len(X_test)} samples):")
    print(f"  MAE:  {mae:.2f}")
    print(f"  R2:   {r2:.4f}")

    artifact_dir = (
        Path(args.output).parent if args.output else Path(__file__).parent.parent / "artifacts"
    )
    artifact_dir.mkdir(parents=True, exist_ok=True)

    model_path = str(Path(args.output) if args.output else artifact_dir / "xgboost_model.json")
    final_model.save_model(model_path)
    print(f"\nModel saved to: {model_path}")

    if args.log_to_mlflow:
        mlflow.set_tracking_uri(cfg.mlflow_tracking_uri)
        mlflow.set_experiment(cfg.experiment_name)

        with mlflow.start_run():
            mlflow.log_params(best_params)
            mlflow.log_params({"train_rows": len(X_train), "test_rows": len(X_test)})
            mlflow.log_metrics({"mae": mae, "r2": r2})
            mlflow.log_artifact(model_path, "model")
            mlflow.xgboost.log_model(final_model, "xgboost_model")
        print("  Logged to MLflow")


if __name__ == "__main__":
    main()
