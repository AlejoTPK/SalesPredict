"use client";

import { ArrowDown, ArrowUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface KpiCardProps {
  title: string;
  value: string | number;
  change?: string;
  changePercent?: string;
  trend?: "up" | "down";
  secondaryValue?: string | number;
  secondaryChange?: string;
  secondaryTrend?: "up" | "down";
}

export function KpiCard({
  title,
  value,
  change,
  changePercent,
  trend = "up",
  secondaryValue,
  secondaryChange,
  secondaryTrend,
}: KpiCardProps) {
  const isPositive = trend === "up";
  const isSecondaryPositive = secondaryTrend === "up";

  return (
    <div className="px-5 py-4">
      <p className="font-heading text-sm text-secondary">{title}</p>
      <div className="mt-2 flex items-baseline gap-3">
        <span className="font-heading text-3xl font-bold text-foreground">{value}</span>
        {changePercent && (
          <span
            className={cn(
              "flex items-center text-sm font-medium",
              isPositive ? "text-green-light" : "text-red-light"
            )}
          >
            {isPositive ? (
              <ArrowUp className="mr-0.5 h-3.5 w-3.5" />
            ) : (
              <ArrowDown className="mr-0.5 h-3.5 w-3.5" />
            )}
            {changePercent}
          </span>
        )}
      </div>
      {change && (
        <p className="mt-1 font-body text-xs text-green-light">{change}</p>
      )}
      {secondaryValue !== undefined && (
        <div className="mt-2 flex items-baseline gap-3 pt-2 border-t border-border/50">
          <span className="font-heading text-xl text-secondary">{secondaryValue}</span>
          {secondaryChange && (
            <span
              className={cn(
                "flex items-center text-xs",
                isSecondaryPositive ? "text-green-light" : "text-red-light"
              )}
            >
              {isSecondaryPositive ? (
                <ArrowUp className="mr-0.5 h-3 w-3" />
              ) : (
                <ArrowDown className="mr-0.5 h-3 w-3" />
              )}
              {secondaryChange}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
