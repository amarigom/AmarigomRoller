/**
 * Products Configuration
 *
 * Defines all products available in the store.
 * Each product includes pricing, descriptions, and specifications.
 */

export interface Product {
  id: string
  name: {
    es: string
    en: string
  }
  description: {
    es: string
    en: string
  }
  price: number
  originalPrice?: number
  image: string
  category: "sunscreen" | "blackout" | "traditional"
  features: {
    es: string[]
    en: string[]
  }
  inStock: boolean
  isPromo?: boolean
}

export const PRODUCTS: Product[] = [
  {
    id: "sunscreen-promo",
    name: {
      es: "Cortina Roller Sunscreen",
      en: "Sunscreen Roller Blind",
    },
    description: {
      es: "Filtra la luz solar manteniendo la visibilidad. Perfecta para salas y oficinas.",
      en: "Filters sunlight while maintaining visibility. Perfect for living rooms and offices.",
    },
    price: 12500,
    originalPrice: 15000,
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/secreen1-3G1WsExUUhg8ACE83sXBOtzLSiTPrL.jpg",
    category: "sunscreen",
    features: {
      es: ["Protección UV", "Mantiene visibilidad", "Fácil instalación", "Varios colores"],
      en: ["UV Protection", "Maintains visibility", "Easy installation", "Multiple colors"],
    },
    inStock: true,
    isPromo: true,
  },
  {
    id: "blackout-promo",
    name: {
      es: "Cortina Roller Blackout",
      en: "Blackout Roller Blind",
    },
    description: {
      es: "Bloqueo total de luz. Ideal para dormitorios y salas de cine.",
      en: "Complete light blocking. Ideal for bedrooms and home theaters.",
    },
    price: 14500,
    originalPrice: 17000,
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen4-27bQZ2wWpBcEifyEnnn0mICyookymo.jpg",
    category: "blackout",
    features: {
      es: ["Bloqueo 100% luz", "Aislamiento térmico", "Privacidad total", "Durabilidad superior"],
      en: ["100% light blocking", "Thermal insulation", "Complete privacy", "Superior durability"],
    },
    inStock: true,
    isPromo: true,
  },
  {
    id: "traditional-curtain",
    name: {
      es: "Cortina Tradicional con Barral",
      en: "Traditional Rod-Mounted Curtain",
    },
    description: {
      es: "Elegancia clásica con telas de alta calidad. Personalizable en color y diseño.",
      en: "Classic elegance with high-quality fabrics. Customizable in color and design.",
    },
    price: 18000,
    image:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/interior-2570933__340-Xj24eVTZ3Lu3DC0Re96km64bqSYP4d.jpg",
    category: "traditional",
    features: {
      es: ["Telas premium", "Diseño personalizado", "Incluye barral", "Instalación profesional"],
      en: ["Premium fabrics", "Custom design", "Includes rod", "Professional installation"],
    },
    inStock: true,
  },
]

export const getProductById = (id: string): Product | undefined => {
  return PRODUCTS.find((product) => product.id === id)
}

export const getPromoProducts = (): Product[] => {
  return PRODUCTS.filter((product) => product.isPromo)
}
