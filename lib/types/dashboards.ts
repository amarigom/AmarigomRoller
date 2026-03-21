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