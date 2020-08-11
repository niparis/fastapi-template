from fastapi import APIRouter

from app import __version__
from app.api.endpoints import routes_rdbms_conn, routes_users
from app.core.config import settings
from app.core.db import db

api_router = APIRouter()
api_router.include_router(routes_users.router, prefix="/users", tags=["users"])
api_router.include_router(
    routes_rdbms_conn.router, prefix="/rdbmsconn", tags=["RDBMS connections"]
)
