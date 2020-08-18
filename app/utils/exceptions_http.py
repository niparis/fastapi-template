from dataclasses import dataclass

from fastapi import Request
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse

from app.utils.exceptions_internal import DuplicateEntityDatabase

# HTTP Exceptions - All these exceptions should return a response with an appropriate HTTP response code (4xx ot 5xx)
# Those exceptions should only be called in the Routes !!

# See https://www.restapitutorial.com/httpstatuscodes.html for docs on HTTP status codes

# Creating a new exception
# 1. Create a class
# 2. Create a handler
# 3. Register the exception and the handler in `register_exception_handlers`


@dataclass
class GenericBadRequest400(Exception):
    error: str
    details: str

    @property
    def content(self):
        return {"error": self.error, "details": self.details}


async def generic_bad_request_handler(
    request: Request, exc: GenericBadRequest400
):
    return ORJSONResponse(status_code=400, content=exc.content,)


@dataclass
class EntityNotFound_404(Exception):
    name: str
    pk_or_id: str


async def not_found_exception_handler(
    request: Request, exc: EntityNotFound_404
):
    return ORJSONResponse(
        status_code=404,
        content={
            "message": f"Entity {exc.name} with id/pd {exc.pk_or_id} could not be found"
        },
    )


@dataclass
class UserInputDuplicate_409(Exception):
    ex: DuplicateEntityDatabase

    @property
    def message(self):
        return f"Warning: {self.ex.entity} already exists {self.ex.name}"


async def user_input_error_exc_handler(
    request: Request, exc: UserInputDuplicate_409
):
    return ORJSONResponse(status_code=409, content={"message": exc.message},)


def register_exception_handlers(app: FastAPI) -> FastAPI:
    """ Registers all the default exception handlers
    """
    app.add_exception_handler(EntityNotFound_404, not_found_exception_handler)
    app.add_exception_handler(
        UserInputDuplicate_409, user_input_error_exc_handler
    )
    app.add_exception_handler(
        GenericBadRequest400, generic_bad_request_handler
    )
    return app
