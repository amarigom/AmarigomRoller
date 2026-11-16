from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from models.user import Role

MIN_PASSWORD_LENGTH = 10
MAX_PASSWORD_LENGTH = 128


def _normalizar_email(v):
    return v.strip().lower() if isinstance(v, str) else v


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=MAX_PASSWORD_LENGTH)

    _email = field_validator('email', mode='before')(_normalizar_email)


class UserCreateIn(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
    rol: Role = Role.VENTAS

    _email = field_validator('email', mode='before')(_normalizar_email)


class UserUpdateIn(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    rol: Optional[Role] = None
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)


class ChangePasswordIn(BaseModel):
    actual: str = Field(..., min_length=1, max_length=MAX_PASSWORD_LENGTH)
    nueva: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)


class UserOut(BaseModel):
    id: int
    email: str
    nombre: str
    rol: str
    activo: bool
    ultimo_login: Optional[datetime]

    @classmethod
    def from_model(cls, u):
        return cls(
            id=u.id, email=u.email, nombre=u.nombre, rol=u.rol,
            activo=u.activo, ultimo_login=u.ultimo_login,
        )


class TokenOut(BaseModel):
    token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserOut
    permissions: list[str]
