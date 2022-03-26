import pytest
import pytest_asyncio
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import GenerateDiscountCodeController
from app.db import Discount, DiscountPurchaseInfo
from app.schemas.discount import DiscountCreateRequestSchema

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def controller(db_session: AsyncSession):
    yield GenerateDiscountCodeController(db_session)


@pytest_asyncio.fixture()
async def generate_discounts_payload(current_time_string):
    yield DiscountCreateRequestSchema(
        **{
            "count": 5,
            "prefix": "campaign1",
            "expires_at": current_time_string,
            "percentage": 0.2,
            "purchase_info": {"product_id": "string", "store_id": "string", "brand_id": "string"},
        }
    )


class TestGenerateDiscountController:
    async def test_generate_discount_controller_pass(
        self, controller, db_session: AsyncSession, generate_discounts_payload
    ):
        await controller.generate(generate_discounts_payload)
        assert (
            await db_session.execute(select(func.count()).select_from(select(Discount).subquery()))
        ).scalar_one() == generate_discounts_payload.count
        assert (
            await db_session.execute(
                select(func.count()).select_from(select(DiscountPurchaseInfo).subquery())
            )
        ).scalar_one() == 1
