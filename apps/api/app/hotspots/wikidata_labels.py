"""Backfill hotspot bootstrap labels from Wikidata.

The checked-in bootstrap files know a Traditional Chinese ``name`` for every
attraction and, for reviewed rows, its original-script ``local_name``. Wikidata
carries the same places with labels in every language the site speaks (CC0),
so this module fills what the seed cannot derive by itself:

* ``local_name`` for rows that still lack an original-script name, from the
  label in the destination country's own language (Japanese, Korean, Thai,
  Vietnamese; Taiwan and Hong Kong already use the Chinese name);
* ``names``: the English, Japanese, Korean and Simplified Chinese labels that
  :class:`app.hotspots.catalog.HotspotSeed` merges into its five-locale map.

Curated fields are never overwritten: ``name`` stays the editorial label and an
existing ``local_name`` wins unless the caller asks otherwise. Everything here
is deterministic and file-based so the result is reviewed in the diff; the only
network call is :func:`fetch_labels`, kept separate so the rest is testable.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypedDict

import httpx

from app.localized_names import original_locale_for

BOOTSTRAP_FILES: tuple[str, ...] = (
    "bootstrap.json",
    "deep_bootstrap.json",
    "secondary_bootstrap.json",
    "food_area_bootstrap.json",
    "kanto_expansion_bootstrap.json",
)
USER_AGENT = "TravelScannerBot/0.1 (+https://github.com/x812033727/travel_scanner)"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
# wbgetentities accepts at most 50 ids per request.
BATCH_SIZE = 50
# Wikidata language codes, in preference order, behind each site locale.
LABEL_LANGUAGES: dict[str, tuple[str, ...]] = {
    "en": ("en",),
    "ja": ("ja",),
    "ko": ("ko",),
    "zh-TW": ("zh-tw", "zh-hant", "zh-hk", "zh"),
    "zh-CN": ("zh-cn", "zh-hans", "zh-sg", "zh"),
    "th": ("th",),
    "vi": ("vi",),
}
# The locales the seed derives from curated data on its own; only the rest are stored.
STORED_LOCALES: tuple[str, ...] = ("en", "ja", "ko", "zh-CN")
REQUESTED_LANGUAGES: tuple[str, ...] = tuple(
    dict.fromkeys(code for codes in LABEL_LANGUAGES.values() for code in codes)
)

Labels = Mapping[str, str]
LabelFetcher = Callable[[Sequence[str]], dict[str, dict[str, str]]]


def site_labels(entity_labels: Labels) -> dict[str, str]:
    """Map raw Wikidata labels (``{"zh-hant": ...}``) onto site locales plus th/vi."""

    result: dict[str, str] = {}
    for locale, codes in LABEL_LANGUAGES.items():
        value = next((entity_labels[code].strip() for code in codes if entity_labels.get(code)), "")
        if value:
            result[locale] = value
    return result


def apply_labels(
    row: dict[str, Any],
    labels: Labels,
    *,
    country_code: str,
    overwrite_original: bool = False,
) -> list[str]:
    """Write Wikidata labels into one bootstrap row; return the fields that changed."""

    changed: list[str] = []
    language = original_locale_for(country_code)
    original = labels.get(language) if language else None
    # Chinese-script destinations already carry the original as the curated name.
    if original and language != "zh-TW" and (overwrite_original or not row.get("local_name")):
        if row.get("local_name") != original:
            _insert_after(row, "name", "local_name", original)
            changed.append("local_name")
    names = {
        locale: labels[locale]
        for locale in STORED_LOCALES
        if labels.get(locale) and labels[locale] != row.get("name")
    }
    if names != (row.get("names") or {}):
        if names:
            _insert_after(row, row.get("local_name") and "local_name" or "name", "names", names)
        else:
            row.pop("names", None)
        changed.append("names")
    return changed


def _insert_after(row: dict[str, Any], anchor: str, key: str, value: Any) -> None:
    """Set ``key`` right after ``anchor`` so the JSON diff stays readable."""

    if key in row:
        row[key] = value
        return
    items = list(row.items())
    index = next((position for position, (name, _) in enumerate(items) if name == anchor), -1)
    items.insert(index + 1, (key, value))
    row.clear()
    row.update(items)


def fetch_labels(
    qids: Sequence[str],
    *,
    client: httpx.Client | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, dict[str, str]]:
    """Fetch raw labels for ``qids`` from Wikidata, 50 items per request."""

    owned = client is None
    session = client or httpx.Client(timeout=30, headers={"User-Agent": USER_AGENT})
    try:
        labels: dict[str, dict[str, str]] = {}
        for start in range(0, len(qids), BATCH_SIZE):
            batch = list(qids[start : start + BATCH_SIZE])
            params = {
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "props": "labels",
                "languages": "|".join(REQUESTED_LANGUAGES),
                "format": "json",
            }
            for attempt in range(6):
                response = session.get(WIKIDATA_API, params=params)
                if response.status_code not in {429, 500, 502, 503, 504}:
                    break
                sleep(min(30, 3 * (attempt + 1)))
            response.raise_for_status()
            payload = response.json()
            if "error" in payload:
                raise RuntimeError(f"Wikidata rejected the request: {payload['error']}")
            for qid, entity in payload.get("entities", {}).items():
                labels[qid] = {
                    code: str(label.get("value", ""))
                    for code, label in (entity.get("labels") or {}).items()
                }
            if start + BATCH_SIZE < len(qids):
                sleep(0.5)
        return labels
    finally:
        if owned:
            session.close()


_SCALAR_ARRAY = re.compile(
    r"\[\s*((?:(?:\"(?:[^\"\\]|\\.)*\"|-?\d[\d.eE+-]*|true|false|null)(?:,\s*)?)+)\s*\]"
)
_SCALAR = re.compile(r"\"(?:[^\"\\]|\\.)*\"|-?\d[\d.eE+-]*|true|false|null")
RENDER_STYLES: tuple[str, ...] = ("indent", "inline_arrays", "inline_short_arrays")


def render_rows(rows: list[dict[str, Any]], style: str = "indent") -> str:
    """Render bootstrap rows with two-space indentation in one of the checked-in styles."""

    text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    if style == "indent":
        return text

    def collapse(match: re.Match[str]) -> str:
        inline = "[" + ", ".join(_SCALAR.findall(match.group(1))) + "]"
        if style == "inline_short_arrays":
            line_start = text.rfind("\n", 0, match.start()) + 1
            if len(text[line_start : match.start()]) + len(inline) > 100:
                return match.group(0)
        return inline

    return _SCALAR_ARRAY.sub(collapse, text)


def detect_style(text: str, rows: list[dict[str, Any]]) -> str:
    """The render style that reproduces ``text`` byte for byte, or ``indent``."""

    for style in RENDER_STYLES:
        if render_rows(rows, style) == text:
            return style
    return "indent"


class FileCounts(TypedDict):
    rows: int
    changed: int
    style: str


@dataclass
class FillReport:
    files: dict[str, FileCounts] = field(default_factory=dict)
    missing_qids: list[str] = field(default_factory=list)
    changed_rows: list[str] = field(default_factory=list)

    @property
    def total_changed(self) -> int:
        return sum(counts["changed"] for counts in self.files.values())


def fill_bootstrap_files(
    root: Path,
    *,
    fetch: LabelFetcher = fetch_labels,
    files: Iterable[str] = BOOTSTRAP_FILES,
    dry_run: bool = False,
    overwrite_original: bool = False,
    country_for_city: Callable[[str], str],
) -> FillReport:
    """Backfill every bootstrap file under ``root``; return what changed per file."""

    report = FillReport()
    loaded: dict[str, tuple[str, list[dict[str, Any]]]] = {}
    for filename in files:
        text = (root / filename).read_text(encoding="utf-8")
        loaded[filename] = (text, json.loads(text))
    qids = sorted(
        {
            str(row["wikidata_item_id"])
            for _, rows in loaded.values()
            for row in rows
            if row.get("wikidata_item_id")
        }
    )
    labels = fetch(qids) if qids else {}
    report.missing_qids = [qid for qid in qids if qid not in labels]
    for filename, (text, rows) in loaded.items():
        style = detect_style(text, rows)
        changed = 0
        for row in rows:
            qid = row.get("wikidata_item_id")
            if not qid or qid not in labels:
                continue
            fields = apply_labels(
                row,
                site_labels(labels[qid]),
                country_code=country_for_city(str(row["city_code"])),
                overwrite_original=overwrite_original,
            )
            if fields:
                changed += 1
                report.changed_rows.append(f"{filename}: {row['name']} ({', '.join(fields)})")
        report.files[filename] = {"rows": len(rows), "changed": changed, "style": style}
        if changed and not dry_run:
            (root / filename).write_text(render_rows(rows, style), encoding="utf-8")
    return report
