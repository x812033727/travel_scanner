"""What `record_event` promises: it identifies, it protects, and it never breaks."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest
from starlette.datastructures import Headers

from app.analytics.context import (
    EMPTY,
    bind_analytics_context,
    context_from_headers,
    reset_analytics_context,
)
from app.analytics.schemas import EventName
from app.analytics.service import (
    COUNTED_EVENT_NAMES,
    EVENT_NAMES,
    FUNNEL_STEPS,
    SERVER_OWNED_EVENTS,
    _properties,
)


def test_the_browser_may_only_claim_names_the_server_does_not_own() -> None:
    """A browser can say it viewed a page. It cannot say a use was charged."""
    claimable = set(EventName.__args__)  # type: ignore[attr-defined]
    assert claimable <= set(EVENT_NAMES)
    # Everything the server is the truth for stays out of reach, whatever a client posts.
    for name in ("usage_charged", "usage_insufficient", "offer_attached", "alert_created"):
        assert name not in claimable
    # `trip_created` is the exception: still accepted from an old bundle, then dropped,
    # so one tab left open across the deploy cannot double-count a trip.
    assert "trip_created" in claimable
    assert SERVER_OWNED_EVENTS == {"trip_created"}


def test_the_funnel_walks_names_that_exist_and_are_counted_per_session() -> None:
    assert set(FUNNEL_STEPS) <= set(COUNTED_EVENT_NAMES)
    assert "page_view" not in COUNTED_EVENT_NAMES
    assert len(set(EVENT_NAMES)) == len(EVENT_NAMES), "an event name is listed twice"
    # 32 characters is the column, and a name that does not fit is written as nothing.
    assert max(len(name) for name in EVENT_NAMES) <= 32


def test_properties_keep_the_shape_of_an_action_and_drop_anything_identifying() -> None:
    kept: dict[str, Any] = {"source": "blank", "uses": 2, "quoted_flight": True}
    assert _properties(kept) == kept
    dropped = {
        "trip_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "someone@example.com",
        "name": "京都五天",
        "note": "Mixed Case",
    }
    # Dropped whole, not truncated: half an identifier still identifies someone.
    assert _properties(dropped) == {}
    assert _properties(None) == {}
    assert len(_properties({f"k{index}": index for index in range(20)})) == 6


def test_every_literal_the_call_sites_pass_survives_the_filter() -> None:
    """A dropped value is a silent hole in the data, so the vocabulary is pinned here.

    These are the enum values the routers hand to ``record_event``. If one is renamed
    into a shape the filter refuses — a hyphen, a capital — the event keeps being
    written and the property quietly stops being there, which is the kind of gap that
    is only noticed a month later when a chart cannot be broken down.
    """
    passed = {
        # trip_created / offer_attached / place_added_to_trip
        "blank", "search", "ai_draft", "manual_blank", "hotel", "stay_area",
        "hotspot", "restaurant", "food_merchant", "lunch", "dinner",
        # alert_created
        "flight", "trip", "automatic", "manual_only",
        # ai_applied
        "day", "openai", "anthropic", "minimax", "catalog",
        "ready", "partial", "needs_setup", "fallback",
        # search_started / usage_*
        "travel_search", "full_trip_search", "flight_hotel_search", "multi_city_search",
        "flexible_flight_search", "full_trip_optimization", "flight_status_lookup",
    }
    for value in sorted(passed):
        assert _properties({"v": value}) == {"v": value}, value


def test_the_analytics_context_takes_only_a_well_formed_session_and_honours_opt_out() -> None:
    session_id = str(uuid4())
    context = context_from_headers(
        Headers(
            {
                "X-Travel-Analytics-Session": session_id,
                "X-Travel-User-Agent": "Mozilla/5.0 (iPhone)",
                "X-Travel-Country": "jp",
            }
        ),
        client_ip="203.0.113.9",
    )
    assert context.session_id == session_id
    assert context.country_code == "JP"
    assert context.opted_out is False

    # Anything that is not a UUID is no session at all, rather than a hash input a
    # caller chose: the digest of a value someone picks is a value someone can group by.
    for bogus in ("../etc", "not-a-uuid", "", "x" * 200):
        assert (
            context_from_headers(
                Headers({"X-Travel-Analytics-Session": bogus}), client_ip=None
            ).session_id
            is None
        )
    for header in ("Sec-GPC", "DNT"):
        assert context_from_headers(Headers({header: "1"}), client_ip=None).opted_out is True
    # Cloudflare's "unknown country" placeholders are not countries.
    for placeholder in ("XX", "T1", "zzz"):
        assert (
            context_from_headers(
                Headers({"X-Travel-Country": placeholder}), client_ip=None
            ).country_code
            is None
        )


def test_the_context_is_empty_outside_a_request_and_restored_after_one() -> None:
    from app.analytics.context import AnalyticsContext, analytics_context

    assert analytics_context() == EMPTY
    token = bind_analytics_context(AnalyticsContext(session_id="s"))
    assert analytics_context().session_id == "s"
    reset_analytics_context(token)
    assert analytics_context() == EMPTY


@pytest.mark.asyncio
async def test_recording_never_raises_at_the_call_site() -> None:
    """The thing being measured must not fail because the measuring did.

    Every call site awaits this in the middle of a request that is doing real work, so
    a broken session, an unknown name or a path analytics refuses has to come back as
    False rather than as an exception the router did not plan for.
    """
    from app.analytics.service import record_event

    class ExplodingSession:
        def __getattr__(self, name: str) -> Any:
            raise RuntimeError("database is gone")

    session = ExplodingSession()
    assert await record_event(session, "trip_created", path="/trips") is False  # type: ignore[arg-type]
    # An unknown name is refused before anything is touched, so a typo in a router
    # cannot silently write a row nothing will ever count.
    assert await record_event(session, "not_an_event", path="/trips") is False  # type: ignore[arg-type]
