// app/(admin)/layout.tsx
"use client"

import { useState } from "react"
import Sidebar from "@/components/dashboard/Sidebar"

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false)

  // Datos de ejemplo (luego vendrán de tu base de datos)
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
      <main className="flex-1 overflow-y-auto p-8">
        {children}
      </main>
    </div>
  )
}