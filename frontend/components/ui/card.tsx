import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  accentColor?: "gold" | "red" | "purple" | "green" | "split-gold-red" | "split-gold-brown";
}

export function Card({ className, accentColor, children, ...props }: CardProps) {
  const accentMap: Record<NonNullable<CardProps["accentColor"]>, string> = {
    gold: "bg-gold",
    red: "bg-red",
    purple: "bg-purple",
    green: "bg-green",
    "split-gold-red": "bg-gradient-to-r from-gold to-red",
    "split-gold-brown": "bg-gradient-to-r from-gold to-[#8b6914]",
  };

  return (
    <div
      className={cn(
        "rounded border border-border bg-card overflow-hidden",
        className
      )}
      {...props}
    >
      {accentColor && (
        <div className={cn("h-1.5 w-full", accentMap[accentColor])} />
      )}
      {children}
    </div>
  );
}

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardHeader({ className, children, ...props }: CardHeaderProps) {
  return (
    <div
      className={cn(
        "px-5 py-4 border-b border-border bg-card-header",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}

export function CardTitle({ className, children, ...props }: CardTitleProps) {
  return (
    <h3
      className={cn(
        "font-heading text-lg text-foreground",
        className
      )}
      {...props}
    >
      {children}
    </h3>
  );
}

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardContent({ className, children, ...props }: CardContentProps) {
  return (
    <div className={cn("p-5", className)} {...props}>
      {children}
    </div>
  );
}
