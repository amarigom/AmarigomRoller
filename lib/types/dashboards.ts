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