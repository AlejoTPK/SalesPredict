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
  ReferenceLine,
} from "recharts";
import type { ForecastPoint } from "@/lib/hooks/usePredictions";

interface Props {
  historical?: { period: string; daily_amount: number }[];
  forecast?: ForecastPoint[];
  height?: number;
}

export function ForecastChart({ historical, forecast, height = 320 }: Props) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  if (!mounted) {
    return <div className="w-full animate-pulse rounded bg-hover" style={{ height }} />;
  }

  const chartData: { date: string; actual?: number; predicted?: number }[] = [];

  if (historical?.length) {
    const last30 = historical.slice(-30);
    for (const h of last30) {
      chartData.push({ date: h.period.slice(0, 10), actual: h.daily_amount });
    }
  }

  const today = historical?.length
    ? historical[historical.length - 1].period.slice(0, 10)
    : new Date().toISOString().slice(0, 10);

  if (forecast?.length) {
    for (const f of forecast) {
      chartData.push({ date: f.date, predicted: f.predicted });
    }
  }

  const gridColor = "hsl(var(--border) / 0.4)";
  const axisColor = "hsl(var(--text-muted))";
  const tick = { fontFamily: "var(--font-body)", fontSize: 11, fill: axisColor };
  const tooltipBg = {
    backgroundColor: "#1a1a2e",
    border: "1px solid hsl(var(--gold) / 0.3)",
    borderRadius: "4px",
    fontFamily: "var(--font-body)",
    fontSize: "12px",
    color: "hsl(var(--text-primary))",
    boxShadow: "0 0 12px hsl(var(--gold) / 0.15)",
  };

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={chartData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
        <XAxis dataKey="date" stroke={axisColor} tick={tick} />
        <YAxis stroke={axisColor} tick={tick} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
        <RechartsTooltip
          contentStyle={tooltipBg}
          formatter={(v: number, name: string) => [
            `$${v.toLocaleString()}`,
            name === "actual" ? "Real" : "Predicho",
          ]}
          labelStyle={{ fontFamily: "var(--font-heading)", color: "hsl(var(--gold))", marginBottom: "4px" }}
        />
        <ReferenceLine
          x={today}
          stroke="hsl(var(--gold))"
          strokeWidth={1}
          strokeDasharray="4 4"
          label={{ value: "HOY", position: "top", fill: "hsl(var(--gold))", fontSize: 10, fontFamily: "var(--font-heading)" }}
        />
        <Line
          type="monotone"
          dataKey="actual"
          stroke="hsl(var(--text-secondary))"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4 }}
          name="Real"
        />
        {forecast?.length ? (
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="hsl(var(--gold))"
            strokeWidth={2.5}
            strokeDasharray="6 3"
            dot={{ r: 3, fill: "hsl(var(--gold))" }}
            activeDot={{ r: 5, fill: "hsl(var(--gold))", stroke: "#1a1a2e", strokeWidth: 2 }}
            name="Predicho"
          />
        ) : null}
      </LineChart>
    </ResponsiveContainer>
  );
}
