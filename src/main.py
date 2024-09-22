from api.products import router as products_router
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
app = FastAPI()


app.include_router(products_router, prefix="/api")
