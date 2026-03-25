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

export interface RecipeItem {
  id: number;
  component_name: string;
  width_delta: number;
  height_delta: number;
  base_quantity: number;
  calculation_type: 'lineal_ancho' | 'lineal_alto' | 'fijo' | 'superficie';
  description?: string;
  sku?: string;
  // Estos campos los calculamos en el useMemo, no vienen del API:
  finalW_cm?: number;
  finalH_cm?: number;
  consumption?: number;
}

export type FabricType = "blackout" | "sunscreen" | "voile"
export type StockStatus = "in-stock" | "low-stock" | "critical"

// En el Frontend (TypeScript)
export interface Supply {
  id: number;
  code: string;
  name: string;
  category: string;// mapea con Fabric typ
  metersLeft: number;  // Este mapea con 'stock_actual'
  widthCm: number;    // Este mapea con 'ancho_cm'
  unit: string;
  price: number;
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