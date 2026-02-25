"use client"

import { useState } from "react"

export default function QuoteForm() {
  // 1. Estado para los datos del formulario
  const [formData, setFormData] = useState({
    email: "",
    color: "",
    width: "",
    height: "",
    fabric_type: "blackout",
    quality: "premium",
    observations: ""
  })

  // 2. Estados para la interfaz (mensaje y carga)
  const [enviando, setEnviando] = useState(false)
  const [message, setMessage] = useState({ text: "" })

  // 3. Función para manejar el envío
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setEnviando(true)
    setMessage({ text: "" }) // Limpiamos mensajes anteriores

    try {
      const API_URL = "https://amarigomroller-backend-test.onrender.com/quote/request"; 

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok && result.success) {
        setEnviando(false);
        setMessage({ text: "Cotización enviada exitosamente. Nos contactaremos pronto." });
        
        // Opcional: Limpiar el formulario
        setFormData({
          email: "",
          color: "",
          width: "",
          height: "",
          fabric_type: "blackout",
          quality: "premium",
          observations: ""
        });
      } else {
        throw new Error(result.error || result.message || "Error en el servidor");
      }
    } catch (error) {
      setEnviando(false);
      console.error("Error al enviar:", error);
      setMessage({ text: "Error al enviar la solicitud. Intente nuevamente." });
    } finally {
      // Limpiar mensaje después de 5 segundos, pase lo que pase
      setTimeout(() => setMessage({ text: "" }), 5000);
    }
  }

  return (
    <section className="py-24 bg-black border-t border-white/5" id="presupuesto">
      <div className="container mx-auto px-6 max-w-4xl">
        <div className="text-center mb-16">
          <h2 className="text-[#c9a961] text-3xl font-serif uppercase tracking-[0.3em] mb-4">
            Cotización Online
          </h2>
          <p className="text-gray-500 italic tracking-widest text-sm">
            Ingresá las medidas de tus aberturas
          </p>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input 
              type="email" 
              placeholder="Tu Email" 
              required
              value={formData.email}
              className="bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all border border-transparent focus:border-[#c9a961]/50"
              onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
            <input 
              type="text" 
              placeholder="Color deseado (opcional)"
              value={formData.color}
              className="bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all border border-transparent focus:border-[#c9a961]/50"
              onChange={(e) => setFormData({...formData, color: e.target.value})}
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <input 
              type="number" 
              placeholder="Ancho" 
              value={formData.width}
              className="bg-zinc-900 p-3 text-center text-white outline-none hover:scale-[1.05] transition-all" 
              onChange={(e) => setFormData({...formData, width: e.target.value})}
            />
            <input 
              type="number" 
              placeholder="Alto" 
              value={formData.height}
              className="bg-zinc-900 p-3 text-center text-white outline-none hover:scale-[1.05] transition-all" 
              onChange={(e) => setFormData({...formData, height: e.target.value})}
            />
            
            <select 
              value={formData.fabric_type}
              className="bg-zinc-900 p-3 text-white outline-none cursor-pointer" 
              onChange={(e) => setFormData({...formData, fabric_type: e.target.value})}
            >
              <option value="blackout">Blackout</option>
              <option value="sunscreen">Sunscreen</option>
              <option value="tradicional">Tradicional</option>
            </select>

            <select 
              value={formData.quality}
              className="bg-zinc-900 p-3 text-white outline-none cursor-pointer" 
              onChange={(e) => setFormData({...formData, quality: e.target.value})}
            >
              <option value="premium">Premium</option>
              <option value="estandar">Estandar</option>
              <option value="superior">Superior</option>
            </select>
          </div>

          <textarea 
            placeholder="Observaciones" 
            value={formData.observations}
            className="w-full bg-zinc-900 p-3 h-24 text-white outline-none hover:border-[#c9a961]/30 border border-transparent transition-all"
            onChange={(e) => setFormData({...formData, observations: e.target.value})}
          />

          <div className="h-4 text-center">
            {message.text && (
              <p className="text-[#f5f5dc] text-xs uppercase tracking-[0.2em] animate-pulse">
                {message.text}
              </p>
            )}
          </div>

          <button 
            type="submit" 
            disabled={enviando}
            className={`
              w-full py-4 uppercase tracking-[0.5em] text-[10px] font-bold
              transition-all duration-500 border
              ${enviando 
                ? 'bg-zinc-800 border-zinc-700 text-zinc-500 cursor-not-allowed' 
                : 'bg-transparent border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black hover:shadow-[0_0_30px_rgba(201,169,97,0.4)]'
              }
            `}
          >
            {enviando ? 'Procesando...' : 'Solicitar Presupuesto'}
          </button>
        </form> 
      </div>
    </section>
  )
}