from typing import List, Optional

from sqlalchemy.sql import select

from app.core.db import db
from app.domain.rdbms_connections.rdbms_connections_schema import (
    RDBMSConnectionsCreateSchema,
    RDBMSConnectionsDB,
)
from app.infrastructure.database.models.sqla_tables import t_rdbms_connections


class RDBMSConnectionsQueries:
    async def create_connection(
        self, rdbmsconn: RDBMSConnectionsCreateSchema
    ) -> t_rdbms_connections:
        query = t_rdbms_connections.insert()
        pk = await db.execute(query=query, values=rdbmsconn.__dict__)
        rdbmsconn.__dict__.update(
            {"connection_id": pk}
        )  # careful, does not consider default fields
        return rdbmsconn

    async def get_connection(self, connection_id: int) -> RDBMSConnectionsDB:
        query = select([t_rdbms_connections]).where(
            t_rdbms_connections.c.connection_id == connection_id
        )
        result_proxy = await db.fetch_all(query=query)
        ddd = [dict(zip(row.keys(), row.values())) for row in result_proxy]
        return [RDBMSConnectionsDB(**k) for k in ddd]

    async def delete_connection_by_id(self, connection_id: int) -> bool:
        query = t_rdbms_connections.delete().where(
            t_rdbms_connections.c.connection_id == connection_id
        )
        _ = await db.execute(query=query)  # always none
        return True
