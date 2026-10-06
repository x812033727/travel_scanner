"""POST /video/media/stock/*: what is asked of Pexels and Pixabay, what comes back, where it goes.

The vendors are never called: every HTTP exchange goes through ``httpx.MockTransport`` the way
test_video_media_locate.py does, with answers shaped like the vendors' public documentation.
"""

from __future__ import annotations

import copy
import hashlib
import io
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis
import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from PIL import Image

from app.admin import service as admin_service
from app.admin.service import apply_runtime_overrides, card_state
from app.config import Settings, official_provider_url_ok
from app.db import get_session
from app.models import ProviderConfig, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.models import DEFAULT_DRAMA, DEFAULT_SLIDES, VideoAutomationSettings
from app.video_media import admin_api, meter, stock
from app.video_media.jobs import MediaContext
from app.video_media.schemas import (
    StockCandidate,
    StockCredit,
    StockFetchIn,
    StockFetchOut,
    StockSearchIn,
    StockSearchOut,
)
from app.video_media.settings import MediaSettings
from app.video_media.stock import (
    IMAGE_TYPES,
    PROBE_QUERY,
    StockError,
    configured,
    fetch,
    pexels_photo,
    pixabay_photo,
    probe,
    search,
    search_request,
    vendors,
)
from app.video_media.storage import MediaStore
from app.video_reviews.storage import StorageRefused
from app.video_speech import admin_api as speech_api
from tests.test_security_config import secure_production_settings

MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 24
BOTH = Settings(pexels_api_key="pex-key", pixabay_api_key="pix-key")


def _image(kind: str, width: int = 64, height: int = 36) -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (width, height), (10, 20, 30)).save(out, format=kind)
    return out.getvalue()


def _pexels(photo_id: int = 3573351, **changes: Any) -> dict[str, Any]:
    """A photo object as https://www.pexels.com/api/documentation describes one."""
    photo = {
        "id": photo_id,
        "width": 3066,
        "height": 3968,
        "url": f"https://www.pexels.com/photo/seoul-at-night-{photo_id}/",
        "photographer": "Lukas Rodriguez",
        "photographer_url": "https://www.pexels.com/@lukas-rodriguez-1845331",
        "photographer_id": 1845331,
        "avg_color": "#374824",
        "src": {
            "original": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.png",
            "large2x": f"https://images.pexels.com/photos/{photo_id}/p.png?w=940&h=650&dpr=2",
            "large": f"https://images.pexels.com/photos/{photo_id}/p.png?w=940&h=650",
            "medium": f"https://images.pexels.com/photos/{photo_id}/p.png?h=350",
            "small": f"https://images.pexels.com/photos/{photo_id}/p.png?h=130",
            "tiny": f"https://images.pexels.com/photos/{photo_id}/p.png?w=280&h=200",
        },
        "liked": False,
        "alt": "Seoul skyline at night",
    }
    photo.update(changes)
    return photo


def _pixabay(photo_id: int = 195893, **changes: Any) -> dict[str, Any]:
    """A hit as https://pixabay.com/api/docs describes one, with full API access fields."""
    hit = {
        "id": photo_id,
        "pageURL": f"https://pixabay.com/photos/seoul-korea-{photo_id}/",
        "type": "photo",
        "tags": "seoul, korea, city",
        "previewURL": f"https://cdn.pixabay.com/photo/2013/10/15/09/12/seoul-{photo_id}_150.jpg",
        "previewWidth": 150,
        "previewHeight": 84,
        "webformatURL": f"https://pixabay.com/get/{photo_id}_640.jpg",
        "webformatWidth": 640,
        "webformatHeight": 360,
        "largeImageURL": f"https://pixabay.com/get/{photo_id}_1280.jpg",
        "fullHDURL": f"https://pixabay.com/get/{photo_id}_1920.jpg",
        "imageURL": f"https://pixabay.com/get/{photo_id}.jpg",
        "imageWidth": 4000,
        "imageHeight": 2250,
        "imageSize": 4731420,
        "views": 7671,
        "downloads": 6439,
        "likes": 5,
        "comments": 2,
        "user_id": 48777,
        "user": "Josch13",
        "userImageURL": "https://cdn.pixabay.com/user/2013/11/05/02-10-23-764_250x250.jpg",
    }
    hit.update(changes)
    return hit


def test_the_keys_are_server_only_and_pinned_to_the_vendors_hosts() -> None:
    assert official_provider_url_ok("pexels_api_base_url", "https://api.pexels.com/v1")
    assert official_provider_url_ok("pixabay_api_base_url", "https://pixabay.com/api/")
    assert not official_provider_url_ok("pexels_api_base_url", "https://evil.example.com/v1")
    assert not official_provider_url_ok("pixabay_api_base_url", "https://cdn.pixabay.com/api/")
    assert not official_provider_url_ok("pixabay_api_base_url", "http://pixabay.com/api/")
    # A key with a base URL off the vendor's host is refused at startup in production ...
    with pytest.raises(RuntimeError, match="PEXELS_API_BASE_URL"):
        secure_production_settings(
            pexels_api_key="k", pexels_api_base_url="https://evil.example.com/v1"
        ).validate_deployment_security()
    with pytest.raises(RuntimeError, match="PIXABAY_API_BASE_URL"):
        secure_production_settings(
            pixabay_api_key="k", pixabay_api_base_url="https://pixabay.example.com/api/"
        ).validate_deployment_security()
    secure_production_settings(
        pexels_api_key="k", pixabay_api_key="k"
    ).validate_deployment_security()
    # ... and one stored from the settings page is ignored, so the key never leaves the host.
    base = Settings(app_secret_key="test-app-secret-at-least-thirty-two-characters")
    row = ProviderConfig(
        provider="stock_photos",
        enabled=True,
        config={"pexels_api_base_url": "https://evil.example.com/v1"},
        secret_config_encrypted=admin_service.encrypt_secrets({"pexels_api_key": "db-key"}, base),
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.pexels_api_key == "db-key"
    assert effective.pexels_api_base_url == "https://api.pexels.com/v1"
    definition = admin_service.PROVIDER_DEFINITIONS["stock_photos"]
    assert definition.secret_fields == ("pexels_api_key", "pixabay_api_key")
    assert definition.config_fields == ("pexels_api_base_url", "pixabay_api_base_url")


def test_vendors_need_a_key_and_come_in_a_fixed_order() -> None:
    with pytest.raises(StockError) as nothing:
        vendors(Settings())
    assert (nothing.value.status, nothing.value.code) == (503, "video_media_stock_unavailable")
    assert "Pexels 或 Pixabay" in nothing.value.detail
    assert [v.name for v in vendors(BOTH)] == ["pexels", "pixabay"]
    assert [v.name for v in vendors(BOTH, "pixabay")] == ["pixabay"]
    assert [v.name for v in vendors(Settings(pixabay_api_key="p"))] == ["pixabay"]
    with pytest.raises(StockError) as missing:
        vendors(Settings(pexels_api_key="p"), "pixabay")
    assert missing.value.status == 503 and "Pixabay" in missing.value.detail
    pexels, pixabay = vendors(BOTH)
    assert (pexels.key, pexels.base, pexels.hosts) == (
        "pex-key",
        "https://api.pexels.com/v1",
        frozenset({"images.pexels.com"}),
    )
    assert (pixabay.key, pixabay.base) == ("pix-key", "https://pixabay.com/api")
    assert pixabay.hosts == frozenset({"pixabay.com", "cdn.pixabay.com"})
    assert configured(Settings(pexels_api_key="p")) == {"pexels": True, "pixabay": False}


def test_each_vendor_is_asked_the_way_its_documentation_says() -> None:
    pexels, pixabay = vendors(BOTH)
    payload = StockSearchIn(query="  Seoul   night market ", orientation="landscape", per_page=1)
    assert payload.query == "Seoul night market", "whitespace is folded; nothing else is touched"
    url, params, headers = search_request(pexels, payload)
    assert url == "https://api.pexels.com/v1/search"
    assert params == {
        "query": "Seoul night market",
        "per_page": 1,
        "page": 1,
        "orientation": "landscape",
    }
    assert headers == {"Authorization": "pex-key"}, "Pexels takes the key as a header"
    url, params, headers = search_request(pixabay, payload)
    assert url == "https://pixabay.com/api/"
    assert params == {
        "key": "pix-key",
        "q": "Seoul night market",
        "image_type": "photo",
        "safesearch": "true",
        "per_page": 3,
        "page": 1,
        "orientation": "horizontal",
    }, "Pixabay takes the key as a parameter, photos only, at least three a page"
    assert headers == {}
    portrait = search_request(pixabay, StockSearchIn(query="x", orientation="portrait"))[1]
    assert portrait["orientation"] == "vertical" and portrait["per_page"] == 15
    square = search_request(pixabay, StockSearchIn(query="x", orientation="square", page=3))[1]
    assert "orientation" not in square and square["page"] == 3, "Pixabay has no square filter"
    for body in (
        {"query": ""},
        {"query": "   "},
        {"query": "x" * 101},
        {"query": "x", "per_page": 0},
        {"query": "x", "per_page": 41},
        {"query": "x", "page": 0},
        {"query": "x", "provider": "getty"},
        {"query": "x", "orientation": "wide"},
    ):
        with pytest.raises(ValueError):
            StockSearchIn.model_validate(body)


def test_a_vendors_photo_becomes_a_candidate_with_the_credit_it_asks_for() -> None:
    photo = pexels_photo(_pexels())
    assert photo is not None
    assert photo.download == "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png"
    assert photo.candidate == StockCandidate(
        provider="pexels",
        id="3573351",
        width=3066,
        height=3968,
        thumbnail="https://images.pexels.com/photos/3573351/p.png?h=350",
        preview="https://images.pexels.com/photos/3573351/p.png?w=940&h=650",
        alt="Seoul skyline at night",
        credit=StockCredit(
            provider="pexels",
            author="Lukas Rodriguez",
            author_url="https://www.pexels.com/@lukas-rodriguez-1845331",
            url="https://www.pexels.com/photo/seoul-at-night-3573351/",
            license="Pexels License",
            license_url="https://www.pexels.com/license/",
            text="Photo by Lukas Rodriguez on Pexels",
        ),
    )
    hit = pixabay_photo(_pixabay())
    assert hit is not None
    assert hit.download == "https://pixabay.com/get/195893.jpg", "the original, with full access"
    assert hit.candidate == StockCandidate(
        provider="pixabay",
        id="195893",
        width=4000,
        height=2250,
        thumbnail="https://cdn.pixabay.com/photo/2013/10/15/09/12/seoul-195893_150.jpg",
        preview="https://pixabay.com/get/195893_640.jpg",
        alt="seoul, korea, city",
        credit=StockCredit(
            provider="pixabay",
            author="Josch13",
            author_url="https://pixabay.com/users/Josch13-48777/",
            url="https://pixabay.com/photos/seoul-korea-195893/",
            license="Pixabay Content License",
            license_url="https://pixabay.com/service/license-summary/",
            text="Image by Josch13 from Pixabay",
        ),
    )
    # A key without full API access gets neither the original nor the 1920 px file, and may
    # not get the original's size either: the 1280 px file and the webformat size stand in.
    plain = _pixabay()
    for field in ("imageURL", "fullHDURL", "imageWidth", "imageHeight", "imageSize", "user_id"):
        del plain[field]
    limited = pixabay_photo(plain)
    assert limited is not None
    assert limited.download == "https://pixabay.com/get/195893_1280.jpg"
    assert (limited.candidate.width, limited.candidate.height) == (640, 360)
    assert limited.candidate.credit.author_url is None
    # Anything a credit or a download needs that is missing or not https drops the photo.
    assert pexels_photo(_pexels(src={"medium": "https://images.pexels.com/x"})) is None
    assert pexels_photo(_pexels(photographer="")) is None
    assert pexels_photo(_pexels(url="http://www.pexels.com/photo/1/")) is None
    assert pexels_photo(_pexels(id="3573351")) is None
    assert pexels_photo(_pexels(width=0)) is None
    assert pexels_photo("photo") is None
    assert pixabay_photo(_pixabay(pageURL=None)) is None
    assert pixabay_photo(_pixabay(largeImageURL="", fullHDURL="", imageURL="")) is None
    assert pixabay_photo(_pixabay(user=" ")) is None


@pytest.mark.asyncio
async def test_search_asks_every_configured_vendor_and_names_the_one_that_failed() -> None:
    seen: list[httpx.Request] = []
    answers: dict[str, httpx.Response] = {
        "api.pexels.com": httpx.Response(
            200, json={"page": 1, "per_page": 1, "total_results": 8000, "photos": [_pexels()]}
        ),
        "pixabay.com": httpx.Response(
            200,
            json={
                "total": 4692,
                "totalHits": 500,
                "hits": [_pixabay(1), _pixabay(2), "junk", _pixabay(3, user="")],
            },
        ),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return answers[request.url.host]

    payload = StockSearchIn(query="Seoul", per_page=1)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        out = await search(BOTH, payload, client)
    assert out == StockSearchOut(
        query="Seoul",
        candidates=[pexels_photo(_pexels()).candidate, pixabay_photo(_pixabay(1)).candidate],  # type: ignore[union-attr]
        total={"pexels": 8000, "pixabay": 4692},
        problems=[],
    ), "vendor order, the vendor's order within, and only per_page from each"
    pexels_call, pixabay_call = seen
    assert pexels_call.url.path == "/v1/search" and pexels_call.url.params["query"] == "Seoul"
    assert pexels_call.headers["Authorization"] == "pex-key"
    assert "pex-key" not in str(pexels_call.url)
    assert pexels_call.headers["User-Agent"].startswith("Mokaair-video/")
    assert pixabay_call.url.path == "/api/" and pixabay_call.url.params["key"] == "pix-key"
    assert pixabay_call.url.params["per_page"] == "3"
    assert "Authorization" not in pixabay_call.headers
    # One vendor asked for explicitly: the other is not called.
    seen.clear()
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        only = await search(BOTH, StockSearchIn(query="Seoul", provider="pixabay"), client)
    assert [c.provider for c in only.candidates] == ["pixabay"] * 2 and len(seen) == 1
    # A vendor that fails while the other answers is named, not fatal ...
    answers["pixabay.com"] = httpx.Response(429, headers={"Retry-After": "30"})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        partial = await search(BOTH, payload, client)
    assert partial.total == {"pexels": 8000} and len(partial.candidates) == 1
    assert partial.problems == ["Pixabay 的額度用完或太忙"]
    # ... and the call fails with the first error only when no vendor answered.
    answers["api.pexels.com"] = httpx.Response(401, json={"error": "bad key"})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(StockError) as refused:
            await search(BOTH, payload, client)
    assert (refused.value.status, refused.value.code) == (502, "video_media_stock_failed")
    assert refused.value.detail == "Pexels 拒絕了網站的金鑰（HTTP 401）"
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(StockError) as busy:
            await search(BOTH, StockSearchIn(query="Seoul", provider="pixabay"), client)
    assert (busy.value.status, busy.value.code, busy.value.retry_after) == (
        429,
        "video_media_upstream_busy",
        "30",
    )
    assert "pix-key" not in busy.value.detail
    with pytest.raises(StockError) as no_key:
        await search(Settings(), payload)
    assert no_key.value.code == "video_media_stock_unavailable"

    def broken(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down")

    async with httpx.AsyncClient(transport=httpx.MockTransport(broken)) as client:
        with pytest.raises(StockError) as down:
            await search(Settings(pexels_api_key="p"), payload, client)
    assert down.value.detail == "Pexels unreachable: ConnectError"
    not_json = httpx.Response(200, content=b"<html>", headers={"content-type": "text/html"})
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r: not_json)) as client:
        with pytest.raises(StockError) as html:
            await search(Settings(pexels_api_key="p"), payload, client)
    assert html.value.detail == "Pexels 回的不是 JSON"


def _store(tmp_path: Path) -> MediaStore:
    return MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)


@pytest.mark.asyncio
async def test_fetch_streams_the_original_from_the_vendor_host_into_the_store(
    tmp_path: Path,
) -> None:
    png = _image("PNG", 64, 36)
    jpeg = _image("JPEG", 48, 48)
    store = _store(tmp_path)
    media = MediaSettings(video_media_dir=str(tmp_path))
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        host, path = request.url.host, request.url.path
        if host == "api.pexels.com":
            assert path == "/v1/photos/3573351"
            return httpx.Response(200, json=_pexels())
        if host == "images.pexels.com":
            return httpx.Response(200, content=png, headers={"content-type": "image/png"})
        if host == "pixabay.com" and path == "/api/":
            assert request.url.params["id"] == "195893"
            return httpx.Response(200, json={"total": 1, "totalHits": 1, "hits": [_pixabay()]})
        if host == "pixabay.com":
            return httpx.Response(200, content=jpeg, headers={"content-type": "image/jpeg"})
        raise AssertionError(f"unexpected call to {host}{path}")

    from_pexels = StockFetchIn(slug="seoul-guide", provider="pexels", id="3573351")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        out = await fetch(BOTH, media, store, from_pexels, client)
    sha = hashlib.sha256(png).hexdigest()
    assert out == StockFetchOut(
        sha256=sha,
        size=len(png),
        content_type="image/png",
        width=64,
        height=36,
        credit=pexels_photo(_pexels()).candidate.credit,  # type: ignore[union-attr]
    ), "the size is read from the stored bytes, not taken from the vendor's numbers"
    path = store.path("seoul-guide", sha)
    assert path is not None and path.read_bytes() == png
    assert not any((tmp_path / "seoul-guide" / ".incoming").iterdir())
    by_id, download = seen
    assert by_id.headers["Authorization"] == "pex-key"
    assert "Authorization" not in download.headers, "the file is public: no key goes to the CDN"
    assert download.headers["User-Agent"].startswith("Mokaair-video/")
    seen.clear()
    from_pixabay = StockFetchIn(slug="seoul-guide", provider="pixabay", id="195893")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        out = await fetch(BOTH, media, store, from_pixabay, client)
    assert (out.sha256, out.content_type, out.width, out.height) == (
        hashlib.sha256(jpeg).hexdigest(),
        "image/jpeg",
        48,
        48,
    )
    assert out.credit.text == "Image by Josch13 from Pixabay"
    assert seen[1].url == "https://pixabay.com/get/195893.jpg", "the original, with full access"
    assert "key" not in seen[1].url.params


@pytest.mark.asyncio
async def test_fetch_refuses_a_file_off_the_vendor_host_a_non_picture_and_an_unknown_photo(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)
    media = MediaSettings(video_media_dir=str(tmp_path))
    payload = StockFetchIn(slug="v", provider="pexels", id="3573351")
    state: dict[str, Any] = {"photo": _pexels(), "file": _image("PNG")}
    downloads: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "api.pexels.com":
            answer = state["photo"]
            if isinstance(answer, httpx.Response):
                return answer
            return httpx.Response(200, json=answer)
        downloads.append(request)
        return httpx.Response(200, content=state["file"])

    async def attempt() -> StockFetchOut:
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await fetch(BOTH, media, store, payload, client)

    elsewhere = _pexels()
    elsewhere["src"]["original"] = "https://evil.example.com/photos/3573351.png"
    state["photo"] = elsewhere
    with pytest.raises(StockError) as off_host:
        await attempt()
    assert off_host.value.status == 502 and "not on the vendor's host" in off_host.value.detail
    assert downloads == [], "nothing is fetched from a host the vendor does not own"
    state["photo"] = _pexels()
    state["file"] = MP4
    with pytest.raises(StorageRefused) as not_picture:
        await attempt()
    assert (not_picture.value.status, not_picture.value.code) == (
        415,
        "video_media_unsupported_type",
    )
    assert "video/mp4" in not_picture.value.detail
    state["file"] = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
    with pytest.raises(StockError) as unreadable:
        await attempt()
    assert unreadable.value.status == 502 and "讀不出尺寸" in unreadable.value.detail
    assert store.files("v") == {}, "a picture that cannot be read is not kept"
    state["photo"] = _pexels(99)
    state["file"] = _image("PNG")
    with pytest.raises(StockError) as other:
        await attempt()
    assert other.value.status == 502 and "另一張照片（99）" in other.value.detail
    state["photo"] = _pexels(src={})
    with pytest.raises(StockError) as incomplete:
        await attempt()
    assert incomplete.value.status == 502 and "不完整" in incomplete.value.detail
    state["photo"] = httpx.Response(404, json={"status": 404})
    with pytest.raises(StockError) as unknown:
        await attempt()
    assert (unknown.value.status, unknown.value.code) == (404, "video_media_stock_not_found")
    empty = httpx.Response(200, json={"total": 0, "totalHits": 0, "hits": []})
    from_pixabay = StockFetchIn(slug="v", provider="pixabay", id="1")
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r: empty)) as client:
        with pytest.raises(StockError) as none:
            await fetch(BOTH, media, store, from_pixabay, client)
    assert none.value.code == "video_media_stock_not_found"
    with pytest.raises(StockError) as no_key:
        await fetch(Settings(pexels_api_key="p"), media, store, from_pixabay)
    assert no_key.value.status == 503 and "Pixabay" in no_key.value.detail
    for body in (
        {"slug": "v", "provider": "pexels"},
        {"slug": "v", "provider": "pexels", "id": "abc"},
        {"slug": "v", "provider": "pexels", "id": "1" * 21},
        {"slug": "V", "provider": "pexels", "id": "1"},
        {"slug": "v", "provider": "unsplash", "id": "1"},
    ):
        with pytest.raises(ValueError):
            StockFetchIn.model_validate(body)


@pytest.mark.asyncio
async def test_the_store_takes_only_the_kinds_a_caller_accepts_under_a_safe_name(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)

    async def chunks(data: bytes) -> Any:
        yield data

    with pytest.raises(StorageRefused) as not_image:
        await store.put_stream("v", "stock-pexels-1", chunks(MP4), accept=IMAGE_TYPES)
    assert (not_image.value.status, not_image.value.code) == (415, "video_media_unsupported_type")
    assert "jpg、png、webp" in not_image.value.detail
    assert store.files("v") == {} and not any((tmp_path / "v" / ".incoming").iterdir())
    stored = await store.put_stream(
        "v", "stock-pexels-1", chunks(_image("WEBP")), accept=IMAGE_TYPES
    )
    assert stored.content_type == "image/webp" and store.path("v", stored.sha256) is not None
    for name in ("", "../x", ".hidden", "a/b", "x" * 121):
        with pytest.raises(StorageRefused) as bad:
            await store.put_stream("v", name, chunks(MP4))
        assert bad.value.code == "video_media_bad_name", name
    assert (await store.put_stream("v", str(uuid4()), chunks(MP4))).content_type == "video/mp4"


@pytest.mark.asyncio
async def test_the_connection_test_searches_each_vendor_once_and_reports_them_together(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[httpx.Request] = []
    answers: dict[str, httpx.Response] = {
        "api.pexels.com": httpx.Response(200, json={"total_results": 1234, "photos": [_pexels()]}),
        "pixabay.com": httpx.Response(200, json={"total": 56, "hits": [_pixabay()]}),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return answers[request.url.host]

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        message = await probe(BOTH, client)
    assert message == (
        f"Pexels ✓（「{PROBE_QUERY}」共 1,234 張）；Pixabay ✓（「{PROBE_QUERY}」共 56 張）"
    )
    assert [r.url.host for r in seen] == ["api.pexels.com", "pixabay.com"]
    assert seen[0].url.params["per_page"] == "1" and seen[1].url.params["per_page"] == "3"
    answers["pixabay.com"] = httpx.Response(403, text="[ERROR 403] forbidden")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(StockError) as failed:
            await probe(BOTH, client)
    assert failed.value.detail == (
        "Pixabay 驗證失敗：Pixabay 拒絕了網站的金鑰（HTTP 403）；"
        f"Pexels ✓（「{PROBE_QUERY}」共 1,234 張）"
    )
    answers["pixabay.com"] = httpx.Response(200, json={"total": 0, "hits": []})
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(StockError) as nothing:
            await probe(BOTH, client)
    assert "沒有回任何可用的照片" in nothing.value.detail
    with pytest.raises(StockError) as no_key:
        await probe(Settings())
    assert no_key.value.status == 503
    # The settings card: its status before any test, and the test wired through the service.
    assert "stock_photos" in admin_service.CONNECTION_TESTED_PROVIDERS
    configured_card = card_state(
        "stock_photos", BOTH, enabled=True, last_test_status=None, last_test_message=None
    )
    assert configured_card == (True, "unverified", "已設定：Pexels、Pixabay；尚未執行連線測試")
    assert card_state(
        "stock_photos", Settings(), enabled=True, last_test_status=None, last_test_message=None
    ) == (False, "not_configured", "尚未設定 Pexels 或 Pixabay 的金鑰；設定任一家就能搜尋")
    assert card_state(
        "stock_photos",
        Settings(pixabay_api_key="p"),
        enabled=True,
        last_test_status="success",
        last_test_message=None,
    ) == (True, "ready", "已設定：Pixabay")
    asked: list[Settings] = []

    async def fake_probe(runtime: Settings, client: Any = None) -> str:
        asked.append(runtime)
        return "Pexels ✓"

    monkeypatch.setattr(stock, "probe", fake_probe)
    assert await admin_service._test_provider("stock_photos", BOTH, object()) == "Pexels ✓"  # type: ignore[arg-type]
    assert asked == [BOTH]
    monkeypatch.undo()
    with pytest.raises(ConnectionError, match="金鑰還沒設定"):
        await admin_service._test_provider("stock_photos", Settings(), object())  # type: ignore[arg-type]


# The routes, on the same fakes as test_video_media_locate.py: a context the test owns, no rate
# limit, a fake Redis.


def _app(token: VideoToolToken | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.media_router, prefix="/api/v1")

    async def session() -> Any:
        fake = AsyncMock()
        fake.scalar = AsyncMock(return_value=None)
        yield fake

    app.dependency_overrides[get_session] = session
    if token is not None:
        app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


def _row(**changes: Any) -> VideoAutomationSettings:
    return VideoAutomationSettings(
        id=1,
        **{
            **copy.deepcopy(DEFAULT_DRAMA),
            **copy.deepcopy(DEFAULT_SLIDES),
            "drama_enabled": True,
            **changes,
        },
    )


@pytest.fixture
def media(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    settings = MediaSettings(video_media_dir=str(tmp_path))
    store = MediaStore(
        tmp_path,
        max_file_bytes=settings.video_media_max_file_bytes,
        max_total_bytes=settings.video_media_max_total_bytes,
    )
    state: dict[str, Any] = {
        "row": _row(),
        "store": store,
        "redis": fakeredis.aioredis.FakeRedis(),
        "settings": settings,
        "limits": AsyncMock(),
        "runtime": Settings(hotspot_guide_gemini_api_key="g"),
        "prune": AsyncMock(),
    }

    async def context(session: Any, token_id: Any) -> MediaContext:
        return MediaContext(
            session=session,
            redis=state["redis"],
            store=store,
            runtime=state["runtime"],
            media=settings,
            row=state["row"],
            token_id=token_id,
        )

    monkeypatch.setattr(admin_api, "_context", context)
    monkeypatch.setattr(admin_api, "get_media_settings", lambda: settings)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", state["limits"])
    monkeypatch.setattr(admin_api, "prune", state["prune"])
    monkeypatch.setattr(meter, "month_usd", AsyncMock(return_value=0.0))
    return state


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")


@pytest.mark.asyncio
async def test_the_routes_need_a_token_and_validate_the_body() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        for path in ("/stock/search", "/stock/fetch"):
            anonymous = await client.post(f"/api/v1/video/media{path}", json={})
            assert anonymous.status_code == 401, path
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        for path, body in (
            ("/stock/search", {}),
            ("/stock/search", {"query": " "}),
            ("/stock/search", {"query": "Seoul", "per_page": 41}),
            ("/stock/search", {"query": "Seoul", "provider": "getty"}),
            ("/stock/search", {"query": "Seoul", "slug": "v"}),
            ("/stock/fetch", {"slug": "v", "provider": "pexels"}),
            ("/stock/fetch", {"slug": "v", "provider": "pexels", "id": "x"}),
        ):
            response = await client.post(f"/api/v1/video/media{path}", json=body)
            assert response.status_code == 422, (path, body)


@pytest.mark.asyncio
async def test_the_routes_search_and_fetch_without_a_budget_and_say_so_on_status(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = pexels_photo(_pexels()).candidate  # type: ignore[union-attr]
    searched: list[StockSearchIn] = []
    fetched: list[StockFetchIn] = []

    async def fake_search(
        runtime: Any, payload: StockSearchIn, client: Any = None
    ) -> StockSearchOut:
        searched.append(payload)
        assert runtime.pexels_api_key == "pex-key", "the runtime settings carry the keys"
        return StockSearchOut(
            query=payload.query, candidates=[candidate], total={"pexels": 1}, problems=[]
        )

    async def fake_fetch(
        runtime: Any, settings: Any, store: Any, payload: StockFetchIn, client: Any = None
    ) -> StockFetchOut:
        fetched.append(payload)
        if payload.id == "7":
            raise StorageRefused(413, "video_media_file_too_large", "too big")
        if payload.id == "8":
            raise StockError(404, "video_media_stock_not_found", "gone")
        return StockFetchOut(
            sha256="a" * 64,
            size=10,
            content_type="image/png",
            width=64,
            height=36,
            credit=candidate.credit,
        )

    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        unavailable = await client.post(
            "/api/v1/video/media/stock/search", json={"query": "Seoul"}
        )
        off = await client.get("/api/v1/video/media/status")
        media["runtime"] = BOTH
        monkeypatch.setattr(stock, "search", fake_search)
        monkeypatch.setattr(stock, "fetch", fake_fetch)
        found = await client.post(
            "/api/v1/video/media/stock/search",
            json={"query": "Seoul", "orientation": "landscape", "per_page": 2},
        )
        body = {"slug": "seoul-guide", "provider": "pexels", "id": "3573351"}
        got = await client.post("/api/v1/video/media/stock/fetch", json=body)
        too_big = await client.post("/api/v1/video/media/stock/fetch", json={**body, "id": "7"})
        gone = await client.post("/api/v1/video/media/stock/fetch", json={**body, "id": "8"})
        on = await client.get("/api/v1/video/media/status")
    assert unavailable.status_code == 503, unavailable.text
    assert unavailable.json()["code"] == "video_media_stock_unavailable"
    assert off.json()["stock"] == {"pexels": False, "pixabay": False}
    assert off.json()["limits"]["stock_per_page"] == 40
    assert found.status_code == 200, found.text
    assert found.json()["candidates"][0]["credit"] == {
        "provider": "pexels",
        "author": "Lukas Rodriguez",
        "author_url": "https://www.pexels.com/@lukas-rodriguez-1845331",
        "url": "https://www.pexels.com/photo/seoul-at-night-3573351/",
        "license": "Pexels License",
        "license_url": "https://www.pexels.com/license/",
        "text": "Photo by Lukas Rodriguez on Pexels",
    }
    assert found.json()["total"] == {"pexels": 1} and found.json()["problems"] == []
    assert searched[0].orientation == "landscape" and searched[0].per_page == 2
    assert got.status_code == 200, got.text
    assert got.json() == {
        "sha256": "a" * 64,
        "size": 10,
        "content_type": "image/png",
        "width": 64,
        "height": 36,
        "credit": found.json()["candidates"][0]["credit"],
    }
    assert fetched[0] == StockFetchIn(slug="seoul-guide", provider="pexels", id="3573351")
    assert too_big.status_code == 413 and too_big.json()["code"] == "video_media_file_too_large"
    assert gone.status_code == 404 and gone.json()["code"] == "video_media_stock_not_found"
    assert on.json()["stock"] == {"pexels": True, "pixabay": True}
    names = [call.args[0] for call in media["limits"].await_args_list]
    assert names.count("video_media_stock") == 5, "search and fetch share one per-hour bucket"
    assert await meter.used(media["redis"], meter.JUDGE_CALLS) == 0, "no budget unit is booked"
    assert media["prune"].await_count == 1, "a fetch that stored a file ran the hourly prune"
