from pydantic import BaseModel
from sqlalchemy import Enum


class CarSchema(BaseModel):
    id: int
    name: str
    brand: str

    class Config:
        orm_mode = True


class CarFilterSchema(BaseModel):
    name: str = None
    brand: str = None

    class Config:
        orm_mode = True


class CarFilter(str, Enum):
    name: str = "name"
    brand: str = "brand"
