"""Load the reviewed news sources in ``sources.json`` into the database.

    python -m app.news_automation.sources_cli            # dry run: validate, write nothing
    python -m app.news_automation.sources_cli --apply --actor-email owner@example.com

The file is the source of truth for what the hourly scanner reads; /admin/news can still
disable or edit a source afterwards. Every write goes through the same service calls as
the admin page, so an enabled source must pass the fetch-and-parse validation from this
host, and each change leaves an audit row for the actor. A source that fails validation
is still recorded, disabled, with the reason, so the list shows what was tried. Sources in
the database but not in the file are reported and left alone.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import SessionFactory, engine
from app.models import User
from app.news_automation import service
from app.news_automation.models import NewsSource
from app.news_automation.schemas import SourcePatch, SourceWrite
from app.news_automation.validation import validate_source_configuration
from app.problems import AppError

DEFAULT_FILE = Path(__file__).with_name("sources.json")
# Fields the file owns; the scan state (etag, last_status, ...) belongs to the scanner.
MANAGED_FIELDS = (
    "name",
    "format",
    "role",
    "vertical",
    "is_first_party",
    "enabled",
    "scan_interval_minutes",
    "allowed_redirect_hosts",
    "config",
)


def load_file(path: Path) -> list[SourceWrite]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows: list[SourceWrite] = []
    for index, raw in enumerate(payload["sources"]):
        values = {key: value for key, value in raw.items() if key != "note"}
        try:
            rows.append(SourceWrite.model_validate(values))
        except ValidationError as error:
            raise SystemExit(f"{path}: source #{index + 1} is invalid: {error}") from error
    urls = [row.url for row in rows]
    if len(urls) != len(set(urls)):
        raise SystemExit(f"{path}: a source URL is listed twice")
    return rows


def _current(row: NewsSource) -> dict[str, Any]:
    return {
        "name": row.name,
        "format": row.format,
        "role": row.role,
        "vertical": row.vertical,
        "is_first_party": row.is_first_party,
        "enabled": row.enabled,
        "scan_interval_minutes": row.scan_interval_minutes,
        "allowed_redirect_hosts": list(row.allowed_redirect_hosts_json or []),
        "config": dict(row.config_json or {}),
    }


async def _actor(session: AsyncSession, email: str) -> User | None:
    """An active administrator, or an owner listed in ADMIN_EMAILS (as the admin bootstrap
    treats them even when users.is_admin was never backfilled)."""
    normalized = email.strip().casefold()
    user: User | None = await session.scalar(
        select(User).where(func.lower(User.email) == normalized)
    )
    if user is None or not user.is_active:
        return None
    return user if user.is_admin or normalized in get_settings().admin_email_set else None


async def _dry_run_error(wanted: SourceWrite) -> str | None:
    if not wanted.enabled:
        return None
    probe = NewsSource(
        name=wanted.name,
        url=wanted.url,
        format=wanted.format,
        role=wanted.role,
        vertical=wanted.vertical,
        is_first_party=wanted.is_first_party,
        allowed_redirect_hosts_json=wanted.allowed_redirect_hosts,
        config_json=wanted.config,
    )
    try:
        await validate_source_configuration(probe)
    except AppError as error:
        return error.detail
    return None


async def _record_refusal(session: AsyncSession, source_id: Any, detail: str) -> None:
    row = await session.get(NewsSource, source_id)
    if row is not None:
        row.last_status = "validation_failed"
        row.last_error = detail[:4000]
        await session.commit()


async def import_sources(
    session: AsyncSession, rows: list[SourceWrite], *, actor: User | None
) -> dict[str, Any]:
    """Dry run when ``actor`` is None; otherwise create or update every listed source."""

    # Plain snapshots, not ORM rows: a refused validation rolls the session back, which
    # expires every loaded row, and reading one afterwards would be blocking IO.
    existing = {
        row.url: (row.id, _current(row)) for row in await session.scalars(select(NewsSource))
    }
    listed = {row.url for row in rows}
    results: list[dict[str, Any]] = []
    for wanted in rows:
        current_id, stored = existing.get(wanted.url, (None, None))
        desired = wanted.model_dump(include=set(MANAGED_FIELDS))
        changes = (
            {key: value for key, value in desired.items() if stored[key] != value}
            if stored is not None
            else desired
        )
        action = "create" if stored is None else ("update" if changes else "unchanged")
        result: dict[str, Any] = {"name": wanted.name, "url": wanted.url, "action": action}
        if actor is None:
            error = await _dry_run_error(wanted)
            result["valid"] = error is None
            if error:
                result["error"] = error
            results.append(result)
            continue
        if stored is not None and action == "unchanged":
            result["enabled"] = stored["enabled"]
            results.append(result)
            continue
        try:
            if current_id is None:
                view = await service.create_source(session, actor, wanted)
            else:
                view = await service.update_source(
                    session, actor, current_id, SourcePatch.model_validate(changes)
                )
            result["enabled"] = view.enabled
        except AppError as error:
            if error.code not in {
                "news_source_unreadable",
                "news_source_detail_unreadable",
                "news_source_validation_failed",
            }:
                raise
            # Keep the definition, switched off, so the admin list shows the attempt.
            fallback = changes | {"enabled": False}
            if current_id is None:
                view = await service.create_source(
                    session, actor, wanted.model_copy(update={"enabled": False})
                )
            else:
                view = await service.update_source(
                    session, actor, current_id, SourcePatch.model_validate(fallback)
                )
            await _record_refusal(session, view.id, error.detail)
            result["enabled"] = False
            result["error"] = error.detail
        results.append(result)
    unlisted = sorted(url for url in existing if url not in listed)
    return {
        "applied": actor is not None,
        "sources": results,
        "not_in_file": unlisted,
        "summary": {
            "create": sum(1 for item in results if item["action"] == "create"),
            "update": sum(1 for item in results if item["action"] == "update"),
            "unchanged": sum(1 for item in results if item["action"] == "unchanged"),
            "failed_validation": sum(1 for item in results if item.get("error")),
        },
    }


async def run(path: Path, *, apply: bool, actor_email: str | None) -> dict[str, Any]:
    rows = load_file(path)
    try:
        async with SessionFactory() as session:
            actor = None
            if apply:
                if not actor_email:
                    raise SystemExit("--actor-email is required with --apply")
                actor = await _actor(session, actor_email)
                if actor is None:
                    raise SystemExit("The actor must be an active administrator")
                # Detached, its loaded id survives the rollback a refused source causes.
                session.expunge(actor)
            return await import_sources(session, rows, actor=actor)
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--apply", action="store_true", help="Write; dry run otherwise")
    parser.add_argument("--actor-email", help="Administrator the audit rows are recorded for")
    args = parser.parse_args()
    report = asyncio.run(run(args.file, apply=args.apply, actor_email=args.actor_email))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
