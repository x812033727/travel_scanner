"""Theme taxonomy seeding, per-hotspot assignments, and the helpers the API reads.

Three sources may attach a theme to a hotspot, and the sync on every collect run
must not undo the other two:

- ``seed`` links come from ``theme_bootstrap.json`` and follow the file exactly —
  created when the pair appears, months and note refreshed, deleted when the pair
  leaves the file.
- ``admin`` and ``ai`` links are never created, changed or removed here. An
  administrator who removes a seeded pair leaves a tombstone (``is_active=False``,
  ``source='admin'``) so the next sync sees the pair exists and does not bring it
  back.
"""

from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

from sqlalchemy import ColumnElement, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.theme_catalog import (
    SEASON_THEME_SLUGS,
    THEME_SEEDS,
    THEME_SEEDS_BY_SLUG,
    validate_months,
)
from app.i18n import Locale
from app.models import HotspotTheme, HotspotThemeLink, TravelHotspot
from app.problems import AppError

BOOTSTRAP_NOTE_MAX_CHARS = 200

# Seasons first, then shop types, each in its display order; the same order the
# facets, the cards and the admin list show.
THEME_ORDER = (
    case((HotspotTheme.kind == "season", 0), else_=1),
    HotspotTheme.display_order,
    HotspotTheme.slug,
)


@dataclass(frozen=True)
class ThemeAssignment:
    hotspot_slug: str
    themes: tuple[str, ...]
    # Per-theme month overrides, only for season themes (Sapporo's sakura is May).
    months: Mapping[str, tuple[int, ...]]
    note: str | None


def _load_bootstrap() -> tuple[ThemeAssignment, ...]:
    rows = json.loads(Path(__file__).with_name("theme_bootstrap.json").read_text(encoding="utf-8"))
    seeds = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    assignments: list[ThemeAssignment] = []
    for row in rows:
        slug = row["slug"]
        seed = seeds.get(slug)
        if seed is None:
            # Slugs here are the resolved catalog slugs (explicit, legacy, or
            # wikidata-<id>); a typo would otherwise silently tag nothing.
            raise RuntimeError(f"theme_bootstrap: unknown hotspot slug {slug}")
        themes = tuple(str(item) for item in row["themes"])
        if not themes or len(set(themes)) != len(themes):
            raise RuntimeError(f"theme_bootstrap: {slug} themes must be non-empty and unique")
        for theme_slug in themes:
            theme = THEME_SEEDS_BY_SLUG.get(theme_slug)
            if theme is None:
                raise RuntimeError(f"theme_bootstrap: {slug} references unknown theme {theme_slug}")
            if theme.kind == "shop" and seed.category != "shopping":
                raise RuntimeError(
                    f"theme_bootstrap: {slug} is a {seed.category} hotspot; "
                    f"shop theme {theme_slug} belongs on category shopping"
                )
        months = {
            str(theme_slug): tuple(int(month) for month in values)
            for theme_slug, values in (row.get("months") or {}).items()
        }
        for theme_slug, values in months.items():
            if theme_slug not in themes:
                raise RuntimeError(f"theme_bootstrap: {slug} sets months for unlisted {theme_slug}")
            if theme_slug not in SEASON_THEME_SLUGS:
                raise RuntimeError(
                    f"theme_bootstrap: {slug} sets months on shop theme {theme_slug}"
                )
            if not values:
                raise RuntimeError(
                    f"theme_bootstrap: {slug} month override for {theme_slug} is empty"
                )
            validate_months(values)
        note = row.get("note")
        if note is not None and (not str(note).strip() or len(note) > BOOTSTRAP_NOTE_MAX_CHARS):
            raise RuntimeError(
                f"theme_bootstrap: {slug} note must be 1-{BOOTSTRAP_NOTE_MAX_CHARS} characters"
            )
        assignments.append(ThemeAssignment(slug, themes, months, note))
    slugs = [assignment.hotspot_slug for assignment in assignments]
    if len(set(slugs)) != len(slugs):
        raise RuntimeError("theme_bootstrap: hotspot slugs must be unique")
    return tuple(assignments)


THEME_BOOTSTRAP: tuple[ThemeAssignment, ...] = _load_bootstrap()
SEED_LINK_PAIRS: frozenset[tuple[str, str]] = frozenset(
    (assignment.hotspot_slug, theme_slug)
    for assignment in THEME_BOOTSTRAP
    for theme_slug in assignment.themes
)


async def seed_hotspot_themes(session: AsyncSession) -> dict[str, HotspotTheme]:
    """Create the themes the catalog lists and are not yet in the database.

    A row that already exists — renamed, reordered or deactivated by an
    administrator — is left exactly as it is, whatever its ``source`` says.
    """

    themes = {row.slug: row for row in (await session.scalars(select(HotspotTheme))).all()}
    for seed in THEME_SEEDS:
        if seed.slug in themes:
            continue
        theme = HotspotTheme(
            slug=seed.slug,
            kind=seed.kind,
            names_json=dict(seed.names),
            months_json=list(seed.months),
            display_order=seed.display_order,
            is_active=True,
            source="seed",
        )
        session.add(theme)
        themes[seed.slug] = theme
    await session.flush()
    return themes


async def sync_hotspot_themes(session: AsyncSession) -> dict[str, int]:
    """Bring the ``seed`` links in line with theme_bootstrap.json; touch nothing else.

    Like ``sync_hotspot_areas`` this runs on every collect run: a month or note
    corrected in the file must reach rows that were linked months ago. Returns the
    counts of links created, updated and removed.
    """

    themes = await seed_hotspot_themes(session)
    wanted_slugs = [assignment.hotspot_slug for assignment in THEME_BOOTSTRAP]
    hotspot_ids: dict[str, UUID] = {}
    if wanted_slugs:
        hotspot_ids = {
            slug: hotspot_id
            for slug, hotspot_id in (
                await session.execute(
                    select(TravelHotspot.slug, TravelHotspot.id).where(
                        TravelHotspot.slug.in_(wanted_slugs)
                    )
                )
            ).all()
        }
    existing = {
        (link.hotspot_id, link.theme_id): link
        for link in (await session.scalars(select(HotspotThemeLink))).all()
    }
    created = updated = removed = 0
    wanted: set[tuple[UUID, UUID]] = set()
    for assignment in THEME_BOOTSTRAP:
        hotspot_id = hotspot_ids.get(assignment.hotspot_slug)
        if hotspot_id is None:
            # seed_catalog has not created the row yet; the next run picks it up.
            continue
        for theme_slug in assignment.themes:
            theme = themes[theme_slug]
            override = assignment.months.get(theme_slug)
            months = list(override) if override else None
            key = (hotspot_id, theme.id)
            wanted.add(key)
            link = existing.get(key)
            if link is None:
                session.add(
                    HotspotThemeLink(
                        hotspot_id=hotspot_id,
                        theme_id=theme.id,
                        months_json=months,
                        source="seed",
                        note=assignment.note,
                        is_active=True,
                    )
                )
                created += 1
            elif link.source == "seed" and (
                link.months_json != months or link.note != assignment.note or not link.is_active
            ):
                link.months_json = months
                link.note = assignment.note
                link.is_active = True
                updated += 1
    for key, link in existing.items():
        if link.source == "seed" and key not in wanted:
            await session.delete(link)
            removed += 1
    await session.flush()
    return {
        "themes": len(themes),
        "links_created": created,
        "links_updated": updated,
        "links_removed": removed,
    }


def theme_name(theme: HotspotTheme, locale: Locale) -> str:
    """The label for ``locale``; zh-CN falls back to the Traditional label, like areas."""

    names = theme.names_json
    name = names.get(locale)
    if name:
        return name
    if locale == "zh-CN" and names.get("zh-TW"):
        return names["zh-TW"]
    return names.get("en") or names.get("zh-TW") or theme.slug


def theme_ref(
    theme: HotspotTheme, locale: Locale, months: list[int] | None = None
) -> dict[str, Any]:
    """The public shape of one theme, with the effective months for one hotspot."""

    return {
        "slug": theme.slug,
        "kind": theme.kind,
        "name": theme_name(theme, locale),
        "months": list(months if months is not None else theme.months_json or []),
    }


async def resolve_theme(session: AsyncSession, slug: str | None) -> HotspotTheme | None:
    """The active theme behind a ``theme=`` filter, or 422 when there is none.

    Administrators add themes at runtime, so the check is a lookup rather than a
    constant list like ``_resolve_area``.
    """

    if not slug:
        return None
    theme = await session.scalar(
        select(HotspotTheme).where(
            HotspotTheme.slug == slug.strip().casefold(), HotspotTheme.is_active.is_(True)
        )
    )
    if theme is None:
        raise AppError(422, "unsupported_theme", "目前沒有這個主題")
    return theme


def theme_filter(slug: str) -> ColumnElement[bool]:
    """WHERE clause: the hotspot carries an active link to the active theme ``slug``."""

    return TravelHotspot.id.in_(
        select(HotspotThemeLink.hotspot_id)
        .join(HotspotTheme, HotspotTheme.id == HotspotThemeLink.theme_id)
        .where(
            HotspotTheme.slug == slug,
            HotspotTheme.is_active.is_(True),
            HotspotThemeLink.is_active.is_(True),
        )
    )


async def load_hotspot_themes(
    session: AsyncSession, hotspot_ids: list[UUID], locale: Locale
) -> dict[UUID, list[dict[str, Any]]]:
    """One batch per page: every active theme of the listed hotspots, in catalog order."""

    if not hotspot_ids:
        return {}
    rows = (
        await session.execute(
            select(HotspotThemeLink, HotspotTheme)
            .join(HotspotTheme, HotspotTheme.id == HotspotThemeLink.theme_id)
            .where(
                HotspotThemeLink.hotspot_id.in_(hotspot_ids),
                HotspotThemeLink.is_active.is_(True),
                HotspotTheme.is_active.is_(True),
            )
            .order_by(*THEME_ORDER)
        )
    ).all()
    themes_by_hotspot: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for link, theme in rows:
        themes_by_hotspot[link.hotspot_id].append(theme_ref(theme, locale, link.months_json))
    return dict(themes_by_hotspot)


async def theme_facets(
    session: AsyncSession, locale: Locale, *conditions: ColumnElement[bool]
) -> list[dict[str, Any]]:
    """Every active theme with its public hotspot count, zero included, in catalog order.

    ``conditions`` are the same public-row predicates the other facets use, so the
    counts agree with what a filtered ranking returns.
    """

    public_links = (
        select(
            HotspotThemeLink.theme_id.label("theme_id"),
            HotspotThemeLink.hotspot_id.label("hotspot_id"),
        )
        .join(TravelHotspot, TravelHotspot.id == HotspotThemeLink.hotspot_id)
        .where(HotspotThemeLink.is_active.is_(True), *conditions)
        .subquery()
    )
    rows = (
        await session.execute(
            select(HotspotTheme, func.count(public_links.c.hotspot_id).label("count"))
            .outerjoin(public_links, public_links.c.theme_id == HotspotTheme.id)
            .where(HotspotTheme.is_active.is_(True))
            .group_by(HotspotTheme.id)
            .order_by(*THEME_ORDER)
        )
    ).all()
    return [{**theme_ref(theme, locale), "count": int(count)} for theme, count in rows]


async def seed_hotspot_themes_once() -> dict[str, int]:
    """One-off back-fill outside a collect run: ``python -m app.hotspots.themes``."""

    from app.db import SessionFactory

    async with SessionFactory() as session:
        report = await sync_hotspot_themes(session)
        await session.commit()
        return report


if __name__ == "__main__":
    print(json.dumps(asyncio.run(seed_hotspot_themes_once())))
