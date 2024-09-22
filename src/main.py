from api.products import router as products_router
from fastapi import FastAPI
from services.database import init_db_engine

init_db_engine()
app = FastAPI()


app.include_router(products_router, prefix="/api")
