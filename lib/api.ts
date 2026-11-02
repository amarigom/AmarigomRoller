export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000"

const STORAGE_KEY = "amarigom_session"

export interface SessionUser {
  id: number
  email: string
  nombre: string
  rol: "admin" | "ventas" | "taller"
}

export interface Session {
  token: string
  user: SessionUser
  permissions: string[]
}

export function getSession(): Session | null {
  if (typeof window === "undefined") return null
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Session) : null
  } catch {
    return null
  }
}

export function saveSession(session: Session) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
}

export function clearSession() {
  window.localStorage.removeItem(STORAGE_KEY)
}

export function hasPermission(session: Session | null, permission: string) {
  return !!session && session.permissions.includes(permission)
}

/** fetch contra la API con el token de la sesión; ante un 401 limpia la sesión y vuelve al login. */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const session = getSession()
  const headers = new Headers(init.headers)
  if (session) headers.set("Authorization", `Bearer ${session.token}`)
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json")

  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers })

  if (response.status === 401 && session && typeof window !== "undefined") {
    clearSession()
    window.location.href = "/login"
  }
  return response
}

export async function login(email: string, password: string): Promise<Session> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.message || "No se pudo iniciar sesión")
  }
  const session: Session = { token: data.token, user: data.user, permissions: data.permissions }
  saveSession(session)
  return session
}

export function logout() {
  clearSession()
  window.location.href = "/login"
}
