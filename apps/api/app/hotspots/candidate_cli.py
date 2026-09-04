"""Run a candidate list through the cross-check and report what each row would become.

The list is a JSON file of untrusted names, typically pasted out of an assistant:

    {"city_code": "TNN", "candidates": [{"name": "赤崁樓", "district": "中西區"}]}

Nothing is written unless ``--apply`` is passed, so the usual order is to look at the
dry-run counts first and only then commit them.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import httpx

from app.admin.service import load_runtime_settings
from app.db import SessionFactory
from app.hotspots.candidate_import import persist_resolutions
from app.hotspots.candidate_sources import CandidateResolver
from app.hotspots.candidates import CandidateInput, summarize
from app.hotspots.cities import CITY_BY_CODE
from app.infra import get_redis
from app.places.google import GoogleTravelService


def load_candidates(path: Path) -> tuple[str, list[CandidateInput]]:
    payload = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    city_code = str(payload["city_code"]).upper()
    city = CITY_BY_CODE.get(city_code)
    if city is None:
        raise SystemExit(f"unknown city_code {city_code}; add it to cities.py first")
    seen: set[str] = set()
    candidates: list[CandidateInput] = []
    for item in payload.get("candidates", []):
        name = str(item.get("name") or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        district = str(item.get("district") or "").strip()
        candidates.append(
            CandidateInput(
                name=name,
                city_code=city_code,
                # The district matters: searching Google for a temple with only the
                # prefecture attached finds a same-named temple in the next city.
                city_qualifier=f"{district} {city.name}".strip(),
            )
        )
    return city_code, candidates


async def import_candidates(path: Path, *, apply: bool, limit: int | None = None) -> dict[str, Any]:
    city_code, candidates = load_candidates(path)
    if limit:
        candidates = candidates[:limit]
    redis = get_redis()
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        google = GoogleTravelService(redis, settings, locale="zh-TW")
        async with httpx.AsyncClient(timeout=25) as client:
            resolver = CandidateResolver(google, client)
            resolutions = await resolver.resolve_all(candidates)
        written = await persist_resolutions(
            session, resolutions, now=datetime.now(UTC), apply=apply
        )
    return {
        "city_code": city_code,
        "candidates": len(candidates),
        "applied": apply,
        "lanes": summarize(resolutions),
        "rows": written,
        "lookup_failures": dict(resolver.failures),
        "held_for_review": [
            {
                "name": item.candidate.name,
                "reason": item.reason,
                "matched": item.article.title if item.article else None,
                "score": item.name_score,
                "km": item.drift_km,
            }
            for item in resolutions
            if item.lane == "needs_review"
        ],
    }
