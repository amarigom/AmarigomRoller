"use client" 

import { useState } from "react"

export default function Gallery() {
  // 1. Definimos las imágenes 
  const galleryImages = [
    
    "/images/gallery/img1.jpg", 
    "/images/gallery/img2.jpg", 
    "/images/gallery/img3.jpg",
    "/images/gallery/img4.jpg",
    "/images/gallery/img5.jpg",
    "/images/gallery/img6.jpg",
    "/images/gallery/img7.jpg",
    "/images/gallery/img8.jpg",
    "/images/gallery/img9.jpg",
    "/images/gallery/img10.jpg"
  ]

  // 2. Lógica del carrusel
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev === galleryImages.length - 1 ? 0 : prev + 1))
  }

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev === 0 ? galleryImages.length - 1 : prev - 1))
  }

  return (
    <section className="py-24 bg-[#0a0a0a]" id="gallery">
      <div className="container mx-auto px-6">
        <h2 className="text-3xl font-serif text-[#c9a961] mb-12 text-center tracking-widest uppercase">
          Galería de Instalaciones
        </h2>
        
        <div className="relative group max-w-5xl mx-auto overflow-hidden">
          {/* Contenedor de las imágenes */}
          <div 
            className="flex transition-transform duration-700 ease-in-out" 
            style={{ transform: `translateX(-${currentIndex * 100}%)` }}
          >
            {galleryImages.map((src, index) => (
              <div key={index} className="min-w-full h-[500px] px-2">
                <img 
                  src={src} 
                  alt={`Instalación ${index + 1}`} 
                  className="w-full h-full object-cover rounded-sm border border-white/5"
                />
              </div>
            ))}
          </div>

          {/* Flecha Izquierda */}
          <button 
            onClick={prevSlide}
            className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full z-20"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>

          {/* Flecha Derecha */}
          <button 
            onClick={nextSlide}
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full z-20"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>

          {/* Puntos de navegación (Dots) */}
          <div className="flex justify-center gap-2 mt-8">
            {galleryImages.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index)}
                className={`h-1 transition-all duration-300 ${
                  currentIndex === index ? "w-8 bg-[#c9a961]" : "w-2 bg-zinc-700"
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}