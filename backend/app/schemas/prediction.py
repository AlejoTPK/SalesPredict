from pydantic import BaseModel


class ForecastPoint(BaseModel):
    date: str
    predicted: float
    lower_bound: float
    upper_bound: float


class PredictionResponse(BaseModel):
    historical: list[dict]
    forecast: list[ForecastPoint]


class ProductRecommendation(BaseModel):
    product_id: str
    product_name: str
    avg_monthly_sales: float
    trend_pct: float
    forecasted_demand: float
    recommended_reorder: int
    confidence: float
    urgency: str  # "high", "medium", "low"


class RecommendationsResponse(BaseModel):
    recommendations: list[ProductRecommendation]
    generated_at: str
