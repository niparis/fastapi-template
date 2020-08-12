import datetime as dt
import logging
import os
from typing import Any, List

import pytest
from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.core.db import db
from app.domain.users.users_schema import (
    UserBase,
    UserCreateSchema,
    UserDBSchema,
    UserUpdateSchema,
)
from app.main import create_app
from app.routes.endpoints.routes_users import router

logger = logging.getLogger(__name__)

USER_MODEL = UserBase(
    name="bob",
    email="bob@microsoft.usa",
    full_name="90909090",
    is_superuser=False,
)


@pytest.fixture
def user_model() -> UserBase:
    return USER_MODEL


@pytest.fixture
def user_schema() -> UserDBSchema:
    return UserDBSchema(
        user_id=1,
        name="bob",
        email="bob@microsoft.usa",
        full_name="90909090",
        is_superuser=False,
    )


class TestUserRouter:
    def test_user_create_valide(
        self,
        client: TestClient,
        user_model: UserBase,
        user_schema: UserDBSchema,
    ) -> None:
        print(f"in test {os.environ.get('TESTING', 'PROD')}")
        response = client.post(
            "/users/",
            json={
                "name": "bob",
                "email": "bob@microsoft.usa",
                "full_name": "90909090",
                "is_superuser": False,
                "password": "nnnn",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == user_schema.__dict__
