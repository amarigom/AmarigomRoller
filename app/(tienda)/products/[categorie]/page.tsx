import Link from 'next/link'
import { notFound } from 'next/navigation'

const productDetails = {
  blackout: {
    title: "Cortinas Blackout",
    items: [
      { name: "Blackout Base", desc: "Vinílico tricapa, bloqueo 100% luz y aislante térmico." },
      { name: "Blackout Premium", desc: "Textura textil elegante con la misma capacidad de bloqueo." }
    ]
  },
  tradicional: {
    title: "Cortinas Tradicionales",
    items: [
      { name: "Con Visillo", desc: "Doble cortina para privacidad y luz suave." },
      { name: "Con Barral o Riel", desc: "Sistemas clásicos reforzados." },
      { name: "Cortinas Romanas", desc: "Plegado horizontal estético y funcional." }
    ]
  },
  sunscreen: {
    title: "Cortinas Sunscreen",
    items: [
      { name: "Sunscreen 5%", desc: "Equilibrio perfecto entre visión al exterior y privacidad." },
      { name: "Sunscreen 1%", desc: "Trama más cerrada para mayor protección solar y térmica." }
    ]
  }
}

export default async function CategoryPage({ 
  params 
}: { 
  params: Promise<{ categorie: string }> 
}) {
  
  const resolvedParams = await params;
  const slug = resolvedParams.categorie;
  
  const category = productDetails[slug as keyof typeof productDetails]

  if (!category) return notFound()

  const getWhatsAppLink = (itemName: string) => {
    const phone = "5492494630750" 
    const message = encodeURIComponent(`Hola Andrea! Vi en la web la cortina *${itemName}* y quería pedirte un presupuesto.`)
    return `https://wa.me/${phone}?text=${message}`
  }

  return (
    <main className="bg-black min-h-screen text-[#f5f5f5] p-6 md:p-12">
      <div className="max-w-5xl mx-auto">
        {/* Link de volver con estilo hueso sutil */}
        <Link href="/" className="text-[#f5f5f5]/50 hover:text-[#c9a961] mb-12 inline-block transition-colors uppercase tracking-[0.2em] text-xs">
          ← Volver al Inicio
        </Link>
        
        {/* Título principal con la estética Amarigom */}
        <h1 className="text-4xl md:text-5xl font-serif font-bold mb-10 text-[#c9a961] tracking-[0.2em] uppercase text-center md:text-left">
          {category.title}
        </h1>

        <div className="grid md:grid-cols-2 gap-10">
          {category.items.map((item, index) => (
            <div 
              key={index} 
              className="bg-black p-8 rounded-none border border-[#c9a961]/30 flex flex-col justify-between hover:border-[#c9a961]/60 transition-colors duration-500"
            >
              <div className="mb-8">
                {/* Nombre en Dorado y fuente Serif */}
                <h3 className="text-2xl font-serif font-bold mb-4 text-[#c9a961] tracking-widest uppercase">
                  {item.name}
                </h3>
                <div className="w-12 h-px bg-[#c9a961]/40 mb-5"></div>
                {/* Descripción en color Hueso */}
                
                <p className="text-[#f5f5f5]/80 font- italic leading-relaxed text-base md:text-lg font-light tracking-wide">
                  {item.desc}
                </p>
              </div>
              
              {/* Botón Invertido (Negro -> Dorado) con bordes cuadrados */}
              <a 
                href={getWhatsAppLink(item.name)}
                target="_blank"
                rel="noopener noreferrer"
                //class="w-16 h-16 bg-zinc-900 border border-[#c9a961]/20 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:border-[#c9a961]/50 transition-colors"
                className="inline-flex items-center justify-center gap-3 bg-transparent border border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black font-bold py-4 px-6 rounded-none transition-all duration-700 ease-in-out active:bg-black active:text-[#c9a961] uppercase tracking-[0.3em] text-[10px]"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.588-5.946 0-6.556 5.332-11.891 11.891-11.891 3.181 0 6.167 1.24 8.413 3.488 2.248 2.248 3.488 5.236 3.488 8.413 0 6.557-5.332 11.892-11.891 11.892-1.997 0-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.438 9.886-9.886 0-5.448-4.438-9.886-9.886-9.886-5.448 0-9.885 4.438-9.885 9.886 0 2.221.634 4.317 1.834 6.085l-1.103 4.033 4.162-1.09z"/>
                </svg>
                Consultar Presupuesto
              </a>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}