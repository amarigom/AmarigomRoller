import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

const filePath = path.join(process.cwd(), "data", "inventory.json");

// GET: Leer todo el inventario
export async function GET() {
  try {
    const fileData = await fs.readFile(filePath, "utf-8");
    return NextResponse.json(JSON.parse(fileData));
  } catch (error) {
    console.error("Error al leer:", error);
    return NextResponse.json([]);
  }
}

// POST: Crear un rollo nuevo
export async function POST(request: Request) {
  try {
    const newRoll = await request.json();
    const fileData = await fs.readFile(filePath, "utf-8");
    const inventory = JSON.parse(fileData);

    const rollToAdd = {
      ...newRoll,
      id: crypto.randomUUID(), // Genera ID único
    };

    inventory.push(rollToAdd);
    await fs.writeFile(filePath, JSON.stringify(inventory, null, 2), "utf-8");

    return NextResponse.json(inventory);
  } catch (error) {
    return NextResponse.json({ error: "Error al guardar" }, { status: 500 });
  }
}

// PATCH: Descontar stock tras un corte
export async function PATCH(request: Request) {
  try {
    const { id, usedMeters } = await request.json();
    const fileData = await fs.readFile(filePath, "utf-8");
    let inventory = JSON.parse(fileData);

    // Buscamos el rollo por ID y restamos los metros
    inventory = inventory.map((roll: any) => {
      if (roll.id === id) {
        const currentMeters = Number(roll.metersLeft);
        const discount = Number(usedMeters);
        return { 
          ...roll, 
          metersLeft: Math.max(0, currentMeters - discount).toFixed(2) 
        };
      }
      return roll;
    });

    await fs.writeFile(filePath, JSON.stringify(inventory, null, 2), "utf-8");
    return NextResponse.json(inventory);
  } catch (error) {
    return NextResponse.json({ error: "Error al actualizar stock" }, { status: 500 });
  }
}