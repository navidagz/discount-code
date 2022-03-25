from typing import Dict

from fastapi import HTTPException, status

from app.controllers.base import BaseController
from app.db import Discount
from app.schemas.discount import FetchDiscountRequestSchema, DiscountPurchaseSchema
from app.utils.external_services.notification_service import NotificationServiceCall


class FetchDiscountCodeController(BaseController):
    """
    Fetch Discount Code Controller
    """

    async def _fetch_available_discount_code(self, purchase_info: DiscountPurchaseSchema):
        """
        Fetch available discount code
        Args:
            purchase_info (FetchDiscountRequestSchema): purchase info

        Returns:
            Discount object

        Exceptions:
            404-HTTPException:
                raises when there is no discount code available
        """

        discount = await Discount.get_available_discount_codes(self.session, purchase_info)
        if not discount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no available discount found to be fetched",
            )
        return discount

    async def _update_discount_and_set_user_id(self, discount: Discount, user_id: str):
        await discount.update_record(self.session, {"user_id": user_id})

    async def fetch(self, payload: FetchDiscountRequestSchema, user_id: str) -> Dict:
        """
        Fetch discount code for user

        Args:
            payload (FetchDiscountRequestSchema): payload for fetching discount code
            user_id (str): user id

        Returns:
            Discount obj
        """

        discount = await self._fetch_available_discount_code(payload.purchase_info)

        await self._update_discount_and_set_user_id(discount, user_id)
        await NotificationServiceCall().notify_brand(discount)

        return discount
