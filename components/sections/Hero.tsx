import Link from "next/link"

export default function Hero() {
  return (
    <section className="hero relative min-h-screen flex items-center justify-center overflow-hidden" id="home">
      {/* Fondo y Overlay - Estas clases deben estar en tu globals.css '/images/hero-bg.jpg' '/images/tela-screen.jpg'*/}
      <div className="hero-background absolute inset-0 bg-[url('/images/tela-screen.jpg')] bg-cover bg-center opacity-40" />
      <div className="hero-overlay absolute inset-0 bg-gradient-to-r from-black/90 via-black/20 to-transparent"  />
      
      <div className="container mx-auto px-4 relative z-10 text-center">
        <h1 className="hero-title text-[#c9a961] text-5xl md:text-7xl font-serif mb-6 drop-shadow-lg">
          AMARIGOM DECO
        </h1>
        <p className="hero-subtitle text-white text-xl md:text-2xl font-light mb-10 max-w-2xl mx-auto italic">
          CORTINAS DE DISEÑO Y AMBIENTES EXCLUSIVOS
        </p>
        <div className="hero-actions flex flex-col md:flex-row gap-4 justify-center ">
          {/* Botón Dorado (Cotizar) */}
          <Link 
            href="#presupuesto" 
            className="bg-[#c9a961] text-black px-8 py-3 rounded-full font-bold uppercase tracking-widest hover:bg-[#b39552] transition-all "
          >
            Solicitar Presupuesto
          </Link>
          
          {/* Botón Outline (Productos) */}
          <Link 
            href="#products" 
            className="border-2 border-white text-white px-8 py-3 rounded-full font-bold uppercase tracking-widest hover:bg-white hover:text-black transition-all"
          >
            Ver Productos
          </Link>
        </div>
      </div>
    </section>
  )
}