import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


def pytest_generate_tests(metafunc):
    os.environ["TESTING"] = "True"


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
    sync(settings, silent=True)
    yield

    drop_database(str(settings.SQLALCHEMY_DATABASE_URI))

    # db = Database(str(settings.SQLALCHEMY_DATABASE_URI), force_rollback=True)

    # # Re-contruct the database for each run

    # yield db

    # dburl = apisecrets.DATABASE_URL
    # create_engine(dburl)
    # assert not database_exists(
    #     dburl), 'Test database already exists. Aborting tests.'
    # create_database(dburl)
    # alembic_config = Config("alembic.ini")
    # command.upgrade(alembic_config, "head")
    # # command.history(alembic_config, indicate_current=True)
    # yield
    # drop_database(dburl)
