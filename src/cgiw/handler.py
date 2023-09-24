from typing import Optional, Any
from traceback import format_exc

from .types import QueryType, HeadersType, GetHandlerType, PostHandlerType, ReturnType
from .exceptions import ApiException
from .logger import log


def handle(
    method: str,
    query: QueryType,
    headers: HeadersType,
    body: Optional[Any] = None,
    get: Optional[GetHandlerType] = None,
    post: Optional[PostHandlerType] = None,
) -> ReturnType:
    try:
        if method == "POST" and post:
            return post(query, headers, body)
        elif method == "GET" and get:
            return get(query, headers)
    except ApiException as e:
        raise e
    except Exception as e:
        log(format_exc())
        raise ApiException(
            500, "Internal Service Error", message="An Unknown Error Has Occurred"
        )

    return ({"Status": "405 Method Not Allowed"}, "")
