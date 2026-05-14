from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import xgboost as xgb


class SalesPredictor:
    def __init__(self, model_path_or_uri: str) -> None:
        if model_path_or_uri.startswith("models:/"):
            import mlflow

            self._model = mlflow.xgboost.load_model(model_path_or_uri)
        elif os.path.exists(model_path_or_uri):
            self._model = xgb.XGBRegressor()
            self._model.load_model(model_path_or_uri)
        else:
            raise FileNotFoundError(f"Model not found: {model_path_or_uri}")

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        return self._model.predict(features)

    def forecast(
        self,
        historical_df: pd.DataFrame,
        days_ahead: int = 30,
        date_col: str = "sale_date",
        amount_col: str = "amount",
    ) -> pd.DataFrame:
        df = historical_df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)

        daily = df.resample("D").agg({amount_col: "sum"}).fillna(0)

        for lag in [1, 3, 7, 14, 30]:
            daily[f"lag_{lag}"] = daily[amount_col].shift(lag)

        daily["rolling_7"] = daily[amount_col].rolling(7).mean()
        daily["rolling_14"] = daily[amount_col].rolling(14).mean()
        daily["rolling_30"] = daily[amount_col].rolling(30).mean()
        daily["ewm_7"] = daily[amount_col].ewm(span=7).mean()

        daily["day_of_week"] = daily.index.dayofweek
        daily["month"] = daily.index.month
        daily["is_month_start"] = daily.index.is_month_start.astype(int)
        daily["is_month_end"] = daily.index.is_month_end.astype(int)

        daily = daily.dropna()
        feature_cols = [c for c in daily.columns if c != amount_col]

        forecasts = []
        last_features = daily[feature_cols].iloc[-1:].copy()

        for i in range(days_ahead):
            pred = float(self._model.predict(last_features)[0])
            forecast_date = daily.index[-1] + pd.Timedelta(days=i + 1)
            forecasts.append({"date": forecast_date, "predicted_amount": pred})

            if i < days_ahead - 1:
                last_features["lag_1"] = pred
                for lag in [3, 7, 14, 30]:
                    if i + 1 >= lag:
                        last_features[f"lag_{lag}"] = forecasts[i + 1 - lag]["predicted_amount"]
                last_features["day_of_week"] = forecast_date.dayofweek
                last_features["month"] = forecast_date.month
                last_features["rolling_7"] = np.mean(
                    [f["predicted_amount"] for f in forecasts[-7:]]
                    if i >= 6
                    else [f["predicted_amount"] for f in forecasts]
                )
                last_features["rolling_14"] = np.mean(
                    [f["predicted_amount"] for f in forecasts[-14:]]
                    if i >= 13
                    else [f["predicted_amount"] for f in forecasts]
                )
                last_features["rolling_30"] = np.mean(
                    [f["predicted_amount"] for f in forecasts[-30:]]
                    if i >= 29
                    else [f["predicted_amount"] for f in forecasts]
                )
                last_features["ewm_7"] = last_features["rolling_7"]
                last_features["is_month_start"] = int(forecast_date.day == 1)
                last_features["is_month_end"] = 0

        return pd.DataFrame(forecasts)
