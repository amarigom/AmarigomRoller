export default function About() {
  return (
  <section className="py-20 md:py-24 bg-[#0a0a0a]" id="about">
    <div className="container mx-auto px-6 grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-20 items-center">
      
      {/* Lado del Texto - En Tablet ocupa 5 columnas y en PC 6 */}
      <div className="space-y-6 md:space-y-8 text-center md:text-left md:col-span-5 lg:col-span-6 order-1">
        <h2 className="text-3xl md:text-4xl font-serif text-[#c9a961] tracking-wide">
          Expertos en Ventanas
        </h2>
        <p className="text-gray-400 leading-relaxed text-base md:text-lg">
          Somos especialistas en cortinas roller sunscreen, blackout y cortinas tradicionales. 
          Con años de experiencia, transformamos espacios con elegancia y funcionalidad.
          Cada proyecto es único y trabajamos con materiales de la más alta calidad para 
          garantizar durabilidad y belleza en cada instalación.
        </p>
        
        <div className="w-20 h-px bg-[#c9a961] mx-auto md:mx-0"></div>
      </div>

      {/* Lado de la Imagen - En Tablet ocupa 7 columnas para acercarse al texto y mostrar más logo */}
      <div className="md:col-span-7 lg:col-span-6 order-2">
        <div className="border border-[#c9a961]/20 rounded-sm overflow-hidden 
          h-[400px] 
          md:h-[550px] 
          lg:h-[600px] 
          w-full relative">
          <img 
            src="/images/hero-bg.jpg" 
            alt="Showroom Amarigom Deco" 
            className="w-full h-full transition-all duration-700
              object-cover
              /* Ajuste de posición: 85% para que el logo respire y no se pegue al borde */
              object-[85%_center] 
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