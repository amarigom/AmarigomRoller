"use client"

/**
 * InventoryView Component
 *
 * Vista de inventario con tarjetas de rollos de tela.
 * Muestra metros restantes, ancho, estado del stock y barra de progreso.
 * Preparado para conectar con: GET /api/inventory
 */

import { useState } from "react"
import { Package, Filter } from "lucide-react"
import type { FabricRoll, FabricType, StockStatus } from "@/lib/types/dashboard"
import { cn } from "@/lib/utils"
import { formatPrice } from "@/lib/utils"

interface InventoryViewProps {
  rolls: FabricRoll[]
  onDiscountStock: (rollId: string, meters: number) => void
}

const FABRIC_TYPE_LABELS: Record<FabricType, string> = {
  blackout: "Blackout",
  sunscreen: "Sunscreen",
  voile: "Voile",
}

const STATUS_CONFIG: Record<StockStatus, { label: string; className: string }> = {
  "in-stock": {
    label: "En Stock",
    className: "bg-[#7a9b76]/15 text-[#7a9b76] border-[#7a9b76]/30",
  },
  "low-stock": {
    label: "Stock Bajo",
    className: "bg-[#d4a843]/15 text-[#d4a843] border-[#d4a843]/30",
  },
  critical: {
    label: "Critico",
    className: "bg-[#c97676]/15 text-[#c97676] border-[#c97676]/30",
  },
}

const FABRIC_COLORS: Record<FabricType, string> = {
  blackout: "#6b6560",
  sunscreen: "#c9a961",
  voile: "#8ba4b8",
}

export default function InventoryView({ rolls, onDiscountStock }: InventoryViewProps) {
  const [filterType, setFilterType] = useState<FabricType | "all">("all")
  const [filterStatus, setFilterStatus] = useState<StockStatus | "all">("all")

  const filtered = rolls.filter((roll) => {
    if (filterType !== "all" && roll.fabricType !== filterType) return false
    if (filterStatus !== "all" && roll.status !== filterStatus) return false
    return true
  })

  const summary = {
    total: rolls.length,
    inStock: rolls.filter((r) => r.status === "in-stock").length,
    lowStock: rolls.filter((r) => r.status === "low-stock").length,
    critical: rolls.filter((r) => r.status === "critical").length,
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-serif text-2xl text-[#f5f0e8]">Inventario de Telas</h2>
          <p className="text-sm text-[#6b6560] mt-1">
            {filtered.length} rollo{filtered.length !== 1 ? "s" : ""} encontrado{filtered.length !== 1 ? "s" : ""}
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total Rollos", value: summary.total, color: "#f5f0e8" },
          { label: "En Stock", value: summary.inStock, color: "#7a9b76" },
          { label: "Stock Bajo", value: summary.lowStock, color: "#d4a843" },
          { label: "Critico", value: summary.critical, color: "#c97676" },
        ].map((item) => (
          <div
            key={item.label}
            className="bg-[#111111] border border-[#2a2520] rounded-lg p-4"
          >
            <p className="text-xs text-[#6b6560] mb-1">{item.label}</p>
            <p className="text-2xl font-serif" style={{ color: item.color }}>
              {item.value}
            </p>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3">
        <Filter size={14} className="text-[#6b6560]" />
        <div className="flex gap-2">
          {(["all", "blackout", "sunscreen", "voile"] as const).map((type) => (
            <button
              key={type}
              onClick={() => setFilterType(type)}
              className={cn(
                "px-3 py-1.5 rounded-md text-xs border transition-all",
                filterType === type
                  ? "bg-[#c9a961]/10 text-[#c9a961] border-[#c9a961]/30"
                  : "text-[#6b6560] border-[#2a2520] hover:border-[#3a3530]"
              )}
            >
              {type === "all" ? "Todos" : FABRIC_TYPE_LABELS[type]}
            </button>
          ))}
        </div>
        <div className="w-px h-4 bg-[#2a2520]" />
        <div className="flex gap-2">
          {(["all", "in-stock", "low-stock", "critical"] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={cn(
                "px-3 py-1.5 rounded-md text-xs border transition-all",
                filterStatus === status
                  ? "bg-[#c9a961]/10 text-[#c9a961] border-[#c9a961]/30"
                  : "text-[#6b6560] border-[#2a2520] hover:border-[#3a3530]"
              )}
            >
              {status === "all"
                ? "Todos"
                : STATUS_CONFIG[status].label}
            </button>
          ))}
        </div>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map((roll) => {
          const percentLeft = Math.round((roll.metersLeft / roll.totalMeters) * 100)
          const config = STATUS_CONFIG[roll.status]
          const accentColor = FABRIC_COLORS[roll.fabricType]

          return (
            <div
              key={roll.id}
              className="bg-[#111111] border border-[#2a2520] rounded-lg p-5 flex flex-col gap-4 hover:border-[#3a3530] transition-colors"
            >
              {/* Top row */}
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: `${accentColor}15` }}
                  >
                    <Package size={18} style={{ color: accentColor }} />
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-[#f5f0e8]">{roll.name}</h3>
                    <p className="text-xs text-[#6b6560] mt-0.5">
                      {FABRIC_TYPE_LABELS[roll.fabricType]} &middot; {roll.color}
                    </p>
                  </div>
                </div>
                <span
                  className={cn(
                    "text-[10px] px-2 py-0.5 rounded-full border font-medium",
                    config.className
                  )}
                >
                  {config.label}
                </span>
              </div>

              {/* Progress bar */}
              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-xs text-[#6b6560]">Metros restantes</span>
                  <span className="text-xs text-[#f5f0e8] font-medium">
                    {roll.metersLeft}m / {roll.totalMeters}m
                  </span>
                </div>
                <div className="h-1.5 bg-[#1a1a1a] rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${percentLeft}%`,
                      backgroundColor:
                        roll.status === "critical"
                          ? "#c97676"
                          : roll.status === "low-stock"
                          ? "#d4a843"
                          : "#7a9b76",
                    }}
                  />
                </div>
              </div>

              {/* Details */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Ancho</p>
                  <p className="text-sm text-[#f5f0e8]">{roll.widthCm} cm</p>
                </div>
                <div>
                  <p className="text-[10px] text-[#6b6560] uppercase tracking-wider">Precio/m</p>
                  <p className="text-sm text-[#c9a961]">{formatPrice(roll.pricePerMeter)}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {filtered.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <Package size={40} className="text-[#2a2520] mb-3" />
          <p className="text-[#6b6560] text-sm">No se encontraron rollos con los filtros seleccionados</p>
        </div>
      )}
    </div>
  )
}
