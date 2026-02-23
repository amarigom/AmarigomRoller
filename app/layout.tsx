import type React from "react"
import type { Metadata } from "next"
import { Cormorant_Garamond, Inter } from "next/font/google"
import "./globals.css"
import Header from "@/components/ui/header"
import Footer from "@/components/ui/footer"
//import { LanguageProvider } from "@/contexts/LanguageContext"g
//import { CartProvider } from "@/contexts/CartContext"

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
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" className={`${cormorant.variable} ${inter.variable}`}>
      <body className="font-sans antialiased">
        {/*<LanguageProvider>
          <CartProvider>*/}
          <Header />
            <main className="min-h-screen">
          {children}
            </main>
          <Footer />
          {/*</CartProvider>*/}
          
        
      </body>
    </html>
  )
}
