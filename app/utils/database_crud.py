import logging
from typing import Any, Union

import pydantic
from databases import Database
from sqlalchemy.sql import Delete, Update
from sqlalchemy.sql.selectable import Select

from app.utils.exceptions_internal import DatabaseError

logger = logging.getLogger(__name__)


async def load_query_in_entity(db: Database, query: Select, entity: Any):
    """ 
        Runs a select query
            and attempts to load the results in a provided class 

            entity: Class to load the data into. attributes must match the column names
    """
    result_proxy = await db.fetch_all(query=query)
    try:
        return [
            entity(**dict(zip(row.keys(), row.values())))
            for row in result_proxy
        ]
    except pydantic.error_wrappers.ValidationError:
        logger.exception(
            f"mismatch between schema class {entity} and query {query}"
        )
        raise DatabaseError(
            f"Schema class {entity} needs to be fixed to represent its underlying table"
        )


async def run_update_delete_returning_row_count(
    db: Database, query: Union[Update, Delete]
) -> int:
    """
            Runs a update / delete query, and returns the number of rows affected

            Workaround needed, implementation coming from: https://github.com/encode/databases/issues/161
        """
    raw_sql = str(query.compile(compile_kwargs={"literal_binds": True}))

    async with db.connection() as connection:
        raw_connection = connection.raw_connection
        status = await raw_connection.execute(raw_sql)

    return int(status.split(" ")[1])
