"""One account's share of the planner's provider bill, and what happens when it is spent.

Creating a blank trip is the widest door onto a paid vendor in the product: it charges the
usage ledger nothing, and the twenty-trip cap it sits behind is undone by a single DELETE,
so create-delete-create was an unbounded loop over a roster that bills up to four times per
attempt. These pin the ceiling that closes it -- and, just as much, pin the paths that must
keep costing nothing, because a budget that counts a manual trip is a bug with a bill.

The counter is exercised through ``budget_spent`` rather than through Redis: ``_incr_window``
runs a Lua script and fakeredis has no Lua, which is the same reason the rest of the suite
patches the limiter instead of the client.
"""

from datetime import UTC, date, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest
from test_ai_itinerary import planner_candidates, request_for
from test_trip_preferences import harness as shared_harness

from app import infra
from app.ai import itinerary as itinerary_module
from app.ai.itinerary import (
    PLANNER_WARNING_BUDGET_REACHED,
    PLANNER_WARNING_FALLBACK_USED,
    PLANNER_WARNING_PROVIDER_FAILED,
    AIItineraryRequest,
    plan_within_budget,
)
from app.config import Settings
from app.models import UsageAccount
from app.trips import router as trips

harness = shared_harness


def keyed_settings(**overrides: object) -> Settings:
    """Settings with a roster, so the gate is reached rather than short-circuited.

    The budgets are pinned rather than left to the defaults because `conftest.py` raises
    them for the suite: what these tests are for is that the configured number reaches the
    counter, not what the number happens to be.
    """
    return Settings(  # type: ignore[arg-type]
        ai_planner_mode="auto",
        openai_api_key="k",
        ai_planner_user_budget=40,
        ai_planner_ip_budget=120,
        ai_planner_user_budget_window_seconds=3_600,
        **overrides,
    )


class PlannerSpy:
    """Stands in for the vendor call, and fails loudly if it happens when it should not."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, _settings: Settings) -> "PlannerSpy":
        return self

    async def generate(self, request: AIItineraryRequest) -> object:
        self.calls += 1
        return itinerary_module.catalog_result(request, [], datetime.now(UTC))


def stub_redis_writes(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """Replace the two Redis writes the gate makes beside the counter, and record them.

    Not optional. ``get_redis`` caches one client for the process, and pytest gives every
    test its own event loop, so whichever test first reached Redis leaves a pooled
    connection bound to a loop that is closed by the time the next one runs. On a machine
    with a Redis server the next write raises ``RuntimeError: Event loop is closed``,
    which ``record_rate_limit_hit`` does not catch -- without one it is a quietly swallowed
    ``ConnectionError``, which is why this only ever failed in CI.
    """
    recorded: list[tuple[str, str]] = []
    refunded: list[tuple[str, str]] = []

    async def record(namespace, identifier):
        recorded.append((namespace, identifier))

    async def refund(namespace, identifier):
        refunded.append((namespace, identifier))

    monkeypatch.setattr(itinerary_module, "record_rate_limit_hit", record)
    monkeypatch.setattr(itinerary_module, "refund_named_rate_limit", refund)
    return SimpleNamespace(recorded=recorded, refunded=refunded)


@pytest.fixture
def gate(monkeypatch: pytest.MonkeyPatch):
    """Record what was counted, and answer each namespace however the test wants."""
    counted: list[tuple[str, str, int, int]] = []
    spent: set[str] = set()

    async def budget_spent(namespace, identifier, *, limit, window_seconds):
        counted.append((namespace, identifier, limit, window_seconds))
        return namespace in spent

    planner = PlannerSpy()
    writes = stub_redis_writes(monkeypatch)
    monkeypatch.setattr(itinerary_module, "budget_spent", budget_spent)
    monkeypatch.setattr(itinerary_module, "AIItineraryPlanner", planner)
    return SimpleNamespace(
        counted=counted,
        recorded=writes.recorded,
        refunded=writes.refunded,
        spent=spent,
        planner=planner,
    )


async def test_a_draft_counts_one_attempt_against_the_account_and_the_address(gate) -> None:
    user_id = uuid4()
    await plan_within_budget(
        keyed_settings(), request_for(), user_id=user_id, source_ip="203.0.113.7"
    )
    assert gate.counted == [
        ("ai-planner-llm-user", str(user_id), 40, 3_600),
        ("ai-planner-llm-ip", "203.0.113.7", 120, 3_600),
    ]
    assert gate.planner.calls == 1


async def test_a_caller_with_no_address_is_still_counted_by_account(gate) -> None:
    # Server-side callers reach the planner without a Request. Losing the address must not
    # quietly lose the account ceiling with it.
    await plan_within_budget(keyed_settings(), request_for(), user_id=uuid4())
    assert [entry[0] for entry in gate.counted] == ["ai-planner-llm-user"]
    assert gate.planner.calls == 1


async def test_a_spent_account_never_also_spends_the_shared_address(gate) -> None:
    # One person on an office network must not be able to empty their colleagues' share on
    # requests that were never going to reach a provider anyway.
    gate.spent.add("ai-planner-llm-user")
    await plan_within_budget(
        keyed_settings(), request_for(), user_id=uuid4(), source_ip="203.0.113.7"
    )
    assert [entry[0] for entry in gate.counted] == ["ai-planner-llm-user"]
    assert gate.planner.calls == 0


async def test_a_spent_budget_returns_a_catalogue_plan_rather_than_an_error(gate) -> None:
    gate.spent.add("ai-planner-llm-user")
    result = await plan_within_budget(keyed_settings(), request_for(), user_id=uuid4())
    assert gate.planner.calls == 0
    assert result.planning.provider == "catalog"
    assert result.planning.status == "fallback"
    # The whole product decision: the traveller still leaves with an itinerary.
    assert any(day.items for day in result.itinerary)


async def test_a_budget_degrade_never_claims_a_provider_failed(gate) -> None:
    # The badge for `status == "fallback"` reads "AI is temporarily unavailable". It is not,
    # and saying so to someone who spent their own hour is the dishonesty the warning code
    # exists to prevent -- the web app picks its headline off exactly this list.
    gate.spent.add("ai-planner-llm-user")
    result = await plan_within_budget(keyed_settings(), request_for(), user_id=uuid4())
    assert result.planning.warnings == [PLANNER_WARNING_BUDGET_REACHED]
    assert PLANNER_WARNING_PROVIDER_FAILED not in result.planning.warnings
    assert PLANNER_WARNING_FALLBACK_USED not in result.planning.warnings


async def test_a_spent_budget_is_recorded_so_the_number_can_be_judged(gate) -> None:
    gate.spent.add("ai-planner-llm-user")
    user_id = uuid4()
    await plan_within_budget(keyed_settings(), request_for(), user_id=user_id)
    assert gate.recorded == [("ai-planner-llm-user", str(user_id))]


async def test_a_spent_address_degrades_an_account_still_inside_its_own_budget(gate) -> None:
    gate.spent.add("ai-planner-llm-ip")
    result = await plan_within_budget(
        keyed_settings(), request_for(), user_id=uuid4(), source_ip="203.0.113.7"
    )
    assert gate.planner.calls == 0
    assert result.planning.provider == "catalog"


async def test_an_address_refusal_gives_the_account_its_count_back(gate) -> None:
    # The account was counted before the shared address turned the attempt away, and no
    # provider was asked. Kept, a busy NAT whose window is spent would drain every traveller
    # behind it of their own hour -- a block that can outlast the shared one, because the
    # two windows open at different times.
    gate.spent.add("ai-planner-llm-ip")
    user_id = uuid4()
    await plan_within_budget(
        keyed_settings(), request_for(), user_id=user_id, source_ip="203.0.113.7"
    )
    assert gate.refunded == [("ai-planner-llm-user", str(user_id))]


async def test_a_spent_account_is_never_refunded(gate) -> None:
    gate.spent.add("ai-planner-llm-user")
    await plan_within_budget(
        keyed_settings(), request_for(), user_id=uuid4(), source_ip="203.0.113.7"
    )
    assert gate.refunded == []


async def test_an_attempt_that_reaches_the_roster_is_never_refunded(gate) -> None:
    # The refund above is for a call that never happened. One that did stays counted, or a
    # caller who can provoke a provider failure is never charged at all.
    await plan_within_budget(
        keyed_settings(), request_for(), user_id=uuid4(), source_ip="203.0.113.7"
    )
    assert gate.planner.calls == 1
    assert gate.refunded == []


async def test_an_uncountable_budget_is_treated_as_spent(monkeypatch) -> None:
    # budget_spent fails closed on an unreachable Redis, and this is the reason it does:
    # "the counter is down" must not be a way to buy an unmetered hour of a paid vendor.
    # Nothing is refused -- the traveller gets the catalogue plan, not a 503.
    planner = PlannerSpy()
    monkeypatch.setattr(itinerary_module, "AIItineraryPlanner", planner)
    writes = stub_redis_writes(monkeypatch)
    # Patched on infra so the real budget_spent runs: its fail-closed branch is the
    # thing under test, not a stub standing in for it.
    monkeypatch.setattr(infra, "_incr_window", lambda *a, **k: _none())
    user_id = uuid4()
    result = await plan_within_budget(keyed_settings(), request_for(), user_id=user_id)
    assert planner.calls == 0
    assert result.planning.provider == "catalog"
    assert writes.recorded == [("ai-planner-llm-user", str(user_id))]


async def _none() -> None:
    return None


async def test_a_planner_with_no_roster_does_not_spend_the_budget(gate) -> None:
    # An administrator pinning the planner to the catalogue spends nothing, so it must not
    # also empty every traveller's hour.
    await plan_within_budget(
        Settings(ai_planner_mode="fallback"), request_for(), user_id=uuid4()
    )
    assert gate.counted == []


async def test_a_request_with_no_candidates_never_reaches_a_provider(gate) -> None:
    # Not about budget at all. normalize_draft keeps only items naming a candidate_key from
    # this set, so an empty set can only come back empty -- after the whole roster has been
    # asked and billed. A destination the catalogue does not know is the ordinary way here,
    # which made a typed place name the cheapest way to spend four vendors at once.
    request = request_for().model_copy(update={"candidates": []})
    result = await plan_within_budget(keyed_settings(), request, user_id=uuid4())
    assert gate.planner.calls == 0
    assert gate.counted == []
    assert result.planning.provider == "catalog"


async def test_a_request_with_candidates_still_reaches_the_provider(gate) -> None:
    # The guard above must not be a way to stop planning working at all.
    assert planner_candidates()
    await plan_within_budget(keyed_settings(), request_for(), user_id=uuid4())
    assert gate.planner.calls == 1


def test_every_budget_setting_is_bounded() -> None:
    # An operator typing 0 into an env file must not silently switch the ceiling off.
    for field, value in [
        ("ai_planner_user_budget", 0),
        ("ai_planner_user_budget", 1_001),
        ("ai_planner_ip_budget", 0),
        ("ai_planner_user_budget_window_seconds", 59),
    ]:
        with pytest.raises(ValueError):
            Settings(**{field: value})  # type: ignore[arg-type]


async def test_creating_a_manual_blank_trip_never_touches_the_planner_budget(
    harness, monkeypatch
) -> None:
    # The wizard's own path, and what every existing creation test uses. A budget that
    # counted these would bill a traveller for typing their own itinerary.
    seen: list[object] = []

    async def spy(*args, **kwargs):
        seen.append(kwargs)
        raise AssertionError("a manual blank trip must never reach the planner")

    monkeypatch.setattr(trips, "plan_within_budget", spy)
    start = date.today() + timedelta(days=60)
    response = await harness["client"].post(
        "/trips",
        json={
            "source": "blank",
            "planning_mode": "manual_blank",
            "name": "Tokyo by hand",
            "destination_name": "Tokyo",
            "start_date": start.isoformat(),
            "end_date": (start + timedelta(days=2)).isoformat(),
            "routing": {"auto_compute": False},
        },
    )
    assert response.status_code == 201, response.text
    assert seen == []


async def test_creating_an_ai_draft_trip_meters_the_account_and_the_address(
    harness, monkeypatch
) -> None:
    seen: list[tuple[object, object]] = []

    async def spy(settings, request, *, user_id, source_ip=None):
        seen.append((user_id, source_ip))
        return itinerary_module.catalog_result(request, [], datetime.now(UTC))

    monkeypatch.setattr(trips, "plan_within_budget", spy)
    start = date.today() + timedelta(days=60)
    response = await harness["client"].post(
        "/trips",
        json={
            "source": "blank",
            "planning_mode": "ai_draft",
            "name": "Tokyo drafted",
            "destination_name": "Tokyo",
            "start_date": start.isoformat(),
            "end_date": (start + timedelta(days=2)).isoformat(),
            "routing": {"auto_compute": False},
        },
    )
    assert response.status_code == 201, response.text
    # The address reaches the gate, which is what bounds throwaway accounts: /auth/register
    # hands back a token immediately, so per-account alone is thirty budgets an hour.
    assert [user for user, _ in seen] == [harness["user"].id]
    assert len(seen) == 1 and seen[0][1] is not None


@pytest.fixture
def metered(monkeypatch):
    """Spy on the gate from the router's side, with the fair-use limiters out of the way."""
    seen: list[tuple[object, object]] = []

    async def spy(settings, request, *, user_id, source_ip=None):
        seen.append((user_id, source_ip))
        return itinerary_module.catalog_result(request, [], datetime.now(UTC))

    async def no_limit(*_args, **_kwargs):
        return None

    async def no_candidates(*_args, **_kwargs):
        # The harness trip travels with a dog, and pet-friendly candidates come from the
        # community, which this app does not mount. What is loaded is not under test here.
        return []

    monkeypatch.setattr(trips, "plan_within_budget", spy)
    monkeypatch.setattr(trips, "enforce_named_rate_limit", no_limit)
    monkeypatch.setattr(trips, "_load_trip_candidates", no_candidates)
    return seen


async def test_previewing_a_replan_meters_the_address_too(harness, metered) -> None:
    # /itinerary/preview and /intents reach the planner through _build_ai_planning. Metered
    # per account only, each freshly registered account would bring its own whole budget, and
    # the address ceiling would bound trip creation and nothing else.
    user_id = harness["user"].id
    trip_id, version = harness["trip"].id, harness["trip"].version
    response = await harness["client"].post(
        f"/trips/{trip_id}/itinerary/preview",
        headers={"Idempotency-Key": "preview-meters-the-address"},
        json={"version": version, "scope": "trip"},
    )
    assert response.status_code == 200, response.text
    assert [user for user, _ in metered] == [user_id]
    assert metered[0][1] is not None


async def test_the_deprecated_generate_route_meters_the_address_too(harness, metered) -> None:
    # This route reserves a use before it plans, so the account needs one to reserve.
    user_id = harness["user"].id
    trip_id, version = harness["trip"].id, harness["trip"].version
    harness["session"].add(
        UsageAccount(id=uuid4(), user_id=user_id, remaining_uses=5, reserved_uses=0)
    )
    await harness["session"].commit()
    response = await harness["client"].post(
        f"/trips/{trip_id}/itinerary/generate",
        headers={"Idempotency-Key": "generate-meters-the-address"},
        json={"version": version, "scope": "trip"},
    )
    # Whatever the route makes of a catalogue plan afterwards, the gate saw the address. The
    # ids were read before the call: the route's own commit expires the harness's objects.
    assert [user for user, _ in metered] == [user_id], response.text
    assert metered[0][1] is not None
