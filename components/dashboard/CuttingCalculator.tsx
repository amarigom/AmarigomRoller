"use client"

import { useState, useMemo, useEffect } from "react"
import { Calculator, Scissors, Check, Loader2, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

// 1. Usamos EXCLUSIVAMENTE los tipos externos (Single Source of Truth)
import type { Product } from "@/lib/types/product"
import type { RecipeComponent } from "@/lib/types/recipe"

interface CuttingCalculatorProps {
  products: Product[]; 
  onDiscountStock: (items: RecipeComponent[]) => void;
  productId?: number; 
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function CuttingCalculator({ 
  products = [], 
  productId, 
  onDiscountStock 
}: CuttingCalculatorProps) {
  
  // Estados
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [budget, setBudget] = useState("")
  const [explosion, setExplosion] = useState<RecipeComponent[] | null>(null)
  const [optimization, setOptimization] = useState<{mensaje: string, id: number} | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)
  
  // Sincronizamos el select con la prop si viene de afuera
  const [selectedProductId, setSelectedProductId] = useState<string>(productId?.toString() || "");

  // --- ACCIÓN: Confirmar Producción ---
  const handleConfirmProduction = async () => {
    if (!explosion || !selectedProductId) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/confirm-production`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          explosion: explosion,
          productId: selectedProductId 
        })
      });

      const data = await response.json();

      if (data.status === "success") {
        setConfirmed(true);
        onDiscountStock(explosion);
        
        setTimeout(() => {
          setConfirmed(false);
          setExplosion(null);
          setWindowWidth("");
          setWindowHeight("");
        }, 3000);
      } else {
        alert("Error: " + data.message);
      }
    } catch (error) {
      console.error("Error de conexión:", error);
    } finally {
      setLoading(false);
    }
  };

  // --- ACCIÓN: Calcular Receta (Explosión) ---
  const calcularReceta = async () => {
    if (!windowWidth || !windowHeight || !selectedProductId) return;
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/test-recipe/${selectedProductId}?w=${windowWidth}&h=${windowHeight}`)
      
      if (!response.ok) throw new Error("Error en el servidor");

      const data = await response.json()
      
      if (data.status === "success") {
        setExplosion(data.explosion)
        
        // Lógica de optimización de retazos
        const telaOpt = data.explosion.find((item: RecipeComponent) => item.metodo === "RETAZO")
        if (telaOpt && telaOpt.id_retazo) {
          setOptimization({ 
            mensaje: telaOpt.mensaje || "Retazo disponible", 
            id: telaOpt.id_retazo 
          })
        } else {
          setOptimization(null)
        }
      }
    } catch (error) {
      console.error("Error al calcular:", error)
    } finally {
      setLoading(false)
    }
  }

  // Debounce para evitar llamadas excesivas a Flask
  useEffect(() => {
    const timer = setTimeout(() => {
      if (windowWidth && windowHeight && selectedProductId) calcularReceta()
    }, 600)
    return () => clearTimeout(timer)
  }, [windowWidth, windowHeight, selectedProductId])

  // Cálculos de costos
  const totalCost = useMemo(() => {
    return explosion?.reduce((acc, item) => acc + item.costo_parcial, 0) || 0
  }, [explosion])

  const isOverBudget = useMemo(() => {
    const b = parseFloat(budget)
    return b > 0 && totalCost > b
  }, [totalCost, budget])

  return (
    <div className="flex flex-col gap-6">
      
      {/* 1. Banner de Optimización */}
      {optimization && (
        <div className="bg-[#c9a961]/10 border border-[#c9a961]/30 p-4 rounded-xl flex items-center gap-4 animate-in fade-in slide-in-from-top-2">
          <div className="bg-[#c9a961] p-2 rounded-full text-black">
            <Sparkles size={20} />
          </div>
          <div className="flex-1">
            <p className="text-[#c9a961] font-bold text-sm">¡Ahorro Detectado en el Taller!</p>
            <p className="text-[#f5f0e8] text-xs italic">{optimization.mensaje}</p>
          </div>
        </div>
      )}

      {/* 2. Selector de Producto */}
      <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-5">
        <label className="text-[10px] text-[#6b6560] uppercase ml-1 font-bold tracking-widest">
          Modelo de Cortina / Receta
        </label>
        <select
          value={selectedProductId}
          onChange={(e) => setSelectedProductId(e.target.value)}
          className="w-full mt-2 bg-black border border-[#2a2520] p-3 rounded-xl text-[#c9a961] outline-none focus:border-[#c9a961] transition-all cursor-pointer"
        >
          <option value="">Seleccioná un modelo para calcular...</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name_es}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* COLUMNA IZQUIERDA: INPUTS */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-6 flex flex-col gap-6">
          <h3 className="text-[#c9a961] font-serif text-lg flex items-center gap-2">
            <Calculator size={18} /> Medidas Finales
          </h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] text-[#6b6560] uppercase ml-1">Ancho (cm)</label>
              <input
                type="number"
                placeholder="0.00"
                value={windowWidth}
                onChange={(e) => setWindowWidth(e.target.value)}
                className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[10px] text-[#6b6560] uppercase ml-1">Alto (cm)</label>
              <input
                type="number"
                placeholder="0.00"
                value={windowHeight}
                onChange={(e) => setWindowHeight(e.target.value)}
                className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
              />
            </div>
          </div>

          <button
            onClick={handleConfirmProduction}
            disabled={!explosion || loading || confirmed}
            className={cn(
              "w-full py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2 shadow-lg mt-auto",
              loading ? "bg-gray-700 cursor-not-allowed" : 
              confirmed ? "bg-green-600 text-white" : 
              "bg-[#c9a961] text-black hover:bg-[#d4b574] active:scale-95 disabled:opacity-30"
            )}
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : confirmed ? <Check size={20} /> : <Scissors size={20} />}
            <span>{loading ? "Procesando en Neon..." : confirmed ? "Stock Actualizado" : "Confirmar y Cortar"}</span>
          </button>
        </div>

        {/* COLUMNA DERECHA: DESGLOSE */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-6 flex flex-col">
          <h3 className="text-[#6b6560] font-serif text-lg mb-4 flex justify-between items-center">
            Desglose de Materiales
            {loading && <Loader2 size={16} className="animate-spin text-[#c9a961]" />}
          </h3>
          
          <div className="flex-1 space-y-3 min-h-[200px]">
            {explosion ? (
              explosion.map((item, index) => (
                <div 
                  key={index} 
                  className={cn(
                    "flex justify-between items-center p-3 rounded-lg border transition-all",
                    item.metodo === "RETAZO" ? "bg-[#c9a961]/5 border-[#c9a961]/40" : "bg-black/40 border-[#2a2520]"
                  )}
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="text-white text-sm font-bold">{item.componente}</p>
                      {item.metodo === "RETAZO" && (
                        <span className="text-[8px] bg-[#c9a961] text-black px-1 rounded font-bold">RETAZO</span>
                      )}
                    </div>
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
                <Calculator size={40} className="mb-2 opacity-20" />
                <p className="text-sm italic">Esperando medidas...</p>
              </div>
            )}
          </div>

          {explosion && (
            <div className={cn("mt-6 pt-4 border-t border-[#2a2520]", isOverBudget && "border-red-900/50")}>
              <div className="flex justify-between items-end">
                <div>
                  <p className="text-[9px] text-[#6b6560] uppercase tracking-widest mb-1">Costo Total</p>
                  <p className="text-2xl text-white font-serif">${totalCost.toLocaleString('es-AR')}</p>
                </div>
                <div className="text-right">
                  <p className="text-[9px] text-[#6b6560] uppercase mb-1 font-bold">PVP Sugerido (40%)</p>
                  <p className="text-xl text-[#c9a961] font-bold">
                    ${(totalCost / 0.6).toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                  </p>
                  {/* 5. VISUALIZACIÓN DE COMPOSICIÓN DE COSTOS */}
{explosion && explosion.length > 0 && (
  <div className="mt-8 space-y-3">
    <div className="flex justify-between items-center">
      <p className="text-[10px] text-[#6b6560] uppercase font-bold tracking-widest">
        Distribución de Gastos
      </p>
      <p className="text-[10px] text-[#c9a961] font-mono">
        {explosion.length} ítems analizados
      </p>
    </div>
    
    {/* Barra de Progreso Segmentada */}
    <div className="h-2 w-full bg-[#1a1a1a] rounded-full overflow-hidden flex">
      {explosion.map((item, idx) => {
        const percentage = (item.costo_parcial / totalCost) * 100;
        // Colores alternados dentro de la gama de AMARIGOM
        const colors = ["#c9a961", "#8e7542", "#5c4d2d", "#3a311d"];
        return (
          <div
            key={idx}
            style={{ width: `${percentage}%`, backgroundColor: colors[idx % colors.length] }}
            className="h-full transition-all duration-500 hover:brightness-125 cursor-help"
            title={`${item.componente}: ${percentage.toFixed(1)}%`}
          />
        );
      })}
    </div>

    {/* Mini Leyenda Dinámica */}
    <div className="flex flex-wrap gap-x-4 gap-y-1">
      {explosion.slice(0, 4).map((item, idx) => {
        const percentage = (item.costo_parcial / totalCost) * 100;
        if (percentage < 5) return null; // No mostramos los que son casi despreciables
        const colors = ["#c9a961", "#8e7542", "#5c4d2d", "#3a311d"];
        return (
          <div key={idx} className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: colors[idx % colors.size] }} />
            <span className="text-[9px] text-[#6b6560]">
              {item.componente.split(' ')[0]} ({percentage.toFixed(0)}%)
            </span>
          </div>
        );
      })}
    </div>
  </div>
)}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div> 
  );
}