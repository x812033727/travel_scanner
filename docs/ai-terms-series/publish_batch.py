"""Driver for the reviewed 83-article zh-TW bundle; no automatic execution.

Run inside the deployed API container, one phase per invocation:
  python publish_batch.py --manifest /bundle/release-manifest.json \\
    --manifest-sha256 <reviewed SHA256> --public-dir /bundle/public \\
    --state-dir /durable/ai-terms-20260914 dry-run
Repeat identical arguments with drafts, publish-articles, then publish-index.
The public directory holds the reviewed assets; packs come from the installed API.
Keep state-dir on durable storage. Never reset its journal to bypass a refusal.

Uses existing load_packs/plan_import/apply_import and their per-article commits.
Every accepted pack has default create flags and existing taxonomy must already
match, so each planned article performs at most one write/commit in each phase.
New drafts stay private; existing publications remain until their publish phase.
A journal intent precedes each write. Resume checks the exact expected revision,
content, actor and all other pinned rows before recording an uncertain success.
No SSH, API/schema changes, actor email output, hidden rollback or bulk approval.

A session-level PostgreSQL advisory lock excludes cooperating publishers. Each
write uses SERIALIZABLE isolation from its guard read through the existing commit;
ordinary editor conflicts fail instead of overwriting a newer draft. All target
rows/locales are compared before and after each article. Failures stop the run.
The local SQLite test is state-machine evidence, not PostgreSQL race validation.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from app.config import get_settings
from app.db import engine
from app.guides.content_pack import (
    apply_import,
    default_directory,
    load_packs,
    plan_import,
)
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.schemas import GuideDocument
from app.guides.service import _topics_for, document_hash
from app.models import User
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

LOCALE = "zh-TW"
INDEX = "ai-terms-index"
SLUGS = (
    "ai-term-prompt-engineering",
    "ai-term-context-engineering",
    "ai-term-harness-engineering",
    "ai-term-loop-engineering",
    "ai-term-agentic-engineering",
    "ai-term-vibe-coding",
    "ai-term-spec-driven-development",
    "ai-term-llmops",
    "ai-term-agentops",
    "ai-term-prompt-chaining",
    "ai-term-artificial-intelligence",
    "ai-term-machine-learning",
    "ai-term-deep-learning",
    "ai-term-generative-ai",
    "what-is-a-large-language-model",
    "ai-term-foundation-model",
    "ai-term-transformer",
    "ai-term-mixture-of-experts",
    "ai-term-small-language-model",
    "ai-term-model-parameters",
    "ai-term-token",
    "ai-term-tokenization",
    "ai-context-window-explained",
    "ai-term-system-prompt",
    "ai-term-few-shot-prompting",
    "ai-term-zero-shot-prompting",
    "ai-term-in-context-learning",
    "ai-term-context-compaction",
    "ai-term-context-rot",
    "ai-term-agent-memory",
    "ai-agents-explained",
    "ai-term-agent-loop",
    "ai-term-multi-agent-system",
    "ai-term-subagent",
    "ai-term-agent-orchestration",
    "ai-term-react-reasoning-acting",
    "ai-term-tool-calling",
    "ai-term-model-context-protocol",
    "ai-term-agent2agent-protocol",
    "ai-term-agent-skills",
    "ai-term-retrieval-augmented-generation",
    "ai-term-agentic-rag",
    "ai-term-graph-rag",
    "ai-term-embedding",
    "ai-term-vector-database",
    "ai-term-semantic-search",
    "ai-term-hybrid-search",
    "ai-term-reranking",
    "ai-term-chunking",
    "ai-term-knowledge-graph",
    "ai-term-pretraining",
    "ai-term-fine-tuning",
    "ai-term-supervised-fine-tuning",
    "ai-term-rlhf",
    "ai-term-direct-preference-optimization",
    "ai-term-lora",
    "ai-term-knowledge-distillation",
    "ai-term-quantization",
    "ai-reasoning-models-explained",
    "ai-term-test-time-compute",
    "ai-term-prompt-caching",
    "ai-term-evals",
    "ai-term-benchmark",
    "ai-term-llm-as-a-judge",
    "ai-hallucination-fact-check",
    "ai-term-prompt-injection",
    "ai-term-jailbreak",
    "ai-term-guardrails",
    "ai-term-sandbox",
    "ai-term-human-in-the-loop",
    "ai-term-red-teaming",
    "ai-term-multimodal-ai",
    "ai-term-diffusion-model",
    "ai-term-text-to-image",
    "ai-term-text-to-video",
    "ai-term-automatic-speech-recognition",
    "ai-term-text-to-speech",
    "ai-term-deepfake",
    "ai-term-open-weights",
    "ai-term-open-source-ai",
    "ai-term-content-credentials",
    "ai-glossary-50-terms",
    "ai-terms-index",
)
UPDATED = {
    "what-is-a-large-language-model",
    "ai-context-window-explained",
    "ai-agents-explained",
    "ai-reasoning-models-explained",
    "ai-hallucination-fact-check",
    "ai-glossary-50-terms",
}
NEW = set(SLUGS) - UPDATED
PHASES = ("dry-run", "drafts", "publish-articles", "publish-index")
PACK_PREFIX = "apps/api/app/guides/content/"
ASSET_PREFIX = "apps/web/public/"
LOCK_KEY = 817420260914
assert len(SLUGS) == len(set(SLUGS)) == 83 and len(NEW) == 77


class Refused(RuntimeError):
    """Operator-readable failure containing no document text or credentials."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Refused(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()


def stamp() -> str:
    return datetime.now(UTC).isoformat()


def safe_path(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    require(
        not rel.is_absolute() and ".." not in rel.parts and "\\" not in relative,
        "Manifest contains an unsafe path",
    )
    path = (root / str(rel)).resolve()
    require(path.is_relative_to(root.resolve()), "Manifest path escapes its root")
    return path


def verify_bundle(manifest_path: Path, pinned_sha: str, public_dir: Path):
    """Read only exact allowlisted pack bytes; load_packs validates a temporary snapshot."""
    raw_manifest = manifest_path.read_bytes()
    require(
        sha(raw_manifest) == pinned_sha, "Manifest SHA256 differs from reviewed value"
    )
    manifest = json.loads(raw_manifest)
    require(
        manifest.get("locale") == LOCALE and manifest.get("index_last") == INDEX,
        "Unexpected locale or index",
    )
    require(
        len(manifest.get("slugs", [])) == 83 and set(manifest["slugs"]) == set(SLUGS),
        "Manifest must contain exactly the reviewed 83 slugs",
    )
    require(
        len(manifest.get("new_slugs", [])) == 77 and set(manifest["new_slugs"]) == NEW,
        "Unexpected new-slug classification",
    )
    require(
        len(manifest.get("updated_slugs", [])) == 6
        and set(manifest["updated_slugs"]) == UPDATED,
        "Unexpected existing-slug classification",
    )
    files = manifest.get("files", {})
    require(isinstance(files, dict), "Manifest files must be a hash mapping")
    expected_files = set()
    with tempfile.TemporaryDirectory(prefix="ai-terms-verified-") as tmp:
        for slug in SLUGS:
            key = PACK_PREFIX + slug + ".json"
            data = (default_directory() / (slug + ".json")).read_bytes()
            require(
                files.get(key) == sha(data), f"{slug}: deployed pack SHA256 mismatch"
            )
            (Path(tmp) / (slug + ".json")).write_bytes(data)
            expected_files.add(key)
        packs = load_packs(Path(tmp), slugs=set(SLUGS))
    for pack in packs:
        require(set(pack.locales) == {LOCALE}, f"{pack.slug}: unexpected pack locale")
        require(pack.kind == "life", f"{pack.slug}: unexpected kind")
        require(
            not pack.featured and pack.display_order == 100,
            f"{pack.slug}: non-default create flags need a separately reviewed driver",
        )
        doc = pack.locales[LOCALE]
        assets = ([doc.hero.src] if doc.hero else []) + [
            block.src for block in doc.blocks if block.type == "image"
        ]
        require(bool(doc.hero), f"{pack.slug}: missing hero")
        for src in assets:
            require(
                src.startswith("/guides/"), f"{pack.slug}: unexpected asset location"
            )
            key = ASSET_PREFIX + src.lstrip("/")
            path = safe_path(public_dir, src.lstrip("/"))
            require(
                files.get(key) == sha(path.read_bytes()),
                f"{pack.slug}: asset SHA256 mismatch",
            )
            expected_files.add(key)
    require(
        set(files) == expected_files, "Manifest contains missing or unrelated files"
    )
    return {pack.slug: pack for pack in packs}


@contextmanager
def journal_lock(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ".lock"
    with path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as error:
                raise Refused("Another publisher holds the journal lock") from error
        else:
            import fcntl

            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as error:
                raise Refused("Another publisher holds the journal lock") from error
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def persist(path: Path, value: dict) -> None:
    """Atomic, durable journal; never prints actor or database credentials."""
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        if os.name != "nt":
            os.fchmod(handle.fileno(), 0o600)
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    if os.name != "nt":
        fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


async def snapshot(session: AsyncSession, *, lock: bool = False) -> dict:
    article_query = (
        select(GuideArticle)
        .where(GuideArticle.slug.in_(SLUGS))
        .order_by(GuideArticle.id)
    )
    if lock:
        article_query = article_query.with_for_update(nowait=True)
    articles = list(
        await session.scalars(article_query.execution_options(populate_existing=True))
    )
    ids = [article.id for article in articles]
    locale_query = (
        select(GuideArticleLocale)
        .where(GuideArticleLocale.article_id.in_(ids))
        .order_by(GuideArticleLocale.id)
    )
    if lock:
        locale_query = locale_query.with_for_update(nowait=True)
    locales = list(
        await session.scalars(locale_query.execution_options(populate_existing=True))
    )
    topics = await _topics_for(session, ids)
    # Only current/published revisions are needed; never export document text.
    versions = {row.id: {row.version, row.published_version} for row in locales}
    revisions = {
        (rev.article_locale_id, rev.version): rev
        for rev in await session.scalars(
            select(GuideArticleRevision).where(
                GuideArticleRevision.article_locale_id.in_(versions)
            )
        )
        if rev.version in versions[rev.article_locale_id]
    }
    result = dict.fromkeys(SLUGS)
    for article in articles:
        row = {
            "id": str(article.id),
            "version": article.version,
            "kind": article.kind,
            "destination_id": article.destination_id,
            "valid_until": str(article.valid_until) if article.valid_until else None,
            "featured": article.featured,
            "display_order": article.display_order,
            "is_active": article.is_active,
            "updated_at": article.updated_at.isoformat(),
            "topics": sorted(item.slug for item in topics.get(article.id, [])),
            "locales": {},
        }
        for item in locales:
            if item.article_id != article.id:
                continue
            latest = revisions.get((item.id, item.version))
            require(latest is not None, f"{article.slug}: missing current revision")
            live_hash = None
            if item.published_version is not None:
                live = revisions.get((item.id, item.published_version))
                require(
                    live is not None and live.action == "published",
                    f"{article.slug}: damaged published revision pointer",
                )
                live_hash = document_hash(
                    GuideDocument.model_validate(live.document_json).model_dump(
                        mode="json"
                    )
                )
            row["locales"][item.locale] = {
                "id": str(item.id),
                "version": item.version,
                "published_version": item.published_version,
                "published_at": item.published_at.isoformat()
                if item.published_at
                else None,
                "updated_at": item.updated_at.isoformat(),
                "draft_sha256": document_hash(
                    GuideDocument.model_validate(item.draft_json).model_dump(
                        mode="json"
                    )
                ),
                "published_sha256": live_hash,
                "latest_action": latest.action,
                "latest_actor": str(latest.created_by_user_id),
            }
        result[article.slug] = row
    return result


def validate_initial(state: dict) -> None:
    for slug in SLUGS:
        row = state[slug]
        if slug in NEW:
            require(
                row is None,
                f"{slug}: expected absent; existing draft/article is unapproved",
            )
            continue
        require(
            row is not None and row["is_active"] and row["kind"] == "life",
            f"{slug}: expected active existing life article",
        )
        require(
            row["valid_until"] is None
            or row["valid_until"] >= datetime.now(UTC).date().isoformat(),
            f"{slug}: existing article expired",
        )
        locale = row["locales"].get(LOCALE)
        require(
            locale is not None and locale["published_version"] is not None,
            f"{slug}: expected existing zh-TW publication",
        )
        require(
            locale["version"] == locale["published_version"]
            and locale["draft_sha256"] == locale["published_sha256"],
            f"{slug}: unexpected unpublished draft; stop for separate editorial review",
        )


def same_state(actual: dict, expected: dict) -> None:
    changed = [slug for slug in SLUGS if actual[slug] != expected[slug]]
    require(not changed, "Concurrent/unexpected change: " + ", ".join(changed))


def require_public(state: dict, packs: dict, slugs) -> None:
    for slug in slugs:
        article = state[slug]
        require(article is not None and article["is_active"], f"{slug}: not active")
        require(
            article["valid_until"] is None
            or article["valid_until"] >= datetime.now(UTC).date().isoformat(),
            f"{slug}: publication expired",
        )
        row = article["locales"].get(LOCALE)
        wanted = document_hash(packs[slug].locales[LOCALE].model_dump(mode="json"))
        require(
            row is not None
            and row["published_sha256"] == wanted
            and row["draft_sha256"] == wanted
            and row["published_version"] == row["version"],
            f"{slug}: publication does not match the exact reviewed document",
        )


def accept_transition(before: dict, after: dict, intent: dict, packs: dict) -> None:
    """Only the intended one-commit transition may differ from the previous snapshot."""
    slug = intent["slug"]
    for other in SLUGS:
        if other != slug:
            require(
                after[other] == before[other], f"{other}: concurrent/unexpected change"
            )
    old, row = before[slug], after[slug]
    require(row is not None, f"{slug}: expected result is absent")
    require(
        {k: v for k, v in row["locales"].items() if k != LOCALE}
        == ({k: v for k, v in old["locales"].items() if k != LOCALE} if old else {}),
        f"{slug}: unrelated locale changed",
    )
    wanted = document_hash(packs[slug].locales[LOCALE].model_dump(mode="json"))
    locale = row["locales"][LOCALE]
    require(locale["draft_sha256"] == wanted, f"{slug}: unexpected draft content")
    if intent["action"] == "unchanged":
        require(row == old, f"{slug}: expected no database write")
        return
    require(
        locale["latest_action"] == intent["action"]
        and locale["latest_actor"] == intent["actor_id"],
        f"{slug}: unexpected revision action or author",
    )
    require(
        locale["version"] == (old["locales"][LOCALE]["version"] + 1 if old else 1),
        f"{slug}: unexpected revision count",
    )
    if old:
        require(
            {k: v for k, v in row.items() if k != "locales"}
            == {k: v for k, v in old.items() if k != "locales"},
            f"{slug}: taxonomy/identity changed",
        )
        require(
            locale["id"] == old["locales"][LOCALE]["id"],
            f"{slug}: locale identity changed",
        )
    else:
        pack = packs[slug]
        expected = {
            "version": 1,
            "kind": pack.kind,
            "destination_id": pack.destination_id,
            "valid_until": str(pack.valid_until) if pack.valid_until else None,
            "featured": pack.featured,
            "display_order": pack.display_order,
            "is_active": True,
            "topics": sorted(pack.topics),
        }
        require(
            all(row[key] == value for key, value in expected.items()),
            f"{slug}: new article taxonomy differs",
        )
    if intent["phase"] == "drafts":
        if old:
            require(
                all(
                    locale[key] == old["locales"][LOCALE][key]
                    for key in ("published_version", "published_at", "published_sha256")
                ),
                f"{slug}: draft changed existing public content",
            )
        else:
            require(
                locale["published_version"] is None and locale["published_at"] is None,
                f"{slug}: new draft became public",
            )
    else:
        require_public(after, packs, [slug])
        if old["locales"][LOCALE]["published_at"] is not None:
            require(
                locale["published_at"] == old["locales"][LOCALE]["published_at"],
                f"{slug}: first-publication timestamp changed",
            )


def selected_slugs(phase: str) -> list[str]:
    return (
        list(SLUGS)
        if phase == "drafts"
        else [slug for slug in SLUGS if slug != INDEX]
        if phase == "publish-articles"
        else [INDEX]
    )


async def active_actor(session: AsyncSession) -> User:
    # Same configured-owner allowance as app.cli._env_owner; email stays internal.
    allowed = get_settings().admin_email_set
    require(bool(allowed), "No configured administrator available")
    actor = await session.scalar(
        select(User)
        .where(func.lower(User.email).in_(allowed), User.is_active.is_(True))
        .order_by(User.id)
        .limit(1)
    )
    require(actor is not None, "No active configured administrator available")
    return actor


def complete_intent(journal: dict, state: dict, result: dict, path: Path) -> None:
    intent = journal["pending"]
    journal["expected"] = state
    journal["done"][intent["phase"]].append(intent["slug"])
    journal["history"].append(
        {
            "phase": intent["phase"],
            "slug": intent["slug"],
            "locale": LOCALE,
            "at": stamp(),
            **result,
        }
    )
    journal["pending"] = None
    persist(path, journal)


def reconcile(journal: dict, actual: dict, path: Path, packs: dict) -> None:
    pending = journal.get("pending")
    if pending is None:
        same_state(actual, journal["expected"])
        return
    if actual == journal["expected"]:
        journal["history"].append(
            {
                "phase": pending["phase"],
                "slug": pending["slug"],
                "locale": LOCALE,
                "at": stamp(),
                "status": "not_written_reconciled",
            }
        )
        journal["pending"] = None
        persist(path, journal)
    else:
        accept_transition(journal["expected"], actual, pending, packs)
        complete_intent(journal, actual, {"status": "committed_reconciled"}, path)


async def execute_phase(
    args, packs: dict, journal_path: Path, db_engine=engine
) -> dict:
    """Existing per-article commits; called only while holding the journal file lock."""
    async with db_engine.connect() as connection:
        postgres = connection.dialect.name == "postgresql"
        if postgres:
            await connection.execution_options(isolation_level="SERIALIZABLE")
            got_lock = await connection.scalar(
                text("SELECT pg_try_advisory_lock(:key)"), {"key": LOCK_KEY}
            )
            await connection.commit()
            require(bool(got_lock), "Another AI-terms publisher is running")
        journal = None
        try:
            async with AsyncSession(bind=connection, expire_on_commit=False) as session:
                current = await snapshot(session)
                if journal_path.exists():
                    journal = json.loads(journal_path.read_text("utf-8"))
                    require(
                        journal.get("schema") == 1
                        and journal.get("manifest_sha256") == args.manifest_sha256,
                        "Journal belongs to a different reviewed bundle",
                    )
                    require(
                        journal.get("locale") == LOCALE
                        and journal.get("slugs") == list(SLUGS),
                        "Unexpected journal scope",
                    )
                    reconcile(journal, current, journal_path, packs)
                else:
                    require(
                        args.phase == "dry-run",
                        "Run dry-run first with a fresh durable journal",
                    )
                    validate_initial(current)
                    journal = {
                        "schema": 1,
                        "manifest_sha256": args.manifest_sha256,
                        "locale": LOCALE,
                        "slugs": list(SLUGS),
                        "created_at": stamp(),
                        "dry_run": False,
                        "expected": current,
                        "history": [],
                        "pending": None,
                        "done": {phase: [] for phase in PHASES[1:]},
                    }
                full_plan = await plan_import(
                    session, [packs[s] for s in SLUGS], locales={LOCALE}
                )
                require(len(full_plan.articles) == 83, "Incomplete import plan")
                # Refuse unexpected taxonomy edits; this driver imports documents only for old rows.
                for entry in full_plan.articles:
                    if current[entry.pack.slug] is not None:
                        require(
                            entry.taxonomy == "unchanged",
                            f"{entry.pack.slug}: taxonomy differs; review outside this driver",
                        )
                if args.phase == "dry-run":
                    journal["dry_run"] = True
                    journal["history"].append(
                        {
                            "phase": "dry-run",
                            "status": "read_only",
                            "at": stamp(),
                            "results": full_plan.as_dict()["articles"],
                        }
                    )
                    persist(journal_path, journal)
                    return {"phase": "dry-run", "status": "read_only", "articles": 83}
                require(journal["dry_run"], "Missing successful dry-run")
                for earlier in PHASES[1 : PHASES.index(args.phase)]:
                    require(
                        journal["done"][earlier] == selected_slugs(earlier),
                        f"Complete {earlier} before {args.phase}",
                    )
                if args.phase == "publish-index":
                    require_public(
                        current, packs, [slug for slug in SLUGS if slug != INDEX]
                    )
                # End the preflight read transaction. Each article starts with fresh guarded reads.
                await session.rollback()
                for slug in selected_slugs(args.phase):
                    if slug in journal["done"][args.phase]:
                        continue
                    verify_bundle(args.manifest, args.manifest_sha256, args.public_dir)
                    if postgres:
                        await session.execute(text("SET LOCAL lock_timeout = '5s'"))
                    # One existing publish commit releases these locks. This prevents an
                    # editor withdrawing any of the 82 dependencies before index commit.
                    before = await snapshot(session, lock=args.phase == "publish-index")
                    same_state(before, journal["expected"])
                    if args.phase == "publish-index":
                        require_public(
                            before, packs, [other for other in SLUGS if other != INDEX]
                        )
                    actor = await active_actor(session)
                    plan = await plan_import(session, [packs[slug]], locales={LOCALE})
                    entry = plan.articles[0]
                    require(
                        entry.taxonomy in ("create", "unchanged"),
                        f"{slug}: unexpected taxonomy update",
                    )
                    item = entry.locales[0]
                    if args.phase != "drafts":
                        require(
                            item.action == "unchanged",
                            f"{slug}: reviewed draft is not ready",
                        )
                    action = (
                        (
                            "created"
                            if item.action == "create"
                            else "draft_saved"
                            if item.action == "update"
                            else "unchanged"
                        )
                        if args.phase == "drafts"
                        else ("published" if item.publish else "unchanged")
                    )
                    journal["pending"] = {
                        "phase": args.phase,
                        "slug": slug,
                        "at": stamp(),
                        "action": action,
                        "actor_id": str(actor.id),
                    }
                    persist(journal_path, journal)
                    report = await apply_import(
                        session, actor, plan, publish=args.phase != "drafts"
                    )
                    require(report.failed is None, f"{slug}: admin write path refused")
                    # apply_import has committed its one write; start a fresh post-write view.
                    await session.rollback()
                    after = await snapshot(session)
                    accept_transition(before, after, journal["pending"], packs)
                    complete_intent(
                        journal,
                        after,
                        {
                            "status": "committed"
                            if action != "unchanged"
                            else "unchanged",
                            "report": report.as_dict(),
                        },
                        journal_path,
                    )
                    await session.rollback()
                final = await snapshot(session)
                same_state(final, journal["expected"])
                if args.phase == "publish-index":
                    require_public(final, packs, SLUGS)
                return {
                    "phase": args.phase,
                    "status": "complete",
                    "articles": len(journal["done"][args.phase]),
                }
        except Exception as error:
            if journal is not None:
                pending = journal.get("pending") or {}
                journal["history"].append(
                    {
                        "phase": args.phase,
                        "slug": pending.get("slug"),
                        "at": stamp(),
                        "status": "stopped",
                        "error_type": type(error).__name__,
                        "reason": str(error)
                        if isinstance(error, Refused)
                        else type(error).__name__,
                    }
                )
                persist(journal_path, journal)
            raise
        finally:
            await connection.rollback()
            if postgres:
                await connection.execute(
                    text("SELECT pg_advisory_unlock(:key)"), {"key": LOCK_KEY}
                )
                await connection.commit()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--public-dir", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("phase", choices=PHASES)
    args = parser.parse_args(argv)
    try:
        require(
            bool(re.fullmatch(r"[0-9a-f]{64}", args.manifest_sha256)),
            "Supply the reviewed lower-case manifest SHA256",
        )
        require(
            engine.dialect.name == "postgresql", "Production CLI requires PostgreSQL"
        )
        packs = verify_bundle(args.manifest, args.manifest_sha256, args.public_dir)
        with journal_lock(args.state_dir):
            result = asyncio.run(
                execute_phase(args, packs, args.state_dir / "journal.json")
            )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Refused as error:
        print(json.dumps({"status": "stopped", "reason": str(error)}), file=sys.stderr)
        return 1
    except Exception as error:  # noqa: BLE001 - avoid leaking DB parameters to operator output
        # DB exceptions can contain SQL parameters, documents and actor details. Never print them.
        print(
            json.dumps(
                {
                    "status": "stopped",
                    "reason": type(error).__name__,
                    "next": "Review journal; no automatic retry. Rerun the same phase only "
                    "after resolving the cause. An uncertain commit is reconciled.",
                }
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
