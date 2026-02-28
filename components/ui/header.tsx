"use client"

import { useState } from "react"
import Link from "next/link"
import { Instagram, MessageCircle, ShoppingCart, Menu, X } from "lucide-react"
import { useIsMobile } from "@/hooks/use-mobile" // Usamos tu hook

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const isMobile = useIsMobile()

  const navLinks = [
    { name: "Nosotros", href: "/#about" },
    { name: "Productos", href: "/#products" },
    { name: "Galería", href: "/#gallery" },
    { name: "Contacto", href: "/#contact" },
    { name: "Presupuesto", href: "/#presupuesto" },
  ]

  return (
    <header className="header sticky top-0 z-50 bg-[#0a0a0a]/90 backdrop-blur-md border-b border-[#c9a961]/20 py-4">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between">
          
          {/* Logo */}
          <div className="logo">
            <Link href="/">
              <h1 className="text-[#c9a961] text-xl md:text-2xl font-serif font-bold tracking-widest cursor-pointer">
                AMARIGOM DECO
              </h1>
            </Link>
          </div>
          
          {/* Navegación Desktop */}
          <nav className="hidden md:flex space-x-8 text-sm uppercase tracking-wider text-[#c4c4b8]">
            {navLinks.map((link) => (
              <Link 
                key={link.name} 
                href={link.href} 
                className="hover:text-[#c9a961] transition-colors"
              >
                {link.name}
              </Link>
            ))}
          </nav>
          
          {/* Acciones */}
          <div className="flex items-center space-x-2 md:space-x-5">
            
            {/* Redes Sociales (Ocultas en mobile muy pequeño si es necesario) */}
            <div className="hidden sm:flex space-x-4 border-r border-gray-700 pr-4">
              <a href="https://wa.me/5492494630750" target="_blank" className="text-[#c4c4b8] hover:text-[#c9a961] transition-colors">
                <MessageCircle size={20} />
              </a>
              <a href="https://instagram.com/amarigom/" target="_blank" className="text-[#c4c4b8] hover:text-[#c9a961] transition-colors">
                <Instagram size={20} />
              </a>
            </div>

            {/* Carrito */}
            <button className="relative text-[#c9a961] p-2 hover:bg-white/5 rounded-full transition-all">
              <ShoppingCart size={22} />
              <span className="absolute top-0 right-0 bg-white text-black text-[10px] font-bold px-1.5 py-0.5 rounded-full border border-black">
                0
              </span>
            </button>

            {/* Botón Menú Móvil (Solo visible en mobile) */}
            <button 
              className="md:hidden text-[#c9a961] p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>

        {/* Menú Móvil Desplegable */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-[#0a0a0a] border-b border-[#c9a961]/20 py-6 px-4 animate-in fade-in slide-in-from-top-5">
            <nav className="flex flex-col space-y-6 text-center">
              {navLinks.map((link) => (
                <Link 
                  key={link.name} 
                  href={link.href} 
                  onClick={() => setIsMenuOpen(false)}
                  className="text-[#c4c4b8] text-lg uppercase tracking-widest hover:text-[#c9a961]"
                >
                  {link.name}
                </Link>
              ))}
              <div className="flex justify-center space-x-8 pt-4 border-t border-white/5">
                <a href="https://wa.me/5492494630750" target="_blank" className="text-[#c9a961]">
                  <MessageCircle size={24} />
                </a>
                <a href="https://instagram.com/amarigom/" target="_blank" className="text-[#c9a961]">
                  <Instagram size={24} />
                </a>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}