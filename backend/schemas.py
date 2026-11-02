# backend/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RolloBase(BaseModel):
    id: Optional[str] = None
    code: str = Field(..., description="Código del rollo (ej: Blackout-01)")
    name: str = Field(..., description="Nombre de la tela")
    color: Optional[str] = None
    width: float = Field(..., description="Ancho en metros")
    metersLeft: float = Field(..., alias="metersLeft", description="Metros disponibles")
    location: Optional[str] = "Depósito"

    class Config:
        # Esto es vital para que Python entienda el JSON que viene del frontend
        populate_by_name = True
        from_attributes = True

class InsumoIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    codigo_sku: Optional[str] = Field(None, max_length=50)
    categoria_id: int = Field(..., gt=0)
    unidad_medida: str = Field("metro", min_length=1, max_length=20)
    precio_costo_unitario: float = Field(0, ge=0)
    stock_actual: float = Field(0, ge=0)
    ancho_cm: float = Field(0, ge=0)


class ClienteIn(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    notas: Optional[str] = Field(None, max_length=2000)
