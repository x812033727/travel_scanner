import logging
import re
import time
from uuid import uuid4

from fastapi import Request
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.analytics.context import (
    bind_analytics_context,
    context_from_headers,
    reset_analytics_context,
)
from app.config import get_settings
from app.i18n import bind_request_locale, request_locale, reset_request_locale
from app.infra import client_ip, forwarded_client_ip, over_named_rate_limit, record_rate_limit_hit
from app.problems import AppError, app_error_handler

logger = logging.getLogger(__name__)

_HOUR_SECONDS = 3_600


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
        # The downstream app runs in a task spawned from this context, so the
        # locale bound here is visible to every handler and serializer. The visitor
        # identity travels the same way, so an event recorded deep under a handler
        # lands on the same session hash as the browser events around it.
        locale_token = bind_request_locale(request_locale(request.headers))
        analytics_token = bind_analytics_context(
            context_from_headers(request.headers, client_ip=client_ip(request))
        )
        try:
            response = await call_next(request)
        finally:
            reset_analytics_context(analytics_token)
            reset_request_locale(locale_token)
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


class PublicReadRateLimitMiddleware:
    """Bound how fast a single source can read the public catalogue.

    Only requests carrying a forwarded client address are counted, and that is the
    load-bearing part. Server rendering calls this API directly rather than through
    the BFF, so those requests arrive without one; counting them would file every
    visitor's page render under the web container's own address and take the whole
    site down the first time anyone browsed quickly. No forwarded address therefore
    means first-party traffic, which is not what this guards against.

    Both windows are counted even when one has already been spent, so the hourly
    figure stays honest about what a source actually asked for, and so ``observe``
    mode produces the numbers the thresholds will later be argued from.
    """

    _NAMESPACE = "public-read-ip"

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        address = self._counted_address(scope)
        if address is None:
            await self.app(scope, receive, send)
            return
        settings = get_settings()
        burst = await over_named_rate_limit(
            f"{self._NAMESPACE}-minute",
            address,
            limit=settings.public_read_ip_limit,
            window_seconds=settings.public_read_ip_window_seconds,
        )
        # Charged even when the burst window is already spent. Stopping here would
        # under-report precisely the sustained crawl the hourly window exists to catch.
        sustained = await over_named_rate_limit(
            f"{self._NAMESPACE}-hour",
            address,
            limit=settings.public_read_ip_hour_limit,
            window_seconds=_HOUR_SECONDS,
        )
        if not (burst or sustained):
            await self.app(scope, receive, send)
            return
        await record_rate_limit_hit(self._NAMESPACE, address)
        logger.warning(
            "public read limit reached on %s (window=%s, enforcing=%s)",
            scope.get("path", ""),
            "hour" if sustained else "minute",
            settings.public_read_rate_limit_mode == "enforce",
        )
        if settings.public_read_rate_limit_mode != "enforce":
            await self.app(scope, receive, send)
            return
        # Name the window that is actually spent: retrying at the end of the burst window
        # when the hour is gone just earns a second refusal.
        await self._reject(
            scope,
            receive,
            send,
            retry_after=(
                _HOUR_SECONDS if sustained else settings.public_read_ip_window_seconds
            ),
        )

    def _counted_address(self, scope: Scope) -> str | None:
        """The source to charge for this request, or ``None`` to leave it alone."""
        if scope["type"] != "http":
            return None
        if get_settings().public_read_rate_limit_mode == "off":
            return None
        # Reads only. Writes are already answered by the per-user limits and the usage
        # ledger, and they are not how a catalogue gets copied.
        if scope.get("method") not in {"GET", "HEAD"}:
            return None
        if not str(scope.get("path", "")).startswith("/api/v1"):
            return None
        return forwarded_client_ip(Headers(scope=scope))

    @staticmethod
    async def _reject(
        scope: Scope, receive: Receive, send: Send, *, retry_after: int
    ) -> None:
        error = AppError(
            429,
            "rate_limit_exceeded",
            "請求過於頻繁，請稍後再試",
            headers={"Retry-After": str(retry_after)},
        )
        response = await app_error_handler(Request(scope, receive), error)
        await response(scope, receive, send)
