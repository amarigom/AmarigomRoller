from typing import Optional

from pydantic import BaseModel, Field

MAX_MEDIDA_CM = 1000


class MedidasIn(BaseModel):
    w: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)
    h: float = Field(100.0, gt=0, le=MAX_MEDIDA_CM)


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
            componente=(insumo.name if insumo else None) or item.nombre_producto or "Insumo",
            cantidad_base=float(item.cantidad_base or 0.0),
        )
