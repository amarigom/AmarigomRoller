// src/types/product.ts

// BUSCÁ ESTO Y DEJA LO ASÍ:
export interface Product {
  id: number;
  name: string;      // Vercel lo pide así
  name_es?: string;  // Opcional, por si tu Python manda este
  category: string;  // ESTO ES LO QUE FALTA y por eso da error
  description?: string;
  activo?: boolean;
}

