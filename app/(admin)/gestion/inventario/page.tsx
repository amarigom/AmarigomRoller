"use client"

import { useState, useEffect } from "react"
import { Plus, X, Loader2 } from "lucide-react"
import InventoryView from "@/components/dashboard/InventoryView"
import { Supply } from "@/lib/types/dashboards"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

interface Categoria {
  id: number;
  name: string;
}

export default function InventarioPage() {
  const [items, setItems] = useState<Supply[]>([])
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [loading, setLoading] = useState(true)
  const [issubmitting, setIsSubmitting] = useState(false) // Para evitar doble click
  const [showForm, setShowForm] = useState(false)
  
  const [newInsumo, setNewInsumo] = useState({
    code: "", 
    name: "", 
    metersLeft: "", 
    widthCm: "", 
    price: "", 
    categoryId: "", 
    unit: "metro"
  })

  const fetchData = async () => {
    setLoading(true)
    try {
      const [resInv, resCats] = await Promise.all([
        fetch(`${API_BASE_URL}/api/inventory`),
        fetch(`${API_BASE_URL}/api/categories`)
      ]);
      const dataInv = await resInv.json()
      const dataCats = await resCats.json()

      // MAPEO PARA CUMPLIR CON LA INTERFAZ SUPPLY Y EVITAR EL ERROR DE FECHA
      const mappedItems: Supply[] = dataInv.map((inv: any) => ({
  id: inv.id,
  code: inv.code,           // Tu JSON ya trae 'code'
  name: inv.name,           // Tu JSON ya trae 'name'
  category: inv.category,   // Tu JSON ya trae 'category'
  metersLeft: inv.metersLeft, // Tu JSON ya trae 'metersLeft'
  totalMeters: inv.totalMeters || inv.metersLeft,
  widthCm: inv.widthCm || 0,
  unit: inv.unit || "unidad",
  
  // CLAVE: En tu JSON la propiedad se llama 'price'
  pricePerMeter: inv.price || 0, 
  
  status: inv.metersLeft > 0 ? "En Stock" : "Sin Stock",
  lastUpdate: new Date()

}));
        
      setItems(mappedItems)
      setCategorias(dataCats)
    } catch (err) {
      console.error("Error en el fetch:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    const payload = {
      name: newInsumo.name,
      codigo_sku: newInsumo.code,
      categoria_id: Number(newInsumo.categoryId),
      unidad_medida: newInsumo.unit,
      precio_costo_unitario: Number(newInsumo.price),
      stock_actual: Number(newInsumo.metersLeft),
      ancho_cm: Number(newInsumo.widthCm) || 0
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/inventory`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        setShowForm(false)
        setNewInsumo({ code: "", name: "", metersLeft: "", widthCm: "", price: "", categoryId: "", unit: "metro" })
        fetchData()
      } else {
        const errorData = await response.json()
        alert("Error al guardar: " + errorData.error)
      }
    } catch (err) {
      console.error("Error de red:", err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="container mx-auto space-y-6 p-4 md:p-8">
      {/* HEADER */}
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

      {/* FORMULARIO */}
      {showForm && (
        <div className="bg-[#111111] border border-[#c9a961]/20 p-6 rounded-2xl shadow-2xl animate-in slide-in-from-top duration-300">
          <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">SKU / Código</label>
                <input 
                    placeholder="Ej: BO-01" 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl focus:border-[#c9a961] outline-none text-sm" 
                    value={newInsumo.code} 
                    onChange={e => setNewInsumo({...newInsumo, code: e.target.value})} 
                    required 
                />
            </div>
            <div className="flex flex-col gap-1 md:col-span-2">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Nombre del Insumo</label>
                <input 
                    placeholder="Nombre completo" 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl focus:border-[#c9a961] outline-none text-sm"
                    value={newInsumo.name} 
                    onChange={e => setNewInsumo({...newInsumo, name: e.target.value})} 
                    required 
                />
            </div>
            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Categoría</label>
                <select 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm outline-none focus:border-[#c9a961]"
                    value={newInsumo.categoryId} 
                    onChange={e => setNewInsumo({...newInsumo, categoryId: e.target.value})}
                    required
                >
                    <option value="">Seleccionar...</option>
                    {categorias.map(cat => (
                      <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </select>
            </div>

            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Stock Inicial</label>
                <input 
                  type="number" step="any" placeholder="0.00" 
                  className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                  value={newInsumo.metersLeft} 
                  onChange={e => setNewInsumo({...newInsumo, metersLeft: e.target.value})} 
                  required 
                />
            </div>

            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Ancho (cm)</label>
                <input 
                  type="number" step="any" placeholder="Ej: 280" 
                  className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                  value={newInsumo.widthCm} 
                  onChange={e => setNewInsumo({...newInsumo, widthCm: e.target.value})} 
                />
            </div>

            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Precio Costo</label>
                <input 
                  type="number" step="any" placeholder="0.00" 
                  className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                  value={newInsumo.price} 
                  onChange={e => setNewInsumo({...newInsumo, price: e.target.value})} 
                  required 
                />
            </div>

            <div className="flex flex-col gap-1">
                <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold">Unidad</label>
                <select 
                    className="bg-black border border-[#2a2520] p-3 text-white rounded-xl text-sm"
                    value={newInsumo.unit} 
                    onChange={e => setNewInsumo({...newInsumo, unit: e.target.value})}
                >
                    <option value="metro">Metros</option>
                    <option value="cm">Centímetros</option>
                    <option value="unidad">Unidades</option>
                </select>
            </div>
            
            <button 
              type="submit" 
              disabled={issubmitting}
              className="md:col-span-4 bg-[#c9a961] text-black py-4 font-bold hover:bg-[#d4b574] transition-all rounded-xl mt-2 shadow-lg disabled:opacity-50 flex justify-center items-center gap-2"
            >
              {issubmitting ? <Loader2 className="animate-spin" size={20} /> : "GUARDAR EN BASE DE DATOS"}
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="animate-spin text-[#c9a961] mb-4" size={32} />
          <p className="text-[#6b6560] font-serif italic">Sincronizando con Neon DB...</p>
        </div>
      ) : (
        <InventoryView supplies={items} />
      )}
    </div>
  )
}