"""Direct enrollment is link-only; provider traffic is always stubbed."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from pydantic import ValidationError

from app.affiliates.registry import PARTNERS_BY_CODE, partner_configured
from app.affiliates.service import AffiliateContext, TravelpayoutsLinkClient, resolve_partner_target
from app.config import Settings
from app.models import (
    DestinationAffiliateOffer,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services.channels import (
    channel_context,
    klook_affiliate_target,
    klook_canonical_target,
    klook_product_target,
    resolve_offer_target,
    same_klook_identity,
    verify_browser_target,
)
from app.travel_services.hotel_quotes import ADAPTERS
from app.travel_services.imports import parse_csv
from app.travel_services.schemas import BrandInput, Facts, ReviewInput
from app.travel_services.service import (
    public_product,
    ready_brand,
    ready_destination_offer,
    ready_offer,
)

TARGET = "https://www.klook.com/zh-TW/activity/12345-reviewed-fixture/"
EVIDENCE = "https://affiliate.klook.com/zh-TW/my_account"
AID = "134379"
NOW = datetime.now(UTC)


def enrollment(**changes):
    return TravelServiceBrand(
        **{
            "id": uuid4(),
            "channel": "klook_direct",
            "code": "klook",
            "project_id": AID,
            "enabled": True,
            "approval": "approved",
            "verified_at": NOW,
            **changes,
        }
    )


def settings(**changes):
    return Settings(klook_enabled=True, klook_affiliate_id=AID, **changes)


@pytest.mark.parametrize(
    "url",
    [
        "https://s.klook.com/a",
        "https://klook.com/activity/1",
        "https://evil.klook.com/activity/1",
        "https://www.klook.com.evil.test/activity/1",
        "http://www.klook.com/activity/1",
        "https://www.klook.com:8443/activity/1",
        "https://user@www.klook.com/activity/1",
        "https://www.klook.com/redirect?url=https%3A%2F%2Fevil.test",
        "https://www.klook.com/activity/1?redirect_url=%2F%2Fevil.test",
        "https://www.klook.com/activity/1?url=https%253A%252F%252Fevil.test",
        "https://www.klook.com/activity/1?next=other",
        "https://www.klook.com/activity/1?aid=2",
        "https://www.klook.com/activity/1?aid=134379&aid=2",
        "https://www.klook.com/activity/1?aid=134379&AID=134379",
        "https://www.klook.com/activity/1?%2561id=134379",
        "https://www.klook.com/activity/1?spm=anotherpartner",
        "https://www.klook.com/%252e%252e/redirect",
        "https://www.klook.com//evil.test",
        "https://www.klook.com/%5c%5cevil.test",
        "https://www.klook.com/activity/1?query=%250afoo",
    ],
)
def test_direct_targets_reject_ambiguous_tracking_and_redirects(url):
    with pytest.raises(ValueError):
        klook_affiliate_target(url, AID)


def test_direct_target_preserves_identity_and_own_aid_without_user_tracking():
    original = TARGET + "?query=Tokyo%20Tower"
    target = klook_affiliate_target(original, AID)
    assert urlsplit(target).path == urlsplit(original).path
    assert parse_qs(urlsplit(target).query) == {"query": ["Tokyo Tower"], "aid": [AID]}
    assert klook_affiliate_target(target, AID) == target
    assert klook_canonical_target(target, AID) == TARGET + "?query=Tokyo+Tower"
    with pytest.raises(ValueError):
        klook_canonical_target(target)


@pytest.mark.parametrize("aid", ["0", "-1", "123&aid=9", "abc", " 134379", "1" * 21])
def test_aid_has_one_numeric_identity(aid):
    with pytest.raises(ValidationError):
        Settings(klook_affiliate_id=aid)
    with pytest.raises(ValueError):
        klook_affiliate_target(TARGET, aid)


def test_empty_aid_and_pricing_key_are_not_enrollment():
    assert Settings(klook_affiliate_id="").klook_affiliate_id is None
    assert not partner_configured(PARTNERS_BY_CODE["klook"], Settings(klook_api_key="not-approval"))
    assert partner_configured(PARTNERS_BY_CODE["klook"], settings())
    assert "klook" not in ADAPTERS


def test_enrollment_evidence_and_browser_attestation_are_separate():
    value = dict(code="klook", approval="approved", enabled=True, evidence_url=EVIDENCE)
    assert BrandInput(channel="klook_direct", **value).channel == "klook_direct"
    with pytest.raises(ValidationError):
        BrandInput(**value)
    with pytest.raises(ValidationError):
        BrandInput(channel="klook_direct", **{**value, "code": "kkday"})
    with pytest.raises(ValidationError):
        BrandInput(channel="klook_direct", **{**value, "evidence_url": TARGET})
    with pytest.raises(ValidationError):
        ReviewInput(version=1, status="approved", browser_verified=True)


def test_exact_product_paths_cannot_be_destination_discovery():
    assert klook_product_target(TARGET, "tour") == TARGET
    assert klook_product_target("https://www.klook.com/zh-TW/hotels/285841", "hotel")
    assert klook_product_target(
        "https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/", "hotel"
    )
    assert same_klook_identity(
        "https://www.klook.com/zh-TW/hotels/285841",
        "https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/",
    )
    assert not same_klook_identity(
        "https://www.klook.com/zh-TW/hotels/285841",
        "https://www.klook.com/zh-TW/hotels/detail/285842-wrong-hotel/",
    )
    for target, kind in [
        (TARGET, "hotel"),
        ("https://www.klook.com/hotels/", "hotel"),
        ("https://www.klook.com/zh-TW/search/", "tour"),
    ]:
        with pytest.raises(ValueError):
            klook_product_target(target, kind)


def test_direct_readiness_isolated_from_tp_and_revoked_aid():
    direct = enrollment()
    config = settings(travelpayouts_enabled=False)
    product = TravelServiceProduct(
        id=uuid4(),
        source_key="fixture:klook:1",
        kind="tour",
        destination_id="tokyo",
        title="Test fixture",
        status="approved",
        names_json={},
        facts=Facts().model_dump(),
        source_url=TARGET,
    )
    offer = TravelServiceOffer(
        id=uuid4(),
        brand_id=direct.id,
        product_id=product.id,
        target_url=TARGET,
        scope="product",
        status="approved",
        verified_at=NOW,
        verification_context=channel_context(config, "klook_direct"),
    )
    assert ready_offer(offer, direct, product, config, NOW)
    assert not ready_brand(enrollment(channel="travelpayouts"), config, NOW)
    assert not ready_brand(direct, config.model_copy(update={"klook_affiliate_id": "2"}), NOW)
    assert not ready_brand(direct, config.model_copy(update={"klook_enabled": False}), NOW)
    assert not ready_brand(enrollment(verified_at=NOW - timedelta(days=31)), config, NOW)
    offer.verification_context = channel_context(config)
    assert not ready_offer(offer, direct, product, config, NOW)
    offer.verification_context = channel_context(config, "klook_direct")
    offer.static_url = "https://tp.st/fixture"
    assert not ready_offer(offer, direct, product, config, NOW)
    offer.static_url = None
    offer.target_url = "https://www.klook.com/hotels/"
    assert not ready_offer(offer, direct, product, config, NOW)
    destination = DestinationAffiliateOffer(
        brand_id=direct.id,
        module="hotel",
        target_url=offer.target_url,
        status="approved",
        verified_at=NOW,
        verification_context=channel_context(config, "klook_direct"),
    )
    assert ready_destination_offer(destination, direct, config, NOW)
    destination.expires_at = NOW
    assert not ready_destination_offer(destination, direct, config, NOW)
    product.kind = "hotel"
    product.facts = Facts(reference_price=999, currency="TWD", price_checked_at=NOW).model_dump(
        mode="json"
    )
    assert public_product(product, "en", NOW)["facts"]["reference_price"] is None


async def test_direct_resolution_never_calls_tp_or_a_price_api(monkeypatch):
    create = AsyncMock(side_effect=AssertionError("Direct Klook must not call Travelpayouts"))
    monkeypatch.setattr(TravelpayoutsLinkClient, "create", create)
    direct = enrollment()
    offer = TravelServiceOffer(target_url=TARGET)
    target = await resolve_offer_target(
        offer, direct, settings(), None, "svc_tour_tokyo_en_trip", cache_context="fixture"
    )
    assert target == TARGET + "?aid=" + AID
    create.assert_not_awaited()
    with pytest.raises(ValueError):
        await resolve_offer_target(
            offer,
            direct,
            settings().model_copy(update={"klook_affiliate_id": "2"}),
            None,
            "fixture",
            cache_context="fixture",
        )


async def test_generic_template_encodes_context_without_tracking_injection():
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    config = settings(
        klook_affiliate_url_template="https://www.klook.com/search/?query={query}&campaign={sub_id}"
    )
    target = await resolve_partner_target(
        PARTNERS_BY_CODE["klook"],
        AffiliateContext("hotel", "Tokyo&aid=99", None, None, "private-user-id"),
        config,
        redis,
    )
    assert parse_qs(urlsplit(target).query) == {
        "query": ["Tokyo&aid=99"],
        "campaign": ["aff_hotel_zh-TW"],
        "aid": [AID],
    }
    assert "private-user-id" not in target
    await redis.aclose()


async def test_browser_review_requires_same_exact_url_and_safe_dns(monkeypatch):
    dns = AsyncMock(return_value=("https://93.184.216.34/", "www.klook.com"))
    monkeypatch.setattr("app.catalog_review.evidence.public_request_target", dns)
    assert await verify_browser_target(enrollment(), TARGET, TARGET + "?aid=" + AID, settings())
    assert not await verify_browser_target(enrollment(), TARGET, TARGET + "other/", settings())
    assert not await verify_browser_target(
        enrollment(channel="travelpayouts"), TARGET, TARGET, settings()
    )
    dns.return_value = None
    assert not await verify_browser_target(enrollment(), TARGET, TARGET, settings())


def test_csv_channel_defaults_and_direct_canonical_product_scope():
    header = "source_key,kind,destination_id,title,source_url,brand,target_url,channel\n"
    row = f"klook:1,tour,tokyo,Test fixture,{TARGET},klook,{TARGET},"
    assert parse_csv(header + row)[0]["offer"]["channel"] == "travelpayouts"
    assert parse_csv(header + row + "klook_direct")[0]["offer"]["channel"] == "klook_direct"
    assert "error" in parse_csv(header + row + "unknown")[0]
    assert (
        "error"
        in parse_csv(
            header + row.replace(TARGET, "https://www.klook.com/search/") + "klook_direct"
        )[0]
    )


@pytest.mark.parametrize(
    "failure", [None, "wrong_hotel", "short_host", "foreign_aid", "private_dns"]
)
async def test_direct_network_checks_final_response_and_same_hotel_id(monkeypatch, failure):
    from app.travel_services import network

    start = "https://www.klook.com/zh-TW/hotels/285841"
    final = "https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/"
    if failure == "wrong_hotel":
        final = final.replace("285841", "285842")
    if failure == "short_host":
        final = final.replace("www.klook.com", "s.klook.com")
    if failure == "foreign_aid":
        final += "?aid=9"
    requested = []

    async def resolve(url):
        if failure == "private_dns" and url == final:
            return None
        return url, httpx.URL(url).host

    def respond(request):
        requested.append(request)
        assert request.headers["host"] == "www.klook.com"
        assert request.extensions["sni_hostname"] == "www.klook.com"
        if len(requested) == 1:
            return httpx.Response(302, headers={"location": final})
        return httpx.Response(200)

    original = httpx.AsyncClient
    monkeypatch.setattr(network, "public_request_target", resolve)
    monkeypatch.setattr(
        network.httpx,
        "AsyncClient",
        lambda **kwargs: original(transport=httpx.MockTransport(respond), **kwargs),
    )
    if failure in ("short_host", "foreign_aid"):
        with pytest.raises(ValueError):
            await network.verify_link(start + "?aid=" + AID, "klook", start, klook_affiliate_id=AID)
        assert len(requested) == 1
    else:
        result = await network.verify_link(
            start + "?aid=" + AID, "klook", start, klook_affiliate_id=AID
        )
        assert result is (failure is None)
        assert len(requested) == (1 if failure == "private_dns" else 2)


@pytest.mark.parametrize("failure", [None, "wrong_hotel", "category", "subdomain", "query"])
async def test_hotel_option_health_allows_only_safe_klook_property_alias(monkeypatch, failure):
    from app.travel_services import network
    from app.travel_services.schemas import HotelLink

    start = "https://www.klook.com/zh-TW/hotels/285841?check_in=2026-11-11"
    final = "https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/?check_in=2026-11-11&dd_referrer="
    if failure == "wrong_hotel":
        final = final.replace("285841", "285842")
    elif failure == "category":
        final = "https://www.klook.com/zh-TW/hotels/"
    elif failure == "subdomain":
        final = final.replace("www.klook.com", "s.klook.com")
    elif failure == "query":
        final = final.replace("2026-11-11", "2026-11-12")
    requests = []

    async def pinned(url):
        return url, httpx.URL(url).host

    def response(request):
        requests.append(request)
        return (
            httpx.Response(302, headers={"location": final})
            if len(requests) == 1
            else httpx.Response(200)
        )

    original = httpx.AsyncClient
    monkeypatch.setattr(network, "public_request_target", pinned)
    monkeypatch.setattr(
        network.httpx,
        "AsyncClient",
        lambda **kwargs: original(transport=httpx.MockTransport(response), **kwargs),
    )
    result = await network.check_hotel_link(
        HotelLink(provider="klook", url=start, evidence_url=start)
    )
    assert result == ("healthy" if failure is None else "unsafe")
    if failure == "subdomain":
        assert len(requests) == 1


def test_hotel_offer_aliases_preserve_bidirectional_query_identity():
    from app.travel_services.hotel_options import same_hotel_target

    short = "https://www.klook.com/zh-TW/hotels/285841"
    detail = "https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/"
    assert same_hotel_target("klook", short, detail)
    assert same_hotel_target("klook", detail, short)
    assert not same_hotel_target("klook", short + "?check_in=2026-11-11", detail)
    assert not same_hotel_target("klook", short, detail + "?check_in=2026-11-11")
    assert not same_hotel_target("klook", short, detail.replace("285841", "285842"))
    assert not same_hotel_target("klook", short, "https://www.klook.com/zh-TW/hotels/")
    assert not same_hotel_target("booking", short, detail)
