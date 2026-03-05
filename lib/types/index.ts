/**
 * Type Definitions
 *
 * Centralized TypeScript types and interfaces for the application.
 */

export type Language = "es" | "en"

export interface Translation {
  es: string
  en: string
}

export interface QuoteFormData {
  name: string
  email: string
  phone: string
  width: string
  height: string
  fabricType: "sunscreen" | "blackout" | "traditional"
  color: string
  quality: "standard" | "premium" | "luxury"
  observations: string
}

export interface CartItem {
  productId: string
  quantity: number
}

export interface CartContextType {
  items: CartItem[]
  addItem: (productId: string, quantity?: number) => void
  removeItem: (productId: string) => void
  updateQuantity: (productId: string, quantity: number) => void
  clearCart: () => void
  totalItems: number
  totalPrice: number
}

export interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
}
