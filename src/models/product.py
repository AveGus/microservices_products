from sqlalchemy import Column, VARCHAR, Integer, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base


class ProductType(Base):
    __tablename__ = 'product_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    product_type_id = Column(Integer, ForeignKey('product_type.id'))
    product_type = relationship(ProductType, lazy='selectin')
