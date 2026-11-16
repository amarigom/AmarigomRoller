"use client"

import { useEffect, useState } from "react"
import { apiFetch } from "@/lib/api"

interface Piece {
  id: number | null
  longitud_original_cm: string
  longitud_actual_cm: string
  es_retazo: boolean
}
interface Snapshot {
  stock: string
  unidad: string
  saldo_historial: string | null
  piezas: Piece[]
}

const field = "rounded-lg border border-[#2a2520] bg-black px-2 py-1 text-sm text-[#f5f0e8]"
const button = "rounded-lg border border-[#c9a961] px-3 py-1.5 text-xs text-[#c9a961] disabled:opacity-50"

export default function ProfileReconciliation({ id, largo, onChanged }: {
  id: number
  largo: number | null
  onChanged: () => void
}) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null)
  const [pieces, setPieces] = useState<Piece[]>([])
  const [reason, setReason] = useState("")
  const [error, setError] = useState("")
  const [info, setInfo] = useState("")
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    setSnapshot(null)
    setPieces([])
    setReason("")
    setError("")
    setInfo("")
  }, [id])

  const load = async () => {
    setBusy(true)
    setError("")
    setInfo("")
    try {
      const res = await apiFetch(`/api/inventory/${id}/pieces/reconcile`)
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || "No se pudo consultar las piezas")
      setSnapshot(data)
      setPieces(data.piezas.map((p: Piece) => ({ ...p })))
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al consultar las piezas")
    } finally {
      setBusy(false)
    }
  }

  const change = (index: number, patch: Partial<Piece>) =>
    setPieces(prev => prev.map((p, i) => i === index ? { ...p, ...patch } : p))

  const save = async () => {
    if (!snapshot || !window.confirm("Se ajustará el stock según las piezas contadas y se registrará el motivo. ¿Continuar?")) return
    setBusy(true)
    setError("")
    setInfo("")
    try {
      const res = await apiFetch(`/api/inventory/${id}/pieces/reconcile`, {
        method: "POST",
        body: JSON.stringify({ stock_esperado: snapshot.stock, piezas_esperadas: snapshot.piezas, piezas: pieces, motivo: reason }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error([data.message, ...(data.detalles || [])].join(": "))
      setSnapshot(null)
      setPieces([])
      setReason("")
      setInfo(`Conciliación registrada. Ajuste: ${data.cantidad}; saldo: ${data.stock_resultante} ${snapshot.unidad}.`)
      onChanged()
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al conciliar")
    } finally {
      setBusy(false)
    }
  }

  const total = pieces.reduce((sum, p) => sum + (Number(p.longitud_actual_cm) || 0), 0)
  const proposed = total / (snapshot?.unidad === "metro" ? 100 : 1)

  return <div className="space-y-2 border-t border-[#2a2520] pt-3">
    <h4 className="text-xs font-semibold text-[#f5f0e8]">Conciliar barras y retazos</h4>
    <p className="text-xs text-[#6b6560]">Contá las piezas reales. Para retirar una pieza existente, indicá longitud 0. No se eliminan sus registros.</p>
    <button className={button} disabled={busy} onClick={load}>CARGAR PIEZAS Y SALDO</button>
    {error && <p role="alert" className="text-xs text-red-300">{error}</p>}
    {info && <p className="text-xs text-green-300">{info}</p>}
    {snapshot && <>
      <p className="text-xs text-[#f5f0e8]">Saldo actual: {snapshot.stock} {snapshot.unidad} · piezas contadas: {total.toFixed(2)} cm · saldo propuesto: {proposed.toFixed(4)} {snapshot.unidad}</p>
      <p className="text-xs text-[#f5f0e8]">Ajuste de stock: {(proposed - Number(snapshot.stock)).toFixed(4)} {snapshot.unidad}</p>
      {snapshot.saldo_historial === null
        ? <p className="text-xs text-amber-300">El historial tiene unidades distintas y debe revisarse antes de conciliar.</p>
        : Number(snapshot.saldo_historial) !== Number(snapshot.stock) && <p className="text-xs text-amber-300">
          El historial suma {snapshot.saldo_historial} {snapshot.unidad}; se registrará una regularización separada por
          {" "}{(Number(snapshot.stock) - Number(snapshot.saldo_historial)).toFixed(4)} {snapshot.unidad}.
        </p>}
      <div className="max-h-80 space-y-2 overflow-auto">
        {pieces.map((p, index) => <div key={p.id ?? `new-${index}`} className="flex flex-wrap items-center gap-2 text-xs text-[#f5f0e8]">
          <span>{p.id ? `#${p.id}` : "Nueva"}</span>
          <span>Original: {p.longitud_original_cm} cm</span>
          <label>Actual (cm): <input aria-label={`Longitud actual pieza ${p.id ?? `nueva ${index + 1}`}`} className={`${field} w-24`} type="number" min="0" step="0.01"
            value={p.longitud_actual_cm} onChange={e => change(index, { longitud_actual_cm: e.target.value })} /></label>
          <label><input type="checkbox" checked={p.es_retazo} onChange={e => change(index, { es_retazo: e.target.checked })} /> Retazo</label>
          {!p.id && <button className={button} onClick={() => setPieces(prev => prev.filter((_, i) => i !== index))}>Quitar</button>}
        </div>)}
      </div>
      <button className={button} disabled={busy || !largo} onClick={() => setPieces(prev => [...prev, {
        id: null, longitud_original_cm: String(largo), longitud_actual_cm: String(largo), es_retazo: false,
      }])}>AGREGAR BARRA O RETAZO</button>
      <input className={`${field} w-full`} placeholder="Motivo obligatorio del ajuste" value={reason} onChange={e => setReason(e.target.value)} />
      <button className={button} disabled={busy || !reason.trim() || pieces.some(p => p.longitud_actual_cm === "")} onClick={save}>CONFIRMAR CONCILIACIÓN</button>
    </>}
  </div>
}
