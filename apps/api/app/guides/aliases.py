"""The other names an article answers to, and where the seed for them comes from.

Two editorial sources already name articles by something other than their title: the AI
glossary's alias list (``docs/ai-terms-series/aliases.json``, ``ML`` for the
machine-learning term) and the lesson keywords of a series catalogue
(``app/guides/series_data``). This module turns both into ``guide_article_aliases`` rows;
``search`` reads the table. An alias shared by several articles of a language is kept for
ranking but names no best match, and the seed says so rather than picking one.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.content_pack import default_directory
from app.guides.models import GuideArticle, GuideArticleAlias
from app.guides.search import normalize, refresh_aliases
from app.guides.series import catalogues

AliasSource = Literal["term", "keyword", "series", "editor"]
MAX_ALIAS_LENGTH = 120


def default_terms_file() -> Path:
    """The glossary's alias list, which ships with the repository rather than the package;
    a container without ``docs/`` seeds the series keywords only."""
    return Path(__file__).resolve().parents[4] / "docs" / "ai-terms-series" / "aliases.json"


@dataclass(frozen=True)
class SeedAlias:
    slug: str
    locale: str
    alias: str
    source: AliasSource

    @property
    def alias_norm(self) -> str:
        return normalize(self.alias)


def _pack_locales(directory: Path, slug: str) -> list[str]:
    path = directory / f"{slug}.json"
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return list(raw.get("locales", {}))


def term_aliases(terms_file: Path | None = None, packs: Path | None = None) -> list[SeedAlias]:
    """The glossary aliases, one row per language the term's pack is written in. A key
    names the ``ai-term-<key>`` pack when there is one, else a pack of that slug."""
    path = terms_file or default_terms_file()
    if not path.is_file():
        # Only the default may be absent (a container without ``docs/``); a path the
        # operator named and got wrong is an error, not an empty seed.
        if terms_file is not None:
            raise FileNotFoundError(path)
        return []
    directory = packs or default_directory()
    rows: list[SeedAlias] = []
    for key, aliases in json.loads(path.read_text(encoding="utf-8")).items():
        slug = next(
            (
                candidate
                for candidate in (f"ai-term-{key}", key)
                if (directory / f"{candidate}.json").is_file()
            ),
            None,
        )
        if slug is None:
            continue
        for locale in _pack_locales(directory, slug):
            rows.extend(SeedAlias(slug, locale, alias, "term") for alias in aliases)
    return rows


def series_aliases() -> list[SeedAlias]:
    return [
        SeedAlias(lesson.slug, catalogue.locale, alias, "series")
        for catalogue in catalogues()
        for lesson in catalogue.entries
        for alias in lesson.aliases
    ]


def seed_rows(terms_file: Path | None = None, packs: Path | None = None) -> list[SeedAlias]:
    """Every alias the two sources name, deduplicated per (slug, locale, folded alias);
    empty or over-long aliases are left out rather than refused at the database."""
    seen: set[tuple[str, str, str]] = set()
    rows: list[SeedAlias] = []
    for row in [*term_aliases(terms_file, packs), *series_aliases()]:
        folded = row.alias_norm
        key = (row.slug, row.locale, folded)
        if not folded or len(row.alias) > MAX_ALIAS_LENGTH or key in seen:
            continue
        seen.add(key)
        rows.append(row)
    return rows


def shared_aliases(rows: list[SeedAlias]) -> dict[str, list[str]]:
    """``locale:alias`` -> the slugs that share it. Informational: these still rank, they
    just never head the results."""
    slugs: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        slugs.setdefault((row.locale, row.alias_norm), set()).add(row.slug)
    return {
        f"{locale}:{alias}": sorted(names)
        for (locale, alias), names in sorted(slugs.items())
        if len(names) > 1
    }


async def apply_seed(
    session: AsyncSession, rows: list[SeedAlias], *, dry_run: bool = False
) -> dict[str, Any]:
    """Insert the aliases that are not there yet and refresh the index rows they touch.

    Never deletes and never rewrites: an alias an editor removed from the table stays
    removed, and one the editor added is not the seed's to judge. Not committed here.
    """
    articles = {
        slug: article_id
        for slug, article_id in await session.execute(
            select(GuideArticle.slug, GuideArticle.id).where(
                GuideArticle.slug.in_(sorted({row.slug for row in rows}))
            )
        )
    }
    existing = {
        (article_id, locale, alias_norm)
        for article_id, locale, alias_norm in await session.execute(
            select(
                GuideArticleAlias.article_id, GuideArticleAlias.locale, GuideArticleAlias.alias_norm
            )
        )
    }
    report: dict[str, Any] = {
        "dry_run": dry_run,
        "inserted": 0,
        "unchanged": 0,
        "unknown_slugs": [],
        "shared": shared_aliases(rows),
        "reindexed": 0,
    }
    touched: set[tuple[Any, str]] = set()
    unknown = Counter(row.slug for row in rows if row.slug not in articles)
    report["unknown_slugs"] = sorted(unknown)
    for row in rows:
        article_id = articles.get(row.slug)
        if article_id is None:
            continue
        if (article_id, row.locale, row.alias_norm) in existing:
            report["unchanged"] += 1
            continue
        report["inserted"] += 1
        touched.add((article_id, row.locale))
        if dry_run:
            continue
        session.add(
            GuideArticleAlias(
                article_id=article_id,
                locale=row.locale,
                alias=row.alias.strip(),
                alias_norm=row.alias_norm,
                source=row.source,
            )
        )
    if not dry_run:
        await session.flush()
        for article_id, locale in sorted(touched, key=lambda item: (str(item[0]), item[1])):
            if await refresh_aliases(session, article_id, locale):
                report["reindexed"] += 1
    return report
