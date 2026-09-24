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
from app.config import Settings
from app.models import AnalyticsDailyRollup


def test_normalize_path_removes_locale_queries_and_dynamic_ids() -> None:
    assert (
        normalize_path(
            "https://mokaair.com/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000?email=a%40b.com#secret"
        )
        == "/trips/:id"
    )
    assert normalize_path("/en/share/abcdefghijklmnopqrstuvwxyz1234?token=secret") == "/share/:id"
    assert normalize_path("/ja/admin/users") is None
    assert normalize_path("/api/v1/auth/me") is None


def test_normalize_path_keeps_the_slug_of_a_published_article_url() -> None:
    # Long enough for the token rule, which used to fold every such article into one row.
    assert (
        normalize_path("/zh-TW/life/claude-code-first-project-setup?utm_source=x")
        == "/life/claude-code-first-project-setup"
    )
    assert normalize_path("/en/guides/howto/tokyo-where-to-stay-first-trip/") == (
        "/guides/howto/tokyo-where-to-stay-first-trip"
    )
    assert normalize_path("/ja/guides/intel/japan-rail-pass-price-change-2026") == (
        "/guides/intel/japan-rail-pass-price-change-2026"
    )
    # No 48-character cut: two slugs that share their first 48 characters stay apart.
    slug = "a" * 48 + "-first-half"
    assert normalize_path(f"/ko/life/{slug}") == f"/life/{slug}"


def test_normalize_path_still_folds_tokens_outside_the_article_shapes() -> None:
    # A share URL is a secret, whatever it looks like.
    assert normalize_path("/zh-TW/share/claude-code-first-project-setup") == "/share/:id"
    # Not a slug: capitals and underscores are what a token looks like.
    assert normalize_path("/zh-TW/life/AbCdEfGhIjKlMnOpQrStUv_") == "/life/:id"
    # Not an article shape: an unknown kind, or anything below the slug.
    assert normalize_path("/zh-TW/guides/news/claude-code-first-project-setup") == (
        "/guides/news/:id"
    )
    assert normalize_path("/zh-TW/life/claude-code-first-project-setup/extra") == (
        "/life/:id/extra"
    )
    trip = "/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000/share"
    assert normalize_path(trip) == "/trips/:id/share"


def test_daily_hashes_rotate_without_exposing_source_values() -> None:
    key = b"a-secret-long-enough"
    first = _digest(key, "analytics-day", "2026-09-01|203.0.113.1|UA")
    second = _digest(key, "analytics-day", "2026-09-02|203.0.113.1|UA")
    assert first != second
    assert "203.0.113.1" not in first
    assert len(first) == 64


def test_rotating_the_signing_key_leaves_analytics_identities_intact() -> None:
    """The property this key derivation exists to create.

    ``app_secret_key`` signs every access token, so it has to be rotatable at short notice.
    While analytics hashed with it directly, rotating it also re-keyed every visitor and
    session hash: returning visitors read as new, sessions split at the boundary, and the
    dashboard said nothing about why. Paying for an emergency rotation in corrupted analytics
    is how the rotation gets put off, which is the actual security cost.
    """
    shared = "settings-encryption-key-at-least-32-chars"
    visitor = "2026-09-14|203.0.113.1|UA"
    before = Settings(
        app_secret_key="signing-key-one-that-is-long-enough-x",
        settings_encryption_key=shared,
    )
    after = Settings(
        app_secret_key="signing-key-two-entirely-different-yy",
        settings_encryption_key=shared,
    )
    assert before.app_secret_key != after.app_secret_key
    assert before.analytics_hash_key == after.analytics_hash_key
    assert _digest(before.analytics_hash_key, "analytics-day", visitor) == _digest(
        after.analytics_hash_key, "analytics-day", visitor
    )


def test_analytics_key_is_derived_rather_than_reused_and_moves_with_its_own_secret() -> None:
    signing = "signing-key-one-that-is-long-enough-x"
    settings = Settings(
        app_secret_key=signing,
        settings_encryption_key="settings-encryption-key-at-least-32-chars",
    )
    # Neither secret is usable as the analytics key, so reading the analytics table does not
    # hand anyone something that signs tokens or decrypts stored provider credentials.
    assert settings.analytics_hash_key not in (
        settings.app_secret_key.encode(),
        (settings.settings_encryption_key or "").encode(),
    )
    assert len(settings.analytics_hash_key) == 32
    # Re-keying is still possible, it just takes re-keying the secret it is derived from.
    rotated = Settings(
        app_secret_key=settings.app_secret_key,
        settings_encryption_key="a-different-settings-encryption-key-32ch",
    )
    assert rotated.analytics_hash_key != settings.analytics_hash_key
    # Outside production `settings_encryption_key` is optional, and then there is one secret
    # and no continuity worth protecting; production forbids that case in
    # `validate_deployment_security`.
    assert (
        Settings(app_secret_key=signing, settings_encryption_key=None).analytics_hash_key
        == Settings(app_secret_key=signing, settings_encryption_key=signing).analytics_hash_key
    )


def test_user_agent_and_referrer_are_reduced_to_categories() -> None:
    device, browser, os_name, bot = _client_details("Mozilla/5.0 (iPhone) AppleWebKit Safari/605.1")
    assert (device, browser, os_name, bot) == ("mobile", "safari", "ios", False)
    assert _client_details("ExampleBot/1.0")[3] is True
    assert _referrer("https://www.google.com/search?q=private", "https://mokaair.com") == (
        "search",
        "www.google.com",
    )
    assert _referrer("https://mokaair.com/zh-TW/search?private=yes", "https://mokaair.com") == (
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
            dimension_value="discover_requested",
            value=2,
        ),
    ]
    assert _rollup_summary(rows)["pages_per_session"] == 3
    funnel = _rollup_funnel(rows)
    # The order is the product's claim about what leads to what, so it is pinned here
    # rather than left to whatever the rollup happened to write.
    assert [step["step"] for step in funnel] == [
        "sessions",
        "discover_requested",
        "trip_created",
        "offer_attached",
        "outbound_click",
    ]
    assert funnel[1] == {
        "step": "discover_requested",
        "sessions": 2,
        "conversion_rate": 50.0,
    }
    # A step the rollup has no row for is zero, not missing: the dashboard draws bars.
    assert funnel[3] == {"step": "offer_attached", "sessions": 0, "conversion_rate": 0}
