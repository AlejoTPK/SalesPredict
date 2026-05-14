"use client";

import { useState, useEffect, useCallback } from "react";
import { apiClient } from "@/lib/api-client";
import { getToken } from "@/lib/auth";

export interface Sale {
  id: string;
  amount: number;
  quantity: number;
  product_id: string;
  product_name: string;
  customer_id: string | null;
  customer_name: string | null;
  region: string | null;
  status: string;
  sale_date: string | null;
}

interface UseSalesReturn {
  sales: Sale[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useSales(limit = 20): UseSalesReturn {
  const [sales, setSales] = useState<Sale[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSales = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const token = getToken();
      const data = await apiClient<Sale[]>(
        `/api/v1/sales?limit=${limit}&offset=0`,
        { token: token || undefined }
      );
      setSales(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load sales");
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchSales();
  }, [fetchSales]);

  return { sales, loading, error, refetch: fetchSales };
}
