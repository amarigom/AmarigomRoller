"use client"

import { useState, useMemo, useEffect } from "react"
import { Calculator, Scissors, AlertTriangle, Check, Loader2, DollarSign, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

interface RecipeComponent {
  componente: string
  consumo_m_o_m2: number
  medida_corte: string
  precio_unitario: number
  costo_parcial: number
  metodo?: "ROLLO" | "RETAZO" // Nuevo: Identifica el origen
  id_retazo?: number         // Nuevo: ID específico si es retazo
}

interface CuttingCalculatorProps {
  rolls: any[] 
  productId: number 
  onDiscountStock: (items: RecipeComponent[]) => void
}

export default function CuttingCalculator({ rolls, productId, onDiscountStock }: CuttingCalculatorProps) {
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [selectedRollId, setSelectedRollId] = useState("")
  const [budget, setBudget] = useState("")
  const [explosion, setExplosion] = useState<RecipeComponent[] | null>(null)
  const [optimization, setOptimization] = useState<{mensaje: string, id: number} | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)

  const calcularReceta = async () => {
    if (!windowWidth || !windowHeight) return
    setLoading(true)
    try {
      // Enviamos ancho y alto para que el backend busque retazos
      const response = await fetch(
      `/api/test-recipe/${productId}?w=${windowWidth}&h=${windowHeight}`
    )
    
    if (!response.ok) throw new Error("Error en la respuesta del servidor");

    const data = await response.json()
      
      if (data.status === "success") {
        setExplosion(data.explosion)
        // Si el backend encontró un retazo para la tela, lo guardamos para el banner
        const telaOpt = data.explosion.find((item: any) => item.metodo === "RETAZO")
        if (telaOpt) {
          setOptimization({ mensaje: telaOpt.mensaje, id: telaOpt.id_retazo })
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

  useEffect(() => {
    const timer = setTimeout(() => {
      if (windowWidth && windowHeight) calcularReceta()
    }, 600)
    return () => clearTimeout(timer)
  }, [windowWidth, windowHeight, productId])

  const totalCost = useMemo(() => {
    if (!explosion) return 0
    return explosion.reduce((acc, item) => acc + item.costo_parcial, 0)
  }, [explosion])

  const isOverBudget = useMemo(() => {
    const b = parseFloat(budget)
    return b > 0 && totalCost > b
  }, [totalCost, budget])

  return (
    <div className="flex flex-col gap-6">
      
      {/* BANNER DE OPTIMIZACIÓN (Aparece solo si hay retazo) */}
      {optimization && (
        <div className="bg-[#c9a961]/10 border border-[#c9a961]/30 p-4 rounded-xl flex items-center gap-4 animate-pulse">
          <div className="bg-[#c9a961] p-2 rounded-full text-black">
            <Sparkles size={20} />
          </div>
          <div className="flex-1">
            <p className="text-[#c9a961] font-bold text-sm">¡Ahorro Detectado!</p>
            <p className="text-[#f5f0e8] text-xs italic">{optimization.mensaje}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* COLUMNA IZQUIERDA: INPUTS */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col gap-5">
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
            onClick={() => {
                onDiscountStock(explosion || [])
                setConfirmed(true)
                setTimeout(() => setConfirmed(false), 3000)
            }}
            disabled={!explosion || loading || confirmed}
            className={cn(
                "w-full py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2 shadow-lg",
                confirmed ? "bg-green-600 text-white" : "bg-[#c9a961] text-black hover:bg-[#d4b574] disabled:opacity-30"
            )}
          >
            {loading ? <Loader2 className="animate-spin" /> : confirmed ? <Check /> : <Scissors />}
            {confirmed ? "Stock Actualizado" : "Confirmar y Cortar"}
          </button>
        </div>

        {/* COLUMNA DERECHA: DESGLOSE */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col">
          <h3 className="text-[#6b6560] font-serif text-lg mb-4 flex justify-between">
            Desglose de Materiales
            {loading && <Loader2 size={16} className="animate-spin text-[#c9a961]" />}
          </h3>
          
          <div className="flex-1 space-y-3">
            {explosion?.map((item, index) => (
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
                    {item.metodo === "RETAZO" && <span className="text-[8px] bg-[#c9a961] text-black px-1 rounded font-bold">RETAZO</span>}
                  </div>
                  <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Corte: {item.medida_corte}</p>
                </div>
                <div className="text-right">
                  <p className="text-[#c9a961] font-mono text-sm">{item.consumo_m_o_m2}</p>
                  <p className="text-[10px] text-[#6b6560] font-bold">${item.costo_parcial.toFixed(2)}</p>
                </div>
              </div>
            ))}
          </div>

          {/* TOTALES */}
          {explosion && (
            <div className={cn(
                "mt-6 pt-4 border-t border-[#2a2520]",
                isOverBudget && "border-red-900/50"
            )}>
              <div className="flex justify-between items-end">
                <div>
                  <p className={cn("text-[9px] uppercase tracking-widest mb-1", isOverBudget ? "text-red-400" : "text-[#6b6560]")}>
                    {isOverBudget ? "⚠️ Presupuesto Excedido" : "Costo Total"}
                  </p>
                  <p className={cn("text-2xl font-serif", isOverBudget ? "text-red-500" : "text-white")}>
                    ${totalCost.toLocaleString('es-AR')}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-[9px] text-[#6b6560] uppercase mb-1">PVP Sugerido</p>
                  <p className="text-xl text-[#c9a961] font-bold">
                    ${(totalCost / 0.6).toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
