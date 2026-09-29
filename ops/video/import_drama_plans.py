"""Import authored drama packages as waiting-for-owner documents, in one transaction.

Run with the API environment and PYTHONPATH=apps/api. --prepare writes a portable
bundle without connecting to a database. Database mode defaults to a read-only dry
run; --apply additionally requires the exact bundle hash and an active admin.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User
from app.video_automation.models import VideoDramaDoc, VideoDramaSeries
from app.video_automation.schemas import SeriesDocSubmitIn, SeriesIn
from app.video_automation.series import chapter_count, doc_problem, series_values

ACTION = "video_series_plans_imported"


def bundle_hash(bundle: dict[str, Any]) -> str:
    data = json.dumps(bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_packs(paths: list[Path]) -> dict[str, Any]:
    """Verify the checked-in receipts before preparing the portable source bundle."""
    works = []
    for path in paths:
        manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        payloads = {}
        for name in ("series-request.json", "documents.json"):
            # Git on Windows may convert line endings; the authored receipts use LF.
            source = (path / name).read_text(encoding="utf-8")
            digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
            if digest != manifest["files"].get(name):
                raise ValueError(f"{path.name}/{name}: manifest hash mismatch")
            payloads[name] = json.loads(source)
        request = payloads["series-request.json"]
        documents = payloads["documents.json"]
        if not (request["slug"] == documents["slug"] == manifest["slug"] == path.name):
            raise ValueError(f"{path}: mismatched source slugs")
        works.append(
            {
                "source": f"{path.parent.name}/{path.name}",
                "manifest_sha256": bundle_hash(manifest),
                "request": request,
                "documents": documents["documents"],
            }
        )
    bundle = {"schema_version": 1, "works": works}
    _validated(bundle)
    return bundle


def _validated(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    if bundle.get("schema_version") != 1 or not isinstance(bundle.get("works"), list):
        raise ValueError("expected a version 1 bundle with works")
    if not bundle["works"]:
        raise ValueError("the bundle has no works")
    plans = []
    seen: set[str] = set()
    now = datetime.now(UTC)
    for work in bundle["works"]:
        request = SeriesIn.model_validate(work["request"])
        if request.kind != "series" or request.hands_off or not request.slug:
            raise ValueError("only named, hands_off=false series can be imported")
        if request.slug in seen:
            raise ValueError(f"duplicate work: {request.slug}")
        seen.add(request.slug)
        if not work.get("source") or not work.get("manifest_sha256"):
            raise ValueError(f"{request.slug}: source provenance is required")
        values = series_values(request, now)
        row = VideoDramaSeries(**values, status="setting")
        docs = [SeriesDocSubmitIn.model_validate(doc) for doc in work["documents"]]
        keys = [(doc.kind, doc.chapter_number) for doc in docs]
        expected = {("setting", 0), ("outline", 0)} | {
            ("chapter", n)
            for n in range(1, chapter_count(row.planned_episodes, row.episodes_per_chapter) + 1)
        }
        if len(keys) != len(set(keys)) or set(keys) != expected:
            raise ValueError(f"{request.slug}: expected one setting, outline and every chapter")
        for doc in docs:
            problem = doc_problem(row, doc)
            if problem:
                raise ValueError(f"{request.slug}/{doc.kind}:{doc.chapter_number}: {problem}")
        plans.append({"work": work, "values": values, "docs": docs})
    return plans


async def import_plans(
    session: AsyncSession, bundle: dict[str, Any], *, actor: User | None = None
) -> list[dict[str, Any]]:
    """Validate/preflight the entire batch, then add it; the caller owns commit/rollback.

    Existing works must be the unchanged output of this importer. A progressed or
    edited work is a collision, never an excuse to replace the owner's decisions.
    No service with auto-approval, scheduling or intermediate commits is called.
    """
    plans = _validated(bundle)
    results = []
    missing = []
    with session.no_autoflush:
        for plan in plans:
            values, work, docs = plan["values"], plan["work"], plan["docs"]
            slug = values["slug"]
            statement = select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
            if actor is not None:
                statement = statement.with_for_update()
            current = await session.scalar(statement)
            if current is None:
                missing.append(plan)
            else:
                stored_docs = list(
                    await session.scalars(
                        select(VideoDramaDoc).where(VideoDramaDoc.series_id == current.id)
                    )
                )
                audit = await session.scalar(
                    select(AdminAuditLog).where(
                        AdminAuditLog.action == ACTION,
                        AdminAuditLog.target == f"video-series:{slug}",
                    )
                )
                wanted_docs = {(doc.kind, doc.chapter_number): doc for doc in docs}
                same = (
                    current.status == "setting"
                    and all(getattr(current, key) == value for key, value in values.items())
                    and len(stored_docs) == len(docs)
                    and audit is not None
                    and audit.metadata_json.get("work_sha256") == bundle_hash(work)
                )
                for doc in stored_docs:
                    wanted = wanted_docs.get((doc.kind, doc.chapter_number))
                    same = same and (
                        wanted is not None
                        and doc.version == 1
                        and doc.status == "review"
                        and doc.decided_at is None
                        and doc.decided_by_user_id is None
                        and doc.body_md == wanted.body_md
                        and doc.body_json == wanted.body_json
                    )
                if not same:
                    raise ValueError(f"{slug}: existing work differs; no works were imported")
            results.append(
                {
                    "slug": slug,
                    "title": values["title"],
                    "action": "create" if current is None else "unchanged",
                    "documents": len(docs),
                }
            )
    if actor is None:
        return results
    now = datetime.now(UTC)
    for plan in missing:
        row = VideoDramaSeries(
            id=uuid4(),
            **plan["values"],
            status="setting",
            created_by_user_id=actor.id,
            created_at=now,
            updated_at=now,
        )
        session.add(row)
        # There is no ORM relationship; insert the parent before its documents.
        await session.flush()
        for doc in plan["docs"]:
            session.add(
                VideoDramaDoc(
                    id=uuid4(),
                    series_id=row.id,
                    kind=doc.kind,
                    chapter_number=doc.chapter_number,
                    version=1,
                    body_md=doc.body_md,
                    body_json=doc.body_json,
                    status="review",
                    created_at=now,
                )
            )
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action=ACTION,
                target=f"video-series:{row.slug}",
                metadata_json={
                    "source": plan["work"]["source"],
                    "manifest_sha256": plan["work"]["manifest_sha256"],
                    "work_sha256": bundle_hash(plan["work"]),
                    "bundle_sha256": bundle_hash(bundle),
                    "documents": len(plan["docs"]),
                    "status": "review",
                },
            )
        )
    await session.flush()
    return results


async def _run(args: argparse.Namespace, bundle: dict[str, Any]) -> None:
    from app.config import get_settings
    from app.db import SessionFactory, engine
    from app.news_automation.sources_cli import admin_actor

    digest = bundle_hash(bundle)
    if args.apply and args.expected_sha256 != digest:
        raise ValueError("--apply requires --expected-sha256 from this bundle's dry run")
    try:
        async with SessionFactory() as session:
            if not args.apply and session.get_bind().dialect.name == "postgresql":
                await session.execute(text("SET TRANSACTION READ ONLY"))
            actor = None
            if args.apply:
                # Use configured administrator identity without printing account addresses.
                email = args.actor_email
                if not email:
                    emails = sorted(get_settings().admin_email_set)
                    if len(emails) != 1:
                        raise ValueError("select an active admin with --actor-email")
                    email = emails[0]
                actor = await admin_actor(session, email)
                if actor is None:
                    raise ValueError("an active administrator is required")
            results = await import_plans(session, bundle, actor=actor)
            if args.apply:
                await session.commit()
            else:
                await session.rollback()
            print(
                json.dumps(
                    {"applied": args.apply, "sha256": digest, "works": results},
                    ensure_ascii=False,
                    indent=2,
                )
            )
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pack", type=Path, action="append", help="one work directory; repeatable")
    source.add_argument("--input", type=Path, help="prepared bundle; '-' reads stdin")
    parser.add_argument(
        "--prepare", type=Path, help="write bundle without connecting to a database"
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--actor-email")
    args = parser.parse_args()
    if args.prepare and args.apply:
        parser.error("--prepare cannot be combined with --apply")
    try:
        if args.pack:
            bundle = load_packs(args.pack)
        else:
            raw = (
                sys.stdin.read()
                if str(args.input) == "-"
                else args.input.read_text(encoding="utf-8")
            )
            bundle = json.loads(raw)
        _validated(bundle)
        if args.prepare:
            args.prepare.write_text(
                json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps({"prepared": len(bundle["works"]), "sha256": bundle_hash(bundle)}))
        else:
            asyncio.run(_run(args, bundle))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Import refused: {error}\n")


if __name__ == "__main__":
    main()
