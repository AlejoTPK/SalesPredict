"use client";

import { useSales } from "@/lib/hooks/useSales";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function SalesPage() {
  const { sales, loading, error } = useSales(50);

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-2xl text-foreground">Sales History</h1>

      {loading && <div className="h-32 animate-pulse rounded bg-hover" />}

      {error && (
        <div className="rounded border border-red-light/30 bg-red/10 p-4 text-sm text-red-light">
          {error}
        </div>
      )}

      {!loading && !error && (
        <Card>
          <CardHeader>
            <CardTitle>All Sales</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b-2 border-gold/30 bg-card-header">
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Date</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Product</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Amount</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Quantity</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Region</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Customer</th>
                    <th className="px-4 py-3 text-left font-heading text-xs text-secondary">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {sales.map((sale, i) => (
                    <tr
                      key={sale.id}
                      className={`border-b border-border/50 transition-colors duration-200 hover:bg-hover ${
                        i % 2 === 0 ? "bg-card" : "bg-table-alt"
                      }`}
                    >
                      <td className="px-4 py-3 font-spectral text-xs text-secondary">
                        {sale.sale_date ? new Date(sale.sale_date).toLocaleDateString() : "N/A"}
                      </td>
                      <td className="px-4 py-3 font-body text-foreground">{sale.product_name}</td>
                      <td className="px-4 py-3 font-body text-foreground">${sale.amount.toLocaleString()}</td>
                      <td className="px-4 py-3 font-body text-secondary">{sale.quantity}</td>
                      <td className="px-4 py-3 font-body text-secondary">{sale.region || "N/A"}</td>
                      <td className="px-4 py-3 font-body text-secondary">{sale.customer_name || "N/A"}</td>
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
          </CardContent>
        </Card>
      )}
    </div>
  );
}
