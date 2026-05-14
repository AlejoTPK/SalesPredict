"use client";

import { ArrowDown, ArrowUp, Package } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ProductRecommendation } from "@/lib/hooks/usePredictions";

interface Props {
  recommendations: ProductRecommendation[];
  loading?: boolean;
}

export function InventoryRecommendations({ recommendations, loading }: Props) {
  if (loading) {
    return (
      <Card accentColor="gold">
        <CardHeader>
          <CardTitle>AI Inventory Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-12 animate-pulse rounded bg-hover" />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (recommendations.length === 0) {
    return (
      <Card accentColor="gold">
        <CardHeader>
          <CardTitle>AI Inventory Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3 py-6 text-secondary">
            <Package className="h-8 w-8 opacity-40" />
            <div>
              <p className="font-heading text-foreground">No recommendations yet</p>
              <p className="font-body text-sm text-secondary">
                Add more sales data to receive AI-powered inventory suggestions.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const urgencyColors: Record<string, { badge: "success" | "warning" | "failed"; text: string }> = {
    high: { badge: "failed", text: "HIGH" },
    medium: { badge: "warning", text: "MED" },
    low: { badge: "success", text: "LOW" },
  };

  return (
    <Card accentColor="gold">
      <CardHeader>
        <CardTitle>AI Inventory Recommendations</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-gold/30 bg-card-header">
                <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Product</th>
                <th className="px-4 py-3 text-right font-heading text-xs text-secondary">Avg/Month</th>
                <th className="px-4 py-3 text-right font-heading text-xs text-secondary">Trend</th>
                <th className="px-4 py-3 text-right font-heading text-xs text-secondary">Forecast</th>
                <th className="px-4 py-3 text-right font-heading text-xs text-secondary">Buy</th>
                <th className="px-4 py-3 text-right font-heading text-xs text-secondary">Confidence</th>
                <th className="px-4 py-3 text-center font-heading text-xs text-secondary">Urgency</th>
              </tr>
            </thead>
            <tbody>
              {recommendations.map((r, i) => (
                <tr
                  key={r.product_id}
                  className={`border-b border-border/50 transition-colors duration-200 hover:bg-hover ${
                    i % 2 === 0 ? "bg-card" : "bg-table-alt"
                  }`}
                >
                  <td className="px-4 py-3 font-body font-medium text-foreground">
                    {r.product_name}
                  </td>
                  <td className="px-4 py-3 text-right font-body text-foreground">
                    {r.avg_monthly_sales.toFixed(0)} u
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span
                      className={`inline-flex items-center font-body text-xs ${
                        r.trend_pct >= 0 ? "text-green-light" : "text-red-light"
                      }`}
                    >
                      {r.trend_pct >= 0 ? (
                        <ArrowUp className="mr-0.5 h-3 w-3" />
                      ) : (
                        <ArrowDown className="mr-0.5 h-3 w-3" />
                      )}
                      {r.trend_pct >= 0 ? "+" : ""}
                      {r.trend_pct}%
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right font-body text-gold">
                    {r.forecasted_demand.toFixed(0)} u
                  </td>
                  <td className="px-4 py-3 text-right font-body font-bold text-foreground">
                    {r.recommended_reorder} u
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <div className="h-1.5 w-12 rounded-full bg-border overflow-hidden">
                        <div
                          className="h-full rounded-full bg-gold transition-all"
                          style={{ width: `${r.confidence}%` }}
                        />
                      </div>
                      <span className="font-body text-xs text-secondary w-8">
                        {r.confidence}%
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Badge variant={urgencyColors[r.urgency].badge}>
                      {urgencyColors[r.urgency].text}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
