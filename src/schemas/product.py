from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    product_type_id: int


class ProductType(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    name: str
    product_type_id: int
    product_type: ProductType
