"""One-off, explicit catalog review operations; run in the existing API container.

No credentials or synthetic actors. The administrator is taken from the authenticated
UI request and checked against its audit log and current effective permission.
Default commands are read-only. Writes require --apply and use existing services.
Follow-up batches retain history and quotas; they never publish model suggestions.
"""

import argparse
import asyncio
import json
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID, uuid4

from app.admin.service import load_runtime_settings
from app.auth.service import is_admin_user
from app.catalog_review.repository import (
    entity_snapshot,
    fingerprint,
    load_entity,
    make_review_item,
    publication_gaps,
)
from app.catalog_review.router import enqueue_saved_run
from app.catalog_review.service import (
    ACTIVE,
    ApplyRequest,
    apply_decisions,
    item_view,
    prepare_resume,
    run_view,
)
from app.db import SessionFactory, engine
from app.foods.admin_router import (
    FoodMerchantBatchPayload,
    FoodMerchantUpdatePayload,
    batch_food_merchants,
    update_food_merchant,
)
from app.foods.styles import StyleReviewRequest, review_style, review_view
from app.infra import enforce_named_rate_limit, get_redis
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
    CatalogReviewRun,
    FoodMerchant,
    FoodMerchantStyle,
    User,
)
from sqlalchemy import select, text

ROOT = UUID("5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a")

# Independently read current official branch pages, 2026-09-08. This is not a
# Gemini assessment and never sets or refreshes map/coordinate verification.
BROWSER_MERCHANTS = {
    "0181ec5c-0143-457b-8090-73f232178c25": (
        "Yamamotoya Honten",
        "https://yamamotoyahonten.co.jp/storeguidance/",
        "官方門市頁確認栄本町通店，名古屋市中区栄2-14-5；非其他同品牌分店。",
    ),
    "ba83ce21-151b-4265-b5af-adece9eb27e9": (
        "Ukishima Brewing Tap Room",
        "https://www.ukishimabrewing.com/tap-room.html",
        "官方觀光局與店家 Tap Room 頁均確認牧志3-3-1水上店舗第二街區3F，"
        "提供餐食與精釀啤酒；不混用工廠，亦不採用舊觀光頁的營業時間。",
    ),
    "353561c3-51c1-4626-b0af-ad106a744c02": (
        "Gecko – Huế Cuisine & Craft Beer",
        "https://www.facebook.com/geckohuecuisine/",
        "瀏覽器核對店家公開頁，確認同名餐飲店、順化09 Pham Ngu Lao地址、"
        "啤酒花園與內用服務及店家發文，不混用其他Gecko分店。",
    ),
    "95019845-606a-4ebd-9c57-79e3d6e80950": (
        "Kanomwan Chang Moi",
        "https://www.facebook.com/Thaidessertcnx",
        "瀏覽器核對同名泰式甜點店及169 Chang Moi地址，完整閱讀店家公告，"
        "其為客訴回應而非停業通知；此核准僅確認身分，不作食品安全或品質背書。",
    ),
}


def emit(value):
    print(json.dumps(value, ensure_ascii=False, default=str), flush=True)


async def actor_for(session):
    root = await session.get(CatalogReviewRun, ROOT)
    if root is None or root.mode != "review_pending":
        raise RuntimeError("Authenticated root review is missing")
    if root.created_at < datetime.now(UTC) - timedelta(days=1):
        raise RuntimeError("Review authorization evidence is older than one day")
    actor = await session.get(User, root.actor_user_id)
    audit = await session.scalar(
        select(AdminAuditLog.id).where(
            AdminAuditLog.actor_user_id == root.actor_user_id,
            AdminAuditLog.action == "catalog_review_requested",
            AdminAuditLog.target == f"catalog-review:{ROOT}",
        )
    )
    if actor is None or not actor.is_active or not is_admin_user(actor) or audit is None:
        raise RuntimeError("Current administrator or authenticated request audit is invalid")
    return root, actor


async def family(session):
    root, actor = await actor_for(session)
    runs = list(
        (
            await session.scalars(
                select(CatalogReviewRun)
                .where(
                    CatalogReviewRun.created_at >= root.created_at,
                )
                .order_by(CatalogReviewRun.created_at)
            )
        ).all()
    )
    runs = [
        r for r in runs if r.id == ROOT or r.request_json.get("operational_root_id") == str(ROOT)
    ]
    items = list(
        (
            await session.scalars(
                select(CatalogReviewItem)
                .where(
                    CatalogReviewItem.run_id.in_([r.id for r in runs]),
                )
                .order_by(CatalogReviewItem.created_at, CatalogReviewItem.id)
            )
        ).all()
    )
    return root, actor, runs, items


async def next_batch(session, apply):
    await session.execute(text("SELECT pg_advisory_xact_lock(793654312)"))
    root, actor, runs, items = await family(session)
    if await session.scalar(
        select(CatalogReviewRun.id).where(CatalogReviewRun.status.in_(ACTIVE)).limit(1)
    ):
        raise RuntimeError("A review is still active; do not duplicate or interrupt it")
    assessed = {
        (i.kind, i.entity_id)
        for i in items
        if i.status in {"assessed", "applied", "stale"} and i.assessed_at
    }
    roots = [i for i in items if i.run_id == ROOT]
    remaining = [i for i in roots if (i.kind, i.entity_id) not in assessed]
    candidates = []
    for item in remaining:
        entity = await load_entity(session, item.kind, item.entity_id)
        if entity is not None and entity.review_status == "pending":
            candidates.append((item.kind, entity))
        if len(candidates) == 640:
            break
    counts = Counter(kind for kind, _ in candidates)
    emit(
        {
            "remaining_unassessed": len(remaining),
            "next_batch": len(candidates),
            "counts": counts,
            "apply": apply,
        }
    )
    if not apply or not candidates:
        return
    if len(runs) >= 5:
        raise RuntimeError(
            "Five-run operational safety ceiling reached; inspect before any further work"
        )
    settings = await load_runtime_settings(session)
    if not settings.hotspot_guide_gemini_api_key:
        raise RuntimeError("Gemini is not configured")
    await enforce_named_rate_limit("catalog-start", str(actor.id), limit=6, window_seconds=3600)
    request = {
        "mode": "review_pending",
        "prior_review_run_id": None,
        "requested_counts": dict(counts),
        "max_calls": 80,
        "operational_root_id": str(ROOT),
        "scope_hash": fingerprint([(k, str(e.id)) for k, e in candidates]),
    }
    run = CatalogReviewRun(
        id=uuid4(),
        actor_user_id=actor.id,
        idempotency_key=f"catalog-all-20260908-{len(runs)}-{request['scope_hash'][:16]}",
        request_hash=fingerprint(request),
        request_json=request,
        mode="review_pending",
        phase="review_pending",
        status="queued",
        version=1,
        model=settings.hotspot_guide_gemini_model,
        usage_json={"calls": 0, "member_charged": False},
        result_json={},
    )
    session.add(run)
    await session.flush()
    for kind, entity in candidates:
        await make_review_item(session, run.id, kind, entity, "review_pending")
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="catalog_review_requested",
            target=f"catalog-review:{run.id}",
            metadata_json={
                **request,
                "reason": "審核全部旅遊目錄：接續本輪未評估項目，保留既有工作與額度。",
            },
        )
    )
    await session.commit()
    await enqueue_saved_run(session, run)
    emit(await run_view(session, run))


async def styles(session, args):
    _, actor = await actor_for(session)
    if not args.manifest:
        rows = (
            await session.execute(
                select(FoodMerchant, FoodMerchantStyle)
                .join(
                    FoodMerchantStyle,
                    FoodMerchantStyle.merchant_id == FoodMerchant.id,
                )
                .where(FoodMerchantStyle.status == "pending")
                .order_by(FoodMerchant.name)
            )
        ).all()
        emit(
            [{"merchant_id": str(m.id), "name": m.name, "before": review_view(s)} for m, s in rows]
        )
        return
    entries = json.loads(await asyncio.to_thread(Path(args.manifest).read_text, encoding="utf-8"))
    if not 1 <= len(entries) <= 44:
        raise ValueError("Explicit manifest must contain 1-44 style decisions")
    for entry in entries:
        merchant_id = UUID(entry["merchant_id"])
        payload = StyleReviewRequest.model_validate(entry["payload"])
        target = f"food_merchant:{merchant_id}:{payload.review.style}"
        prior = await session.scalar(
            select(AdminAuditLog)
            .where(
                AdminAuditLog.actor_user_id == actor.id,
                AdminAuditLog.action == "food_merchant_style_reviewed",
                AdminAuditLog.target == target,
            )
            .order_by(AdminAuditLog.created_at.desc())
            .limit(1)
        )
        if prior and prior.metadata_json.get("reason") == payload.reason:
            emit({"name": entry["name"], "status": "replayed"})
            continue
        row = await session.scalar(
            select(FoodMerchantStyle).where(
                FoodMerchantStyle.merchant_id == merchant_id,
                FoodMerchantStyle.style == payload.review.style,
            )
        )
        merchant = await session.get(FoodMerchant, merchant_id)
        if (
            row is None
            or merchant is None
            or merchant.name != entry["name"]
            or review_view(row) != entry["before"]
        ):
            raise RuntimeError(f"Style snapshot changed: {entry['name']}")
        if row.status != "pending" or payload.expected_updated_at != row.updated_at:
            raise RuntimeError("Only the exact previously inspected pending style may change")
        if not args.apply:
            emit(
                {
                    "name": entry["name"],
                    "action": payload.review.status,
                    "reason": payload.reason,
                }
            )
        else:
            result = await review_style(session, merchant_id, payload, actor)
            emit(
                {
                    "name": entry["name"],
                    "style": result["style"],
                    "status": result["status"],
                }
            )


async def main(args):
    async with SessionFactory() as session:
        if args.command == "styles":
            await styles(session, args)
        elif args.command == "next":
            await next_batch(session, args.apply)
        else:
            _, actor, runs, items = await family(session)
            if args.command == "status":
                emit([await run_view(session, r) for r in runs])
            elif args.command == "correct-maks-identity":
                # Final public UI verification exposed a pre-existing identity conflict.
                # Correct only this task's own approval; never erase its audit history.
                entity_id = UUID("29732d41-650b-4931-9c85-beeb5445cc80")
                merchant = await load_entity(session, "merchant", entity_id, lock=True)
                prior = await session.scalar(
                    select(AdminAuditLog.id).where(
                        AdminAuditLog.action == "catalog_review_browser_override",
                        AdminAuditLog.target == f"merchant:{entity_id}",
                        AdminAuditLog.actor_user_id == actor.id,
                    )
                )
                corrected = await session.scalar(
                    select(AdminAuditLog.id).where(
                        AdminAuditLog.action == "catalog_review_identity_correction",
                        AdminAuditLog.target == f"merchant:{entity_id}",
                        AdminAuditLog.actor_user_id == actor.id,
                    )
                )
                if merchant is None or prior is None:
                    raise RuntimeError("Own previous approval is missing")
                if corrected:
                    if (
                        merchant.review_status != "pending"
                        or merchant.is_active
                        or merchant.map_match_status != "ambiguous"
                    ):
                        raise RuntimeError("Corrected merchant changed; inspect before proceeding")
                    emit({"name": merchant.name, "status": "correction_replayed"})
                    return
                root_item = next(i for i in items if i.run_id == ROOT and i.entity_id == entity_id)
                snapshot = await entity_snapshot(session, merchant)
                normalized = dict(snapshot)
                normalized["review_status"] = "pending"
                normalized["is_active"] = False
                normalized["updated_at"] = root_item.snapshot_json["updated_at"]
                if (
                    merchant.name != "Mak's Noodle Central"
                    or merchant.review_status != "approved"
                    or merchant.google_place_id != "ChIJx7wp6HwABDQRcl6W0a4eJL8"
                    or str(merchant.updated_at) != "2026-09-08 07:47:38.851847+00:00"
                    or fingerprint(normalized) != root_item.snapshot_hash
                ):
                    raise RuntimeError("Correction target changed beyond this task's approval")
                reason = (
                    "最終公開畫面複核發現名稱與地圖混店：官方及香港旅發局的Mak's Noodle"
                    "為威靈頓街77號麥奀雲吞麵世家；國泰來源的麥奀記忠記為永吉街37號。"
                    "瀏覽器核對既有精準Place ID確實指向後者，不能沿用作前者的驗證。"
                    "撤回本輪核准為待審並標記地圖ambiguous；保留原ID、座標及所有稽核，"
                    "待釐清名稱、來源與定位後重審。"
                )
                emit({"name": merchant.name, "action": "pending", "apply": args.apply})
                if args.apply:
                    session.add(
                        AdminAuditLog(
                            actor_user_id=actor.id,
                            action="catalog_review_identity_correction",
                            target=f"merchant:{entity_id}",
                            metadata_json={
                                "root_run_id": str(ROOT),
                                "prior_approval_audit_id": str(prior),
                                "action": "keep_pending",
                                "reason": reason,
                                "source_urls": [
                                    "https://www.discoverhongkong.com/tc/place-to-go/"
                                    "travel.guide-mak-s-noodle.html",
                                    "https://www.cathaypacific.com/cx/zh_TW/inspiration/"
                                    "dining/must-try-hong-kong-food.html",
                                ],
                                "before": {
                                    "review_status": merchant.review_status,
                                    "is_active": merchant.is_active,
                                    "map_match_status": merchant.map_match_status,
                                    "verified_at": str(merchant.verified_at),
                                },
                                "after": {
                                    "review_status": "pending",
                                    "is_active": False,
                                    "map_match_status": "ambiguous",
                                    "verified_at": None,
                                },
                            },
                        )
                    )
                    await update_food_merchant(
                        entity_id,
                        FoodMerchantUpdatePayload(
                            review_status="pending",
                            is_active=False,
                            map_match_status="ambiguous",
                        ),
                        actor,
                        session,
                    )
                    emit({"name": merchant.name, "status": "corrected_to_pending"})
            elif args.command == "browser-merchants":
                for identifier, (name, url, finding) in BROWSER_MERCHANTS.items():
                    entity_id = UUID(identifier)
                    item = next(
                        i
                        for i in items
                        if i.run_id == ROOT and i.kind == "merchant" and i.entity_id == entity_id
                    )
                    merchant = await load_entity(session, "merchant", entity_id, lock=True)
                    if merchant is None:
                        raise RuntimeError("Manual review target missing")
                    reason = "2026-09-08 全目錄人工來源複核：" + finding + " 來源：" + url
                    prior = await session.scalar(
                        select(AdminAuditLog.id).where(
                            AdminAuditLog.action == "catalog_review_browser_override",
                            AdminAuditLog.target == f"merchant:{entity_id}",
                            AdminAuditLog.actor_user_id == actor.id,
                        )
                    )
                    if prior and merchant.review_status == "approved":
                        emit({"name": name, "status": "replayed"})
                        continue
                    if merchant.name != name or merchant.review_status != "pending":
                        raise RuntimeError("Manual review target changed")
                    snapshot = await entity_snapshot(session, merchant)
                    if fingerprint(snapshot) != item.snapshot_hash:
                        raise RuntimeError("Manual review snapshot changed")
                    gaps = publication_gaps("merchant", snapshot)
                    applied_item = next(
                        (
                            candidate
                            for candidate in reversed(items)
                            if candidate.kind == "merchant"
                            and candidate.entity_id == entity_id
                            and candidate.applied_action == "keep_pending"
                            and candidate.assessed_at
                        ),
                        None,
                    )
                    if gaps or applied_item is None:
                        raise RuntimeError(f"Unresolved publication gaps: {gaps}")
                    emit(
                        {
                            "name": name,
                            "action": "approve",
                            "reason": reason,
                            "apply": args.apply,
                        }
                    )
                    if args.apply:
                        session.add(
                            AdminAuditLog(
                                actor_user_id=actor.id,
                                action="catalog_review_browser_override",
                                target=f"merchant:{entity_id}",
                                metadata_json={
                                    "root_run_id": str(ROOT),
                                    "item_id": str(applied_item.id),
                                    "assessment_run_id": str(applied_item.run_id),
                                    "prior_action": "keep_pending",
                                    "action": "approve",
                                    "reason": reason,
                                    "source_url": url,
                                    "map_verification_unchanged": True,
                                    "coordinate_verification_unchanged": True,
                                },
                            )
                        )
                        result = await batch_food_merchants(
                            FoodMerchantBatchPayload(
                                ids=[entity_id], action="approve", reason=reason
                            ),
                            actor,
                            session,
                        )
                        emit(result)
            elif args.command == "coverage":
                initial = {(i.kind, i.entity_id): i for i in items if i.run_id == ROOT}
                assessed = {
                    (i.kind, i.entity_id): i
                    for i in items
                    if i.assessed_at
                    and i.status in {"assessed", "applied", "stale"}
                    and (i.kind, i.entity_id) in initial
                }
                missing = [i for key, i in initial.items() if key not in assessed]
                emit(
                    {
                        "initial": len(initial),
                        "assessed": len(assessed),
                        "unassessed": len(missing),
                        "initial_kinds": Counter(i.kind for i in initial.values()),
                        "assessed_kinds": Counter(i.kind for i in assessed.values()),
                        "applied": Counter(i.applied_action for i in assessed.values()),
                        "pending_gaps": Counter(
                            g
                            for i in assessed.values()
                            if i.applied_action == "keep_pending"
                            for g in i.gaps_json
                        ),
                        "calls": sum(r.usage_json.get("calls", 0) for r in runs),
                        "unassessed_sample": [
                            {"name": i.name, "kind": i.kind} for i in missing[:20]
                        ],
                    }
                )
            elif args.command == "resume":
                run_id = UUID(args.run_id)
                if run_id not in {r.id for r in runs}:
                    raise RuntimeError("Resume outside the authorized review family")
                run = await session.get(CatalogReviewRun, run_id)
                emit(await run_view(session, run))
                if args.apply:
                    await enforce_named_rate_limit(
                        "catalog-resume", str(actor.id), limit=6, window_seconds=3600
                    )
                    run = await prepare_resume(session, run_id, actor.id)
                    await enqueue_saved_run(session, run)
                    emit(await run_view(session, run))
            elif args.command == "items":
                selected = [
                    i
                    for i in items
                    if (not args.decision or i.decision == args.decision)
                    and (not args.run_id or str(i.run_id) == args.run_id)
                ]
                emit(
                    [
                        (
                            {
                                k: v
                                for k, v in item_view(i).items()
                                if k not in {"evidence", "reason"}
                            }
                            if args.compact
                            else item_view(i)
                        )
                        | {"run_id": str(i.run_id)}
                        for i in selected[args.offset : args.offset + args.limit]
                    ]
                )
            elif args.command == "apply":
                entries = json.loads(
                    await asyncio.to_thread(Path(args.manifest).read_text, encoding="utf-8")
                )
                family_ids = {r.id for r in runs}
                for entry in entries:
                    run_id = UUID(entry["run_id"])
                    if run_id not in family_ids:
                        raise RuntimeError("Decision outside the authorized review family")
                    run = await session.get(CatalogReviewRun, run_id, populate_existing=True)
                    payload = ApplyRequest(
                        item_ids=entry["item_ids"],
                        action=entry["action"],
                        expected_version=entry["expected_version"],
                    )
                    notes = entry.get("reviewer_notes", {})
                    if set(notes) != set(entry["item_ids"]):
                        raise RuntimeError(
                            "Every explicit decision requires an editorial review note"
                        )
                    selected = [i for i in items if str(i.id) in notes and i.run_id == run_id]
                    if len(selected) != len(notes) or any(
                        not isinstance(n, str) or not n.strip() for n in notes.values()
                    ):
                        raise RuntimeError("Invalid editorial notes or item ownership")
                    if args.apply:
                        receipt_key = fingerprint(
                            {"actor": str(actor.id), "key": entry["idempotency_key"]}
                        )
                        if receipt_key not in (run.result_json or {}).get("apply_receipts", {}):
                            # Same transaction as the existing application service. Keep Gemini's
                            # original assessment immutable and distinguish editorial overrides.
                            for item in selected:
                                session.add(
                                    AdminAuditLog(
                                        actor_user_id=actor.id,
                                        action="catalog_review_editorial_decision",
                                        target=f"{item.kind}:{item.entity_id}",
                                        metadata_json={
                                            "run_id": str(run_id),
                                            "item_id": str(item.id),
                                            "model_decision": item.decision,
                                            "action": payload.action,
                                            "reason": notes[str(item.id)],
                                            "manifest_key": entry["idempotency_key"],
                                        },
                                    )
                                )
                        result = await apply_decisions(
                            session, run_id, actor.id, payload, entry["idempotency_key"]
                        )
                        emit(
                            {
                                "updated": result["updated"],
                                "outcomes": result["outcomes"],
                            }
                        )
                    else:
                        emit(
                            {
                                "run_id": str(run_id),
                                "action": payload.action,
                                "count": len(payload.item_ids),
                            }
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "status",
            "coverage",
            "items",
            "next",
            "styles",
            "apply",
            "resume",
            "browser-merchants",
            "correct-maks-identity",
        ),
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--manifest")
    parser.add_argument("--decision")
    parser.add_argument("--run-id")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=100)
    arguments = parser.parse_args()

    async def run():
        try:
            await main(arguments)
        finally:
            await get_redis().aclose()
            await engine.dispose()

    asyncio.run(run())
