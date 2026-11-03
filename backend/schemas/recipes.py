from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

MAX_MEDIDA_CM = 1000


class MedidasIn(BaseModel):
    w: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)
    h: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)
    # Para recalcular con la receta que estaba vigente (un presupuesto viejo no cambia)
    fecha: Optional[date] = None
    version: Optional[int] = Field(None, gt=0)


class RecipeItemIn(BaseModel):
    id_insumo: Optional[int] = Field(None, gt=0)
    nombre: str = Field(..., min_length=1, max_length=100)
    tipo_calculo: str = Field(..., min_length=1, max_length=30)
    descripcion: Optional[str] = None
    delta_ancho_cm: float = Field(0, ge=-MAX_MEDIDA_CM, le=MAX_MEDIDA_CM)
    delta_alto_cm: float = Field(0, ge=-MAX_MEDIDA_CM, le=MAX_MEDIDA_CM)
    cantidad_base: float = Field(1, ge=0)
    merma_pct: float = Field(0, ge=0, le=100)
    minutos_mano_obra: float = Field(0, ge=0)
    formula_ancho: Optional[str] = Field(None, max_length=200)
    formula_alto: Optional[str] = Field(None, max_length=200)
    formula_cantidad: Optional[str] = Field(None, max_length=200)
    condicion: Optional[str] = Field(None, max_length=200)


class RecipeVersionIn(BaseModel):
    items: list[RecipeItemIn] = Field(..., min_length=1, max_length=100)
    nota: Optional[str] = Field(None, max_length=255)


class PreviewIn(BaseModel):
    """Receta sin guardar + medidas de prueba, para ver el cálculo antes de publicar."""
    items: list[RecipeItemIn] = Field(..., min_length=1, max_length=100)
    w: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)
    h: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)
    opciones: dict = {}


class ProductIn(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    categoria: Optional[str] = Field(None, max_length=100)


class DuplicateIn(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    version: Optional[int] = Field(None, gt=0)


class ImportIn(BaseModel):
    csv: str = Field(..., min_length=1, max_length=500_000)
    # False = solo valida y muestra qué se crearía
    aplicar: bool = False
    nota: Optional[str] = Field(None, max_length=255)


class RecipeItemFullOut(RecipeItemIn):
    id: int
    insumo: Optional[str] = None

    @classmethod
    def from_model(cls, i):
        campos = {k: getattr(i, k) for k in RecipeItemIn.model_fields}
        for k in ('delta_ancho_cm', 'delta_alto_cm', 'cantidad_base', 'merma_pct', 'minutos_mano_obra'):
            campos[k] = float(campos[k] or 0)
        return cls(id=i.id, insumo=i.insumo.name if i.insumo else None, **campos)


class ProductRecipeOut(BaseModel):
    id: int
    nombre: str
    categoria: Optional[str]
    version_vigente: Optional[int]
    items: int


class RecipeVersionOut(BaseModel):
    id: int
    version: int
    vigente_desde: datetime
    vigente_hasta: Optional[datetime]
    nota: Optional[str]
    items: int

    @classmethod
    def from_model(cls, r):
        return cls(id=r.id, version=r.version, vigente_desde=r.vigente_desde,
                   vigente_hasta=r.vigente_hasta, nota=r.nota, items=len(r.items))


class ExplosionItemOut(BaseModel):
    componente: str
    consumo_m_o_m2: float
    unidad: str
    consumo_cm: float
    medida_corte: str
    precio_unitario: float
    costo_parcial: float
    metodo: str
    id_retazo: Optional[int]
    mensaje: str
    merma_pct: float = 0
    minutos: float = 0
    cortes: list[dict] = []


class ExplosionOut(BaseModel):
    status: str = "success"
    version: Optional[int] = None
    explosion: list[ExplosionItemOut]
    total_materiales: float
    total_minutos: float = 0
    total_mano_obra: float = 0
    total: float = 0


class StockDescontadoOut(BaseModel):
    id_insumo: int
    insumo: str
    cantidad: float
    stock_restante: float
    unidad: Optional[str]


class ProduccionOut(BaseModel):
    status: str = "success"
    version: Optional[int] = None
    descontado: list[StockDescontadoOut]
    retazos_usados: list[int]
    retazos_perfil_generados: int = 0
    total_materiales: float
    total_minutos: float = 0
    total_mano_obra: float = 0
    total: float = 0


class RecipeItemOut(BaseModel):
    id: int
    componente: str
    cantidad_base: float

    @classmethod
    def from_model(cls, item):
        insumo = item.insumo
        return cls(
            id=item.id,
            componente=(insumo.name if insumo else None) or item.nombre or "Insumo",
            cantidad_base=float(item.cantidad_base or 0.0),
        )
