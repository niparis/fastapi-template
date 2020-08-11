# isort:skip_file
import logging
import sys

sys.path.extend(["./"])

from sentry_sdk import init as initialize_sentry
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi import FastAPI

# from app.application import app
from app.routes.api import api_router
from app.core.config import settings
from app.core.db import db
from app.utils.middleware import PerformanceMonitoringMiddleware
from app import __version__, SERVICE_NAME
from app.utils.exception_handlers import not_found_exception_handler
from app.utils.exceptions import EntityNotFound


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    if settings.SENTRY_DSN.__str__() not in ("None", ""):
        initialize_sentry(
            dsn=settings.SENTRY_DSN.__str__(),
            integrations=[SqlalchemyIntegration()],
        )

    logger.info("Initiliase fast-API app")
    app = FastAPI(
        title=SERVICE_NAME,
        version=__version__,
        on_startup=[db.connect],
        on_shutdown=[db.disconnect],
    )
    # db.init_app(app=app)

    @api_router.get("/")
    async def healthcheck() -> dict:
        """
            Checks that we are connected to database and return service information
        """
        query = "SELECT 1;"
        await db.fetch_one(query=query)
        return {
            "service": SERVICE_NAME,
            "version": __version__,
        }

    app.include_router(api_router)

    if settings.SENTRY_DSN.__str__() not in ("None", ""):
        app.add_middleware(SentryAsgiMiddleware)

    app.add_middleware(PerformanceMonitoringMiddleware)

    # Exceptions handles
    app.add_exception_handler(EntityNotFound, not_found_exception_handler)

    return app


try:
    app = create_app()
except Exception as e:
    logger.error(f"Error in fast-API app initialisation => {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
