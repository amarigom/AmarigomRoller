"use client"

import { useCallback, useEffect, useState } from "react"
import { apiFetch, getSession } from "@/lib/api"

interface ComponentDetail {
  componente: string
  consumo_m_o_m2: number
  unidad: string
  costo_parcial?: number
  metodo: string
}

interface Production {
  id: number
  producto_id: number
  producto_nombre: string
  receta_version: number
  ancho_cm: number
  alto_cm: number
  opciones: Record<string, string | number>
  referencia: string | null
  total_materiales?: number
  total_minutos: number
  total_mano_obra?: number
  total_desgaste?: number
  total?: number
  detalle: ComponentDetail[]
  usuario: string | null
  creado_en: string
}

export default function ProductionHistory({ refreshKey = 0 }: { refreshKey?: number }) {
  const [producciones, setProducciones] = useState<Production[]>([])
  const [referencia, setReferencia] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const canViewCosts = getSession()?.user.rol === "admin"

  const cargar = useCallback(async () => {
    setLoading(true)
    setError("")
    try {
      const params = new URLSearchParams({ limit: "100" })
      if (referencia.trim()) params.set("referencia", referencia.trim())
      const response = await apiFetch(`/api/recipes/productions?${params}`)
      const data = await response.json().catch(() => ({}))
      if (!response.ok) throw new Error(data.message || "No se pudo cargar el historial")
      setProducciones(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al cargar producciones")
    } finally {
      setLoading(false)
    }
  }, [referencia])

  useEffect(() => {
    cargar()
  }, [cargar, refreshKey])

  return (
    <section className="mt-8 space-y-4 rounded-2xl border border-[#2a2520] bg-[#111111] p-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
        <div>
          <h2 className="font-serif text-xl text-[#c9a961]">Historial de producciones</h2>
          <p className="mt-1 text-xs text-[#6b6560]">Quién produjo cada producto, cuándo y con qué receta{canViewCosts && " y costo"}.</p>
        </div>
        <div className="flex gap-2">
          <input
            className="rounded-lg border border-[#2a2520] bg-black px-3 py-2 text-sm text-[#f5f0e8] outline-none focus:border-[#c9a961]"
            value={referencia}
            onChange={(e) => setReferencia(e.target.value)}
            placeholder="Filtrar por referencia"
          />
          <button
            className="rounded-lg border border-[#2a2520] px-3 py-2 text-xs text-[#c9a961] hover:border-[#c9a961]"
            onClick={cargar}
            disabled={loading}
          >
            BUSCAR
          </button>
        </div>
      </div>
      {error && <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-xs text-red-200">{error}</p>}
      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px] text-left text-xs text-[#f5f0e8]">
          <thead className="text-[10px] uppercase tracking-wider text-[#6b6560]">
            <tr>
              <th className="p-2">Fecha</th>
              <th className="p-2">Producto / medidas</th>
              <th className="p-2">Referencia</th>
              <th className="p-2">Usuario</th>
              <th className="p-2">Receta</th>
              {canViewCosts && <th className="p-2 text-right">Total</th>}
              <th className="p-2">Detalle</th>
            </tr>
          </thead>
          <tbody>
            {producciones.map((p) => (
              <tr key={p.id} className="border-t border-[#2a2520] align-top">
                <td className="whitespace-nowrap p-2 text-[#a49b8e]">
                  {new Date(`${p.creado_en}Z`).toLocaleString("es-AR")}
                </td>
                <td className="p-2">
                  {p.producto_nombre}
                  <span className="block text-[#6b6560]">{p.ancho_cm} × {p.alto_cm} cm</span>
                  {Object.keys(p.opciones).length > 0 && (
                    <span className="block text-[#6b6560]">
                      {Object.entries(p.opciones).map(([k, v]) => `${k}: ${v}`).join(" · ")}
                    </span>
                  )}
                </td>
                <td className="p-2">{p.referencia || "—"}</td>
                <td className="p-2">{p.usuario || "Sistema"}</td>
                <td className="p-2">v{p.receta_version}</td>
                {canViewCosts && <td className="whitespace-nowrap p-2 text-right text-[#c9a961]">
                  {p.total != null ? `$${p.total.toLocaleString("es-AR")}` : "—"}
                </td>}
                <td className="p-2">
                  <details>
                    <summary className="cursor-pointer text-[#c9a961]">Ver</summary>
                    <ul className="mt-2 space-y-1">
                      {p.detalle.map((d, i) => (
                        <li key={`${p.id}-${i}`} className="text-[#a49b8e]">
                          {d.componente}: {d.consumo_m_o_m2} {d.unidad}{canViewCosts && d.costo_parcial != null && ` · $${d.costo_parcial.toLocaleString("es-AR")}`}
                        </li>
                      ))}
                    </ul>
                    <p className="mt-1 text-[#6b6560]">
                      Mano de obra {p.total_minutos} min
                      {canViewCosts && p.total_materiales != null && ` · materiales $${p.total_materiales.toLocaleString("es-AR")}`}
                      {canViewCosts && p.total_mano_obra != null && ` · mano de obra $${p.total_mano_obra.toLocaleString("es-AR")}`}
                      {canViewCosts && p.total_desgaste != null && ` · desgaste $${p.total_desgaste.toLocaleString("es-AR")}`}
                    </p>
                  </details>
                </td>
              </tr>
            ))}
            {!loading && producciones.length === 0 && (
              <tr><td colSpan={7} className="p-5 text-center text-[#6b6560]">Todavía no hay producciones registradas.</td></tr>
            )}
            {loading && (
              <tr><td colSpan={7} className="p-5 text-center text-[#6b6560]">Cargando historial…</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
