"use client"

import { useCallback, useEffect, useState } from "react"
import { apiFetch, getSession, hasPermission } from "@/lib/api"
import ProfileReconciliation from "./ProfileReconciliation"
import StockReconciliation from "./StockReconciliation"
import PriceSyncStatus from "./PriceSyncStatus"
import { displayNumber, linearDisplay } from "@/lib/display-units"

interface Supply {
  id: number
  name: string
  unit: string | null
  metersLeft: number
  stock_minimo: number
  price?: number
  es_tela: boolean
  precio_m2?: number | null
  widthCm: number
  largo_pieza_cm: number | null
  perfil_en_receta: boolean
  unidad_compra: string | null
  factor_conversion: number | null
}
interface Movement {
  id: number
  tipo: string
  cantidad: number
  stock_resultante: number
  referencia: string | null
  notas: string | null
  creado_en: string
  usuario: string | null
  unidad: string | null
}
interface PriceHistory {
  id: number
  precio: number
  precio_m2: number | null
  vigente_desde: string
  motivo: string | null
  usuario: string | null
  unidad: string | null
}
interface Alert {
  id_insumo: number
  insumo: string
  stock_actual: number
  stock_minimo: number
  faltante: number
  unidad: string | null
}
interface Scrap {
  id: number
  insumo: string
  ancho_cm: number
  largo_cm: number
  fecha_generado: string
  referencia: string | null
  estado: "disponible" | "reservado"
}

const field =
  "w-full rounded-lg border border-[#2a2520] bg-black px-3 py-2 text-sm text-[#f5f0e8] outline-none focus:border-[#c9a961]"
const button =
  "rounded-lg bg-[#c9a961] px-4 py-2 text-xs font-bold text-black hover:bg-[#d4b574] disabled:opacity-50"
const outline =
  "rounded-lg border border-[#2a2520] px-3 py-1.5 text-xs text-[#c9a961] hover:border-[#c9a961] disabled:opacity-50"

async function errorMessage(res: Response) {
  const body = await res.json().catch(() => ({}))
  const details = Array.isArray(body.detalles) ? `: ${body.detalles.join("; ")}` : ""
  return `${body.message || "No se pudo completar la operación"}${details}`
}

export default function InventoryOperations({ refreshKey = 0, onChanged }: { refreshKey?: number; onChanged?: () => void }) {
  const [supplies, setSupplies] = useState<Supply[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [scraps, setScraps] = useState<Scrap[]>([])
  const [movements, setMovements] = useState<Movement[]>([])
  const [prices, setPrices] = useState<PriceHistory[]>([])
  const [selectedId, setSelectedId] = useState("")
  const [tipo, setTipo] = useState<"entrada" | "ajuste">("entrada")
  const [cantidad, setCantidad] = useState("")
  const [cantidadPiezas, setCantidadPiezas] = useState("")
  const [referencia, setReferencia] = useState("")
  const [notas, setNotas] = useState("")
  const [minimo, setMinimo] = useState("")
  const [porcentaje, setPorcentaje] = useState("")
  const [motivo, setMotivo] = useState("")
  const [preciosCsv, setPreciosCsv] = useState("")
  const [telasCsv, setTelasCsv] = useState("")
  const [anchoTela, setAnchoTela] = useState("")
  const [largoRollo, setLargoRollo] = useState("")
  const [unidadCompra, setUnidadCompra] = useState("")
  const [factorCompra, setFactorCompra] = useState("")
  const [cantidadCompra, setCantidadCompra] = useState("")
  const [reservaRef, setReservaRef] = useState("")
  const [error, setError] = useState("")
  const [info, setInfo] = useState("")
  const [busy, setBusy] = useState(false)
  const [canWrite, setCanWrite] = useState(false)
  const [canManage, setCanManage] = useState(false)
  const selected = supplies.find((s) => String(s.id) === selectedId)

  useEffect(() => {
    setAnchoTela(selected?.widthCm ? String(selected.widthCm) : "")
    setLargoRollo(selected?.largo_pieza_cm ? String(selected.largo_pieza_cm) : "")
    setUnidadCompra(selected?.unidad_compra || "")
    setFactorCompra(selected?.factor_conversion != null ? String(selected.factor_conversion) : "")
  }, [selectedId])

  useEffect(() => {
    const session = getSession()
    setCanWrite(hasPermission(session, "inventory:write"))
    setCanManage(hasPermission(session, "inventory:manage"))
  }, [])

  const cargar = useCallback(async () => {
    const [stockRes, alertRes, scrapRes] = await Promise.all([
      apiFetch("/api/inventory"),
      apiFetch("/api/inventory/alerts"),
      apiFetch("/api/inventory/scraps"),
    ])
    for (const res of [stockRes, alertRes, scrapRes]) {
      if (!res.ok) throw new Error(await errorMessage(res))
    }
    const stock: Supply[] = await stockRes.json()
    setSupplies(stock)
    setAlerts(await alertRes.json())
    setScraps(await scrapRes.json())
    if (!selectedId && stock.length) setSelectedId(String(stock[0].id))
  }, [selectedId])

  useEffect(() => {
    cargar().catch((e) => setError(e instanceof Error ? e.message : "Error al cargar inventario"))
  }, [cargar, refreshKey])

  const cargarDetalle = useCallback(async () => {
    if (!selectedId) return
    const movementRes = await apiFetch(`/api/inventory/${selectedId}/movements?limit=20`)
    if (!movementRes.ok) throw new Error(await errorMessage(movementRes))
    setMovements(await movementRes.json())
    if (canManage) {
      const priceRes = await apiFetch(`/api/inventory/${selectedId}/prices`)
      if (!priceRes.ok) throw new Error(await errorMessage(priceRes))
      setPrices(await priceRes.json())
    }
  }, [selectedId, canManage])

  useEffect(() => {
    cargarDetalle().catch((e) => setError(e instanceof Error ? e.message : "Error al cargar historial"))
  }, [cargarDetalle])

  const ejecutar = async (fn: () => Promise<string>) => {
    setBusy(true)
    setError("")
    setInfo("")
    try {
      setInfo(await fn())
      await Promise.all([cargar(), cargarDetalle()])
      onChanged?.()
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error inesperado")
    } finally {
      setBusy(false)
    }
  }

  const registrarMovimiento = () => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/${selectedId}/movements`, {
      method: "POST",
      body: JSON.stringify({
        tipo, cantidad: Number(cantidad), referencia: referencia || null, notas: notas || null,
      }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    setCantidad("")
    setReferencia("")
    setNotas("")
    return "Movimiento de stock registrado."
  })

  const guardarMinimo = () => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/${selectedId}/minimum`, {
      method: "PATCH", body: JSON.stringify({ stock_minimo: Number(minimo) }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    return "Stock mínimo actualizado."
  })

  const ingresarPiezas = () => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/${selectedId}/pieces`, {
      method: "POST", body: JSON.stringify({ cantidad: Number(cantidadPiezas), referencia: referencia || null }),
    })

    if (!res.ok) throw new Error(await errorMessage(res))
    setCantidadPiezas("")
    return "Piezas físicas ingresadas."
  })

  const ingresarCompra = () => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/${selectedId}/purchases`, {
      method: "POST", body: JSON.stringify({ cantidad: cantidadCompra, referencia: referencia || null }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    setCantidadCompra("")
    return "Compra ingresada y convertida a la unidad de stock."
  })

  const actualizarPrecios = (modo: "porcentaje" | "lista") => ejecutar(async () => {
    const body = modo === "porcentaje"
      ? { porcentaje: Number(porcentaje), motivo: motivo || null }
      : {
          items: preciosCsv.split(/\r?\n/).filter((line) => line.trim()).map((line, index) => {
            const columns = line.split(";").map((v) => v.trim())
            const [id, precio] = columns
            if (columns.length !== 2 || !/^[1-9]\d*$/.test(id) || !/^\d+(?:[.,]\d+)?$/.test(precio)) {
              throw new Error(`Línea ${index + 1}: indicá id;precio válidos`)
            }
            return { id_insumo: Number(id), precio: Number(precio.replace(",", ".")) }
          }),
          motivo: motivo || "Lista de proveedor",
        }
    const res = await apiFetch("/api/inventory/prices", { method: "POST", body: JSON.stringify(body) })
    if (!res.ok) throw new Error(await errorMessage(res))
    const data = await res.json()
    return `Precios actualizados: ${data.actualizados}. Los cálculos siguientes usarán esos valores.`
  })

  const configurarTela = () => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/${selectedId}/fabric`, {
      method: "PATCH",
      body: JSON.stringify({
        ancho_cm: Number(anchoTela), largo_pieza_cm: largoRollo ? Number(largoRollo) : null,
        unidad_compra: unidadCompra || null, factor_conversion: factorCompra || null,
      }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    return "Tela configurada; el stock y el precio base deben estar en metros lineales."
  })

  const importarTelas = (aplicar: boolean) => ejecutar(async () => {
    const res = await apiFetch("/api/inventory/prices/fabrics/import", {
      method: "POST", body: JSON.stringify({ csv: telasCsv, aplicar, motivo: motivo || null }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    const data = await res.json()
    return aplicar ? `Lista aplicada: ${data.actualizados} precios actualizados.` : `Lista válida: ${data.filas} filas. Podés aplicarla.`
  })

  const reservar = (scrapId: number) => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/scraps/${scrapId}/reserve`, {
      method: "POST", body: JSON.stringify({ referencia: reservaRef }),
    })
    if (!res.ok) throw new Error(await errorMessage(res))
    return `Retazo reservado para "${reservaRef}".`
  })

  const liberar = (scrapId: number) => ejecutar(async () => {
    const res = await apiFetch(`/api/inventory/scraps/${scrapId}/release`, { method: "POST" })
    if (!res.ok) throw new Error(await errorMessage(res))
    return "Reserva liberada."
  })

  return (
    <section className="space-y-5 rounded-2xl border border-[#c9a961]/20 bg-[#111111] p-5">
      <div>
        <h2 className="font-serif text-xl text-[#c9a961]">Control de stock{canManage && " y costos"}</h2>
        <p className="mt-1 text-xs text-[#6b6560]">
          Cada entrada, ajuste y consumo de producción queda en el historial del insumo.
        </p>
      </div>
      {error && <pre className="whitespace-pre-wrap rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-xs text-red-200">{error}</pre>}
      {info && <p className="rounded-lg border border-green-500/40 bg-green-500/10 p-3 text-xs text-green-200">{info}</p>}

      <div className="grid gap-5 xl:grid-cols-2">
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-[#f5f0e8]">Movimiento de stock</h3>
          <select className={field} value={selectedId} onChange={(e) => {
            setSelectedId(e.target.value)
            setMinimo("")
          }}>
            {supplies.map((s) => {
              const stock = linearDisplay(s.metersLeft, 0, s.unit)
              return <option key={s.id} value={s.id}>ID {s.id} · {s.name} · {displayNumber(stock.quantity, stock.unit === "metro" ? 2 : 0)} {stock.unit === "metro" ? "m" : stock.unit}</option>
            })}
          </select>
          {selected && (
            <p className="text-xs text-[#6b6560]">
              Saldo: {displayNumber(linearDisplay(selected.metersLeft, 0, selected.unit).quantity, selected.unit === "cm" || selected.unit === "metro" ? 2 : 0)} {selected.unit === "cm" || selected.unit === "metro" ? "m" : selected.unit}
              {" · "}mínimo: {displayNumber(linearDisplay(selected.stock_minimo, 0, selected.unit).quantity, selected.unit === "cm" || selected.unit === "metro" ? 2 : 0)} {selected.unit === "cm" || selected.unit === "metro" ? "m" : selected.unit}
              {selected.unit === "cm" && " · operaciones y valores ingresados en cm"}
            </p>
          )}
          {canWrite && selected?.perfil_en_receta && (
            <div className="space-y-2">
              <p className="text-xs text-[#6b6560]">Ingresá barras completas de {selected.largo_pieza_cm} cm. Los saldos deben estar conciliados.</p>
              <input className={field} type="number" min="1" step="1" value={cantidadPiezas} placeholder="Cantidad de barras"
                onChange={e => setCantidadPiezas(e.target.value)} />
              <input className={field} value={referencia} placeholder="Referencia de compra" onChange={e => setReferencia(e.target.value)} />
              <button className={button} disabled={busy || !cantidadPiezas} onClick={ingresarPiezas}>INGRESAR PIEZAS</button>
            </div>
          )}
          {canManage && selected?.perfil_en_receta && (
            <ProfileReconciliation key={selected.id} id={selected.id} largo={selected.largo_pieza_cm}
              onChanged={() => { void Promise.all([cargar(), cargarDetalle()]).catch((e) => setError(e instanceof Error ? e.message : "Error al actualizar")); onChanged?.() }} />
          )}
          {canManage && selected && !selected.perfil_en_receta && (
            <StockReconciliation key={selected.id} id={selected.id}
              onChanged={() => { void Promise.all([cargar(), cargarDetalle()]).catch((e) => setError(e instanceof Error ? e.message : "Error al actualizar")); onChanged?.() }} />
          )}
          {canWrite && !selected?.perfil_en_receta && (
            <div className="grid gap-2 sm:grid-cols-2">
              <select className={field} value={tipo} onChange={(e) => setTipo(e.target.value as "entrada" | "ajuste")}>
                <option value="entrada">Entrada (cantidad positiva)</option>
                <option value="ajuste">Ajuste (positivo o negativo)</option>
              </select>
              <input className={field} type="number" step="any" value={cantidad} placeholder="Cantidad"
                onChange={(e) => setCantidad(e.target.value)} />
              <input className={field} value={referencia} placeholder="Referencia: factura / pedido"
                onChange={(e) => setReferencia(e.target.value)} />
              <input className={field} value={notas} placeholder="Notas"
                onChange={(e) => setNotas(e.target.value)} />
              <button className={`${button} sm:col-span-2`} disabled={busy || !selectedId || !cantidad}
                onClick={registrarMovimiento}>REGISTRAR MOVIMIENTO</button>
            </div>
          )}
          {canWrite && selected?.unidad_compra && !selected.perfil_en_receta && (
            <div className="space-y-2 border-t border-[#2a2520] pt-3">
              <p className="text-xs text-[#6b6560]">Compra: 1 {selected.unidad_compra} = {selected.factor_conversion} {selected.unit}</p>
              <input className={field} type="number" min="0" step="any" value={cantidadCompra}
                placeholder={`Cantidad de ${selected.unidad_compra}`} onChange={e => setCantidadCompra(e.target.value)} />
              <button className={outline} disabled={busy || !cantidadCompra} onClick={ingresarCompra}>REGISTRAR COMPRA</button>
            </div>
          )}
          {canManage && selected && (
            <div className="flex flex-wrap gap-2 border-t border-[#2a2520] pt-3">
              <input className={`${field} min-w-40 flex-1`} type="number" min="0" step="any"
                value={minimo !== "" ? minimo : String(selected.stock_minimo)} placeholder="Stock mínimo"
                onChange={(e) => setMinimo(e.target.value)} />
              <button className={outline} disabled={busy || minimo === ""} onClick={guardarMinimo}>
                GUARDAR MÍNIMO
              </button>
            </div>
          )}
          {canManage && selected && selected.unit === "metro" && (
            <div className="space-y-2 border-t border-[#2a2520] pt-3">
              <h4 className="text-xs font-semibold text-[#f5f0e8]">Configurar tela para roller y tradicional</h4>
              <p className="text-xs text-[#6b6560]">El precio y el stock existentes deben estar expresados por metro lineal.</p>
              <input className={field} type="number" min="0" step="any" value={anchoTela} placeholder={`Ancho del rollo (cm; actual ${selected.widthCm})`} onChange={e => setAnchoTela(e.target.value)} />
              <input className={field} type="number" min="0" step="any" value={largoRollo} placeholder="Largo del rollo (cm), opcional" onChange={e => setLargoRollo(e.target.value)} />
              <input className={field} value={unidadCompra} placeholder="Unidad de compra (ej. rollo)" onChange={e => setUnidadCompra(e.target.value)} />
              <input className={field} type="number" min="0" step="any" value={factorCompra} placeholder="Metros lineales por unidad de compra" onChange={e => setFactorCompra(e.target.value)} />
              <button className={outline} disabled={busy || !anchoTela} onClick={configurarTela}>GUARDAR CONFIGURACIÓN DE TELA</button>
            </div>
          )}
        </div>

        <div className="space-y-3">
          <h3 className="text-sm font-bold text-[#f5f0e8]">Alertas de reposición</h3>
          {alerts.length === 0 ? (
            <p className="text-xs text-[#6b6560]">No hay insumos debajo del mínimo configurado.</p>
          ) : (
            <ul className="space-y-2">
              {alerts.map((a) => {
                const actual = linearDisplay(a.stock_actual, 0, a.unidad)
                const minimo = linearDisplay(a.stock_minimo, 0, a.unidad)
                const faltante = linearDisplay(a.faltante, 0, a.unidad)
                const unidad = actual.unit === "metro" ? "m" : actual.unit
                const decimals = actual.unit === "metro" ? 2 : 0
                return (
                <li key={a.id_insumo} className="flex justify-between rounded-lg border border-amber-500/20 bg-amber-500/5 p-2 text-xs">
                  <span className="text-[#f5f0e8]">{a.insumo}</span>
                  <span className="text-amber-300">{displayNumber(actual.quantity, decimals)}/{displayNumber(minimo.quantity, decimals)} {unidad} · faltan {displayNumber(faltante.quantity, decimals)}</span>
                </li>
              )})}
            </ul>
          )}
          {canManage && (
            <div className="space-y-2 border-t border-[#2a2520] pt-3">
              <h4 className="text-xs font-semibold text-[#f5f0e8]">Actualizar precios</h4>
              <PriceSyncStatus canManage={canManage} onSynced={() => { void cargar(); onChanged?.() }} />
              <div className="flex gap-2">
                <input className={field} type="number" step="0.01" value={porcentaje} placeholder="Inflación / ajuste %"
                  onChange={(e) => setPorcentaje(e.target.value)} />
                <button className={outline} disabled={busy || porcentaje === ""}
                  onClick={() => actualizarPrecios("porcentaje")}>APLICAR %</button>
              </div>
              <textarea className={`${field} h-16 font-mono`} value={preciosCsv}
                placeholder={"Lista proveedor: un insumo por línea, id;precio\n12;1540.50"}
                onChange={(e) => setPreciosCsv(e.target.value)} />
              <p className="text-xs text-[#6b6560]">La lista general usa el precio por unidad de registro de cada insumo (por cm si está registrado en cm). Para telas usá el CSV por metro lineal.</p>
              <input className={field} value={motivo} placeholder="Motivo / proveedor"
                onChange={(e) => setMotivo(e.target.value)} />
              <button className={outline} disabled={busy || !preciosCsv.trim()}
                onClick={() => actualizarPrecios("lista")}>APLICAR LISTA DE PRECIOS</button>
              <textarea className={`${field} h-24 font-mono`} value={telasCsv}
                placeholder={"CSV de telas separado por ;\nid_insumo;precio_metro\n12;1500"}
                onChange={(e) => setTelasCsv(e.target.value)} />
              <input className={field} type="file" accept=".csv,text/csv"
                onChange={async (e) => {
                  const archivo = e.target.files?.[0]
                  if (!archivo) return
                  try { setTelasCsv(await archivo.text()) }
                  catch { setError("No se pudo leer el archivo CSV") }
                }} />
              <div className="flex gap-2">
                <button className={outline} disabled={busy || !telasCsv.trim()} onClick={() => importarTelas(false)}>VALIDAR CSV TELAS</button>
                <button className={outline} disabled={busy || !telasCsv.trim()} onClick={() => importarTelas(true)}>APLICAR CSV TELAS</button>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-2">
        <div className="space-y-2">
          <h3 className="text-sm font-bold text-[#f5f0e8]">Movimientos recientes {selected ? `· ${selected.name}` : ""}</h3>
          <div className="max-h-56 overflow-auto rounded-lg border border-[#2a2520]">
            {movements.map((m) => (
              <div key={m.id} className="flex justify-between gap-3 border-b border-[#2a2520] p-2 text-[11px]">
                <span className="text-[#f5f0e8]">{m.tipo} {m.referencia && `· ${m.referencia}`}
                  {m.notas && <span className="block break-all text-[#aaa39a]">{m.notas}</span>}
                  <span className="block text-[#6b6560]">{new Date(`${m.creado_en}Z`).toLocaleString("es-AR")} · {m.usuario || "sistema"}</span>
                </span>
                <span className="whitespace-nowrap text-[#c9a961]">{m.cantidad > 0 ? "+" : ""}{m.cantidad} → {m.stock_resultante} {m.unidad || selected?.unit}</span>
              </div>
            ))}
            {movements.length === 0 && <p className="p-3 text-xs text-[#6b6560]">Sin movimientos.</p>}
          </div>
        </div>
        {canManage && <div className="space-y-2">
          <h3 className="text-sm font-bold text-[#f5f0e8]">Historial de precios {selected ? `· ${selected.name}` : ""}</h3>
          <div className="max-h-56 overflow-auto rounded-lg border border-[#2a2520]">
            {prices.map((p) => (
              <div key={p.id} className="flex justify-between gap-3 border-b border-[#2a2520] p-2 text-[11px]">
                <span className="text-[#f5f0e8]">${p.precio.toLocaleString("es-AR")} / {p.unidad || selected?.unit || "unidad"}
                  {p.precio_m2 != null && ` · $${p.precio_m2.toLocaleString("es-AR")} / m²`} · {p.motivo || "Cambio de precio"}
                  <span className="block text-[#6b6560]">{new Date(`${p.vigente_desde}Z`).toLocaleString("es-AR")} · {p.usuario || "sistema"}</span>
                </span>
              </div>
            ))}
            {prices.length === 0 && <p className="p-3 text-xs text-[#6b6560]">Sin historial.</p>}
          </div>
        </div>}
      </div>

      <div className="space-y-3 border-t border-[#2a2520] pt-4">
        <div>
          <h3 className="text-sm font-bold text-[#f5f0e8]">Retazos de tela</h3>
          <p className="text-xs text-[#6b6560]">Solo se generan al confirmar producción y si ambas dimensiones superan 80 cm.</p>
        </div>
        {canWrite && <input className={`${field} max-w-lg`} value={reservaRef}
          placeholder="Referencia de presupuesto/pedido para reservar"
          onChange={(e) => setReservaRef(e.target.value)} />}
        <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-3">
          {scraps.map((s) => (
            <div key={s.id} className="flex items-center justify-between gap-3 rounded-lg border border-[#2a2520] p-3 text-xs">
              <div>
                <p className="text-[#f5f0e8]">{s.insumo} · {s.ancho_cm} × {s.largo_cm} cm</p>
                <p className="text-[#6b6560]">{s.estado}{s.referencia ? ` · ${s.referencia}` : ""}</p>
              </div>
              {canWrite && (s.estado === "disponible"
                ? <button className={outline} disabled={busy || !reservaRef.trim()} onClick={() => reservar(s.id)}>RESERVAR</button>
                : <button className={outline} disabled={busy} onClick={() => liberar(s.id)}>LIBERAR</button>)}
            </div>
          ))}
          {scraps.length === 0 && <p className="text-xs text-[#6b6560]">No hay retazos disponibles o reservados.</p>}
        </div>
      </div>
    </section>
  )
}
