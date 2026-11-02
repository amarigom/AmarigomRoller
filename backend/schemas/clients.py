from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class ClienteIn(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    notas: Optional[str] = Field(None, max_length=2000)

    @field_validator('nombre', 'apellido', 'email', mode='before')
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class ClienteOut(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str]
    email: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]

    @classmethod
    def from_model(cls, c):
        return cls(
            id=c.id,
            nombre=f"{c.nombre} {c.apellido}",
            telefono=c.telefono,
            email=c.email,
            direccion=c.direccion,
            ciudad=c.ciudad,
        )
