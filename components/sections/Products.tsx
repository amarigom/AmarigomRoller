import Link from 'next/link';
const PRODUCTOS_DATA = [
  {
    nombre: 'Sunscreen',
    img: '/images/products/sunscreen.jpg',
    desc: 'Protección UV y visibilidad'
  },
  {
    nombre: 'Blackout',
    img: '/images/products/bk1.jpg',
    desc: 'Privacidad y oscuridad total'
  },
  {
    nombre: 'Tradicional',
    img: '/images/products/traditional.jpg',
    desc: 'Elegancia clásica en tela'
  }
];

export default function Products() {
  return (
    <section className="py-24 bg-black" id="products">
      <div className="container mx-auto px-6 text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-serif text-[#c9a961] mb-4 tracking-widest uppercase">
          Nuestros Productos
        </h2>
        <div className="w-24 h-px bg-[#c9a961] mx-auto"></div>
      </div>
      
      <div className="container mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12">
        {PRODUCTOS_DATA.map((producto) => (
          <div key={producto.nombre} className="group border border-white/5 p-4 hover:border-[#c9a961]/50 transition-all duration-500">
            <div className="h-80 bg-zinc-900 mb-6 relative overflow-hidden">
              
              {/* Overlay: En móvil es transparente, en Desktop es oscuro y aclara al hover */}
              <div className="absolute inset-0 bg-transparent lg:bg-black/40 lg:group-hover:bg-transparent transition-all z-10"></div>
              
              <img 
                src={producto.img} 
                alt={producto.nombre}
                className="w-full h-full object-cover transition-all duration-1000 
                  grayscale-0 lg:grayscale lg:group-hover:grayscale-0 lg:group-hover:scale-110"
                /* ↑ grayscale-0 por defecto (móvil), grayscale solo en computadoras (md) */
              />
            </div>

            <h3 className="text-[#c9a961] text-xl font-serif mb-2 tracking-widest uppercase">
              {producto.nombre}
            </h3>
            <p className="text-gray-500 text-sm mb-6 uppercase tracking-wider italic">
              {producto.desc}
            </p>
            
            
<Link 
             href={`/products/${producto.nombre.toLowerCase()}`} 
            className="bg-black text-white px-4 py-2 rounded"
          >
             Explorar
</Link>
          </div>
        ))}
      </div>
    </section>
  )
}