"""Ordinary hotel links use reviewed identities, never affiliate credentials."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from pydantic import ValidationError

from app.models import TravelServiceProduct
from app.travel_services import network
from app.travel_services.schemas import CatalogConfig, Facts, HotelLink, ProductInput
from app.travel_services.service import public_product, ready_hotel_links


def hotel_link(**updates):
    return HotelLink.model_validate(
        {
            "provider": "official",
            "url": "https://hotel.example.com/stay",
            "evidence_url": "https://hotel.example.com/location",
            **updates,
        }
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://hotel.example.com/stay",
        "https://127.0.0.1/stay",
        "https://hotel.local/stay",
        "https://user:secret@hotel.example.com/stay",
        "https://hotel.example.com:8443/stay",
        "https://hotel.example.com/stay?aid=123",
        "https://hotel.example.com/stay?utm_medium=affiliate",
        "https://hotel.example.com/stay?redirect=https%3A%2F%2Fevil.example.com",
        "https://booking.com/hotel/foo",
        "https://klook.tpx.gr/foo",
        "https://tp.st/foo",
    ],
)
def test_reject_unsafe_or_disguised_affiliate_urls(url):
    with pytest.raises(ValidationError):
        hotel_link(url=url, evidence_url=url)


def test_exact_platform_host_and_official_evidence_required():
    assert hotel_link(provider="booking", url="https://www.booking.com/hotel/jp/test.html")
    for value in ("https://www.booking.com/", "https://booking.com.evil.example.com/hotel"):
        with pytest.raises(ValidationError):
            hotel_link(provider="booking", url=value)
    with pytest.raises(ValidationError):
        hotel_link(evidence_url="https://unrelated.example.com/location")
    with pytest.raises(ValidationError):
        Facts(hotel_links=[hotel_link(), hotel_link()])
    with pytest.raises(ValidationError):
        ProductInput(
            source_key="test",
            kind="tour",
            destination_id="tokyo",
            title="Test",
            source_url="https://hotel.example.com/",
            facts=Facts(hotel_links=[hotel_link()]),
        )


def test_direct_link_freshness_flag_and_public_data_minimization():
    now = datetime.now(UTC)
    product = TravelServiceProduct(
        id=uuid4(),
        kind="hotel",
        title="Example",
        names_json={},
        destination_id="tokyo",
        source_url="https://hotel.example.com/",
        status="approved",
        verified_at=now,
        facts=Facts(
            hotel_links=[hotel_link()], reference_price=999, currency="USD", price_checked_at=now
        ).model_dump(mode="json"),
    )
    config = CatalogConfig(
        enabled_kinds=["hotel"], enabled_destinations=["tokyo"], direct_hotel_links_enabled=True
    )
    assert ready_hotel_links(product, config, now) == [hotel_link()]
    assert not ready_hotel_links(product, CatalogConfig(), now)
    assert not ready_hotel_links(product, config, now + timedelta(days=30, seconds=1))
    assert not ready_hotel_links(product, config, now - timedelta(seconds=1))
    public = public_product(product, "ja", now)
    assert "hotel_links" not in public["facts"]
    assert public["facts"]["reference_price"] is None
    assert public["facts"]["currency"] is None
    assert public["direct_links"] == []  # Only recommendations attaches eligible links.
    product.status = "pending"
    assert not ready_hotel_links(product, config, now)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "location,expected",
    [
        (None, True),
        ("https://www.hotel.example.com/stay", True),
        ("https://private.example.com/stay", False),
        ("https://hotel.example.com/other-hotel", False),
        ("https://hotel.example.com/stay?aid=123", False),
        ("http://hotel.example.com/stay", False),
        ("https://hotel.example.com/stay?url=https://evil.example.com", False),
    ],
)
async def test_dns_pinned_redirect_chain(monkeypatch, location, expected):
    calls = []

    def handle(request):
        calls.append(request)
        assert request.headers["host"] == "hotel.example.com"
        assert request.extensions["sni_hostname"] == "hotel.example.com"
        if location and len(calls) == 1:
            return httpx.Response(302, headers={"Location": location})
        return httpx.Response(200)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handle))
    monkeypatch.setattr(network.httpx, "AsyncClient", lambda **kwargs: client)
    monkeypatch.setattr(
        network,
        "public_request_target",
        AsyncMock(return_value=("https://93.184.216.34/stay", "hotel.example.com")),
    )
    try:
        actual = await network.verify_hotel_link(hotel_link())
    except ValueError:
        actual = False
    assert actual is expected


@pytest.mark.asyncio
async def test_private_dns_never_requested(monkeypatch):
    monkeypatch.setattr(network, "public_request_target", AsyncMock(return_value=None))
    assert not await network.verify_hotel_link(hotel_link())


@pytest.mark.asyncio
async def test_mismatch_identity_query_or_status_rejected(monkeypatch):
    client = httpx.AsyncClient(transport=httpx.MockTransport(lambda req: httpx.Response(404)))
    monkeypatch.setattr(network.httpx, "AsyncClient", lambda **kwargs: client)
    monkeypatch.setattr(
        network,
        "public_request_target",
        AsyncMock(return_value=("https://93.184.216.34/stay", "hotel.example.com")),
    )
    assert not await network.verify_hotel_link(hotel_link())
