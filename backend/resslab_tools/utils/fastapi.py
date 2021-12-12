from enum import Enum

from fastapi import FastAPI
from fastapi.routing import APIRoute


class MediaType(Enum):
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    """
    CSV = 'text/csv'


class HttpHeader(Enum):
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
    """
    CONTENT_DISPOSITION = 'Content-Disposition'


def attachment(filename: str) -> str:
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    """
    return f'attachment; filename="{filename}"'


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.
    Should be called only after all routes have been added.
    https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#openapi-operationid
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
