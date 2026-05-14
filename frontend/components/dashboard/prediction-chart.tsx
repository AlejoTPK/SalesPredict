"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

interface ChartDataPoint {
  period: string;
  total_amount: number;
  total_quantity?: number;
  count?: number;
}

interface PredictionChartProps {
  data?: ChartDataPoint[];
  type?: "line" | "bar";
}

export function PredictionChart({ data, type = "line" }: PredictionChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="h-[300px] w-full animate-pulse rounded bg-hover" />;
  }

  const chartData = data && data.length > 0
    ? data.map((d) => ({
        period: d.period.slice(0, 7),
        revenue: Math.round(d.total_amount),
      }))
    : (() => {
        const months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"];
        return months.map((m) => ({
          period: m,
          revenue: Math.round(Math.random() * 100000 + 50000),
        }));
      })();

  const gridColor = "hsl(var(--border) / 0.5)";
  const axisColor = "hsl(var(--text-muted))";
  const tickStyle = { fontFamily: "var(--font-body)", fontSize: 11, fill: axisColor };

  if (type === "bar") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
          <XAxis dataKey="period" stroke={axisColor} tick={tickStyle} />
          <YAxis stroke={axisColor} tick={tickStyle} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
          <RechartsTooltip
            contentStyle={{
              backgroundColor: "#1a1a2e",
              border: "1px solid hsl(var(--gold) / 0.3)",
              borderRadius: "4px",
              fontFamily: "var(--font-body)",
              fontSize: "12px",
              color: "hsl(var(--text-primary))",
              boxShadow: "0 0 12px hsl(var(--gold) / 0.15)",
            }}
            formatter={(v: number) => [`$${v.toLocaleString()}`, "Revenue"]}
            labelStyle={{ fontFamily: "var(--font-heading)", color: "hsl(var(--gold))", marginBottom: "4px" }}
            itemStyle={{ color: "hsl(var(--text-primary))" }}
          />
          <Bar dataKey="revenue" fill="hsl(var(--gold))" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
        <XAxis dataKey="period" stroke={axisColor} tick={tickStyle} />
        <YAxis stroke={axisColor} tick={tickStyle} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
        <RechartsTooltip
          contentStyle={{
            backgroundColor: "#1a1a2e",
            border: "1px solid hsl(var(--gold) / 0.3)",
            borderRadius: "4px",
            fontFamily: "var(--font-body)",
            fontSize: "12px",
            color: "hsl(var(--text-primary))",
            boxShadow: "0 0 12px hsl(var(--gold) / 0.15)",
          }}
          formatter={(v: number) => [`$${v.toLocaleString()}`, "Revenue"]}
          labelStyle={{ fontFamily: "var(--font-heading)", color: "hsl(var(--gold))", marginBottom: "4px" }}
          itemStyle={{ color: "hsl(var(--text-primary))" }}
        />
        <Line
          type="monotone"
          dataKey="revenue"
          stroke="hsl(var(--gold))"
          strokeWidth={2}
          dot={{ fill: "hsl(var(--gold))", r: 4 }}
          activeDot={{ r: 6, fill: "hsl(var(--gold))", stroke: "hsl(var(--bg-page))", strokeWidth: 2 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
