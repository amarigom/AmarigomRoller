"use client"

import { useCallback, useEffect, useState } from "react"
import { Copy, Loader2, Plus, Trash2, Upload } from "lucide-react"
import { apiFetch } from "@/lib/api"
import type {
  ImportSummary, RecipeComponent, RecipeItemDraft, RecipeProductSummary, RecipeVersionSummary,
} from "@/lib/types/recipe"

interface Insumo { id: number; name: string; unit: string | null }
interface TipoCalculo { tipo: string; descripcion: string }
interface Preview {
  explosion: RecipeComponent[]
  total_materiales: number
  total_minutos: number
  total_mano_obra: number
  total: number
}

const inputClass =
  "w-full rounded-lg border border-[#2a2520] bg-black px-2 py-1.5 text-sm text-[#f5f0e8] outline-none focus:border-[#c9a961]"
const btn = "rounded-lg px-4 py-2 text-xs font-bold disabled:opacity-50"
const gold = `${btn} bg-[#c9a961] text-black hover:bg-[#d4b574]`
const ghost = `${btn} border border-[#2a2520] text-[#c9a961] hover:border-[#c9a961]`

const ITEM_VACIO: RecipeItemDraft = {
  id_insumo: null, nombre: "", tipo_calculo: "fijo", descripcion: null, delta_ancho_cm: 0, delta_alto_cm: 0,
  cantidad_base: 1, merma_pct: 0, minutos_mano_obra: 0, formula_ancho: null, formula_alto: null,
  formula_cantidad: null, condicion: null,
}

async function mensaje(res: Response) {
  const data = await res.json().catch(() => ({}))
  const detalles = Array.isArray(data.detalles) && data.detalles.length ? `\n- ${data.detalles.join("\n- ")}` : ""
  return (data.message || "No se pudo completar la acción") + detalles
}

// "sistema=cadena, color=blanco" -> { sistema: "cadena", color: "blanco" }
function parseOpciones(texto: string): Record<string, string> {
  const resultado: Record<string, string> = {}
  for (const par of texto.split(",")) {
    const [k, ...v] = par.split("=")
    if (k?.trim() && v.length) resultado[k.trim()] = v.join("=").trim()
  }
  return resultado
}

export default function RecipeEditor() {
  const [productos, setProductos] = useState<RecipeProductSummary[]>([])
  const [insumos, setInsumos] = useState<Insumo[]>([])
  const [tipos, setTipos] = useState<TipoCalculo[]>([])
  const [productoId, setProductoId] = useState<number | null>(null)
  const [versiones, setVersiones] = useState<RecipeVersionSummary[]>([])
  const [items, setItems] = useState<RecipeItemDraft[]>([])
  const [nota, setNota] = useState("")
  const [medidas, setMedidas] = useState({ w: 150, h: 200, opciones: "" })
  const [preview, setPreview] = useState<Preview | null>(null)
  const [csv, setCsv] = useState("")
  const [resumenCsv, setResumenCsv] = useState<ImportSummary | null>(null)
  const [error, setError] = useState("")
  const [info, setInfo] = useState("")
  const [busy, setBusy] = useState(false)

  const cargarProductos = useCallback(async () => {
    const res = await apiFetch("/api/recipes/products")
    if (res.ok) setProductos(await res.json())
  }, [])

  useEffect(() => {
    cargarProductos()
    apiFetch("/api/inventory").then(async (r) => r.ok && setInsumos(await r.json()))
    apiFetch("/api/recipes/calculation-types").then(async (r) => r.ok && setTipos(await r.json()))
  }, [cargarProductos])

  const abrir = async (id: number, version?: number) => {
    setProductoId(id)
    setPreview(null)
    setError("")
    setInfo("")
    const [det, vers] = await Promise.all([
      apiFetch(`/api/recipes/${id}/detail${version ? `?version=${version}` : ""}`),
      apiFetch(`/api/recipes/${id}/versions`),
    ])
    setItems(det.ok ? await det.json() : [])
    setVersiones(vers.ok ? await vers.json() : [])
  }

  // Ejecuta una acción de la API mostrando el error o el mensaje de éxito
  const ejecutar = async (accion: () => Promise<string | void>) => {
    setBusy(true)
    setError("")
    setInfo("")
    try {
      const ok = await accion()
      if (ok) setInfo(ok)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error inesperado")
    } finally {
      setBusy(false)
    }
  }

  const cambiar = <K extends keyof RecipeItemDraft>(n: number, campo: K, valor: RecipeItemDraft[K]) =>
    setItems(items.map((it, i) => (i === n ? { ...it, [campo]: valor } : it)))

  const texto = (n: number, campo: "formula_ancho" | "formula_alto" | "formula_cantidad" | "condicion", v: string) =>
    cambiar(n, campo, v === "" ? null : v)

  const numero = (v: string) => (v === "" ? 0 : Number(v))

  const nuevoProducto = () => {
    const nombre = window.prompt("Nombre del producto nuevo")
    if (!nombre) return
    ejecutar(async () => {
      const res = await apiFetch("/api/recipes/products", { method: "POST", body: JSON.stringify({ nombre }) })
      if (!res.ok) throw new Error(await mensaje(res))
      const creado: RecipeProductSummary = await res.json()
      await cargarProductos()
      await abrir(creado.id)
      return "Producto creado. Cargá los componentes y publicá la receta."
    })
  }

  const duplicar = () => {
    const origen = productos.find((p) => p.id === productoId)
    const nombre = window.prompt("Nombre del producto copia", origen ? `${origen.nombre} (copia)` : "")
    if (!nombre || productoId === null) return
    ejecutar(async () => {
      const res = await apiFetch(`/api/recipes/${productoId}/duplicate`, { method: "POST", body: JSON.stringify({ nombre }) })
      if (!res.ok) throw new Error(await mensaje(res))
      const data = await res.json()
      await cargarProductos()
      await abrir(data.producto.id)
      return `Receta duplicada en "${data.producto.nombre}".`
    })
  }

  const calcular = () =>
    ejecutar(async () => {
      const res = await apiFetch("/api/recipes/preview", {
        method: "POST",
        body: JSON.stringify({ items, w: medidas.w, h: medidas.h, opciones: parseOpciones(medidas.opciones) }),
      })
      if (!res.ok) throw new Error(await mensaje(res))
      setPreview(await res.json())
    })

  const publicar = () => {
    if (productoId === null) return
    ejecutar(async () => {
      const res = await apiFetch(`/api/recipes/${productoId}/versions`, {
        method: "POST", body: JSON.stringify({ items, nota: nota || null }),
      })
      if (!res.ok) throw new Error(await mensaje(res))
      const v: RecipeVersionSummary = await res.json()
      setNota("")
      await Promise.all([abrir(productoId), cargarProductos()])
      return `Versión ${v.version} publicada. Los presupuestos anteriores siguen usando su versión.`
    })
  }

  const importar = (aplicar: boolean) =>
    ejecutar(async () => {
      const res = await apiFetch("/api/recipes/import", { method: "POST", body: JSON.stringify({ csv, aplicar }) })
      if (!res.ok) throw new Error(await mensaje(res))
      const data: ImportSummary = await res.json()
      setResumenCsv(data)
      if (aplicar) {
        await cargarProductos()
        setCsv("")
        return "Importación aplicada."
      }
      return "El archivo es válido. Revisá el resumen y aplicá la importación."
    })

  const leerArchivo = async (file: File | undefined) => {
    if (!file) return
    setCsv(await file.text())
    setResumenCsv(null)
  }

  const descargarPlantilla = async () => {
    const res = await apiFetch("/api/recipes/import/template")
    if (res.ok) setCsv((await res.json()).csv)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-serif text-3xl text-[#f5f0e8]">Recetas</h1>
        <p className="mt-1 text-sm italic text-[#6b6560]">
          Cada cambio se publica como una versión nueva: los presupuestos anteriores no se modifican
        </p>
      </div>

      {error && (
        <pre className="whitespace-pre-wrap rounded-lg border border-red-500/50 bg-red-500/10 p-3 text-sm text-red-200">{error}</pre>
      )}
      {info && <div className="rounded-lg border border-green-500/40 bg-green-500/10 p-3 text-sm text-green-200">{info}</div>}

      <div className="grid gap-6 lg:grid-cols-[260px_1fr]">
        <aside className="space-y-3">
          <button onClick={nuevoProducto} disabled={busy} className={`${gold} flex w-full items-center justify-center gap-2`}>
            <Plus size={14} /> NUEVO PRODUCTO
          </button>
          <ul className="space-y-1 rounded-2xl border border-[#2a2520] bg-[#111111] p-2">
            {productos.map((p) => (
              <li key={p.id}>
                <button
                  onClick={() => abrir(p.id)}
                  className={`w-full rounded-lg px-3 py-2 text-left text-sm ${
                    p.id === productoId ? "bg-[#c9a961]/15 text-[#c9a961]" : "text-[#f5f0e8] hover:bg-[#1a1a1a]"
                  }`}
                >
                  {p.nombre}
                  <span className="block text-[10px] text-[#6b6560]">
                    {p.version_vigente ? `v${p.version_vigente} · ${p.items} componentes` : "sin receta"}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </aside>

        <section className="space-y-6">
          {productoId === null ? (
            <p className="rounded-2xl border border-[#2a2520] bg-[#111111] p-6 text-sm text-[#6b6560]">
              Elegí un producto para ver o editar su receta.
            </p>
          ) : (
            <>
              <div className="flex flex-wrap items-center gap-3">
                <select
                  className={`${inputClass} !w-auto`}
                  value=""
                  onChange={(e) => e.target.value && abrir(productoId, Number(e.target.value))}
                >
                  <option value="">Cargar una versión anterior…</option>
                  {versiones.map((v) => (
                    <option key={v.id} value={v.version}>
                      v{v.version} · {new Date(v.vigente_desde + "Z").toLocaleDateString("es-AR")}
                      {v.vigente_hasta ? "" : " (vigente)"}{v.nota ? ` · ${v.nota}` : ""}
                    </option>
                  ))}
                </select>
                <button onClick={duplicar} disabled={busy} className={`${ghost} flex items-center gap-2`}>
                  <Copy size={14} /> DUPLICAR COMO PRODUCTO NUEVO
                </button>
              </div>

              <div className="space-y-3">
                {items.map((it, n) => (
                  <div key={n} className="grid grid-cols-2 gap-2 rounded-2xl border border-[#2a2520] bg-[#111111] p-4 md:grid-cols-6">
                    <input className={`${inputClass} md:col-span-2`} placeholder="Nombre del componente" value={it.nombre}
                      onChange={(e) => cambiar(n, "nombre", e.target.value)} />
                    <select className={`${inputClass} md:col-span-2`} value={it.id_insumo ?? ""}
                      onChange={(e) => cambiar(n, "id_insumo", e.target.value ? Number(e.target.value) : null)}>
                      <option value="">{it.tipo_calculo === "mano_obra" ? "(sin insumo)" : "Insumo…"}</option>
                      {insumos.map((s) => <option key={s.id} value={s.id}>{s.name} ({s.unit})</option>)}
                    </select>
                    <select className={`${inputClass} md:col-span-2`} value={it.tipo_calculo}
                      onChange={(e) => cambiar(n, "tipo_calculo", e.target.value)}
                      title={tipos.find((t) => t.tipo === it.tipo_calculo)?.descripcion}>
                      {tipos.map((t) => <option key={t.tipo} value={t.tipo}>{t.tipo}</option>)}
                    </select>
                    {([
                      ["delta_ancho_cm", "Δ ancho (cm)"], ["delta_alto_cm", "Δ alto (cm)"], ["cantidad_base", "Cantidad"],
                      ["merma_pct", "Merma %"], ["minutos_mano_obra", "Minutos"],
                    ] as const).map(([campo, etiqueta]) => (
                      <label key={campo} className="text-[10px] uppercase tracking-wider text-[#6b6560]">
                        {etiqueta}
                        <input type="number" step="any" className={inputClass} value={it[campo]}
                          onChange={(e) => cambiar(n, campo, numero(e.target.value))} />
                      </label>
                    ))}
                    <button onClick={() => setItems(items.filter((_, i) => i !== n))}
                      className="flex items-center justify-center text-red-400 hover:text-red-300" title="Quitar componente">
                      <Trash2 size={16} />
                    </button>
                    {([
                      ["formula_ancho", "Fórmula ancho (ej: ancho - 3)"], ["formula_alto", "Fórmula alto"],
                      ["formula_cantidad", "Fórmula cantidad (ej: ceil(ancho/100))"], ["condicion", "Condición (ej: ancho > 200)"],
                    ] as const).map(([campo, etiqueta]) => (
                      <input key={campo} className={`${inputClass} md:col-span-3`} placeholder={etiqueta}
                        value={it[campo] ?? ""} onChange={(e) => texto(n, campo, e.target.value)} />
                    ))}
                  </div>
                ))}
                <button onClick={() => setItems([...items, { ...ITEM_VACIO }])} className={`${ghost} flex items-center gap-2`}>
                  <Plus size={14} /> AGREGAR COMPONENTE
                </button>
              </div>

              <div className="space-y-3 rounded-2xl border border-[#c9a961]/20 bg-[#111111] p-4">
                <h2 className="font-serif text-lg text-[#c9a961]">Vista previa</h2>
                <div className="grid gap-2 md:grid-cols-4">
                  <input type="number" className={inputClass} value={medidas.w} placeholder="Ancho (cm)"
                    onChange={(e) => setMedidas({ ...medidas, w: numero(e.target.value) })} />
                  <input type="number" className={inputClass} value={medidas.h} placeholder="Alto (cm)"
                    onChange={(e) => setMedidas({ ...medidas, h: numero(e.target.value) })} />
                  <input className={`${inputClass} md:col-span-2`} placeholder="Opciones: sistema=cadena, color=blanco"
                    value={medidas.opciones} onChange={(e) => setMedidas({ ...medidas, opciones: e.target.value })} />
                </div>
                <button onClick={calcular} disabled={busy || items.length === 0} className={ghost}>CALCULAR (sin guardar)</button>
                {preview && (
                  <table className="w-full text-left text-sm text-[#f5f0e8]">
                    <tbody>
                      {preview.explosion.map((e, i) => (
                        <tr key={i} className="border-t border-[#2a2520]">
                          <td className="py-1.5">{e.componente}<span className="block text-[10px] text-[#6b6560]">{e.mensaje}</span></td>
                          <td className="py-1.5 text-[#6b6560]">{e.medida_corte}</td>
                          <td className="py-1.5 text-right">${e.costo_parcial.toLocaleString("es-AR")}</td>
                        </tr>
                      ))}
                      <tr className="border-t border-[#c9a961]/40 font-bold text-[#c9a961]">
                        <td className="py-2" colSpan={2}>Total ({preview.total_minutos} min de mano de obra)</td>
                        <td className="py-2 text-right">${preview.total.toLocaleString("es-AR")}</td>
                      </tr>
                    </tbody>
                  </table>
                )}
              </div>

              <div className="flex flex-wrap gap-3">
                <input className={`${inputClass} !w-auto flex-1`} placeholder="Nota de la versión (qué cambió)" value={nota}
                  onChange={(e) => setNota(e.target.value)} />
                <button onClick={publicar} disabled={busy || items.length === 0} className={`${gold} flex items-center gap-2`}>
                  {busy && <Loader2 size={14} className="animate-spin" />} PUBLICAR NUEVA VERSIÓN
                </button>
              </div>
            </>
          )}

          <div className="space-y-3 rounded-2xl border border-[#2a2520] bg-[#111111] p-4">
            <h2 className="flex items-center gap-2 font-serif text-lg text-[#c9a961]"><Upload size={16} /> Importar recetas desde CSV</h2>
            <p className="text-xs text-[#6b6560]">
              Una fila por componente, agrupadas por la columna <code>producto</code>. Guardá la planilla de Excel como CSV.
            </p>
            <div className="flex flex-wrap gap-3">
              <input type="file" accept=".csv,text/csv" onChange={(e) => leerArchivo(e.target.files?.[0])} className="text-xs text-[#f5f0e8]" />
              <button onClick={descargarPlantilla} className={ghost}>VER ENCABEZADOS</button>
            </div>
            <textarea className={`${inputClass} h-32 font-mono`} value={csv} onChange={(e) => { setCsv(e.target.value); setResumenCsv(null) }} />
            <div className="flex gap-3">
              <button onClick={() => importar(false)} disabled={busy || !csv} className={ghost}>VALIDAR</button>
              <button onClick={() => importar(true)} disabled={busy || !csv || !resumenCsv || resumenCsv.aplicado} className={gold}>
                APLICAR IMPORTACIÓN
              </button>
            </div>
            {resumenCsv && (
              <ul className="text-sm text-[#f5f0e8]">
                {resumenCsv.productos.map((p) => (
                  <li key={p.producto}>
                    {p.producto}: {p.items} componentes → {resumenCsv.aplicado ? "versión" : "será la versión"} {p.version}
                    {p.existe ? "" : " (producto nuevo)"}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      </div>
    </div>
  )
}
