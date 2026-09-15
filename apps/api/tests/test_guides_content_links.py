"""Links between packaged articles must use the address the target article renders at.

An article lives at exactly one URL, fixed by its kind: ``/<locale>/life/<slug>`` or
``/<locale>/guides/<kind>/<slug>``. Any other kind in the path renders the "not available
here" page, so the link looks fine in the pack and is dead on the site. On 2026-09-15 the
en, ja, ko and zh-CN versions of ``taipei-4-day-itinerary`` linked the intel article
``taiwan-entry-2026-arrival-card`` under ``/guides/howto/``, and neither the schema nor
``pack_cli lint`` looks at link targets.

Only links to slugs that have a pack are checked: an article can also exist solely in the
database, and this file cannot know its kind.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from app.guides.content_pack import default_directory

SITE_LINK = re.compile(
    r"https://mokaair\.com/(?:en|ja|ko|zh-CN|zh-TW)/(?:life/|guides/(howto|intel)/)([a-z0-9-]+)"
)


def _packs() -> dict[str, dict[str, Any]]:
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(Path(default_directory()).glob("*.json"))
    }


def _article_inlines(node: Any) -> Iterator[tuple[str, str]]:
    """Every ``{"type": "article"}`` inline under ``node``, as (kind, slug)."""
    stack = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if current.get("type") == "article" and isinstance(current.get("slug"), str):
                yield current.get("kind", "life"), current["slug"]
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)


def _wrong_kind_links(packs: dict[str, dict[str, Any]]) -> list[str]:
    kinds = {pack["slug"]: pack.get("kind", "life") for pack in packs.values()}
    wrong: list[str] = []
    for source, pack in packs.items():
        for locale, document in pack["locales"].items():
            text = json.dumps(document, ensure_ascii=False)
            where = f"{source} ({locale})"
            for match in SITE_LINK.finditer(text):
                linked, slug = match.group(1) or "life", match.group(2)
                if slug in kinds and kinds[slug] != linked:
                    wrong.append(f"{where}: {match.group(0)} but {slug} is {kinds[slug]}")
            for linked, slug in _article_inlines(document):
                if slug in kinds and kinds[slug] != linked:
                    wrong.append(
                        f"{where}: article inline {linked}/{slug} but {slug} is {kinds[slug]}"
                    )
    return wrong


def test_links_to_packaged_articles_use_the_target_kind() -> None:
    wrong = _wrong_kind_links(_packs())
    assert not wrong, "links that render the not-available page:\n" + "\n".join(wrong)


def test_a_link_under_the_wrong_kind_is_reported() -> None:
    packs = {
        "entry": {"slug": "entry", "kind": "intel", "locales": {"en": {"blocks": []}}},
        "itinerary": {
            "slug": "itinerary",
            "kind": "howto",
            "locales": {
                "en": {
                    "blocks": [
                        {
                            "type": "link",
                            "text": "Entry",
                            "url": "https://mokaair.com/en/guides/howto/entry",
                        },
                        {
                            "type": "rich_paragraph",
                            "inlines": [
                                {
                                    "type": "article",
                                    "text": "Entry",
                                    "kind": "life",
                                    "slug": "entry",
                                }
                            ],
                        },
                    ]
                }
            },
        },
    }
    wrong = _wrong_kind_links(packs)
    assert len(wrong) == 2
    assert all(line.startswith("itinerary (en): ") for line in wrong)


def test_a_link_to_an_article_without_a_pack_is_left_alone() -> None:
    packs = {
        "itinerary": {
            "slug": "itinerary",
            "kind": "howto",
            "locales": {
                "en": {
                    "blocks": [
                        {
                            "type": "link",
                            "text": "Elsewhere",
                            "url": "https://mokaair.com/en/guides/intel/db-only",
                        }
                    ]
                }
            },
        }
    }
    assert _wrong_kind_links(packs) == []
