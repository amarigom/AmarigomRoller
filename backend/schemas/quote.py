from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from schemas.recipes import MAX_MEDIDA_CM

SIN_DATO = {
    'color': 'No especificado',
    'quality': 'Estándar',
    'fabric_type': 'No especificada',
    'observations': 'Sin observaciones',
}


class PresupuestoIn(BaseModel):
    email: EmailStr
    width: float = Field(..., gt=0, le=MAX_MEDIDA_CM)
    height: float = Field(..., gt=0, le=MAX_MEDIDA_CM)
    fabric_type: str = Field(SIN_DATO['fabric_type'], max_length=50)
    quality: str = Field(SIN_DATO['quality'], max_length=50)
    color: str = Field(SIN_DATO['color'], max_length=50)
    observations: Optional[str] = Field(SIN_DATO['observations'], max_length=2000)

    @field_validator('fabric_type', 'quality', 'color', 'observations', mode='before')
    @classmethod
    def _vacio_a_default(cls, v, info):
        if v is None or (isinstance(v, str) and not v.strip()):
            return SIN_DATO[info.field_name]
        return v.strip() if isinstance(v, str) else v
