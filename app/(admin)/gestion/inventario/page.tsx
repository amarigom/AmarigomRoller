"use client"

import { useState, useEffect } from "react"
import { Package, Plus, Search, Edit2 } from "lucide-react"
import { formatPrice } from "@/lib/utils"
import type { FabricRoll } from "@/lib/types/dashboards"

export default function InventarioPage() {
  const [rolls, setRolls] = useState<FabricRoll[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log("Iniciando carga de inventario...")
    fetch("/api/inventory")
      .then(res => res.json())
      .then(data => {
        console.log("Datos recibidos de la API:", data) // <--- ESTO ES CLAVE
        setRolls(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Error en el fetch:", err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="font-serif text-3xl text-[#f5f0e8]">Inventario de Rollos</h2>
          <p className="text-[#6b6560] mt-1 text-sm">Gestioná las telas disponibles</p>
        </div>
      </div>

      <div className="bg-[#111111] border border-[#2a2520] rounded-sm overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-[#0a0a0a] border-b border-[#2a2520]">
            <tr>
              <th className="px-6 py-4 text-xs font-medium text-[#6b6560] uppercase tracking-wider">Código</th>
              <th className="px-6 py-4 text-xs font-medium text-[#6b6560] uppercase tracking-wider">Nombre</th>
              <th className="px-6 py-4 text-xs font-medium text-[#6b6560] uppercase tracking-wider text-right">Stock (m)</th>
              <th className="px-6 py-4 text-xs font-medium text-[#6b6560] uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#2a2520]">
            {loading ? (
              <tr key="loading"><td colSpan={4} className="px-6 py-10 text-center text-gray-500 italic">Cargando...</td></tr>
            ) : rolls && rolls.length > 0 ? (
              rolls.map((roll, index) => (
                <tr key={roll.id || index} className="hover:bg-white/[0.02]">
                  <td className="px-6 py-4 text-sm font-mono text-[#c9a961]">{roll.code}</td>
                  <td className="px-6 py-4 text-sm text-white">{roll.name}</td>
                  <td className="px-6 py-4 text-sm text-right text-green-400">{roll.metersLeft} m</td>
                  <td className="px-6 py-4">
                    <button className="text-[#6b6560] hover:text-[#c9a961]"><Edit2 size={16} /></button>
                  </td>
                </tr>
              ))
            ) : (
              <tr key="empty"><td colSpan={4} className="px-6 py-10 text-center text-gray-500 italic">No hay datos (Rolls está vacío)</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}