"use client";

import { useSales } from "@/lib/hooks/useSales";
import { Badge } from "@/components/ui/badge";

export function SalesTable() {
  const { sales, loading, error } = useSales(10);

  if (loading) {
    return <div className="h-32 animate-pulse rounded bg-hover" />;
  }

  if (error) {
    return (
      <div className="rounded border border-red-light/30 bg-red/10 p-4 text-sm text-red-light">
        {error}
      </div>
    );
  }

  if (sales.length === 0) {
    return (
      <div className="py-8 text-center text-sm text-secondary">
        No sales recorded yet. Start by creating a sale via the API.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-gold/30 bg-card-header">
            <th className="px-4 py-3 text-left font-heading text-xs text-secondary">
              Product
            </th>
            <th className="px-4 py-3 text-left font-heading text-xs text-secondary">
              Amount
            </th>
            <th className="px-4 py-3 text-left font-heading text-xs text-secondary">
              Quantity
            </th>
            <th className="px-4 py-3 text-left font-heading text-xs text-secondary">
              Region
            </th>
            <th className="px-4 py-3 text-left font-heading text-xs text-secondary">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {sales.map((sale, i) => (
            <tr
              key={sale.id}
              className={cn(
                "border-b border-border/50 transition-colors duration-200",
                i % 2 === 0 ? "bg-card" : "bg-table-alt",
                "hover:bg-hover"
              )}
            >
              <td className="px-4 py-3 font-body text-foreground">
                {sale.product_name}
              </td>
              <td className="px-4 py-3 font-body text-foreground">
                ${sale.amount.toLocaleString()}
              </td>
              <td className="px-4 py-3 font-body text-secondary">
                {sale.quantity}
              </td>
              <td className="px-4 py-3 font-body text-secondary">
                {sale.region || "N/A"}
              </td>
              <td className="px-4 py-3">
                <Badge variant={sale.status === "completed" ? "success" : "failed"}>
                  {sale.status.toUpperCase()}
                </Badge>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function cn(...classes: (string | undefined | false)[]) {
  return classes.filter(Boolean).join(" ");
}
