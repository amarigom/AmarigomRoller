import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format price to Argentine Peso currency
 */
export function formatPrice(price: number): string {
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
  }).format(price)
}

/**
 * Format phone number for WhatsApp link
 */
export function formatWhatsAppLink(phone: string, message?: string): string {
  const cleanPhone = phone.replace(/\D/g, "")
  const encodedMessage = message ? encodeURIComponent(message) : ""
  return `https://wa.me/${cleanPhone}${encodedMessage ? `?text=${encodedMessage}` : ""}`
}
