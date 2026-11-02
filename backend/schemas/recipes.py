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


class ExplosionOut(BaseModel):
    status: str = "success"
    explosion: list[ExplosionItemOut]
    total_materiales: float


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
