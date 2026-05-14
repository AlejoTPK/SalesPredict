import { forwardRef, useId } from "react";
import { cn } from "@/lib/utils";

export interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
}

const Radio = forwardRef<HTMLInputElement, RadioProps>(
  ({ className, label, id, ...props }, ref) => {
    const generatedId = useId();
    const inputId = id || generatedId;

    return (
      <label htmlFor={inputId} className="flex items-center gap-2 cursor-pointer">
        <input
          ref={ref}
          type="radio"
          id={inputId}
          className={cn(
            "peer h-5 w-5 rounded-full border-2 border-border bg-input",
            "appearance-none cursor-pointer transition-all duration-200",
            "checked:border-gold checked:bg-gold checked:[background-image:radial-gradient(circle,transparent_3px,hsl(var(--bg-card))_3px)]",
            "focus:ring-2 focus:ring-gold/20 focus:outline-none",
            className
          )}
          {...props}
        />
        {label && (
          <span className="font-body text-sm text-foreground">{label}</span>
        )}
      </label>
    );
  }
);

Radio.displayName = "Radio";

export { Radio };
