"""What the request knows about the visitor, for events the server sends itself.

Server-side events are recorded from wherever the action actually happens — a router,
but also ``usage.service`` deep under one — and threading a ``Request`` through every
one of those signatures to reach four header values is not worth it. So the values are
bound once by ``RequestContextMiddleware`` and read from a context variable, the same
shape ``app.i18n`` already uses for the request locale.

The one that matters is ``session_id``. The funnel counts distinct sessions per step,
so a server event that invented its own identity would not be comparable with the
browser events on either side of it: the same person would look like two. The browser
sends its analytics session id on every API call it makes (``lib/api.ts``), the BFF
forwards it, and ``record_event`` hashes it exactly the way visitor ingest does, so
both halves of a funnel land under one hash.
"""

from __future__ import annotations

import re
from contextvars import ContextVar, Token
from dataclasses import dataclass

from starlette.datastructures import Headers

_HEX = "[0-9a-fA-F]"
_UUID = re.compile(rf"\A{_HEX}{{8}}-{_HEX}{{4}}-{_HEX}{{4}}-{_HEX}{{4}}-{_HEX}{{12}}\Z")


@dataclass(frozen=True, slots=True)
class AnalyticsContext:
    """The visitor-identifying parts of a request, or empty outside one."""

    session_id: str | None = None
    client_ip: str | None = None
    user_agent: str | None = None
    country_code: str | None = None
    #: Set by Sec-GPC or DNT. Honoured for server events too: a visitor who asked not
    #: to be measured did not mean "except when the measuring happens server-side".
    opted_out: bool = False


EMPTY = AnalyticsContext()

_analytics_context: ContextVar[AnalyticsContext] = ContextVar("analytics_context", default=EMPTY)


def context_from_headers(headers: Headers, *, client_ip: str | None) -> AnalyticsContext:
    session_id = headers.get("X-Travel-Analytics-Session", "").strip()
    country = headers.get("X-Travel-Country", "").strip().upper()
    return AnalyticsContext(
        session_id=session_id if _UUID.match(session_id) else None,
        client_ip=client_ip,
        user_agent=(headers.get("X-Travel-User-Agent") or "")[:512] or None,
        country_code=country
        if re.fullmatch(r"[A-Z]{2}", country) and country not in {"XX", "T1"}
        else None,
        opted_out=headers.get("Sec-GPC") == "1" or headers.get("DNT") == "1",
    )


def analytics_context() -> AnalyticsContext:
    return _analytics_context.get()


def bind_analytics_context(value: AnalyticsContext) -> Token[AnalyticsContext]:
    return _analytics_context.set(value)


def reset_analytics_context(token: Token[AnalyticsContext]) -> None:
    _analytics_context.reset(token)
