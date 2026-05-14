"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { getToken } from "@/lib/auth";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { PredictionChart } from "@/components/dashboard/prediction-chart";
import { SalesTable } from "@/components/dashboard/sales-table";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface AggRecord {
  period: string;
  total_amount: number;
  total_quantity: number;
  count: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const [aggregates, setAggregates] = useState<AggRecord[]>([]);
  const [kpiLoading, setKpiLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    const start = new Date();
    start.setMonth(start.getMonth() - 6);
    const startStr = start.toISOString().slice(0, 10);
    const endStr = new Date().toISOString().slice(0, 10);

    apiClient<AggRecord[]>(
      `/api/v1/sales/aggregates/daterange?start_date=${startStr}&end_date=${endStr}&group_by=month`,
      { token }
    )
      .then(setAggregates)
      .catch(() => {})
      .finally(() => setKpiLoading(false));
  }, [router]);

  const totalRevenue = aggregates.reduce((sum, r) => sum + r.total_amount, 0);
  const totalDeals = aggregates.reduce((sum, r) => sum + r.count, 0);
  const avgDealSize = totalDeals > 0 ? totalRevenue / totalDeals : 0;

  const sorted = [...aggregates].sort((a, b) => b.period.localeCompare(a.period));
  const currentMonth = sorted[0];
  const prevMonth = sorted[1];
  const revenueChange = prevMonth?.total_amount > 0
    ? ((currentMonth?.total_amount - prevMonth.total_amount) / prevMonth.total_amount * 100).toFixed(1)
    : null;

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-2xl text-foreground">Analytics Overview</h1>

      <div className="grid gap-4 md:grid-cols-3">
        {kpiLoading ? (
          <>
            <div className="h-28 animate-pulse rounded border border-border bg-card" />
            <div className="h-28 animate-pulse rounded border border-border bg-card" />
            <div className="h-28 animate-pulse rounded border border-border bg-card" />
          </>
        ) : (
          <>
            <Card accentColor="split-gold-red">
              <KpiCard
                title="Total Revenue"
                value={`$${(totalRevenue / 1000).toFixed(1)}k`}
                changePercent={revenueChange ? `${revenueChange}%` : undefined}
                change={revenueChange && parseFloat(revenueChange) >= 0 ? `+12% last month` : `-5% last month`}
                trend={revenueChange && parseFloat(revenueChange) >= 0 ? "up" : "down"}
              />
            </Card>
            <Card accentColor="purple">
              <KpiCard
                title="Total Deals"
                value={totalDeals}
                secondaryValue={`${aggregates.length} months`}
                secondaryChange="-5% last month"
                secondaryTrend="down"
              />
            </Card>
            <Card accentColor="split-gold-brown">
              <KpiCard
                title="Avg Deal Size"
                value={`$${(avgDealSize / 1000).toFixed(1)}k`}
                change={totalDeals > 0 ? "+8% last month" : "N/A"}
                changePercent={totalDeals > 0 ? "+30%" : undefined}
                trend="up"
              />
            </Card>
          </>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Revenue Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <PredictionChart data={aggregates} type="line" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Deals by Month</CardTitle>
          </CardHeader>
          <CardContent>
            <PredictionChart data={aggregates} type="bar" />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <SalesTable />
        </CardContent>
      </Card>
    </div>
  );
}
