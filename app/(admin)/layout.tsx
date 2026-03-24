// app/(admin)/layout.tsx
"use client"

import { useState } from "react"
import Sidebar from "@/components/dashboard/Sidebar"

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false)

  // Datos de ejemplo
  const stats = {
    totalRolls: 24,
    totalClients: 85,
    activeOrders: 3
  }

  return (
    <div className="flex min-h-screen bg-[#0a0a0a]">
      <Sidebar 
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed(!collapsed)}
        stats={stats}
      />
      
      {/* Ajustamos el main:
          1. 'w-full' para que ocupe todo en móvil.
          2. 'p-4' en móvil (más espacio útil) y 'md:p-8' en PC.
          3. 'mt-16' o similar en móvil para que el botón hamburguesa no tape el título.
      */}
      <main className="flex-1 w-full min-w-0 overflow-y-auto p-4 md:p-8 mt-14 lg:mt-0">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  )
}