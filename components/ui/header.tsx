"use client" // Esto permite que los botones funcionen

import Link from "next/link"

export default function Header() {
  return (
    <header className="header sticky top-0 z-50 bg-[#0a0a0a]/90 backdrop-blur-md border-b border-[#c9a961]/20 py-4">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between">
          
          {/* Logo */}
          <div className="logo">
            <h1 className="text-[#c9a961] text-2xl font-serif font-bold tracking-widest">
              AMARIGOM DECO
            </h1>
          </div>
          
          {/* Navegación Desktop */}
          <nav className="hidden md:flex space-x-8 text-sm uppercase tracking-wider text-[#c4c4b8]">
            <Link href="#about" className="hover:text-[#c9a961] transition-colors">Nosotros</Link>
            <Link href="#products" className="hover:text-[#c9a961] transition-colors">Productos</Link>
            <Link href="#gallery" className="hover:text-[#c9a961] transition-colors">Galería</Link>
            <Link href="#contact" className="hover:text-[#c9a961] transition-colors">Contacto</Link>
          </nav>
          
          {/* Acciones (Idioma, Redes, Carrito) */}
          <div className="flex items-center space-x-5">
            
            {/* Redes Sociales */}
            <div className="flex space-x-4 border-r border-gray-700 pr-4">
              <a href="https://wa.me/5492494630750" target="_blank" className="text-[#c4c4b8] hover:text-[#c9a961]">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                </svg>
              </a>
              <a href="https://instagram.com/amarigom/" target="_blank" className="text-[#c4c4b8] hover:text-[#c9a961]">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                </svg>
              </a>
            </div>

            {/* Carrito */}
            <button className="relative text-[#c9a961] p-2 hover:bg-white/5 rounded-full transition-all">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              <span className="absolute top-0 right-0 bg-white text-black text-[10px] font-bold px-1.5 py-0.5 rounded-full border border-black">
                0
              </span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}