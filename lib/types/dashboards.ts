// lib/types/dashboards.ts

export interface InventoryItem {
  id: number;
  code: string;
  name: string;
  category: string;
  metersLeft: number;
  widthCm: number;
  unit: string;
  price: number;
  lastUpdate: string;
}


export type FabricType = "blackout" | "sunscreen" | "voile"
export type StockStatus = "in-stock" | "low-stock" | "critical"

// En el Frontend (TypeScript)
// Lo que ve todo el mundo en AMARIGOM DECO
export interface Supply {
  id: number;
  code: string;
  name: string;
  category: string;
  metersLeft: number;
  totalCMeters: number;
  widthCm: number;
  unit: string;
  status: StockStatus;
  pricePerCMeter: number;
}

// Lo que ves vos como Dueño (Extensión)
export interface AdminSupply extends Supply {
  costPrice?: number;        // Opcional, por si el JSON no lo trae
  lastRestockDate?: string;
  supplierName?: string;
}

// ─── Clientes ───────────────────────────────────────────────────
export type ClientStatus = "quoted" | "in-production" | "installed"

export interface Client {
  id: string
  name: string
  email: string
  phone: string
  address: string
  status: ClientStatus
  totalOrders: number
  lastOrderDate: string
  createdAt: string
}

// ─── Ordenes ────────────────────────────────────────────────────
export type OrderStatus = "pending" | "cutting" | "production" | "ready" | "delivered"

export interface OrderItem {
  fabricRollId: string
  fabricName: string
  widthCm: number
  heightCm: number
  linearMeters: number
}

export interface Order {
  id: string
  clientId: string
  clientName: string
  items: OrderItem[]
  status: OrderStatus
  totalPrice: number
  notes: string
  createdAt: string
  estimatedDelivery: string
}

// ─── Calculadora de Corte ───────────────────────────────────────
export interface CuttingCalculation {
  windowWidthCm: number
  windowHeightCm: number
  adjustedWidthCm: number  // +5cm cada lado
  adjustedHeightCm: number // +30cm tubo enrollado
  linearMeters: number     // metros lineales a cortar
  selectedRollId: string | null
}

// ─── Navegacion del Dashboard ───────────────────────────────────
export type DashboardView = "inventory" | "clients" | "calculator" | "orders"