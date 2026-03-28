"use client"

import { useState, useMemo, useEffect } from "react"
import { Calculator, Scissors, Check, Loader2, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"
import type { RecipeComponent, RecipeItem } from "@/lib/types/recipe"

interface CuttingCalculatorProps {
  selectedProductId: number | null;
  recipe: RecipeItem[];
  onRefreshInventory: () => void;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function CuttingCalculator({ 
  selectedProductId, 
  recipe,
  onRefreshInventory 
}: CuttingCalculatorProps) {
  
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [explosion, setExplosion] = useState<RecipeComponent[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)

  // Acción: Calcular explosión basada únicamente en medidas e ID
  const calcularReceta = async () => {
    if (!windowWidth || !windowHeight || !selectedProductId) return;
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/test-recipe/${selectedProductId}?w=${windowWidth}&h=${windowHeight}`)
      if (!response.ok) throw new Error();
      
      const data = await response.json()
      if (data.status === "success") {
        setExplosion(data.explosion)
      }
    } catch (error) {
      setExplosion(null)
    } finally {
      setLoading(false)
    }
  }

  // Debounce para evitar saturar Flask mientras escribís medidas
  useEffect(() => {
    const timer = setTimeout(() => {
      calcularReceta()
    }, 600)
    return () => clearTimeout(timer)
  }, [windowWidth, windowHeight, selectedProductId])

  const totalCost = useMemo(() => 
    explosion?.reduce((acc, item) => acc + item.costo_parcial, 0) || 0
  , [explosion])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      {/* Columna Izquierda: Inputs de Medidas */}
      <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-6 flex flex-col gap-6 shadow-2xl">
        <h3 className="text-[#c9a961] font-serif text-lg flex items-center gap-2">
          <Calculator size={18} /> Dimensiones Finales
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-[10px] text-[#6b6560] uppercase ml-1">Ancho (cm)</label>
            <input
              type="number"
              value={windowWidth}
              onChange={(e) => setWindowWidth(e.target.value)}
              className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
              placeholder="0.00"
            />
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-[#6b6560] uppercase ml-1">Alto (cm)</label>
            <input
              type="number"
              value={windowHeight}
              onChange={(e) => setWindowHeight(e.target.value)}
              className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
              placeholder="0.00"
            />
          </div>
        </div>

        <button
          disabled={!explosion || loading || confirmed}
          className={cn(
            "w-full py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2 mt-auto shadow-lg",
            confirmed ? "bg-green-600 text-white" : "bg-[#c9a961] text-black hover:bg-[#d4b574] disabled:opacity-20"
          )}
        >
          {loading ? <Loader2 className="animate-spin" size={20} /> : confirmed ? <Check size={20} /> : <Scissors size={20} />}
          <span>{confirmed ? "Stock Actualizado" : "Confirmar Producción"}</span>
        </button>
      </div>
      
      {/* BANNER DE OPTIMIZACIÓN - Solo para el vendedor */}
      {explosion && explosion.some(item => item.metodo === "RETAZO") && (
        <div className="mb-6 animate-in fade-in slide-in-from-top-2 duration-500">
          <div className="bg-[#c9a961]/10 border border-[#c9a961]/40 rounded-xl p-4 flex items-center gap-4 shadow-sm">
            <div className="bg-[#c9a961] p-2 rounded-full shadow-lg">
              <Sparkles size={18} className="text-black" />
            </div>
            <div>
              <h4 className="text-[#c9a961] font-bold text-sm tracking-tight uppercase">
                ¡Optimización Disponible!
              </h4>
              <p className="text-[#f5f0e8]/80 text-xs">
                Detectado <span className="text-[#c9a961] font-bold underline">retazo disponible</span> en el taller que cubre las medidas solicitadas: <strong>{` ${explosion.find(item => item.metodo === "RETAZO")?.medida_corte} `}</strong>.
              </p>
              
            </div>
            
          </div>
        </div>
      )}

      {/* Columna Derecha: Desglose de Materiales */}
      <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-6 flex flex-col shadow-2xl">
        <h3 className="text-[#6b6560] font-serif text-lg mb-4 flex justify-between items-center">
          Desglose de Materiales
          {loading && <Loader2 size={16} className="animate-spin text-[#c9a961]" />}
        </h3>
        
        <div className="flex-1 space-y-3 min-h-[250px]">
          {explosion ? (
            explosion.map((item, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-black/40 border border-[#2a2520] rounded-lg">
                <div>
                  <p className="text-white text-sm font-bold">{item.componente}</p>
                  <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Corte: {item.medida_corte}</p>
                </div>
                <div className="text-right">
                  <p className="text-[#c9a961] font-mono text-sm">{item.consumo_m_o_m2}</p>
                  <p className="text-[10px] text-[#6b6560] font-bold">${item.costo_parcial.toFixed(2)}</p>
                </div>
              </div>
            ))
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-[#2a2520] border-2 border-dashed border-[#1a1a1a] rounded-xl p-10">
              <Calculator size={40} className="mb-2 opacity-10" />
              <p className="text-sm italic">Cargando datos de receta...</p>
            </div>
          )}
        </div>

        {explosion && (
          <div className="mt-6 pt-4 border-t border-[#2a2520] flex justify-between items-end">
            <div>
              <p className="text-[9px] text-[#6b6560] uppercase tracking-widest mb-1">Costo Total</p>
              <p className="text-2xl text-white font-serif">${totalCost.toLocaleString('es-AR')}</p>
            </div>
            <div className="text-right">
              <p className="text-[9px] text-[#6b6560] uppercase mb-1 font-bold">PVP Sugerido (40%)</p>
              <p className="text-xl text-[#c9a961] font-bold">${(totalCost / 0.6).toLocaleString('es-AR', { maximumFractionDigits: 0 })}</p>
            </div>
          </div>
        )}
      </div>
    </div> 
  );
}