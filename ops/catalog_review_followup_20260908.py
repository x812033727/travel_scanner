"""Explicit browser/source repairs; no discovery, scraping or automatic approval.

Run inside the existing API container. Requires this task's original authenticated
review script beside it. The manifest is reviewed by a human/assistant, not Gemini.
Snapshots and full audit before/after remain private on the existing server.
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
from app.foods.admin_router import FoodMerchantUpdatePayload, update_food_merchant
from app.models import AdminAuditLog, CatalogReviewItem
from app.restaurants.editorial import validate_editorial_url
from catalog_review_20260908 import ROOT, actor_for
from sqlalchemy import select

TAG = "catalog-browser-repair-20260908-v1"
ALLOWED = {
    "70a97881-68e3-435c-8658-bf23ccd24048",
    "daada54b-92dd-4866-9310-3c5c2437c051",
    "83ee9b26-82f0-4686-8986-cadb000da775",
    "9feea103-829e-4a7f-adb9-cec522bff3cc",
    "c56f4794-885e-4138-a442-d3196b69e9a8",
    "9034a7dc-d91e-4e99-a606-716a7d7f6e89",
    "23d0b22b-d98e-45b3-bb7e-42306120f7a1",
    "8b244f82-abe6-4662-bf75-0e94cba6e66d",
    "28248e3a-3ed9-4464-84fd-b48136070557",
}
FIELDS = {
    "address",
    "sources",
    "official_website_url",
    "latitude",
    "longitude",
    "coordinate_source_type",
    "coordinate_source_url",
}
PRIOR = {
    "0181ec5c-0143-457b-8090-73f232178c25": (
        "Yamamotoya Honten",
        "dd897dca99e79e6fe19794f91b1a650ce2d75304c88ee133975666e5def7626d",
    ),
    "ba83ce21-151b-4265-b5af-adece9eb27e9": (
        "Ukishima Brewing Tap Room",
        "df46e86e510516845d0db1527d9bbb7eb0e547aa9ba2c8892c208e2e88821d21",
    ),
    "353561c3-51c1-4626-b0af-ad106a744c02": (
        "Gecko – Huế Cuisine & Craft Beer",
        "81641ab2447a03a1ded796ad639056ecb66517699aa5f6b8c945b820b5167f6f",
    ),
    "95019845-606a-4ebd-9c57-79e3d6e80950": (
        "Kanomwan Chang Moi",
        "ff2b2de28c17e9151ca4d19525391f3b6f1c339395fce2e4543e8595043865ff",
    ),
}


async def audited_update(session, row, actor, payload, audit):
    session.add(audit)
    commit = session.commit

    async def commit_with_receipt():
        await session.flush()
        await session.refresh(row)
        after = await entity_snapshot(session, row)
        audit.metadata_json = {**audit.metadata_json, "after_hash": fingerprint(after)}
        await commit()

    session.commit = commit_with_receipt
    try:
        await update_food_merchant(row.id, payload, actor, session)
    finally:
        session.commit = commit


async def correct_prior(args):
    async with SessionFactory() as session:
        _, actor = await actor_for(session)
        for identifier, (name, expected) in PRIOR.items():
            entity_id = UUID(identifier)
            row = await load_entity(session, "merchant", entity_id, lock=args.apply)
            own_approval = await session.scalar(
                select(AdminAuditLog.id).where(
                    AdminAuditLog.action == "catalog_review_browser_override",
                    AdminAuditLog.actor_user_id == actor.id,
                    AdminAuditLog.target == f"merchant:{entity_id}",
                    AdminAuditLog.metadata_json["root_run_id"].as_string() == str(ROOT),
                )
            )
            if row is None or row.name != name or own_approval is None:
                raise RuntimeError("Own exact previous approval missing")
            before = await entity_snapshot(session, row)
            if args.command == "prior-snapshot":
                emit({"id": identifier, "name": name, "hash": fingerprint(before)})
                continue
            existing = await session.scalar(
                select(AdminAuditLog).where(
                    AdminAuditLog.action == "catalog_review_provenance_correction",
                    AdminAuditLog.target == f"merchant:{entity_id}",
                    AdminAuditLog.metadata_json["operation"].as_string() == TAG,
                )
            )
            if existing:
                if fingerprint(before) != existing.metadata_json["after_hash"]:
                    raise RuntimeError("Correction changed; inspect again")
                emit({"name": name, "status": "correction_replayed"})
                continue
            if (
                row.review_status != "approved"
                or not row.is_active
                or row.coordinate_source_type != "admin_verified"
                or urlsplit(row.coordinate_source_url or "").hostname != "maps.google.com"
                or fingerprint(before) != expected
            ):
                raise RuntimeError("Previous approval or coordinate provenance changed")
            payload = FoodMerchantUpdatePayload(
                review_status="pending",
                is_active=False,
                map_match_status="unverified",
                coordinate_source_type=None,
            )
            emit({"name": name, "action": "withdraw_own_approval", "dry_run": not args.apply})
            if args.apply:
                audit = AdminAuditLog(
                    actor_user_id=actor.id,
                    action="catalog_review_provenance_correction",
                    target=f"merchant:{entity_id}",
                    metadata_json={
                        "operation": TAG,
                        "root_run_id": str(ROOT),
                        "prior_approval_audit_id": str(own_approval),
                        "before": before,
                        "reason": "補查發現本輪先前核准沿用的永久座標實際源自Google，"
                        "不符合獨立持久來源要求。撤回自己的核准，保留原ID、座標、來源與歷史，"
                        "清除不成立的驗證標記；不代表停業，待獨立座標佐證後重審。",
                        "payload": payload.model_dump(mode="json", exclude_unset=True),
                    },
                )
                await audited_update(session, row, actor, payload, audit)
                emit({"name": name, "status": row.review_status, "active": row.is_active})


def emit(value):
    print(json.dumps(value, ensure_ascii=False, default=str), flush=True)


async def run(args):
    if datetime.now(UTC) > datetime(2026, 9, 9, 8, 0, tzinfo=UTC):
        raise RuntimeError("One-off review authorization window has expired")
    if args.command in {"prior-snapshot", "correct-prior"}:
        await correct_prior(args)
        await engine.dispose()
        return
    entries = json.loads(await asyncio.to_thread(Path(args.manifest).read_text, encoding="utf-8"))
    if {e["id"] for e in entries} != ALLOWED or len(entries) != len(ALLOWED):
        raise RuntimeError("Manifest does not match the exact nine reviewed merchants")
    async with SessionFactory() as session:
        _, actor = await actor_for(session)
        for entry in entries:
            entity_id = UUID(entry["id"])
            row = await load_entity(session, "merchant", entity_id, lock=args.command == "apply")
            original = await session.scalar(
                select(CatalogReviewItem.id).where(
                    CatalogReviewItem.run_id == ROOT,
                    CatalogReviewItem.kind == "merchant",
                    CatalogReviewItem.entity_id == entity_id,
                )
            )
            if row is None or original is None or row.name != entry["name"]:
                raise RuntimeError("Merchant is not the exact initial-scope candidate")
            before = await entity_snapshot(session, row)
            if args.command == "snapshot":
                emit(
                    {
                        "id": entry["id"],
                        "name": row.name,
                        "hash": fingerprint(before),
                        "place_id": row.google_place_id,
                        "sources": before["sources"],
                        "gaps": publication_gaps("merchant", before),
                    }
                )
                continue
            digest = fingerprint(entry)
            previous = await session.scalar(
                select(AdminAuditLog).where(
                    AdminAuditLog.action == "catalog_review_source_repaired",
                    AdminAuditLog.target == f"merchant:{entity_id}",
                    AdminAuditLog.metadata_json["operation"].as_string() == TAG,
                )
            )
            if previous:
                if previous.metadata_json["manifest_hash"] != digest:
                    raise RuntimeError("Idempotency key was reused with a changed manifest")
                if fingerprint(before) != previous.metadata_json["after_hash"]:
                    raise RuntimeError("Previously repaired merchant changed; review again")
                emit({"name": row.name, "status": "replayed"})
                continue
            if (
                row.review_status != "pending"
                or row.is_active
                or fingerprint(before) != entry["expected_hash"]
                or row.google_place_id != entry["place_id"]
            ):
                raise RuntimeError("Full snapshot or pending state changed")
            if before["sources"]:
                raise RuntimeError("Do not replace or refresh existing unreviewed source rows")
            if not entry["map_checked"] or not entry["reason"].strip():
                raise RuntimeError("Independent exact map check and reason are required")
            fields = dict(entry["payload"])
            if set(fields) - FIELDS:
                raise RuntimeError("Unreviewed mutation field in manifest")
            if entry["publish"]:
                source_url = fields.get("coordinate_source_url", "")
                validate_editorial_url(source_url)
                if fields.get("coordinate_source_type") not in {
                    "merchant_official",
                    "official_tourism",
                } or not any(
                    s["source_url"] == source_url and "coordinates" in s["claims"]
                    for s in fields["sources"]
                ):
                    raise RuntimeError("Publication requires independent coordinate evidence")
                if urlsplit(source_url).hostname not in {"yungkee.com.hk", "data.taipei"}:
                    raise RuntimeError("Unexpected coordinate source")
                fields.update(review_status="approved", is_active=True, map_match_status="verified")
            else:
                # Preserve legacy coordinates/URL in the private row and full audit,
                # but remove the unsupported durable-source assertion and its stamp.
                # The existing service couples verified map status to durable coordinates.
                # Keep the exact ID and record our identity check in the audit, but leave
                # complete location verification pending until the coordinate gap is filled.
                fields.update(
                    review_status="pending",
                    is_active=False,
                    coordinate_source_type=None,
                    map_match_status="unverified",
                )
            payload = FoodMerchantUpdatePayload.model_validate(fields)
            candidate = dict(before)
            candidate.update({k: v for k, v in fields.items() if k != "sources"})
            candidate["sources"] = [
                dict(s, claims_json=s["claims"], is_current=s.get("is_current", True))
                for s in fields["sources"]
            ]
            gaps = publication_gaps("merchant", candidate)
            if entry["publish"] and gaps:
                raise RuntimeError(f"Publication gaps remain: {gaps}")
            emit(
                {
                    "name": row.name,
                    "action": "approve" if entry["publish"] else "repair_keep_pending",
                    "dry_run": not args.apply,
                    "gaps": gaps,
                }
            )
            if not args.apply:
                continue
            audit = AdminAuditLog(
                actor_user_id=actor.id,
                action="catalog_review_source_repaired",
                target=f"merchant:{entity_id}",
                metadata_json={
                    "operation": TAG,
                    "root_run_id": str(ROOT),
                    "manifest_hash": digest,
                    "reason": entry["reason"],
                    "before": before,
                    "payload": fields,
                    "independent_map_check": True,
                    "unresolved": [] if entry["publish"] else ["independent_durable_coordinates"],
                },
            )
            await audited_update(session, row, actor, payload, audit)
            emit({"name": row.name, "status": row.review_status, "active": row.is_active})
    await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["snapshot", "apply", "prior-snapshot", "correct-prior"])
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    asyncio.run(run(arguments))
