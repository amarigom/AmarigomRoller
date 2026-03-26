// src/lib/mappers.ts
import { RecipeItem } from "./types/recipe"; 

export const mapBackendToRecipe = (item: any): RecipeItem => {
  return {
    id: item.id,
    productId: item.id_padre, // Coincide con self.id_padre en Python
    supplyId: item.id_insumo,  // Coincide con self.id_insumo en Python
    
    // Si en Flask pusiste "nombre", aquí usamos item.nombre
    productName: item.nombre || "Producto sin nombre",
    
    // Agregamos el nombre del insumo que Flask debería mandar
    supplyName: item.insumo_nombre || "Insumo genérico",
    
    // Los Deltas (Fíjate si en Flask los llamaste delta_ancho o delta_ancho_cm)
    deltaWidth: Number(item.delta_ancho || 0),
    deltaHeight: Number(item.delta_alto || 0),
    
    calculationType: item.tipo_calculo || "unidad",
    
    stockInfo: {
      // Accedemos al objeto anidado que armamos en el to_dict de Python
      unit: item.stock_info?.medida || "un",
      basePrice: Number(item.stock_info?.precio_base || 0)
    }
  };
};