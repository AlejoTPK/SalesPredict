"""Prediction service — ML-powered forecasting and inventory recommendations."""

import math
from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PredictionError
from app.infrastructure.repositories import sale_repo
from app.schemas.prediction import ForecastPoint, ProductRecommendation

_FORECAST_CACHE: dict[str, dict] = {}


def _std_dev_from_residuals(historical: list[float], predicted: list[float]) -> float:
    if len(historical) < 2:
        return 0.0
    residuals = [abs(h - p) for h, p in zip(historical, predicted, strict=False)]
    return float(np.std(residuals)) if residuals else 0.0


def _compute_trend(old_val: float, new_val: float) -> float:
    if old_val <= 0:
        return 100.0 if new_val > 0 else 0.0
    return round((new_val - old_val) / old_val * 100, 1)


async def _simple_forecast(daily_data: pd.DataFrame, days_ahead: int) -> list[ForecastPoint]:
    if daily_data.empty or len(daily_data) < 3:
        return []

    amounts = daily_data["daily_amount"].tolist()
    dates = daily_data["period"].tolist()

    last_date = pd.to_datetime(dates[-1])
    window = min(14, len(amounts))
    rolling_avg = float(np.mean(amounts[-window:]))

    recent = amounts[-window:]
    trend = 0.0
    if len(recent) > 1:
        x = np.arange(len(recent))
        coeffs = np.polyfit(x, recent, 1)
        trend = float(coeffs[0])

    std_dev = float(np.std(amounts[-window:])) if len(amounts[-window:]) > 1 else rolling_avg * 0.1

    forecasts: list[ForecastPoint] = []
    for i in range(1, days_ahead + 1):
        base_pred = rolling_avg + trend * i
        predicted = max(0.0, base_pred)
        forecasts.append(
            ForecastPoint(
                date=(last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
                predicted=round(predicted, 2),
                lower_bound=round(max(0, predicted - std_dev * 1.28), 2),
                upper_bound=round(predicted + std_dev * 1.28, 2),
            )
        )

    return forecasts


async def generate_forecast(db: AsyncSession, days_ahead: int = 30) -> dict:
    cache_key = f"forecast_{days_ahead}"
    if cache_key in _FORECAST_CACHE:
        cached = _FORECAST_CACHE[cache_key]
        cache_age = (datetime.now(UTC) - cached["ts"]).total_seconds()
        if cache_age < 300:
            return cached["data"]

    end = datetime.now(UTC)
    start = end - timedelta(days=min(365, days_ahead * 6))

    raw = await sale_repo.get_aggregated_sales(db, start, end, group_by="day")
    if len(raw) < 7:
        raise PredictionError("Insufficient historical data (need at least 7 days)")

    rows = [{"period": r["period"], "daily_amount": r["total_amount"]} for r in raw]
    df = pd.DataFrame(rows)

    forecast_points = await _simple_forecast(df, days_ahead)

    historical = rows[-90:] if len(rows) > 90 else rows

    result: dict = {
        "historical": historical,
        "forecast": [fp.model_dump() for fp in forecast_points],
    }

    _FORECAST_CACHE[cache_key] = {"data": result, "ts": datetime.now(UTC)}
    return result


async def generate_recommendations(db: AsyncSession) -> dict:
    end = datetime.now(UTC)
    start_full = end - timedelta(days=90)
    start_prev = end - timedelta(days=60)
    start_current = end - timedelta(days=30)

    products = await sale_repo.get_product_sales_breakdown(db, start_full, end)
    if not products:
        return {"recommendations": [], "generated_at": end.isoformat()}

    prev_totals = {}
    prev_breakdown = await sale_repo.get_product_sales_breakdown(db, start_prev, start_current)
    for p in prev_breakdown:
        prev_totals[p["product_id"]] = p["total_quantity"]

    current_totals = {}
    current_breakdown = await sale_repo.get_product_sales_breakdown(db, start_current, end)
    for p in current_breakdown:
        current_totals[p["product_id"]] = p["total_quantity"]

    all_quantities: list[float] = [p["total_quantity"] for p in products]
    global_avg = float(np.mean(all_quantities)) if all_quantities else 1.0

    recommendations: list[ProductRecommendation] = []
    for p in products:
        current_qty = current_totals.get(p["product_id"], 0)
        prev_qty = prev_totals.get(p["product_id"], 0)
        trend_pct = _compute_trend(prev_qty, current_qty)

        monthly_sales = p["total_quantity"] / 3.0
        growth_factor = 1.0 + max(-0.3, min(0.3, trend_pct / 100.0))
        forecasted = round(monthly_sales * growth_factor, 1)
        safety = 1.2
        recommended = max(1, math.ceil(forecasted * safety))

        if forecasted > global_avg * 1.5:
            urgency = "high"
        elif forecasted > global_avg * 0.5:
            urgency = "medium"
        else:
            urgency = "low"

        confidence = round(min(95.0, 60.0 + abs(trend_pct) * 1.5 + (p["sale_count"] * 0.5)), 1)

        recommendations.append(
            ProductRecommendation(
                product_id=p["product_id"],
                product_name=p["product_name"],
                avg_monthly_sales=round(monthly_sales, 1),
                trend_pct=trend_pct,
                forecasted_demand=forecasted,
                recommended_reorder=recommended,
                confidence=confidence,
                urgency=urgency,
            )
        )

    recommendations.sort(
        key=lambda r: (
            0 if r.urgency == "high" else 1 if r.urgency == "medium" else 2,
            -r.forecasted_demand,
        )
    )

    return {
        "recommendations": [r.model_dump() for r in recommendations],
        "generated_at": end.isoformat(),
    }
