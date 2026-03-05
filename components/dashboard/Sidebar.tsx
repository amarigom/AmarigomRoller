"use client"

/**
 * Sidebar Component
 *
 * Navegacion lateral del dashboard.
 * Muestra el logo, las secciones y estadisticas rapidas.
 */

import { Package, Users, Calculator, ClipboardList, ChevronLeft, ChevronRight } from "lucide-react"
import type { DashboardView } from "@/lib/types/dashboard"
import { cn } from "@/lib/utils"

interface SidebarProps {
  activeView: DashboardView
  onViewChange: (view: DashboardView) => void
  collapsed: boolean
  onToggleCollapse: () => void
  stats: {
    totalRolls: number
    totalClients: number
    activeOrders: number
  }
}

const NAV_ITEMS: { view: DashboardView; label: string; icon: typeof Package }[] = [
  { view: "inventory", label: "Inventario", icon: Package },
  { view: "clients", label: "Clientes", icon: Users },
  { view: "calculator", label: "Calculadora de Corte", icon: Calculator },
  { view: "orders", label: "Ordenes", icon: ClipboardList },
]

export default function Sidebar({
  activeView,
  onViewChange,
  collapsed,
  onToggleCollapse,
  stats,
}: SidebarProps) {
  return (
    <aside
      className={cn(
        "flex flex-col h-screen bg-[#0e0e0e] border-r border-[#2a2520] transition-all duration-300 sticky top-0",
        collapsed ? "w-[72px]" : "w-[260px]"
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-6 border-b border-[#2a2520]">
        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-[#c9a961] text-[#0a0a0a] flex-shrink-0">
          <span className="font-serif text-lg font-semibold leading-none">A</span>
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <h1 className="font-serif text-lg text-[#c9a961] tracking-wider leading-tight">
              AMARIGOM
            </h1>
            <p className="text-[10px] text-[#6b6560] tracking-[0.2em] uppercase">
              Panel de gestion
            </p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-1">
        {NAV_ITEMS.map(({ view, label, icon: Icon }) => {
          const isActive = activeView === view
          return (
            <button
              key={view}
              onClick={() => onViewChange(view)}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 w-full text-left",
                isActive
                  ? "bg-[#c9a961]/10 text-[#c9a961] border border-[#c9a961]/20"
                  : "text-[#a0998c] hover:bg-[#1a1a1a] hover:text-[#f5f0e8] border border-transparent"
              )}
              title={collapsed ? label : undefined}
            >
              <Icon size={18} className="flex-shrink-0" />
              {!collapsed && <span>{label}</span>}
            </button>
          )
        })}
      </nav>

      {/* Stats - solo visible si esta expandido */}
      {!collapsed && (
        <div className="px-4 py-4 border-t border-[#2a2520]">
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <span className="text-xs text-[#6b6560]">Rollos</span>
              <span className="text-xs font-medium text-[#f5f0e8]">{stats.totalRolls}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs text-[#6b6560]">Clientes</span>
              <span className="text-xs font-medium text-[#f5f0e8]">{stats.totalClients}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs text-[#6b6560]">Ordenes activas</span>
              <span className="text-xs font-medium text-[#c9a961]">{stats.activeOrders}</span>
            </div>
          </div>
        </div>
      )}

      {/* Collapse Toggle */}
      <button
        onClick={onToggleCollapse}
        className="flex items-center justify-center py-3 border-t border-[#2a2520] text-[#6b6560] hover:text-[#c9a961] transition-colors"
      >
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>
    </aside>
  )
}
