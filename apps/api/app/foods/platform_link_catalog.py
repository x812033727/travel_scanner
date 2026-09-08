"""Conservative initial audit of every curated food merchant.

Only branch pages confirmed during the catalog audit are published.  Every other
merchant is recorded as ``ambiguous`` when the seed itself does not contain enough
evidence to identify a branch page. This makes the first-pass result explicit without
falsely claiming that a platform was exhaustively searched.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.foods.merchant_catalog import MERCHANT_SEEDS
from app.foods.platform_links import expected_platform


@dataclass(frozen=True)
class MerchantPlatformAuditSeed:
    merchant_slug: str
    provider: str
    status: str
    canonical_url: str | None = None
    localized_urls: dict[str, str] = field(default_factory=dict)
    review_note: str = (
        "The catalog seed does not contain enough evidence to identify one exact "
        "platform branch page; manual platform verification is still required."
    )


_VERIFIED: dict[str, MerchantPlatformAuditSeed] = {
    "fukuoka-sushi-sakai": MerchantPlatformAuditSeed(
        merchant_slug="fukuoka-sushi-sakai",
        provider="tablecheck",
        status="verified",
        canonical_url="https://www.tablecheck.com/en/shops/sushi-sakai/reserve",
        review_note="Exact Sushi Sakai reservation page confirmed.",
    ),
    "singapore-song-fa": MerchantPlatformAuditSeed(
        merchant_slug="singapore-song-fa",
        provider="chope",
        status="verified",
        canonical_url="https://www.chope.co/singapore-restaurants/restaurant/song-fa-bak-kut-teh",
        review_note="Exact New Bridge Road merchant page confirmed.",
    ),
    "hong-kong-yat-lok": MerchantPlatformAuditSeed(
        merchant_slug="hong-kong-yat-lok",
        provider="openrice",
        status="verified",
        canonical_url="https://www.openrice.com/en/hongkong/p-yat-lok-restaurant-p23206360",
        review_note="Exact Yat Lok merchant overview confirmed.",
    ),
}


PLATFORM_LINK_AUDIT_SEEDS: tuple[MerchantPlatformAuditSeed, ...] = tuple(
    _VERIFIED.get(
        merchant.slug,
        MerchantPlatformAuditSeed(
            merchant_slug=merchant.slug,
            provider=expected_platform(merchant.country_code).provider,
            status="ambiguous",
        ),
    )
    for merchant in MERCHANT_SEEDS
)
