import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

pytestmark = pytest.mark.asyncio


class TestFetchDiscountAPIValidation:
    async def test_fetch_discount_success(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        fetch_discount_payload,
        generate_discount_payload,
    ) -> None:
        await async_client.post("/api/v1/discounts/", json=generate_discount_payload)
        response = await async_client.post("/api/v1/discounts/fetch/", json=fetch_discount_payload)
        assert response.status_code == status.HTTP_200_OK
        assert "expires_at" in response.json()
        assert "percentage" in response.json()

    async def test_fetch_discount_fail(
        self, async_client: AsyncClient, db_session: AsyncSession, fetch_discount_payload
    ) -> None:
        fetch_discount_payload.pop("purchase_info", None)
        response = await async_client.post("/api/v1/discounts/fetch/", json=fetch_discount_payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "purchase_info" in response.content.decode("utf-8")
