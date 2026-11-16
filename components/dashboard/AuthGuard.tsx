"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Loader2 } from "lucide-react"
import { apiFetch, clearSession, getSession, saveSession, type Session } from "@/lib/api"

/** Exige sesión válida: revalida con /api/auth/me para tomar el rol y permisos vigentes. */
export default function AuthGuard({
  children,
  onSession,
}: {
  children: React.ReactNode
  onSession?: (session: Session) => void
}) {
  const router = useRouter()
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const stored = getSession()
    if (!stored) {
      router.replace("/login")
      return
    }
    apiFetch("/api/auth/me")
      .then(async (res) => {
        if (!res.ok) throw new Error("sesión inválida")
        const data = await res.json()
        const session: Session = { token: stored.token, user: data.user, permissions: data.permissions }
        saveSession(session)
        onSession?.(session)
        setReady(true)
      })
      .catch(() => {
        clearSession()
        router.replace("/login")
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router])

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a] text-[#c9a961]">
        <Loader2 className="animate-spin" />
      </div>
    )
  }
  return <>{children}</>
}
