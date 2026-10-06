"""Stock photos for the illustrated slides: Pexels and Pixabay searched and fetched here.

The pipeline had no real photographs at all; the slides of a Seoul guide were drawn as prints or
AI pictures while both vendors hold photos of Seoul, Busan and Jeju under licences that allow
commercial use. The vendors' keys never reach the local tool (every key of the pipeline is
server-only), so the tool sends a query here with its video tool token, picks a candidate from
the answer, and asks the server to fetch it: the file goes into the media store the way a
generated file does (``MediaStore.put_stream``: hashed as it arrives, typed from its bytes,
capped), and the credit the vendor asks for travels with it so the description cannot lose it.

Neither vendor charges, so a stock call is not a ``video_media_jobs`` row and books nothing on
the month's budgets; the route's per-hour limit is the only brake. A key goes only to the host
its base URL is pinned to (``OFFICIAL_PROVIDER_HOSTS``), and a file is fetched only from the
vendor's own hosts (``HOSTS``), checked before a byte is read. Pixabay takes its key as a query
parameter, which is why no error raised here carries a URL, only a vendor's name and a status.

What the vendors ask for (docs/videos/ILLUSTRATED.md §圖庫照片 keeps the rules): both licences
allow commercial use without attribution, both vendors ask that the photographer and the site
be credited where possible, and both forbid hotlinking and reselling the unaltered file; each
candidate carries the credit line in the vendor's own wording. Written from the vendors'
public API documentation only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from PIL import Image

from app.config import Settings
from app.video_media.providers import (
    USER_AGENT,
    Download,
    MediaUpstreamError,
    check_download,
)
from app.video_media.schemas import (
    StockCandidate,
    StockCredit,
    StockFetchIn,
    StockFetchOut,
    StockProvider,
    StockSearchIn,
    StockSearchOut,
)
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

ORDER: tuple[StockProvider, ...] = ("pexels", "pixabay")
LABELS: dict[str, str] = {"pexels": "Pexels", "pixabay": "Pixabay"}
# Where each vendor serves the files its API points at; a download anywhere else is refused.
HOSTS: dict[str, frozenset[str]] = {
    "pexels": frozenset({"images.pexels.com"}),
    "pixabay": frozenset({"pixabay.com", "cdn.pixabay.com"}),
}
LICENSES: dict[str, tuple[str, str]] = {
    "pexels": ("Pexels License", "https://www.pexels.com/license/"),
    "pixabay": ("Pixabay Content License", "https://pixabay.com/service/license-summary/"),
}
# A stock photo is a picture: an mp4 or a sound from a photo endpoint is refused by the store.
IMAGE_TYPES = frozenset({"image/png", "image/jpeg", "image/webp"})
API_TIMEOUT_SECONDS = 20.0
# Pixabay refuses a page smaller than this; the answer is cut back to what was asked.
PIXABAY_MIN_PER_PAGE = 3
PROBE_QUERY = "Seoul skyline"


class StockError(Exception):
    def __init__(self, status: int, code: str, detail: str, retry_after: str | None = None) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.retry_after = retry_after


@dataclass(frozen=True)
class Vendor:
    name: StockProvider
    label: str
    key: str
    base: str
    hosts: frozenset[str]


@dataclass(frozen=True)
class Photo:
    """One vendor answer: the candidate the tool sees and the file URL only ``fetch`` uses."""

    candidate: StockCandidate
    download: str


def configured(runtime: Settings) -> dict[str, bool]:
    """Vendor by vendor, whether the site holds a key (``GET /status`` says this to the tool)."""
    return {"pexels": bool(runtime.pexels_api_key), "pixabay": bool(runtime.pixabay_api_key)}


def vendors(runtime: Settings, only: StockProvider | None = None) -> list[Vendor]:
    """The configured vendors in a fixed order, or the one asked for; 503 when there is none."""
    found: list[Vendor] = []
    for name in ORDER:
        if only is not None and name != only:
            continue
        if name == "pexels":
            key, base = runtime.pexels_api_key, runtime.pexels_api_base_url
        else:
            key, base = runtime.pixabay_api_key, runtime.pixabay_api_base_url
        if key:
            found.append(Vendor(name, LABELS[name], key, base.rstrip("/"), HOSTS[name]))
    if not found:
        wanted = LABELS[only] if only else "Pexels 或 Pixabay"
        raise StockError(
            503, "video_media_stock_unavailable", f"網站的 {wanted} 金鑰還沒設定，圖庫照片不能用"
        )
    return found


def _check(response: httpx.Response, vendor: Vendor) -> None:
    """A vendor's status as who can fix it; 2xx passes. Never the URL: Pixabay's holds the key."""
    status = response.status_code
    if 200 <= status < 300:
        return
    if status == 429:
        raise StockError(
            429,
            "video_media_upstream_busy",
            f"{vendor.label} 的額度用完或太忙",
            response.headers.get("Retry-After"),
        )
    if status in (401, 403):
        raise StockError(
            502, "video_media_stock_failed", f"{vendor.label} 拒絕了網站的金鑰（HTTP {status}）"
        )
    if status == 404:
        raise StockError(404, "video_media_stock_not_found", f"{vendor.label} 沒有這張照片")
    if status == 400:
        # Pixabay answers 400 to a bad key as well as to a bad parameter.
        raise StockError(
            502,
            "video_media_stock_failed",
            f"{vendor.label} 拒絕了這個請求（HTTP 400：金鑰或參數有誤）",
        )
    raise StockError(502, "video_media_stock_failed", f"{vendor.label} 回應 HTTP {status}")


async def _get(
    http: httpx.AsyncClient,
    vendor: Vendor,
    url: str,
    params: dict[str, str | int],
    headers: dict[str, str],
) -> Any:
    try:
        response = await http.get(
            url, params=params, headers={**headers, "User-Agent": USER_AGENT}
        )
    except httpx.HTTPError as error:
        raise StockError(
            502, "video_media_stock_failed", f"{vendor.label} unreachable: {type(error).__name__}"
        ) from error
    _check(response, vendor)
    try:
        return response.json()
    except ValueError as error:
        raise StockError(
            502, "video_media_stock_failed", f"{vendor.label} 回的不是 JSON"
        ) from error


def _int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    number = int(value)
    return number if number > 0 else None


def _text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = " ".join(value.split())
    return text[:200] or None


def _https(value: Any) -> str | None:
    text = _text(value)
    return text if text and text.startswith("https://") and " " not in text else None


def pexels_photo(item: Any) -> Photo | None:
    """One Pexels photo object, or None when a field the credit or the file needs is missing."""
    if not isinstance(item, dict):
        return None
    src = item.get("src")
    if not isinstance(src, dict):
        src = {}
    photo_id = _int(item.get("id"))
    width, height = _int(item.get("width")), _int(item.get("height"))
    page, author = _https(item.get("url")), _text(item.get("photographer"))
    original = _https(src.get("original"))
    medium, large = _https(src.get("medium")), _https(src.get("large"))
    if not (photo_id and width and height and page and author and original and medium and large):
        return None
    license_name, license_url = LICENSES["pexels"]
    credit = StockCredit(
        provider="pexels",
        author=author,
        author_url=_https(item.get("photographer_url")),
        url=page,
        license=license_name,
        license_url=license_url,
        text=f"Photo by {author} on Pexels",
    )
    candidate = StockCandidate(
        provider="pexels",
        id=str(photo_id),
        width=width,
        height=height,
        thumbnail=medium,
        preview=large,
        alt=_text(item.get("alt")),
        credit=credit,
    )
    return Photo(candidate=candidate, download=original)


def pixabay_photo(item: Any) -> Photo | None:
    """One Pixabay hit. The original (``imageURL``) and the 1920 px file (``fullHDURL``) come
    only with full API access; a key without it gets the 1280 px ``largeImageURL``."""
    if not isinstance(item, dict):
        return None
    photo_id = _int(item.get("id"))
    page, author = _https(item.get("pageURL")), _text(item.get("user"))
    thumbnail, preview = _https(item.get("previewURL")), _https(item.get("webformatURL"))
    download = next(
        (
            url
            for url in (
                _https(item.get("imageURL")),
                _https(item.get("fullHDURL")),
                _https(item.get("largeImageURL")),
            )
            if url
        ),
        None,
    )
    width = _int(item.get("imageWidth")) or _int(item.get("webformatWidth"))
    height = _int(item.get("imageHeight")) or _int(item.get("webformatHeight"))
    if not (photo_id and page and author and thumbnail and preview and download):
        return None
    if not (width and height):
        return None
    user_id = _int(item.get("user_id"))
    # The profile page is not in the answer; Pixabay builds it from the name and the number.
    author_url = (
        f"https://pixabay.com/users/{author}-{user_id}/" if user_id and " " not in author else None
    )
    license_name, license_url = LICENSES["pixabay"]
    credit = StockCredit(
        provider="pixabay",
        author=author,
        author_url=author_url,
        url=page,
        license=license_name,
        license_url=license_url,
        text=f"Image by {author} from Pixabay",
    )
    candidate = StockCandidate(
        provider="pixabay",
        id=str(photo_id),
        width=width,
        height=height,
        thumbnail=thumbnail,
        preview=preview,
        alt=_text(item.get("tags")),
        credit=credit,
    )
    return Photo(candidate=candidate, download=download)


def _photos(vendor: Vendor, answer: Any) -> list[Photo]:
    """The usable photos of a search answer, in the vendor's order."""
    if not isinstance(answer, dict):
        return []
    raw = answer.get("photos" if vendor.name == "pexels" else "hits")
    if not isinstance(raw, list):
        return []
    parse = pexels_photo if vendor.name == "pexels" else pixabay_photo
    return [photo for photo in (parse(item) for item in raw) if photo is not None]


def _total(vendor: Vendor, answer: Any) -> int:
    if not isinstance(answer, dict):
        return 0
    return _int(answer.get("total_results" if vendor.name == "pexels" else "total")) or 0


def search_request(
    vendor: Vendor, payload: StockSearchIn
) -> tuple[str, dict[str, str | int], dict[str, str]]:
    """The vendor's search call: URL, query parameters and headers; the key rides in one of them."""
    if vendor.name == "pexels":
        params: dict[str, str | int] = {
            "query": payload.query,
            "per_page": payload.per_page,
            "page": payload.page,
        }
        if payload.orientation:
            params["orientation"] = payload.orientation
        return f"{vendor.base}/search", params, {"Authorization": vendor.key}
    params = {
        "key": vendor.key,
        "q": payload.query,
        "image_type": "photo",
        "safesearch": "true",
        "per_page": max(payload.per_page, PIXABAY_MIN_PER_PAGE),
        "page": payload.page,
    }
    if payload.orientation == "landscape":
        params["orientation"] = "horizontal"
    elif payload.orientation == "portrait":
        params["orientation"] = "vertical"
    return f"{vendor.base}/", params, {}


async def _search_one(
    http: httpx.AsyncClient, vendor: Vendor, payload: StockSearchIn
) -> tuple[list[StockCandidate], int]:
    url, params, headers = search_request(vendor, payload)
    answer = await _get(http, vendor, url, params, headers)
    photos = _photos(vendor, answer)
    return [photo.candidate for photo in photos[: payload.per_page]], _total(vendor, answer)


async def search(
    runtime: Settings, payload: StockSearchIn, client: httpx.AsyncClient | None = None
) -> StockSearchOut:
    """Candidates from one vendor or every configured one; a vendor that fails while another
    answers is named in ``problems``, and the call fails only when no vendor answered."""
    asked = vendors(runtime, payload.provider)
    owned = client is None
    http = client or httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS, trust_env=False)
    candidates: list[StockCandidate] = []
    total: dict[str, int] = {}
    problems: list[str] = []
    first: StockError | None = None
    try:
        for vendor in asked:
            try:
                found, count = await _search_one(http, vendor, payload)
            except StockError as error:
                problems.append(error.detail)
                first = first or error
                continue
            candidates.extend(found)
            total[vendor.name] = count
    finally:
        if owned:
            await http.aclose()
    if not total and first is not None:
        raise first
    return StockSearchOut(
        query=payload.query, candidates=candidates, total=total, problems=problems
    )


async def _photo(http: httpx.AsyncClient, vendor: Vendor, photo_id: str) -> Photo:
    """The one photo ``fetch`` was asked for, from the vendor's by-id call."""
    if vendor.name == "pexels":
        answer = await _get(
            http, vendor, f"{vendor.base}/photos/{photo_id}", {}, {"Authorization": vendor.key}
        )
        photo = pexels_photo(answer)
    else:
        answer = await _get(
            http, vendor, f"{vendor.base}/", {"key": vendor.key, "id": photo_id}, {}
        )
        found = _photos(vendor, answer)
        if not found:
            raise StockError(404, "video_media_stock_not_found", f"{vendor.label} 沒有這張照片")
        photo = found[0]
    if photo is None:
        raise StockError(
            502,
            "video_media_stock_failed",
            f"{vendor.label} 回的照片資料不完整，沒有可下載的檔案",
        )
    if photo.candidate.id != photo_id:
        raise StockError(
            502,
            "video_media_stock_failed",
            f"{vendor.label} 回的是另一張照片（{photo.candidate.id}）",
        )
    return photo


def _dimensions(path: Path, vendor: Vendor) -> tuple[int, int]:
    """The stored file's width and height from its header; the vendor's numbers are not trusted."""
    try:
        with Image.open(path) as image:
            width, height = image.size
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        path.unlink(missing_ok=True)
        raise StockError(
            502,
            "video_media_stock_failed",
            f"{vendor.label} 送來的圖片讀不出尺寸：{type(error).__name__}",
        ) from error
    if width < 1 or height < 1:
        path.unlink(missing_ok=True)
        raise StockError(502, "video_media_stock_failed", f"{vendor.label} 送來的圖片沒有大小")
    return width, height


async def fetch(
    runtime: Settings,
    media: MediaSettings,
    store: MediaStore,
    payload: StockFetchIn,
    client: httpx.AsyncClient | None = None,
) -> StockFetchOut:
    """The photo's largest file, streamed into the media store, with its credit.

    The by-id call is made again rather than trusting a URL from the tool: the vendor's answer is
    the only place a download URL may come from, and it must sit on the vendor's own host.
    Raises ``StorageRefused`` for the store's own refusals (too large, full, not a picture).
    """
    vendor = vendors(runtime, payload.provider)[0]
    owned = client is None
    http = client or httpx.AsyncClient(
        timeout=media.video_media_fetch_timeout_seconds, trust_env=False
    )
    try:
        photo = await _photo(http, vendor, payload.id)
        try:
            url = check_download(Download(photo.download), vendor.hosts)
        except MediaUpstreamError as error:
            raise StockError(
                502, "video_media_stock_failed", f"{vendor.label}: {error.message}"
            ) from error
        try:
            # The file is public on the vendor's host: no key goes with this request.
            async with http.stream("GET", url, headers={"User-Agent": USER_AGENT}) as response:
                _check(response, vendor)
                stored = await store.put_stream(
                    payload.slug,
                    f"stock-{vendor.name}-{payload.id}",
                    response.aiter_bytes(),
                    accept=IMAGE_TYPES,
                )
        except httpx.HTTPError as error:
            raise StockError(
                502,
                "video_media_stock_failed",
                f"{vendor.label} 的下載中斷：{type(error).__name__}",
            ) from error
    finally:
        if owned:
            await http.aclose()
    path = store.path(payload.slug, stored.sha256)
    if path is None:  # pragma: no cover - the store named it a moment ago
        raise StockError(502, "video_media_stock_failed", "下載的檔案沒有留在媒體庫裡")
    width, height = _dimensions(path, vendor)
    return StockFetchOut(
        sha256=stored.sha256,
        size=stored.size,
        content_type=stored.content_type,
        width=width,
        height=height,
        credit=photo.candidate.credit,
    )


async def probe(runtime: Settings, client: httpx.AsyncClient | None = None) -> str:
    """The settings card's connection test: one real search per configured vendor.

    It proves the key, the pinned host and the answer's shape in one free call each; every
    vendor is tried, and one failure fails the test with the others' results beside it.
    """
    asked = vendors(runtime)
    payload = StockSearchIn(query=PROBE_QUERY, per_page=1)
    owned = client is None
    http = client or httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS, trust_env=False)
    verified: list[str] = []
    failures: list[str] = []
    try:
        for vendor in asked:
            try:
                found, count = await _search_one(http, vendor, payload)
            except StockError as error:
                failures.append(f"{vendor.label} 驗證失敗：{error.detail}")
                continue
            if not found:
                failures.append(f"{vendor.label} 可連線，但「{PROBE_QUERY}」沒有回任何可用的照片")
                continue
            verified.append(f"{vendor.label} ✓（「{PROBE_QUERY}」共 {count:,} 張）")
    finally:
        if owned:
            await http.aclose()
    if failures:
        raise StockError(502, "video_media_stock_failed", "；".join(failures + verified))
    return "；".join(verified)
