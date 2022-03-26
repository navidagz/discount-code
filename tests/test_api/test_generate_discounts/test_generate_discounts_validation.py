from datetime import timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.utils.datetime_utils import current_datetime

pytestmark = pytest.mark.asyncio


class TestGenerateDiscountsAPIValidation:
    async def test_generate_discounts_success(
        self, async_client: AsyncClient, db_session: AsyncSession, generate_discount_payload
    ) -> None:
        response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"success": True, "msg": ""}

    async def test_generate_discounts_missing_payload(
        self, async_client: AsyncClient, db_session: AsyncSession, generate_discount_payload
    ) -> None:
        generate_discount_payload.pop("percentage", None)

        response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "percentage" in response.content.decode("utf-8")

    async def test_generate_discounts_expires_at_in_the_pass(
        self, async_client: AsyncClient, db_session: AsyncSession, generate_discount_payload
    ) -> None:
        generate_discount_payload["expires_at"] = (
            current_datetime() - timedelta(days=10)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "expires_at can not be in the past" in response.content.decode("utf-8")
