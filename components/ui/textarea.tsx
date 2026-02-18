import * as React from "react"
import { cn } from "@/lib/utils"

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[100px] w-full rounded-md border border-[#3A3A3A] bg-[#1A1A1A] px-4 py-3 text-sm text-[#F5F5F0] placeholder:text-[#8A8A7E] focus:border-[#C9A961] focus:outline-none focus:ring-2 focus:ring-[#C9A961]/20 disabled:cursor-not-allowed disabled:opacity-50 transition-all resize-none",
        className,
      )}
      ref={ref}
      {...props}
    />
  )
})
Textarea.displayName = "Textarea"

export { Textarea }
