export default function About() {
  return (
  <section className="py-20 md:py-24 bg-[#0a0a0a]" id="about">
    {/* Cambiamos el grid para que solo sea 2 columnas en pantallas grandes (lg) */}
    <div className="container mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
      
      {/* Lado del Texto - Centrado en móvil y tablet, alineado a la izquierda en PC */}
      <div className="space-y-6 md:space-y-8 text-center lg:text-left max-w-3xl mx-auto lg:mx-0">
        <h2 className="text-3xl md:text-5xl font-serif text-[#c9a961] tracking-wide">
          Expertos en Ventanas
        </h2>
        <p className="text-gray-400 leading-relaxed text-base md:text-xl">
          Somos especialistas en cortinas roller sunscreen, blackout y cortinas tradicionales. 
          Con años de experiencia, transformamos espacios con elegancia y funcionalidad.
          Cada proyecto es único y trabajamos con materiales de la más alta calidad para 
          garantizar durabilidad y belleza en cada instalación.
        </p>
        
        <div className="w-20 h-px bg-[#c9a961] mx-auto lg:mx-0"></div>
      </div>

      {/* Lado de la Imagen - Ahora abajo en tablet, ocupando todo el ancho */}
      <div className="w-full max-w-4xl mx-auto lg:max-w-none">
        <div className="border border-[#c9a961]/20 rounded-sm overflow-hidden 
          h-[350px] 
          md:h-[500px] 
          lg:h-[600px] 
          w-full relative">
          <img 
            src="/images/hero-bg.jpg" 
            alt="Showroom Amarigom Deco" 
            className="w-full h-full transition-all duration-700
              object-cover
              /* En tablet y móvil centramos la imagen porque ya tenemos ancho de sobra */
              object-center 
              lg:object-center  
              
              grayscale-0       
              lg:grayscale      
              lg:hover:grayscale-0"
          />
        </div>
      </div>

    </div>
  </section>
)
}