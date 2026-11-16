from typing import Optional

from pydantic import BaseModel


class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]

    @classmethod
    def from_model(cls, p):
        return cls(
            id=p.id,
            name=p.nombre,
            category=p.categoria or "General",
            description=p.descripcion,
        )
