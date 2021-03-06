import logging
import os

from databases import Database

from app.core.config import settings

logger = logging.getLogger(__name__)

if settings.TESTING:
    db = Database(str(settings.SQLALCHEMY_DATABASE_URI), force_rollback=True)
else:
    db = Database(str(settings.SQLALCHEMY_DATABASE_URI))
