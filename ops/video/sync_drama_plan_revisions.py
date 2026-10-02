"""Synchronize reviewed drama plans without approving or starting production.

Run with PYTHONPATH=apps/api and the API environment. The default is a PostgreSQL
read-only dry run. --apply requires the exact reviewed bundle hash and an active
administrator. All preflight checks precede writes; one transaction owns the batch.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import SERIES_SLUG_PATTERN, SeriesDocSubmitIn
from app.video_automation.series import chapter_count, doc_problem

ACTION = "video_series_plan_revisions_synced"
OMITTED_COLUMNS = {"created_by_user_id", "decided_by_user_id"}


def bundle_hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def row_snapshot(row: Any) -> dict[str, Any]:
    """The same table-column representation as the reviewed live snapshot."""
    return {
        column.name: getattr(row, column.name)
        for column in row.__table__.columns
        if column.name not in OMITTED_COLUMNS
    }


def documents_hash(docs: list[VideoDramaDoc]) -> str:
    return bundle_hash(
        [
            row_snapshot(doc)
            for doc in sorted(docs, key=lambda d: (d.kind, d.chapter_number, d.version))
        ]
    )


class SeriesUpdates(BaseModel):
    model_config = ConfigDict(extra="forbid")

    premise: str | None = Field(default=None, min_length=1, max_length=4000)
    note: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def nonnull_premise(self) -> SeriesUpdates:
        if "premise" in self.model_fields_set and self.premise is None:
            raise ValueError("premise cannot be null")
        return self


class WorkPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slug: str = Field(pattern=SERIES_SLUG_PATTERN)
    expected_series_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    expected_documents_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    documents: list[SeriesDocSubmitIn] = Field(min_length=6, max_length=6)
    visual_tier: Literal["clips"]
    series_updates: SeriesUpdates | None = None

    @model_validator(mode="after")
    def no_verdict(self) -> WorkPlan:
        if any("judge" in doc.model_fields_set for doc in self.documents):
            raise ValueError("document judge is forbidden: this operation grants no approval")
        return self


class SyncPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1]
    source_git_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    works: list[WorkPlan] = Field(min_length=1, max_length=10)

    @model_validator(mode="after")
    def distinct_works(self) -> SyncPlan:
        if len({work.slug for work in self.works}) != len(self.works):
            raise ValueError("duplicate work slug")
        return self


async def sync_revisions(
    session: AsyncSession, bundle: dict[str, Any], *, actor: User | None = None
) -> list[dict[str, Any]]:
    """Preflight the entire batch, then append revisions; caller commits or rolls back.

    Dry runs neither lock nor flush caller state. Apply locks settings, then series
    in slug order, then their documents. Existing rows and decisions are retained.
    No scheduling, approval, request or media service is called.
    """
    plan = SyncPlan.model_validate(bundle)
    digest = bundle_hash(bundle)
    prepared: list[tuple[WorkPlan, VideoDramaSeries, list[VideoDramaDoc], dict[str, Any]]] = []
    reports: list[dict[str, Any]] = []
    with session.no_autoflush:
        settings_query = (
            select(VideoAutomationSettings)
            .where(VideoAutomationSettings.id == 1)
            .execution_options(populate_existing=True)
        )
        if actor is not None:
            from app.auth.service import user_is_suspended
            from app.config import get_settings

            settings_query = settings_query.with_for_update()
            current_actor = await session.scalar(
                select(User)
                .where(User.id == actor.id)
                # Block role revocation while allowing audit actor FK key-share locks.
                .with_for_update(read=True)
                .execution_options(populate_existing=True)
            )
            if (
                current_actor is None
                or not current_actor.is_active
                or current_actor.deleted_at is not None
                or user_is_suspended(current_actor)
                or not (
                    current_actor.is_admin
                    or current_actor.email.strip().casefold() in get_settings().admin_email_set
                )
            ):
                raise ValueError("an active administrator is required")
        settings = await session.scalar(settings_query)
        if settings is None or settings.drama_enabled:
            raise ValueError("drama_enabled must already be false; settings will not be changed")
        settings_before = bundle_hash(row_snapshot(settings))
        for work in sorted(plan.works, key=lambda entry: entry.slug):
            query = (
                select(VideoDramaSeries)
                .where(VideoDramaSeries.slug == work.slug)
                .execution_options(populate_existing=True)
            )
            if actor is not None:
                query = query.with_for_update()
            series = await session.scalar(query)
            if series is None:
                raise ValueError(f"{work.slug}: existing series is required")
            if series.kind != "series" or series.status != "setting" or series.hands_off:
                raise ValueError(f"{work.slug}: series must be setting with hands_off=false")
            docs_query = (
                select(VideoDramaDoc)
                .where(VideoDramaDoc.series_id == series.id)
                .order_by(VideoDramaDoc.kind, VideoDramaDoc.chapter_number, VideoDramaDoc.version)
                .execution_options(populate_existing=True)
            )
            if actor is not None:
                docs_query = docs_query.with_for_update()
            docs = list(await session.scalars(docs_query))
            if not docs or any(
                doc.status != "review"
                or doc.decided_at is not None
                or doc.decided_by_user_id is not None
                for doc in docs
            ):
                raise ValueError(f"{work.slug}: all existing documents must be undecided review")
            for model in (VideoDramaEpisode, VideoDramaRequest):
                if await session.scalar(
                    select(model.id).where(model.series_id == series.id).limit(1)
                ):
                    raise ValueError(f"{work.slug}: existing episodes or requests prohibit sync")
            pending = await session.scalar(
                select(VideoDramaMessage.id)
                .where(
                    VideoDramaMessage.series_id == series.id,
                    VideoDramaMessage.author == "owner",
                    VideoDramaMessage.answered_at.is_(None),
                )
                .limit(1)
            )
            if pending:
                raise ValueError(f"{work.slug}: pending owner discussion prohibits sync")
            keys = {(doc.kind, doc.chapter_number) for doc in work.documents}
            expected = {("setting", 0), ("outline", 0)} | {
                ("chapter", number)
                for number in range(
                    1, chapter_count(series.planned_episodes, series.episodes_per_chapter) + 1
                )
            }
            if keys != expected or len(keys) != len(work.documents):
                raise ValueError(
                    f"{work.slug}: expected setting, outline and every chapter exactly once"
                )
            if {(doc.kind, doc.chapter_number) for doc in docs} != expected:
                raise ValueError(f"{work.slug}: existing document keys differ")
            for doc in work.documents:
                problem = doc_problem(series, doc)
                if problem:
                    raise ValueError(f"{work.slug}/{doc.kind}:{doc.chapter_number}: {problem}")
            before = {
                "series_sha256": bundle_hash(row_snapshot(series)),
                "documents_sha256": documents_hash(docs),
            }
            audits = list(
                await session.scalars(
                    select(AdminAuditLog).where(
                        AdminAuditLog.action == ACTION,
                        AdminAuditLog.target == f"video-series:{work.slug}",
                    )
                )
            )
            previous = next(
                (audit for audit in audits if audit.metadata_json.get("bundle_sha256") == digest),
                None,
            )
            report = {
                "slug": work.slug,
                "action": "revise",
                "documents": len(work.documents),
                "before": before,
                "series_updates": {
                    "visual_tier": work.visual_tier,
                    **(
                        work.series_updates.model_dump(exclude_unset=True)
                        if work.series_updates is not None
                        else {}
                    ),
                },
            }
            if previous is not None:
                if previous.metadata_json.get("after") != before:
                    raise ValueError(f"{work.slug}: previously synchronized work has changed")
                report["action"] = "unchanged"
                reports.append(report)
                continue
            if before != {
                "series_sha256": work.expected_series_sha256,
                "documents_sha256": work.expected_documents_sha256,
            }:
                raise ValueError(
                    f"{work.slug}: expected snapshot hash differs; no works were synchronized"
                )
            prepared.append((work, series, docs, report))
            reports.append(report)
    if actor is None:
        return reports
    for work, series, docs, report in prepared:
        latest = {(doc.kind, doc.chapter_number): doc for doc in docs}
        revisions = []
        for payload in work.documents:
            old = latest[(payload.kind, payload.chapter_number)]
            revision = VideoDramaDoc(
                id=uuid4(),
                series_id=series.id,
                kind=payload.kind,
                chapter_number=payload.chapter_number,
                version=old.version + 1,
                body_md=payload.body_md,
                body_json=payload.body_json,
                status="review",
                note="製作設定與最新來源同步，尚未核准或啟動生成",
                created_at=datetime.now(UTC),
            )
            session.add(revision)
            revisions.append(
                {
                    "kind": payload.kind,
                    "chapter": payload.chapter_number,
                    "previous_id": str(old.id),
                    "id": str(revision.id),
                    "before_version": old.version,
                    "version": revision.version,
                }
            )
        patch = {"visual_tier": work.visual_tier}
        if work.series_updates is not None:
            patch.update(work.series_updates.model_dump(exclude_unset=True))
        for field, value in patch.items():
            setattr(series, field, value)
        series.updated_at = datetime.now(UTC)
        await session.flush()
        # Refresh database representations (including timezone behavior in SQLite tests)
        # before pinning the post-state used by an idempotent replay.
        await session.refresh(series)
        stored = list(
            await session.scalars(
                select(VideoDramaDoc)
                .where(VideoDramaDoc.series_id == series.id)
                .execution_options(populate_existing=True)
            )
        )
        after = {
            "series_sha256": bundle_hash(row_snapshot(series)),
            "documents_sha256": documents_hash(stored),
        }
        report["after"] = after
        report["revisions"] = revisions
        report["series_updates"] = patch
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action=ACTION,
                target=f"video-series:{work.slug}",
                metadata_json={
                    "source_git_sha": plan.source_git_sha,
                    "bundle_sha256": digest,
                    "before": report["before"],
                    "after": after,
                    "revisions": revisions,
                    "settings_sha256": settings_before,
                    "approval_granted": False,
                    "generation_started": False,
                    "series_updates": patch,
                },
            )
        )
    if bundle_hash(row_snapshot(settings)) != settings_before:
        raise ValueError("settings changed during synchronization")
    await session.flush()
    return reports


async def _run(args: argparse.Namespace, bundle: dict[str, Any]) -> None:
    digest = bundle_hash(bundle)
    if args.apply and args.expected_sha256 != digest:
        raise ValueError("--apply requires --expected-sha256 from this exact bundle's dry run")
    SyncPlan.model_validate(bundle)
    from app.config import get_settings
    from app.db import SessionFactory, engine
    from app.news_automation.sources_cli import admin_actor

    try:
        async with SessionFactory() as session, session.begin():
            if not args.apply and session.get_bind().dialect.name == "postgresql":
                await session.execute(text("SET TRANSACTION READ ONLY"))
            actor = None
            if args.apply:
                email = args.actor_email
                if not email:
                    emails = sorted(get_settings().admin_email_set)
                    if len(emails) != 1:
                        raise ValueError("select an active admin with --actor-email")
                    email = emails[0]
                actor = await admin_actor(session, email)
                if actor is None:
                    raise ValueError("an active administrator is required")
            reports = await sync_revisions(session, bundle, actor=actor)
        print(
            json.dumps(
                {"applied": args.apply, "sha256": digest, "works": reports},
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="reviewed plan; '-' reads stdin")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--actor-email")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if str(args.input) == "-" else args.input.read_text(encoding="utf-8")
        asyncio.run(_run(args, json.loads(raw)))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Sync refused: {error}\n")


if __name__ == "__main__":
    main()
