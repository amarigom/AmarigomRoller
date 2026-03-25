"use client"

import { useState, useEffect } from "react"
import CuttingCalculator from "@/components/dashboard/CuttingCalculator"
//import type { FabricRoll } from "@/lib/types/dashboards"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function CalculadoraPage() {
  const [rolls, setRolls] = useState<FabricRoll[]>([])

  // 1. DEFINIR LA VARIABLE QUE FALTA
  const [productList, setProductList] = useState([]);
  useEffect(() => {
    const productosPrueba = [
      { id: 1, name_es: 'Cortina Roller Sunscreen' },
      { id: 5, name_es: 'Cortina Roller Blackout estandar' },
      { id: 3, name_es: 'Cortinas Tradicionales' }
    ];
    setProductList(productosPrueba);
    
    // Si después querés traerlos de la API, usás:
    // fetch('/api/products').then(res => res.json()).then(data => setProductList(data));
  }, []);

  // Función para cargar o refrescar los rollos
  const loadInventory = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/inventory`);
      const data = await res.json();
      setRolls(data);
    } catch (error) {
      console.error("Error cargando inventario:", error);
    }
  };

  useEffect(() => {
    loadInventory();
  }, []);

  // Esta es la función que llama el componente cuando confirmás un corte
  const handleDiscountStock = async (rollId: string, meters: number) => {
    try {
      const response = await fetch("/api/inventory", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          id: rollId, 
          usedMeters: meters 
        }),
      });

      if (response.ok) {
        const updatedInventory = await response.json();
        setRolls(updatedInventory); // Actualiza la lista localmente
        alert("¡Corte registrado! El stock de AMARIGOM DECO ha sido actualizado.");
      } else {
        alert("No se pudo actualizar el stock. Verificá la conexión.");
      }
    } catch (error) {
      console.error("Error en la operación:", error);
      alert("Error crítico al procesar el descuento.");
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="font-serif text-3xl text-[#f5f0e8]">Calculadora de Cortes</h1>
        <p className="text-[#6b6560]">Calculá medidas y descontá stock automáticamente</p>
      </div>

      <CuttingCalculator 
        products={productList }
        onDiscountStock={(items) => console.log("Confirmado:", items)}
      />
    </div>
  )
}