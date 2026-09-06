"""A trip cover may only point at hosts this product already shows images from."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.trips.router import TripMetadataPatchRequest, cover_image_host_allowed


def patch(url: str | None) -> TripMetadataPatchRequest:
    return TripMetadataPatchRequest(version=1, cover_image_url=url)


@pytest.mark.parametrize(
    "url",
    [
        "https://i.ytimg.com/vi/abc/hqdefault.jpg",
        "https://lh3.googleusercontent.com/places/photo.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/ab/Sensoji.jpg",
        "https://www.mokaair.com/covers/tokyo.jpg",
    ],
)
def test_an_image_from_a_host_we_already_show_is_accepted(url: str) -> None:
    assert patch(url).cover_image_url == url
    assert cover_image_host_allowed(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://i.ytimg.com/vi/abc/hqdefault.jpg",
        "https://example.com/anything.jpg",
        "https://evil.i.ytimg.com.attacker.test/x.jpg",
        "https://mokaair.com.attacker.test/x.jpg",
        "javascript:alert(1)",
        "https://192.168.0.1/internal.jpg",
    ],
)
def test_anything_else_is_refused(url: str) -> None:
    assert not cover_image_host_allowed(url)
    with pytest.raises(ValidationError):
        patch(url)


def test_a_blank_cover_clears_it_rather_than_failing() -> None:
    assert patch("   ").cover_image_url is None
    assert patch(None).cover_image_url is None
