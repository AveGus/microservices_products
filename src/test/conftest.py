import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from main import app
from models import ProductType
from schemas.product import ProductCreate
from services.database import Base, get_async_session
from config import DB_USER_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_NAME_TEST, DB_HOST_TEST
from services.products import create_product

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def product(product_factory):
    return await product_factory(name="Orange")


@pytest.fixture
async def product_type(product_type_factory):
    return await product_type_factory(name="Food")


@pytest.fixture
def product_factory(product_type_factory):
    async def factory(**kwargs):
        product_type = await product_type_factory(name='Test Product')
        async with async_session_maker() as session:
            product = ProductCreate(
                product_type_id=product_type.id,
                **kwargs
            )
            product = await create_product(product, session)
        return product

    return factory


@pytest.fixture
def product_type_factory():
    async def factory(**kwargs):
        async with async_session_maker() as session:
            product_type = ProductType(**kwargs)
            session.add(product_type)
            await session.commit()
            await session.refresh(product_type)
        return product_type

    return factory
