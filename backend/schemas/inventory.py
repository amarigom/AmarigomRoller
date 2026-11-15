from datetime import datetime
from decimal import Decimal
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
    es_tela: bool = False
    precio_m2: Optional[float] = Field(None, ge=0, allow_inf_nan=False)
    unidad_compra: Optional[str] = Field(None, min_length=1, max_length=20)
    factor_conversion: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=4, allow_inf_nan=False)

    @model_validator(mode='after')
    def validar_tela(self):
        if self.es_tela and (self.unidad_medida != 'metro' or self.ancho_cm <= 0):
            raise ValueError('La tela requiere stock en metro lineal y ancho positivo en cm')
        if not self.es_tela and self.precio_m2 is not None:
            raise ValueError('El precio por m² solo corresponde a telas')
        if (self.unidad_compra is None) != (self.factor_conversion is None):
            raise ValueError('La unidad de compra y el factor de conversión deben indicarse juntos')
        return self


class TelaConfigIn(BaseModel):
    ancho_cm: float = Field(..., gt=0, allow_inf_nan=False)
    largo_pieza_cm: Optional[float] = Field(None, gt=0, allow_inf_nan=False)
    precio_m2: Optional[float] = Field(None, ge=0, allow_inf_nan=False)
    unidad_compra: Optional[str] = Field(None, min_length=1, max_length=20)
    factor_conversion: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=4, allow_inf_nan=False)

    @model_validator(mode='after')
    def validar_compra(self):
        if (self.unidad_compra is None) != (self.factor_conversion is None):
            raise ValueError('La unidad de compra y el factor de conversión deben indicarse juntos')
        return self


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
    es_tela: bool
    precio_m2: Optional[float]
    largo_pieza_cm: Optional[float]
    unidad_compra: Optional[str]
    factor_conversion: Optional[float]
    perfil_en_receta: bool = False
    piezas_enteras: int = 0
    piezas_retazos: int = 0
    longitud_piezas_cm: float = 0
    piezas_conciliadas: Optional[bool] = None

    @classmethod
    def from_model(cls, s, perfil=False, resumen=None):
        stock = float(s.stock_actual or 0)
        resumen = resumen or {'enteras': 0, 'retazos': 0, 'total_cm': 0}
        conciliadas = None
        if perfil and s.unidad_medida in ('cm', 'metro'):
            conciliadas = stock * (100 if s.unidad_medida == 'metro' else 1) == float(resumen['total_cm'])
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
            es_tela=s.es_tela,
            precio_m2=float(s.precio_m2) if s.precio_m2 is not None else None,
            largo_pieza_cm=float(s.largo_pieza_cm) if s.largo_pieza_cm is not None else None,
            unidad_compra=s.unidad_compra,
            factor_conversion=float(s.factor_conversion) if s.factor_conversion is not None else None,
            perfil_en_receta=perfil, piezas_enteras=resumen['enteras'], piezas_retazos=resumen['retazos'],
            longitud_piezas_cm=float(resumen['total_cm']), piezas_conciliadas=conciliadas,
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


class ProfilePiecesIn(BaseModel):
    cantidad: int = Field(..., gt=0, le=1000)
    referencia: Optional[str] = Field(None, max_length=255)


class ProfilePieceIn(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    longitud_original_cm: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, allow_inf_nan=False)
    longitud_actual_cm: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2, allow_inf_nan=False)
    es_retazo: bool

    @model_validator(mode='after')
    def validar_longitud(self):
        if self.longitud_actual_cm > self.longitud_original_cm:
            raise ValueError('La longitud actual no puede superar la original')
        if not self.es_retazo and self.longitud_actual_cm not in (0, self.longitud_original_cm):
            raise ValueError('Una pieza parcial debe ser un retazo')
        return self


class ProfileReconcileIn(BaseModel):
    stock_esperado: Decimal = Field(..., ge=0, max_digits=12, decimal_places=4, allow_inf_nan=False)
    piezas_esperadas: list[ProfilePieceIn] = Field(..., max_length=1000)
    piezas: list[ProfilePieceIn] = Field(..., max_length=1000)
    motivo: str = Field(..., min_length=1, max_length=255)

    @model_validator(mode='after')
    def validar_piezas(self):
        self.motivo = self.motivo.strip()
        if not self.motivo:
            raise ValueError('Indicá el motivo de la conciliación')
        for piezas in (self.piezas_esperadas, self.piezas):
            ids = [p.id for p in piezas if p.id is not None]
            if len(ids) != len(set(ids)):
                raise ValueError('No repitas identificadores de piezas')
        if any(p.id is None or p.longitud_actual_cm == 0 for p in self.piezas_esperadas):
            raise ValueError('Las piezas esperadas deben ser piezas activas con identificador')
        if any(p.id is None and p.longitud_actual_cm == 0 for p in self.piezas):
            raise ValueError('No se puede crear una pieza sin longitud')
        return self


class PurchaseIn(BaseModel):
    cantidad: Decimal = Field(..., gt=0, max_digits=12, decimal_places=4, allow_inf_nan=False)
    referencia: Optional[str] = Field(None, max_length=255)


class StockMinimumIn(BaseModel):
    stock_minimo: float = Field(..., ge=0, allow_inf_nan=False)


class StockReconcileIn(BaseModel):
    stock_esperado: Decimal = Field(..., ge=0, max_digits=12, decimal_places=4, allow_inf_nan=False)
    historial_esperado: Decimal = Field(..., max_digits=14, decimal_places=4, allow_inf_nan=False)
    stock_contado: Decimal = Field(..., ge=0, max_digits=12, decimal_places=4, allow_inf_nan=False)
    motivo: str = Field(..., min_length=1, max_length=255)

    @model_validator(mode='after')
    def validar_motivo(self):
        self.motivo = self.motivo.strip()
        if not self.motivo:
            raise ValueError('Indicá el motivo de la conciliación')
        return self


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
    precio_m2: Optional[float] = Field(None, ge=0, allow_inf_nan=False)


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


class FabricPriceCsvIn(BaseModel):
    csv: str = Field(..., min_length=1, max_length=500000)
    aplicar: bool = False
    motivo: Optional[str] = Field(None, max_length=255)


class InventoryMovementOut(BaseModel):
    id: int
    tipo: str
    cantidad: float
    stock_resultante: float
    referencia: Optional[str]
    notas: Optional[str]
    creado_en: datetime
    usuario: Optional[str]
    unidad: Optional[str]

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, tipo=m.tipo, cantidad=float(m.cantidad),
                   stock_resultante=float(m.stock_resultante), referencia=m.referencia,
                   notas=m.notas, creado_en=m.creado_en,
                   usuario=m.usuario.nombre if m.usuario else None, unidad=m.unidad)


class PriceHistoryOut(BaseModel):
    id: int
    precio: float
    precio_m2: Optional[float]
    vigente_desde: datetime
    motivo: Optional[str]
    usuario: Optional[str]
    unidad: Optional[str]

    @classmethod
    def from_model(cls, p):
        return cls(id=p.id, precio=float(p.precio),
                   precio_m2=float(p.precio_m2) if p.precio_m2 is not None else None, vigente_desde=p.vigente_desde,
                   motivo=p.motivo, usuario=p.usuario.nombre if p.usuario else None, unidad=p.unidad)


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
