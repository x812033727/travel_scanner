"""Bounded, independently evidenced hotspot review; no discovery or provider calls.

Run beside catalog_review_20260908.py inside the existing API container.
`snapshot` reads the twelve exact initial-scope rows. `dry-run --manifest FILE`
validates reviewed evidence and changes. Only `apply --manifest FILE --apply`
writes, using the normal hotspot review route and an atomic audit receipt.
The manifest is an explicit editorial decision, never raw model output.
"""

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

from app.catalog_review.repository import (
    entity_snapshot,
    fingerprint,
    load_entity,
    publication_gaps,
)
from app.db import SessionFactory, engine
from app.hotspots.admin_router import HotspotReviewRequest, review_hotspot_candidates
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
    HotspotLocalization,
    TravelHotspot,
)
from app.restaurants.editorial import validate_editorial_url
from catalog_review_20260908 import ROOT, actor_for
from sqlalchemy import select

TAG = "hotspot-browser-review-20260908-v1"
AUDIT_ACTION = "hotspot_candidate_browser_reviewed"
ALLOWED = (
    "986cbbf1-7a48-4403-ac8c-64c03b108f78",
    "6906c2f9-d5e7-4672-95eb-13ddaf09975a",
    "6549d291-ba31-4a3a-a917-07ad841ee774",
    "300aa3ea-c23b-4131-93dd-3eb3751110d8",
    "1a5add70-128a-48fe-a14e-0c34d3bcbf77",
    "59fb22f2-1523-46ea-b89f-2aa31a15e0aa",
    "7ef78031-c249-4595-bf48-e7bad72e29d2",
    "69b346b1-bdc3-4611-8ad8-34c7e008dd5a",
    "20f2672c-7be5-474b-adac-f235584956c7",
    "d58ed880-edc4-4278-ba3c-d7eb2a4ea71f",
    "e449e086-ea19-4ee5-a617-2cde4a0ca765",
    "b1ded271-2409-42b8-904c-8a85eefc3c89",
)
LOCATION_FIELDS = {
    "google_place_id",
    "naver_map_url",
    "latitude",
    "longitude",
    "coordinate_source_type",
    "coordinate_source_url",
    "map_match_status",
}
COORDINATE_FIELDS = {
    "latitude",
    "longitude",
    "coordinate_source_type",
    "coordinate_source_url",
}
ENTRY_FIELDS = {
    "id",
    "name",
    "expected_hash",
    "decision",
    "reason",
    "source_urls",
    "map_checked",
    "coordinates_checked",
    "map_evidence_url",
    "payload",
}


def emit(value):
    print(json.dumps(value, ensure_ascii=False, default=str), flush=True)


def validated_entries(document):
    if (
        not isinstance(document, list)
        or len(document) != len(ALLOWED)
        or any(not isinstance(entry, dict) for entry in document)
        or {entry.get("id") for entry in document} != set(ALLOWED)
    ):
        raise RuntimeError(
            "Manifest must contain exactly the twelve allowed hotspot IDs"
        )
    result = {}
    for entry in document:
        if set(entry) - ENTRY_FIELDS or ENTRY_FIELDS - {"map_evidence_url"} - set(
            entry
        ):
            raise RuntimeError("Unexpected or missing manifest field")
        if (
            not isinstance(entry["name"], str)
            or not entry["name"].strip()
            or not isinstance(entry["expected_hash"], str)
            or len(entry["expected_hash"]) != 64
            or any(c not in "0123456789abcdef" for c in entry["expected_hash"])
            or entry["decision"] not in {"approve", "keep_pending"}
            or not isinstance(entry["reason"], str)
            or not 1 <= len(entry["reason"].strip()) <= 500
            or type(entry["map_checked"]) is not bool
            or type(entry["coordinates_checked"]) is not bool
            or not isinstance(entry["payload"], dict)
            or set(entry["payload"]) - LOCATION_FIELDS
        ):
            raise RuntimeError(
                "Invalid explicit editorial decision or location payload"
            )
        urls = entry["source_urls"]
        if (
            not isinstance(urls, list)
            or not 1 <= len(urls) <= 10
            or any(not isinstance(url, str) for url in urls)
            or len(set(urls)) != len(urls)
        ):
            raise RuntimeError(
                "One to ten distinct independently read source URLs required"
            )
        for url in urls:
            if len(url) > 2048 or validate_editorial_url(url) != url:
                raise RuntimeError(
                    "Source URLs must be canonical public non-map HTTPS URLs"
                )
        map_url = entry.get("map_evidence_url")
        if map_url is not None:
            if not isinstance(map_url, str) or len(map_url) > 2048:
                raise RuntimeError("Invalid map evidence URL")
            parsed = urlsplit(map_url)
            if (
                parsed.scheme != "https"
                or parsed.hostname
                not in {
                    "www.google.com",
                    "maps.google.com",
                    "map.naver.com",
                    "developers.google.com",
                }
                or parsed.username
                or parsed.password
                or parsed.port not in {None, 443}
            ):
                raise RuntimeError(
                    "Map evidence must identify the inspected provider surface"
                )
        result[entry["id"]] = entry
    return result


def prepare_payload(entry, before):
    fields = dict(entry["payload"])
    if before.get("country_code") == "KR":
        if fields.get("google_place_id"):
            raise RuntimeError("Korean public identities require Naver, not Google")
    elif fields.get("naver_map_url"):
        raise RuntimeError("Non-Korean public identities require a Google Place ID")
    if any(isinstance(fields.get(key), bool) for key in ("latitude", "longitude")):
        raise RuntimeError("Coordinate values cannot be booleans")
    if (
        fields.keys() & {"google_place_id", "naver_map_url"}
        and not entry["map_checked"]
    ):
        raise RuntimeError("Changing a map identity requires an independent map check")
    if fields.keys() & COORDINATE_FIELDS and not entry["coordinates_checked"]:
        raise RuntimeError("Coordinate changes require independent coordinate evidence")
    approving = entry["decision"] == "approve"
    if approving:
        if not entry["map_checked"] or not entry["coordinates_checked"]:
            raise RuntimeError(
                "Approval requires both exact map and durable coordinate checks"
            )
        if fields.get("map_match_status", "verified") != "verified":
            raise RuntimeError("Approval conflicts with the supplied map status")
        fields["map_match_status"] = "verified"
    payload = HotspotReviewRequest.model_validate(
        {
            **fields,
            "ids": [entry["id"]],
            "action": "approve" if approving else "update",
            "reason": entry["reason"].strip(),
        }
    )
    candidate = dict(before)
    candidate.update(fields)
    verifying_map = fields.get("map_match_status") == "verified"
    if approving or verifying_map or fields.keys() & COORDINATE_FIELDS:
        source_url = candidate.get("coordinate_source_url")
        if (
            not entry["coordinates_checked"]
            or candidate.get("coordinate_source_type")
            not in {"wikidata", "official_tourism", "merchant_official"}
            or source_url not in entry["source_urls"]
        ):
            raise RuntimeError(
                "Coordinate claims need an independently inspected durable source"
            )
        validate_editorial_url(source_url)
    now = datetime.now(UTC).isoformat()
    if verifying_map:
        if not entry["map_checked"]:
            raise RuntimeError(
                "Map verification requires an independent exact identity check"
            )
        candidate["map_verified_at"] = now
    elif fields.get("map_match_status") in {"unverified", "ambiguous", "disabled"}:
        candidate["map_verified_at"] = None
    if fields.keys() & COORDINATE_FIELDS:
        candidate["coordinate_verified_at"] = (
            now
            if has_durable_coordinates(
                candidate.get("latitude"),
                candidate.get("longitude"),
                candidate.get("coordinate_source_type"),
                candidate.get("coordinate_source_url"),
            )
            else None
        )
    gaps = publication_gaps("hotspot", candidate)
    if approving and gaps:
        raise RuntimeError(f"Publication requirements remain: {gaps}")
    return payload, gaps


async def check_duplicate_identities(session, row, payload):
    for field in ("google_place_id", "naver_map_url"):
        value = (
            getattr(payload, field)
            if field in payload.model_fields_set
            else getattr(row, field)
        )
        if value:
            other = await session.scalar(
                select(TravelHotspot.id).where(
                    getattr(TravelHotspot, field) == value, TravelHotspot.id != row.id
                )
            )
            if other is not None:
                raise RuntimeError(
                    f"Exact map identity is already owned by hotspot {other}"
                )


async def audited_review(session, row, actor, payload, audit, approving):
    """Capture server timestamps and a replay hash before the route's single commit."""
    session.add(audit)
    commit = session.commit
    committed = False

    async def commit_with_receipt():
        nonlocal committed
        if committed:
            raise RuntimeError("Unexpected second route commit")
        await session.flush()
        await session.refresh(row)
        after = await entity_snapshot(session, row)
        gaps = publication_gaps("hotspot", after)
        if approving:
            if row.review_status != "approved" or not row.is_active or gaps:
                raise RuntimeError(
                    "Post-update publication state failed strict validation"
                )
        elif row.review_status != "pending" or row.is_active:
            raise RuntimeError("A keep-pending review must not publish the hotspot")
        audit.metadata_json = {
            **audit.metadata_json,
            "after": after,
            "after_hash": fingerprint(after),
            "gaps": gaps,
        }
        await commit()
        committed = True

    session.commit = commit_with_receipt
    try:
        await review_hotspot_candidates(payload, actor, session)
        if not committed:
            raise RuntimeError("Normal review route did not commit its audit receipt")
    finally:
        session.commit = commit


async def run(args):
    if datetime.now(UTC) >= datetime(2026, 9, 9, 6, 45, tzinfo=UTC):
        raise RuntimeError("One-off review authorization window has expired")
    if args.apply != (args.command == "apply"):
        raise RuntimeError("Writes require both the apply command and --apply")
    entries = None
    if args.command != "snapshot":
        if not args.manifest:
            raise RuntimeError("A reviewed manifest is required")
        document = json.loads(
            await asyncio.to_thread(Path(args.manifest).read_text, encoding="utf-8")
        )
        entries = validated_entries(document)
    elif args.manifest:
        raise RuntimeError("snapshot does not use a manifest")
    try:
        for identifier in ALLOWED:
            async with SessionFactory() as session:
                _, actor = await actor_for(session)
                entity_id = UUID(identifier)
                row = await load_entity(session, "hotspot", entity_id, lock=args.apply)
                original = await session.scalar(
                    select(CatalogReviewItem.id).where(
                        CatalogReviewItem.run_id == ROOT,
                        CatalogReviewItem.kind == "hotspot",
                        CatalogReviewItem.entity_id == entity_id,
                    )
                )
                if row is None or original is None:
                    raise RuntimeError(
                        "Hotspot is not in the authenticated original review scope"
                    )
                if args.apply:
                    # Lock existing translations too: the full reviewed snapshot includes them.
                    await session.scalars(
                        select(HotspotLocalization)
                        .where(HotspotLocalization.hotspot_id == entity_id)
                        .order_by(HotspotLocalization.locale)
                        .with_for_update()
                    )
                before = await entity_snapshot(session, row)
                if args.command == "snapshot":
                    emit(
                        {
                            "id": identifier,
                            "name": row.name,
                            "hash": fingerprint(before),
                            "gaps": publication_gaps("hotspot", before),
                            "snapshot": before,
                        }
                    )
                    continue
                entry = entries[identifier]
                if row.name != entry["name"]:
                    raise RuntimeError(
                        "Canonical hotspot name differs from the reviewed manifest"
                    )
                digest = fingerprint(entry)
                previous = await session.scalar(
                    select(AdminAuditLog).where(
                        AdminAuditLog.action == AUDIT_ACTION,
                        AdminAuditLog.target == f"hotspot:{identifier}",
                        AdminAuditLog.metadata_json["operation"].as_string() == TAG,
                    )
                )
                if previous:
                    if (
                        previous.actor_user_id != actor.id
                        or previous.metadata_json.get("root_run_id") != str(ROOT)
                        or previous.metadata_json.get("manifest_hash") != digest
                        or previous.metadata_json.get("after_hash")
                        != fingerprint(before)
                    ):
                        raise RuntimeError(
                            "Replay actor, manifest or committed hotspot changed"
                        )
                    emit(
                        {
                            "id": identifier,
                            "name": row.name,
                            "result": "replayed",
                            "status": row.review_status,
                            "active": row.is_active,
                        }
                    )
                    continue
                if (
                    row.review_status != "pending"
                    or row.is_active
                    or fingerprint(before) != entry["expected_hash"]
                ):
                    raise RuntimeError(
                        "Full reviewed snapshot or inactive pending state changed"
                    )
                payload, gaps = prepare_payload(entry, before)
                await check_duplicate_identities(session, row, payload)
                emit(
                    {
                        "id": identifier,
                        "name": row.name,
                        "decision": entry["decision"],
                        "dry_run": not args.apply,
                        "gaps": gaps,
                    }
                )
                if not args.apply:
                    continue
                audit = AdminAuditLog(
                    actor_user_id=actor.id,
                    action=AUDIT_ACTION,
                    target=f"hotspot:{identifier}",
                    metadata_json={
                        "operation": TAG,
                        "root_run_id": str(ROOT),
                        "root_item_id": str(original),
                        "manifest_hash": digest,
                        "reason": entry["reason"],
                        "source_urls": entry["source_urls"],
                        "map_evidence_url": entry.get("map_evidence_url"),
                        "independent_map_check": entry["map_checked"],
                        "independent_coordinate_check": entry["coordinates_checked"],
                        "decision": entry["decision"],
                        "before": before,
                        "payload": payload.model_dump(mode="json", exclude_unset=True),
                    },
                )
                await audited_review(
                    session, row, actor, payload, audit, entry["decision"] == "approve"
                )
                emit(
                    {
                        "id": identifier,
                        "name": row.name,
                        "result": "applied",
                        "status": row.review_status,
                        "active": row.is_active,
                    }
                )
    finally:
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["snapshot", "dry-run", "apply"])
    parser.add_argument("--manifest")
    parser.add_argument("--apply", action="store_true")
    asyncio.run(run(parser.parse_args()))
