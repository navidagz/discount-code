from datetime import datetime

import pytz

from app.config.settings import settings


def current_datetime():
    """
    Get current timezone aware datetime
    Returns:

    """
    return datetime.utcnow().replace(tzinfo=pytz.timezone(settings.TIMEZONE))
