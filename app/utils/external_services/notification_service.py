from app.utils.external_services.base import BaseExternalServiceCall


class NotificationServiceCall(BaseExternalServiceCall):
    async def notify_brand(self, discount):
        """
        Notify brand that user fetched a discount code
        """
        pass
