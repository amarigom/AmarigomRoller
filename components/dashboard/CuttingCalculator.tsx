"use client"

import { useState, useMemo, useEffect } from "react"
import { Calculator, Scissors, AlertTriangle, Check, Loader2, DollarSign } from "lucide-react"
import { cn } from "@/lib/utils"

// Actualizamos la interfaz con los datos de costo del backend
interface RecipeComponent {
  componente: string
  consumo_m_o_m2: number
  medida_corte: string
  precio_unitario: number
  costo_parcial: number
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
  const [budget, setBudget] = useState("") // Estado para presupuesto objetivo
  const [explosion, setExplosion] = useState<RecipeComponent[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)

  const calcularReceta = async () => {
    if (!windowWidth || !windowHeight) return
    setLoading(true)
    try {
      const response = await fetch(`/api/test-recipe/${productId}`)
      const data = await response.json()
      if (data.status === "success") {
        setExplosion(data.explosion)
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
    }, 500)
    return () => clearTimeout(timer)
  }, [windowWidth, windowHeight])

  // Cálculo de Costo Total
  const totalCost = useMemo(() => {
    if (!explosion) return 0
    return explosion.reduce((acc, item) => acc + item.costo_parcial, 0)
  }, [explosion])

  // Lógica de Alerta de Presupuesto
  const isOverBudget = useMemo(() => {
    const b = parseFloat(budget)
    return b > 0 && totalCost > b
  }, [totalCost, budget])

  const selectedRoll = rolls.find((r) => r.id === selectedRollId)

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* COLUMNA IZQUIERDA: INPUTS */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col gap-5">
          <h3 className="text-[#c9a961] font-serif text-lg flex items-center gap-2">
            <Calculator size={18} /> Medidas Finales
          </h3>
          
          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              placeholder="Ancho cm"
              value={windowWidth}
              onChange={(e) => setWindowWidth(e.target.value)}
              className="bg-black border border-[#2a2520] p-3 rounded text-white outline-none focus:border-[#c9a961]"
            />
            <input
              type="number"
              placeholder="Alto cm"
              value={windowHeight}
              onChange={(e) => setWindowHeight(e.target.value)}
              className="bg-black border border-[#2a2520] p-3 rounded text-white outline-none focus:border-[#c9a961]"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-[10px] text-[#6b6560] uppercase">Presupuesto Objetivo ($)</label>
            <input
              type="number"
              placeholder="Ej: 50000"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="bg-black border border-[#2a2520] p-3 rounded text-white outline-none focus:border-[#c9a961]"
            />
          </div>

          <select
            value={selectedRollId}
            onChange={(e) => setSelectedRollId(e.target.value)}
            className="bg-black border border-[#2a2520] p-3 rounded text-white outline-none"
          >
            <option value="">Seleccionar Rollo de Tela</option>
            {rolls.map(roll => (
              <option key={roll.id} value={roll.id}>{roll.name} ({roll.metersLeft}m)</option>
            ))}
          </select>

          <button
            onClick={() => {
                onDiscountStock(explosion || [])
                setConfirmed(true)
                setTimeout(() => setConfirmed(false), 3000)
            }}
            disabled={!explosion || confirmed}
            className={cn(
                "w-full py-4 rounded-lg font-bold transition-all flex justify-center items-center gap-2",
                confirmed ? "bg-green-700 text-white" : "bg-[#c9a961] text-black hover:bg-[#d4b574]"
            )}
          >
            {confirmed ? <Check /> : <Scissors />}
            {confirmed ? "Stock Descontado" : "Confirmar Producción"}
          </button>
        </div>

        {/* COLUMNA DERECHA: RESULTADOS Y COSTOS */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col">
          <h3 className="text-[#c9a961] font-serif text-lg mb-4">Desglose de Materiales</h3>
          
          <div className="flex-1 overflow-y-auto space-y-3 max-h-[400px] pr-2 custom-scrollbar">
            {loading ? (
              <div className="flex justify-center py-10"><Loader2 className="animate-spin text-[#c9a961]" /></div>
            ) : explosion ? (
              explosion.map((item, index) => (
                <div key={index} className="flex justify-between items-center bg-black/40 p-3 rounded border border-[#2a2520]">
                  <div>
                    <p className="text-white text-sm font-bold">{item.componente}</p>
                    <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Corte: {item.medida_corte}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[#c9a961] font-mono">{item.consumo_m_o_m2}</p>
                    <p className="text-[10px] text-[#6b6560] font-bold">${item.costo_parcial.toFixed(2)}</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-[#6b6560] text-center py-10">Ingresá medidas para calcular...</p>
            )}
          </div>

          {/* SECCIÓN DE TOTALES */}
          {explosion && (
            <div className={cn(
                "mt-6 pt-6 border-t border-[#2a2520] transition-all duration-500",
                isOverBudget ? "bg-red-950/20 -m-2 p-4 rounded-lg border border-red-900/50" : ""
            )}>
              <div className="flex justify-between items-end">
                <div className="flex flex-col">
                    <span className={cn(
                        "text-[10px] uppercase tracking-[2px] mb-1",
                        isOverBudget ? "text-red-400 font-bold" : "text-[#6b6560]"
                    )}>
                        {isOverBudget ? "⚠️ Excede Presupuesto" : "Costo Total Materiales"}
                    </span>
                    <span className={cn(
                        "text-3xl font-serif",
                        isOverBudget ? "text-red-500" : "text-white"
                    )}>
                        ${totalCost.toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </span>
                </div>
                
                <div className="text-right">
                    <p className="text-[10px] text-[#6b6560] uppercase mb-1">Precio Sugerido (40% marg.)</p>
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