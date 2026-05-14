"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isAuthenticated() && pathname !== "/login") {
      router.push("/login");
    }
  }, [mounted, router, pathname]);

  if (!mounted || (!isAuthenticated() && pathname !== "/login")) {
    return (
      <div className="flex h-screen items-center justify-center bg-[hsl(var(--bg-page))]">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gold border-t-transparent" />
      </div>
    );
  }

  return <>{children}</>;
}
