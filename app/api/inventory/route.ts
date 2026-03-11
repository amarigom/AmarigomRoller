import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

export async function GET() {
  // Buscamos el archivo en la carpeta data que creaste en la raíz
  const filePath = path.join(process.cwd(), "data", "inventory.json");
  console.log("Buscando inventario en:", filePath);
  
  
  try {
    const fileData = await fs.readFile(filePath, "utf-8");
    const inventory = JSON.parse(fileData);
    
    // Enviamos los datos al navegador
    return NextResponse.json(inventory);
  } catch (error) {
    console.error("Error al leer el inventario:", error);
    // Si el archivo no existe o está mal, devolvemos un array vacío para que no explote la web
    return NextResponse.json([]);
  }
}