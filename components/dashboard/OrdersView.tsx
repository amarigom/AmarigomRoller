"use client"

/**
 * OrdersView Component
 *
 * Vista de ordenes con tarjetas detalladas y timeline de estado.
 * Preparado para conectar con: GET /api/orders
 */

import { useState } from "react"
import { ClipboardList, Calendar, User, FileText } from "lucide-react"
import type { Order, OrderStatus } from "@/lib/types/dashboards"
import { cn, formatPrice } from "@/lib/utils"

interface OrdersViewProps {
  orders: Order[]
}

const STATUS_STEPS: OrderStatus[] = ["pending", "cutting", "production", "ready", "delivered"]

const STATUS_CONFIG: Record<OrderStatus, { label: string; color: string }> = {
  pending: { label: "Pendiente", color: "#6b6560" },
  cutting: { label: "Corte", color: "#6b9bc9" },
  production: { label: "Produccion", color: "#d4a843" },
  ready: { label: "Listo", color: "#c9a961" },
  delivered: { label: "Entregado", color: "#7a9b76" },
}

export default function OrdersView({ orders }: OrdersViewProps) {
  const [filterStatus, setFilterStatus] = useState<OrderStatus | "all">("all")

  const filtered = orders.filter((order) => {
    if (filterStatus === "all") return true
    return order.status === filterStatus
  })

  function getStepIndex(status: OrderStatus) {
    return STATUS_STEPS.indexOf(status)
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div>
        <h2 className="font-serif text-2xl text-[#f5f0e8]">Ordenes</h2>
        <p className="text-sm text-[#6b6560] mt-1">
          {filtered.length} orden{filtered.length !== 1 ? "es" : ""}
        </p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-5 gap-3">
        {STATUS_STEPS.map((status) => {
          const config = STATUS_CONFIG[status]
          const count = orders.filter((o) => o.status === status).length
          return (
            <div
              key={status}
              className="bg-[#111111] border border-[#2a2520] rounded-lg p-3 text-center"
            >
              <p className="text-xs text-[#6b6560] mb-1">{config.label}</p>
              <p className="text-xl font-serif" style={{ color: config.color }}>
                {count}
              </p>
            </div>
          )
        })}
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilterStatus("all")}
          className={cn(
            "px-3 py-1.5 rounded-md text-xs border transition-all",
            filterStatus === "all"
              ? "bg-[#c9a961]/10 text-[#c9a961] border-[#c9a961]/30"
              : "text-[#6b6560] border-[#2a2520] hover:border-[#3a3530]"
          )}
        >
          Todas
        </button>
        {STATUS_STEPS.map((status) => {
          const config = STATUS_CONFIG[status]
          return (
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
              {config.label}
            </button>
          )
        })}
      </div>

      {/* Orders List */}
      <div className="flex flex-col gap-4">
        {filtered.map((order) => {
          const currentStep = getStepIndex(order.status)
          const config = STATUS_CONFIG[order.status]

          return (
            <div
              key={order.id}
              className="bg-[#111111] border border-[#2a2520] rounded-lg p-6 hover:border-[#3a3530] transition-colors"
            >
              {/* Order Header */}
              <div className="flex items-start justify-between mb-5">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-[#c9a961]/10 flex items-center justify-center">
                    <ClipboardList size={18} className="text-[#c9a961]" />
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-[#f5f0e8]">{order.id.toUpperCase()}</h3>
                    <div className="flex items-center gap-3 mt-0.5">
                      <span className="flex items-center gap-1 text-xs text-[#6b6560]">
                        <User size={10} />
                        {order.clientName}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-[#6b6560]">
                        <Calendar size={10} />
                        {order.createdAt}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-serif text-[#c9a961]">{formatPrice(order.totalPrice)}</p>
                  <p className="text-[10px] text-[#6b6560]">
                    Entrega est.: {order.estimatedDelivery}
                  </p>
                </div>
              </div>

              {/* Progress Timeline */}
              <div className="flex items-center gap-1 mb-5">
                {STATUS_STEPS.map((step, i) => {
                  const stepConfig = STATUS_CONFIG[step]
                  const isCompleted = i <= currentStep
                  const isCurrent = i === currentStep
                  return (
                    <div key={step} className="flex-1 flex flex-col items-center gap-1.5">
                      <div className="w-full flex items-center">
                        <div
                          className={cn(
                            "flex-1 h-1 rounded-full transition-colors",
                            i === 0 ? "rounded-l-full" : "",
                            i === STATUS_STEPS.length - 1 ? "rounded-r-full" : ""
                          )}
                          style={{
                            backgroundColor: isCompleted ? config.color : "#1a1a1a",
                          }}
                        />
                      </div>
                      <span
                        className={cn(
                          "text-[9px] uppercase tracking-wider",
                          isCurrent ? "font-medium" : ""
                        )}
                        style={{ color: isCompleted ? stepConfig.color : "#3a3530" }}
                      >
                        {stepConfig.label}
                      </span>
                    </div>
                  )
                })}
              </div>

              {/* Items */}
              <div className="bg-[#0a0a0a] rounded-lg p-4">
                <div className="flex flex-col gap-2">
                  {order.items.map((item, i) => (
                    <div
                      key={i}
                      className="flex justify-between items-center text-sm"
                    >
                      <span className="text-[#a0998c]">{item.fabricName}</span>
                      <span className="text-[#6b6560]">
                        {item.widthCm}x{item.heightCm}cm &middot; {item.linearMeters}m
                      </span>
                    </div>
                  ))}
                </div>
                {order.notes && (
                  <div className="flex items-start gap-1.5 mt-3 pt-3 border-t border-[#2a2520]">
                    <FileText size={11} className="text-[#6b6560] mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-[#6b6560]">{order.notes}</p>
                  </div>
                )}
              </div>
            </div>
          )
        })}

        {filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 bg-[#111111] border border-[#2a2520] rounded-lg">
            <ClipboardList size={40} className="text-[#2a2520] mb-3" />
            <p className="text-sm text-[#6b6560]">No se encontraron ordenes</p>
          </div>
        )}
      </div>
    </div>
  )
}

