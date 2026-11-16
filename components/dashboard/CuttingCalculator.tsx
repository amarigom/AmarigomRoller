"use client"

import { useState, useEffect } from "react"
import { Calculator, Scissors, Check, Loader2, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"
import { apiFetch, getSession, hasPermission } from "@/lib/api"
import type { ExplosionTotals, MaterialComponent, QuoteTotals, RecipeComponent, RecipeItem } from "@/lib/types/recipe"
import { displayNumber, linearDisplay } from "@/lib/display-units"

interface CuttingCalculatorProps {
  selectedProductId: number | null;
  recipe: RecipeItem[];
  onRefreshInventory: () => void;
  priceRevision?: number;
  onQuoteSaved?: () => void;
}

function tieneCostos(item: MaterialComponent): item is RecipeComponent {
  return "precio_unitario" in item && typeof item.precio_unitario === "number"
    && "costo_parcial" in item && typeof item.costo_parcial === "number"
}

export default function CuttingCalculator({ 
  selectedProductId, 
  recipe,
  onRefreshInventory,
  priceRevision = 0,
  onQuoteSaved,
}: CuttingCalculatorProps) {
  
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [referencia, setReferencia] = useState("")
  const [kmObra, setKmObra] = useState("0")
  const [explosion, setExplosion] = useState<MaterialComponent[] | null>(null)
  const [totals, setTotals] = useState<QuoteTotals | ExplosionTotals | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmed, setConfirmed] = useState(false)
  const [producing, setProducing] = useState(false)
  const [produceError, setProduceError] = useState<string | null>(null)
  const [quoteToken, setQuoteToken] = useState<string | null>(null)
  const [savingQuote, setSavingQuote] = useState(false)
  const [savedQuote, setSavedQuote] = useState<number | null>(null)
  const canProduce = hasPermission(getSession(), "recipes:produce")
  const role = getSession()?.user.rol
  const canQuote = role === "admin" || role === "ventas"
  const canViewCosts = role === "admin"

  // Al cambiar medidas o producto hay que volver a confirmar
  useEffect(() => {
    setConfirmed(false)
    setProduceError(null)
    setExplosion(null)
    setTotals(null)
  }, [windowWidth, windowHeight, selectedProductId, referencia])

  const confirmarProduccion = async () => {
    if (!explosion || !selectedProductId) return
    if (!window.confirm("Se descontará el stock y se marcarán los retazos usados. ¿Confirmar producción?")) return
    setProducing(true)
    setProduceError(null)
    try {
      const response = await apiFetch(`/api/recipes/${selectedProductId}/produce`, {
        method: "POST",
        body: JSON.stringify({
          w: Number(windowWidth), h: Number(windowHeight), referencia: referencia || null,
        }),
      })
      const data = await response.json().catch(() => ({}))
      if (!response.ok) {
        const detalle = Array.isArray(data.detalles) && data.detalles.length ? ` (${data.detalles.join("; ")})` : ""
        setProduceError((data.message || "No se pudo confirmar la producción") + detalle)
        return
      }
      setConfirmed(true)
      onRefreshInventory()
    } catch {
      setProduceError("Error de red al confirmar la producción")
    } finally {
      setProducing(false)
    }
  }

  const guardarPresupuesto = async () => {
    if (!quoteToken) return
    setSavingQuote(true)
    setProduceError(null)
    try {
      const response = await apiFetch("/api/quotes/saved", {
        method: "POST", body: JSON.stringify({ token: quoteToken }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || "No se pudo guardar el presupuesto")
      setSavedQuote(data.id)
      onQuoteSaved?.()
    } catch (error) {
      setProduceError(error instanceof Error ? error.message : "No se pudo guardar el presupuesto")
    } finally {
      setSavingQuote(false)
    }
  }

  useEffect(() => {
    const controller = new AbortController()
    setExplosion(null)
    setTotals(null)
    setQuoteToken(null)
    setSavedQuote(null)
    setProduceError(null)
    if (!windowWidth || !windowHeight || !selectedProductId) {
      setLoading(false)
      return () => controller.abort()
    }
    if (!role) return () => controller.abort()
    if (canQuote && !kmObra.trim()) {
      setLoading(false)
      setProduceError("Indicá la distancia de ida a la obra.")
      return () => controller.abort()
    }
    setLoading(true)
    const timer = setTimeout(() => {
      const calcularReceta = async () => {
        try {
          const params = new URLSearchParams({ w: windowWidth, h: windowHeight })
          if (canQuote) params.set("km_obra", kmObra)
          if (referencia) params.set("referencia", referencia)
          const response = await apiFetch(`/api/recipes/${selectedProductId}/${canQuote ? "quote" : "explosion"}?${params}`, {
            signal: controller.signal,
          })
          const data = await response.json()
          if (!response.ok) {
            const detalle = Array.isArray(data.detalles) && data.detalles.length ? ` (${data.detalles.join("; ")})` : ""
            throw new Error((data.message || "No se pudo calcular la receta") + detalle)
          }
          if (controller.signal.aborted) return
          setExplosion(data.explosion)
          if (canQuote) {
            setTotals(data)
            setQuoteToken(data.guardado_token)
          }
        } catch (error) {
          if (!controller.signal.aborted) {
            setProduceError(error instanceof Error ? error.message : "Error al calcular la receta")
          }
        } finally {
          if (!controller.signal.aborted) setLoading(false)
        }
      }
      void calcularReceta()
    }, 600)
    return () => {
      clearTimeout(timer)
      controller.abort()
    }
  }, [windowWidth, windowHeight, selectedProductId, referencia, kmObra, priceRevision, role, canQuote])

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
            <label className="text-[10px] text-[#6b6560] uppercase ml-1">Referencia de presupuesto / pedido (opcional)</label>
            <input
              type="text"
              value={referencia}
              onChange={(e) => setReferencia(e.target.value)}
              maxLength={255}
              className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
              placeholder="Ej: PED-2026-001"
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
          {canQuote && <div className="space-y-1">
            <label htmlFor="km-obra" className="text-[10px] text-[#6b6560] uppercase ml-1">Distancia de ida a la obra (km)</label>
            <input
              id="km-obra"
              type="number"
              min="0"
              step="0.01"
              value={kmObra}
              onChange={(e) => setKmObra(e.target.value)}
              className="w-full bg-black border border-[#2a2520] p-3 rounded-xl text-white outline-none focus:border-[#c9a961] transition-all"
            />
          </div>}
        </div>

        {produceError && <p className="text-sm text-red-400">{produceError}</p>}
        {!canProduce && (
          <p className="text-xs text-[#6b6560]">Tu rol no puede confirmar producciones.</p>
        )}

        {canQuote && <button onClick={guardarPresupuesto} disabled={!quoteToken || loading || savingQuote || savedQuote !== null}
          className="w-full rounded-xl border border-[#c9a961] py-3 text-sm text-[#c9a961] disabled:opacity-40">
          {savingQuote ? "Guardando…" : savedQuote ? `Presupuesto #${savedQuote} guardado` : "Guardar presupuesto"}
        </button>}

        <button
          onClick={confirmarProduccion}
          disabled={!explosion || loading || producing || confirmed || !canProduce}
          className={cn(
            "w-full py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2 mt-auto shadow-lg",
            confirmed ? "bg-green-600 text-white" : "bg-[#c9a961] text-black hover:bg-[#d4b574] disabled:opacity-20"
          )}
        >
          {loading || producing ? <Loader2 className="animate-spin" size={20} /> : confirmed ? <Check size={20} /> : <Scissors size={20} />}
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
            explosion.map((item, index) => {
              const stock = linearDisplay(item.metodo === "RETAZO" ? 0 : item.consumo_m_o_m2, 0, item.unidad)
              const priced = canViewCosts && tieneCostos(item) ? item : null
              const costo = priced && linearDisplay(priced.cantidad_costo ?? (priced.metodo === "RETAZO" ? 0 : priced.consumo_m_o_m2), priced.precio_unitario, priced.unidad_costo ?? priced.unidad)
              return (
              <div key={index} className="flex justify-between items-center p-3 bg-black/40 border border-[#2a2520] rounded-lg">
                <div>
                  <p className="text-white text-sm font-bold">{item.componente}</p>
                  <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Corte: {item.medida_corte}</p>
                  {item.mensaje && <p className="text-[10px] text-[#c9a961]/80">{item.mensaje}</p>}
                  {!!item.merma_pct && <p className="text-[10px] text-[#6b6560]">Merma {item.merma_pct}%</p>}
                  {!!item.minutos && <p className="text-[10px] text-[#6b6560]">Mano de obra {item.minutos} min</p>}
                </div>
                <div className="text-right">
                  <p className="text-[#c9a961] font-mono text-sm">Stock rollo / insumo: {displayNumber(stock.quantity, stock.unit === "metro" ? 2 : 0)} {stock.unit === "metro" ? "m" : stock.unit}</p>
                  {priced && costo && <>
                    {item.metodo !== "MANO_OBRA" && <p className="text-[10px] text-[#6b6560]">Costo: {displayNumber(costo.quantity, costo.unit === "metro" ? 2 : 0)} {costo.unit === "metro" ? "m" : costo.unit} × ${displayNumber(costo.price, 2)} / {costo.unit === "metro" ? "m" : costo.unit}</p>}
                    <p className="text-[10px] text-[#6b6560] font-bold">Costo real: ${priced.costo_parcial.toFixed(2)}</p>
                    {!!priced.costo_reposicion && <p className="text-[10px] text-[#c9a961]">Referencia para venta: {displayNumber(priced.cantidad_reposicion ?? 0, 2)} m × ${displayNumber(priced.precio_unitario, 2)} / m = ${displayNumber(priced.costo_reposicion, 2)}</p>}
                  </>}
                </div>
              </div>
            )})
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-[#2a2520] border-2 border-dashed border-[#1a1a1a] rounded-xl p-10">
              <Calculator size={40} className="mb-2 opacity-10" />
              <p className="text-sm italic">Cargando datos de receta...</p>
            </div>
          )}
        </div>

        {explosion && totals && (
          <div className="mt-6 pt-4 border-t border-[#2a2520] flex justify-between items-end">
            {canViewCosts && "total" in totals && <div>
              <p className="text-[9px] text-[#6b6560] uppercase tracking-widest mb-1">Costo Total</p>
              <p className="text-2xl text-white font-serif">${totals.total.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
              <p className="text-[10px] text-[#6b6560]">Materiales: ${totals.total_materiales.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
              <p className="text-[10px] text-[#6b6560]">Mano de obra: ${totals.total_mano_obra.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ({totals.total_minutos} min)</p>
              <p className="text-[10px] text-[#6b6560]">Desgaste maquinaria: ${totals.total_desgaste.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>}
            <div className="text-right">
              <p className="text-[9px] text-[#6b6560] uppercase mb-1 font-bold">Cortina{canViewCosts && "markup_pct" in totals.precio_producto && ` (markup ${totals.precio_producto.markup_pct}% sobre costo de referencia)`}</p>
              <p className="text-xl text-[#c9a961] font-bold">${totals.precio_producto.precio_venta_final.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
              {canViewCosts && "total" in totals && <>
                <p className="text-[10px] text-[#6b6560]">Ganancia bruta: ${totals.precio_producto.ganancia_markup.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                <p className="text-[10px] text-[#6b6560]">Margen sobre ventas: {totals.precio_producto.margen_sobre_ventas_pct}%</p>
                <p className="text-[10px] text-[#6b6560]">Colocación: ${totals.servicio_colocacion.tarifa_base.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                <p className="text-[10px] text-[#6b6560]">Traslado ({totals.servicio_colocacion.km_totales} km ida y vuelta): ${totals.servicio_colocacion.costo_traslado.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
              </>}
              {!canViewCosts && <p className="text-[10px] text-[#6b6560]">Colocación y traslado: ${totals.servicio_colocacion.total_colocacion.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>}
              <p className="text-sm text-white font-bold">Total presupuesto: ${totals.total_presupuesto.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
          </div>
        )}
      </div>
    </div> 
  );
}