// types/client.ts
export interface Cliente {
  id: number;
  nombre: string;
  telefono: string;
  direccion?: string;
  email?: string;
  // Podés agregar otros campos que ya tengas en tu tabla de Neon
}