from typing import Any

from databases import Database
from sqlalchemy.sql.selectable import Select


async def load_query_in_entity(db: Database, query: Select, entity: Any):
    result_proxy = await db.fetch_all(query=query)
    return [
        entity(**dict(zip(row.keys(), row.values()))) for row in result_proxy
    ]
