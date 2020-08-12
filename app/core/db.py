import logging
import os

from databases import Database

from app.core.config import settings

logger = logging.getLogger(__name__)

if os.environ.get("TESTING") == "true":
    db = Database(str(settings.SQLALCHEMY_DATABASE_URI), force_rollback=True)
else:
    db = Database(str(settings.SQLALCHEMY_DATABASE_URI))
