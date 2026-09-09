"""Offline regression tests for the scoped operator; never connects to a database.

Run with the API environment and PYTHONPATH=apps/api:
pytest docs/hotel-review-all-20260908/test_operator_guards.py
"""

import copy
import importlib.util
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "hotel_review_ops", REPO / "ops/hotel_review_all_20260908.py"
)
ops = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ops)
BASE, ROWS, PENDING = ops.baseline_data(Path(__file__).with_name("checks-before.json"))
PARNAS = ROWS[("product", "e94492db-9582-4457-b47f-4b44f3112fbb")]


def timestamp(days=0):
    return (datetime.now(UTC) - timedelta(days=days)).isoformat()


def manifest(days=0):
    result = ops.template(BASE, PENDING)
    for entry in result["decisions"]:
        entry["checked_at"] = timestamp(days)
        entry["reason"] = "Offline test fixture: inspected identity remains unresolved; hold."
    return result


def coordinate_evidence(row):
    dataset = ops.COORDINATE_DATASETS[row["destination_id"]]
    return {
        "url": dataset[0],
        "license_url": dataset[1],
        "non_google": True,
        "checked_at": timestamp(),
    }


def input_for(row):
    return ops.ProductInput.model_validate(
        {
            key: copy.deepcopy(row[key])
            for key in (
                "source_key",
                "kind",
                "destination_id",
                "title",
                "names_json",
                "source_url",
                "facts",
            )
        }
    )


def parnas_entry():
    entry = next(e for e in manifest()["decisions"] if e["id"] == PARNAS["id"])
    url = "https://map.naver.com/p/entry/place/11583199"
    coords = coordinate_evidence(PARNAS)
    entry.update(
        decision="approve",
        method="iab",
        browser_verified=True,
        facts_patch={"map_verified": True, "naver_map_url": url},
        source_urls=[PARNAS["source_url"], coords["url"], url],
        evidence={
            "coordinates": coords,
            "map": {
                "url": url,
                "identity_verified": True,
                "method": "iab",
                "checked_at": timestamp(),
            },
        },
    )
    return entry


@pytest.mark.parametrize("identifier", list(ops.COORDINATE_ROWS))
def test_all_ten_pinned_coordinate_records(identifier):
    row = ROWS[("product", identifier)]
    ops.validate_coordinate_evidence(row, input_for(row), coordinate_evidence(row))


@pytest.mark.parametrize(
    "url",
    [
        "https://www.skyscanner.net/hotels/south-korea/seoul-hotels/example/",
        "https://www.booking.com/hotel/kr/example.html",
        "https://www.expedia.com/Example.h123.Hotel-Information",
        "https://maps.google.com/maps?q=Seoul",
        "https://map.naver.com/p/entry/place/11583199",
        "https://data.seoul.go.kr/dataList/UNREVIEWED/S/1/datasetView.do",
    ],
)
def test_non_google_flag_does_not_allow_unreviewed_upstream(url):
    row = copy.deepcopy(PARNAS)
    row["facts"]["coordinate_source_url"] = url
    evidence = {**coordinate_evidence(PARNAS), "url": url, "non_google": True}
    with pytest.raises(ValueError, match="not allowlisted"):
        ops.validate_coordinate_evidence(row, input_for(row), evidence)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda r, e: r["facts"].update(latitude=r["facts"]["latitude"] + 0.001),
        lambda r, e: r["facts"].update(longitude=r["facts"]["longitude"] + 0.001),
        lambda r, e: e.update(license_url="https://creativecommons.org/publicdomain/zero/1.0/"),
        lambda r, e: r["facts"]["source_credits"][0].update(license_name="CC0"),
        lambda r, e: r["facts"]["source_credits"][0].update(changes="Changed provenance"),
        lambda r, e: r["facts"]["source_credits"][0].update(url="https://example.com/other"),
        lambda r, e: r["facts"].update(source_credits=[]),
        lambda r, e: r.update(source_key="editorial:seoul:wrong-hotel"),
        lambda r, e: e.update(upstream="skyscanner"),
    ],
)
def test_coordinate_identity_values_credits_and_license_bound(mutation):
    row, evidence = copy.deepcopy(PARNAS), coordinate_evidence(PARNAS)
    mutation(row, evidence)
    with pytest.raises(ValueError):
        ops.validate_coordinate_evidence(row, input_for(row), evidence)


@pytest.mark.parametrize(
    "field", ["latitude", "longitude", "coordinate_source_url", "source_credits", "area_code"]
)
def test_product_patch_cannot_even_roundtrip_coordinate_fields(field):
    entry = parnas_entry()
    entry["facts_patch"][field] = copy.deepcopy(PARNAS["facts"][field])
    with pytest.raises(ValueError, match="cannot alter"):
        ops.product_payload(PARNAS, entry)


def test_exact_map_only_product_and_legacy_option_protection():
    payload = ops.product_payload(PARNAS, parnas_entry())
    assert payload.facts.latitude == PARNAS["facts"]["latitude"]
    assert "hotel_links" not in payload.facts.model_fields_set


def test_kyoto_new_coordinate_candidates_not_authorized_in_this_batch():
    row = next(r for r in BASE["products"] if r["destination_id"] == "kyoto")
    with pytest.raises(ValueError, match="ten pinned"):
        ops.validate_coordinate_evidence(row, input_for(row), coordinate_evidence(PARNAS))


def test_old_manifest_is_readable_but_new_write_is_not_fresh():
    data = manifest(days=2)
    ops.validate_manifest(data, PENDING)
    with pytest.raises(ValueError, match="older than one day"):
        ops.require_fresh_entry(data["decisions"][0])


def test_old_product_evidence_readable_but_new_write_rejected():
    entry = parnas_entry()
    entry["evidence"]["coordinates"]["checked_at"] = timestamp(days=2)
    ops.product_payload(PARNAS, entry)
    with pytest.raises(ValueError, match="older than one day"):
        ops.require_fresh_entry(entry)


def test_missing_timezone_still_rejected_for_read_only_manifest():
    data = manifest(days=2)
    data["decisions"][0]["checked_at"] = "2026-09-08T00:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        ops.validate_manifest(data, PENDING)


class ActorSession:
    def __init__(self, active=True):
        self.actor = SimpleNamespace(id=uuid4(), is_active=active)
        self.root = SimpleNamespace(
            mode="review_pending", created_at=timestamp(days=2), actor_user_id=self.actor.id
        )

    async def get(self, model, identifier, **kwargs):
        return self.root if model is ops.CatalogReviewRun else self.actor

    async def scalar(self, query):
        return uuid4()


@pytest.mark.asyncio
async def test_old_root_allows_read_but_not_new_write(monkeypatch):
    monkeypatch.setattr(ops, "is_admin_user", lambda user: True)
    session = ActorSession()
    assert await ops.actor_for(session) is session.actor
    with pytest.raises(ValueError, match="older than one day"):
        await ops.actor_for(session, require_fresh=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("active,admin", [(False, True), (True, False)])
async def test_old_receipt_actor_must_still_be_effective_admin(monkeypatch, active, admin):
    monkeypatch.setattr(ops, "is_admin_user", lambda user: admin)
    with pytest.raises(RuntimeError, match="administrator"):
        await ops.actor_for(ActorSession(active))


def receipt(entry, actor):
    return SimpleNamespace(
        id=uuid4(),
        target=ops.target(entry),
        actor_user_id=actor.id,
        metadata_json={
            "baseline_hash": ops.BASELINE_HASH,
            "root_run_id": str(ops.ROOT),
            "entry_hash": ops.digest(entry),
            "before_hash": entry["before_hash"],
            "after_hash": entry["before_hash"],
            "before_version": entry["version"],
            "after_version": entry["version"],
            "outcome": "hold",
        },
    )


def install_read_fixture(monkeypatch, data, selected_receipts):
    actor = SimpleNamespace(id=uuid4())
    existing = [receipt(e, actor) for e in selected_receipts]
    calls = {"fresh": 0, "commit": 0}
    objects = {key: ops.MODELS[key[0]](**copy.deepcopy(row)) for key, row in ROWS.items()}

    class Session:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def scalars(self, statement):
            return SimpleNamespace(all=lambda: existing)

        async def commit(self):
            calls["commit"] += 1

    async def actor_for(session, *, require_fresh=False):
        calls["fresh"] += int(require_fresh)
        return actor

    async def inventory(session, lock=False):
        return copy.deepcopy(BASE), objects

    async def lock(session, entry):
        pass

    monkeypatch.setattr(ops, "SessionFactory", Session)
    monkeypatch.setattr(ops, "actor_for", actor_for)
    monkeypatch.setattr(ops, "inventory", inventory)
    monkeypatch.setattr(ops, "lock_entry", lock)
    monkeypatch.setattr(ops, "read_json", lambda path: data)
    return calls, existing


@pytest.mark.asyncio
async def test_all_290_old_receipts_verify_without_freshness_or_write(monkeypatch):
    data = manifest(days=2)
    calls, _ = install_read_fixture(monkeypatch, data, data["decisions"])
    await ops.review_all(SimpleNamespace(mode="verify", manifest="memory"), BASE, ROWS, PENDING)
    assert calls == {"fresh": 0, "commit": 0}


@pytest.mark.asyncio
async def test_old_receipt_apply_replay_is_read_only(monkeypatch):
    data = manifest(days=2)
    entry = data["decisions"][0]
    calls, existing = install_read_fixture(monkeypatch, data, [entry])
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls == {"fresh": 0, "commit": 0}
    assert len(existing) == 1


@pytest.mark.asyncio
async def test_old_unexecuted_entry_cannot_create_even_hold_receipt(monkeypatch):
    data = manifest(days=2)
    entry = data["decisions"][0]
    calls, existing = install_read_fixture(monkeypatch, data, [])
    with pytest.raises(ValueError, match="older than one day"):
        await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls == {"fresh": 1, "commit": 0}
    assert not existing


@pytest.mark.asyncio
async def test_old_replay_still_rejects_edited_manifest(monkeypatch):
    data = manifest(days=2)
    entry = data["decisions"][0]
    calls, _ = install_read_fixture(monkeypatch, data, [entry])
    entry["reason"] += " Edited after receipt creation."
    with pytest.raises(RuntimeError, match="edited decision"):
        await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls == {"fresh": 0, "commit": 0}


@pytest.mark.asyncio
async def test_old_approved_option_receipt_replays_without_renewing_evidence(monkeypatch):
    data = manifest(days=2)
    entry = next(
        e
        for e in data["decisions"]
        if e["kind"] == "option" and ROWS[("option", e["id"])]["discovery_status"] == "found"
    )
    entry.update(decision="approve", identity_note="Offline exact identity fixture matched.")
    calls, existing = install_read_fixture(monkeypatch, data, [entry])
    current = copy.deepcopy(BASE)
    row = next(r for r in current["options"] if r["id"] == entry["id"])
    row.update(status="approved", version=row["version"] + 1, verified_at=timestamp(days=2))
    existing[0].metadata_json.update(
        outcome="approved", after_hash=ops.digest(row), after_version=row["version"]
    )

    async def inventory(session, lock=False):
        return current, {("option", entry["id"]): ops.HotelBookingOption(**row)}

    monkeypatch.setattr(ops, "inventory", inventory)
    ops.validate_manifest(data, PENDING)
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls == {"fresh": 0, "commit": 0}
    assert len(existing) == 1


@pytest.mark.asyncio
async def test_old_receipt_verification_still_detects_changed_current_row(monkeypatch):
    data = manifest(days=2)
    calls, _ = install_read_fixture(monkeypatch, data, data["decisions"])
    current = copy.deepcopy(BASE)
    current["options"][0]["identity_note"] = "Unrelated modification after the old receipt."

    async def inventory(session, lock=False):
        return current, {}

    monkeypatch.setattr(ops, "inventory", inventory)
    with pytest.raises(RuntimeError, match="Full-row snapshot changed"):
        await ops.review_all(SimpleNamespace(mode="verify", manifest="memory"), BASE, ROWS, PENDING)
    assert calls == {"fresh": 0, "commit": 0}
