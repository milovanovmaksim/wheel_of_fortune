from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(schema: Any, data: Any = None) -> Response:
    return Response(
        body=schema().dumps(data),
        headers={'Content-Type': 'application/json', })


def error_json_response(http_status: int, status: str,
                        message: Optional[str] = None,
                        data: Optional[dict] = None):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "code": http_status,
            "status": status,
            "message": message,
            "data": data, })
