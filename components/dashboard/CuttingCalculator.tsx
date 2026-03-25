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
  metodo?: "ROLLO" | "RETAZO" 
  id_retazo?: number         
}

interface Product {
  id: number;
  name_es: string;
}
interface CuttingCalculatorProps {
  products: Product[]; 
  onDiscountStock: (items: RecipeComponent[]) => void;
  productId?: number; 
}

export default function CuttingCalculator({ products = [], productId, onDiscountStock }: CuttingCalculatorProps) {
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [selectedRollId, setSelectedRollId] = useState("")
  const [budget, setBudget] = useState("")
  const [explosion, setExplosion] = useState<RecipeComponent[] | null>(null)
  const [optimization, setOptimization] = useState<{mensaje: string, id: number} | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)
  const [selectedProductId, setSelectedProductId] = useState<string>("");
  
const handleConfirmProduction = async () => {
  if (!explosion) return; // Si no hay receta calculada, no hacemos nada
  setLoading(true);
  try {
    // LLAMADA AL BACKEND PARA DESCONTAR DE NEON
    const response = await fetch('/api/confirm-production', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        explosion: explosion,
        productId: selectedProductId 
      })
    });

    const data = await response.json();

    if (data.status === "success") {
      // SI NEON SE ACTUALIZÓ OK:
      setConfirmed(true);
      
      // Avisamos al componente padre por si quiere refrescar algo visualmente
      onDiscountStock(explosion);
      
      // Limpiamos después de 3 segundos para el próximo pedido
      setTimeout(() => {
        setConfirmed(false);
        setExplosion(null);
        setWindowWidth("");
        setWindowHeight("");
      }, 3000);
    } else {
      alert("Error al actualizar base de datos: " + data.message);
    }
  } catch (error) {
    console.error("Error de conexión:", error);
    alert("No se pudo conectar con el servidor para descontar stock.");
  } finally {
    setLoading(false);
  }
};


  const calcularReceta = async () => {
    if (!windowWidth || !windowHeight|| !selectedProductId) return;
    setLoading(true)
    try {
      // Enviamos ancho y alto para que el backend busque retazos
      const response = await fetch(`/api/test-recipe/${selectedProductId}?w=${windowWidth}&h=${windowHeight}`)
    
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
      if (windowWidth && windowHeight && selectedProductId) calcularReceta()
    }, 600)
    return () => clearTimeout(timer)
  }, [windowWidth, windowHeight, selectedProductId])

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
      
      {/* 1. BANNER DE OPTIMIZACIÓN (Solo si el backend detecta retazo) */}
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

      {/* 2. SELECTOR DE MODELO (Ocupa todo el ancho arriba) */}
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

      {/* 3. GRID PRINCIPAL (Inputs a la izquierda, Resultados a la derecha) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* COLUMNA IZQUIERDA: INPUTS DE MEDIDAS */}
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
            {loading ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                <span>Procesando en Neon...</span>
              </>
            ) : confirmed ? (
              <>
                <Check size={20} />
                <span>Stock Actualizado</span>
              </>
            ) : (
              <>
                <Scissors size={20} />
                <span>Confirmar y Cortar</span>
              </>
            )}
          </button>
        </div>

        {/* COLUMNA DERECHA: DESGLOSE DE MATERIALES */}
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

          {/* 4. TOTALES Y PRECIO SUGERIDO */}
          {explosion && (
            <div className={cn(
                "mt-6 pt-4 border-t border-[#2a2520]",
                isOverBudget && "border-red-900/50"
            )}>
              <div className="flex justify-between items-end">
                <div>
                  <p className={cn("text-[9px] uppercase tracking-widest mb-1", isOverBudget ? "text-red-400" : "text-[#6b6560]")}>
                    {isOverBudget ? "Presupuesto Excedido" : "Costo Total (Insumos)"}
                  </p>
                  <p className={cn("text-2xl font-serif", isOverBudget ? "text-red-500" : "text-white")}>
                    ${totalCost.toLocaleString('es-AR')}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-[9px] text-[#6b6560] uppercase mb-1 font-bold">PVP Sugerido (40% Margen)</p>
                  <p className="text-xl text-[#c9a961] font-bold">
                    ${(totalCost / 0.6).toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div> {/* Fin Columna Derecha */}
      </div> {/* Fin Grid Principal */}
    </div> 
  );
}