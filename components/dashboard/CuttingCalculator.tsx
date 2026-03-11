"use client"

import { useState, useMemo } from "react"
import { Calculator, Scissors, AlertTriangle, Check } from "lucide-react"
import type { FabricRoll, CuttingCalculation } from "@/lib/types/dashboards"
import { cn, formatPrice } from "@/lib/utils"

interface CuttingCalculatorProps {
  rolls: FabricRoll[]
  onDiscountStock: (rollId: string, meters: number) => void
}

export default function CuttingCalculator({ rolls, onDiscountStock }: CuttingCalculatorProps) {
  const [windowWidth, setWindowWidth] = useState("")
  const [windowHeight, setWindowHeight] = useState("")
  const [selectedRollId, setSelectedRollId] = useState("")
  const [confirmed, setConfirmed] = useState(false)

  const calculation: CuttingCalculation | null = useMemo(() => {
    const w = parseFloat(windowWidth)
    const h = parseFloat(windowHeight)
    if (isNaN(w) || isNaN(h) || w <= 0 || h <= 0) return null

    const adjustedWidth = w + 10 
    const adjustedHeight = h + 30
    const linearMeters = adjustedHeight / 100

    return {
      windowWidthCm: w,
      windowHeightCm: h,
      adjustedWidthCm: adjustedWidth,
      adjustedHeightCm: adjustedHeight,
      linearMeters: Math.round(linearMeters * 100) / 100,
      selectedRollId: selectedRollId || null,
    }
  }, [windowWidth, windowHeight, selectedRollId])

  const selectedRoll = rolls.find((r) => r.id === selectedRollId)

  // --- FUNCIÓN DE NORMALIZACIÓN DE ANCHO (Metros o CM) ---
  const getRollWidthInCm = (roll: FabricRoll | undefined) => {
    if (!roll) return 0
    const w = Number(roll.widthCm)
    // Si el valor es pequeño (ej: 2.1), son metros. Si es grande (ej: 210), son cm.
    return w < 10 ? w * 100 : w
  }

  const canConfirm = useMemo(() => {
    if (!calculation || !selectedRoll) return false
    
    // 1. Validar Largo (Stock disponible)
    const tieneStockLargo = calculation.linearMeters <= Number(selectedRoll.metersLeft)
    
    // 2. Validar Ancho (Físico de la tela)
    const anchoRolloCm = getRollWidthInCm(selectedRoll)
    const cabeAncho = calculation.adjustedWidthCm <= anchoRolloCm
    
    return tieneStockLargo && cabeAncho
  }, [calculation, selectedRoll])

  const estimatedPrice = useMemo(() => {
    if (!calculation || !selectedRoll) return 0
    return Math.round(calculation.linearMeters * selectedRoll.pricePerMeter)
  }, [calculation, selectedRoll])

  function handleConfirm() {
    if (!canConfirm || !calculation || !selectedRollId) return
    onDiscountStock(selectedRollId, calculation.linearMeters)
    setConfirmed(true)
    setTimeout(() => {
      setConfirmed(false)
      handleReset()
    }, 3000)
  }

  function handleReset() {
    setWindowWidth("")
    setWindowHeight("")
    setSelectedRollId("")
    setConfirmed(false)
  }

  const availableRolls = rolls.filter((r) => Number(r.metersLeft) > 0)

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="font-serif text-2xl text-[#f5f0e8]">Calculadora de Corte</h2>
        <p className="text-sm text-[#6b6560] mt-1">Gestión de stock para AMARIGOM DECO</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col gap-5">
          <div className="flex items-center gap-2 text-[#c9a961] mb-1">
            <Calculator size={18} />
            <h3 className="font-serif text-lg">Medidas de la ventana</h3>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-[#6b6560] uppercase mb-2">Ancho (cm)</label>
              <input
                type="number"
                value={windowWidth}
                onChange={(e) => { setWindowWidth(e.target.value); setConfirmed(false) }}
                placeholder="150"
                className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] outline-none"
              />
            </div>
            <div>
              <label className="block text-xs text-[#6b6560] uppercase mb-2">Alto (cm)</label>
              <input
                type="number"
                value={windowHeight}
                onChange={(e) => { setWindowHeight(e.target.value); setConfirmed(false) }}
                placeholder="200"
                className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs text-[#6b6560] uppercase mb-2">Seleccionar rollo de tela</label>
            <select
              value={selectedRollId}
              onChange={(e) => { setSelectedRollId(e.target.value); setConfirmed(false) }}
              className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] transition-colors outline-none"
            >
              <option value="">-- Seleccionar rollo --</option>
              {availableRolls.map((roll) => (
                <option key={roll.id} value={roll.id}>
                  {roll.name} ({roll.metersLeft}m disp. - {getRollWidthInCm(roll)}cm ancho)
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-3 mt-2">
            <button
              onClick={handleConfirm}
              disabled={!canConfirm || confirmed}
              className={cn(
                "flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg text-sm font-medium transition-all",
                confirmed ? "bg-[#7a9b76] text-[#0a0a0a]" : canConfirm ? "bg-[#c9a961] text-[#0a0a0a] hover:bg-[#d4b574]" : "bg-[#1a1a1a] text-[#3a3530] cursor-not-allowed"
              )}
            >
              {confirmed ? <><Check size={16} /> ¡Stock actualizado!</> : <><Scissors size={16} /> Confirmar y descontar stock</>}
            </button>
            <button onClick={handleReset} className="px-4 py-3 rounded-lg text-sm border border-[#2a2520] text-[#6b6560] hover:text-white">
              Limpiar
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6">
            <h3 className="font-serif text-lg text-[#c9a961] mb-4">Resultado del cálculo</h3>

            {calculation ? (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase">Ancho + Margen (+10)</p>
                    <p className="text-lg text-[#c9a961] font-serif">{calculation.adjustedWidthCm} cm</p>
                  </div>
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase">Alto + Margen (+30)</p>
                    <p className="text-lg text-[#c9a961] font-serif">{calculation.adjustedHeightCm} cm</p>
                  </div>
                </div>

                <div className="bg-[#c9a961]/5 border border-[#c9a961]/20 rounded-lg p-5 text-center">
                  <p className="text-xs text-[#c9a961] uppercase mb-1">Metros lineales necesarios</p>
                  <p className="text-4xl font-serif text-[#c9a961]">{calculation.linearMeters} m</p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center py-8 text-[#2a2520]">
                <Calculator size={40} className="mb-3" />
                <p className="text-sm text-[#6b6560]">Ingresá medidas para ver el cálculo</p>
              </div>
            )}
          </div>

          {/* --- ALERTAS DE VALIDACIÓN --- */}
          {calculation && selectedRoll && (
            <div className="flex flex-col gap-2">
              {calculation.adjustedWidthCm > getRollWidthInCm(selectedRoll) && (
                <div className="flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3 text-[#c97676]">
                  <AlertTriangle size={16} className="flex-shrink-0" />
                  <p className="text-xs">
                    El ancho ajustado ({calculation.adjustedWidthCm}cm) supera el ancho del rollo ({getRollWidthInCm(selectedRoll)}cm). La cortina no entra.
                  </p>
                </div>
              )}
              {calculation.linearMeters > Number(selectedRoll.metersLeft) && (
                <div className="flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3 text-[#c97676]">
                  <AlertTriangle size={16} className="flex-shrink-0" />
                  <p className="text-xs">Stock insuficiente en metros lineales ({selectedRoll.metersLeft}m disponibles)</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}