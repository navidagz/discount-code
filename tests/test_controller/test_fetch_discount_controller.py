import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import FetchDiscountCodeController
from app.schemas.discount import FetchDiscountRequestSchema

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def controller(db_session: AsyncSession):
    yield FetchDiscountCodeController(db_session)


@pytest_asyncio.fixture
async def fetch_discount_payload():
    yield FetchDiscountRequestSchema(
        **{"purchase_info": {"product_id": "string", "store_id": "string", "brand_id": "string"}}
    )


class TestFetchDiscountController:
    async def test_fetch_discount_controller_pass(
        self, controller, db_session: AsyncSession, fetch_discount_payload, generate_discount_code
    ):
        discount = await controller.fetch(fetch_discount_payload, user_id="test-user-id")
        assert discount.redeemed == False
        assert discount.user_id == "test-user-id"
        assert discount.is_expired == False
        assert discount.is_discount_valid == True

    async def test_fetch_discount_controller_no_discount_available(
        self, controller, db_session: AsyncSession, fetch_discount_payload
    ):
        with pytest.raises(HTTPException) as exc:
            await controller.fetch(fetch_discount_payload, user_id="test-user-id")

        assert "no available discount found to be fetched" in str(exc)
