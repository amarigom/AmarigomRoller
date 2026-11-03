from typing import Optional

from pydantic import BaseModel, Field


class InsumoIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    codigo_sku: Optional[str] = Field(None, max_length=50)
    categoria_id: int = Field(..., gt=0)
    unidad_medida: str = Field("metro", min_length=1, max_length=20)
    precio_costo_unitario: float = Field(0, ge=0)
    stock_actual: float = Field(0, ge=0)
    ancho_cm: float = Field(0, ge=0)
    largo_pieza_cm: Optional[float] = Field(None, gt=0)


class SupplyOut(BaseModel):
    id: int
    code: Optional[str]
    name: str
    category: str
    metersLeft: float
    widthCm: float
    unit: Optional[str]
    price: float
    totalMeters: float

    @classmethod
    def from_model(cls, s):
        stock = float(s.stock_actual or 0)
        return cls(
            id=s.id,
            code=s.codigo_sku,
            name=s.name,
            category=s.category.name if s.category else "Sin Categoría",
            metersLeft=stock,
            widthCm=float(s.ancho_cm or 0),
            unit=s.unidad_medida,
            price=float(s.precio_costo_unitario or 0),
            totalMeters=stock,
        )


class CategoryOut(BaseModel):
    id: int
    name: str

    @classmethod
    def from_model(cls, c):
        return cls(id=c.id, name=c.name)
