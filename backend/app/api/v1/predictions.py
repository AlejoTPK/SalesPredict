from fastapi import APIRouter, HTTPException, Query

from app.api.deps import DbDep
from app.core.exceptions import PredictionError
from app.schemas.prediction import PredictionResponse, RecommendationsResponse
from app.services import insights_service, prediction_service

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("/")
async def get_forecast(
    db: DbDep,
    days_ahead: int = Query(default=30, ge=7, le=180),
) -> PredictionResponse:
    try:
        result = await prediction_service.generate_forecast(db, days_ahead)
        return PredictionResponse(**result)
    except PredictionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/recommendations")
async def get_recommendations(
    db: DbDep,
) -> RecommendationsResponse:
    result = await prediction_service.generate_recommendations(db)
    return RecommendationsResponse(**result)


@router.get("/insights")
async def get_insights(
    db: DbDep,
    days_ahead: int = Query(default=30, ge=7, le=180),
) -> dict:
    forecast_data = await prediction_service.generate_forecast(db, days_ahead)
    recs_data = await prediction_service.generate_recommendations(db)

    forecast_pts = forecast_data.get("forecast", [])
    historical = forecast_data.get("historical", [])
    recommendations = recs_data.get("recommendations", [])

    import asyncio

    inv_insight, fc_insight = await asyncio.gather(
        insights_service.generate_inventory_insight(recommendations),
        insights_service.generate_forecast_insight(forecast_pts, historical),
    )

    return {
        "inventory_insight": inv_insight,
        "forecast_insight": fc_insight,
    }
