from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import Discount

pytestmark = pytest.mark.asyncio


async def test_fetch_discount_fail(
    async_client: AsyncClient, db_session: AsyncSession, fetch_discount_payload
) -> None:
    response = await async_client.post("/api/v1/discounts/fetch/", json=fetch_discount_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "no available discount found to be fetched"}


async def test_fetch_discount_success(
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
