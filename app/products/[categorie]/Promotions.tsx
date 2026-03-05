"use client"
import Image from "next/image"

const promotions = [
  {
    id: 101,
    badge: "-25%",
    title: { es: "Cortina roller Blackout + cortina tradicional voile texturado", en: "Traditional Blackout + Voile" },
    description: {
      es: "Cortina voile de 2 paños. Cada paño de 1,5 m de ancho x 2,10 m de alto. Cortina roller blackout de 1,5 m x 1,5 m",
      en: "2 traditional blinds up to 1.5m x 2.1m",
    },
    oldPrice: "$305.000",
    newPrice: "$260.000",
    image: '/images/products/gasa-bck.png', 
  },
  {
    id: 102,
    badge: "-30%",
    title: { es: "Roller Blackout Premium + roller Sunscreen", en: "Roller Blackout Premium + roller Sunscreen" },
    description: {
      es: "Cortina blackout premium 1,5 m x 1,5 m + cortina sunscreen 1,5 m x 1,5 m",
      en: "Premium blackout 1.5m x 1.5m + sunscreen 1.5m x 1.5m",
    },
    oldPrice: "$350.000",
    newPrice: "$245.000",
    image: '/images/products/suns-bck-roller.png',
  },
  {
    id: 103,
    badge: "-25%",
    title: { es: "Cortina tradicionales Blackout +  voile texturado", en: "Traditional Blackout + Voile" },
    description: {
      es: "2 Cortinas de 2 paños. Cada paño de 1,5 m de ancho x 2,10 m de alto",
      en: "2 traditional blinds up to 1.5m x 2.1m",
    },
    oldPrice: "$305.000",
    newPrice: "$260.000",
    image: '/images/products/trad-bck-trad-voile.jpg', 
  },
]

export default function Promotions({ lang = "es" }: { lang?: "es" | "en" }) {
  
  const getWhatsAppLink = (itemName: string) => {
    const phone = "5492494630750" 
    const message = encodeURIComponent(`Hola Andrea! Vi la oferta de *${itemName}* y quería consultarte.`)
    return `https://wa.me/${phone}?text=${message}`
  }

  return (
    <section className="py-20 bg-black" id="promotions">
      <div className="container mx-auto px-4">
        
        <h2 className="text-3xl md:text-4xl font-serif font-bold mb-12 text-[#c9a961] tracking-[0.3em] uppercase text-center">
          {lang === "es" ? "Promociones: Sets de Diseño" : "Special Offers"}
        </h2>

        <div className="grid md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          {promotions.map((promo) => (
            <div 
              key={promo.id} 
              className="group relative border border-transparent rounded-none overflow-hidden bg-black hover:border-[#c9a961]/60 transition-all duration-500 flex flex-col h-full"
            >
              {/* Badge */}
              <div className="absolute top-2 right-2 z-10 bg-[#c9a961] text-black px-3 py-1 font-bold tracking-tighter text-xs">
                {promo.badge}
              </div>

              {/* CONTENEDOR MARCO (Zinc 900) */}
              <div className="h-72 bg-zinc-900 relative overflow-hidden p-6 border-none border-[#c9a961]/10">
                <div className="relative h-full w-full overflow-hidden">
                  {/* Overlay: En móvil es transparente, en Desktop es oscuro y aclara al hover */}
              <div className="absolute inset-0 bg-transparent lg:bg-black/40 lg:group-hover:bg-transparent transition-all z-10"></div>
                  <Image
                    src={promo.image}
                    alt={promo.title[lang]}
                    fill sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    className="object-cover transition-all duration-700 
                               /* COLOR EN CELULAR, GRIS EN PC */
                                grayscale-0 lg:grayscale 
                              /* AL PASAR EL MOUSE EN PC, VUELVE EL COLOR */
                                lg:group-hover:grayscale-0 
                                opacity-100 lg:opacity-80 
                                lg:group-hover:opacity-100 
                                group-hover:scale-110"
                  />
                </div>
              </div>

              {/* CUERPO DE TEXTO (Ahora fuera del marco de la imagen) */}
              <div className="p-8 flex flex-col flex-grow">
                <h3 className="text-xl font-serif font-bold mb-12 text-[#c9a961] tracking-widest uppercase leading-tight h-14">
                  {promo.title[lang]}
                </h3>
                
                <div className="w-10 h-px bg-[#c9a961]/40 mb-4"></div>

                <p className="text-[#f5f5f5]/70 italic font-light tracking-wide mb-6 leading-relaxed flex-grow">
                  {promo.description[lang]}
                </p>
                
                <div className="flex items-baseline gap-4 mb-8">
                  <span className="text-[#f5f5f5]/40 line-through text-sm tracking-widest">
                    {promo.oldPrice}
                  </span>
                  <span className="text-2xl font-bold text-[#c9a961] tracking-tighter">
                    {promo.newPrice}
                  </span>
                </div>

                <a 
                  href={getWhatsAppLink(promo.title[lang])}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-3 bg-transparent border border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black font-bold py-4 px-6 rounded-none transition-all duration-700 ease-in-out uppercase tracking-[0.3em] text-[10px]"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.588-5.946 0-6.556 5.332-11.891 11.891-11.891 3.181 0 6.167 1.24 8.413 3.488 2.248 2.248 3.488 5.236 3.488 8.413 0 6.557-5.332 11.892-11.891 11.892-1.997 0-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.438 9.886-9.886 0-5.448-4.438-9.886-9.886-9.886-5.448 0-9.885 4.438-9.885 9.886 0 2.221.634 4.317 1.834 6.085l-1.103 4.033 4.162-1.09z"/>
                  </svg>
                  Consultar Promo
                </a>
              </div>

            </div>
          ))}
        </div>
      </div>
    </section>
  )
}