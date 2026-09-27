"""The image, clip and music models the drama route can use, with what each offers and costs.

Kept apart from ``app.ai.catalog`` (text models): these are chosen on the settings tab of
/admin/videos, validated there, and priced here so the media status can estimate the month's
spend. Ids and prices are the vendors' pages as read on 2026-09-26; the adapter ticket
(2026-09-26-video-drama-media-api) re-checks each id against the official page before it
calls the vendor, and a model whose id is not yet confirmed is marked ``preview``. A retired
model stays listed so that a stored setting naming it is refused by name, not silently kept.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MediaVendor = Literal["gemini", "minimax"]
MediaKind = Literal["image", "clip", "music"]
MediaStatus = Literal["stable", "preview", "retired"]
MEDIA_VENDORS: tuple[MediaVendor, ...] = ("gemini", "minimax")
MEDIA_KINDS: tuple[MediaKind, ...] = ("image", "clip", "music")


@dataclass(frozen=True)
class MediaModel:
    id: str
    vendor: MediaVendor
    kind: MediaKind
    label: str
    note: str | None = None
    status: MediaStatus = "stable"
    # Clips: the resolutions and whole seconds the vendor accepts for one generation.
    resolutions: tuple[str, ...] = ()
    durations: tuple[int, ...] = ()
    aspects: tuple[str, ...] = ("16:9", "9:16")
    # How many reference images (character sheets, style frames) one request may carry.
    reference_images: int = 0
    native_audio: bool = False
    usd_per_second: float | None = None
    usd_per_image: float | None = None
    usd_per_track: float | None = None


_SECONDS_4_TO_10 = (4, 5, 6, 7, 8, 9, 10)

MEDIA_CATALOG: tuple[MediaModel, ...] = (
    MediaModel(
        "gemini-3-pro-image",
        "gemini",
        "image",
        "Gemini 3 Pro Image（Nano Banana Pro）",
        note="最多 14 張參考圖，角色跨鏡頭最一致；1K 到 2K 每張 US$0.134",
        reference_images=14,
        usd_per_image=0.134,
    ),
    MediaModel(
        "gemini-3.1-flash-image",
        "gemini",
        "image",
        "Gemini 3.1 Flash Image（Nano Banana 2）",
        note="便宜的草稿與候選；0.5K 每張 US$0.045",
        reference_images=5,
        usd_per_image=0.045,
    ),
    MediaModel(
        "image-01",
        "minimax",
        "image",
        "MiniMax image-01",
        note="每張 US$0.0035，做大量候選；subject_reference 不保證同一張臉",
        reference_images=1,
        usd_per_image=0.0035,
    ),
    MediaModel(
        "gemini-omni-1.1-flash",
        "gemini",
        "clip",
        "Gemini Omni 1.1 Flash",
        note="圖生影片榜首；3 到 10 秒、首尾影格、角色參考圖；1080p 每秒 US$0.15",
        resolutions=("720p", "1080p"),
        durations=_SECONDS_4_TO_10,
        reference_images=3,
        native_audio=True,
        usd_per_second=0.15,
    ),
    MediaModel(
        "veo-3.1-generate-001",
        "gemini",
        "clip",
        "Veo 3.1",
        note="主鏡頭用；4、6、8 秒，1080p 只有 8 秒；每秒 US$0.40；id 實作時核對",
        status="preview",
        resolutions=("720p", "1080p"),
        durations=(4, 6, 8),
        reference_images=3,
        native_audio=True,
        usd_per_second=0.40,
    ),
    MediaModel(
        "veo-3.1-fast-generate-001",
        "gemini",
        "clip",
        "Veo 3.1 Fast",
        note="4、6、8 秒；1080p 每秒 US$0.12；id 實作時核對",
        status="preview",
        resolutions=("720p", "1080p"),
        durations=(4, 6, 8),
        reference_images=3,
        native_audio=True,
        usd_per_second=0.12,
    ),
    MediaModel(
        "MiniMax-H3",
        "minimax",
        "clip",
        "MiniMax H3（Hailuo 3.0）",
        note="4 到 15 秒；最多 9 張參考圖，可帶音訊參考；2K 每秒 US$0.13、768p US$0.08",
        resolutions=("768p", "2k"),
        durations=_SECONDS_4_TO_10,
        reference_images=9,
        native_audio=True,
        usd_per_second=0.13,
    ),
    MediaModel(
        "lyria-3.5",
        "gemini",
        "music",
        "Lyria 3.5",
        note="一首完整的曲子 US$0.08；帶 SynthID 浮水印",
        usd_per_track=0.08,
    ),
)

DEFAULT_IMAGE: tuple[MediaVendor, str] = ("gemini", "gemini-3-pro-image")
DEFAULT_CLIP: tuple[MediaVendor, str] = ("gemini", "gemini-omni-1.1-flash")
DEFAULT_MUSIC: tuple[MediaVendor, str] = ("gemini", "lyria-3.5")
# What one judge call (Gemini looking at an image or a clip) costs, for the spend estimate.
JUDGE_USD_PER_CALL = 0.01


def media_options(vendor: MediaVendor, kind: MediaKind) -> tuple[MediaModel, ...]:
    """The models of one vendor and kind a setting may name: everything not retired."""
    return tuple(
        model
        for model in MEDIA_CATALOG
        if model.vendor == vendor and model.kind == kind and model.status != "retired"
    )


def find_model(vendor: MediaVendor, kind: MediaKind, model_id: str) -> MediaModel | None:
    """The catalog entry, retired ones included, so a stale setting is named."""
    return next(
        (m for m in MEDIA_CATALOG if m.vendor == vendor and m.kind == kind and m.id == model_id),
        None,
    )


PRICES: dict[str, float] = {
    model.id: price
    for model in MEDIA_CATALOG
    for price in (model.usd_per_second, model.usd_per_image, model.usd_per_track)
    if price is not None
}
