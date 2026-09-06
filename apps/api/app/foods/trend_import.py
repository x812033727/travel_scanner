"""Import a batch of 潮流街區 merchants from JSON, idempotently.

The 99 merchants attached to the trend districts reached production on 2026-09-06
through a throwaway script that lived in one session's scratch directory, so nobody
could re-run, verify or extend that pipeline. This module is that script, kept: the
same JSON shape, the same rules, re-runnable by anyone with
``python -m app.cli import-trend-merchants [--file <json>] [--apply]``. The batch
itself lives next to it in ``data/trend_merchants.json``; the next sweep appends to it.

What a row becomes, and why:

* ``review_status='pending'``, ``is_active=False``, ``map_match_status='unverified'``.
  This path cannot publish anything: publication still needs an administrator's
  approval and a durable coordinate, exactly as for a seeded merchant.
* ``area_id`` is the ``food_areas`` row named ``f"{destination}-{district_key}"``,
  recorded with ``area_source='admin'`` so ``seed-foods`` never reassigns it.
* One ``FoodMerchantSource``: a ``merchant_official`` page is the shop's own site
  (``source_scope='merchant_website'``), an ``official_tourism`` page is a tourism
  board's page about that one shop (``'merchant_listing'``); both claim the display
  name and the address. Only https pages are accepted — do not rewrite an http address
  blindly, check that the https version answers first.
* Up to three categories, the first one primary, ``source='admin'``.
* One ``AdminAuditLog`` row per applied batch (``food_merchant_created``).

Deduplication has two layers, because a slug alone was not enough on 2026-09-06: one
Tainan shop collided on slug and another on the same ``local_name`` under a different
slug. Both are skipped and reported, never merged into the existing row.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from app.db import SessionFactory
from app.destinations.catalog import destination_for_id
from app.foods.category_catalog import CATEGORY_SEEDS_BY_SLUG, SLUG_PATTERN
from app.foods.service import destination_country_code
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantSource,
)

DEFAULT_FILE = Path(__file__).resolve().parent / "data" / "trend_merchants.json"
SOURCE_SCOPES: dict[str, str] = {
    "merchant_official": "merchant_website",
    "official_tourism": "merchant_listing",
}
SOURCE_CLAIMS: tuple[str, ...] = ("display_name", "address")
MAX_CATEGORIES = 3
MERCHANT_DISPLAY_ORDER = 100
AUDIT_ACTION = "food_merchant_created"
AUDIT_SOURCE = "trend-merchant-sweep"

_LATIN_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9&'’.-]*")


class TrendImportError(ValueError):
    """The file cannot be imported as it is; the message names the row and the rule."""


@dataclass(frozen=True)
class TrendMerchant:
    slug: str
    destination_id: str
    district_key: str
    name: str
    local_name: str
    address: str | None
    category_slugs: tuple[str, ...]
    source_url: str
    source_title: str
    source_kind: str
    note: str | None = None
    confidence: str | None = None

    @property
    def area_slug(self) -> str:
        return f"{self.destination_id}-{self.district_key}"

    @property
    def source_scope(self) -> str:
        return SOURCE_SCOPES[self.source_kind]

    @property
    def identity(self) -> tuple[str, str]:
        """The second dedupe key: the same shop under another slug."""
        return (self.destination_id, self.local_name.casefold())


def slug_for(destination_id: str, name: str, local_name: str) -> str:
    """A slug from the Latin brand in the name when there is one, else a transliteration.

    Trend shops almost always carry a Latin brand (FUGLEN TOKYO → ``tokyo-fuglen-tokyo``);
    a purely local name is transliterated (喫茶半月 → ``tokyo-chi-cha-ban-yue``). The
    result is an internal identifier only — merchant slugs never appear in public API
    output — so a pinyin-looking slug is acceptable.
    """
    latin = " ".join(_LATIN_TOKEN.findall(name)) or " ".join(_LATIN_TOKEN.findall(local_name))
    basis = latin or unidecode(local_name or name)
    key = re.sub(r"[^a-z0-9]+", "-", basis.casefold()).strip("-")
    if not key:
        raise TrendImportError(f"cannot build a slug for {name!r} / {local_name!r}")
    return f"{destination_id}-{key}"


def _text(raw: Mapping[str, Any], key: str, *, row: int, required: bool = True) -> str | None:
    value = raw.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise TrendImportError(f"row {row}: {key} is required")
        return None
    if not isinstance(value, str):
        raise TrendImportError(f"row {row}: {key} must be a string")
    return value.strip()


def parse_merchant(raw: Mapping[str, Any], *, row: int) -> TrendMerchant:
    """Validate one JSON object; every rule that production relied on is checked here."""
    destination_id = _text(raw, "destination", row=row) or ""
    if destination_for_id(destination_id) is None:
        raise TrendImportError(f"row {row}: unknown destination {destination_id!r}")
    district_key = _text(raw, "district_key", row=row) or ""
    if not SLUG_PATTERN.match(district_key):
        raise TrendImportError(
            f"row {row}: district_key {district_key!r} must be lowercase kebab-case"
        )
    name = _text(raw, "name_zh", row=row) or ""
    local_name = _text(raw, "local_name", row=row) or ""
    slug = _text(raw, "slug", row=row, required=False) or slug_for(destination_id, name, local_name)
    if not SLUG_PATTERN.match(slug) or not slug.startswith(f"{destination_id}-"):
        raise TrendImportError(
            f"row {row}: slug {slug!r} must be lowercase kebab-case and start with "
            f"{destination_id + '-'!r}"
        )
    source_url = _text(raw, "source_url", row=row) or ""
    if not source_url.startswith("https://"):
        raise TrendImportError(f"row {row}: source_url must be https, got {source_url!r}")
    source_kind = _text(raw, "source_kind", row=row) or ""
    if source_kind not in SOURCE_SCOPES:
        raise TrendImportError(
            f"row {row}: source_kind must be one of {sorted(SOURCE_SCOPES)}, got {source_kind!r}"
        )
    categories = raw.get("category_slugs")
    if not isinstance(categories, list) or not categories:
        raise TrendImportError(f"row {row}: category_slugs must be a non-empty list")
    if len(categories) > MAX_CATEGORIES:
        raise TrendImportError(f"row {row}: at most {MAX_CATEGORIES} categories")
    if len(set(categories)) != len(categories):
        raise TrendImportError(f"row {row}: category_slugs repeats a category")
    unknown = [slug for slug in categories if slug not in CATEGORY_SEEDS_BY_SLUG]
    if unknown:
        raise TrendImportError(f"row {row}: unknown categories {unknown}")
    return TrendMerchant(
        slug=slug,
        destination_id=destination_id,
        district_key=district_key,
        name=name,
        local_name=local_name,
        address=_text(raw, "address_local", row=row, required=False),
        category_slugs=tuple(str(slug) for slug in categories),
        source_url=source_url,
        source_title=_text(raw, "source_title", row=row) or "",
        source_kind=source_kind,
        note=_text(raw, "note", row=row, required=False),
        confidence=_text(raw, "confidence", row=row, required=False),
    )


def parse_merchants(rows: Iterable[Mapping[str, Any]]) -> list[TrendMerchant]:
    merchants = [parse_merchant(raw, row=index) for index, raw in enumerate(rows, start=1)]
    repeated_slugs = sorted(slug for slug, n in Counter(m.slug for m in merchants).items() if n > 1)
    if repeated_slugs:
        raise TrendImportError(f"duplicate slugs in file: {repeated_slugs}")
    repeated_names = sorted(
        f"{destination}:{local_name}"
        for (destination, local_name), n in Counter(m.identity for m in merchants).items()
        if n > 1
    )
    if repeated_names:
        raise TrendImportError(f"same destination and local_name twice in file: {repeated_names}")
    return merchants


def load_trend_merchants(path: Path) -> list[TrendMerchant]:
    with path.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        raise TrendImportError(f"{path.name}: expected a JSON list of merchants")
    return parse_merchants(rows)


async def _create(
    session: AsyncSession,
    merchant: TrendMerchant,
    area: FoodArea,
    categories: Mapping[str, FoodCategory],
) -> FoodMerchant:
    row = FoodMerchant(
        slug=merchant.slug,
        destination_id=merchant.destination_id,
        country_code=destination_country_code(merchant.destination_id) or area.country_code,
        name=merchant.name,
        local_name=merchant.local_name,
        address=merchant.address,
        google_place_id=None,
        naver_map_url=None,
        map_match_status="unverified",
        review_status="pending",
        is_active=False,
        verified_at=None,
        display_order=MERCHANT_DISPLAY_ORDER,
        area_id=area.id,
        area_source="admin",
    )
    session.add(row)
    await session.flush()
    session.add(
        FoodMerchantSource(
            merchant_id=row.id,
            source_type=merchant.source_kind,
            source_scope=merchant.source_scope,
            source_title=merchant.source_title,
            source_url=merchant.source_url,
            claims_json=list(SOURCE_CLAIMS),
            edition_year=None,
            distinction=None,
            is_current=True,
        )
    )
    for order, slug in enumerate(merchant.category_slugs):
        session.add(
            FoodMerchantCategory(
                merchant_id=row.id,
                category_id=categories[slug].id,
                is_primary=order == 0,
                display_order=order,
                source="admin",
            )
        )
    return row


async def persist_trend_merchants(
    session: AsyncSession,
    merchants: Sequence[TrendMerchant],
    *,
    apply: bool,
    source_file: str = "",
) -> dict[str, Any]:
    """Write the merchants that are new, report every one, commit only with ``apply``.

    A dry run reads the same tables and produces the same report with ``would_create``
    in place of ``created``, so the operator sees exactly what ``--apply`` will do.
    """
    area_slugs = {merchant.area_slug for merchant in merchants}
    areas = {
        row.slug: row
        for row in (
            await session.scalars(select(FoodArea).where(FoodArea.slug.in_(area_slugs)))
        ).all()
    }
    categories = {row.slug: row for row in (await session.scalars(select(FoodCategory))).all()}
    existing = (
        await session.scalars(
            select(FoodMerchant).where(
                or_(
                    FoodMerchant.slug.in_({merchant.slug for merchant in merchants}),
                    FoodMerchant.destination_id.in_({m.destination_id for m in merchants}),
                )
            )
        )
    ).all()
    by_slug = {row.slug: row for row in existing}
    by_identity = {(row.destination_id, row.local_name.casefold()): row for row in existing}
    outcomes: Counter[str] = Counter()
    rows: list[dict[str, Any]] = []
    created = 0
    for merchant in merchants:
        detail: str | None = None
        if merchant.slug in by_slug:
            outcome = "skipped_existing_slug"
        elif merchant.identity in by_identity:
            outcome, detail = "skipped_same_name", by_identity[merchant.identity].slug
        elif merchant.area_slug not in areas:
            outcome, detail = "missing_area", merchant.area_slug
        elif any(slug not in categories for slug in merchant.category_slugs):
            outcome = "missing_category"
            detail = ",".join(s for s in merchant.category_slugs if s not in categories)
        else:
            outcome = "created" if apply else "would_create"
            created += 1
            if apply:
                row = await _create(session, merchant, areas[merchant.area_slug], categories)
                by_slug[merchant.slug] = row
                by_identity[merchant.identity] = row
        outcomes[outcome] += 1
        rows.append({"slug": merchant.slug, "outcome": outcome, "detail": detail})
    if apply:
        if created:
            session.add(
                AdminAuditLog(
                    actor_user_id=None,
                    action=AUDIT_ACTION,
                    target=f"food_merchants:{created}",
                    metadata_json={"source": AUDIT_SOURCE, "count": created, "file": source_file},
                )
            )
        await session.commit()
    return {
        "applied": apply,
        "total": len(merchants),
        "created": created,
        "outcomes": dict(sorted(outcomes.items())),
        "rows": rows,
    }


async def import_trend_merchants(
    path: Path, *, apply: bool, limit: int | None = None
) -> dict[str, Any]:
    merchants = load_trend_merchants(path)
    if limit:
        merchants = merchants[:limit]
    async with SessionFactory() as session:
        return await persist_trend_merchants(session, merchants, apply=apply, source_file=path.name)
