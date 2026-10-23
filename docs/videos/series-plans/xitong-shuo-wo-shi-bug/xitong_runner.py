"""Put 《系統說我是 BUG》 on the site from inside the API container, as the admin would.

Commands (python /tmp/xitong_runner.py <cmd> ...):
  status                       the series' status, documents and episodes
  create <bundle.json>         create the series row from bundle["series"]
  fill <bundle.json> [minutes] wait for each planned document's first version, replace it with
                               the authored one (approved), then switch the series to hands-off
                               and series_auto_continue on; gives up after <minutes> (default 150)
  continue-on                  only set series_auto_continue = true
Every call opens its own session; nothing here runs a model or spends media budget.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from typing import Any

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation.sources_cli import admin_actor
from app.video_automation import series as drama
from app.video_automation.schemas import SeriesDocEditIn, SeriesDocSubmitIn, SeriesIn, SeriesPatch
from app.video_automation.settings import settings_problems, settings_row, settings_values, update_settings

SLUG = "xitong-shuo-wo-shi-bug"


async def actor_for(session):
    email = os.environ.get("ACTOR_EMAIL")
    if not email:
        emails = sorted(get_settings().admin_email_set)
        if len(emails) != 1:
            raise SystemExit(f"{len(emails)} admin emails configured; set ACTOR_EMAIL")
        email = emails[0]
    actor = await admin_actor(session, email)
    if actor is None:
        raise SystemExit("no active administrator for the configured email")
    return actor


def summary(view) -> dict[str, Any]:
    return {
        "slug": view.slug,
        "status": view.status,
        "hands_off": view.hands_off,
        "docs": [(d.kind, d.chapter_number, d.version, d.status, len(d.body_md)) for d in view.docs],
        "episodes": [(e.number, e.status, e.slug) for e in view.episodes],
    }


def latest(view, kind: str, chapter: int):
    found = [d for d in view.docs if d.kind == kind and d.chapter_number == chapter]
    return max(found, key=lambda d: d.version) if found else None


async def cmd_status():
    async with SessionFactory() as session:
        view = await drama.series_view(session, SLUG)
        print(json.dumps(summary(view), ensure_ascii=False, indent=1))


async def cmd_create(bundle):
    async with SessionFactory() as session:
        actor = await actor_for(session)
        view = await drama.create_series(session, actor, SeriesIn(**bundle["series"]))
        print(json.dumps(summary(view), ensure_ascii=False, indent=1))


async def set_auto_continue():
    async with SessionFactory() as session:
        actor = await actor_for(session)
        row = await settings_row(session)
        payload = settings_values(row)
        if payload.drama.series_auto_continue:
            print("series_auto_continue already true")
            return
        payload.drama.series_auto_continue = True
        # settings_problems needs the API keys the admin router sees; inside the container the
        # runtime lacks them, and the one change here is a boolean on an already-saved row.
        problems = settings_problems(payload, get_settings())
        if problems:
            print(f"(settings_problems in this runtime: {problems})", flush=True)
        await update_settings(session, actor, payload)
        print("series_auto_continue -> true")


async def cmd_fill(bundle, minutes: float):
    deadline = time.monotonic() + minutes * 60
    for doc in bundle["docs"]:
        kind, chapter = doc["kind"], doc["chapter"]
        while True:
            async with SessionFactory() as session:
                view = await drama.series_view(session, SLUG)
                current = latest(view, kind, chapter)
                if current is not None and current.body_md == doc["body_md"] and current.status == "approved":
                    print(f"{kind}/{chapter}: ours is approved (v{current.version})", flush=True)
                    break
                if current is not None and current.status in ("review", "rejected", "approved"):
                    actor = await actor_for(session)
                    edit = SeriesDocEditIn(body_md=doc["body_md"], body_json=doc["body_json"], approve=True)
                    view = await drama.edit_doc(session, actor, SLUG, kind, chapter, edit)
                    after = latest(view, kind, chapter)
                    print(f"{kind}/{chapter}: replaced v{current.version} ({current.status}) with authored v{after.version} ({after.status}); series {view.status}", flush=True)
                    break
                state = "absent" if current is None else current.status
                print(f"{kind}/{chapter}: waiting ({state}); series {view.status}; {time.strftime('%H:%M:%S')}", flush=True)
            if time.monotonic() > deadline:
                raise SystemExit(f"gave up waiting for {kind}/{chapter}")
            await asyncio.sleep(45)
    async with SessionFactory() as session:
        actor = await actor_for(session)
        view = await drama.patch_series(session, actor, SLUG, SeriesPatch(hands_off=True))
        print("hands_off ->", view.hands_off, flush=True)
    await set_auto_continue()
    await cmd_status()


async def cmd_submit(bundle, only: list[str]):
    """File each bundle document as the worker would: a first version waiting for the owner
    (the fill loop then replaces and approves it). Skips a kind whose latest version is already
    waiting or approved."""
    for doc in bundle["docs"]:
        key = f"{doc['kind']}/{doc['chapter']}"
        if only and key not in only:
            continue
        async with SessionFactory() as session:
            view = await drama.series_view(session, SLUG)
            current = latest(view, doc["kind"], doc["chapter"])
            if current is not None and current.status in ("review", "approved"):
                print(f"{key}: already v{current.version} ({current.status}); not filed", flush=True)
                continue
            payload = SeriesDocSubmitIn(
                kind=doc["kind"], chapter_number=doc["chapter"],
                body_md=doc["body_md"], body_json=doc["body_json"],
            )
            filed = await drama.submit_doc(session, SLUG, payload, await settings_row(session))
            print(f"{key}: filed v{filed.version} ({filed.status})", flush=True)


async def main(argv: list[str]) -> None:
    cmd = argv[0]
    try:
        if cmd == "submit":
            await cmd_submit(json.load(open(argv[1], encoding="utf-8")), argv[2:])
        elif cmd == "status":
            await cmd_status()
        elif cmd == "create":
            await cmd_create(json.load(open(argv[1], encoding="utf-8")))
        elif cmd == "fill":
            await cmd_fill(json.load(open(argv[1], encoding="utf-8")), float(argv[2]) if len(argv) > 2 else 150)
        elif cmd == "continue-on":
            await set_auto_continue()
        else:
            raise SystemExit(__doc__)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
