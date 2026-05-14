"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Settings,
  FileText,
  Target,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/sales", label: "Reports", icon: FileText },
  { href: "/predictions", label: "Quests", icon: Target },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-60 flex-col border-r border-border bg-sidebar">
      <div className="flex h-14 items-center border-b border-border px-5">
        <span className="font-heading text-lg text-gold" style={{ textShadow: "0 0 20px hsl(var(--gold) / 0.4)" }}>
          SalesPredict
        </span>
      </div>
      <nav className="flex-1 space-y-0.5 p-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded px-3 py-2 text-sm transition-colors duration-200",
                isActive
                  ? "bg-gold/20 text-gold border border-gold/20"
                  : "text-secondary hover:bg-hover hover:text-foreground"
              )}
            >
              <Icon className="h-4 w-4" />
              <span className="font-body">{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-3 border-t border-border">
        <Link
          href="/sales"
          className="flex w-full items-center justify-center rounded bg-gold px-4 py-2 text-sm font-heading text-[hsl(var(--bg-page))] hover:bg-gold-light transition-colors duration-200"
        >
          New Report
        </Link>
      </div>
    </aside>
  );
}
