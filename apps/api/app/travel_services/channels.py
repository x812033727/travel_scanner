"""Explicit affiliate enrollment channels; never a product or price API adapter."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from app.config import Settings
from app.i18n import active_locale
from app.models import DestinationAffiliateOffer, TravelServiceBrand, TravelServiceOffer
from app.travel_services.registry import affiliate_click_target, affiliate_target, brand_target
from app.travel_services.schemas import safe_url


def channel_for(brand: TravelServiceBrand) -> str:
    # SQL defaults apply on flush; legacy callers also construct transient brand objects.
    return brand.channel or "travelpayouts"


def channel_project(settings: Settings, channel: str) -> str | None:
    if channel == "travelpayouts":
        return settings.travelpayouts_project_id
    if channel == "klook_direct":
        return settings.klook_affiliate_id
    return None


def channel_context(settings: Settings, channel: str = "travelpayouts") -> str:
    # Keep existing Travelpayouts review hashes valid during migration.
    parts = (
        [settings.travelpayouts_project_id, settings.travelpayouts_marker]
        if channel == "travelpayouts"
        else [channel, settings.klook_affiliate_id]
    )
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()


def klook_canonical_target(value: str, affiliate_id: str | None = None) -> str:
    """Validate an exact official origin and remove only our own optional AID.

    Neither short links nor redirect endpoints prove an affiliate product identity.
    No caller-controlled URL, identity, tracking ID, or nested redirect is accepted.
    """
    value = safe_url(value)
    parsed = urlsplit(value)
    if parsed.hostname != "www.klook.com":
        raise ValueError("Direct Klook links require www.klook.com")
    decoded = unquote(unquote(parsed.path))
    if (
        any(ord(c) < 33 for c in decoded)
        or "\\" in decoded
        or "//" in decoded
        or any(p in (".", "..") for p in decoded.split("/"))
        or re.search(
            r"(?:^|/)(?:redirect|redirector|redirects|out|click|login|logout|auth)(?:/|$)",
            decoded,
            re.I,
        )
    ):
        raise ValueError("Direct Klook destination required")
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    seen: set[str] = set()
    retained: list[tuple[str, str]] = []
    for key, item in pairs:
        normalized = unquote(key).casefold()
        if normalized in seen:
            raise ValueError("Duplicate Klook query parameter")
        seen.add(normalized)
        if normalized == "aid":
            if key != "aid" or not affiliate_id or item != affiliate_id:
                raise ValueError("Foreign or unverified Klook AID")
            continue
        if (
            normalized.startswith("utm_")
            or normalized
            in {
                "url",
                "redirect",
                "redirect_url",
                "redirect_uri",
                "redirecturl",
                "return",
                "return_url",
                "returnurl",
                "next",
                "continue",
                "target",
                "dest",
                "destination",
                "callback",
                "callback_url",
                "goto",
                "link",
                "u",
                "r",
                "marker",
                "trs",
                "cid",
                "aff",
                "affiliate",
                "affiliate_id",
                "aff_id",
                "sub_id",
                "subid",
                "tag",
                "sid",
                "clickid",
                "irclickid",
                "partner_id",
                "ref",
                "refid",
                "spm",
            }
            or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", key)
            or any(ord(c) < 32 for c in unquote(item))
            or re.search(r"(?:https?:|//|\\)", unquote(unquote(item)), re.I)
        ):
            raise ValueError("Untracked Klook destination required")
        retained.append((key, item))
    return urlunsplit(("https", "www.klook.com", parsed.path, urlencode(retained), ""))


def klook_affiliate_target(value: str, affiliate_id: str) -> str:
    if not re.fullmatch(r"[1-9][0-9]{0,19}", affiliate_id):
        raise ValueError("Klook AID required")
    canonical = urlsplit(klook_canonical_target(value, affiliate_id))
    query = parse_qsl(canonical.query, keep_blank_values=True) + [("aid", affiliate_id)]
    return urlunsplit(canonical._replace(query=urlencode(query)))


def validate_offer_target(brand: TravelServiceBrand, target: str, static_url: str | None) -> str:
    if channel_for(brand) == "klook_direct":
        if brand.code != "klook" or static_url:
            raise ValueError("Direct Klook uses an original canonical destination only")
        return klook_canonical_target(target)
    target = brand_target(brand.code, target)
    if static_url:
        affiliate_target(static_url)
    return target


def klook_product_target(value: str, kind: str) -> str:
    target = klook_canonical_target(value)
    section = "hotels" if kind == "hotel" else "activity"
    identity = klook_product_identity(target)
    if not identity or identity[0] != section:
        raise ValueError("Exact Klook product identity required")
    return target


def klook_product_identity(value: str) -> tuple[str, str] | None:
    target = klook_canonical_target(value)
    match = re.fullmatch(
        r"/(?:[a-z]{2}(?:-[A-Za-z]{2})?/)?(hotels|activity)/(?:detail/)?"
        r"([1-9][0-9]*)(?:-[^/]+)?/?",
        urlsplit(target).path,
    )
    return (match[1], match[2]) if match else None


def same_klook_identity(expected: str, actual: str) -> bool:
    """A hotel's short/detail aliases must keep the provider's numeric identity."""
    expected_identity, actual_identity = (
        klook_product_identity(expected),
        klook_product_identity(actual),
    )
    same_path = (
        expected_identity == actual_identity
        if expected_identity is not None
        else urlsplit(expected).path.rstrip("/") == urlsplit(actual).path.rstrip("/")
    )
    expected_query = dict(parse_qsl(urlsplit(expected).query, keep_blank_values=True))
    actual_query = dict(parse_qsl(urlsplit(actual).query, keep_blank_values=True))
    return same_path and all(
        actual_query.get(key) == value for key, value in expected_query.items()
    )


async def verify_browser_target(
    brand: TravelServiceBrand, target: str, evidence_url: str | None, settings: Settings
) -> bool:
    from app.catalog_review.evidence import public_request_target

    if channel_for(brand) != "klook_direct" or not evidence_url:
        return False
    expected = klook_canonical_target(target)
    evidence = klook_canonical_target(evidence_url, settings.klook_affiliate_id)
    return (
        same_klook_identity(expected, evidence)
        and await public_request_target(expected) is not None
    )


async def resolve_offer_target(
    offer: TravelServiceOffer | DestinationAffiliateOffer,
    brand: TravelServiceBrand,
    settings: Settings,
    redis: Any,
    sub_id: str,
    *,
    cache_context: str,
) -> str:
    from app.affiliates.service import TravelpayoutsLinkClient
    from app.affiliates.sub_id import coarse_sub_id, safe_sub_id

    # The other egress. This path reaches the Travelpayouts Links API directly, so the
    # gate in resolve_partner_target never sees it; without this line a caller could
    # transmit any string it liked.
    sub_id = safe_sub_id(sub_id, rebuild=coarse_sub_id("svc", "offer", None, active_locale()))
    target = validate_offer_target(brand, offer.target_url, offer.static_url)
    if channel_for(brand) == "klook_direct":
        if not settings.klook_enabled or brand.project_id != settings.klook_affiliate_id:
            raise ValueError("Klook enrollment is unavailable")
        return klook_affiliate_target(target, settings.klook_affiliate_id or "")
    return affiliate_click_target(
        brand.code,
        offer.static_url
        or await TravelpayoutsLinkClient(redis, settings).create(
            target, sub_id, cache_context=cache_context
        ),
    )
