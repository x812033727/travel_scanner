"""Small, allowlisted diagnostics; never persist provider bodies, URLs or exception text."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

ERROR_CODES = frozenset(
    {
        "catalog_response_truncated",
        "catalog_response_blocked",
        "catalog_response_empty",
        "catalog_response_invalid",
        "catalog_response_ids_invalid",
        "catalog_provider_rate_limited",
        "catalog_provider_timeout",
        "catalog_provider_unavailable",
    }
)
_FINISH_REASONS = frozenset(
    {
        "STOP",
        "MAX_TOKENS",
        "SAFETY",
        "RECITATION",
        "BLOCKLIST",
        "PROHIBITED_CONTENT",
        "SPII",
        "IMAGE_SAFETY",
        "OTHER",
        "MALFORMED_FUNCTION_CALL",
        "UNEXPECTED_TOOL_CALL",
        "FINISH_REASON_UNSPECIFIED",
        "UNKNOWN",
    }
)
_NUMERIC_DETAILS = frozenset(
    {
        "http_status",
        "attempt",
        "candidate_count",
        "max_output_tokens",
        "input_chars",
        "input_tokens",
        "output_tokens",
        "thought_tokens",
        "validation_error_count",
    }
)
_VALIDATION_FIELDS = frozenset(
    {
        "items",
        "candidate_id",
        "decision",
        "confidence",
        "reason",
        "evidence",
        "url",
        "quote",
        "corrections",
        "kind",
        "name",
        "local_name",
        "destination_id",
        "slug",
        "source_urls",
        "data",
        "localizations",
        "locale",
        "summary",
        "unknown_field",
    }
)
_VALIDATION_TYPES = frozenset(
    {
        "json_invalid",
        "missing",
        "extra_forbidden",
        "string_type",
        "string_too_short",
        "string_too_long",
        "string_pattern_mismatch",
        "literal_error",
        "float_type",
        "float_parsing",
        "finite_number",
        "greater_than_equal",
        "less_than_equal",
        "too_long",
        "too_short",
        "list_type",
        "dict_type",
        "model_type",
        "value_error",
        "unknown",
    }
)


def _safe_path(value: Any) -> str:
    if not isinstance(value, (list, tuple)):
        return "unknown_field"
    return (
        ".".join(
            str(part)
            if isinstance(part, int) and not isinstance(part, bool) and 0 <= part <= 100
            else part
            if isinstance(part, str) and part in _VALIDATION_FIELDS
            else "unknown_field"
            for part in value[:8]
        )
        or "items"
    )


def validation_details(error: ValidationError) -> dict[str, Any]:
    entries = error.errors(include_input=False, include_context=False, include_url=False)
    first: dict[str, Any] = dict(entries[0]) if entries else {}
    raw_type = first.get("type")
    return {
        "validation_error_count": len(entries),
        "validation_path": _safe_path(first.get("loc")),
        "validation_type": raw_type if raw_type in _VALIDATION_TYPES else "unknown",
    }


def _safe_details(details: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in details.items():
        if key in _NUMERIC_DETAILS and isinstance(value, int) and not isinstance(value, bool):
            if 0 <= value <= 1_000_000_000:
                result[key] = value
        elif key == "finish_reason":
            result[key] = (
                value if isinstance(value, str) and value in _FINISH_REASONS else "UNKNOWN"
            )
        elif key == "validation_type":
            result[key] = (
                value if isinstance(value, str) and value in _VALIDATION_TYPES else "unknown"
            )
        elif key == "validation_path" and isinstance(value, str):
            result[key] = _safe_path(
                [
                    int(part) if part.isascii() and part.isdigit() and len(part) <= 3 else part
                    for part in value.split(".")[:8]
                ]
            )
    return result


class CatalogAssessmentError(Exception):
    """Only provider failures use this type; lease/budget/database errors remain distinct."""

    def __init__(
        self,
        code: str,
        *,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code if code in ERROR_CODES else "catalog_response_invalid"
        self.retryable = retryable
        self.details = _safe_details(details or {})
        super().__init__(self.code)


def safe_error_diagnostics(error: Exception) -> dict[str, Any]:
    if isinstance(error, CatalogAssessmentError):
        return {
            "error": "CatalogAssessmentError",
            "code": error.code,
            "retryable": error.retryable,
            "details": _safe_details(error.details),
        }
    # Legacy errors cannot establish a cause; do not turn ValueError into a guessed
    # truncation diagnosis or persist its potentially sensitive message/type name.
    return {
        "error": "Exception",
        "code": None,
        "retryable": False,
        "details": {},
    }
