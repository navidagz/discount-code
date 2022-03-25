from fastapi import APIRouter

from app.api.v1.fetch_discount import fetch_discount_router as v1_fetch_discount_router
from app.api.v1.generate_discounts import generate_discount_router as v1_generate_discount_router

v1_api_router = APIRouter(prefix="/v1")

v1_api_router.include_router(
    router=v1_generate_discount_router, prefix="/discounts", tags=["Generate Discounts V1"]
)
v1_api_router.include_router(
    router=v1_fetch_discount_router, prefix="/discounts/fetch", tags=["Fetch Discount V1"]
)
