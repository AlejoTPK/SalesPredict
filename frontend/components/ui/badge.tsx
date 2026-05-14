import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "success" | "failed" | "warning" | "info";
}

export function Badge({ className, variant = "info", children, ...props }: BadgeProps) {
  const variants: Record<NonNullable<BadgeProps["variant"]>, string> = {
    success: "bg-green/25 text-green-light border-green/30",
    failed: "bg-red/25 text-red-light border-red/30",
    warning: "bg-gold/20 text-gold-light border-gold/30",
    info: "bg-purple/20 text-purple-light border-purple/30",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-0.5",
        "font-body text-xs font-medium border",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
