import random
import secrets
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String,
    TIMESTAMP,
    Integer,
    Boolean,
    FLOAT,
    Index,
    ForeignKey,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

from app.config.settings import settings
from app.db.base import Base
from app.schemas.discount import DiscountPurchaseSchema
from app.utils.datetime_utils import current_datetime


class DiscountPurchaseInfo(Base):
    __tablename__ = "discount_purchase_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(String, nullable=False, index=True)
    brand_id = Column(String, nullable=False, index=True)
    product_id = Column(String, nullable=False, index=True)

    discounts = relationship("Discount", backref="purchase_info")

    __table_args__ = (
        Index("discount_purchase_info_indices", "store_id", "brand_id", "product_id"),
    )


class Discount(Base):
    __tablename__ = "discount"

    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(String, nullable=False, unique=True, index=True)
    percentage = Column(FLOAT, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)
    expires_at = Column(TIMESTAMP)

    redeemed = Column(Boolean, default=False)
    redeemed_at = Column(TIMESTAMP)
    user_id = Column(String, index=True)

    purchase_info_id = Column(
        Integer, ForeignKey(f"{DiscountPurchaseInfo.__tablename__}.id"), nullable=False
    )

    @property
    def is_expired(self) -> bool:
        """
        Is code expired or not

        Returns:
            boolean indicates code has expired or not
        """
        return datetime.utcnow() > self.expires_at if self.expires_at else False

    @property
    def is_discount_valid(self) -> bool:
        """
        Is discount code valid or not (takes expiration date and redeemed into account)

        Returns:
            boolean indicates code is valid or not
        """
        return not self.is_expired and not self.redeemed

    async def redeem_discount(self, session: AsyncSession):  # pragma: no cover
        """
        Redeem discount code

        Args:
            session (AsyncSession): db session

        """
        self.redeemed = True
        self.redeemed_at = func.now()
        await session.commit()

    @classmethod
    def generate_new_discount_code(cls, prefix: str = "") -> str:
        """
        Generate discount code using secrets library
        If prefix is available, it will be added to the beginning of the discount code

        Args:
            prefix (str): prefix to be added to the beginning of code

        Returns:
            code (str): generated code
        """
        code_length = random.randrange(
            settings.MIN_CODE_LENGTH_WITHOUT_PREFIX, settings.MAX_CODE_LENGTH_WITHOUT_PREFIX
        )
        code = secrets.token_urlsafe(code_length)

        if prefix:
            code = f"{prefix}-{code}"

        return code

    @classmethod
    async def bulk_create_discount_code(
        cls, session: AsyncSession, purchase_info_id: int, **kwargs
    ):
        """
        Bulk create discount codes

        Args:
            session (AsyncSession): db session
            purchase_info_id (int): purchase info id

        """
        prefix = kwargs.pop("prefix")
        count = kwargs.pop("count")
        discount_objs = [
            Discount(
                code=Discount.generate_new_discount_code(prefix=prefix),
                purchase_info_id=purchase_info_id,
                **kwargs,
            )
            for _ in range(count)
        ]
        session.add_all(discount_objs)
        await session.commit()

    @classmethod
    async def get_available_discount_codes(
        cls, session: AsyncSession, purchase_info: DiscountPurchaseSchema
    ):
        """
        Gets available discount code which matches the following criteria
        1. discount is not assigned to user
        2. is not redeemed
        3. is not expired
        4. matches the purchase info

        Args:
            session (AsyncSession): db session
            purchase_info (DiscountPurchaseSchema): purchase info

        Returns:
            Discount instance or None
        """

        cls: Discount
        q = (
            select(cls)
            .join(DiscountPurchaseInfo, cls.purchase_info_id == DiscountPurchaseInfo.id)
            .where(cls.user_id == None, cls.redeemed == False, cls.expires_at > datetime.utcnow())
        )
        q = cls.build_where(DiscountPurchaseInfo, q, purchase_info.dict())
        return (await session.execute(q)).scalars().first()
