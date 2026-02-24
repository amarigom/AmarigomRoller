"use client";

import About from '@/components/sections/About';
import Gallery from '@/components/sections/Gallery';
import Hero from '@/components/sections/Hero';
import Products from '@/components/sections/Products';
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
    fetch('https://amarigomroller-backend-test.onrender.com/')
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
      <Hero/>
      <About/>
      <Products/>
     
      
 

   
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


      

    </div>
  );
}