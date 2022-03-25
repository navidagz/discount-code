from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import FetchDiscountCodeController
from app.dependencies import db_session
from app.schemas.discount import FetchDiscountResponseSchema, FetchDiscountRequestSchema
from app.utils.logger import get_logger

fetch_discount_router = APIRouter()
logger = get_logger(__file__)


@fetch_discount_router.post(
    "/", status_code=status.HTTP_200_OK, response_model=FetchDiscountResponseSchema
)
async def fetch_discount(
    payload: FetchDiscountRequestSchema, session: AsyncSession = Depends(db_session)
):
    return await FetchDiscountCodeController(session=session).fetch(
        payload, user_id="user-number-1"
    )
