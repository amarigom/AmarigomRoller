"use client"

import { useState, useEffect } from "react"
import { Plus, X, Edit2 } from "lucide-react"

// 1. URL base dinámica: usa la variable de entorno en Vercel o nada en local (para usar el proxy)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

interface FabricRoll {
  id?: string;
  code: string;
  name: string;
  metersLeft: number;
  widthCm: number;
  pricePerMeter: number;
  category: string;
  status?: string;
}

export default function InventarioPage() {
  const [rolls, setRolls] = useState<FabricRoll[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  
  const [newRoll, setNewRoll] = useState({
    code: "", 
    name: "", 
    metersLeft: "", 
    widthCm: "", 
    pricePerMeter: "", 
    category: "blackout"
  })

  // MODIFICADO: Ahora usa la constante API_BASE_URL
  const fetchInventory = () => {
    setLoading(true)
    fetch(`${API_BASE_URL}/api/inventory`)
      .then(res => res.json())
      .then((data: FabricRoll[]) => {
        setRolls(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Error en el fetch:", err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchInventory()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const payload = {
      name: newRoll.name,
      code: newRoll.code,
      category: newRoll.category,
      metersLeft: Number(newRoll.metersLeft),
      widthCm: Number(newRoll.widthCm),
      pricePerMeter: Number(newRoll.pricePerMeter),
      status: "in_stock"
    }

    try {
      // MODIFICADO: Ahora usa la constante API_BASE_URL
      const response = await fetch(`${API_BASE_URL}/api/inventory`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        setShowForm(false)
        setNewRoll({ code: "", name: "", metersLeft: "", widthCm: "", pricePerMeter: "", category: "blackout" })
        fetchInventory()
      } else {
        const errorData = await response.json()
        console.error("Error del servidor:", errorData.error)
        alert("Error al guardar: " + errorData.error)
      }
    } catch (err) {
      console.error("Error de red:", err)
    }
  }

  // ... (el resto del return queda igual que el tuyo)
  return (
    <div className="space-y-6 p-4">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="font-serif text-3xl text-[#f5f0e8]">Inventario de Rollos</h2>
          <p className="text-[#6b6560] mt-1 text-sm">Gestioná las telas disponibles para AMARIGOM DECO</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-[#c9a961] text-[#0a0a0a] px-4 py-2 rounded-sm text-sm font-medium hover:bg-[#d4b574] transition-colors"
        >
          {showForm ? <X size={16} /> : <Plus size={16} />}
          {showForm ? "Cerrar" : "Nuevo Rollo"}
        </button>
      </div>

      {showForm && (
        <div className="bg-[#111111] border border-[#c9a961]/30 p-6 rounded-sm animate-in fade-in duration-500">
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input 
              placeholder="Código (ej: BO-01)" 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm focus:border-[#c9a961] outline-none" 
              value={newRoll.code} 
              onChange={e => setNewRoll({...newRoll, code: e.target.value})} 
              required 
            />
            <input 
              placeholder="Nombre de la tela" 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm focus:border-[#c9a961] outline-none"
              value={newRoll.name} 
              onChange={e => setNewRoll({...newRoll, name: e.target.value})} 
              required 
            />
            <select 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm"
              value={newRoll.category} 
              onChange={e => setNewRoll({...newRoll, category: e.target.value})}
            >
              <option value="blackout">Blackout</option>
              <option value="sunscreen">Sunscreen</option>
              <option value="tradicional">Tradicional</option>
            </select>
            <input 
              type="number" 
              placeholder="Metros totales" 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm"
              value={newRoll.metersLeft} 
              onChange={e => setNewRoll({...newRoll, metersLeft: e.target.value})} 
              required 
            />
            <input 
              type="number" 
              placeholder="Ancho (cm)" 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm"
              value={newRoll.widthCm} 
              onChange={e => setNewRoll({...newRoll, widthCm: e.target.value})} 
              required 
            />
            <input 
              type="number" 
              placeholder="Precio por metro" 
              className="bg-black border border-[#2a2520] p-2 text-white rounded-sm"
              value={newRoll.pricePerMeter} 
              onChange={e => setNewRoll({...newRoll, pricePerMeter: e.target.value})} 
              required 
            />
            <button type="submit" className="md:col-span-3 bg-[#c9a961] text-black p-2 font-bold hover:bg-[#d4b574] transition-all rounded-sm uppercase text-xs tracking-widest">
              GUARDAR EN STOCK
            </button>
          </form>
        </div>
      )}

      <div className="bg-[#111111] border border-[#2a2520] rounded-sm overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-[#0a0a0a] border-b border-[#2a2520]">
            <tr>
              <th className="px-6 py-4 text-[10px] font-bold text-[#6b6560] uppercase tracking-widest">Código</th>
              <th className="px-6 py-4 text-[10px] font-bold text-[#6b6560] uppercase tracking-widest">Nombre</th>
              <th className="px-6 py-4 text-[10px] font-bold text-[#6b6560] uppercase tracking-widest text-right">Stock (m)</th>
              <th className="px-6 py-4 text-[10px] font-bold text-[#6b6560] uppercase tracking-widest">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#2a2520]">
            {loading ? (
              <tr><td colSpan={4} className="px-6 py-10 text-center text-gray-500 italic">Cargando inventario...</td></tr>
            ) : rolls && rolls.length > 0 ? (
              rolls.map((roll, index) => (
                <tr key={roll.id || `roll-${index}`} className="hover:bg-white/[0.02] transition-colors group">
                  <td className="px-6 py-4 text-sm font-mono text-[#c9a961]">{roll.code}</td>
                  <td className="px-6 py-4 text-sm text-[#f5f0e8]">{roll.name}</td>
                  <td className={`px-6 py-4 text-sm text-right font-medium ${roll.metersLeft < 5 ? 'text-orange-400' : 'text-green-400'}`}>{roll.metersLeft} m</td>
                  <td className="px-6 py-4">
                    <button className="text-[#6b6560] hover:text-[#c9a961] transition-colors">
                      <Edit2 size={16} />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr><td colSpan={4} className="px-6 py-10 text-center text-gray-500 italic text-sm">No se encontraron rollos en el inventario.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}