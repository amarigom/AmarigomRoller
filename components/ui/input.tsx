import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-11 w-full rounded-md border border-[#3A3A3A] bg-[#1A1A1A] px-4 py-2 text-sm text-[#F5F5F0] placeholder:text-[#8A8A7E] focus:border-[#C9A961] focus:outline-none focus:ring-2 focus:ring-[#C9A961]/20 disabled:cursor-not-allowed disabled:opacity-50 transition-all",
        className,
      )}
      ref={ref}
      {...props}
    />
  )
})
Input.displayName = "Input"

export { Input }
