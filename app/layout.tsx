import type React from "react"
import type { Metadata } from "next"
import { Cormorant_Garamond, Inter } from "next/font/google"
import "./globals.css"
import Header from "@/components/ui/header"
import Footer from "@/components/ui/footer"
//import { LanguageProvider } from "@/contexts/LanguageContext"g
//import { CartProvider } from "@/contexts/CartContext"

import { Toaster } from "@/components/ui/toaster" // o la ruta donde esté tu componente de toast



const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  variable: "--font-cormorant",
})

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  variable: "--font-inter",
})

export const metadata: Metadata = {
  title: "AMARIGOM DECO - Cortinas Roller & Tradicionales",
  description: "Cortinas Roller Blackout y Sunscreen, Cortinas Tradicionales de alta calidad",
    
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" data-scroll-behavior="smooth"className={`${cormorant.variable} ${inter.variable} scroll-smooth`}>
      <body className="font-sans antialiased bg-black text-white">
        
          {/* El contenido crece para empujar el footer abajo si hay poco texto */}
          <main className="flex-grow">
            {children}
          </main>
        {/* Componente de Radix para las notificaciones (Toasts) */}
        <Toaster />
      </body>
    </html>
  )
}