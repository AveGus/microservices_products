from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.products import get_product_by_id as get_product_by_id_service
from services.products import get_products_by_type as get_products_by_type_service
from schemas.product import ProductCreate, Product
from services.database import get_async_session
from services.products import get_all_products, create_product

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/",
            summary="Getting all products in database",
            description="Getting all products by the request in database with SQLAlchemy and asyncio",
            response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_async_session)):
    return await get_all_products(session)


@router.post("/",
             summary="Creating a new product",
             description="Creating a new product with pydantic model",
             response_model=Product)
async def add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    product = await create_product(new_product, session)
    if product is None:
        raise HTTPException(status_code=404, detail="Product could not be created")
    else:

        return product


@router.get("/{product_id}",
            summary="Getting a product by id",
            description="Getting a product by id by using SQLAlchemy model",
            response_model=Product)
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_async_session)):
    product = await get_product_by_id_service(product_id, session)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return product


@router.get("/type/{type_id}",
            summary="Getting a product by type",
            description="Getting a product by type by using SQLAlchemy model",
            response_model=list[Product])
async def get_product_by_type(type_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await get_products_by_type_service(type_id, session)
    return result
