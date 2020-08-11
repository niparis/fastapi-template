from sqlalchemy.orm import Session

from app.domain.rdbms_connections.rdbms_connections_service import (
    RDBMSConnectionsService,
)
from app.domain.users.users_service import UserService
from app.infrastructure.database.queries.rdbms_connection import (
    RDBMSConnectionsQueries,
)
from app.infrastructure.database.queries.user import UserQueries


def get_user_services() -> UserService:
    return UserService(UserQueries())


def get_rdbms_connections_service() -> RDBMSConnectionsService:
    return RDBMSConnectionsService(RDBMSConnectionsQueries())
