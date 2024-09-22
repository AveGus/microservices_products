from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError, NoResultFound
from schemas.product import ProductCreate
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product, ProductType
from services.database import get_async_session, Base


async def get_all_products(
        session: AsyncSession = Depends(get_async_session)
) -> list[Product]:
    stmt = select(Product)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_product(
        new_product: ProductCreate,
        session: AsyncSession = Depends(get_async_session)
) -> Product:
    try:
        product = Product(**new_product.dict())
        session.add(product)
        await session.flush()
        await session.commit()
        await session.refresh(product)
        return product
    except IntegrityError:
        await session.rollback()
        return None


async def get_product_by_id(
        id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Product | None:
    try:
        product = await session.execute(select(Product).where(Product.id == id))
        return product.scalar_one()
    except NoResultFound:
        return None


async def get_products_by_type(type_id: int,
                               session: AsyncSession = Depends(get_async_session)
                               ) -> list[Product]:
    product = await session.execute(select(Product).where(type_id == Product.product_type_id))
    return product.scalars()
