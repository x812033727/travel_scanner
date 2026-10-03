"""Import a CatchTable candidate file in one pass: the merchants and their platform rows.

The first three batches (2026-09-23) went through two passes: ``tools/catchtable_build_batches.py``
turned the candidate file into an ``import-trend-merchants`` file, the merchants were applied, a
worklist was exported for their ids, and only then could the ``apply-food-platform-reviews`` file
be built. Every batch went to the host twice, the audit said ``trend-merchant-sweep`` (the trend
districts' importer) and the CatchTable alias that identifies the shop never reached it. This is
the same pipeline with the round trip taken out::

    python -m app.cli import-catchtable-candidates --file <candidates.json> [--limit N] [--apply]

What the candidate file may say lives in ``CandidateBatch`` (the field rules are in
``app/foods/data/catchtable/README.md``); the whole file is validated, including the two
importers' own rules, before anything opens a session, so one bad record stops the batch.

What a record becomes:

* ``import``: one merchant built exactly as ``trend_import`` builds it (pending, inactive,
  ``map_match_status='unverified'``, no coordinates, no ``naver_map_url``, one source, up to
  three categories), deduplicated on slug and on ``(destination, local_name)`` the same way,
  then its ``catchtable_global`` row. A slug that already exists for the same shop (a re-run)
  keeps the merchant and goes on to the platform row; a slug held by another shop, the same
  name under another slug, an unknown 商圈 or category skip the record.
* ``duplicate``: only the platform row, on the catalog merchant named by ``duplicate_of``.
* ``no_official_source``, ``not_a_restaurant``, ``unclear``: nothing; they stay in the file.

Platform rows go through ``platform_review_import``'s own validation and its ``_review_one``,
so the branch-identity lock, ``skipped_admin_reviewed`` and ``skipped_branch_conflict`` behave
exactly as in ``apply-food-platform-reviews``. One rule is added on top: a row that already
holds the same status and the same URLs is reported ``unchanged`` even when its note differs,
so a later batch that meets an earlier batch's shop again does not rewrite that batch's
evidence (the owner's 2026-09-23 condition on batch 2, which had to delete such a row by hand).
A new merchant whose CatchTable page already belongs to another merchant is not created at all:
the alias is the one reliable identity, so that is a duplicate the research missed.

Each record is its own transaction. A dry run makes the same calls and rolls back, so its report
has the same shape as the apply with ``would_*`` in place of the writes. Applied writes leave one
audit row each — ``food_merchant_created`` for a merchant and the platform importer's own action
for a platform row — whose ``source`` is ``catchtable-ranking-sweep`` and which carry the alias
and the ranking evidence (admin-only; rank numbers are never public).

Two things this module deliberately does not do, both decided in
``docs/catchtable-ranking-discovery.md``: it asks no classifier (no Jev, 2026-09-22 owner
principle; the conditions to reconsider are at the end of that document), and it writes no
Naver place page — whether a candidate file may carry one is the document's open question 2,
so the schema refuses the field instead of guessing.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit
from uuid import NAMESPACE_URL, UUID, uuid5

from pydantic import (
    AwareDatetime,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory
from app.destinations.catalog import destination_for_id
from app.foods import platform_review_import
from app.foods.category_catalog import CATEGORY_SEEDS_BY_SLUG, SLUG_PATTERN
from app.foods.enrichment import is_platform_host
from app.foods.platform_review_import import (
    PlatformReviewBatch,
    PlatformReviewRecord,
    ReviewFileError,
    check_review_batch,
)
from app.foods.trend_import import AUDIT_ACTION as MERCHANT_AUDIT_ACTION
from app.foods.trend_import import (
    TrendImportError,
    TrendMerchant,
    _create,
    parse_merchants,
)
from app.localized_names import is_latin_script
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantPlatformLink,
)

SCHEMA_VERSION = 1
PROVIDER = "catchtable_global"
COUNTRY_CODE = "KR"
AUDIT_SOURCE = "catchtable-ranking-sweep"
CATCHTABLE_HOST = "https://www.catchtable.net"
# The prefixes the shop pages' own hreflang uses. There is no Korean edition; a `ko` entry
# would be invented.
LOCALE_PREFIXES = {"zh-TW": "/zh-TW", "zh-CN": "/zh-CN", "ja": "/ja-JP"}
BOOKINGS = ("reservation", "waiting_only", "none", "unclear")
BOOKING_STATUS = {"reservation": "verified", "waiting_only": "disabled", "none": "disabled"}
WRITABLE_OUTCOMES = frozenset({"import", "duplicate"})
SOURCE_KINDS = ("merchant_official", "official_tourism", "merchant_platform")
MAX_CATEGORIES = 3
MAX_QUOTE = 300
MAX_NOTE = 1000
MAX_OBSERVATION = 1000
WRITES = frozenset({"created", "updated"})
WOULD_WRITE = frozenset({"would_create", "would_update"})

# Mirrors platform_links._CATCHTABLE_SLUG: a dot segment may start with an underscore but is
# never empty, and the whole id starts alphanumeric.
ALIAS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_][A-Za-z0-9_-]*)*$")
# Sites a Korean batch meets that may lead a researcher to a shop but are never its source,
# on top of the catalog-wide list in ``app.foods.enrichment.PLATFORM_HOSTS``.
KOREAN_DISCOVERY_HOSTS = (
    "naver.com",
    "naver.me",
    "google.com",
    "goo.gl",
    "tripadvisor.co.kr",
    "guide.michelin.com",
    "mangoplate.com",
    "siksinhot.com",
    "kakao.com",
    "blog.me",
    "tistory.com",
)

Outcome = Literal["import", "duplicate", "no_official_source", "not_a_restaurant", "unclear"]
Booking = Literal["reservation", "waiting_only", "none", "unclear"]
SourceKind = Literal["merchant_official", "official_tourism", "merchant_platform"]


class CandidateFileError(ValueError):
    """The candidate file cannot be imported; the message lists every problem found."""


def _blank_to_none(value: Any) -> Any:
    return None if isinstance(value, str) and not value.strip() else value


Text = Annotated[str, BeforeValidator(_blank_to_none)]
OptionalText = Annotated[str | None, BeforeValidator(_blank_to_none)]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RankingEvidence(_Model):
    page: Text = Field(max_length=2048)
    rank: int = Field(ge=1, strict=True)
    captured_at: AwareDatetime

    @model_validator(mode="after")
    def on_catchtable(self) -> RankingEvidence:
        if not self.page.startswith(f"{CATCHTABLE_HOST}/"):
            raise ValueError("page must be a CatchTable page")
        return self


class CatchtableListing(_Model):
    listed_name: OptionalText = None
    listed_address: OptionalText = None
    listed_cuisine: OptionalText = None
    listed_area: OptionalText = None
    localized_urls: dict[str, str] | None = None
    booking: Booking | None = None
    booking_observation: OptionalText = Field(default=None, max_length=MAX_OBSERVATION)
    #: The /info tab's website field as the shop registered it (merchant_platform custody).
    website: OptionalText = Field(default=None, max_length=2048)


class MerchantSource(_Model):
    url: Text = Field(max_length=2048)
    title: Text = Field(max_length=255)
    kind: SourceKind
    quote: Text = Field(max_length=MAX_QUOTE)


class CandidateMerchant(_Model):
    slug: OptionalText = Field(default=None, max_length=128)
    district_key: OptionalText = Field(default=None, max_length=128)
    name_zh: Text = Field(max_length=255)
    name_en: OptionalText = Field(default=None, max_length=255)
    local_name: Text = Field(max_length=255)
    address_local: OptionalText = Field(default=None, max_length=1000)
    category_slugs: list[str] = Field(min_length=1, max_length=MAX_CATEGORIES)
    source: MerchantSource

    @model_validator(mode="after")
    def validate_merchant(self) -> CandidateMerchant:
        problems: list[str] = []
        if self.district_key is not None and not SLUG_PATTERN.match(self.district_key):
            problems.append(f"district_key {self.district_key!r} must be lowercase kebab-case")
        if self.name_en is not None and not is_latin_script(self.name_en):
            problems.append(f"name_en {self.name_en!r} is not a Latin label")
        if len(set(self.category_slugs)) != len(self.category_slugs):
            problems.append("category_slugs repeats a category")
        unknown = [slug for slug in self.category_slugs if slug not in CATEGORY_SEEDS_BY_SLUG]
        if unknown:
            problems.append(f"unknown categories {unknown}")
        if not self.source.url.startswith("https://"):
            problems.append("source.url must be https")
        if problems:
            raise ValueError("; ".join(problems))
        return self


def shop_url(alias: str, locale: str | None = None) -> str:
    prefix = LOCALE_PREFIXES[locale] if locale else ""
    return f"{CATCHTABLE_HOST}{prefix}/shop/{alias}"


def alias_slug(destination: str, alias: str) -> str:
    """The slug a record without one gets: the alias, kebab-cased, under the destination."""
    key = re.sub(r"[^a-z0-9]+", "-", alias.casefold()).strip("-")
    return f"{destination}-{key}" if key else f"{destination}-shop"


def _host(url: str) -> str:
    return (urlsplit(url).hostname or "").casefold().rstrip(".").removeprefix("www.")


def never_a_source(url: str) -> bool:
    host = _host(url)
    return is_platform_host(url) or any(
        host == item or host.endswith(f".{item}") for item in KOREAN_DISCOVERY_HOSTS
    )


class CandidateRecord(_Model):
    alias: Text = Field(max_length=160)
    outcome: Outcome
    checked_at: AwareDatetime
    ranking_evidence: list[RankingEvidence] = Field(min_length=1)
    catchtable: CatchtableListing | None = None
    merchant: CandidateMerchant | None = None
    duplicate_of: OptionalText = Field(default=None, max_length=128)
    notes: OptionalText = Field(default=None, max_length=MAX_NOTE)

    @property
    def booking(self) -> str | None:
        return self.catchtable.booking if self.catchtable else None

    @property
    def platform_status(self) -> str | None:
        """verified or disabled for a record that leaves a platform row, else None."""
        if self.outcome not in WRITABLE_OUTCOMES:
            return None
        return BOOKING_STATUS.get(self.booking or "")

    @property
    def localized_urls(self) -> dict[str, str]:
        return dict(self.catchtable.localized_urls or {}) if self.catchtable else {}

    def is_own_platform_page(self, url: str) -> bool:
        """This alias's own CatchTable shop page (any locale, optionally /info), or the exact
        URL the researcher copied from the /info tab's website field into ``website``."""
        own = {shop_url(self.alias)} | {shop_url(self.alias, locale) for locale in LOCALE_PREFIXES}
        own |= {f"{page}/info" for page in list(own)}
        if url.rstrip("/") in own:
            return True
        return bool(self.catchtable and self.catchtable.website == url)

    @model_validator(mode="after")
    def validate_record(self) -> CandidateRecord:
        problems: list[str] = []
        if not ALIAS.match(self.alias):
            problems.append(f"alias {self.alias!r} is not a CatchTable shop id")
        if self.outcome in WRITABLE_OUTCOMES:
            problems += self._listing_problems()
        if self.outcome == "import":
            if self.merchant is None:
                problems.append("an import record needs a merchant object")
            else:
                problems += self._source_problems(self.merchant.source)
        elif self.outcome == "duplicate":
            if self.duplicate_of is None:
                problems.append("duplicate_of is required for a duplicate record")
            elif not SLUG_PATTERN.match(self.duplicate_of):
                problems.append(
                    f"duplicate_of {self.duplicate_of!r} must be the catalog merchant's slug"
                )
        elif self.merchant is not None:
            problems.append(f"a {self.outcome} record must not carry a merchant block")
        if problems:
            raise ValueError("; ".join(problems))
        return self

    def _listing_problems(self) -> list[str]:
        if self.catchtable is None:
            return ["catchtable block is required for import and duplicate records"]
        problems: list[str] = []
        booking = self.catchtable.booking
        if booking is None:
            problems.append(f"catchtable.booking must be one of {list(BOOKINGS)}")
        if booking in BOOKING_STATUS and not self.catchtable.booking_observation:
            problems.append("catchtable.booking_observation is required")
        urls = self.catchtable.localized_urls
        if urls is None:
            if booking == "reservation":
                problems.append(
                    "catchtable.localized_urls with zh-TW, zh-CN and ja are required for a "
                    "bookable shop"
                )
            return problems
        for locale, url in urls.items():
            if locale not in LOCALE_PREFIXES:
                problems.append(
                    f"catchtable: locale {locale!r} is not one CatchTable publishes "
                    "(zh-TW, zh-CN, ja; there is no ko)"
                )
            elif url != shop_url(self.alias, locale):
                problems.append(
                    f"catchtable: {locale} URL must be {shop_url(self.alias, locale)}, "
                    f"got {url!r}"
                )
        if booking == "reservation":
            problems += [
                f"catchtable.localized_urls is missing {locale}"
                for locale in LOCALE_PREFIXES
                if locale not in urls
            ]
        return problems

    def _source_problems(self, source: MerchantSource) -> list[str]:
        if not source.url.startswith("https://"):
            return []  # Reported by the merchant block itself.
        if source.kind == "merchant_platform":
            if not self.is_own_platform_page(source.url):
                return [
                    "merchant.source.url: a merchant_platform source must be this alias's own "
                    "CatchTable page (or its /info tab), or exactly the URL recorded in "
                    "catchtable.website"
                ]
        elif never_a_source(source.url):
            return [
                f"merchant.source.url: {_host(source.url)} is a platform, aggregator or social "
                "site and is never a source"
            ]
        return []


class CandidateBatch(_Model):
    schema_version: Literal[1]
    batch_id: Text = Field(max_length=120)
    destination: Text = Field(max_length=64)
    collected_at: AwareDatetime
    researched_by: OptionalText = Field(default=None, max_length=255)
    method: OptionalText = Field(default=None, max_length=4000)
    #: The ranking pages as captured; evidence only, never read by the importer.
    rankings: list[dict[str, Any]]
    records: list[CandidateRecord]

    @model_validator(mode="after")
    def validate_batch(self) -> CandidateBatch:
        problems: list[str] = []
        if destination_for_id(self.destination) is None:
            problems.append(f"destination {self.destination!r} is not a destination id")
        aliases: set[str] = set()
        slugs: set[str] = set()
        names: set[str] = set()
        for index, record in enumerate(self.records):
            label = f"records[{index}] {record.alias}"
            if record.alias in aliases:
                problems.append(f"{label}: alias appears twice")
            aliases.add(record.alias)
            if record.outcome != "import" or record.merchant is None:
                continue
            merchant = record.merchant
            if merchant.slug is None:
                merchant.slug = alias_slug(self.destination, record.alias)
            if not SLUG_PATTERN.match(merchant.slug) or not merchant.slug.startswith(
                f"{self.destination}-"
            ):
                problems.append(
                    f"{label}: merchant.slug {merchant.slug!r} must be lowercase kebab-case "
                    f"starting with {self.destination + '-'!r}"
                )
            if merchant.slug in slugs:
                problems.append(f"{label}: slug {merchant.slug!r} appears twice")
            slugs.add(merchant.slug)
            if merchant.local_name.casefold() in names:
                problems.append(f"{label}: local_name {merchant.local_name!r} appears twice")
            names.add(merchant.local_name.casefold())
        if problems:
            raise ValueError(" | ".join(problems))
        return self

    @property
    def researched_at(self) -> datetime:
        return max((record.checked_at for record in self.records), default=self.collected_at)


def _record_label(location: tuple[Any, ...], raw: Any) -> str:
    if len(location) > 1 and location[0] == "records" and isinstance(location[1], int):
        records = raw.get("records") if isinstance(raw, dict) else None
        record = records[location[1]] if isinstance(records, list) else None
        alias = record.get("alias") if isinstance(record, dict) else None
        rest = ".".join(str(part) for part in location[2:])
        return f"records[{location[1]}] {alias}" + (f".{rest}" if rest else "")
    return ".".join(str(part) for part in location) or "file"


def _ranking_sentence(record: CandidateRecord) -> str:
    parts = []
    for item in record.ranking_evidence:
        kind = (
            "候位榜"
            if "/top-list/waiting/" in item.page
            else "最佳餐廳榜"
            if "/ranking/" in item.page
            else "榜單"
        )
        parts.append(f"CatchTable {kind} 第 {item.rank} 名（{item.captured_at.date()} 擷取）")
    return "；".join(parts)


def merchant_row(batch: CandidateBatch, record: CandidateRecord) -> dict[str, Any]:
    """One ``import`` record in the ``import-trend-merchants`` list format."""
    merchant = record.merchant
    assert merchant is not None and merchant.slug is not None
    source = merchant.source
    note = f"{_ranking_sentence(record)}；僅作發現與處理順序，不公開。來源引文：{source.quote}"
    row: dict[str, Any] = {
        "destination": batch.destination,
        "district_key": merchant.district_key,
        "name_zh": merchant.name_zh,
        "name_en": merchant.name_en,
        "local_name": merchant.local_name,
        "address_local": merchant.address_local,
        "category_slugs": list(merchant.category_slugs),
        "source_url": source.url,
        "source_title": source.title,
        "source_kind": source.kind,
        "note": note[:MAX_NOTE],
        "confidence": "high",
        "slug": merchant.slug,
    }
    return {key: value for key, value in row.items() if value is not None}


def merchant_rows(batch: CandidateBatch) -> list[dict[str, Any]]:
    return [merchant_row(batch, record) for record in batch.records if record.outcome == "import"]


def record_slug(record: CandidateRecord) -> str:
    """The catalog slug a writable record lands on."""
    if record.outcome == "import":
        assert record.merchant is not None and record.merchant.slug is not None
        return record.merchant.slug
    assert record.duplicate_of is not None
    return record.duplicate_of


def platform_row(record: CandidateRecord, merchant_id: UUID | str) -> dict[str, Any] | None:
    """One record in the ``apply-food-platform-reviews`` batch format, or None without a row."""
    status = record.platform_status
    if status is None:
        return None
    alias = record.alias
    slug = record_slug(record)
    listing = record.catchtable
    assert listing is not None and listing.booking_observation is not None
    observation = listing.booking_observation
    if record.outcome == "import":
        assert record.merchant is not None
        name = record.merchant.local_name
    else:
        name = listing.listed_name or slug
    localized = record.localized_urls
    verdict = (
        "頁面有店家自己的訂位控制項，公開。"
        if status == "verified"
        else "只有候位或沒有訂位控制項，依 2026-09-11 規則存停用、不公開。"
    )
    review_note = (
        f"{record.checked_at.date()}：{_ranking_sentence(record)}。{observation} {verdict}"
    )
    if record.notes:
        review_note += f" {record.notes}"
    evidence: list[dict[str, str]] = [
        {
            "url": localized.get("zh-TW") or shop_url(alias, "zh-TW"),
            "role": "platform_page",
            "observation": observation[:MAX_OBSERVATION],
        }
    ]
    if "ja" in localized:
        evidence.append(
            {
                "url": localized["ja"],
                "role": "locale_variant",
                "observation": (
                    "店頁 hreflang：ja 對 /ja-JP/、zh-Hans 對 /zh-CN/、zh-Hant 對 /zh-TW/、"
                    "x-default 對無前綴；沒有韓文版。"
                ),
            }
        )
    for item in record.ranking_evidence[:2]:
        evidence.append(
            {
                "url": item.page,
                "role": "ranking_page",
                "observation": (
                    f"第 {item.rank} 名，{item.captured_at.date()} 擷取；名次只作發現用，不公開。"
                ),
            }
        )
    return {
        "merchant_id": str(merchant_id),
        "slug": slug,
        "name": name,
        "country_code": COUNTRY_CODE,
        "provider": PROVIDER,
        "status": status,
        "canonical_url": shop_url(alias),
        "localized_urls": localized,
        "review_note": review_note[:MAX_NOTE],
        "booking_observation": observation[:MAX_OBSERVATION],
        "evidence": evidence,
    }


def platform_document(
    batch: CandidateBatch, ids: Mapping[str, str]
) -> tuple[dict[str, Any], list[str]]:
    """The two-pass ``apply-food-platform-reviews`` file; returns it and the slugs left out."""
    records: list[dict[str, Any]] = []
    missing: list[str] = []
    for record in batch.records:
        if record.platform_status is None:
            continue
        merchant_id = ids.get(record_slug(record))
        if merchant_id is None:
            missing.append(record_slug(record))
            continue
        row = platform_row(record, merchant_id)
        assert row is not None
        records.append(row)
    document = {
        "schema_version": 1,
        "batch_id": f"{batch.batch_id}-platforms",
        "researched_at": batch.researched_at.isoformat(),
        "method": (
            "CatchTable 榜單反推：本機瀏覽器渲染店頁判斷控制項；"
            "只有店家自己的訂位控制項算可訂位。"
        ),
        "rules": (
            "可訂位存 verified；只能候位或沒有控制項存 disabled；"
            "語言網址取自店頁 hreflang，沒有 ko。"
        ),
        "records": records,
    }
    return document, missing


def _placeholder_id(slug: str) -> UUID:
    """A stable stand-in merchant id for validating platform rows before the merchant exists."""
    return uuid5(NAMESPACE_URL, f"catchtable-candidate:{slug}")


def platform_batch(batch: CandidateBatch) -> PlatformReviewBatch:
    """Every platform row the file asks for, validated by the platform importer's own rules.

    Merchant ids are placeholders here; the importer swaps in the real id per record.
    """
    rows = [
        platform_row(record, _placeholder_id(record_slug(record)))
        for record in batch.records
        if record.platform_status is not None
    ]
    return PlatformReviewBatch.model_validate(
        {
            "schema_version": 1,
            "batch_id": f"{batch.batch_id}-platforms",
            "researched_at": batch.researched_at,
            "records": rows,
        }
    )


@dataclass(frozen=True)
class PreparedBatch:
    """A validated candidate file and what each importer would read from it."""

    candidates: CandidateBatch
    merchants: dict[str, TrendMerchant]
    platforms: PlatformReviewBatch
    name: str

    def platform_record(self, record: CandidateRecord) -> PlatformReviewRecord | None:
        if record.platform_status is None:
            return None
        slug = record_slug(record)
        return next(item for item in self.platforms.records if item.slug == slug)


def prepare_candidates(raw: Any, *, name: str = "candidates.json") -> PreparedBatch:
    """Validate the whole file, the two importers' rules included; raise with every problem."""
    try:
        batch = CandidateBatch.model_validate(raw)
    except ValidationError as exc:
        problems = []
        for error in exc.errors():
            message = str(error["msg"]).removeprefix("Value error, ")
            problems.append(f"{_record_label(tuple(error['loc']), raw)}: {message}")
        raise CandidateFileError(f"{name}: " + " | ".join(problems)) from None
    try:
        merchants = parse_merchants(merchant_rows(batch))
        platforms = check_review_batch(platform_batch(batch), name=name)
    except (TrendImportError, ReviewFileError, ValidationError) as exc:
        raise CandidateFileError(f"{name}: {exc}") from None
    return PreparedBatch(
        candidates=batch,
        merchants={merchant.slug: merchant for merchant in merchants},
        platforms=platforms,
        name=name,
    )


def load_candidate_file(path: Path) -> PreparedBatch:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CandidateFileError(f"{path}: {exc}") from exc
    return prepare_candidates(raw, name=path.name)


@dataclass(frozen=True)
class CandidateOutcome:
    alias: str
    research_outcome: str
    slug: str | None = None
    merchant: str | None = None
    platform: str | None = None
    status: str | None = None
    detail: str | None = None

    @property
    def writes(self) -> bool:
        return self.merchant in WRITES or self.platform in WRITES

    @property
    def skipped(self) -> bool:
        return any(
            action is not None and (action.startswith("skipped") or action.startswith("missing"))
            for action in (self.merchant, self.platform)
        )

    def line(self) -> str:
        parts = [f"{self.alias} ({self.research_outcome})"]
        if self.slug:
            parts.append(self.slug)
        parts.append(f"merchant={self.merchant or '-'}")
        status = f"/{self.status}" if self.status else ""
        parts.append(f"platform={self.platform or '-'}{status}")
        if self.detail:
            parts.append(self.detail)
        return " ".join(parts)


def _audit_evidence(record: CandidateRecord) -> dict[str, Any]:
    return {
        "source": AUDIT_SOURCE,
        "alias": record.alias,
        "ranking_evidence": [
            {"page": item.page, "rank": item.rank, "captured_at": item.captured_at.isoformat()}
            for item in record.ranking_evidence
        ],
    }


async def _merchant_for_import(
    session: AsyncSession, merchant: TrendMerchant, *, apply: bool
) -> tuple[str, str | None, FoodMerchant | None]:
    """``trend_import``'s dedupe and build, for one record inside its own transaction."""
    existing = await session.scalar(select(FoodMerchant).where(FoodMerchant.slug == merchant.slug))
    if existing is not None:
        if (existing.destination_id, existing.local_name.casefold()) == merchant.identity:
            return "skipped_existing_slug", None, existing
        # A colliding slug is not permission to give a different shop this platform row.
        return "skipped_existing_slug", f"held by {existing.local_name}", None
    neighbours = await session.scalars(
        select(FoodMerchant).where(FoodMerchant.destination_id == merchant.destination_id)
    )
    for row in neighbours.all():
        if row.local_name.casefold() == merchant.identity[1]:
            return "skipped_same_name", row.slug, None
    area = None
    if merchant.area_slug:
        area = await session.scalar(select(FoodArea).where(FoodArea.slug == merchant.area_slug))
        if area is None:
            return "missing_area", merchant.area_slug, None
    categories = {
        row.slug: row
        for row in (
            await session.scalars(
                select(FoodCategory).where(FoodCategory.slug.in_(merchant.category_slugs))
            )
        ).all()
    }
    missing = [slug for slug in merchant.category_slugs if slug not in categories]
    if missing:
        return "missing_category", ",".join(missing), None
    row = await _create(session, merchant, area, categories)
    return ("created" if apply else "would_create"), None, row


async def _same_link(
    session: AsyncSession, merchant_id: UUID, record: PlatformReviewRecord
) -> bool:
    row = await session.scalar(
        select(FoodMerchantPlatformLink).where(
            FoodMerchantPlatformLink.merchant_id == merchant_id,
            FoodMerchantPlatformLink.provider == record.provider,
        )
    )
    return row is not None and (
        row.status,
        row.canonical_url,
        row.localized_urls_json or {},
    ) == (record.status, record.canonical_url, record.localized_urls)


async def _import_one(
    session: AsyncSession,
    prepared: PreparedBatch,
    record: CandidateRecord,
    *,
    apply: bool,
) -> CandidateOutcome:
    """Everything one record writes, in the session's current transaction; never commits."""
    slug = record_slug(record)
    platform_record = prepared.platform_record(record)

    def result(**values: Any) -> CandidateOutcome:
        return CandidateOutcome(record.alias, record.outcome, slug, **values)

    merchant_action: str | None = None
    if record.outcome == "import":
        merchant_action, detail, merchant = await _merchant_for_import(
            session, prepared.merchants[slug], apply=apply
        )
        if merchant is None:
            return result(merchant=merchant_action, detail=detail)
    else:
        merchant = await session.scalar(select(FoodMerchant).where(FoodMerchant.slug == slug))
        if merchant is None:
            return result(platform="skipped_missing_merchant", detail=f"no merchant {slug}")
    created = merchant_action in {"created", "would_create"}
    if created and apply:
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action=MERCHANT_AUDIT_ACTION,
                target=f"food_merchant:{merchant.id}",
                metadata_json={
                    **_audit_evidence(record),
                    "batch_id": prepared.candidates.batch_id,
                    "file": prepared.name,
                    "slug": slug,
                    "destination_id": merchant.destination_id,
                    "source_kind": prepared.merchants[slug].source_kind,
                    "source_url": prepared.merchants[slug].source_url,
                },
            )
        )
    if platform_record is None:
        return result(merchant=merchant_action, detail="booking unclear: no platform row")
    wanted = platform_record.model_copy(update={"merchant_id": merchant.id})
    if await _same_link(session, merchant.id, wanted):
        return result(merchant=merchant_action, platform="unchanged", status=wanted.status)
    reviewed = await platform_review_import._review_one(
        session, prepared.platforms, wanted, apply=apply, audit=_audit_evidence(record)
    )
    if created and reviewed.action == "skipped_branch_conflict":
        # The alias already belongs to another merchant: this shop is in the catalog under
        # another name, and creating it again would be the duplicate the alias exists to stop.
        return result(
            merchant="skipped_branch_conflict",
            platform=reviewed.action,
            detail=f"the CatchTable page belongs to merchant {reviewed.detail}",
        )
    status = wanted.status if reviewed.action in WRITES | WOULD_WRITE else None
    return result(
        merchant=merchant_action, platform=reviewed.action, status=status, detail=reviewed.detail
    )


async def import_candidate_batch(
    session: AsyncSession,
    prepared: PreparedBatch,
    *,
    apply: bool,
    limit: int | None = None,
    progress: Callable[[str], None] | None = None,
) -> list[CandidateOutcome]:
    """Each record in its own transaction; a dry run makes the same calls and rolls back."""
    budget = limit
    outcomes: list[CandidateOutcome] = []
    for record in prepared.candidates.records:
        if record.outcome not in WRITABLE_OUTCOMES:
            outcome = CandidateOutcome(record.alias, record.outcome, detail="nothing to write")
        elif budget is not None and budget <= 0:
            continue
        else:
            if budget is not None:
                budget -= 1
            try:
                outcome = await _import_one(session, prepared, record, apply=apply)
                if apply and outcome.writes:
                    await session.commit()
                else:
                    # Ends the transaction: a dry run's rows and every lock it took go with it.
                    await session.rollback()
            except IntegrityError as exc:
                await session.rollback()
                outcome = CandidateOutcome(
                    record.alias,
                    record.outcome,
                    record_slug(record),
                    merchant="skipped_conflict" if record.outcome == "import" else None,
                    platform="skipped_conflict",
                    detail=type(exc.orig).__name__,
                )
        outcomes.append(outcome)
        if progress:
            progress(outcome.line())
    return outcomes


def summarize(
    prepared: PreparedBatch, outcomes: Sequence[CandidateOutcome], *, apply: bool
) -> dict[str, Any]:
    batch = prepared.candidates
    return {
        "batch_id": batch.batch_id,
        "destination": batch.destination,
        "applied": apply,
        "records": len(batch.records),
        "processed": len(outcomes),
        "research_outcomes": dict(sorted(Counter(r.outcome for r in batch.records).items())),
        "merchants": dict(sorted(Counter(o.merchant for o in outcomes if o.merchant).items())),
        "platform_rows": dict(
            sorted(Counter(o.platform for o in outcomes if o.platform).items())
        ),
        # As in apply-food-platform-reviews: the statuses this run writes (or would write).
        "statuses": dict(
            sorted(
                Counter(
                    o.status for o in outcomes if o.status and o.platform in WRITES | WOULD_WRITE
                ).items()
            )
        ),
        "skipped": [asdict(o) for o in outcomes if o.skipped],
        "rows": [asdict(o) for o in outcomes],
    }


def check_summary(prepared: PreparedBatch) -> dict[str, Any]:
    """What ``--check`` prints: the file is valid, and what it would ask the database for."""
    batch = prepared.candidates
    return {
        "batch_id": batch.batch_id,
        "destination": batch.destination,
        "valid": True,
        "records": len(batch.records),
        "research_outcomes": dict(sorted(Counter(r.outcome for r in batch.records).items())),
        "bookings": dict(
            sorted(
                Counter(
                    str(r.booking) for r in batch.records if r.outcome in WRITABLE_OUTCOMES
                ).items()
            )
        ),
        "merchant_slugs": sorted(prepared.merchants),
        "platform_statuses": dict(
            sorted(Counter(item.status for item in prepared.platforms.records).items())
        ),
    }


async def import_catchtable_candidates(
    path: Path, *, apply: bool, limit: int | None = None, check_only: bool = False
) -> dict[str, Any]:
    prepared = load_candidate_file(path)
    if check_only:
        return check_summary(prepared)
    async with SessionFactory() as session:
        outcomes = await import_candidate_batch(
            session,
            prepared,
            apply=apply,
            limit=limit,
            progress=lambda line: print(line, file=sys.stderr, flush=True),
        )
    return summarize(prepared, outcomes, apply=apply)
