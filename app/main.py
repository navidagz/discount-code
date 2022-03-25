import os
import time

from fastapi import FastAPI

from app.api.router import v1_api_router
from app.config.settings import settings

os.environ["TZ"] = settings.TIMEZONE
time.tzset()


def get_app():
    fastapi_app = FastAPI(title="Discount Code", debug=settings.DEBUG)
    fastapi_app.include_router(v1_api_router, prefix="/api")
    return fastapi_app


app = FastAPI(title="Discount Code", debug=settings.DEBUG)
app.include_router(v1_api_router, prefix="/api")


@app.get("/health")
def main():
    return {"status": "ok"}
