import abc

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import DiscountPurchaseInfo
from app.schemas.discount import DiscountPurchaseSchema


class BaseController(abc.ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_purchase_info(
        self, purchase_info: DiscountPurchaseSchema
    ) -> DiscountPurchaseInfo:
        instance, _ = await DiscountPurchaseInfo.get_or_create(self.session, **purchase_info.dict())
        return instance
