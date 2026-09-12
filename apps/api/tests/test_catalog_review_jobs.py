"""Worker orchestration with in-memory sessions, mocked evidence and no Gemini HTTP."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from sqlalchemy.sql import operators
from sqlalchemy.sql.elements import Null

from app.catalog_review import jobs
from app.catalog_review.enrichment import EnrichmentTaxonomy, VerifiedCandidate
from app.catalog_review.errors import CatalogAssessmentError
from app.catalog_review.provider import VerifiedEnrichment
from app.catalog_review.schemas import (
    AssessmentBatch,
    DiscoveryBatch,
    DiscoveryDraft,
    EnrichmentAssessment,
    EvidenceSource,
    ReviewAssessment,
)
from app.catalog_review.service import allowed_actions as jobs_allowed_actions
from app.foods.place_matching import MerchantMatchReport
from app.models import CatalogReviewItem, CatalogReviewRun, FoodMerchant
from app.worker import QUEUE_NAMES


def matches(row: Any, expression: Any) -> bool:
    if expression is None:
        return True
    if hasattr(expression, "clauses"):
        return all(matches(row, clause) for clause in expression.clauses)
    left = getattr(row, expression.left.key)
    right = expression.right.value if hasattr(expression.right, "value") else True
    if expression.operator is operators.in_op:
        return left in right
    if expression.operator is operators.not_in_op:
        return left not in right
    if expression.operator is operators.is_:
        return left is None if isinstance(expression.right, Null) else left is right
    return left == right


class Store:
    def __init__(self, run: CatalogReviewRun, items: list[CatalogReviewItem] | None = None):
        self.rows: list[Any] = [run, *(items or [])]
        self.lock = asyncio.Lock()
        self.events: list[str] = []
        self.savepoints = 0

    def session(self) -> Session:
        return Session(self)


class Savepoint:
    def __init__(self, store: Store):
        self.store = store

    async def __aenter__(self) -> None:
        self.before = list(self.store.rows)
        self.store.savepoints += 1

    async def __aexit__(self, typ: Any, exc: Any, tb: Any) -> None:
        if exc is not None:
            self.store.rows = self.before


class Session:
    def __init__(self, store: Store):
        self.store = store
        self.locked = False

    async def __aenter__(self) -> Session:
        return self

    async def __aexit__(self, *_args: Any) -> None:
        self.release()

    def release(self) -> None:
        if self.locked:
            self.locked = False
            self.store.lock.release()

    async def scalars(self, statement: Any) -> SimpleNamespace:
        if statement._for_update_arg is not None and not self.locked:
            await self.store.lock.acquire()
            self.locked = True
        column = statement.column_descriptions[0]
        model = column["entity"]
        rows = [
            row
            for row in self.store.rows
            if isinstance(row, model) and matches(row, statement.whereclause)
        ]
        if column["expr"] is not model:
            rows = [getattr(row, column["expr"].key) for row in rows]
        return SimpleNamespace(all=lambda: rows)

    async def scalar(self, statement: Any) -> Any:
        rows = (await self.scalars(statement)).all()
        return rows[0] if rows else None

    async def commit(self) -> None:
        self.store.events.append("commit")
        self.release()

    async def flush(self) -> None:
        pass

    def add(self, row: Any) -> None:
        self.store.rows.append(row)

    def begin_nested(self) -> Savepoint:
        return Savepoint(self.store)


def new_run(**values: Any) -> CatalogReviewRun:
    defaults = dict(
        id=uuid4(),
        actor_user_id=uuid4(),
        mode="review_pending",
        status="queued",
        model="mock-gemini",
        version=1,
        usage_json={},
        result_json={},
        request_json={"max_calls": 80},
        phase="review_pending",
    )
    return CatalogReviewRun(**(defaults | values))


def new_item(run: CatalogReviewRun, number: int, **values: Any) -> CatalogReviewItem:
    defaults = dict(
        id=UUID(int=number),
        run_id=run.id,
        entity_id=uuid4(),
        kind="hotspot",
        name=f"Candidate {number}",
        destination_id="tokyo",
        status="pending",
        phase="review_pending",
        snapshot_hash="hash",
        snapshot_json={"source_urls": [f"https://www.wikidata.org/wiki/Q{number}"]},
        assessment_json={},
        evidence_json=[],
        gaps_json=[],
    )
    return CatalogReviewItem(**(defaults | values))


class FakeProvider:
    def __init__(self, store: Store):
        self.store = store
        self.reserve: Any = None
        self.usage = {key: 0 for key in jobs.TOKEN_KEYS}
        self.assess_calls: list[list[str]] = []
        self.discover_calls: list[dict[str, Any]] = []
        self.assess_failures = 0
        self.assess_plan: list[Exception | None] = []
        self.discover_failures = 0
        self.discover_batches: list[DiscoveryBatch] = []
        self.closed = False

    async def sent(self) -> None:
        await self.reserve()
        assert self.store.events[-1] == "commit"  # reservation persisted before HTTP
        self.store.events.append("http")
        self.usage["input_tokens"] += 10
        self.usage["output_tokens"] += 5

    async def assess(self, candidates: list[Any]) -> AssessmentBatch:
        await self.sent()
        self.assess_calls.append([item.candidate_id for item in candidates])
        if self.assess_plan:
            error = self.assess_plan.pop(0)
            if error is not None:
                raise error
        if self.assess_failures:
            self.assess_failures -= 1
            raise CatalogAssessmentError("catalog_response_truncated", retryable=True)
        return AssessmentBatch(
            items=[
                ReviewAssessment(
                    candidate_id=item.candidate_id,
                    decision="needs_review",
                    confidence=0.5,
                    reason="Exact map identity still needs independent review",
                )
                for item in candidates
            ]
        )

    async def discover(
        self, kind: str, count: int, destinations: Any, avoid: Any
    ) -> DiscoveryBatch:
        await self.sent()
        self.discover_calls.append(
            dict(kind=kind, count=count, destinations=destinations, avoid=avoid)
        )
        if self.discover_failures:
            self.discover_failures -= 1
            raise CatalogAssessmentError("catalog_provider_timeout", retryable=True)
        return self.discover_batches.pop(0) if self.discover_batches else DiscoveryBatch()

    async def close(self) -> None:
        self.closed = True


def setup(
    monkeypatch: pytest.MonkeyPatch,
    run: CatalogReviewRun,
    items: list[CatalogReviewItem] | None = None,
) -> tuple[Store, FakeProvider]:
    store = Store(run, items)
    provider = FakeProvider(store)
    monkeypatch.setattr(jobs, "SessionFactory", store.session)
    monkeypatch.setattr(jobs, "get_redis", lambda: object())
    monkeypatch.setattr(jobs, "consume_search_budget", AsyncMock(return_value=True))
    monkeypatch.setattr(
        jobs,
        "load_runtime_settings",
        AsyncMock(
            return_value=SimpleNamespace(
                hotspot_guide_gemini_daily_search_budget=30,
            )
        ),
    )
    monkeypatch.setattr(jobs, "trusted_hosts", AsyncMock(return_value={"www.wikidata.org"}))

    async def evidence(urls: list[str], _hosts: Any) -> list[EvidenceSource]:
        text = "A short verified factual source excerpt."
        return [
            EvidenceSource(
                url=url,
                text=text,
                fetched=True,
                trusted=True,
                fingerprint=hashlib.sha256(text.encode()).hexdigest(),
            )
            for url in urls
        ]

    monkeypatch.setattr(jobs, "fetch_sources", AsyncMock(side_effect=evidence))

    def factory(_settings: Any, reserve: Any, **_kwargs: Any) -> FakeProvider:
        provider.reserve = reserve
        return provider

    monkeypatch.setattr(jobs, "CatalogGeminiProvider", factory)
    return store, provider


@pytest.mark.parametrize("status", ["completed", "partial", "failed", "cancelled"])
async def test_terminal_dispatch_does_not_make_calls(status: str, monkeypatch: pytest.MonkeyPatch):
    run = new_run(status=status)
    _, provider = setup(monkeypatch, run)
    await jobs._run(run.id)
    assert run.status == status
    assert not provider.assess_calls and not provider.discover_calls


async def test_only_one_worker_claims_and_stale_tokens_cannot_reserve(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run()
    setup(monkeypatch, run)
    claimed = await asyncio.gather(jobs._claim_run(run.id), jobs._claim_run(run.id))
    assert sum(value is not None for value in claimed) == 1
    original_token = run.lease_token
    run.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    assert await jobs._claim_run(run.id) is run
    assert run.lease_token != original_token
    settings = SimpleNamespace(hotspot_guide_gemini_daily_search_budget=30)
    with pytest.raises(jobs.LeaseLost):
        await jobs.reserve_call(run.id, original_token, settings)
    assert run.usage_json == {}


async def test_concurrent_budget_reservations_never_exceed_run_limit(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(request_json={"max_calls": 1})
    setup(monkeypatch, run)
    await jobs._claim_run(run.id)
    settings = SimpleNamespace(hotspot_guide_gemini_daily_search_budget=30)
    values = await asyncio.gather(
        *(jobs.reserve_call(run.id, run.lease_token, settings) for _ in range(2)),
        return_exceptions=True,
    )
    assert sum(value is True for value in values) == 1
    assert sum(isinstance(value, jobs.BudgetStopped) for value in values) == 1
    assert run.usage_json["calls"] == 1
    assert jobs.consume_search_budget.await_count == 1


@pytest.mark.parametrize("configured_limit", [40, 80, 300])
async def test_worker_honors_explicit_run_snapshot_above_80_not_current_settings(
    monkeypatch: pytest.MonkeyPatch, configured_limit: int
):
    run = new_run(request_json={"max_calls": 160}, usage_json={"calls": 159})
    store, _ = setup(monkeypatch, run)
    await jobs._claim_run(run.id)
    settings = SimpleNamespace(
        catalog_review_max_calls=configured_limit,
        hotspot_guide_gemini_daily_search_budget=250,
    )
    values = await asyncio.gather(
        *(jobs.reserve_call(run.id, run.lease_token, settings) for _ in range(3)),
        return_exceptions=True,
    )
    assert sum(value is True for value in values) == 1
    stopped = [value for value in values if isinstance(value, jobs.BudgetStopped)]
    assert len(stopped) == 2
    assert all(str(value) == "catalog_review_call_limit" for value in stopped)
    assert run.usage_json == {"calls": 160, "member_charged": False}
    jobs.consume_search_budget.assert_awaited_once()
    assert jobs.consume_search_budget.await_args.args[1:] == ("gemini", 250)
    assert store.events[-1] == "commit"


async def test_increased_run_cap_does_not_bypass_daily_budget(monkeypatch: pytest.MonkeyPatch):
    run = new_run(request_json={"max_calls": 160}, usage_json={"calls": 80})
    setup(monkeypatch, run)
    await jobs._claim_run(run.id)
    monkeypatch.setattr(jobs, "consume_search_budget", AsyncMock(return_value=False))
    settings = SimpleNamespace(hotspot_guide_gemini_daily_search_budget=80)
    with pytest.raises(jobs.BudgetStopped, match="catalog_review_daily_budget"):
        await jobs.reserve_call(run.id, run.lease_token, settings)
    assert run.usage_json == {"calls": 80}
    assert jobs.consume_search_budget.await_count == 1


async def test_missing_legacy_snapshot_still_stops_at_80(monkeypatch: pytest.MonkeyPatch):
    run = new_run(request_json={}, usage_json={"calls": 80})
    setup(monkeypatch, run)
    await jobs._claim_run(run.id)
    settings = SimpleNamespace(
        catalog_review_max_calls=1000, hotspot_guide_gemini_daily_search_budget=1000
    )
    with pytest.raises(jobs.BudgetStopped, match="catalog_review_call_limit"):
        await jobs.reserve_call(run.id, run.lease_token, settings)
    assert run.usage_json == {"calls": 80}
    jobs.consume_search_budget.assert_not_awaited()


async def test_batches_commit_and_resume_retries_only_errors(monkeypatch: pytest.MonkeyPatch):
    run = new_run()
    items = [new_item(run, number) for number in range(1, 26)]
    store, provider = setup(monkeypatch, run, items)
    provider.assess_failures = 1
    await jobs._run(run.id)
    assert [len(batch) for batch in provider.assess_calls] == [8, 8, 8, 1]
    assert [item.status for item in items] == ["error"] * 8 + ["assessed"] * 17
    assert run.status == "partial"
    assert run.usage_json == {
        "calls": 4,
        "input_tokens": 40,
        "output_tokens": 20,
        "thought_tokens": 0,
        "member_charged": False,
    }
    assert all("text" not in evidence for item in items for evidence in item.evidence_json)
    paid_items = [item_id for batch in provider.assess_calls[1:] for item_id in batch]
    # Explicit API resume retains item states, calls and all saved progress.
    run.status = "queued"
    _, resumed = setup(monkeypatch, run, items)
    await jobs._run(run.id)
    assert run.status == "completed"
    assert len(resumed.assess_calls) == 1
    assert not set(resumed.assess_calls[0]) & set(paid_items)
    assert run.usage_json["calls"] == 5
    assert jobs.fetch_sources.await_count == 1  # evidence is re-fetched for the retry
    assert store.events.count("http") == 4


async def test_daily_budget_is_partial_without_http_or_member_charge(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run()
    item = new_item(run, 1)
    _, provider = setup(monkeypatch, run, [item])
    monkeypatch.setattr(jobs, "consume_search_budget", AsyncMock(return_value=False))
    await jobs._run(run.id)
    assert run.status == "partial"
    assert run.error_code == "catalog_review_daily_budget"
    assert run.usage_json.get("calls", 0) == 0
    assert run.usage_json["member_charged"] is False
    assert item.status == "pending"
    assert not provider.assess_calls


async def test_runtime_call_limit_bounds_failing_batches(monkeypatch: pytest.MonkeyPatch):
    run = new_run(request_json={"max_calls": 1})
    items = [new_item(run, number) for number in range(1, 46)]
    _, provider = setup(monkeypatch, run, items)
    provider.assess_failures = 10
    await jobs._run(run.id)
    assert run.status == "partial" and run.error_code == "catalog_review_call_limit"
    assert len(provider.assess_calls) == 1
    assert sum(item.status == "error" for item in items) == 8
    assert sum(item.status == "pending" for item in items) == 37


def draft(number: int) -> DiscoveryDraft:
    return DiscoveryDraft(
        kind="merchant",
        name=f"Restaurant {number}",
        local_name=f"料理店{number}",
        slug=f"restaurant-{number}",
        destination_id="tokyo",
        source_urls=[f"https://www.wikidata.org/wiki/Q{number}"],
    )


async def test_discovery_counts_committed_rows_dedupes_and_reviews_new(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(
        mode="discover_new",
        request_json={
            "max_calls": 80,
            "requested_counts": {"hotspot": 0, "food": 0, "merchant": 2},
        },
    )
    store, provider = setup(monkeypatch, run)
    tombstone = FoodMerchant(
        id=uuid4(),
        slug="restaurant-1",
        name="Restaurant 1",
        local_name="料理店1",
        review_status="rejected",
        destination_id="tokyo",
    )
    store.rows.append(tombstone)
    provider.discover_batches = [
        DiscoveryBatch(items=[draft(1), draft(2)]),
        DiscoveryBatch(items=[draft(3)]),
    ]

    async def importing(session: Session, entry: DiscoveryDraft, *_args: Any) -> Any:
        if any(isinstance(row, FoodMerchant) and row.slug == entry.slug for row in store.rows):
            return None
        row = FoodMerchant(
            id=uuid4(),
            slug=entry.slug,
            name=entry.name,
            local_name=entry.local_name,
            destination_id="tokyo",
            review_status="pending",
            is_active=False,
        )
        session.add(row)
        return row

    async def review_item(session: Session, _run_id: UUID, _kind: str, row: Any, phase: str):
        item = new_item(
            run, len(store.rows) + 1, kind="merchant", name=row.name, entity_id=row.id, phase=phase
        )
        session.add(item)
        return item

    monkeypatch.setattr(jobs, "import_draft", importing)
    monkeypatch.setattr(jobs, "make_review_item", review_item)
    await jobs._run(run.id)
    assert run.status == "completed"
    assert run.result_json["created_counts"] == {"merchant": 2}
    assert run.result_json["duplicates"] == 1
    assert [call["count"] for call in provider.discover_calls] == [2, 1]
    assert "restaurant-1" in provider.discover_calls[0]["avoid"]
    assert "Restaurant 1" in provider.discover_calls[0]["avoid"]
    assert provider.discover_calls[0]["destinations"] != provider.discover_calls[1]["destinations"]
    assert store.savepoints == 3
    assert len(provider.assess_calls) == 1
    assert tombstone.review_status == "rejected"
    # A resumed/duplicated dispatch neither regenerates nor re-assesses completed records.
    run.status = "queued"
    await jobs._run(run.id)
    assert len(provider.discover_calls) == 2 and len(provider.assess_calls) == 1


async def test_three_empty_discovery_rounds_report_honest_shortfall(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(
        mode="discover_new",
        request_json={
            "requested_counts": {"hotspot": 0, "food": 0, "merchant": 7},
        },
    )
    _, provider = setup(monkeypatch, run)
    await jobs._run(run.id)
    assert run.status == "partial"
    assert run.result_json["shortfalls"]["merchant"] == 7
    assert run.result_json["created_counts"].get("merchant", 0) == 0
    assert len(provider.discover_calls) == 3
    assert all(call["count"] == 5 for call in provider.discover_calls)
    destination_windows = [
        tuple(entry["id"] for entry in call["destinations"]) for call in provider.discover_calls
    ]
    assert len(set(destination_windows)) == 3
    assert all(
        len(window) <= jobs.DISCOVERY_DESTINATION_BATCH_SIZE for window in destination_windows
    )
    assert run.result_json["discovery_round_counts"]["merchant"] == 3
    assert not provider.assess_calls


def test_enqueue_uses_registered_queue_and_closes_sync_redis(monkeypatch: pytest.MonkeyPatch):
    connection = Mock()
    queue = Mock()
    queue.enqueue.return_value.id = "job-123"
    factory = Mock(return_value=queue)
    monkeypatch.setattr(jobs.SyncRedis, "from_url", Mock(return_value=connection))
    monkeypatch.setattr(jobs, "Queue", factory)
    run_id = uuid4()
    assert jobs.enqueue_catalog_run(run_id) == "job-123"
    assert "catalog-review" in QUEUE_NAMES
    factory.assert_called_once_with("catalog-review", connection=connection)
    assert queue.enqueue.call_args.args == (
        "app.catalog_review.jobs.run_catalog_review",
        str(run_id),
    )
    connection.close.assert_called_once()


async def test_heartbeat_renews_only_the_current_worker_lease(monkeypatch: pytest.MonkeyPatch):
    run = new_run()
    setup(monkeypatch, run)
    await jobs._claim_run(run.id)
    run.lease_until = datetime.now(UTC) + timedelta(seconds=10)
    initial = run.lease_until
    monkeypatch.setattr(jobs, "HEARTBEAT_SECONDS", 0.001)
    token = run.lease_token
    heartbeat = asyncio.create_task(jobs._heartbeat(run.id, token))
    for _ in range(100):
        if run.lease_until > initial:
            break
        await asyncio.sleep(0.001)
    assert run.lease_until > initial + timedelta(seconds=200)
    run.lease_token = "replacement-worker-token"
    replacement_until = run.lease_until
    await asyncio.wait_for(heartbeat, timeout=1)
    assert run.lease_until == replacement_until


async def test_resuming_discovery_reviews_saved_new_items_without_recreating(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(
        mode="discover_new",
        request_json={
            "requested_counts": {"hotspot": 0, "food": 0, "merchant": 1},
        },
        result_json={"created_counts": {"merchant": 1}},
        usage_json={"calls": 1},
    )
    item = new_item(run, 1, kind="merchant", phase="review_new")
    _, provider = setup(monkeypatch, run, [item])
    importing = AsyncMock()
    monkeypatch.setattr(jobs, "import_draft", importing)
    await jobs._run(run.id)
    assert run.status == "completed"
    assert run.result_json["created_counts"] == {"merchant": 1}
    assert not provider.discover_calls
    assert len(provider.assess_calls) == 1
    importing.assert_not_called()
    assert run.usage_json["calls"] == 2


async def test_bad_draft_savepoint_keeps_good_drafts_and_counts_only_success(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(
        mode="discover_new",
        request_json={
            "requested_counts": {"hotspot": 0, "food": 0, "merchant": 2},
        },
    )
    store, provider = setup(monkeypatch, run)
    provider.discover_batches = [
        DiscoveryBatch(items=[draft(1), draft(2)]),
        DiscoveryBatch(items=[draft(3)]),
    ]

    async def importing(session: Session, entry: DiscoveryDraft, *_args: Any) -> Any:
        row = FoodMerchant(
            id=uuid4(),
            slug=entry.slug,
            name=entry.name,
            local_name=entry.local_name,
            destination_id="tokyo",
        )
        session.add(row)
        if entry.slug == "restaurant-1":
            raise ValueError("invalid draft after first entity flush")
        return row

    async def make_item(session: Session, _run_id: UUID, _kind: str, row: Any, phase: str):
        item = new_item(run, len(store.rows) + 10, entity_id=row.id, phase=phase)
        session.add(item)
        return item

    monkeypatch.setattr(jobs, "import_draft", importing)
    monkeypatch.setattr(jobs, "make_review_item", make_item)
    await jobs._run(run.id)
    assert run.status == "completed"
    assert run.result_json["created_counts"] == {"merchant": 2}
    assert store.savepoints == 3
    assert {row.slug for row in store.rows if isinstance(row, FoodMerchant)} == {
        "restaurant-2",
        "restaurant-3",
    }


async def test_assessed_applied_and_stale_items_are_never_reassessed(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run()
    items = [
        new_item(run, index + 1, status=status)
        for index, status in enumerate(("assessed", "applied", "stale", "pending"))
    ]
    _, provider = setup(monkeypatch, run, items)
    await jobs._run(run.id)
    assert provider.assess_calls == [[str(items[-1].id)]]
    assert [item.status for item in items] == ["assessed", "applied", "stale", "assessed"]


async def test_307_rows_fit_39_eight_item_requests_before_repairs(monkeypatch: pytest.MonkeyPatch):
    run = new_run()
    items = [new_item(run, number) for number in range(1, 308)]
    _, provider = setup(monkeypatch, run, items)
    await jobs._run(run.id)
    assert [len(batch) for batch in provider.assess_calls] == [8] * 38 + [3]
    assert run.usage_json["calls"] == 39
    assert run.status == "completed"
    assert all(item.status == "assessed" for item in items)


async def test_provider_circuit_preserves_success_and_unattempted_rows_until_explicit_resume(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run()
    items = [new_item(run, number) for number in range(1, 41)]
    _, provider = setup(monkeypatch, run, items)
    provider.assess_plan = [None] + [
        CatalogAssessmentError("catalog_provider_timeout", retryable=True, details={"attempt": 2})
        for _ in range(3)
    ]
    await jobs._run(run.id)
    assert run.status == "partial"
    assert run.error_code == "catalog_review_provider_circuit_open"
    assert [item.status for item in items] == ["assessed"] * 8 + ["error"] * 24 + ["pending"] * 8
    assert all(item.reason for item in items[-8:])
    assert run.lease_token is None and run.lease_until is None
    assert run.usage_json["calls"] == 4 and run.usage_json["member_charged"] is False
    assert len(provider.assess_calls) == 4
    assert jobs.fetch_sources.await_count == 4
    diagnostic = items[8].assessment_json
    assert diagnostic["code"] == "catalog_provider_timeout"
    assert diagnostic["retryable"] is True
    assert diagnostic["details"]["attempt"] == 2
    assert run.result_json["last_review_error"] == diagnostic
    assert run.result_json["consecutive_provider_failures"] == 3
    prior_assessments = [dict(item.assessment_json) for item in items[:8]]

    # A repeated queue delivery cannot reopen a partial circuit.
    await jobs._run(run.id)
    assert len(provider.assess_calls) == 4
    run.status = "queued"  # Only the explicit resume API makes this transition.
    _, resumed = setup(monkeypatch, run, items)
    await jobs._run(run.id)
    assert run.status == "completed"
    assert len(resumed.assess_calls) == 4
    assert not {str(item.id) for item in items[:8]} & {
        candidate_id for batch in resumed.assess_calls for candidate_id in batch
    }
    assert [item.assessment_json for item in items[:8]] == prior_assessments
    assert run.usage_json["calls"] == 8
    assert jobs.fetch_sources.await_count == 4
    assert run.result_json["consecutive_provider_failures"] == 0


async def test_success_resets_consecutive_provider_failure_count(monkeypatch: pytest.MonkeyPatch):
    run = new_run()
    items = [new_item(run, number) for number in range(1, 49)]
    _, provider = setup(monkeypatch, run, items)
    error = CatalogAssessmentError("catalog_response_truncated", retryable=True)
    provider.assess_plan = [error, error, None, error, error, None]
    await jobs._run(run.id)
    assert len(provider.assess_calls) == 6
    assert run.error_code == "catalog_review_incomplete"
    assert sum(item.status == "assessed" for item in items) == 16
    assert sum(item.status == "error" for item in items) == 32
    assert run.result_json["consecutive_provider_failures"] == 0


async def test_unknown_batch_error_is_sanitized_without_triggering_provider_circuit(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run()
    items = [new_item(run, number) for number in range(1, 33)]
    _, provider = setup(monkeypatch, run, items)
    secret = "raw-response-private-key-VERY-SECRET"
    provider.assess_plan = [ValueError(secret)] * 3 + [None]
    await jobs._run(run.id)
    assert len(provider.assess_calls) == 4
    assert run.error_code == "catalog_review_incomplete"
    assert items[0].assessment_json["code"] is None
    assert secret not in json.dumps(
        [run.result_json, *[item.assessment_json for item in items]], ensure_ascii=False
    )
    assert all("text" not in source for item in items for source in item.evidence_json)


async def test_budget_stop_remains_authoritative_before_circuit_threshold(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(request_json={"max_calls": 2})
    items = [new_item(run, number) for number in range(1, 41)]
    _, provider = setup(monkeypatch, run, items)
    provider.assess_failures = 3
    await jobs._run(run.id)
    assert run.error_code == "catalog_review_call_limit"
    assert run.usage_json["calls"] == 2
    assert run.result_json["consecutive_provider_failures"] == 2
    assert sum(item.status == "pending" for item in items) == 24


async def test_discovery_provider_circuit_stops_before_spending_on_other_kinds(
    monkeypatch: pytest.MonkeyPatch,
):
    run = new_run(
        mode="discover_new",
        request_json={"requested_counts": {"hotspot": 40, "food": 20, "merchant": 40}},
    )
    _, provider = setup(monkeypatch, run)
    provider.discover_failures = 9
    await jobs._run(run.id)
    assert run.status == "partial"
    assert run.error_code == "catalog_review_provider_circuit_open"
    assert len(provider.discover_calls) == 3 and not provider.assess_calls
    assert {call["kind"] for call in provider.discover_calls} == {"hotspot"}
    assert run.result_json["last_discovery_error"]["code"] == "catalog_provider_timeout"
    assert run.result_json["created_counts"] == {"hotspot": 0}
    assert run.result_json["shortfalls"] == {"hotspot": 40, "food": 20, "merchant": 40}
    assert run.usage_json["calls"] == 3 and run.usage_json["member_charged"] is False


@pytest.mark.parametrize("prior_failures", [2, 3])
async def test_expired_worker_reclaim_preserves_committed_failure_streak(
    monkeypatch: pytest.MonkeyPatch, prior_failures: int
):
    run = new_run(
        status="running",
        lease_token="expired-worker",
        lease_until=datetime.now(UTC) - timedelta(seconds=1),
        result_json={"consecutive_provider_failures": prior_failures},
        usage_json={"calls": prior_failures},
    )
    items = [new_item(run, number) for number in range(1, 17)]
    _, provider = setup(monkeypatch, run, items)
    provider.assess_failures = 3
    await jobs._run(run.id)
    assert run.status == "partial" and run.error_code == "catalog_review_provider_circuit_open"
    assert len(provider.assess_calls) == 3 - prior_failures
    assert run.usage_json["calls"] == 3
    assert run.result_json["consecutive_provider_failures"] == 3


# --- merchant enrichment -------------------------------------------------------------


def merchant_row(number: int, **values: Any) -> FoodMerchant:
    defaults = dict(
        id=UUID(int=1000 + number),
        slug=f"tokyo-sushi-{number}",
        destination_id="tokyo",
        country_code="JP",
        name=f"Sushi {number}",
        local_name=f"寿司{number}",
        names_json={},
        address=None,
        google_place_id=None,
        review_status="pending",
        map_match_status="unverified",
        is_active=False,
        display_order=number,
    )
    return FoodMerchant(**(defaults | values))


def enrich_item(run: CatalogReviewRun, merchant: FoodMerchant, number: int) -> CatalogReviewItem:
    return new_item(
        run,
        number,
        kind="merchant",
        entity_id=merchant.id,
        phase="enrich_merchants",
        name=merchant.name,
        snapshot_json={"source_urls": []},
        snapshot_hash="stale",
    )


def enrich_run(**values: Any) -> CatalogReviewRun:
    request = {"max_calls": 80, "scope": "foods", "identify_places": True}
    request.update(values.pop("request_json", {}))
    return new_run(
        mode="enrich_merchants", phase="enrich_merchants", request_json=request, **values
    )


def merchant_page_url(name: str) -> str:
    return f"https://{name.lower().replace(' ', '-')}.example/tsukiji"


class FakeEnrichProvider(FakeProvider):
    def __init__(self, store: Store):
        super().__init__(store)
        self.search_calls: list[list[str]] = []
        self.enrich_assess_calls: list[list[str]] = []
        self.search_failures = 0
        self.enrichment_diagnostics: dict[str, int] = {}

    async def enrich_search(self, merchants: list[dict[str, Any]]) -> list[dict[str, Any]]:
        await self.sent()
        self.search_calls.append([item["candidate_id"] for item in merchants])
        if self.search_failures:
            self.search_failures -= 1
            raise CatalogAssessmentError("catalog_provider_timeout", retryable=True)
        return [
            {
                "source_url": merchant_page_url(item["name"]),
                "title": f"{item['name']} official",
                "supporting_claims": [],
                "trusted": False,
            }
            for item in merchants
        ]

    async def enrich_assess(
        self,
        candidates: list[Any],
        *,
        verified: dict[str, list[VerifiedCandidate]],
        area_slugs: dict[str, list[str]],
        catalog: dict[str, Any],
    ) -> dict[str, VerifiedEnrichment]:
        await self.sent()
        self.enrich_assess_calls.append([item.candidate_id for item in candidates])
        results: dict[str, VerifiedEnrichment] = {}
        for item in candidates:
            pages = [
                page for page in verified.get(item.candidate_id, []) if page.kind == "official"
            ]
            corrections = [
                {
                    "field": "official_website_url",
                    "value": page.url,
                    "source_url": page.url,
                    "quote": item.local_name,
                    "title": page.title,
                    "kind": "merchant_website",
                }
                for page in pages[:1]
            ]
            results[item.candidate_id] = VerifiedEnrichment(
                assessment=EnrichmentAssessment(
                    candidate_id=item.candidate_id, confidence=0.8, reason="找到官網。"
                ),
                corrections=corrections,
                rejected={},
            )
        return results


def enrich_setup(
    monkeypatch: pytest.MonkeyPatch,
    run: CatalogReviewRun,
    merchants: list[FoodMerchant],
    *,
    match_outcomes: list[str] | None = None,
    fetched_text: Callable[[str], str | None] | None = None,
) -> tuple[Store, FakeEnrichProvider, list[CatalogReviewItem], list[list[str]]]:
    items = [enrich_item(run, merchant, number) for number, merchant in enumerate(merchants, 1)]
    store = Store(run, items)
    store.rows.extend(merchants)
    provider = FakeEnrichProvider(store)
    monkeypatch.setattr(jobs, "SessionFactory", store.session)
    monkeypatch.setattr(jobs, "get_redis", lambda: object())
    monkeypatch.setattr(jobs, "consume_search_budget", AsyncMock(return_value=True))
    monkeypatch.setattr(
        jobs,
        "load_runtime_settings",
        AsyncMock(return_value=SimpleNamespace(hotspot_guide_gemini_daily_search_budget=30)),
    )
    monkeypatch.setattr(jobs, "trusted_hosts", AsyncMock(return_value={"www.gotokyo.org"}))
    monkeypatch.setattr(
        jobs,
        "load_enrichment_taxonomy",
        AsyncMock(
            return_value=EnrichmentTaxonomy(
                areas_by_destination={
                    "tokyo": [{"slug": "tokyo-tsukiji", "names": {}, "match_terms": ["築地"]}]
                },
                categories=[{"slug": "sushi", "names": {}}],
            )
        ),
    )
    by_page = {merchant_page_url(merchant.name): merchant for merchant in merchants}

    async def evidence(urls: list[str], _hosts: Any) -> list[EvidenceSource]:
        sources = []
        for url in urls:
            merchant = by_page.get(url)
            text = (
                fetched_text(url)
                if fetched_text is not None
                else f"{merchant.local_name} {merchant.name} 東京都中央区築地 Tokyo"
                if merchant is not None
                else None
            )
            if text is None:
                sources.append(EvidenceSource(url=url, error="http_403"))
                continue
            sources.append(
                EvidenceSource(
                    url=url,
                    text=text,
                    fetched=True,
                    trusted=False,
                    fingerprint=hashlib.sha256(text.encode()).hexdigest(),
                )
            )
        return sources

    monkeypatch.setattr(jobs, "fetch_sources", AsyncMock(side_effect=evidence))
    matcher_calls: list[list[str]] = []
    outcomes = list(match_outcomes or [])

    async def fake_matcher(
        _session: Any, _redis: Any, _settings: Any, chunk: list[FoodMerchant], **kwargs: Any
    ) -> list[MerchantMatchReport]:
        assert kwargs["apply"] is True and kwargs["origin"] == "catalog_review"
        assert kwargs["run_id"] == run.id and kwargs["actor_id"] == run.actor_user_id
        assert await kwargs["should_continue"]() is True
        matcher_calls.append([merchant.slug for merchant in chunk])
        reports = []
        for merchant in chunk:
            outcome = outcomes.pop(0) if outcomes else "matched"
            if outcome == "matched":
                merchant.google_place_id = f"ChIJ{merchant.slug}"
            reports.append(MerchantMatchReport(merchant.slug, merchant.name, outcome))
            if outcome in jobs.ENRICH_STOP_OUTCOMES:
                break
        return reports

    monkeypatch.setattr(jobs, "match_merchant_places", fake_matcher)

    def factory(_settings: Any, reserve: Any, **_kwargs: Any) -> FakeEnrichProvider:
        provider.reserve = reserve
        return provider

    monkeypatch.setattr(jobs, "CatalogGeminiProvider", factory)
    return store, provider, items, matcher_calls


async def test_enrich_run_identifies_then_refreshes_snapshot_before_assessing(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    without_id = merchant_row(1)
    with_id = merchant_row(2, google_place_id="ChIJexisting")
    _, provider, items, matcher_calls = enrich_setup(monkeypatch, run, [without_id, with_id])
    await jobs._run(run.id)

    assert matcher_calls == [["tokyo-sushi-1"]]
    assert run.result_json["identify"] == {
        "processed": 1,
        "outcomes": {"matched": 1},
        "stopped": None,
        "matched_entity_ids": [str(without_id.id)],
    }
    assert provider.search_calls == [[str(items[0].id), str(items[1].id)]]
    assert provider.enrich_assess_calls == [[str(items[0].id), str(items[1].id)]]
    assert run.usage_json["calls"] == 2
    assert run.status == "completed" and run.phase == "enrich_merchants"
    first, second = items
    assert first.snapshot_hash != "stale"
    assert first.snapshot_json["google_place_id"] == "ChIJtokyo-sushi-1"
    assert first.assessment_json["identify"] == {
        "matched_in_run": True,
        "place_id": "ChIJtokyo-sushi-1",
        "skipped": None,
    }
    assert second.assessment_json["identify"]["matched_in_run"] is False
    for item in items:
        assert item.status == "assessed" and item.decision == "needs_review"
        (correction,) = item.assessment_json["corrections"]
        assert correction["kind"] == "merchant_website"
        assert correction["value"] == merchant_page_url(item.name)
        assert all("text" not in entry for entry in item.evidence_json)
        assert "missing_durable_coordinates" in item.gaps_json
    assert run.result_json["consecutive_provider_failures"] == 0


async def test_enrich_identify_skips_kr_rows_and_rows_with_place_id(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    korea = merchant_row(1, country_code="KR", destination_id="seoul", slug="seoul-hani")
    done = merchant_row(2, google_place_id="ChIJdone")
    fresh = merchant_row(3)
    _, provider, items, matcher_calls = enrich_setup(monkeypatch, run, [korea, done, fresh])
    await jobs._run(run.id)
    assert matcher_calls == [["tokyo-sushi-3"]]
    assert korea.google_place_id is None
    assert items[0].assessment_json["identify"]["skipped"] == "kr"
    assert items[1].assessment_json["identify"] == {
        "matched_in_run": False,
        "place_id": "ChIJdone",
        "skipped": None,
    }
    assert provider.search_calls and run.status == "completed"


async def test_enrich_identify_can_be_disabled_and_stops_on_usage_guard(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    run.request_json = {**run.request_json, "identify_places": False}
    _, provider, _, matcher_calls = enrich_setup(monkeypatch, run, [merchant_row(1)])
    await jobs._run(run.id)
    assert matcher_calls == []
    assert run.result_json["identify"]["stopped"] == "disabled"
    assert provider.search_calls and run.status == "completed"

    guarded = enrich_run()
    _, provider, _, matcher_calls = enrich_setup(
        monkeypatch, guarded, [merchant_row(1), merchant_row(2)], match_outcomes=["usage_guard"]
    )
    await jobs._run(guarded.id)
    assert matcher_calls == [["tokyo-sushi-1", "tokyo-sushi-2"]]
    assert guarded.result_json["identify"]["stopped"] == "usage_guard"
    assert guarded.result_json["identify"]["outcomes"] == {"usage_guard": 1}
    assert len(provider.search_calls) == 1 and guarded.status == "completed"


async def test_enrich_batches_two_calls_per_five_items(monkeypatch: pytest.MonkeyPatch):
    run = enrich_run()
    merchants = [merchant_row(n, google_place_id=f"ChIJ{n}") for n in range(1, 13)]
    _, provider, items, _ = enrich_setup(monkeypatch, run, merchants)
    await jobs._run(run.id)
    assert [len(call) for call in provider.search_calls] == [5, 5, 2]
    assert [len(call) for call in provider.enrich_assess_calls] == [5, 5, 2]
    assert run.usage_json["calls"] == 6
    assert all(item.status == "assessed" for item in items)
    assert run.status == "completed"


async def test_enrich_skips_the_structured_call_when_nothing_was_fetched(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    _, provider, items, _ = enrich_setup(
        monkeypatch,
        run,
        [merchant_row(1, google_place_id="ChIJ1")],
        fetched_text=lambda _url: None,
    )
    await jobs._run(run.id)
    assert len(provider.search_calls) == 1 and provider.enrich_assess_calls == []
    assert run.usage_json["calls"] == 1
    (item,) = items
    assert item.status == "assessed" and item.decision == "needs_review"
    assert item.reason == jobs.NO_PAGES_REASON
    assert item.assessment_json["corrections"] == []
    assert item.evidence_json == []
    assert jobs_allowed_actions(item) == ["keep_pending"]


async def test_enrich_marks_non_pending_merchants_stale_without_spending(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    approved = merchant_row(1, review_status="approved", google_place_id="ChIJ1")
    _, provider, items, matcher_calls = enrich_setup(monkeypatch, run, [approved])
    await jobs._run(run.id)
    assert matcher_calls == [] and provider.search_calls == []
    (item,) = items
    assert item.status == "stale" and item.reason == jobs.STALE_MERCHANT_REASON
    assert run.usage_json.get("calls", 0) == 0
    assert run.status == "completed"


async def test_enrich_circuit_breaker_after_three_failed_batches(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run()
    merchants = [merchant_row(n, google_place_id=f"ChIJ{n}") for n in range(1, 21)]
    _, provider, items, _ = enrich_setup(monkeypatch, run, merchants)
    provider.search_failures = 3
    await jobs._run(run.id)
    assert len(provider.search_calls) == 3 and provider.enrich_assess_calls == []
    assert run.status == "partial"
    assert run.error_code == "catalog_review_provider_circuit_open"
    assert sum(item.status == "error" for item in items) == 15
    assert sum(item.status == "pending" for item in items) == 5


async def test_enrich_budget_stop_is_partial_and_keeps_progress(
    monkeypatch: pytest.MonkeyPatch,
):
    run = enrich_run(request_json={"max_calls": 1, "scope": "foods"})
    _, provider, items, _ = enrich_setup(
        monkeypatch, run, [merchant_row(1, google_place_id="ChIJ1")]
    )
    await jobs._run(run.id)
    assert len(provider.search_calls) == 1 and provider.enrich_assess_calls == []
    assert run.status == "partial" and run.error_code == "catalog_review_call_limit"
    assert run.usage_json["calls"] == 1
    assert items[0].status == "pending"
