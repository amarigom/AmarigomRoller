"use client"

import { useEffect, useState } from "react"
import { Loader2, Plus, X } from "lucide-react"
import { apiFetch, getSession } from "@/lib/api"

type Rol = "admin" | "ventas" | "taller"

interface Usuario {
  id: number
  email: string
  nombre: string
  rol: Rol
  activo: boolean
  ultimo_login: string | null
}

const ROLES: Rol[] = ["admin", "ventas", "taller"]
const FORM_VACIO = { nombre: "", email: "", password: "", rol: "ventas" as Rol }

const inputClass =
  "w-full rounded-lg border border-[#2a2520] bg-black px-3 py-2 text-[#f5f0e8] outline-none focus:border-[#c9a961]"

export default function UsuariosPage() {
  const miId = getSession()?.user.id
  const [usuarios, setUsuarios] = useState<Usuario[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(FORM_VACIO)
  const [saving, setSaving] = useState(false)

  const mensajeError = async (res: Response) => {
    const data = await res.json().catch(() => ({}))
    const detalle = Array.isArray(data.detalles) && data.detalles.length ? ` (${data.detalles.join("; ")})` : ""
    return (data.message || "No se pudo completar la acción") + detalle
  }

  const cargar = async () => {
    setLoading(true)
    try {
      const res = await apiFetch("/api/users")
      if (!res.ok) throw new Error(await mensajeError(res))
      setUsuarios(await res.json())
      setError("")
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al cargar usuarios")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    cargar()
  }, [])

  const crear = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError("")
    try {
      const res = await apiFetch("/api/users", { method: "POST", body: JSON.stringify(form) })
      if (!res.ok) {
        setError(await mensajeError(res))
        return
      }
      setForm(FORM_VACIO)
      setShowForm(false)
      cargar()
    } finally {
      setSaving(false)
    }
  }

  const actualizar = async (id: number, cambios: Partial<Pick<Usuario, "rol" | "activo">>) => {
    setError("")
    const res = await apiFetch(`/api/users/${id}`, { method: "PATCH", body: JSON.stringify(cambios) })
    if (!res.ok) setError(await mensajeError(res))
    cargar()
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="font-serif text-3xl text-[#f5f0e8]">Usuarios</h1>
          <p className="mt-1 text-sm italic text-[#6b6560]">Accesos y roles del equipo</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center justify-center gap-2 rounded-xl bg-[#c9a961] px-6 py-3 text-sm font-bold text-[#0a0a0a] hover:bg-[#d4b574]"
        >
          {showForm ? <X size={18} /> : <Plus size={18} />}
          {showForm ? "CANCELAR" : "NUEVO USUARIO"}
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-red-500/50 bg-red-500/10 p-3 text-sm text-red-200">{error}</div>
      )}

      {showForm && (
        <form
          onSubmit={crear}
          className="grid grid-cols-1 gap-4 rounded-2xl border border-[#c9a961]/20 bg-[#111111] p-6 md:grid-cols-4"
        >
          <input required placeholder="Nombre" className={inputClass} value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
          <input required type="email" placeholder="Email" className={inputClass} value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input required type="password" minLength={10} autoComplete="new-password"
            placeholder="Contraseña (mín. 10)" className={inputClass} value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <select className={inputClass} value={form.rol}
            onChange={(e) => setForm({ ...form, rol: e.target.value as Rol })}>
            {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
          </select>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center justify-center gap-2 rounded-xl bg-[#c9a961] py-2 text-sm font-bold text-black disabled:opacity-50 md:col-span-4"
          >
            {saving && <Loader2 size={16} className="animate-spin" />} CREAR USUARIO
          </button>
        </form>
      )}

      <div className="overflow-x-auto rounded-2xl border border-[#2a2520] bg-[#111111]">
        <table className="w-full text-left text-sm text-[#f5f0e8]">
          <thead className="text-[10px] uppercase tracking-widest text-[#6b6560]">
            <tr>
              <th className="p-4">Nombre</th>
              <th className="p-4">Email</th>
              <th className="p-4">Rol</th>
              <th className="p-4">Estado</th>
              <th className="p-4">Último acceso</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="p-6 text-center text-[#c9a961]"><Loader2 className="inline animate-spin" /></td></tr>
            ) : (
              usuarios.map((u) => (
                <tr key={u.id} className="border-t border-[#2a2520]">
                  <td className="p-4">{u.nombre}{u.id === miId && <span className="ml-2 text-xs text-[#6b6560]">(vos)</span>}</td>
                  <td className="p-4">{u.email}</td>
                  <td className="p-4">
                    <select
                      value={u.rol}
                      onChange={(e) => actualizar(u.id, { rol: e.target.value as Rol })}
                      className="rounded-lg border border-[#2a2520] bg-black px-2 py-1 text-[#c9a961]"
                    >
                      {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                    </select>
                  </td>
                  <td className="p-4">
                    <button
                      onClick={() => actualizar(u.id, { activo: !u.activo })}
                      className={u.activo ? "text-green-400 hover:underline" : "text-red-400 hover:underline"}
                    >
                      {u.activo ? "Activo" : "Inactivo"}
                    </button>
                  </td>
                  <td className="p-4 text-[#6b6560]">
                    {u.ultimo_login ? new Date(u.ultimo_login + "Z").toLocaleString("es-AR") : "—"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
