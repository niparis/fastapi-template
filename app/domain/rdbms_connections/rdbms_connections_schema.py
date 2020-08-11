from enum import Enum
from typing import Optional

import orjson
from pydantic import BaseModel, validator


class RdbmsRole(str, Enum):
    source = "SOURCE"
    sink = "SINK"


# Shared properties
class RDBMSConnections(BaseModel):
    client_id: Optional[int] = None
    engine: str
    rdbms_role: RdbmsRole
    host: str
    username: str
    password: str
    port: int


class RDBMSConnectionsCreateSchema(RDBMSConnections):
    class Config:
        schema_extra = {
            "example": {
                "client_id": 0,
                "engine": "postgres",
                "rdbms_role": "SINK",
                "host": "200.197.56.12",
                "username": "read-only",
                "password": "password",
                "port": 5432,
            }
        }


class RDBMSConnectionsUpdateSchema(RDBMSConnections):
    pass


# Response


class RDBMSConnectionsDelete(BaseModel):
    success: bool


class RDBMSConnectionsDB(RDBMSConnections):
    connection_id: int
    connection_schema: Optional[dict] = None

    class Config:
        orm_mode = True

    @validator("connection_schema", pre=True)
    def convert_to_json(cls, v):
        if type(v) is dict:
            return v
        return orjson.loads(v)
