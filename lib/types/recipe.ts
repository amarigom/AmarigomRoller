// 1. LA DEFINICIÓN (Lo que traemos de la DB/BOM)
export interface RecipeItem {
  id: number;
  productId: number | null; // id_padre en Python
  supplyId: number | null;  // id_insumo
  supplyName: string;       // nombre del insumo
  productName: string;      // nombre_producto
  
  // Lógica de dimensiones (Deltas)
  deltaWidth: number;       // delta_ancho
  deltaHeight: number;      // delta_alto
  calculationType: string;  // unidad, lineal, m2
  
  // Datos de stock y costos
  stockInfo: {
    unit: string;           // mts, unidades, etc.
    basePrice: number;      // precio_costo_unitario
  };
}

// 2. EL RESULTADO (Lo que genera la calculadora tras poner las medidas)
export interface RecipeComponent {
  componente: string;      // Ej: "Tela Blackout"
  consumo_m_o_m2: number;  // Ej: 2.45
  medida_corte: string;    // Ej: "155 x 210"
  precio_unitario: number;
  costo_parcial: number;
  metodo?: "ROLLO" | "RETAZO"; 
  id_retazo?: number;         
  mensaje?: string;        // Si hay un ahorro detectado
}