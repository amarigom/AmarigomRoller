"use client"

import { useState, useEffect } from "react"
import { Plus, X, Loader2 } from "lucide-react"
import InventoryView from "@/components/dashboard/InventoryView"// Asegurate que esta ruta sea correcta
import { InventoryItem } from "@/lib/types/dashboards"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export default function InventarioPage() {
  const [items, setItems] = useState<InventoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  
  const [newInsumo, setNewInsumo] = useState({
    code: "", 
    name: "", 
    metersLeft: "", 
    widthCm: "", 
    price: "", 
    category: "Telas",
    unit: "metro"
  })

  const fetchInventory = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/inventory`)
      const data = await res.json()
      setItems(data)
    } catch (err) {
      console.error("Error en el fetch:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInventory()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload = {
      name: newInsumo.name,
      code: newInsumo.code,
      category: newInsumo.category,
      metersLeft: Number(newInsumo.metersLeft),
      widthCm: Number(newInsumo.widthCm) || 0,
      price: Number(newInsumo.price),
      unit: newInsumo.unit
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/inventory`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        setShowForm(false)
        setNewInsumo({ code: "", name: "", metersLeft: "", widthCm: "", price: "", category: "Telas", unit: "metro" })
        fetchInventory()
      } else {
        const errorData = await response.json()
        alert("Error al guardar: " + errorData.error)
      }
    } catch (err) {
      console.error("Error de red:", err)
    }
  }

  return (
    <div className="container mx-auto space-y-6 p-4 md:p-8">
      {/* HEADER DINÁMICO */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="font-serif text-3xl text-[#f5f0e8]">Gestión de Stock</h1>
          <p className="text-[#6b6560] mt-1 text-sm italic">AMARIGOM DECO - Insumos e Inventario</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="w-full md:w-auto flex items-center justify-center gap-2 bg-[#c9a961] text-[#0a0a0a] px-6 py-3 rounded-xl text-sm font-bold hover:bg-[#d4b574] transition-all shadow-lg"
        >
          {showForm ? <X size={18} /> : <Plus size={18} />}
          {showForm ? "CANCELAR" : "NUEVO INSUMO"}
        </button>
      </div>

      {/* FORMULARIO (Diseño mejorado) */}
      {showForm && (
        <div className="bg-[#111111] border border-[#c9a961]/20 p-6 rounded-2xl shadow-2xl animate-in slide-in-from-top duration-300">
          <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1">SKU / Código</label>
                <input 
                    placeholder="Ej: BO-01" 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl focus:border-[#c9a961] outline-none text-sm" 
                    value={newInsumo.code} 
                    onChange={e => setNewInsumo({...newInsumo, code: e.target.value})} 
                    required 
                />
            </div>
            <div className="flex flex-col gap-1 md:col-span-2">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1">Nombre del Insumo</label>
                <input 
                    placeholder="Nombre completo" 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl focus:border-[#c9a961] outline-none text-sm"
                    value={newInsumo.name} 
                    onChange={e => setNewInsumo({...newInsumo, name: e.target.value})} 
                    required 
                />
            </div>
            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1">Categoría</label>
                <select 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                    value={newInsumo.category} 
                    onChange={e => setNewInsumo({...newInsumo, category: e.target.value})}
                >
                    <option value="Telas">Telas</option>
                    <option value="Sistemas Roller">Sistemas Roller</option>
                    <option value="Perfiles y Tubos">Perfiles y Tubos</option>
                    <option value="Accesorios">Accesorios</option>
                </select>
            </div>
            <input 
              type="number" step="any" placeholder="Stock Inicial" 
              className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
              value={newInsumo.metersLeft} 
              onChange={e => setNewInsumo({...newInsumo, metersLeft: e.target.value})} 
              required 
            />
            <input 
              type="number" step="any" placeholder="Ancho (cm)" 
              className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
              value={newInsumo.widthCm} 
              onChange={e => setNewInsumo({...newInsumo, widthCm: e.target.value})} 
            />
            <input 
              type="number" step="any" placeholder="Precio Costo" 
              className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
              value={newInsumo.price} 
              onChange={e => setNewInsumo({...newInsumo, price: e.target.value})} 
              required 
            />
            <select 
                className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                value={newInsumo.unit} 
                onChange={e => setNewInsumo({...newInsumo, unit: e.target.value})}
            >
                <option value="metro">Metros</option>
                <option value="cm">Centímetros</option>
                <option value="unidad">Unidades</option>
            </select>
            
            <button type="submit" className="md:col-span-4 bg-[#c9a961] text-black py-4 font-bold hover:bg-[#d4b574] transition-all rounded-xl mt-2 shadow-lg">
              GUARDAR EN BASE DE DATOS
            </button>
          </form>
        </div>
      )}

      {/* AHORA SÍ: Usamos el componente visual que diseñamos */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="animate-spin text-[#c9a961] mb-4" size={32} />
          <p className="text-[#6b6560] font-serif italic">Sincronizando con Neon DB...</p>
        </div>
      ) : (
        <InventoryView items={items} />
      )}
    </div>
  )
}