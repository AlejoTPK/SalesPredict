import { Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";

interface Props {
  inventoryInsight: string;
  forecastInsight: string;
}

function InsightBlock({ title, content, accent }: { title: string; content: string; accent: string }) {
  const lines = content.split("\n").filter(Boolean);
  return (
    <div className="space-y-2">
      <h4 className="font-heading text-sm text-foreground flex items-center gap-2">
        <Sparkles className="h-3.5 w-3.5" style={{ color: accent }} />
        {title}
      </h4>
      <div className="space-y-1">
        {lines.map((line, i) => (
          <p key={i} className="font-body text-sm text-secondary leading-relaxed">
            {line}
          </p>
        ))}
      </div>
    </div>
  );
}

export function InsightsPanel({ inventoryInsight, forecastInsight }: Props) {
  return (
    <Card>
      <div className="px-5 py-4 space-y-5">
        <InsightBlock
          title="AI Inventory Analysis"
          content={inventoryInsight || "Analyzing your sales data..."}
          accent="hsl(35, 55%, 58%)"
        />
        <div className="border-t border-border/50" />
        <InsightBlock
          title="Forecast Intelligence"
          content={forecastInsight || "Crunching the numbers..."}
          accent="hsl(270, 30%, 45%)"
        />
      </div>
    </Card>
  );
}
