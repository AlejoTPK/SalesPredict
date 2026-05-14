import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", disabled, ...props }, ref) => {
    const base =
      "inline-flex items-center justify-center font-heading transition-all duration-200 cursor-pointer disabled:cursor-not-allowed disabled:opacity-40";

    const variants: Record<NonNullable<ButtonProps["variant"]>, string> = {
      primary: cn(
        "bg-gold text-[hsl(var(--bg-page))] border border-gold-light/30",
        "hover:bg-gold-light active:bg-gold-dark",
        "shadow-[0_0_12px_hsl(var(--gold)/0.2)]"
      ),
      secondary: cn(
        "bg-transparent text-gold border border-gold/40",
        "hover:bg-gold/10 active:bg-gold/20"
      ),
      ghost: cn(
        "bg-transparent text-secondary border-0",
        "hover:bg-hover"
      ),
      destructive: cn(
        "bg-red text-foreground border border-red-light/30",
        "hover:bg-red-light active:bg-red"
      ),
    };

    const sizes: Record<NonNullable<ButtonProps["size"]>, string> = {
      sm: "px-3 py-1.5 text-xs",
      md: "px-5 py-2 text-sm",
      lg: "px-7 py-2.5 text-base",
    };

    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], "rounded", className)}
        disabled={disabled}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button };
