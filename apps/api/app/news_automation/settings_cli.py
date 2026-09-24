"""Show or change the news automation switch from the host.

    python -m app.news_automation.settings_cli                       # show, change nothing
    python -m app.news_automation.settings_cli --enable --writer-provider minimax \\
        --verifier-provider minimax                                   # dry run of a change
    python -m app.news_automation.settings_cli --enable ... --apply --actor-email <admin>

The same settings live on /admin/news; this exists for hosts where nobody can open the
admin page. Changes go through ``service.update_settings`` (audit row, activation-gate
rules), mode and auto-publish are never touched here, and the scanner is only switched
on when the writer and checker vendors have a key, neither is Gemini (its schema adapter
cannot express a news article yet), and Jev is configured -- otherwise every candidate
would fail after spending its Jev calls. Keys are reported as present or missing only.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, cast

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import Settings
from app.db import SessionFactory, engine
from app.models import User
from app.news_automation import service
from app.news_automation.models import NewsSource
from app.news_automation.schemas import ProviderName, SettingsWrite
from app.news_automation.sources_cli import admin_actor

PROVIDERS: tuple[ProviderName, ...] = ("openai", "anthropic", "minimax", "gemini")
# Gemini's responseSchema adapter keeps one option of every union (follow-up task
# 2026-09-24-let-gemini-serve-news-stages-without).
UNSUPPORTED_FOR_NEWS = frozenset({"gemini"})


def readiness(runtime: Settings) -> dict[str, bool]:
    keys = {
        "openai": runtime.openai_api_key,
        "anthropic": runtime.anthropic_api_key,
        "minimax": runtime.minimax_api_key,
        "gemini": runtime.hotspot_guide_gemini_api_key,
    }
    return {**{name: bool(value) for name, value in keys.items()}, "jev": runtime.jev_configured}


def blockers(payload: SettingsWrite, ready: dict[str, bool]) -> list[str]:
    if not payload.enabled:
        return []
    problems: list[str] = []
    for role in ("writer", "verifier"):
        vendor = cast(str, getattr(payload, f"{role}_provider"))
        if vendor in UNSUPPORTED_FOR_NEWS:
            problems.append(f"{role} vendor {vendor} cannot write a news article yet")
        elif not ready.get(vendor):
            problems.append(f"{role} vendor {vendor} has no API key configured")
    if not ready["jev"]:
        problems.append("Jev is not configured (its key is in the admin AI vendor card)")
    return problems


async def _source_counts(session: AsyncSession) -> dict[str, int]:
    total = int(await session.scalar(select(func.count()).select_from(NewsSource)) or 0)
    enabled = int(
        await session.scalar(
            select(func.count()).select_from(NewsSource).where(NewsSource.enabled.is_(True))
        )
        or 0
    )
    return {"total": total, "enabled": enabled}


async def run(
    *,
    enable: bool | None,
    writer_provider: str | None,
    writer_model: str | None,
    verifier_provider: str | None,
    verifier_model: str | None,
    apply: bool,
    actor_email: str | None,
) -> dict[str, Any]:
    try:
        async with SessionFactory() as session:
            view = await service.settings_view(session)
            runtime = await load_runtime_settings(session)
            ready = readiness(runtime)
            current = SettingsWrite.model_validate(
                view.model_dump(include=set(SettingsWrite.model_fields))
            )
            overrides: dict[str, Any] = {}
            if enable is not None:
                overrides["enabled"] = enable
            for key, value in (
                ("writer_provider", writer_provider),
                ("writer_model", writer_model),
                ("verifier_provider", verifier_provider),
                ("verifier_model", verifier_model),
            ):
                if value is not None:
                    # An empty string means "back to the vendor default".
                    overrides[key] = value or None
            wanted = SettingsWrite.model_validate({**current.model_dump(), **overrides})
            changes = {
                key: value
                for key, value in wanted.model_dump().items()
                if getattr(current, key) != value
            }
            problems = blockers(wanted, ready)
            report: dict[str, Any] = {
                "settings": {
                    key: getattr(view, key)
                    for key in (
                        "enabled",
                        "mode",
                        "writer_provider",
                        "writer_model",
                        "verifier_provider",
                        "verifier_model",
                        "auto_publish_ai",
                        "auto_publish_tech",
                        "auto_publish_crypto",
                    )
                },
                "default_models": view.default_models,
                "keys_configured": ready,
                "sources": await _source_counts(session),
                "changes": changes,
                "blockers": problems,
                "applied": False,
            }
            if not changes or not apply:
                return report
            if problems:
                raise SystemExit("Refusing to apply: " + "; ".join(problems))
            if not actor_email:
                raise SystemExit("--actor-email is required with --apply")
            actor: User | None = await admin_actor(session, actor_email)
            if actor is None:
                raise SystemExit("The actor must be an active administrator")
            session.expunge(actor)
            updated = await service.update_settings(session, actor, wanted)
            report["applied"] = True
            report["settings"] = {key: getattr(updated, key) for key in report["settings"]}
            return report
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    switch = parser.add_mutually_exclusive_group()
    switch.add_argument("--enable", dest="enable", action="store_true", default=None)
    switch.add_argument("--disable", dest="enable", action="store_false")
    parser.add_argument("--writer-provider", choices=PROVIDERS)
    parser.add_argument("--writer-model", help="Model id; an empty string restores the default")
    parser.add_argument("--verifier-provider", choices=PROVIDERS)
    parser.add_argument("--verifier-model", help="Model id; an empty string restores the default")
    parser.add_argument("--apply", action="store_true", help="Write; show the change otherwise")
    parser.add_argument("--actor-email", help="Administrator the audit row is recorded for")
    args = parser.parse_args()
    report = asyncio.run(
        run(
            enable=args.enable,
            writer_provider=args.writer_provider,
            writer_model=args.writer_model,
            verifier_provider=args.verifier_provider,
            verifier_model=args.verifier_model,
            apply=args.apply,
            actor_email=args.actor_email,
        )
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()

