"use client"

import { useState, useEffect } from "react"
// Si InventoryView está en la misma carpeta, queda así:
import InventoryView from "./InventoryView" 
// Asegurate que la ruta a tus tipos sea la correcta
import type { Supply } from "@/lib/types/dashboards"

const mapBackendToFrontend = (backendRoll: any): Supply => {
  return {
    id: backendRoll.id,
    name: backendRoll.name,
    category: backendRoll.category ,
    code: backendRoll.code,
    metersLeft: backendRoll.metersLeft,
    totalMeters: backendRoll.totalMeters,
    widthCm: backendRoll.widthCm,
    pricePerMeter: backendRoll.pricePerMeter,
    status: backendRoll.status === "in_stock" ? "in-stock" : backendRoll.status,
    // para cumplir con la interfaz FabricRoll si es necesario
    //createdAt: new Date().toISOString(),
    //updatedAt: new Date().toISOString()
  }
}

export default function InventoryPage() {
  const [rolls, setRolls] = useState<Supply[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        
        const response = await fetch("https://amarigom-roller.vercel.app/api/inventory")
        
        if (!response.ok) throw new Error(`Error: ${response.statusText}`)
        
        const data = await response.json()
        setRolls(data.map(mapBackendToFrontend))
      } catch (err: any) {
        setError(err.message || "Error de conexión")
      } finally {
        setLoading(false)
      }
    }
    fetchInventory()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#0a0a0a] gap-4">
        <div className="w-8 h-8 border-2 border-[#c9a961] border-t-transparent rounded-full animate-spin" />
        <p className="font-serif text-[#c9a961]">Sincronizando AMARIGOM...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0a0a0a]">
        <div className="p-6 bg-[#c97676]/10 border border-[#c97676]/30 rounded-lg text-[#c97676] text-center">
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="mt-4 underline text-xs">REINTENTAR</button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 lg:p-10 bg-[#0a0a0a] min-h-screen">
      <InventoryView rolls={rolls} onDiscountStock={() => {}} />
    </div>
  )
}