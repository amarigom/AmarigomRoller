"use client"

import { useState } from "react" // Agregamos estado local para el móvil
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Package, Users, Calculator, ClipboardList, ChevronLeft, ChevronRight, Menu, X } from "lucide-react"
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
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false) // Estado para el menú en celular

  return (
    <>
      {/* --- BOTÓN HAMBURGUESA (Solo visible en celular/tablet) --- */}
      <div className="lg:hidden fixed top-4 left-4 z-[60]">
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2 bg-[#c9a961] text-[#0a0a0a] rounded-lg shadow-lg"
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* --- OVERLAY (Oscurece el fondo cuando el menú está abierto en móvil) --- */}
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-[40] lg:hidden" 
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* --- EL SIDEBAR --- */}
      <aside
        className={cn(
          // Clases base y desktop
          "flex flex-col h-screen bg-[#0e0e0e] border-r border-[#2a2520] transition-all duration-300 sticky top-0 z-[50]",
          // Comportamiento en Móvil: se oculta a la izquierda y sale con translate
          "fixed lg:sticky lg:translate-x-0",
          mobileOpen ? "translate-x-0 w-[260px]" : "-translate-x-full lg:translate-x-0",
          // Ancho en Desktop basado en colapso
          collapsed ? "lg:w-[72px]" : "lg:w-[260px]"
        )}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-6 border-b border-[#2a2520]">
          <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-[#c9a961] text-[#0a0a0a] flex-shrink-0">
            <span className="font-serif text-lg font-semibold leading-none">A</span>
          </div>
          {/* Mostramos texto si NO está colapsado O si estamos en móvil (donde no colapsa) */}
          {(!collapsed || mobileOpen) && (
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

        {/* Navegación */}
        <nav className="flex-1 px-3 py-4 flex flex-col gap-1">
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const isActive = pathname === href
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setMobileOpen(false)} // Cierra el menú al clickear en móvil
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 w-full",
                  isActive
                    ? "bg-[#c9a961]/10 text-[#c9a961] border border-[#c9a961]/20"
                    : "text-[#a0998c] hover:bg-[#1a1a1a] hover:text-[#f5f0e8] border border-transparent"
                )}
              >
                <Icon size={18} className="flex-shrink-0" />
                {(!collapsed || mobileOpen) && <span>{label}</span>}
              </Link>
            )
          })}
        </nav>

        {/* Estadísticas (Solo se ven si hay espacio) */}
        {(!collapsed || mobileOpen) && (
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

        {/* Botón de Colapsar (Oculto en móvil, no tiene sentido ahí) */}
        <button
          onClick={onToggleCollapse}
          className="hidden lg:flex items-center justify-center py-3 border-t border-[#2a2520] text-[#6b6560] hover:text-[#c9a961]"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </aside>
    </>
  )
}