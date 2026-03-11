"use client"

import { useState, useEffect } from "react"
import CuttingCalculator from "@/components/dashboard/CuttingCalculator"
import type { FabricRoll } from "@/lib/types/dashboards"

export default function CalculadoraPage() {
  const [rolls, setRolls] = useState<FabricRoll[]>([])

  // Cargar los rollos al abrir la página
  useEffect(() => {
    fetch("/api/inventory") // Necesitarías crear un GET simple similar al POST anterior
      .then(res => res.json())
      .then(data => setRolls(data));
  }, []);

  const handleDiscountStock = async (rollId: string, meters: number) => {
    const response = await fetch("/api/inventory/discount", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rollId, meters }),
    });

    if (response.ok) {
      const data = await response.json();
      setRolls(data.inventory); // Actualizamos la pantalla con los datos nuevos
      alert("¡Corte registrado y stock actualizado!");
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <CuttingCalculator rolls={rolls} onDiscountStock={handleDiscountStock} />
    </div>
  )
}