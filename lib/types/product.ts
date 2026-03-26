// src/types/product.ts



export interface Product {
  id: number;
  name_es: string; // Coincide con el to_dict de product.py
  description?: string;
  active?: boolean;
}