import { forwardRef, useId } from "react";
import { cn } from "@/lib/utils";

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, id, ...props }, ref) => {
    const generatedId = useId();
    const inputId = id || generatedId;

    return (
      <label htmlFor={inputId} className="flex items-center gap-2 cursor-pointer">
        <input
          ref={ref}
          type="checkbox"
          id={inputId}
          className={cn(
            "peer h-5 w-5 rounded border-2 border-border bg-input",
            "appearance-none cursor-pointer transition-all duration-200",
            "checked:bg-gold checked:border-gold",
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

Checkbox.displayName = "Checkbox";

export { Checkbox };
