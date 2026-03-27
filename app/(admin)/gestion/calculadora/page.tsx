"use client"

import { useState, useEffect } from "react"
import CuttingCalculator from "@/components/dashboard/CuttingCalculator"
import type { Supply } from "@/lib/types/dashboards"
import type { RecipeItem } from "@/lib/types/recipe"
import type { Product } from "@/lib/types/product"
// IMPORTANTE: Traemos el mapeador que creamos
import { mapBackendToRecipe } from "@/lib/mappers" 

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function CalculadoraPage() {
  const [rolls, setRolls] = useState<Supply[]>([])
  const [productList, setProductList] = useState<Product[]>([]) // La variable que faltaba
  const [recipe, setRecipe] = useState<RecipeItem[]>([]);
  const [loading, setLoading] = useState(true);

  // 2. Cargar Productos e Inventario al iniciar
  const loadInitialData = async () => {
    setLoading(true);
    try {
      // Traemos productos e inventario en paralelo para ganar velocidad
      const [resProducts, resInventory] = await Promise.all([
        fetch(`${API_BASE_URL}/api/products`),
        fetch(`${API_BASE_URL}/api/inventory`)
      ]);
      // BLINDAJE: Si no es OK, no intentamos procesar el JSON
      if (!resProducts.ok || !resInventory.ok) {
      throw new Error(`Error en servidor: P:${resProducts.status} I:${resInventory.status}`);
    }
      const productsData = await resProducts.json();
      const inventoryData = await resInventory.json();

      setProductList(productsData);
      setRolls(inventoryData);
    } catch (error) {
      console.error("Error cargando datos de productos e inventario:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // 3. Manejador de selección de producto (USA EL MAPEADOR)
  const handleProductSelect = async (id: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/recipes/${id}`);
      const data = await res.json();
      
      // Aquí usamos el "blindaje" de TypeScript:
      const cleanRecipe = data.map(mapBackendToRecipe);
      setRecipe(cleanRecipe);
    } catch (error) {
      console.error("Error al obtener la receta:", error);
    }
  };

  // 4. Función que se dispara al "Confirmar y Cortar"
  const handleDiscountStock = async (explosion: any) => {
    // Aquí podrías refrescar el inventario después de que el backend 
    // de Neon confirme el descuento de stock
    console.log("Descontando stock en Neon para:", explosion);
    await loadInitialData(); // Refrescamos los números de los rollos
  };

  if (loading) return <div className="p-10 text-[#c9a961]">Cargando taller...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="font-serif text-3xl text-[#f5f0e8]">Calculadora de Cortes</h1>
        <p className="text-[#6b6560]">Gestión de producción integrada con Neon</p>
      </div>

      <CuttingCalculator 
        products={productList}
        onDiscountStock={handleDiscountStock}
      />
      
      {/* Opcional: Podrías pasarle los 'rolls' si la calculadora 
          necesita mostrar el stock actual de las telas */}
    </div>
  )
}