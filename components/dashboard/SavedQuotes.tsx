"use client"

import { useEffect, useState } from "react"
import { apiFetch, getSession } from "@/lib/api"
import type { ExplosionTotals, MaterialComponent, QuoteTotals, RecipeComponent } from "@/lib/types/recipe"

interface SavedQuote {
  id: number
  producto_nombre: string
  receta_version: number
  ancho_cm: number
  alto_cm: number
  referencia: string | null
  usuario: string | null
  creado_en: string
  resultado: (QuoteTotals & { explosion: MaterialComponent[] }) | (ExplosionTotals & { explosion: RecipeComponent[] })
}

export default function SavedQuotes({ refreshKey = 0 }: { refreshKey?: number }) {
  const [quotes, setQuotes] = useState<SavedQuote[]>([])
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)
  const canViewCosts = getSession()?.user.rol === "admin"

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const response = await apiFetch("/api/quotes/saved")
        const data = await response.json()
        if (!response.ok) throw new Error(data.message || "No se pudieron cargar los presupuestos")
        if (active) { setQuotes(data); setError("") }
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : "Error al cargar presupuestos")
      } finally {
        if (active) setLoading(false)
      }
    }
    void load()
    return () => { active = false }
  }, [refreshKey])

  return (
    <section className="mt-8 space-y-3 rounded-2xl border border-[#2a2520] bg-[#111111] p-5">
      <h2 className="font-serif text-xl text-[#c9a961]">Presupuestos guardados</h2>
      <p className="text-xs text-[#6b6560]">Importes{canViewCosts && " y costos"} conservados tal como se calcularon, sin reservar stock.</p>
      {error && <p className="text-sm text-red-300">{error}</p>}
      {loading && <p className="text-sm text-[#6b6560]">Cargando…</p>}
      {!loading && !error && !quotes.length && <p className="text-sm text-[#6b6560]">Todavía no hay presupuestos guardados.</p>}
      {quotes.map((q) => (
        <details key={q.id} className="rounded-lg border border-[#2a2520] p-3 text-sm text-[#f5f0e8]">
          <summary className="cursor-pointer">
            #{q.id} · {q.producto_nombre} · {q.ancho_cm} × {q.alto_cm} cm · ${q.resultado.total_presupuesto.toLocaleString("es-AR")}
          </summary>
          <p className="mt-2 text-xs text-[#a49b8e]">
            {new Date(q.creado_en).toLocaleString("es-AR")} · {q.usuario || "Sistema"} · receta v{q.receta_version}
            {q.referencia ? ` · ${q.referencia}` : ""}
          </p>
          <ul className="mt-2 space-y-1 text-xs text-[#a49b8e]">
            {q.resultado.explosion.map((item, index) => (
              <li key={index}>{item.componente}: {item.consumo_m_o_m2} {item.unidad}
                {canViewCosts && "precio_unitario" in item && typeof item.precio_unitario === "number" && ` · precio unitario $${item.precio_unitario.toLocaleString("es-AR")}`}
                {canViewCosts && "costo_parcial" in item && typeof item.costo_parcial === "number" && ` · costo $${item.costo_parcial.toLocaleString("es-AR")}`}
              </li>
            ))}
          </ul>
          <p className="mt-2 text-xs text-[#a49b8e]">
            {canViewCosts && "total" in q.resultado && `Fabricación $${q.resultado.total.toLocaleString("es-AR")} · `}
            cortina ${q.resultado.precio_producto.precio_venta_final.toLocaleString("es-AR")}
            {" "}· colocación y traslado ${q.resultado.servicio_colocacion.total_colocacion.toLocaleString("es-AR")}
          </p>
        </details>
      ))}
    </section>
  )
}
