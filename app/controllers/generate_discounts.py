from typing import Dict

from app.controllers.base import BaseController
from app.db import Discount, DiscountPurchaseInfo
from app.schemas.discount import DiscountCreateRequestSchema, DiscountPurchaseSchema


class GenerateDiscountCodeController(BaseController):
    """
    Generate Discount Codes Controller
    """

    async def _create_payload_for_controller(self, payload) -> Dict:
        payload_dict = {
            **payload.dict(),
            "purchase_info_id": (
                await self.get_purchase_info(purchase_info=payload.purchase_info)
            ).id,
        }
        payload_dict.pop("purchase_info", None)
        return payload_dict

    async def generate(self, payload: DiscountCreateRequestSchema):
        return await Discount.bulk_create_discount_code(
            self.session, **(await self._create_payload_for_controller(payload))
        )
