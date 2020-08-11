from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.orm import Session
from starlette import status

from app.api.servicesfac import get_rdbms_connections_service
from app.domain.rdbms_connections.rdbms_connections_schema import (
    RDBMSConnectionsCreateSchema,
    RDBMSConnectionsDB,
    RDBMSConnectionsDelete,
)
from app.domain.rdbms_connections.rdbms_connections_service import (
    RDBMSConnectionsService,
)
from app.utils.exceptions import EntityNotFound

router = APIRouter()


@router.post(
    "/", response_model=RDBMSConnectionsDB, response_class=ORJSONResponse
)
async def create_rdbmsconn(
    rdbmsconn: RDBMSConnectionsCreateSchema,
    rdbms_service: RDBMSConnectionsService = Depends(
        get_rdbms_connections_service
    ),
) -> RDBMSConnectionsDB:
    print("calling service")
    return await rdbms_service.create_rdbmsconn(rdbmsconn)


@router.get(
    "/{conn_id}",
    response_model=RDBMSConnectionsDB,
    response_class=JSONResponse,
    summary="Gets an RDBMS connection",
    response_description="The connections information (without password)",
)
async def get_rdbmsconn(
    conn_id: int = Path(..., title="The ID of the connection to get", ge=1),
    rdbms_service: RDBMSConnectionsService = Depends(
        get_rdbms_connections_service
    ),
) -> RDBMSConnectionsDB:
    rdbms_conn = await rdbms_service.get_rdbmsconn_by_id(conn_id)
    if rdbms_conn:
        return rdbms_conn
    else:
        raise EntityNotFound(name=conn_id)


@router.delete(
    "/{conn_id}",
    response_model=RDBMSConnectionsDelete,
    response_class=ORJSONResponse,
)
async def delete_rdbmsconn(
    conn_id: int,
    rdbms_service: RDBMSConnectionsService = Depends(
        get_rdbms_connections_service
    ),
) -> RDBMSConnectionsDB:
    _ = await rdbms_service.delete_rdbmsconn_by_id(conn_id)
    return RDBMSConnectionsDelete(success=True)
