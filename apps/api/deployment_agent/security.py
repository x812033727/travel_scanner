import hashlib
import hmac
import re
import time

from deployment_agent.store import AgentStore

SECRET_PATTERNS = (
    re.compile(r"(?i)(password|token|secret|api[_-]?key)\s*[=:]\s*[^\s,;]+"),
    re.compile(r"(?i)authorization:\s*[^\s]+(?:\s+[^\s]+)?"),
)
URL_CREDENTIALS = re.compile(r"(://[^:/\s]+:)[^@\s]+(@)")


def sanitize(value: str, limit: int = 500) -> str:
    cleaned = value.replace("\x00", " ")
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub(
            lambda match: f"{match.group(1) if match.lastindex else 'secret'}=***", cleaned
        )
    cleaned = URL_CREDENTIALS.sub(r"\1***\2", cleaned)
    return " ".join(cleaned.split())[:limit]


def verify_request(
    store: AgentStore,
    key: str,
    method: str,
    path: str,
    body: bytes,
    timestamp: str | None,
    nonce: str | None,
    signature: str | None,
) -> bool:
    if not timestamp or not nonce or not signature or not re.fullmatch(r"[0-9a-f]{32}", nonce):
        return False
    try:
        instant = int(timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - instant) > 60:
        return False
    digest = hashlib.sha256(body).hexdigest()
    message = f"{timestamp}\n{nonce}\n{method.upper()}\n{path}\n{digest}".encode()
    expected = hmac.new(key.encode(), message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return False
    return store.consume_nonce(nonce, instant)
