from uuid import uuid4

import jwt

from app.auth.service import (
    ALGORITHM,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.config import get_settings
from app.problems import AppError
from app.usage.router import decode_cursor, encode_cursor
from app.usage.service import PACKAGE_DEFAULTS, search_operation, search_summary


def test_password_and_jwt_roundtrip() -> None:
    hashed = hash_password("a-strong-demo-password")
    assert verify_password("a-strong-demo-password", hashed)
    user_id = uuid4()
    assert decode_access_token(create_access_token(user_id)) == user_id


def test_access_tokens_require_issuer_audience_and_session_version() -> None:
    token = jwt.encode(
        {"sub": str(uuid4())},
        get_settings().app_secret_key,
        algorithm=ALGORITHM,
    )
    try:
        decode_access_token(token)
    except AppError as exc:
        assert exc.code == "invalid_token"
    else:
        raise AssertionError("legacy token without required claims was accepted")


def test_search_operations_all_use_one_accounting_unit() -> None:
    assert search_operation({"trip_type": "multi_city", "modules": ["flight"]}) == (
        "multi_city_search"
    )
    assert (
        search_operation(
            {
                "trip_type": "round_trip",
                "modules": ["flight", "hotel", "activities", "transport"],
                "preferences": {"optimization_mode": "balanced"},
            }
        )
        == "full_trip_search"
    )
    assert search_operation({"modules": ["flight", "hotel"]}) == "flight_hotel_search"


def test_usage_package_catalog_and_safe_summary() -> None:
    assert {code: (item["uses"], item["price_twd"]) for code, item in PACKAGE_DEFAULTS.items()} == {
        "TRIAL_3": (3, 0),
        "PACK_10": (10, 199),
        "PACK_30": (30, 499),
        "PACK_100": (100, 1299),
    }
    summary = search_summary(
        {
            "origin": "TPE",
            "destination": "NRT",
            "departure_date": "2026-11-10",
            "return_date": "2026-11-15",
            "travelers": {"adults": 2},
            "preferences": {"interests": ["food"]},
        }
    )
    assert summary == "旅程查詢 TPE → NRT · 2026-11-10–2026-11-15"
    assert "adults" not in summary


def test_usage_history_cursor_roundtrip_and_validation() -> None:
    from datetime import UTC, datetime

    ledger_id = uuid4()
    occurred_at = datetime(2026, 8, 31, 12, 30, tzinfo=UTC)
    assert decode_cursor(encode_cursor(occurred_at, ledger_id)) == (occurred_at, ledger_id)
    for invalid in ("not-base64!", "MjAyNi0wOC0zMVQxMjozMDowMHxub3QtYS11dWlk"):
        try:
            decode_cursor(invalid)
        except AppError as exc:
            assert exc.code == "invalid_usage_cursor"
        else:
            raise AssertionError("invalid usage cursor was accepted")
