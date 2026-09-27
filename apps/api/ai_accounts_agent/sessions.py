import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4

PENDING = "pending"
VERIFYING = "verifying"
SUCCEEDED = "succeeded"
FAILED = "failed"
CANCELLED = "cancelled"
EXPIRED = "expired"
ACTIVE_STATES = frozenset({PENDING, VERIFYING})
# Finished sessions stay readable long enough for the page to show the outcome.
FINISHED_RETENTION_SECONDS = 600.0


# What a finalizer returns when the CLI never saved a login; the handle then explains
# the failure from what the CLI printed.
NOT_SIGNED_IN = "the CLI did not save a login"

# Called once a CLI reports a finished login. Returns None to accept it, or a safe
# message after undoing a login that must not stand.
Finalizer = Callable[[], str | None]


class LoginError(RuntimeError):
    """A login could not start or continue; the message is already safe to show."""


class LoginHandle(Protocol):
    kind: str
    url: str
    user_code: str | None

    def state(self) -> tuple[str, str | None]: ...

    def submit_code(self, code: str) -> None: ...

    def cancel(self) -> None: ...


@dataclass
class LoginSession:
    tool: str
    slot: str
    handle: LoginHandle
    created_at: float
    expires_at: float
    id: str = field(default_factory=lambda: uuid4().hex)
    final_state: tuple[str, str | None] | None = None
    finished_at: float | None = None

    def current(self, now: float) -> tuple[str, str | None]:
        if self.final_state is not None:
            return self.final_state
        status, error = self.handle.state()
        if status in ACTIVE_STATES and now >= self.expires_at:
            self.handle.cancel()
            status, error = EXPIRED, "the login was not completed in time"
        if status not in ACTIVE_STATES:
            self.final_state = (status, error)
            self.finished_at = now
        return status, error

    def view(self, now: float) -> dict[str, Any]:
        status, error = self.current(now)
        active = status in ACTIVE_STATES
        return {
            "id": self.id,
            "tool": self.tool,
            "slot": self.slot,
            "kind": self.handle.kind,
            "status": status,
            # The URL and code are only useful, and only shown, while the login is open.
            "url": self.handle.url if active else None,
            "user_code": self.handle.user_code if active else None,
            "error": error,
            "expires_at": int(self.expires_at),
        }


class LoginRegistry:
    def __init__(self, ttl_seconds: float, clock: Callable[[], float] = time.time) -> None:
        self._ttl = ttl_seconds
        self._clock = clock
        self._sessions: dict[str, LoginSession] = {}
        self._lock = threading.Lock()

    def now(self) -> float:
        return self._clock()

    def _sweep(self, now: float) -> None:
        for session_id, session in list(self._sessions.items()):
            session.current(now)
            if (
                session.finished_at is not None
                and now - session.finished_at > FINISHED_RETENTION_SECONDS
            ):
                del self._sessions[session_id]

    def active_for(self, tool: str, slot: str) -> LoginSession | None:
        with self._lock:
            now = self._clock()
            self._sweep(now)
            for session in self._sessions.values():
                if (
                    session.tool == tool
                    and session.slot == slot
                    and session.current(now)[0] in ACTIVE_STATES
                ):
                    return session
            return None

    def start(
        self, tool: str, slot: str, factory: Callable[[], LoginHandle]
    ) -> tuple[LoginSession, bool]:
        """Start a login, or return the one already open for this slot.

        The lock is held while the CLI starts so two clicks cannot open two logins for one
        account; starting takes a few seconds at most.
        """
        with self._lock:
            now = self._clock()
            self._sweep(now)
            for session in self._sessions.values():
                if (
                    session.tool == tool
                    and session.slot == slot
                    and session.current(now)[0] in ACTIVE_STATES
                ):
                    return session, False
            handle = factory()
            session = LoginSession(
                tool=tool,
                slot=slot,
                handle=handle,
                created_at=now,
                expires_at=now + self._ttl,
            )
            self._sessions[session.id] = session
            return session, True

    def get(self, session_id: str) -> LoginSession | None:
        with self._lock:
            self._sweep(self._clock())
            return self._sessions.get(session_id)

    def cancel(self, session_id: str) -> LoginSession | None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            now = self._clock()
            if session.current(now)[0] in ACTIVE_STATES:
                session.handle.cancel()
                session.final_state = (CANCELLED, None)
                session.finished_at = now
            return session

    def cancel_slot(self, tool: str, slot: str) -> None:
        with self._lock:
            now = self._clock()
            for session in self._sessions.values():
                if (
                    session.tool == tool
                    and session.slot == slot
                    and session.current(now)[0] in ACTIVE_STATES
                ):
                    session.handle.cancel()
                    session.final_state = (CANCELLED, None)
                    session.finished_at = now

    def close_all(self) -> None:
        with self._lock:
            for session in self._sessions.values():
                if session.final_state is None:
                    session.handle.cancel()
