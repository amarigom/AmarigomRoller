// types/client.ts
export interface Cliente {
   id: number;
  nombre: string;
  apellido: string; // <--- AGREGÁ ESTA LÍNEA SI NO ESTÁ
  email: string;
  telefono?: string;
  direccion?: string;
  notas?: string;
  fecha_registro?: string;
  
}
