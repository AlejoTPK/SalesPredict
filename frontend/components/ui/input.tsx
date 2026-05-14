import { forwardRef, useId } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const generatedId = useId();
    const inputId = id || generatedId;

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="mb-1.5 block font-body text-xs text-secondary"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            "h-10 w-full rounded border bg-input px-3 py-2",
            "font-body text-sm text-foreground",
            "placeholder:text-muted/50",
            "transition-colors duration-200",
            "border-border hover:border-gold/50",
            "focus:border-gold focus:outline-none focus:ring-2 focus:ring-gold/20",
            "disabled:border-border/30 disabled:bg-bg-page disabled:cursor-not-allowed",
            error && "border-red-light focus:border-red-light focus:ring-red-light/20",
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-1 font-body text-xs text-red-light">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
