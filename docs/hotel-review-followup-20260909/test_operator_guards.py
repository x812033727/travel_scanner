"""Offline follow-up operator guards; no database, network or production writes."""

import copy
import importlib.util
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "hotel_followup_ops", REPO / "ops/hotel_review_followup_20260909.py"
)
ops = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ops)
BASE, ROWS, PENDING = ops.baseline_data(Path(__file__).with_name("before.json"))
CAPTURED = ops.evidence_timestamp(ops.BASELINE_CAPTURED_AT)


def stamp():
    return max(datetime.now(UTC), CAPTURED + timedelta(seconds=1)).isoformat()


def entry_for(kind, identifier, approve=False):
    row = PENDING[(kind, identifier)]
    urls = [row["source_url"]] if kind == "product" else [row["url"], row["evidence_url"]]
    entry = {
        "kind": kind,
        "id": identifier,
        "version": row["version"],
        "before_hash": ops.digest(row),
        "decision": "approve" if approve else "hold",
        "reason": "Offline fixture: fresh exact hotel evidence was independently checked.",
        "new_evidence": "Offline fixture: newly opened exact hotel name and address page.",
        "source_urls": list(dict.fromkeys(u for u in urls if u)),
        "method": "iab",
        "checked_at": stamp(),
        "browser_verified": True,
    }
    if approve and kind == "option":
        entry["identity_note"] = "Offline fixture: exact hotel name and address matched."
    if approve and kind == "product":
        coords = ops.coordinate_evidence(row, stamp())
        place = "ChIJ_Offline_exact_ID_12345"
        map_url = "https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder"
        entry.update(
            facts_patch={
                **ops.coordinate_patch(row),
                "google_place_id": place,
                "map_verified": True,
            },
            evidence={
                "coordinates": coords,
                "map": {
                    "url": map_url,
                    "identity_verified": True,
                    "method": "iab",
                    "checked_at": stamp(),
                    "place_id": place,
                },
            },
            source_urls=entry["source_urls"] + [coords["url"], map_url],
        )
    return entry


def option_entry(approve=False):
    key = next(
        k
        for k, r in PENDING.items()
        if k[0] == "option" and r["discovery_status"] == "found" and r["url"]
    )
    return entry_for(*key, approve=approve)


def product_entry(identifier=None):
    return entry_for("product", identifier or next(iter(ops.COORDINATE_ROWS)), approve=True)


def manifest(*entries):
    return {
        "schema_version": 1,
        "tag": ops.TAG,
        "baseline_hash": ops.BASELINE_HASH,
        "decisions": list(entries or [option_entry()]),
    }


def old_evidence(monkeypatch, data):
    old = CAPTURED + timedelta(seconds=1)

    class LaterClock(datetime):
        @classmethod
        def now(cls, tz=None):
            return (old + timedelta(days=3)).astimezone(tz)

    for entry in data["decisions"]:
        entry["checked_at"] = old.isoformat()
        for item in entry.get("evidence", {}).values():
            item["checked_at"] = old.isoformat()
    monkeypatch.setattr(ops, "datetime", LaterClock)


def test_pinned_baseline_and_subset_not_blanket_reaudit():
    assert len(ROWS) == 420 and len(PENDING) == 174
    assert sum(r["status"] == "approved" for r in ROWS.values()) == 246
    ops.validate_manifest(manifest(), PENDING)
    with pytest.raises(ValueError, match="nonempty subset"):
        ops.validate_manifest(manifest(**{}) | {"decisions": []}, PENDING)
    draft = ops.template(BASE, PENDING)
    assert len(draft["decisions"]) == 174
    with pytest.raises(ValueError):
        ops.validate_manifest(draft, PENDING)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda m: m.update(tag="hotel-review-all-20260908"),
        lambda m: m.update(baseline_hash="0" * 64),
        lambda m: m["decisions"].append(copy.deepcopy(m["decisions"][0])),
        lambda m: m["decisions"][0].update(version=999),
        lambda m: m["decisions"][0].update(before_hash="0" * 64),
        lambda m: m["decisions"][0].update(new_evidence=""),
        lambda m: m["decisions"][0].update(new_evidence="TEMPLATE: no new evidence"),
        lambda m: m["decisions"][0].update(source_urls=[]),
        lambda m: m["decisions"][0].update(method="missing_exact_identity", browser_verified=False),
        lambda m: m["decisions"][0].update(checked_at=ops.BASELINE_CAPTURED_AT),
        lambda m: m["decisions"][0].update(checked_at="2026-09-08T17:00:00"),
        lambda m: m["decisions"][0].update(method="primary_web", browser_verified=True),
        lambda m: m["decisions"][0].update(facts_patch={"map_verified": True}),
    ],
)
def test_invalid_subset_or_unchanged_old_evidence_rejected(mutation):
    data = manifest()
    mutation(data)
    with pytest.raises((ValueError, TypeError)):
        ops.validate_manifest(data, PENDING)


@pytest.mark.parametrize("kind", ["product", "option"])
def test_previously_approved_rows_cannot_be_selected(kind):
    key = next(k for k, r in ROWS.items() if k[0] == kind and r["status"] == "approved")
    data = manifest()
    data["decisions"][0].update(kind=kind, id=key[1])
    with pytest.raises(ValueError, match="approved"):
        ops.validate_manifest(data, PENDING)


@pytest.mark.parametrize("identifier", list(ops.COORDINATE_ROWS))
def test_three_exact_cc0_claims_preserve_credits_and_options(identifier):
    entry = product_entry(identifier)
    row = ROWS[("product", identifier)]
    ops.validate_manifest(manifest(entry), PENDING)
    payload = ops.product_payload(row, entry)
    credits = [c.model_dump(mode="json") for c in payload.facts.source_credits]
    assert credits[:-1] == row["facts"]["source_credits"]
    assert credits[-1] == ops.coordinate_credit(ops.COORDINATE_ROWS[identifier])
    assert "hotel_links" not in payload.facts.model_fields_set
    assert payload.facts.latitude == ops.COORDINATE_ROWS[identifier]["latitude"]
    assert "?revision=" in payload.facts.coordinate_source_url


@pytest.mark.parametrize(
    "mutation",
    [
        lambda e: e["facts_patch"].update(latitude=1),
        lambda e: e["facts_patch"].update(longitude=1),
        lambda e: e["facts_patch"].update(
            coordinate_source_url="https://www.skyscanner.net/hotels/"
        ),
        lambda e: e["facts_patch"].update(source_credits=[]),
        lambda e: e["facts_patch"]["source_credits"][0].update(changes="Replaced original credit"),
        lambda e: e["facts_patch"]["source_credits"][-1].update(license_name="ODbL"),
        lambda e: e["facts_patch"]["source_credits"][-1].update(
            changes="Unbound alternative claim"
        ),
        lambda e: e["evidence"]["coordinates"].update(claim_id="other Skyscanner claim"),
        lambda e: e["evidence"]["coordinates"].update(revision=123),
        lambda e: e["evidence"]["coordinates"].update(reference="P248:Q1319169"),
        lambda e: e["evidence"]["coordinates"].update(qid="Q1"),
        lambda e: e["evidence"]["coordinates"].update(license_url="https://example.com/license"),
        lambda e: e["evidence"]["coordinates"].update(upstream="OTA"),
        lambda e: e["evidence"]["map"].update(place_id="mismatched_google_identity"),
        lambda e: e["evidence"]["map"].update(method="primary_web"),
        lambda e: e.update(method="primary_web", browser_verified=False),
        lambda e: e["facts_patch"].update(area_code="gion"),
        lambda e: e["facts_patch"].update(hotel_links=[]),
    ],
)
def test_new_coordinates_and_map_evidence_cannot_escape_allowlist(mutation):
    entry = product_entry()
    mutation(entry)
    with pytest.raises(ValueError):
        ops.validate_manifest(manifest(entry), PENDING)


@pytest.mark.parametrize("city", ["kyoto", "busan"])
def test_unallowlisted_product_never_gets_new_coordinates(city):
    row = next(
        r
        for (k, i), r in PENDING.items()
        if k == "product" and r["destination_id"] == city and i not in ops.COORDINATE_ROWS
    )
    with pytest.raises(ValueError, match="three exact"):
        ops.coordinate_patch(row)


def test_mutated_original_row_cannot_generate_coordinate_patch():
    row = copy.deepcopy(ROWS[("product", next(iter(ops.COORDINATE_ROWS)))])
    row["facts"]["latitude"] = 1
    with pytest.raises(ValueError, match="exact pending"):
        ops.coordinate_patch(row)


@pytest.mark.parametrize("method,browser", [("iab", True), ("primary_web", False)])
def test_option_approval_preserves_normal_health_contract(method, browser):
    entry = option_entry(True)
    entry.update(method=method, browser_verified=browser)
    ops.validate_manifest(manifest(entry), PENDING)


def test_independent_operating_date_hold_is_not_resolved_by_browser_identity():
    key = next(
        k
        for k, r in PENDING.items()
        if k[0] == "option" and r["product_id"] in ops.OPERATING_DATE_HOLDS and r["url"]
    )
    entry = entry_for(*key, approve=True)
    with pytest.raises(ValueError, match="operating-date"):
        ops.validate_manifest(manifest(entry), PENDING)
    entry.update(decision="hold")
    entry.pop("identity_note")
    ops.validate_manifest(manifest(entry), PENDING)


def test_full_snapshot_protects_all_omitted_rows_and_configuration():
    entry = option_entry()
    data = manifest(entry)
    ops.verify_state(BASE, BASE, ROWS, data, {})
    current = copy.deepcopy(BASE)
    current["configs"][0]["version"] += 1
    with pytest.raises(RuntimeError, match="Configuration changed"):
        ops.verify_state(current, BASE, ROWS, data, {})
    current = copy.deepcopy(BASE)
    row = next(r for r in current["options"] if r["id"] != entry["id"])
    row["identity_note"] += " unrelated change"
    with pytest.raises(RuntimeError, match="Full-row snapshot"):
        ops.verify_state(current, BASE, ROWS, data, {})
    current["options"].pop()
    with pytest.raises(RuntimeError, match="membership"):
        ops.verify_state(current, BASE, ROWS, data, {})


def test_duplicate_google_identity_rejected():
    entry = product_entry()
    payload = ops.product_payload(ROWS[("product", entry["id"])], entry)
    other = copy.deepcopy(BASE["products"][0])
    other["source_key"] = "editorial:other:hotel"
    other["facts"]["google_place_id"] = payload.facts.google_place_id
    with pytest.raises(RuntimeError, match="Duplicate map"):
        ops.duplicate_map(payload, [other])


class ActorSession:
    def __init__(self, active=True):
        self.actor = SimpleNamespace(id=uuid4(), is_active=active)
        self.root = SimpleNamespace(
            mode="review_pending", created_at=CAPTURED, actor_user_id=self.actor.id
        )

    async def get(self, model, identifier, **kwargs):
        return self.root if model is ops.CatalogReviewRun else self.actor

    async def scalar(self, query):
        return uuid4()


@pytest.mark.asyncio
async def test_old_authorization_readable_but_new_write_freshness_required(monkeypatch):
    old_evidence(monkeypatch, manifest())
    monkeypatch.setattr(ops, "is_admin_user", lambda user: True)
    session = ActorSession()
    assert await ops.actor_for(session) is session.actor
    with pytest.raises(ValueError, match="older than one day"):
        await ops.actor_for(session, require_fresh=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("active,admin", [(False, True), (True, False)])
async def test_current_admin_required_even_for_replay(monkeypatch, active, admin):
    monkeypatch.setattr(ops, "is_admin_user", lambda user: admin)
    with pytest.raises(RuntimeError, match="administrator"):
        await ops.actor_for(ActorSession(active))


def install_session(monkeypatch, data, existing_entries=()):
    actor = SimpleNamespace(id=uuid4())
    objects = {k: ops.MODELS[k[0]](**copy.deepcopy(r)) for k, r in ROWS.items()}
    receipts, added = [], []
    calls = {"fresh": 0, "commit": 0, "flush": 0, "refresh": 0, "locked": []}
    for entry in existing_entries:
        receipts.append(
            SimpleNamespace(
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
        )

    class Session:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def scalars(self, statement):
            return SimpleNamespace(all=lambda: receipts)

        async def commit(self):
            calls["commit"] += 1

        async def flush(self):
            calls["flush"] += 1
            for receipt in added:
                if receipt.id is None:
                    receipt.id = uuid4()

        async def refresh(self, row):
            calls["refresh"] += 1

        def add(self, row):
            added.append(row)

    async def actor_for(session, *, require_fresh=False):
        calls["fresh"] += int(require_fresh)
        return actor

    async def inventory(session, lock=False):
        current = copy.deepcopy(BASE)
        current["products"] = [
            ops.normalized(ops.record(o)) for k, o in objects.items() if k[0] == "product"
        ]
        current["options"] = [
            ops.normalized(ops.record(o)) for k, o in objects.items() if k[0] == "option"
        ]
        return current, objects

    async def lock(session, entry):
        calls["locked"].append(ops.target(entry))

    monkeypatch.setattr(ops, "SessionFactory", Session)
    monkeypatch.setattr(ops, "actor_for", actor_for)
    monkeypatch.setattr(ops, "inventory", inventory)
    monkeypatch.setattr(ops, "lock_entry", lock)
    monkeypatch.setattr(ops, "read_json", lambda path: data)
    return calls, objects, receipts, added


@pytest.mark.asyncio
async def test_dry_run_zero_writes_and_hold_commits_only_receipt(monkeypatch):
    data = manifest()
    entry = data["decisions"][0]
    calls, objects, _, added = install_session(monkeypatch, data)
    await ops.process_entry(entry, BASE, ROWS, data, False)
    assert calls["commit"] == calls["flush"] == calls["fresh"] == 0 and not added
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls["commit"] == 1 and len(added) == 1
    meta = added[0].metadata_json
    assert meta["before_hash"] == meta["after_hash"] == entry["before_hash"]
    assert meta["new_evidence"] == entry["new_evidence"]
    assert objects[(entry["kind"], entry["id"])].status == "pending"


@pytest.mark.asyncio
async def test_option_normal_route_deferred_commit_and_refreshed_receipt(monkeypatch):
    entry = option_entry(True)
    data = manifest(entry)
    calls, objects, _, added = install_session(monkeypatch, data)

    async def normal_review(*, product_id, option_id, payload, user, session):
        assert isinstance(session, ops.DeferredCommit)
        row = objects[("option", str(option_id))]
        assert row.product_id == product_id and payload.version == row.version
        row.status, row.version = "approved", row.version + 1
        row.identity_note, row.health_status = payload.identity_note, "unconfirmed"
        row.checked_at, row.verified_at = stamp(), stamp()
        await session.commit()
        assert calls["commit"] == 0

    monkeypatch.setattr(ops.admin, "review_hotel_option", normal_review)
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls["commit"] == 1 and calls["refresh"] == 1 and len(added) == 1
    assert added[0].metadata_json["after_hash"] == ops.digest(
        ops.normalized(ops.record(objects[("option", entry["id"])]))
    )
    assert added[0].metadata_json["outcome"] == "approved"


@pytest.mark.asyncio
async def test_product_uses_normal_edit_then_review_and_no_option_writes(monkeypatch):
    entry = product_entry()
    data = manifest(entry)
    calls, objects, _, added = install_session(monkeypatch, data)
    normal_actions = []
    options_before = {
        k: ops.digest(ops.normalized(ops.record(o))) for k, o in objects.items() if k[0] == "option"
    }

    async def edit(*, product_id, payload, version, user, session):
        assert isinstance(session, ops.DeferredCommit)
        row = objects[("product", str(product_id))]
        assert version == row.version and "hotel_links" not in payload.facts.model_fields_set
        row.facts.update(copy.deepcopy(entry["facts_patch"]))
        row.version += 1
        normal_actions.append("product_edit")
        await session.commit()
        assert calls["commit"] == 0

    async def review(*, product_id, payload, user, session):
        row = objects[("product", str(product_id))]
        assert payload.version == row.version == entry["version"] + 1
        row.status, row.version = "approved", row.version + 1
        row.verified_at = stamp()
        normal_actions.append("product_review")
        await session.commit()
        assert calls["commit"] == 0

    monkeypatch.setattr(ops.admin, "edit_product", edit)
    monkeypatch.setattr(ops.admin, "review_product", review)
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert normal_actions == ["product_edit", "product_review"]
    assert calls["commit"] == 1 and calls["refresh"] == 1 and len(added) == 1
    assert options_before == {
        k: ops.digest(ops.normalized(ops.record(o))) for k, o in objects.items() if k[0] == "option"
    }
    assert added[0].metadata_json["after_version"] == entry["version"] + 2


@pytest.mark.asyncio
async def test_old_approved_option_receipt_replays_without_renewing_evidence(monkeypatch):
    entry = option_entry(True)
    data = manifest(entry)
    old_evidence(monkeypatch, data)
    calls, objects, receipts, added = install_session(monkeypatch, data, [entry])
    row = objects[("option", entry["id"])]
    row.status, row.version = "approved", row.version + 1
    row.identity_note = entry["identity_note"]
    receipts[0].metadata_json.update(
        outcome="approved",
        after_hash=ops.digest(ops.normalized(ops.record(row))),
        after_version=row.version,
    )
    await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls["fresh"] == calls["commit"] == calls["flush"] == 0 and not added


@pytest.mark.asyncio
async def test_old_subset_receipts_verify_and_replay_without_new_audits(monkeypatch):
    data = manifest()
    old_evidence(monkeypatch, data)
    calls, _, _, added = install_session(monkeypatch, data, data["decisions"])
    await ops.review_all(SimpleNamespace(mode="verify", manifest="memory"), BASE, ROWS, PENDING)
    await ops.process_entry(data["decisions"][0], BASE, ROWS, data, True)
    assert calls["fresh"] == calls["commit"] == calls["flush"] == 0 and not added


@pytest.mark.asyncio
async def test_old_unreceipted_entry_cannot_write_hold(monkeypatch):
    data = manifest()
    old_evidence(monkeypatch, data)
    calls, _, _, added = install_session(monkeypatch, data)
    with pytest.raises(ValueError, match="older than one day"):
        await ops.process_entry(data["decisions"][0], BASE, ROWS, data, True)
    assert calls["commit"] == 0 and not added


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["manifest", "row", "duplicate", "actor", "extra_target"])
async def test_replay_keeps_full_guards(monkeypatch, change):
    data = manifest()
    entry = data["decisions"][0]
    calls, objects, receipts, added = install_session(monkeypatch, data, [entry])
    if change == "manifest":
        entry["new_evidence"] += " edited after receipt"
    elif change == "row":
        objects[("option", entry["id"])].version += 1
    elif change == "duplicate":
        receipts.append(copy.deepcopy(receipts[0]))
    elif change == "actor":
        receipts[0].actor_user_id = uuid4()
    else:
        receipts[0].target = ops.TAG + ":option:" + str(uuid4())
    with pytest.raises(RuntimeError):
        await ops.process_entry(entry, BASE, ROWS, data, True)
    assert calls["commit"] == 0 and not added


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["known", "unknown_app", "programming"])
async def test_fallback_only_known_normal_guard_errors(monkeypatch, kind):
    data = manifest(option_entry(True))
    monkeypatch.setattr(ops, "read_json", lambda path: data)
    calls = []

    async def process(entry, baseline, rows, current_manifest, apply, fallback_code=None):
        calls.append(fallback_code)
        if fallback_code is None:
            if kind == "programming":
                raise RuntimeError("Unexpected program error")
            raise ops.AppError(
                409,
                "service_link_unavailable" if kind == "known" else "service_version_conflict",
                "Offline guard fixture",
            )

    monkeypatch.setattr(ops, "process_entry", process)
    args = SimpleNamespace(mode="apply", manifest="memory")
    if kind == "known":
        await ops.review_all(args, BASE, ROWS, PENDING)
        assert calls == [None, "service_link_unavailable"]
    else:
        with pytest.raises((ops.AppError, RuntimeError)):
            await ops.review_all(args, BASE, ROWS, PENDING)
        assert calls == [None]


def test_result_must_persist_exact_coordinate_and_credit_patch():
    entry = product_entry()
    before = ROWS[("product", entry["id"])]
    after = copy.deepcopy(before)
    after.update(status="approved", version=before["version"] + 2)
    after["facts"].update(copy.deepcopy(entry["facts_patch"]))
    ops.allowed_result(before, after, entry)
    after["facts"]["latitude"] += 0.1
    with pytest.raises(RuntimeError, match="exact authorized fact"):
        ops.allowed_result(before, after, entry)
