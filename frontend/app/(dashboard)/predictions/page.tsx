"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { usePredictions } from "@/lib/hooks/usePredictions";
import { InventoryRecommendations } from "@/components/dashboard/inventory-recommendations";
import { ForecastChart } from "@/components/dashboard/forecast-chart";
import { InsightsPanel } from "@/components/dashboard/insights-panel";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { isAuthenticated } from "@/lib/auth";
import { Sparkles, TrendingUp, Package, BarChart3 } from "lucide-react";

export default function PredictionsPage() {
  const router = useRouter();
  const [daysAhead, setDaysAhead] = useState(30);
  const { historical, forecast, recommendations, inventoryInsight, forecastInsight, loading, error } =
    usePredictions(daysAhead);

  if (typeof window !== "undefined" && !isAuthenticated()) {
    router.push("/login");
    return null;
  }

  const totalForecasted = forecast.reduce((sum, f) => sum + f.predicted, 0);
  const avgDaily = forecast.length > 0 ? totalForecasted / forecast.length : 0;
  const growthRate =
    forecast.length > 1
      ? ((forecast[forecast.length - 1].predicted - forecast[0].predicted) /
          Math.max(1, forecast[0].predicted)) * 100
      : 0;

  const urgencyCounts = { high: 0, medium: 0, low: 0 };
  for (const r of recommendations) urgencyCounts[r.urgency]++;

  return (
    <div className="space-y-6 pb-8">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading text-2xl text-foreground" style={{ textShadow: "0 0 20px hsl(var(--gold) / 0.3)" }}>
            AI Predictions &amp; Insights
          </h1>
          <p className="mt-1 font-body text-sm text-secondary">
            Forecasts and recommendations powered by machine learning + Groq AI
          </p>
        </div>
        <select
          value={daysAhead}
          onChange={(e) => setDaysAhead(Number(e.target.value))}
          className="rounded border border-border bg-input px-4 py-2 text-sm text-foreground font-body transition-colors hover:border-gold/50 focus:border-gold focus:outline-none focus:ring-2 focus:ring-gold/20"
        >
          <option value={7}>7 days</option>
          <option value={14}>14 days</option>
          <option value={30}>30 days</option>
          <option value={60}>60 days</option>
          <option value={90}>90 days</option>
        </select>
      </div>

      {/* ── Error ── */}
      {error && (
        <div className="rounded border border-red-light/30 bg-red/10 p-4 text-sm text-red-light">{error}</div>
      )}

      {/* ── Loading ── */}
      {loading && (
        <div className="space-y-6">
          <div className="grid gap-4 md:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-28 animate-pulse rounded border border-border bg-card" />
            ))}
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="md:col-span-2 h-80 animate-pulse rounded border border-border bg-card" />
            <div className="h-80 animate-pulse rounded border border-border bg-card" />
          </div>
        </div>
      )}

      {/* ── Loaded ── */}
      {!loading && !error && (
        <>
          {/* ── KPI Row ── */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card accentColor="gold">
              <div className="px-5 py-4">
                <p className="font-heading text-sm text-secondary flex items-center gap-2">
                  <TrendingUp className="h-3.5 w-3.5 text-gold" />
                  Forecast Total
                </p>
                <p className="mt-2 font-heading text-3xl font-bold text-foreground">
                  ${(totalForecasted / 1000).toFixed(1)}k
                </p>
                <p className="mt-0.5 font-body text-xs text-secondary">next {daysAhead} days</p>
              </div>
            </Card>
            <Card accentColor="purple">
              <div className="px-5 py-4">
                <p className="font-heading text-sm text-secondary flex items-center gap-2">
                  <BarChart3 className="h-3.5 w-3.5 text-purple" />
                  Daily Avg
                </p>
                <p className="mt-2 font-heading text-3xl font-bold text-foreground">
                  ${(avgDaily / 1000).toFixed(1)}k
                </p>
                <p className="mt-0.5 font-body text-xs text-secondary">per day</p>
              </div>
            </Card>
            <Card accentColor={growthRate >= 0 ? "green" : "red"}>
              <div className="px-5 py-4">
                <p className="font-heading text-sm text-secondary flex items-center gap-2">
                  <TrendingUp className={`h-3.5 w-3.5 ${growthRate >= 0 ? "text-green-light" : "text-red-light"}`} />
                  Growth
                </p>
                <p className="mt-2 font-heading text-3xl font-bold text-foreground">
                  {growthRate >= 0 ? "+" : ""}{growthRate.toFixed(1)}%
                </p>
                <p className="mt-0.5 font-body text-xs text-secondary">
                  {growthRate > 3 ? "strong uptrend" : growthRate > 0 ? "mild growth" : growthRate > -3 ? "mild decline" : "declining"}
                </p>
              </div>
            </Card>
            <Card accentColor="gold">
              <div className="px-5 py-4">
                <p className="font-heading text-sm text-secondary flex items-center gap-2">
                  <Package className="h-3.5 w-3.5 text-gold" />
                  Urgent Items
                </p>
                <p className="mt-2 font-heading text-3xl font-bold text-foreground">
                  {urgencyCounts.high}
                </p>
                <p className="mt-0.5 font-body text-xs text-secondary">
                  products need restock
                </p>
              </div>
            </Card>
          </div>

          {/* ── Chart + Insights ── */}
          <div className="grid gap-4 md:grid-cols-3">
            {/* Chart — 2 cols */}
            <div className="md:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Revenue Forecast</CardTitle>
                </CardHeader>
                <CardContent>
                  <ForecastChart historical={historical} forecast={forecast} height={300} />
                  <div className="mt-4 flex flex-wrap items-center gap-5 text-xs font-body text-secondary">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-6 rounded-sm bg-[hsl(var(--text-secondary))]" />
                      Real data
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="h-0.5 w-6 border-t-2 border-dashed border-gold" />
                      AI prediction
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="h-4 w-0.5 border-l border-dashed border-gold" />
                      TODAY
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
            {/* Insights — 1 col */}
            <InsightsPanel inventoryInsight={inventoryInsight} forecastInsight={forecastInsight} />
          </div>

          {/* ── Inventory Recommendations ── */}
          <InventoryRecommendations recommendations={recommendations} />
        </>
      )}
    </div>
  );
}
