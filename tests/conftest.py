import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module", autouse=True)
def prepare_database() -> Generator:
    """Prepare an empty test database"""
    from databases import Database
    from app.core.config import settings
    from app.utils.migrations import sync

    from sqlbag.createdrop import create_database, drop_database

    print("\nprep database")
    print(settings.SQLALCHEMY_DATABASE_URI)

    create_database(
        str(settings.SQLALCHEMY_DATABASE_URI), wipe_if_existing=False
    )
    print("\ndatabase created")
    sync(settings, silent=True)
    print("\ndatabase synced")
    yield

    drop_database(str(settings.SQLALCHEMY_DATABASE_URI))
