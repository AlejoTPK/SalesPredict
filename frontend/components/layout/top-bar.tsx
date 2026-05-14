"use client";

import { useRouter } from "next/navigation";
import { LogOut, User, Bell, Star, Settings } from "lucide-react";
import { removeToken } from "@/lib/auth";

export function TopBar() {
  const router = useRouter();

  const handleLogout = () => {
    removeToken();
    router.push("/");
  };

  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-sidebar px-5">
      <div className="flex items-center gap-4">
        <span className="font-heading text-lg text-gold" style={{ textShadow: "0 0 20px hsl(var(--gold) / 0.4)" }}>
          SalesPredict
        </span>
        <span className="rounded bg-card px-3 py-1 text-sm text-secondary font-body">
          Dashboard
        </span>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-sm text-secondary">
          <div className="h-8 w-8 rounded-full bg-gold/20 border border-gold/30 flex items-center justify-center">
            <User className="h-4 w-4 text-gold" />
          </div>
          <span className="font-body text-sm text-secondary">Admin</span>
          <div className="h-2 w-2 rounded-full bg-green-light ml-1" />
        </div>
        <button className="rounded p-1.5 text-secondary hover:text-foreground hover:bg-hover transition-colors">
          <Bell className="h-4 w-4" />
        </button>
        <button className="rounded p-1.5 text-secondary hover:text-foreground hover:bg-hover transition-colors">
          <Star className="h-4 w-4" />
        </button>
        <button
          onClick={handleLogout}
          className="rounded p-1.5 text-secondary hover:text-foreground hover:bg-hover transition-colors"
        >
          <Settings className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}
