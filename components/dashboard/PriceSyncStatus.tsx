"use client"

import { useCallback, useEffect, useRef, useState } from "react"
import { apiFetch } from "@/lib/api"

interface SyncStatus {
  configurado: boolean
  ultimo_intento: string | null
  ultima_exitosa: string | null
  error: string | null
  actualizados: number | null
  omitidos: number | null
  advertencia: boolean
}

export default function PriceSyncStatus({ canManage = false, onSynced }: {
  canManage?: boolean
  onSynced?: () => void
}) {
  const [status, setStatus] = useState<SyncStatus | null>(null)
  const [error, setError] = useState("")
  const [busy, setBusy] = useState(false)
  const lastSuccess = useRef<string | null>(null)
  const initialized = useRef(false)
  const callback = useRef(onSynced)
  callback.current = onSynced

  const load = useCallback(async () => {
    try {
      const response = await apiFetch("/api/inventory/prices/sheets")
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || "No se pudo consultar la sincronización")
      if (initialized.current && data.ultima_exitosa !== lastSuccess.current) callback.current?.()
      initialized.current = true
      lastSuccess.current = data.ultima_exitosa
      setStatus(data)
      setError("")
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo consultar la sincronización")
    }
  }, [])

  useEffect(() => {
    void load()
    const timer = setInterval(() => void load(), 60000)
    return () => clearInterval(timer)
  }, [load])

  const sync = async () => {
    setBusy(true)
    setError("")
    try {
      const response = await apiFetch("/api/inventory/prices/sheets", { method: "POST" })
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || "No se pudo sincronizar")
      callback.current?.()
      await load()
    } catch (e) {
      await load()
      setError(e instanceof Error ? e.message : "No se pudo sincronizar")
    } finally {
      setBusy(false)
    }
  }

  const ultima = status?.ultima_exitosa
    ? new Date(status.ultima_exitosa).toLocaleString("es-AR", { timeZone: "America/Argentina/Buenos_Aires" })
    : "ninguna"
  return (
    <div className="my-4 rounded-lg border border-[#2a2520] bg-black/40 p-3 text-xs text-[#f5f0e8]">
      <p className="font-semibold text-[#c9a961]">Precios de Google Sheets</p>
      <p>Última sincronización exitosa: {ultima} (hora Argentina).</p>
      {status && !status.configurado && <p className="text-amber-300">Integración no configurada; se usan los precios guardados.</p>}
      {status?.configurado && status.advertencia && (
        <p className="text-amber-300">
          Precios posiblemente desactualizados; se usan los últimos guardados.
          {status.error ? ` ${status.error}` : ""}
        </p>
      )}
      {status?.ultima_exitosa && <p>Última ejecución exitosa: {status.actualizados} actualizados; {status.omitidos} artículos sin SKU coincidente.</p>}
      {error && <p className="text-red-300">No se pudo verificar o actualizar el estado: {error}</p>}
      {canManage && <button className="mt-2 text-[#c9a961] underline disabled:opacity-50" onClick={sync} disabled={busy}>
        {busy ? "Sincronizando…" : "Sincronizar ahora"}
      </button>}
    </div>
  )
}
