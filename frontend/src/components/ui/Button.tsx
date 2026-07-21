import * as React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link" | "gradient"
  size?: "default" | "sm" | "lg" | "icon" | "xs"
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    const variants = {
      default:
        "bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-[0_4px_14px_rgba(99,102,241,0.3)] hover:shadow-[0_6px_20px_rgba(99,102,241,0.4)] hover:-translate-y-0.5 active:translate-y-0",
      gradient:
        "bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500 text-white shadow-[0_4px_14px_rgba(99,102,241,0.35)] hover:shadow-[0_6px_20px_rgba(99,102,241,0.5)] hover:-translate-y-0.5 active:translate-y-0",
      destructive:
        "bg-gradient-to-r from-red-500 to-rose-600 text-white shadow-[0_4px_14px_rgba(239,68,68,0.3)] hover:shadow-[0_6px_20px_rgba(239,68,68,0.4)] hover:-translate-y-0.5",
      outline:
        "border border-white/10 bg-white/5 text-slate-300 hover:bg-white/10 hover:text-slate-100 hover:border-white/20 backdrop-blur-sm",
      secondary:
        "bg-white/8 text-slate-200 hover:bg-white/12 hover:text-slate-100 border border-white/8",
      ghost:
        "text-slate-400 hover:bg-white/6 hover:text-slate-200",
      link:
        "text-blue-400 underline-offset-4 hover:underline hover:text-blue-300",
    }

    const sizes = {
      xs: "h-7 px-2.5 text-xs rounded-lg",
      default: "h-9 px-4 py-2 text-sm rounded-xl",
      sm: "h-8 px-3 text-sm rounded-lg",
      lg: "h-11 px-6 text-base rounded-xl",
      icon: "h-9 w-9 rounded-xl",
    }

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center whitespace-nowrap font-medium",
          "ring-offset-background transition-all duration-200",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50 focus-visible:ring-offset-2",
          "disabled:pointer-events-none disabled:opacity-40",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
