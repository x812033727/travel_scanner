from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    payload: dict[str, Any] = {
        "type": f"https://travel-scanner.local/problems/{exc.code}",
        "title": exc.code.replace("_", " ").title(),
        "status": exc.status,
        "code": exc.code,
        "detail": exc.detail,
        "request_id": getattr(request.state, "request_id", None),
    }
    return JSONResponse(payload, status_code=exc.status, media_type="application/problem+json")
