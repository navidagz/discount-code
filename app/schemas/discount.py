from datetime import datetime

from pydantic import Field, validator

from app.schemas.base import BaseSchema
from app.utils.datetime_utils import current_datetime


class DiscountPurchaseSchema(BaseSchema):
    product_id: str
    store_id: str
    brand_id: str


class DiscountCreateRequestSchema(BaseSchema):
    count: int = Field(default=1, ge=1, le=50)
    prefix: str = ""
    expires_at: datetime = None
    percentage: float = Field(gt=0.0, le=1.0)

    purchase_info: DiscountPurchaseSchema

    @validator("expires_at")
    def expires_at_not_in_past(cls, expires_at):
        if expires_at is not None and expires_at <= current_datetime():
            raise ValueError("expires_at can not be in the past")

        return expires_at


class DiscountCreateResponseSchema(BaseSchema):
    success: bool
    msg: str = ""


class FetchDiscountRequestSchema(BaseSchema):
    purchase_info: DiscountPurchaseSchema


class FetchDiscountResponseSchema(BaseSchema):
    code: str
    expires_at: datetime
