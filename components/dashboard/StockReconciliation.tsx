"use client"

import { useState } from "react"
import { apiFetch } from "@/lib/api"

interface Snapshot {
  stock: string
  historial: string
  diferencia: string
  unidad: string
}

const field = "w-full rounded-lg border border-[#2a2520] bg-black px-2 py-1 text-sm text-[#f5f0e8]"
const button = "rounded-lg border border-[#c9a961] px-3 py-1.5 text-xs text-[#c9a961] disabled:opacity-50"

export default function StockReconciliation({ id, onChanged }: { id: number; onChanged: () => void }) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null)
  const [count, setCount] = useState("")
  const [reason, setReason] = useState("")
  const [message, setMessage] = useState("")
  const [busy, setBusy] = useState(false)
  const load = async () => {
    setBusy(true)
    setMessage("")
    try {
      const res = await apiFetch(`/api/inventory/${id}/reconcile`)
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || "No se pudo consultar la conciliación")
      setSnapshot(data)
      setCount(data.stock)
    } catch (e) {
      setSnapshot(null)
      setMessage(e instanceof Error ? e.message : "Error al consultar")
    } finally { setBusy(false) }
  }
  const save = async () => {
    if (!snapshot || !window.confirm("Se registrarán los ajustes indicados. ¿Confirmar el conteo?")) return
    setBusy(true)
    setMessage("")
    try {
      const res = await apiFetch(`/api/inventory/${id}/reconcile`, {
        method: "POST",
        body: JSON.stringify({ stock_esperado: snapshot.stock, historial_esperado: snapshot.historial,
          stock_contado: count, motivo: reason }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error([data.message, ...(data.detalles || [])].join(": "))
      setSnapshot(null)
      setReason("")
      setMessage(`Conciliación registrada. Saldo: ${data.stock} ${data.unidad}.`)
      onChanged()
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Error al conciliar")
    } finally { setBusy(false) }
  }
  return <div className="space-y-2 border-t border-[#2a2520] pt-3">
    <h4 className="text-xs font-semibold text-[#f5f0e8]">Auditar y conciliar stock</h4>
    <button className={button} disabled={busy} onClick={load}>CONSULTAR SALDO E HISTORIAL</button>
    {message && <p role="status" className="text-xs text-[#f5f0e8]">{message}</p>}
    {snapshot && <>
      <p className="text-xs text-[#f5f0e8]">Saldo: {snapshot.stock} {snapshot.unidad} · movimientos: {snapshot.historial} {snapshot.unidad} · diferencia: {snapshot.diferencia} {snapshot.unidad}</p>
      <p className="text-xs text-[#6b6560]">Si el historial no explica el saldo se registrará una regularización separada; el conteo ajusta el stock físico.</p>
      <label className="block text-xs text-[#f5f0e8]">Stock contado ({snapshot.unidad})
        <input className={field} type="number" min="0" step="0.0001" value={count} onChange={e => setCount(e.target.value)} />
      </label>
      {count !== "" && Number.isFinite(Number(count)) && <p className="text-xs text-[#f5f0e8]">
        Ajuste de conteo previsto: {(Number(count) - Number(snapshot.stock)).toLocaleString("es-AR", { maximumFractionDigits: 4 })} {snapshot.unidad}
      </p>}
      <input className={field} placeholder="Motivo obligatorio" value={reason} onChange={e => setReason(e.target.value)} />
      <button className={button} disabled={busy || count === "" || !reason.trim()} onClick={save}>CONFIRMAR CONCILIACIÓN</button>
    </>}
  </div>
}
