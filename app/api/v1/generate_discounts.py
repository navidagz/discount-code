from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import GenerateDiscountCodeController
from app.dependencies import db_session
from app.schemas.discount import DiscountCreateResponseSchema, DiscountCreateRequestSchema
from app.utils.logger import get_logger

generate_discount_router = APIRouter()
logger = get_logger(__file__)


@generate_discount_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=DiscountCreateResponseSchema
)
async def generate_branch_discount(
    payload: DiscountCreateRequestSchema, session: AsyncSession = Depends(db_session)
):
    try:
        await GenerateDiscountCodeController(session=session).generate(payload)
        return DiscountCreateResponseSchema(success=True)
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            DiscountCreateResponseSchema(success=False, msg="Can not create discount code").dict(),
        )
