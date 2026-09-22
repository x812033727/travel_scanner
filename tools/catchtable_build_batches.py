"""Turn a CatchTable candidate file into the two importer files, and refuse what they would refuse.

Standard library only, so it runs on the researcher's own machine (Windows included) without
the API virtualenv. It is deliberately a converter, not an importer: nothing here reads or writes
the database. The authoritative rules live in ``app.foods.trend_import`` (merchants) and
``app.foods.platform_review_import`` (platform rows); both reject a whole file over one bad
record, which is why this script checks the shapes that would trip them before anything is
written to disk.

Two passes, because the platform rows need merchant ids that only exist after the merchants
are imported::

    catchtable_build_batches.py --candidates <BATCH>/candidates.json \
        --merchants-out <BATCH>/merchants.json
    # import-trend-merchants --file ... --apply on the host, then export the worklist, then
    catchtable_build_batches.py --candidates <BATCH>/candidates.json --worklist worklist.json \
        --platform-out <BATCH>/platform-reviews.json

``--check`` alone validates and prints the summary. Rank numbers never leave the candidate
file: they go into the merchant ``note`` (which the importer does not store) and into one
platform-row evidence entry, as the reason the shop was looked at.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
PROVIDER = "catchtable_global"
COUNTRY_CODE = "KR"
CATCHTABLE_HOST = "https://www.catchtable.net"
# The prefixes the shop pages' own hreflang uses. There is no Korean edition; a `ko` entry
# would be invented, and the importer's language check would reject it anyway.
LOCALE_PREFIXES = {"zh-TW": "/zh-TW", "zh-CN": "/zh-CN", "ja": "/ja-JP"}
OUTCOMES = ("import", "duplicate", "no_official_source", "not_a_restaurant", "unclear")
BOOKINGS = ("reservation", "waiting_only", "none", "unclear")
BOOKING_STATUS = {"reservation": "verified", "waiting_only": "disabled", "none": "disabled"}
SOURCE_KINDS = ("merchant_official", "official_tourism")
MAX_CATEGORIES = 3
MAX_QUOTE = 300
MAX_NOTE = 1000
MAX_OBSERVATION = 1000

# Mirrors platform_links._CATCHTABLE_SLUG: a dot segment may start with an underscore but is
# never empty, and the whole id starts alphanumeric.
ALIAS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LATIN = re.compile(
    r"^[A-Za-z0-9\s&'’.,()/\-àâäáãåçéèêëíìîïñóòôöõúùûüýÿœæÀÂÄÁÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŒÆ]+$"
)
# Sites that may lead a researcher to a shop but are never its source. The full list lives in
# app/foods/enrichment.py (PLATFORM_HOSTS); this is the subset a Korean batch actually meets.
NEVER_A_SOURCE = (
    "catchtable.net",
    "catchtable.co.kr",
    "naver.com",
    "naver.me",
    "google.com",
    "goo.gl",
    "instagram.com",
    "facebook.com",
    "fb.com",
    "tripadvisor.com",
    "tripadvisor.co.kr",
    "guide.michelin.com",
    "mangoplate.com",
    "siksinhot.com",
    "kakao.com",
    "youtube.com",
    "tiktok.com",
    "x.com",
    "twitter.com",
    "blog.me",
    "tistory.com",
    "smartstore.naver.com",
)


class CandidateFileError(ValueError):
    """The candidate file cannot be converted; the message lists every problem found."""


def _aware(value: Any, label: str, problems: list[str]) -> None:
    if not isinstance(value, str):
        problems.append(f"{label}: must be an ISO 8601 timestamp with a timezone")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        problems.append(f"{label}: {value!r} is not an ISO 8601 timestamp")
        return
    if parsed.tzinfo is None:
        problems.append(f"{label}: {value!r} has no timezone")


def _text(
    value: Any, label: str, problems: list[str], *, required: bool, limit: int = 255
) -> str | None:
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            problems.append(f"{label}: required")
        return None
    if not isinstance(value, str):
        problems.append(f"{label}: must be a string")
        return None
    text = value.strip()
    if len(text) > limit:
        problems.append(f"{label}: longer than {limit} characters")
    return text


def _host(url: str) -> str:
    return (urlsplit(url).hostname or "").casefold().removeprefix("www.")


def _is_platform(url: str) -> bool:
    host = _host(url)
    return any(host == item or host.endswith(f".{item}") for item in NEVER_A_SOURCE)


def slug_for(destination: str, alias: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "-", alias.casefold()).strip("-")
    return f"{destination}-{key}" if key else f"{destination}-shop"


def shop_url(alias: str, locale: str | None = None) -> str:
    prefix = LOCALE_PREFIXES[locale] if locale else ""
    return f"{CATCHTABLE_HOST}{prefix}/shop/{alias}"


def _check_localized(
    alias: str, urls: Any, label: str, problems: list[str], *, required: bool
) -> dict[str, str]:
    if urls is None:
        if required:
            problems.append(
                f"{label}: localized_urls with zh-TW, zh-CN and ja are required for a bookable shop"
            )
        return {}
    if not isinstance(urls, dict):
        problems.append(f"{label}: localized_urls must be an object")
        return {}
    result: dict[str, str] = {}
    for locale, url in urls.items():
        if locale not in LOCALE_PREFIXES:
            problems.append(
                f"{label}: locale {locale!r} is not one CatchTable publishes "
                "(zh-TW, zh-CN, ja; there is no ko)"
            )
            continue
        expected = shop_url(alias, locale)
        if url != expected:
            problems.append(f"{label}: {locale} URL must be {expected}, got {url!r}")
            continue
        result[locale] = url
    if required:
        for locale in LOCALE_PREFIXES:
            if locale not in result:
                problems.append(f"{label}: localized_urls is missing {locale}")
    return result


def _check_ranking_evidence(
    record: dict[str, Any], label: str, problems: list[str]
) -> list[dict[str, Any]]:
    evidence = record.get("ranking_evidence")
    if not isinstance(evidence, list) or not evidence:
        problems.append(f"{label}: ranking_evidence must list at least one ranking page")
        return []
    kept: list[dict[str, Any]] = []
    for index, item in enumerate(evidence):
        where = f"{label}.ranking_evidence[{index}]"
        if not isinstance(item, dict):
            problems.append(f"{where}: must be an object")
            continue
        page = _text(item.get("page"), f"{where}.page", problems, required=True, limit=2048)
        if page and not page.startswith(f"{CATCHTABLE_HOST}/"):
            problems.append(f"{where}.page: must be a CatchTable page")
        rank = item.get("rank")
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            problems.append(f"{where}.rank: must be a positive integer")
        _aware(item.get("captured_at"), f"{where}.captured_at", problems)
        kept.append(item)
    return kept


def _check_merchant(
    record: dict[str, Any], destination: str, label: str, problems: list[str]
) -> dict[str, Any] | None:
    merchant = record.get("merchant")
    if not isinstance(merchant, dict):
        problems.append(f"{label}: an import record needs a merchant object")
        return None
    where = f"{label}.merchant"
    slug = _text(merchant.get("slug"), f"{where}.slug", problems, required=False, limit=128)
    if slug is None:
        slug = slug_for(destination, str(record.get("alias", "")))
    if not SLUG.match(slug) or not slug.startswith(f"{destination}-"):
        problems.append(
            f"{where}.slug: {slug!r} must be lowercase kebab-case starting with "
            f"{destination + '-'!r}"
        )
    district = _text(
        merchant.get("district_key"), f"{where}.district_key", problems, required=False, limit=128
    )
    if district is not None and not SLUG.match(district):
        problems.append(
            f"{where}.district_key: {district!r} must be lowercase kebab-case "
            f"(an area key of {destination})"
        )
    name_zh = _text(merchant.get("name_zh"), f"{where}.name_zh", problems, required=True)
    name_en = _text(merchant.get("name_en"), f"{where}.name_en", problems, required=False)
    if name_en is not None and not LATIN.match(name_en):
        problems.append(f"{where}.name_en: {name_en!r} is not a Latin label")
    local_name = _text(merchant.get("local_name"), f"{where}.local_name", problems, required=True)
    address = _text(
        merchant.get("address_local"),
        f"{where}.address_local",
        problems,
        required=False,
        limit=1000,
    )
    categories = merchant.get("category_slugs")
    if not isinstance(categories, list) or not categories:
        problems.append(f"{where}.category_slugs: must be a non-empty list")
        categories = []
    elif len(categories) > MAX_CATEGORIES:
        problems.append(f"{where}.category_slugs: at most {MAX_CATEGORIES}")
    elif len(set(categories)) != len(categories):
        problems.append(f"{where}.category_slugs: repeats a category")
    for slug_value in categories:
        if not isinstance(slug_value, str) or not SLUG.match(slug_value):
            problems.append(f"{where}.category_slugs: {slug_value!r} is not a category slug")
    source = merchant.get("source")
    if not isinstance(source, dict):
        problems.append(
            f"{where}.source: required (the official site or the tourism-board page "
            "about this branch)"
        )
        source = {}
    url = _text(source.get("url"), f"{where}.source.url", problems, required=True, limit=2048)
    if url:
        if not url.startswith("https://"):
            problems.append(f"{where}.source.url: must be https")
        elif _is_platform(url):
            problems.append(
                f"{where}.source.url: {_host(url)} is a platform, aggregator or social site "
                "and is never a source"
            )
    _text(source.get("title"), f"{where}.source.title", problems, required=True)
    kind = _text(source.get("kind"), f"{where}.source.kind", problems, required=True, limit=32)
    if kind is not None and kind not in SOURCE_KINDS:
        problems.append(f"{where}.source.kind: must be one of {list(SOURCE_KINDS)}")
    _text(source.get("quote"), f"{where}.source.quote", problems, required=True, limit=MAX_QUOTE)
    return {
        "slug": slug,
        "district_key": district,
        "name_zh": name_zh,
        "name_en": name_en,
        "local_name": local_name,
        "address_local": address,
        "category_slugs": list(categories),
        "source": source,
    }


def load_candidates(path: Path) -> dict[str, Any]:
    """Parse and validate the whole file; every problem is reported at once."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CandidateFileError(f"{path}: {exc}") from exc
    problems: list[str] = []
    if not isinstance(document, dict):
        raise CandidateFileError(f"{path}: expected a JSON object")
    if document.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version must be {SCHEMA_VERSION}")
    batch_id = _text(document.get("batch_id"), "batch_id", problems, required=True, limit=120)
    destination = (
        _text(document.get("destination"), "destination", problems, required=True, limit=64) or ""
    )
    if destination and not SLUG.match(destination):
        problems.append(f"destination: {destination!r} must be a destination id such as seoul")
    _aware(document.get("collected_at"), "collected_at", problems)
    rankings = document.get("rankings")
    if not isinstance(rankings, list):
        problems.append("rankings: must be a list of captured ranking pages")
    records = document.get("records")
    if not isinstance(records, list):
        problems.append("records: must be a list")
        records = []
    seen_aliases: set[str] = set()
    seen_slugs: set[str] = set()
    seen_identities: set[str] = set()
    checked: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        label = f"records[{index}]"
        if not isinstance(record, dict):
            problems.append(f"{label}: must be an object")
            continue
        alias = (
            _text(record.get("alias"), f"{label}.alias", problems, required=True, limit=160) or ""
        )
        label = f"records[{index}] {alias}"
        if alias and not ALIAS.match(alias):
            problems.append(f"{label}: alias {alias!r} is not a CatchTable shop id")
        if alias in seen_aliases:
            problems.append(f"{label}: alias appears twice")
        seen_aliases.add(alias)
        outcome = record.get("outcome")
        if outcome not in OUTCOMES:
            problems.append(f"{label}: outcome must be one of {list(OUTCOMES)}")
        _aware(record.get("checked_at"), f"{label}.checked_at", problems)
        ranking = _check_ranking_evidence(record, label, problems)
        catchtable = record.get("catchtable")
        booking = None
        localized: dict[str, str] = {}
        observation = None
        if outcome in {"import", "duplicate"}:
            if not isinstance(catchtable, dict):
                problems.append(
                    f"{label}: catchtable block is required for import and duplicate records"
                )
                catchtable = {}
            booking = catchtable.get("booking")
            if booking not in BOOKINGS:
                problems.append(f"{label}.catchtable.booking: must be one of {list(BOOKINGS)}")
            observation = _text(
                catchtable.get("booking_observation"),
                f"{label}.catchtable.booking_observation",
                problems,
                required=booking in BOOKING_STATUS,
                limit=MAX_OBSERVATION,
            )
            localized = _check_localized(
                alias,
                catchtable.get("localized_urls"),
                f"{label}.catchtable",
                problems,
                required=booking == "reservation",
            )
        merchant = None
        duplicate_of = None
        if outcome == "import":
            merchant = _check_merchant(record, destination, label, problems)
            if merchant:
                if merchant["slug"] in seen_slugs:
                    problems.append(f"{label}: slug {merchant['slug']!r} appears twice")
                seen_slugs.add(merchant["slug"])
                identity = (merchant["local_name"] or "").casefold()
                if identity in seen_identities:
                    problems.append(f"{label}: local_name {merchant['local_name']!r} appears twice")
                seen_identities.add(identity)
        elif outcome == "duplicate":
            duplicate_of = _text(
                record.get("duplicate_of"),
                f"{label}.duplicate_of",
                problems,
                required=True,
                limit=128,
            )
            if duplicate_of and not SLUG.match(duplicate_of):
                problems.append(
                    f"{label}.duplicate_of: {duplicate_of!r} must be the catalog merchant's slug"
                )
        elif record.get("merchant") is not None:
            problems.append(f"{label}: a {outcome} record must not carry a merchant block")
        _text(record.get("notes"), f"{label}.notes", problems, required=False, limit=MAX_NOTE)
        checked.append(
            {
                "alias": alias,
                "outcome": outcome,
                "checked_at": record.get("checked_at"),
                "ranking_evidence": ranking,
                "catchtable": catchtable if isinstance(catchtable, dict) else {},
                "booking": booking,
                "booking_observation": observation,
                "localized_urls": localized,
                "merchant": merchant,
                "duplicate_of": duplicate_of,
                "notes": record.get("notes"),
            }
        )
    if problems:
        raise CandidateFileError(f"{path.name}: " + " | ".join(problems))
    return {"batch_id": batch_id, "destination": destination, "records": checked}


def _ranking_sentence(record: dict[str, Any]) -> str:
    parts = []
    for item in record["ranking_evidence"]:
        page = str(item["page"])
        kind = (
            "候位榜"
            if "/top-list/waiting/" in page
            else "最佳餐廳榜"
            if "/ranking/" in page
            else "榜單"
        )
        parts.append(
            f"CatchTable {kind} 第 {item['rank']} 名（{str(item['captured_at'])[:10]} 擷取）"
        )
    return "；".join(parts)


def build_merchants(batch: dict[str, Any]) -> list[dict[str, Any]]:
    """The list ``import-trend-merchants --file`` reads, one entry per ``import`` record."""
    rows: list[dict[str, Any]] = []
    for record in batch["records"]:
        if record["outcome"] != "import":
            continue
        merchant = record["merchant"]
        source = merchant["source"]
        note = (
            f"{_ranking_sentence(record)}；僅作發現與處理順序，不公開。來源引文：{source['quote']}"
        )
        row: dict[str, Any] = {
            "destination": batch["destination"],
            "district_key": merchant["district_key"],
            "name_zh": merchant["name_zh"],
            "name_en": merchant["name_en"],
            "local_name": merchant["local_name"],
            "address_local": merchant["address_local"],
            "category_slugs": merchant["category_slugs"],
            "source_url": source["url"],
            "source_title": source["title"],
            "source_kind": source["kind"],
            "note": note[:MAX_NOTE],
            "confidence": "high",
            "slug": merchant["slug"],
        }
        rows.append({key: value for key, value in row.items() if value is not None})
    return rows


def load_worklist(path: Path) -> dict[str, str]:
    """slug -> merchant id from ``export-food-merchant-worklist`` output (or any list of rows)."""
    document = json.loads(path.read_text(encoding="utf-8"))
    rows: Any = document
    if isinstance(document, dict):
        for key in ("merchants", "rows", "items"):
            if isinstance(document.get(key), list):
                rows = document[key]
                break
    if not isinstance(rows, list):
        raise CandidateFileError(f"{path}: expected a worklist with a list of merchants")
    ids: dict[str, str] = {}
    for row in rows:
        if (
            isinstance(row, dict)
            and isinstance(row.get("slug"), str)
            and isinstance(row.get("id"), str)
        ):
            ids[row["slug"]] = row["id"]
    return ids


def build_platform_reviews(
    batch: dict[str, Any], ids: dict[str, str]
) -> tuple[dict[str, Any], list[str]]:
    """The batch ``apply-food-platform-reviews --file`` reads; returns it and the slugs left out."""
    records: list[dict[str, Any]] = []
    missing: list[str] = []
    for record in batch["records"]:
        status = BOOKING_STATUS.get(record["booking"] or "")
        if record["outcome"] not in {"import", "duplicate"} or status is None:
            continue
        slug = (
            record["merchant"]["slug"] if record["outcome"] == "import" else record["duplicate_of"]
        )
        merchant_id = ids.get(slug)
        if merchant_id is None:
            missing.append(slug)
            continue
        alias = record["alias"]
        local_name = (
            record["merchant"]["local_name"]
            if record["outcome"] == "import"
            else record["catchtable"].get("listed_name") or slug
        )
        date = str(record["checked_at"])[:10]
        verdict = (
            "頁面有店家自己的訂位控制項，公開。"
            if status == "verified"
            else "只有候位或沒有訂位控制項，依 2026-09-11 規則存停用、不公開。"
        )
        review_note = (
            f"{date}：{_ranking_sentence(record)}。{record['booking_observation']} {verdict}"
        )
        if record["notes"]:
            review_note += f" {record['notes']}"
        evidence: list[dict[str, str]] = [
            {
                "url": record["localized_urls"].get("zh-TW") or shop_url(alias, "zh-TW"),
                "role": "platform_page",
                "observation": str(record["booking_observation"])[:MAX_OBSERVATION],
            }
        ]
        if "ja" in record["localized_urls"]:
            evidence.append(
                {
                    "url": record["localized_urls"]["ja"],
                    "role": "locale_variant",
                    "observation": (
                        "店頁 hreflang：ja 對 /ja-JP/、zh-Hans 對 /zh-CN/、zh-Hant 對 /zh-TW/、"
                        "x-default 對無前綴；沒有韓文版。"
                    ),
                }
            )
        for item in record["ranking_evidence"][:2]:
            evidence.append(
                {
                    "url": str(item["page"]),
                    "role": "ranking_page",
                    "observation": (
                        f"第 {item['rank']} 名，{str(item['captured_at'])[:10]} 擷取；"
                        "名次只作發現用，不公開。"
                    ),
                }
            )
        records.append(
            {
                "merchant_id": merchant_id,
                "slug": slug,
                "name": local_name,
                "country_code": COUNTRY_CODE,
                "provider": PROVIDER,
                "status": status,
                "canonical_url": shop_url(alias),
                "localized_urls": dict(record["localized_urls"]),
                "review_note": review_note[:MAX_NOTE],
                "booking_observation": str(record["booking_observation"])[:MAX_OBSERVATION],
                "evidence": evidence,
            }
        )
    researched_at = max(
        (str(r["checked_at"]) for r in batch["records"]),
        default=datetime.now().astimezone().isoformat(),
    )
    return (
        {
            "schema_version": 1,
            "batch_id": f"{batch['batch_id']}-platforms",
            "researched_at": researched_at,
            "method": (
                "CatchTable 榜單反推：本機瀏覽器渲染店頁判斷控制項；"
                "只有店家自己的訂位控制項算可訂位。"
            ),
            "rules": (
                "可訂位存 verified；只能候位或沒有控制項存 disabled；"
                "語言網址取自店頁 hreflang，沒有 ko。"
            ),
            "records": records,
        },
        missing,
    )


def summary(batch: dict[str, Any]) -> dict[str, Any]:
    outcomes = Counter(record["outcome"] for record in batch["records"])
    bookings = Counter(
        str(record["booking"])
        for record in batch["records"]
        if record["outcome"] in {"import", "duplicate"}
    )
    return {
        "batch_id": batch["batch_id"],
        "destination": batch["destination"],
        "records": len(batch["records"]),
        "outcomes": dict(sorted(outcomes.items())),
        "bookings": dict(sorted(bookings.items())),
        "slugs": [r["merchant"]["slug"] for r in batch["records"] if r["outcome"] == "import"],
    }


def _write(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument(
        "--merchants-out", type=Path, help="Write the import-trend-merchants file here"
    )
    parser.add_argument(
        "--platform-out", type=Path, help="Write the apply-food-platform-reviews file here"
    )
    parser.add_argument(
        "--worklist", type=Path, help="export-food-merchant-worklist output, for merchant ids"
    )
    parser.add_argument("--check", action="store_true", help="Validate and summarize only")
    args = parser.parse_args(argv)
    try:
        batch = load_candidates(args.candidates)
    except CandidateFileError as exc:
        for line in str(exc).split(" | "):
            print(f"ERROR {line}", file=sys.stderr)
        return 2
    report = summary(batch)
    if args.merchants_out:
        rows = build_merchants(batch)
        _write(args.merchants_out, rows)
        report["merchants_written"] = len(rows)
    if args.platform_out:
        if not args.worklist:
            print(
                "ERROR --platform-out needs --worklist "
                "(merchant ids come from the exported worklist)",
                file=sys.stderr,
            )
            return 2
        ids = load_worklist(args.worklist)
        reviews, missing = build_platform_reviews(batch, ids)
        _write(args.platform_out, reviews)
        report["platform_rows_written"] = len(reviews["records"])
        report["platform_rows_without_merchant"] = missing
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
