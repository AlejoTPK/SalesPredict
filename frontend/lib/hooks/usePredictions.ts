"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api-client";

export interface ForecastPoint {
  date: string;
  predicted: number;
  lower_bound: number;
  upper_bound: number;
}

export interface ProductRecommendation {
  product_id: string;
  product_name: string;
  avg_monthly_sales: number;
  trend_pct: number;
  forecasted_demand: number;
  recommended_reorder: number;
  confidence: number;
  urgency: "high" | "medium" | "low";
}

interface ForecastResponse {
  historical: { period: string; daily_amount: number }[];
  forecast: ForecastPoint[];
}

interface RecommendationsResponse {
  recommendations: ProductRecommendation[];
  generated_at: string;
}

interface InsightsResponse {
  inventory_insight: string;
  forecast_insight: string;
}

export function usePredictions(daysAhead = 30) {
  const [historical, setHistorical] = useState<ForecastResponse["historical"]>([]);
  const [forecast, setForecast] = useState<ForecastPoint[]>([]);
  const [recommendations, setRecommendations] = useState<ProductRecommendation[]>([]);
  const [inventoryInsight, setInventoryInsight] = useState("");
  const [forecastInsight, setForecastInsight] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all([
      apiClient<ForecastResponse>(`/api/v1/predictions/?days_ahead=${daysAhead}`).catch(() => null),
      apiClient<RecommendationsResponse>("/api/v1/predictions/recommendations").catch(() => null),
      apiClient<InsightsResponse>(`/api/v1/predictions/insights?days_ahead=${daysAhead}`).catch(() => null),
    ])
      .then(([forecastRes, recsRes, insightsRes]) => {
        if (cancelled) return;
        if (forecastRes) {
          setHistorical(forecastRes.historical);
          setForecast(forecastRes.forecast);
        }
        if (recsRes) setRecommendations(recsRes.recommendations);
        if (insightsRes) {
          setInventoryInsight(insightsRes.inventory_insight);
          setForecastInsight(insightsRes.forecast_insight);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load predictions");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [daysAhead]);

  return { historical, forecast, recommendations, inventoryInsight, forecastInsight, loading, error };
}
