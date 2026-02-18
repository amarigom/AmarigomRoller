/**
 * Image Assets Configuration
 *
 * Centralized image management for the application.
 * All images are stored in /public/images/ directory.
 *
 * Usage:
 * import { IMAGES } from '@/lib/constants/images'
 * <img src={IMAGES.hero.businessCard || "/placeholder.svg"} alt="..." />
 */

export const IMAGES = {
  // Hero Section
  hero: {
    businessCard:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Sin%20t%C3%ADtulo-tD6xG5aYBAKCDFdKG5pt99uPe9g44H.png",
  },

  // Product Images - Real installations
  products: {
    sunscreenLiving:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/secreen1-3G1WsExUUhg8ACE83sXBOtzLSiTPrL.jpg",
    curtainDetail:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/interior-2570933__340-Xj24eVTZ3Lu3DC0Re96km64bqSYP4d.jpg",
    blackoutMinimalist:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen4-27bQZ2wWpBcEifyEnnn0mICyookymo.jpg",
    sunscreenWhiteRoom:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen3-hbIF5cymViK7zlgZtHCbX47yUMRQV3.jpg",
    sunscreenFullWindow:
      "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen5-QAYn3KTtQtIqLwX8uEaLgiNW2Jz1CF.jpg",
  },

  // Gallery Images
  gallery: [
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/secreen1-3G1WsExUUhg8ACE83sXBOtzLSiTPrL.jpg",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/interior-2570933__340-Xj24eVTZ3Lu3DC0Re96km64bqSYP4d.jpg",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen4-27bQZ2wWpBcEifyEnnn0mICyookymo.jpg",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen3-hbIF5cymViK7zlgZtHCbX47yUMRQV3.jpg",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/screen5-QAYn3KTtQtIqLwX8uEaLgiNW2Jz1CF.jpg",
  ],

  // Placeholder for future images
  // Add new images here as you expand the site
  // Example:
  // newProduct: '/images/new-product.jpg',
} as const

/**
 * Image Alt Text Configuration
 * Provides accessible alt text for all images
 */
export const IMAGE_ALT = {
  hero: {
    businessCard: "AMARIGOM DECO - Cortinas Roller Blackout y Sunscreen",
  },
  products: {
    sunscreenLiving: "Cortina roller sunscreen en sala de estar con luz natural",
    curtainDetail: "Detalle de tela de cortina con luz natural",
    blackoutMinimalist: "Cortina roller blackout en habitación minimalista",
    sunscreenWhiteRoom: "Cortina roller sunscreen en habitación blanca",
    sunscreenFullWindow: "Cortina roller sunscreen en ventana completa",
  },
} as const
