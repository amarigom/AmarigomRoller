"use client"

import { useState, useEffect } from "react"
import CuttingCalculator from "@/components/dashboard/CuttingCalculator"
import type { Product } from "@/lib/types/product"
import type { RecipeItem } from "@/lib/types/recipe"
import { mapBackendToRecipe } from "@/lib/mappers" 

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function CalculadoraPage() {
  const [productList, setProductList] = useState<Product[]>([])
  const [recipe, setRecipe] = useState<RecipeItem[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [recipeError, setRecipeError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  // Carga inicial de productos
  useEffect(() => {
    const loadProducts = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/products`);
        if (!res.ok) throw new Error("Error al cargar productos");
        const data = await res.json();
        setProductList(data);
      } catch (error) {
        console.error("Error inicial:", error);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  // Único punto de entrada para pedir la receta (Acción del usuario)
  const handleProductChange = async (id: number) => {
    setSelectedId(id);
    setRecipeError(null);
    setRecipe([]);

    if (!id) return;

    try {
      const res = await fetch(`${API_BASE_URL}/api/recipes/${id}`);
      const data = await res.json();

      if (!res.ok) {
        // Frenamos el flujo si Flask devuelve error (ej. 404 o 500)
        setRecipeError(data.message || "Este modelo no tiene receta configurada.");
        return;
      }
    
      // Solo mapeamos si la respuesta fue exitosa (Array)
      const cleanRecipe = data.map(mapBackendToRecipe);
      setRecipe(cleanRecipe);
    } catch (error) {
      setRecipeError("Hubo un problema de conexión con el servidor.");
    }
  };

  if (loading) return <div className="p-10 text-[#c9a961] font-serif">Cargando taller...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="mb-8">
        <h1 className="font-serif text-3xl text-[#f5f0e8]">Calculadora de Cortes</h1>
        <p className="text-[#6b6560]">Gestión de producción AMARIGOM DECO</p>
      </header>

      {/* SELECTOR: Fuera del componente para evitar renders circulares */}
      <div className="bg-[#111111] border border-[#2a2520] rounded-xl p-5 mb-6">
        <label className="text-[10px] text-[#6b6560] uppercase font-bold tracking-widest ml-1">
          Modelo de Cortina / Receta
        </label>
        <select
          onChange={(e) => handleProductChange(Number(e.target.value))}
          className="w-full mt-2 bg-black border border-[#2a2520] p-3 rounded-xl text-[#c9a961] outline-none focus:border-[#c9a961] transition-all cursor-pointer"
        >
          <option value="">Seleccioná un modelo para comenzar...</option>
          {productList.map((p) => (
            <option key={p.id} value={p.id}>{p.name_es || p.name}</option>
          ))}
        </select>
      </div>

      {/* BANNER DE ERROR */}
      {recipeError && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded-lg mb-6 flex items-center gap-2 animate-in fade-in slide-in-from-top-1">
          <span className="text-lg"> </span>
          <p className="text-sm font-medium">{recipeError}</p>
        </div>
      )}

      {/* EL COMPONENTE (Puro y Mudo) */}
      <CuttingCalculator 
        selectedProductId={selectedId}
        recipe={recipe} 
        onRefreshInventory={() => { /* Lógica para refrescar stock si es necesario */ }}
      />
    </div>
  )
}