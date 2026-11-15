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
export interface MaterialComponent {
  componente: string;      // Ej: "Tela Blackout"
  consumo_m_o_m2: number;  // Ej: 2.45
  unidad?: string;         // Unidad del insumo: metro, m2, unidad
  medida_corte: string;    // Ej: "155 x 210"
  metodo?: "ROLLO" | "RETAZO" | "BARRA" | "PERFIL" | "UNIDAD" | "MANO_OBRA";
  id_retazo?: number;         
  mensaje?: string;        // Si hay un ahorro detectado
  merma_pct?: number;
  minutos?: number;        // Mano de obra del componente
}

export interface RecipeComponent extends MaterialComponent {
  precio_unitario: number;
  costo_parcial: number;
  unidad_costo?: string | null;
  cantidad_costo?: number | null;
  cantidad_reposicion?: number | null;
  costo_reposicion?: number;
}

export interface QuoteTotals {
  precio_producto: {
    precio_venta_final: number;
  };
  servicio_colocacion: {
    km_ida: number;
    km_totales: number;
    total_colocacion: number;
  };
  total_presupuesto: number;
}

export interface ExplosionTotals extends QuoteTotals {
  total_materiales: number;
  total_minutos: number;
  total_mano_obra: number;
  total_desgaste: number;
  total: number;
  precio_producto: {
    markup_pct: number;
    ganancia_markup: number;
    margen_sobre_ventas_pct: number;
    precio_venta_final: number;
  };
  servicio_colocacion: {
    tarifa_base: number;
    km_ida: number;
    km_totales: number;
    costo_traslado: number;
    total_colocacion: number;
  };
  total_presupuesto: number;
}

// 3. EDICIÓN DE RECETAS (versiones publicadas por el admin)
export interface RecipeItemDraft {
  id_insumo: number | null;
  nombre: string;
  tipo_calculo: string;
  descripcion: string | null;
  delta_ancho_cm: number;
  delta_alto_cm: number;
  cantidad_base: number;
  merma_pct: number;
  minutos_mano_obra: number;
  formula_ancho: string | null;
  formula_alto: string | null;
  formula_cantidad: string | null;
  condicion: string | null;
  insumos_alternativos: number[];
}

export interface RecipeProductSummary {
  id: number;
  nombre: string;
  categoria: string | null;
  version_vigente: number | null;
  items: number;
}

export interface RecipeVersionSummary {
  id: number;
  version: number;
  vigente_desde: string;
  vigente_hasta: string | null;
  nota: string | null;
  items: number;
}

export interface ImportSummary {
  aplicado: boolean;
  productos: { producto: string; existe: boolean; items: number; version: number }[];
}
