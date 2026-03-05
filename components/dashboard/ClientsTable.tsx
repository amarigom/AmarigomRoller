"use client"

/**
 * ClientsTable Component
 *
 * Tabla moderna de clientes con estados y busqueda.
 * Preparado para conectar con: GET /api/clients
 */

import { useState } from "react"
import { Search, Users, MapPin, Mail, Phone } from "lucide-react"
import type { Client, ClientStatus } from "@/lib/types/dashboards"
import { cn } from "@/lib/utils"

interface ClientsTableProps {
  clients: Client[]
}

const STATUS_CONFIG: Record<ClientStatus, { label: string; className: string }> = {
  quoted: {
    label: "Cotizado",
    className: "bg-[#6b9bc9]/15 text-[#6b9bc9] border-[#6b9bc9]/30",
  },
  "in-production": {
    label: "En Produccion",
    className: "bg-[#d4a843]/15 text-[#d4a843] border-[#d4a843]/30",
  },
  installed: {
    label: "Instalado",
    className: "bg-[#7a9b76]/15 text-[#7a9b76] border-[#7a9b76]/30",
  },
}

export default function ClientsTable({ clients }: ClientsTableProps) {
  const [search, setSearch] = useState("")
  const [filterStatus, setFilterStatus] = useState<ClientStatus | "all">("all")

  const filtered = clients.filter((client) => {
    const matchesSearch =
      client.name.toLowerCase().includes(search.toLowerCase()) ||
      client.address.toLowerCase().includes(search.toLowerCase()) ||
      client.email.toLowerCase().includes(search.toLowerCase())
    const matchesStatus = filterStatus === "all" || client.status === filterStatus
    return matchesSearch && matchesStatus
  })

  const summary = {
    total: clients.length,
    quoted: clients.filter((c) => c.status === "quoted").length,
    inProduction: clients.filter((c) => c.status === "in-production").length,
    installed: clients.filter((c) => c.status === "installed").length,
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div>
        <h2 className="font-serif text-2xl text-[#f5f0e8]">Clientes</h2>
        <p className="text-sm text-[#6b6560] mt-1">
          {filtered.length} cliente{filtered.length !== 1 ? "s" : ""}
        </p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total", value: summary.total, color: "#f5f0e8" },
          { label: "Cotizados", value: summary.quoted, color: "#6b9bc9" },
          { label: "En Produccion", value: summary.inProduction, color: "#d4a843" },
          { label: "Instalados", value: summary.installed, color: "#7a9b76" },
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

      {/* Search and Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1 relative">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#6b6560]" />
          <input
            type="text"
            placeholder="Buscar por nombre, direccion o email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#111111] border border-[#2a2520] rounded-lg pl-9 pr-4 py-2.5 text-sm text-[#f5f0e8] placeholder-[#3a3530] focus:outline-none focus:border-[#c9a961] transition-colors"
          />
        </div>
        <div className="flex gap-2">
          {(["all", "quoted", "in-production", "installed"] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={cn(
                "px-3 py-2 rounded-md text-xs border transition-all",
                filterStatus === status
                  ? "bg-[#c9a961]/10 text-[#c9a961] border-[#c9a961]/30"
                  : "text-[#6b6560] border-[#2a2520] hover:border-[#3a3530]"
              )}
            >
              {status === "all" ? "Todos" : STATUS_CONFIG[status].label}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-[#111111] border border-[#2a2520] rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[#2a2520]">
                <th className="text-left text-[10px] text-[#6b6560] uppercase tracking-wider px-5 py-3 font-medium">
                  Cliente
                </th>
                <th className="text-left text-[10px] text-[#6b6560] uppercase tracking-wider px-5 py-3 font-medium">
                  Contacto
                </th>
                <th className="text-left text-[10px] text-[#6b6560] uppercase tracking-wider px-5 py-3 font-medium">
                  Direccion
                </th>
                <th className="text-left text-[10px] text-[#6b6560] uppercase tracking-wider px-5 py-3 font-medium">
                  Estado
                </th>
                <th className="text-right text-[10px] text-[#6b6560] uppercase tracking-wider px-5 py-3 font-medium">
                  Ordenes
                </th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((client, i) => {
                const config = STATUS_CONFIG[client.status]
                return (
                  <tr
                    key={client.id}
                    className={cn(
                      "border-b border-[#2a2520]/50 hover:bg-[#1a1a1a]/50 transition-colors",
                      i === filtered.length - 1 && "border-b-0"
                    )}
                  >
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-[#c9a961]/10 flex items-center justify-center text-[#c9a961] text-xs font-medium flex-shrink-0">
                          {client.name.charAt(0)}
                        </div>
                        <span className="text-sm text-[#f5f0e8]">{client.name}</span>
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex flex-col gap-0.5">
                        <div className="flex items-center gap-1.5 text-xs text-[#a0998c]">
                          <Mail size={10} />
                          {client.email}
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-[#6b6560]">
                          <Phone size={10} />
                          {client.phone}
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-1.5 text-xs text-[#a0998c]">
                        <MapPin size={10} className="flex-shrink-0" />
                        {client.address}
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <span
                        className={cn(
                          "text-[10px] px-2 py-0.5 rounded-full border font-medium",
                          config.className
                        )}
                      >
                        {config.label}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-right">
                      <span className="text-sm text-[#f5f0e8]">{client.totalOrders}</span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12">
            <Users size={36} className="text-[#2a2520] mb-3" />
            <p className="text-sm text-[#6b6560]">No se encontraron clientes</p>
          </div>
        )}
      </div>
    </div>
  )
}
