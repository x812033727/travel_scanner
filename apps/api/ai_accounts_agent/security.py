import hashlib
import hmac
import re
import threading
import time

TIMESTAMP_HEADER = "X-Agent-Timestamp"
NONCE_HEADER = "X-Agent-Nonce"
SIGNATURE_HEADER = "X-Agent-Signature"
MAX_CLOCK_SKEW_SECONDS = 60

_NAMED_SECRETS = re.compile(
    r"(?i)\b(password|token|secret|api[_-]?key|access_token|refresh_token|id_token)"
    r"\s*[=:]\s*[^\s,;&]+"
)
# OAuth query parameters. Only the `=` form, so "exit code: 1" survives.
_OAUTH_PARAMETERS = re.compile(r"(?i)\b(code|state|code_challenge|code_verifier)=[^\s&]+")
_UNNAMED_SECRETS = (
    re.compile(r"(?i)authorization:\s*[^\s]+(?:\s+[^\s]+)?"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    # Google: access tokens, refresh tokens and the authorization codes agy takes.
    re.compile(r"\bya29\.[A-Za-z0-9._-]+"),
    re.compile(r"\b1//[A-Za-z0-9._-]{10,}"),
    re.compile(r"\b4/[0-9A-Za-z][A-Za-z0-9._-]{10,}"),
)
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def sanitize(value: str, limit: int = 300) -> str:
    """Make CLI output safe to hand to the API: no tokens, codes or terminal escapes."""
    cleaned = _CONTROL.sub(" ", value)
    cleaned = _NAMED_SECRETS.sub(lambda match: f"{match.group(1)}=***", cleaned)
    cleaned = _OAUTH_PARAMETERS.sub(lambda match: f"{match.group(1)}=***", cleaned)
    for pattern in _UNNAMED_SECRETS:
        cleaned = pattern.sub("***", cleaned)
    return " ".join(cleaned.split())[:limit]


def redact_emails(value: str) -> str:
    """Replace anything shaped like an email address, domain included."""
    return _EMAIL.sub("<email>", value)


def signature_for(
    key: str, timestamp: str, nonce: str, method: str, path: str, body: bytes
) -> str:
    digest = hashlib.sha256(body).hexdigest()
    message = f"{timestamp}\n{nonce}\n{method.upper()}\n{path}\n{digest}".encode()
    return hmac.new(key.encode(), message, hashlib.sha256).hexdigest()


class NonceCache:
    """Remembers nonces for twice the allowed clock skew so a request cannot be replayed."""

    def __init__(self, ttl_seconds: float = 2 * MAX_CLOCK_SKEW_SECONDS) -> None:
        self._ttl = ttl_seconds
        self._seen: dict[str, float] = {}
        self._lock = threading.Lock()

    def consume(self, nonce: str, now: float) -> bool:
        with self._lock:
            for stale in [key for key, expires in self._seen.items() if expires <= now]:
                del self._seen[stale]
            if nonce in self._seen:
                return False
            self._seen[nonce] = now + self._ttl
            return True


def verify_request(
    nonces: NonceCache,
    key: str,
    method: str,
    path: str,
    body: bytes,
    timestamp: str | None,
    nonce: str | None,
    signature: str | None,
    now: float | None = None,
) -> bool:
    if (
        not timestamp
        or not nonce
        or not signature
        or not re.fullmatch(r"[0-9a-f]{32}", nonce)
        or not re.fullmatch(r"[0-9a-f]{64}", signature)
    ):
        return False
    try:
        instant = int(timestamp)
    except ValueError:
        return False
    current = time.time() if now is None else now
    if abs(current - instant) > MAX_CLOCK_SKEW_SECONDS:
        return False
    expected = signature_for(key, timestamp, nonce, method, path, body)
    if not hmac.compare_digest(expected, signature):
        return False
    return nonces.consume(nonce, current)
