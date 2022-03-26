import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import GenerateDiscountCodeController
from app.schemas.discount import DiscountCreateRequestSchema


@pytest.fixture
def generate_discount_payload(current_time_string):
    yield {
        "count": 5,
        "prefix": "campaign1",
        "expires_at": current_time_string,
        "percentage": 0.2,
        "purchase_info": {"product_id": "string", "store_id": "string", "brand_id": "string"},
    }


@pytest.fixture
def fetch_discount_payload():
    yield {"purchase_info": {"product_id": "string", "store_id": "string", "brand_id": "string"}}


@pytest_asyncio.fixture
async def generate_discount_code(db_session: AsyncSession, generate_discount_payload):
    await GenerateDiscountCodeController(db_session).generate(
        DiscountCreateRequestSchema(**generate_discount_payload)
    )
