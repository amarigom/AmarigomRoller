"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Package, Users, Calculator, ClipboardList, ChevronLeft, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

interface SidebarProps {
  collapsed: boolean
  onToggleCollapse: () => void
  stats: {
    totalRolls: number
    totalClients: number
    activeOrders: number
  }
}

const NAV_ITEMS = [
  { href: "/gestion/inventario", label: "Inventario", icon: Package },
  { href: "/gestion/clientes", label: "Clientes", icon: Users },
  { href: "/gestion/calculadora", label: "Calculadora de Corte", icon: Calculator },
  { href: "/gestion/ordenes", label: "Ordenes", icon: ClipboardList },
]

export default function Sidebar({ collapsed, onToggleCollapse, stats }: SidebarProps) {
  const pathname = usePathname() // Detecta la URL actual (ej: /gestion/inventario)

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
            <h1 className="font-serif text-lg text-[#c9a961] tracking-wider leading-tight uppercase">
              AMARIGOM
            </h1>
            <p className="text-[10px] text-[#6b6560] tracking-[0.2em] uppercase">
              Gestión Interna
            </p>
          </div>
        )}
      </div>

      {/* Navegación por Links */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-1">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href // Verifica si esta es la página actual
          
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 w-full",
                isActive
                  ? "bg-[#c9a961]/10 text-[#c9a961] border border-[#c9a961]/20"
                  : "text-[#a0998c] hover:bg-[#1a1a1a] hover:text-[#f5f0e8] border border-transparent"
              )}
            >
              <Icon size={18} className="flex-shrink-0" />
              {!collapsed && <span>{label}</span>}
            </Link>
          )
        })}
      </nav>

      {/* Estadísticas */}
      {!collapsed && (
        <div className="px-4 py-4 border-t border-[#2a2520]">
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center text-xs">
              <span className="text-[#6b6560]">Rollos</span>
              <span className="font-medium text-[#f5f0e8]">{stats.totalRolls}</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-[#6b6560]">Clientes</span>
              <span className="font-medium text-[#f5f0e8]">{stats.totalClients}</span>
            </div>
          </div>
        </div>
      )}

      {/* Botón de Colapsar */}
      <button
        onClick={onToggleCollapse}
        className="flex items-center justify-center py-3 border-t border-[#2a2520] text-[#6b6560] hover:text-[#c9a961]"
      >
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>
    </aside>
  )
}