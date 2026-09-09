import re

SENSITIVE_AUDIT_KEY_PARTS = (
    "password",
    "token",
    "secret",
    "hmac",
    "api_key",
    "api-key",
    "api key",
    "apikey",
)
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passphrase|token|secret|hmac|api[-_ ]?key)\b"
    r"\s*[:=]\s*(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
)
AUTHORIZATION_VALUE = re.compile(
    r"(?i)\bauthorization\s*:\s*(?:bearer\s+)?[A-Za-z0-9._~+/=-]+"
)
BEARER_VALUE = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+")
URL_CREDENTIALS = re.compile(r"(://[^:/\s]+:)[^@\s]+(@)")
JWT_VALUE = re.compile(
    r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9_-]{10,}\.){2}[A-Za-z0-9_-]{10,}"
    r"(?![A-Za-z0-9_-])"
)


def _safe_audit_string(value: str) -> str:
    cleaned = value.replace("\x00", " ")
    cleaned = AUTHORIZATION_VALUE.sub("Authorization: ***", cleaned)
    cleaned = BEARER_VALUE.sub("Bearer ***", cleaned)
    cleaned = URL_CREDENTIALS.sub(r"\1***\2", cleaned)
    cleaned = SENSITIVE_ASSIGNMENT.sub(lambda match: f"{match.group(1)}=***", cleaned)
    cleaned = JWT_VALUE.sub("***", cleaned)
    return cleaned[:1000]


def safe_audit_metadata(value: object) -> object:
    """Redact and bound legacy audit payloads before they reach an operator browser."""
    if isinstance(value, dict):
        cleaned: dict[str, object] = {}
        for raw_key, child in value.items():
            key = str(raw_key)
            if any(part in key.lower() for part in SENSITIVE_AUDIT_KEY_PARTS):
                continue
            cleaned[key] = safe_audit_metadata(child)
        return cleaned
    if isinstance(value, list):
        return [safe_audit_metadata(child) for child in value[:100]]
    if isinstance(value, str):
        return _safe_audit_string(value)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return str(value)[:1000]
