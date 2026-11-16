"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Loader2 } from "lucide-react"
import { login } from "@/lib/api"

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)
    try {
      await login(email, password)
      router.replace("/gestion")
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo iniciar sesión")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a] p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm space-y-5 rounded-2xl border border-[#c9a961]/20 bg-[#111111] p-8 shadow-2xl"
      >
        <div className="text-center">
          <h1 className="font-serif text-2xl uppercase tracking-wider text-[#c9a961]">AMARIGOM</h1>
          <p className="mt-1 text-[10px] uppercase tracking-[0.2em] text-[#6b6560]">Gestión Interna</p>
        </div>

        <label className="block text-sm text-[#a0998c]">
          Email
          <input
            type="email"
            required
            autoComplete="username"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded-lg border border-[#2a2520] bg-[#0a0a0a] px-3 py-2 text-[#f5f0e8] outline-none focus:border-[#c9a961]"
          />
        </label>

        <label className="block text-sm text-[#a0998c]">
          Contraseña
          <input
            type="password"
            required
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-lg border border-[#2a2520] bg-[#0a0a0a] px-3 py-2 text-[#f5f0e8] outline-none focus:border-[#c9a961]"
          />
        </label>

        {error && <p className="text-sm text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#c9a961] py-3 text-sm font-bold text-[#0a0a0a] hover:bg-[#d4b574] disabled:opacity-60"
        >
          {loading && <Loader2 size={16} className="animate-spin" />}
          INGRESAR
        </button>
      </form>
    </div>
  )
}
