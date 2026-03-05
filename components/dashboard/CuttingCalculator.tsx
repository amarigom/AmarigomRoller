"use client"

/**
 * CuttingCalculator Component
 *
 * Calculadora de corte para cortinas roller.
 * Ajusta automaticamente: +5cm cada lado (ancho), +30cm tubo (alto).
 * Permite seleccionar un rollo y descontar stock.
 *
 * Preparado para conectar con: POST /api/inventory/:id/discount
 */

import { useState, useMemo } from "react"
import { Calculator, Scissors, AlertTriangle, Check } from "lucide-react"
import type { FabricRoll, CuttingCalculation } from "@/lib/types/dashboard"
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

    const adjustedWidth = w + 10  // +5cm cada lado
    const adjustedHeight = h + 30 // +30cm tubo roller
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

  const canConfirm = useMemo(() => {
    if (!calculation || !selectedRoll) return false
    if (calculation.linearMeters > selectedRoll.metersLeft) return false
    if (calculation.adjustedWidthCm > selectedRoll.widthCm) return false
    return true
  }, [calculation, selectedRoll])

  const estimatedPrice = useMemo(() => {
    if (!calculation || !selectedRoll) return 0
    return Math.round(calculation.linearMeters * selectedRoll.pricePerMeter)
  }, [calculation, selectedRoll])

  function handleConfirm() {
    if (!canConfirm || !calculation || !selectedRollId) return
    onDiscountStock(selectedRollId, calculation.linearMeters)
    setConfirmed(true)
    setTimeout(() => setConfirmed(false), 3000)
  }

  function handleReset() {
    setWindowWidth("")
    setWindowHeight("")
    setSelectedRollId("")
    setConfirmed(false)
  }

  // Filtrar solo rollos con stock
  const availableRolls = rolls.filter((r) => r.status !== "critical" || r.metersLeft > 0)

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div>
        <h2 className="font-serif text-2xl text-[#f5f0e8]">Calculadora de Corte</h2>
        <p className="text-sm text-[#6b6560] mt-1">
          Calcula los metros lineales necesarios y desconta del stock
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Inputs */}
        <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col gap-5">
          <div className="flex items-center gap-2 text-[#c9a961] mb-1">
            <Calculator size={18} />
            <h3 className="font-serif text-lg">Medidas de la ventana</h3>
          </div>

          {/* Width Input */}
          <div>
            <label className="block text-xs text-[#6b6560] uppercase tracking-wider mb-2">
              Ancho de ventana (cm)
            </label>
            <input
              type="number"
              value={windowWidth}
              onChange={(e) => { setWindowWidth(e.target.value); setConfirmed(false) }}
              placeholder="Ej: 150"
              className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] placeholder-[#3a3530] focus:outline-none focus:border-[#c9a961] transition-colors"
            />
            <p className="text-[10px] text-[#6b6560] mt-1">Se agregan +5cm de cada lado automaticamente</p>
          </div>

          {/* Height Input */}
          <div>
            <label className="block text-xs text-[#6b6560] uppercase tracking-wider mb-2">
              Alto de ventana (cm)
            </label>
            <input
              type="number"
              value={windowHeight}
              onChange={(e) => { setWindowHeight(e.target.value); setConfirmed(false) }}
              placeholder="Ej: 200"
              className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] placeholder-[#3a3530] focus:outline-none focus:border-[#c9a961] transition-colors"
            />
            <p className="text-[10px] text-[#6b6560] mt-1">Se agregan +30cm para el tubo roller automaticamente</p>
          </div>

          {/* Roll Selection */}
          <div>
            <label className="block text-xs text-[#6b6560] uppercase tracking-wider mb-2">
              Seleccionar rollo de tela
            </label>
            <select
              value={selectedRollId}
              onChange={(e) => { setSelectedRollId(e.target.value); setConfirmed(false) }}
              className="w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:outline-none focus:border-[#c9a961] transition-colors appearance-none"
            >
              <option value="">-- Seleccionar rollo --</option>
              {availableRolls.map((roll) => (
                <option key={roll.id} value={roll.id}>
                  {roll.name} ({roll.metersLeft}m disponibles - {roll.widthCm}cm ancho)
                </option>
              ))}
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mt-2">
            <button
              onClick={handleConfirm}
              disabled={!canConfirm || confirmed}
              className={cn(
                "flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg text-sm font-medium transition-all",
                confirmed
                  ? "bg-[#7a9b76] text-[#0a0a0a]"
                  : canConfirm
                  ? "bg-[#c9a961] text-[#0a0a0a] hover:bg-[#d4b574]"
                  : "bg-[#1a1a1a] text-[#3a3530] cursor-not-allowed"
              )}
            >
              {confirmed ? (
                <>
                  <Check size={16} />
                  Stock descontado
                </>
              ) : (
                <>
                  <Scissors size={16} />
                  Confirmar y descontar stock
                </>
              )}
            </button>
            <button
              onClick={handleReset}
              className="px-4 py-3 rounded-lg text-sm border border-[#2a2520] text-[#6b6560] hover:border-[#3a3530] hover:text-[#a0998c] transition-all"
            >
              Limpiar
            </button>
          </div>
        </div>

        {/* Right: Results */}
        <div className="flex flex-col gap-4">
          {/* Calculation Result */}
          <div className="bg-[#111111] border border-[#2a2520] rounded-lg p-6">
            <h3 className="font-serif text-lg text-[#c9a961] mb-4">Resultado del calculo</h3>

            {calculation ? (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Ancho original</p>
                    <p className="text-lg text-[#f5f0e8] font-serif">{calculation.windowWidthCm} cm</p>
                  </div>
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Ancho ajustado</p>
                    <p className="text-lg text-[#c9a961] font-serif">{calculation.adjustedWidthCm} cm</p>
                  </div>
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Alto original</p>
                    <p className="text-lg text-[#f5f0e8] font-serif">{calculation.windowHeightCm} cm</p>
                  </div>
                  <div className="bg-[#0a0a0a] rounded-lg p-4">
                    <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Alto ajustado</p>
                    <p className="text-lg text-[#c9a961] font-serif">{calculation.adjustedHeightCm} cm</p>
                  </div>
                </div>

                {/* Linear Meters */}
                <div className="bg-[#c9a961]/5 border border-[#c9a961]/20 rounded-lg p-5 text-center">
                  <p className="text-xs text-[#c9a961] uppercase tracking-wider mb-1">Metros lineales a cortar</p>
                  <p className="text-4xl font-serif text-[#c9a961]">{calculation.linearMeters} m</p>
                </div>

                {/* Estimated Price */}
                {selectedRoll && (
                  <div className="bg-[#0a0a0a] rounded-lg p-4 flex justify-between items-center">
                    <span className="text-xs text-[#6b6560]">Costo estimado</span>
                    <span className="text-lg text-[#c9a961] font-serif">{formatPrice(estimatedPrice)}</span>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center py-8 text-[#2a2520]">
                <Calculator size={40} className="mb-3" />
                <p className="text-sm text-[#6b6560]">Ingresa las medidas para ver el calculo</p>
              </div>
            )}
          </div>

          {/* Warnings */}
          {calculation && selectedRoll && (
            <div className="flex flex-col gap-2">
              {calculation.adjustedWidthCm > selectedRoll.widthCm && (
                <div className="flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3">
                  <AlertTriangle size={16} className="text-[#c97676] flex-shrink-0" />
                  <p className="text-xs text-[#c97676]">
                    El ancho ajustado ({calculation.adjustedWidthCm}cm) supera el ancho del rollo ({selectedRoll.widthCm}cm)
                  </p>
                </div>
              )}
              {calculation.linearMeters > selectedRoll.metersLeft && (
                <div className="flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3">
                  <AlertTriangle size={16} className="text-[#c97676] flex-shrink-0" />
                  <p className="text-xs text-[#c97676]">
                    No hay suficientes metros en el rollo ({selectedRoll.metersLeft}m disponibles, se necesitan {calculation.linearMeters}m)
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
