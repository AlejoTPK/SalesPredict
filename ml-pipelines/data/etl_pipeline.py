from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(str(path))


def load_from_postgres(connection_string: str, query: str) -> pd.DataFrame:
    from sqlalchemy import create_engine

    engine = create_engine(connection_string)
    try:
        return pd.read_sql(query, engine)
    finally:
        engine.dispose()


def export_to_csv(df: pd.DataFrame, path: str | Path) -> str:
    os.makedirs(str(Path(path).parent), exist_ok=True)
    df.to_csv(str(path), index=False)
    return str(path)


def validate_sales_df(df: pd.DataFrame) -> dict[str, Any]:
    required_columns = {"sale_date", "amount"}
    missing = required_columns - set(df.columns)
    warnings: list[str] = []

    for col in missing:
        warnings.append(f"Missing required column: {col}")

    if "sale_date" in df.columns:
        try:
            pd.to_datetime(df["sale_date"])
        except Exception:
            warnings.append("Column sale_date is not parseable as datetime")

    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            warnings.append("Column amount is not numeric")
        elif (df["amount"] < 0).any():
            warnings.append("Column amount contains negative values")

    if warnings:
        return {"valid": False, "warnings": warnings}

    return {"valid": True, "warnings": [], "rows": len(df), "columns": list(df.columns)}


def generate_date_range_parquet(start: str, end: str, output_path: str, freq: str = "D") -> str:
    dates = pd.date_range(start=start, end=end, freq=freq)
    df = pd.DataFrame({"date": dates})
    os.makedirs(str(Path(output_path).parent), exist_ok=True)
    df.to_parquet(output_path, index=False)
    return output_path
