from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class InsumoIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    codigo_sku: Optional[str] = Field(None, max_length=50)
    categoria_id: int = Field(..., gt=0)
    unidad_medida: str = Field("metro", min_length=1, max_length=20)
    precio_costo_unitario: float = Field(0, ge=0, allow_inf_nan=False)
    stock_actual: float = Field(0, ge=0, allow_inf_nan=False)
    stock_minimo: float = Field(0, ge=0, allow_inf_nan=False)
    ancho_cm: float = Field(0, ge=0, allow_inf_nan=False)
    largo_pieza_cm: Optional[float] = Field(None, gt=0, allow_inf_nan=False)


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
    stock_minimo: float

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
            stock_minimo=float(s.stock_minimo or 0),
        )


class CategoryOut(BaseModel):
    id: int
    name: str

    @classmethod
    def from_model(cls, c):
        return cls(id=c.id, name=c.name)


class InventoryMovementIn(BaseModel):
    tipo: Literal['entrada', 'ajuste']
    cantidad: float = Field(..., allow_inf_nan=False)
    referencia: Optional[str] = Field(None, max_length=255)
    notas: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode='after')
    def validar_cantidad(self):
        if self.tipo == 'entrada' and self.cantidad <= 0:
            raise ValueError('La entrada debe ser mayor a cero')
        if self.tipo == 'ajuste' and self.cantidad == 0:
            raise ValueError('El ajuste no puede ser cero')
        return self


class StockMinimumIn(BaseModel):
    stock_minimo: float = Field(..., ge=0, allow_inf_nan=False)


class ScrapReservationIn(BaseModel):
    referencia: str = Field(..., min_length=1, max_length=255)

    @model_validator(mode='after')
    def referencia_no_vacia(self):
        self.referencia = self.referencia.strip()
        if not self.referencia:
            raise ValueError('La referencia no puede estar vacía')
        return self


class BulkPriceItemIn(BaseModel):
    id_insumo: int = Field(..., gt=0)
    precio: float = Field(..., ge=0, allow_inf_nan=False)


class BulkPriceIn(BaseModel):
    porcentaje: Optional[float] = Field(None, ge=-100, le=10000, allow_inf_nan=False)
    items: Optional[list[BulkPriceItemIn]] = Field(None, min_length=1, max_length=500)
    motivo: Optional[str] = Field(None, max_length=255)

    @model_validator(mode='after')
    def exactamente_una_fuente(self):
        if (self.porcentaje is None) == (self.items is None):
            raise ValueError('Indicá un porcentaje o una lista de precios, pero no ambos')
        if self.items and len({i.id_insumo for i in self.items}) != len(self.items):
            raise ValueError('No repitas insumos en la lista de precios')
        return self


class InventoryMovementOut(BaseModel):
    id: int
    tipo: str
    cantidad: float
    stock_resultante: float
    referencia: Optional[str]
    notas: Optional[str]
    creado_en: datetime
    usuario: Optional[str]

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, tipo=m.tipo, cantidad=float(m.cantidad),
                   stock_resultante=float(m.stock_resultante), referencia=m.referencia,
                   notas=m.notas, creado_en=m.creado_en,
                   usuario=m.usuario.nombre if m.usuario else None)


class PriceHistoryOut(BaseModel):
    id: int
    precio: float
    vigente_desde: datetime
    motivo: Optional[str]
    usuario: Optional[str]

    @classmethod
    def from_model(cls, p):
        return cls(id=p.id, precio=float(p.precio), vigente_desde=p.vigente_desde,
                   motivo=p.motivo, usuario=p.usuario.nombre if p.usuario else None)


class StockAlertOut(BaseModel):
    id_insumo: int
    insumo: str
    stock_actual: float
    stock_minimo: float
    faltante: float
    unidad: Optional[str]


class ScrapOut(BaseModel):
    id: int
    insumo: str
    ancho_cm: float
    largo_cm: float
    fecha_generado: datetime
    referencia: Optional[str]
    estado: str

    @classmethod
    def from_model(cls, r):
        return cls(id=r.id, insumo=r.insumo_base.name, ancho_cm=float(r.ancho_cm),
                   largo_cm=float(r.largo_cm), fecha_generado=r.fecha_generado,
                   referencia=r.referencia, estado=r.estado)
