from datetime import UTC, date, datetime
from uuid import uuid4

from app.analytics.schemas import AnalyticsEventBatch
from app.analytics.service import (
    _client_details,
    _digest,
    _referrer,
    _rollup_funnel,
    _rollup_summary,
    normalize_path,
)
from app.models import AnalyticsDailyRollup


def test_normalize_path_removes_locale_queries_and_dynamic_ids() -> None:
    assert (
        normalize_path(
            "https://mocair.io/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000?email=a%40b.com#secret"
        )
        == "/trips/:id"
    )
    assert normalize_path("/en/share/abcdefghijklmnopqrstuvwxyz1234?token=secret") == "/share/:id"
    assert normalize_path("/ja/admin/users") is None
    assert normalize_path("/api/v1/auth/me") is None


def test_daily_hashes_rotate_without_exposing_source_values() -> None:
    first = _digest("a-secret-long-enough", "analytics-day", "2026-09-01|203.0.113.1|UA")
    second = _digest("a-secret-long-enough", "analytics-day", "2026-09-02|203.0.113.1|UA")
    assert first != second
    assert "203.0.113.1" not in first
    assert len(first) == 64


def test_user_agent_and_referrer_are_reduced_to_categories() -> None:
    device, browser, os_name, bot = _client_details("Mozilla/5.0 (iPhone) AppleWebKit Safari/605.1")
    assert (device, browser, os_name, bot) == ("mobile", "safari", "ios", False)
    assert _client_details("ExampleBot/1.0")[3] is True
    assert _referrer("https://www.google.com/search?q=private", "https://mocair.io") == (
        "search",
        "www.google.com",
    )
    assert _referrer("https://mocair.io/zh-TW/search?private=yes", "https://mocair.io") == (
        "internal",
        None,
    )


def test_event_schema_rejects_unknown_properties() -> None:
    try:
        AnalyticsEventBatch.model_validate(
            {
                "session_id": str(uuid4()),
                "events": [
                    {
                        "event_id": str(uuid4()),
                        "name": "page_view",
                        "occurred_at": datetime.now(UTC).isoformat(),
                        "path": "/zh-TW/",
                        "locale": "zh-TW",
                        "email": "must-not-be-accepted@example.com",
                    }
                ],
            }
        )
    except ValueError:
        pass
    else:
        raise AssertionError("unknown analytics attributes must be rejected")


def test_rollup_summary_and_funnel_use_aggregate_session_scope() -> None:
    rows = [
        AnalyticsDailyRollup(
            day=date(2026, 9, 1),
            environment="production",
            is_bot=False,
            metric="event_count",
            dimension="event",
            dimension_value="page_view",
            value=12,
        ),
        AnalyticsDailyRollup(
            day=date(2026, 9, 1),
            environment="production",
            is_bot=False,
            metric="unique_sessions",
            dimension="all",
            dimension_value="all",
            value=4,
        ),
        AnalyticsDailyRollup(
            day=date(2026, 9, 1),
            environment="production",
            is_bot=False,
            metric="daily_visitors",
            dimension="all",
            dimension_value="all",
            value=3,
        ),
        AnalyticsDailyRollup(
            day=date(2026, 9, 1),
            environment="production",
            is_bot=False,
            metric="funnel_sessions",
            dimension="step",
            dimension_value="search_completed",
            value=2,
        ),
    ]
    assert _rollup_summary(rows)["pages_per_session"] == 3
    assert _rollup_funnel(rows)[1] == {
        "step": "search_completed",
        "sessions": 2,
        "conversion_rate": 50.0,
    }
