"use client";

import React,{ useEffect, useState } from 'react';

export default function Home() {
  const [translations, setTranslations] = useState<any>(null);
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const galleryImages = [
  '/images/gallery/img1.jpg', '/images/gallery/img2.jpg', '/images/gallery/img3.jpg',
  '/images/gallery/img4.jpg', '/images/gallery/img5.jpg', '/images/gallery/img6.jpg',
  '/images/gallery/img7.jpg', '/images/gallery/img8.jpg', '/images/gallery/img9.jpg',
  '/images/gallery/img10.jpg'
];

const nextSlide = () => {
  setCurrentIndex((prev) => (prev === galleryImages.length - 1 ? 0 : prev + 1));
};

const prevSlide = () => {
  setCurrentIndex((prev) => (prev === 0 ? galleryImages.length - 1 : prev - 1));
};

const [formData, setFormData] = useState({
  email: '',
  width: '',
  height: '',
  fabric_type: 'blackout',
  color: '',
  quality: 'premium',
  observations: ''
});

const [message, setMessage] = useState({ text: '', type: '' });
const [enviando, setEnviando] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setEnviando(true);
  
  // Limpiamos mensajes previos
  setMessage({ text: '', type: '' });

  try {
    const response = await fetch('https://amarigomroller-backend-test.onrender.com/api/presupuesto', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...formData,
        color: formData.color || 'No especificado',
        observations: formData.observations || 'Ninguna'
      }),
    });

    const data = await response.json();

    if (data.status === 'success') {
      setMessage({ text: "¡Presupuesto enviado con éxito!", type: 'success' });
      // Aquí podrías resetear el form si quieres
    } else {
      setMessage({ text: data.message || "Error al enviar", type: 'error' });
    }
  } catch (error) {
    setMessage({ text: "Error de conexión con el servidor", type: 'error' });
  } finally {
    setEnviando(false);
    // Ocultar mensaje después de 5 segundos (como tu código original)
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  }
};

  useEffect(() => {
    // Le pedimos los datos a nuestro Flask
    fetch('http://127.0.0.1:5000/')
      .then(res => res.json())
      .then(data => {
        // Guardamos las traducciones que vienen de Python
        setTranslations(data.translations);
      })
      .catch(err => console.error("Error conectando con Python:", err));
  }, []);

useEffect(() => {
  const timer = setInterval(() => {
    nextSlide(); // Esto hará que pase a la siguiente foto cada 5 segundos
  }, 5000);

  return () => clearInterval(timer); // Limpieza para que no se vuelva loco al salir de la página
}, [currentIndex]); // Se reinicia cada vez que cambias de imagen

  if (!translations) {
    return (
      <div className="flex h-screen bg-black items-center justify-center">
        <p className="text-[#c9a961] font-serif animate-pulse tracking-[0.3em] uppercase">
          Amarigom Deco
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-black text-white selection:bg-[#c9a961] selection:text-black">
      
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* Imagen de fondo  */}
        <div className="absolute inset-0 bg-[url('/images/hero-bg.jpg')] bg-cover bg-center opacity-90"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 to-black"></div>
        
        <div className="container relative z-10 text-center px-4">
          <h1 className="text-5xl md:text-8xl font-serif text-[#c9a961] mb-6 tracking-tighter">
            AMARIGOM DECO
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-2xl mx-auto mb-10 font-light uppercase tracking-[0.2em]">
            Cortinas de Diseño & Ambientes Exclusivos
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <a href="#quote" className="bg-[#c9a961] text-black px-10 py-4 font-bold uppercase tracking-widest hover:bg-white transition-all">
              Solicitar Presupuesto
            </a>
            <a href="#products" className="border border-[#c9a961] text-[#c9a961] px-10 py-4 font-bold uppercase tracking-widest hover:bg-[#c9a961] hover:text-black transition-all">
              Ver Colecciones
            </a>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-24 bg-[#0a0a0a]" id="about">
        <div className="container mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <h2 className="text-4xl font-serif text-[#c9a961]">Expertos en Ventanas</h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              Somos especialistas en cortinas roller sunscreen, blackout y cortinas tradicionales. 
              Con años de experiencia, transformamos espacios con elegancia y funcionalidad.
              Cada proyecto es único y trabajamos con materiales de la más alta calidad para 
              garantizar durabilidad y belleza en cada instalación.
            </p>
          </div>
          <div className="border border-[#c9a961]/20 rounded-sm overflow-hidden h-[500px]">
            <img 
              src="images/hero-bg.jpg" 
              alt="Showroom" 
              className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 "
            />
          </div>
        </div>
      </section>

      {/* Product Placeholder (Donde actuará tu product.py luego) */}
      <section className="py-24 bg-black" id="products">
        <div className="container mx-auto px-6 text-center mb-16">
          <h2 className="text-4xl font-serif text-[#c9a961] mb-4 tracking-widest">NUESTROS PRODUCTOS</h2>
          <div className="w-24 h-px bg-[#c9a961] mx-auto"></div>
        </div>
        
        <div className="container mx-auto px-6 grid md:grid-cols-3 gap-12">
          {[
            {nombre:'Sunscreen',
              img:'images/products/sunscreen.jpg',
              desc:'descripcion1'
            },
             {nombre:'Blackout',
              img:'images/products/blackout.jpg',
              desc:'descripcion2'},
             {nombre:'Tradicional',
              img:'images/products/traditional.jpg',
              desc:'descripcion3'}
            
            ].map((producto) => (
            <div key={producto.nombre} className="group border border-white/5 p-4 hover:border-[#c9a961]/50 transition-all">
              <div className="h-80 bg-zinc-900 mb-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-[#c9a961]/10 group-hover:bg-transparent transition-all"></div>
                <img 
                  src={producto.img} 
                  alt={producto.nombre}
                  className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700"
                />
                <p className="flex items-center justify-center h-full text-zinc-700 font-serif italic text-2xl">{producto.nombre}</p>
              </div>
              <h3 className="text-[#c9a961] text-xl font-serif mb-2 tracking-widest uppercase">{producto.nombre}</h3>
              <p className="text-gray-500 text-sm mb-6 uppercase tracking-wider italic">{producto.desc}</p>
              <button className="w-full border border-white/20 py-3 text-xs tracking-[0.3em] uppercase hover:bg-white hover:text-black transition-all">
                Explorar
              </button>
            </div>
          ))}
        </div>
      </section>

   <section className="py-24 bg-[#0a0a0a]" id="gallery">
  <div className="container mx-auto px-6">
    <h2 className="text-3xl font-serif text-[#c9a961] mb-12 text-center tracking-widest uppercase">Galería de Instalaciones</h2>
    
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
        className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="rotate-0">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>

      {/* Flecha Derecha */}
      <button 
        onClick={nextSlide}
        className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full"
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
<section className="py-24 bg-black border-t border-white/5" id="presupuesto">
  <div className="container mx-auto px-6 max-w-4xl">
    <div className="text-center mb-16">
      <h2 className="text-[#c9a961] text-3xl font-serif uppercase tracking-[0.3em] mb-4">Cotización Online</h2>
      <p className="text-gray-500 italic tracking-widest text-sm">Ingresá las medidas de tus aberturas</p>
    </div>

   <form className="space-y-6" onSubmit={handleSubmit}>
  <div 
    className="grid grid-cols-1 md:grid-cols-2 gap-6">
    {/* Email */}
    <input 
      type="email" placeholder="Tu Email" required
      className="bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all"
      onChange={(e) => setFormData({...formData, email: e.target.value})}
    />
    {/* Color */}
    <input 
      type="text" placeholder="Color deseado (opcional)"
      className="bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all"
      onChange={(e) => setFormData({...formData, color: e.target.value})}
    />
  </div>

  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
    <input type="number" placeholder="Ancho" className="bg-zinc-900 p-3 text-center outline-none hover:scale-[1.05] transition-all" onChange={(e) => setFormData({...formData, width: e.target.value})}/>
    <input type="number" placeholder="Alto" className="bg-zinc-900 p-3 text-center outline-none hover:scale-[1.05] transition-all" onChange={(e) => setFormData({...formData, height: e.target.value})}/>
    
    <select className="bg-zinc-900 p-3 outline-none" onChange={(e) => setFormData({...formData, fabric_type: e.target.value})}>
      <option value="blackout">Blackout</option>
      <option value="sunscreen">Sunscreen</option>
      <option value="tradicional">Tradicional</option>
    </select>

    <select className="bg-zinc-900 p-3 outline-none" onChange={(e) => setFormData({...formData, quality: e.target.value})}>
      <option value="premium">Premium</option>
      <option value="estandar">Estandar</option>
      <option value="superior">Superior</option>
    </select>
  </div>

  <textarea 
    placeholder="Observaciones" 
    className="w-full bg-zinc-900 p-3 h-24 outline-none hover:border-[#c9a961]/30 border border-transparent transition-all"
    onChange={(e) => setFormData({...formData, observations: e.target.value})}
  />

  {/* Mensaje en color HUESO */}
  <div className="h-4 text-center">
    {message.text && (
      <p className="text-[#f5f5dc] text-xs uppercase tracking-[0.2em] animate-fade-in">
        {message.text}
      </p>
    )}
  </div>

  <button 
  type="submit" 
  disabled={enviando} // Evita múltiples clics
  className={`
    w-full py-4 uppercase tracking-[0.5em] text-[10px] font-bold
    transition-all duration-500 border
    ${enviando 
      ? 'bg-zinc-800 border-zinc-700 text-zinc-500 cursor-not-allowed' 
      : 'bg-transparent border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black hover:shadow-[0_0_30px_rgba(201,169,97,0.4)]'
    }
  `}
>
  {enviando ? (
    <span className="flex items-center justify-center gap-2">
      {/* Icono de carga simple (Spinner) */}
      <svg className="animate-spin h-4 w-4 text-zinc-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Procesando...
    </span>
  ) : (
    'Solicitar Presupuesto'
  )}
</button>
</form> 
  </div>
</section>


      {/* Footer */}
      <footer className="py-12 border-t border-white/5 text-center">
        <p className="text-[#c9a961] font-serif tracking-widest text-xl">AMARIGOM DECO</p>
        <p className="text-zinc-600 text-[10px] mt-4 tracking-[0.5em] uppercase">© 2026 Andrea Roller</p>
      </footer>

    </div>
  );
}