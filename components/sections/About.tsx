export default function About() {
  return (
    <section className="py-24 bg-[#0a0a0a]" id="about">
      <div className="container mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
        {/* Lado del Texto */}
        <div className="space-y-8">
          <h2 className="text-4xl font-serif text-[#c9a961]">
            Expertos en Ventanas
          </h2>
          <p className="text-gray-400 leading-relaxed text-lg">
            Somos especialistas en cortinas roller sunscreen, blackout y cortinas tradicionales. 
            Con años de experiencia, transformamos espacios con elegancia y funcionalidad.
            Cada proyecto es único y trabajamos con materiales de la más alta calidad para 
            garantizar durabilidad y belleza en cada instalación.
          </p>
          
          {/* Un detalle decorativo opcional: una línea dorada corta */}
          <div className="w-20 h-px bg-[#c9a961]"></div>
        </div>

        {/* Lado de la Imagen con el efecto que elegiste */}
        <div className="border border-[#c9a961]/20 rounded-sm overflow-hidden h-[500px]">
          <img 
            src="/images/hero-bg.jpg"  /* Agregué la / inicial */
            alt="Showroom" 
            className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
          />
        </div>
      </div>
    </section>
  )
}