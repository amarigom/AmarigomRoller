import Link from "next/link"

export default function Hero() {
  return (
    /* Cambiamos el fondo de #0a0a0a a un gris carbón más suave #1a1a1a */
    <section className="hero relative min-h-screen flex items-center justify-center overflow-hidden bg-[#1a1a1a]" id="home">
      
      {/* Fondo con textura: Subimos un poco la opacidad para que se vea la tela */}
      <div 
        className="hero-background absolute inset-0 bg-[url('/images/tela-screen.jpg')] bg-cover bg-center opacity-50 md:opacity-35 transition-opacity duration-1000"
        style={{
          /* Suavizamos el fundido para que la imagen ocupe más espacio visual */
          maskImage: 'radial-gradient(circle, black 40%, transparent 95%)',
          WebkitMaskImage: 'radial-gradient(circle, black 40%, transparent 95%)'
        }}
      />

      {/* Overlay: Menos opaco (opacity-60) para que la sección respire más luz */}
      <div className="hero-overlay absolute inset-0 bg-gradient-to-r from-[#1a1a1a]/80 via-transparent to-[#1a1a1a]/40" />
      
      <div className="container mx-auto px-4 relative z-10 text-center">
        {/* Título: Reducimos un poco la sombra proyectada para que sea más limpio */}
        <h1 className="hero-title text-[#c9a961] text-5xl md:text-7xl font-serif mb-6 drop-shadow-md tracking-tight">
          AMARIGOM DECO
        </h1>
        
        {/* Subtítulo: Cambiamos text-white por un blanco hueso o gris muy claro para suavizar */}
        <p className="hero-subtitle text-gray-200 text-xl md:text-2xl font-light mb-10 max-w-2xl mx-auto italic">
          CORTINAS DE DISEÑO Y AMBIENTES EXCLUSIVOS
        </p>

        <div className="hero-actions flex flex-col md:flex-row gap-5 justify-center items-center">
          {/* Botón Dorado: Un poco más grande y con sombra más suave */}
          <Link 
            href="#presupuesto" 
            className="bg-[#c9a961] text-black px-10 py-4 rounded-full font-bold uppercase tracking-[0.15em] hover:bg-[#d4b574] hover:scale-105 transition-all shadow-lg"
          >
            Solicitar Presupuesto
          </Link>
          
          {/* Botón Outline: Borde más fino y elegante */}
          <Link 
            href="#products" 
            className="border border-white/30 text-white px-10 py-4 rounded-full font-bold uppercase tracking-[0.15em] hover:bg-white/10 transition-all backdrop-blur-md"
          >
            Ver Productos
          </Link>
        </div>
      </div>

      {/* Fundido inferior hacia la siguiente sección: Muy sutil */}
      <div className="absolute bottom-0 left-0 w-full h-24 bg-gradient-to-t from-[#1a1a1a] to-transparent" />
    </section>
  )
}