import re
import time
from uuid import uuid4

from fastapi import Request
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.problems import AppError, app_error_handler


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        supplied_request_id = request.headers.get("X-Request-ID", "")
        request_id = (
            supplied_request_id
            if re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", supplied_request_id)
            else str(uuid4())
        )
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = f"{(time.perf_counter() - started) * 1000:.1f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        if (
            request.url.path.startswith("/api/v1/auth")
            or request.headers.get("authorization")
            or request.cookies.get("travel_access")
        ):
            response.headers["Cache-Control"] = "no-store"
        return response


class RequestBodyLimitMiddleware:
    """Reject request bodies above ``max_bytes`` before the application buffers them.

    A declared ``Content-Length`` is checked up front; bodies without one (chunked uploads)
    are counted as they stream and cut off with the same 413 problem response.
    """

    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        declared = Headers(scope=scope).get("content-length")
        if declared is not None:
            try:
                length = int(declared)
            except ValueError:
                length = -1
            if length < 0:
                await self._reject(scope, receive, send, 400, "invalid_content_length")
                return
            if length > self.max_bytes:
                await self._reject(scope, receive, send, 413, "request_too_large")
                return
        received = 0

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    raise AppError(413, "request_too_large", "請求內容超過允許大小")
            return message

        await self.app(scope, limited_receive, send)

    @staticmethod
    async def _reject(scope: Scope, receive: Receive, send: Send, status: int, code: str) -> None:
        detail = "請求內容超過允許大小" if status == 413 else "Content-Length 標頭無效"
        response = await app_error_handler(Request(scope, receive), AppError(status, code, detail))
        await response(scope, receive, send)
