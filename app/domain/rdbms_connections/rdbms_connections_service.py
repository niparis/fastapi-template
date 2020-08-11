from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.domain.rdbms_connections.rdbms_connections_schema import (
    RDBMSConnectionsCreateSchema,
    RDBMSConnectionsDB,
)


class RDBMSConnectionsService:
    def __init__(self, rdms_queries: Any):
        self.__rdbms_queries = rdms_queries

    async def create_rdbmsconn(
        self, rdbmsconn: RDBMSConnectionsCreateSchema
    ) -> RDBMSConnectionsDB:
        new_rdbmsconn = await self.__rdbms_queries.create_connection(rdbmsconn)
        return RDBMSConnectionsDB.from_orm(new_rdbmsconn)

    async def get_rdbmsconn_by_id(self, conn_id: int) -> RDBMSConnectionsDB:
        rdbmsconn = await self.__rdbms_queries.get_connection(conn_id)
        if rdbmsconn:
            return rdbmsconn[0]

        return None

    async def delete_rdbmsconn_by_id(self, conn_id: int) -> RDBMSConnectionsDB:
        rdbmsconn = await self.__rdbms_queries.delete_connection_by_id(conn_id)
        if rdbmsconn:
            return rdbmsconn

        return None
