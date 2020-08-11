from fastapi import Request
from fastapi.responses import ORJSONResponse

from app.utils.exceptions import EntityNotFound


async def not_found_exception_handler(request: Request, exc: EntityNotFound):
    return ORJSONResponse(
        status_code=404,
        content={"message": f"Entity {exc.name} could not be found"},
    )
