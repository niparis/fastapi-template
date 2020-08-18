from dataclasses import dataclass

from databases.core import Database

# Internal exceptions: raise by the infrastructure or service layers.
# The router will decide what HTTP status code to return
# The goal of this separation is to have full visibility on which codes can be returned
# just by looking at the code of the router


@dataclass
class DuplicateEntityDatabase(Exception):
    entity: str
    name: str


@dataclass
class ConnectionToHostFailed(Exception):
    host_name: str


@dataclass
class DatabaseError(Exception):
    """ A generic database error. 
        Goal is to make logs easier to parse (the low level exceptions are overly verbose)
    """

    message: str


@dataclass
class UnhandledException(Exception):
    """ A generic exception, for any case where we explicitly choose to send a 500 without explanation 
    """

    message: str
