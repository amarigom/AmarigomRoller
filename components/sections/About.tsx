export default function About() {
  return (
    <section className="py-20 md:py-24 bg-[#0a0a0a]" id="about">
      <div className="container mx-auto px-6 grid md:grid-cols-2 gap-12 md:gap-16 items-center">
        
        {/* Lado del Texto - En móvil se centra el texto para mejor lectura */}
        <div className="space-y-6 md:space-y-8 text-center md:text-left">
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

        {/* Lado de la Imagen */}
        <div className="border border-[#c9a961]/20 rounded-sm overflow-hidden h-[350px] md:h-[500px] w-full">
          <img 
            src="/images/hero-bg.jpg" 
            alt="Showroom Amarigom Deco" 
            className="w-full h-full object-cover transition-all duration-700
      
      
      object-right       
      lg:object-center  
      
      grayscale-0       
      lg:grayscale      
      lg:hover:grayscale-0"
            /* object-center: Asegura que la imagen esté centrada.
               grayscale-0: Color total en móvil.
               lg:grayscale: Blanco y negro solo en computadoras.
            */
          />
        </div>
      </div>
    </section>
  )
}