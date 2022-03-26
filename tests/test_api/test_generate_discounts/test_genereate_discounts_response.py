from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

pytestmark = pytest.mark.asyncio


class TestGenerateDiscountAPIResponse:
    async def test_generate_discounts_fail(
        self, async_client: AsyncClient, db_session: AsyncSession, generate_discount_payload
    ) -> None:
        with mock.patch(
            "app.api.v1.generate_discounts.GenerateDiscountCodeController"
        ) as mock_generate:
            mock_generate.return_value.generate.side_effect = Exception("test-exception")
            response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'detail': {'msg': 'Can not create discount code', 'success': False}
        }

    async def test_generate_discounts_success(
        self, async_client: AsyncClient, db_session: AsyncSession, generate_discount_payload
    ) -> None:
        response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"success": True, "msg": ""}

    async def test_generate_discount_success_with_existing_purchase_info(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        generate_discount_payload
    ):
        await async_client.post("/api/v1/discounts/", json=generate_discount_payload)
        response = await async_client.post("/api/v1/discounts/", json=generate_discount_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"success": True, "msg": ""}
