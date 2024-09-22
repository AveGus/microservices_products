from api.products import router as products_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(products_router, prefix="/api")
