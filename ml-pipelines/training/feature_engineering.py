from datetime import datetime, timedelta
from typing import Tuple

import numpy as np
import pandas as pd


def generate_synthetic_sales(rows: int = 500) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    start = datetime.utcnow() - timedelta(days=rows)
    dates = pd.date_range(start, periods=rows, freq="D")

    products = ["Enterprise Suite", "Starter Plan", "Consulting", "Support Pro"]
    regions = ["North America", "Europe", "Asia Pacific", "Latin America"]

    data = {
        "sale_date": dates,
        "product_id": rng.choice(products, size=rows),
        "region": rng.choice(regions, size=rows),
        "amount": rng.lognormal(mean=8.0, sigma=1.2, size=rows),
        "quantity": rng.integers(1, 20, size=rows),
        "status": rng.choice(["completed", "completed", "completed", "pending"], size=rows),
    }
    return pd.DataFrame(data)


def add_time_features(df: pd.DataFrame, date_col: str = "sale_date") -> pd.DataFrame:
    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    df["day_of_week"] = df[date_col].dt.dayofweek
    df["day_of_month"] = df[date_col].dt.day
    df["month"] = df[date_col].dt.month
    df["quarter"] = df[date_col].dt.quarter
    df["year"] = df[date_col].dt.year
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    return df


def build_aggregated_features(
    df: pd.DataFrame,
    date_col: str = "sale_date",
    target_col: str = "amount",
) -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)

    daily = df.resample("D").agg({target_col: "sum", "quantity": "sum"}).fillna(0)

    for lag in [1, 3, 7, 14, 30]:
        daily[f"lag_{lag}"] = daily[target_col].shift(lag)

    daily["rolling_7"] = daily[target_col].rolling(7).mean()
    daily["rolling_14"] = daily[target_col].rolling(14).mean()
    daily["rolling_30"] = daily[target_col].rolling(30).mean()
    daily["ewm_7"] = daily[target_col].ewm(span=7).mean()

    daily["day_of_week"] = daily.index.dayofweek
    daily["month"] = daily.index.month
    daily["is_month_start"] = daily.index.is_month_start.astype(int)
    daily["is_month_end"] = daily.index.is_month_end.astype(int)

    return daily.dropna()


def split_train_test(
    df: pd.DataFrame, target_col: str = "amount"
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    split_idx = int(len(df) * 0.8)

    features = [c for c in df.columns if c != target_col]
    X = df[features]
    y = df[target_col]

    return X.iloc[:split_idx], y.iloc[:split_idx], X.iloc[split_idx:], y.iloc[split_idx:]
