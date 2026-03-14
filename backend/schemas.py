# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class RolloBase(BaseModel):
    id: Optional[str] = None
    code: str = Field(..., description="Código del rollo (ej: Blackout-01)")
    name: str = Field(..., description="Nombre de la tela")
    color: str
    width: float = Field(..., description="Ancho en metros")
    metersLeft: float = Field(..., alias="metersLeft", description="Metros disponibles")
    location: Optional[str] = "Depósito"

    class Config:
        # Esto es vital para que Python entienda el JSON que viene del frontend
        populate_by_name = True
        from_attributes = True