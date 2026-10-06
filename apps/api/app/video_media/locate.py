"""Where the subjects are in a stored picture: Gemini's ``box_2d`` boxes, booked like a judge call.

The judge scores and answers yes/no and never gives coordinates, and the pipeline has no face
or object detector; a vertical cut of a 16:9 episode, a smart crop for a Short and any later
reframing need one answer to "where is the main character". Gemini returns bounding boxes in
JSON mode as ``box_2d: [ymin, xmin, ymax, xmax]`` on a 0-1000 scale of the picture's height
and width, so this module asks for them the way judge.py asks for scores: same model, key,
pinned host and inline-size cap, one call for one picture. The route books the call on the
judge meter and the judge per-hour limit. A clip is refused: the tool extracts a frame and
uploads it first.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeGuard

import httpx
from PIL import Image

from app.ai.structured_output import gemini_output_text
from app.config import Settings
from app.video_media.providers import USER_AGENT, MediaUpstreamError, raise_for_status
from app.video_media.schemas import LocateIn, LocateOut, SubjectBox
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

IMAGE_TYPES = frozenset({"image/png", "image/jpeg", "image/webp"})
# Gemini's box scale: a coordinate is a thousandth of the picture's height or width.
SCALE = 1000
MAX_BOXES = 20
MAX_LABEL_CHARS = 80
SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "boxes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "box_2d": {"type": "array", "items": {"type": "integer"}},
                    "score": {"type": "number"},
                },
                "required": ["label", "box_2d", "score"],
            },
        }
    },
    "required": ["boxes"],
}
# One line, like the judge's fault checks: the box format is the one Gemini is trained on, the
# scale is named so a model never answers in pixels, and an empty list is said to be fine so
# that a subject that is not there is not invented.
INSTRUCTIONS = (
    "You locate subjects in one picture of an AI anime-drama pipeline. Answer with one bounding "
    "box per subject: box_2d is [ymin, xmin, ymax, xmax] on a 0-1000 scale of the picture's "
    "height and width, and score is how sure you are, from 0 to 1, that the box holds that "
    "subject. A box holds the whole figure, head to feet or to where the frame cuts it, not "
    "only the face. Leave out what is not in the picture: an empty list is a correct answer."
)


class LocateError(Exception):
    def __init__(self, status: int, code: str, detail: str, retry_after: str | None = None) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.retry_after = retry_after


@dataclass(frozen=True)
class Picture:
    content_type: str
    data: bytes
    width: int
    height: int


def image_size(path: Path) -> tuple[int, int]:
    """The picture's width and height from its header; Pillow decodes no pixels for this."""
    try:
        with Image.open(path) as image:
            width, height = image.size
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        raise LocateError(
            422, "video_media_invalid", f"這張圖片的檔頭讀不出尺寸：{type(error).__name__}"
        ) from error
    if width < 1 or height < 1:
        raise LocateError(422, "video_media_invalid", "這張圖片的檔頭說它沒有大小")
    return width, height


def picture(store: MediaStore, media: MediaSettings, payload: LocateIn) -> Picture:
    """The stored picture, checked before any budget is spent on it."""
    path = store.path(payload.slug, payload.sha256)
    if path is None:
        raise LocateError(404, "video_media_file_not_found", "這個檔案不在媒體庫裡")
    content_type = store.content_type_of(path)
    if content_type not in IMAGE_TYPES:
        raise LocateError(
            422,
            "video_media_invalid",
            f"locate 只看 png、jpeg、webp 圖片，這個檔案是 {content_type}；片段請先抽出一格再上傳",
        )
    data = path.read_bytes()
    if len(data) > media.video_media_inline_judge_bytes:
        raise LocateError(
            413,
            "video_media_judge_too_large",
            f"送給 Gemini 的圖片超過 {media.video_media_inline_judge_bytes} 位元組；請先縮小",
        )
    width, height = image_size(path)
    return Picture(content_type=content_type, data=data, width=width, height=height)


def lead(payload: LocateIn) -> str:
    """What to box: the labels the tool named, or the characters and prominent subjects."""
    if payload.labels:
        wanted = json.dumps(payload.labels, ensure_ascii=False)
        return (
            f"Subjects to box: {wanted}. Box each of these that is in the picture, with its "
            "label exactly as given, and leave out any that is not there. The picture follows."
        )
    return (
        "Subjects to box: every character in the picture, the main character first, then the one "
        "or two most prominent other subjects, each with a short label. The picture follows."
    )


def request_body(payload: LocateIn, image: Picture) -> dict[str, Any]:
    parts = [
        {"text": lead(payload)},
        {
            "inline_data": {
                "mime_type": image.content_type,
                "data": base64.b64encode(image.data).decode("ascii"),
            }
        },
    ]
    return {
        "system_instruction": {"parts": [{"text": INSTRUCTIONS}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
            "responseSchema": SCHEMA,
        },
    }


def _number(value: Any) -> TypeGuard[int | float]:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _box(item: Any) -> SubjectBox | None:
    """One answer as a box: coordinates clamped to the scale and ordered, or None when unusable."""
    if not isinstance(item, dict):
        return None
    raw = item.get("box_2d")
    if not isinstance(raw, list) or len(raw) != 4 or not all(_number(v) for v in raw):
        return None
    y0, x0, y1, x1 = (min(max(round(float(v)), 0), SCALE) for v in raw)
    ymin, ymax = sorted((y0, y1))
    xmin, xmax = sorted((x0, x1))
    if ymin == ymax or xmin == xmax:
        return None
    label = str(item.get("label") or "").strip()[:MAX_LABEL_CHARS] or "subject"
    score = item.get("score")
    sure = float(score) if _number(score) else 0.0
    return SubjectBox(
        label=label, box=(ymin, xmin, ymax, xmax), score=round(min(max(sure, 0.0), 1.0), 3)
    )


def boxes(text: str) -> list[SubjectBox]:
    """The model's JSON as boxes: unusable entries dropped, at most MAX_BOXES, model order kept."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise LocateError(
            502, "video_media_locate_failed", f"locate 回的不是 JSON：{error}"
        ) from error
    raw = data.get("boxes") if isinstance(data, dict) else None
    if not isinstance(raw, list):
        raise LocateError(502, "video_media_locate_failed", "locate 沒有給方框")
    found = [box for box in (_box(item) for item in raw) if box is not None]
    return found[:MAX_BOXES]


async def locate(
    runtime: Settings,
    media: MediaSettings,
    store: MediaStore,
    payload: LocateIn,
    client: httpx.AsyncClient | None = None,
) -> LocateOut:
    key = runtime.hotspot_guide_gemini_api_key
    if not key:
        raise LocateError(
            503, "video_media_locate_unavailable", "網站的 Gemini 金鑰還沒設定，locate 不能用"
        )
    model = runtime.hotspot_guide_gemini_model
    image = picture(store, media, payload)
    body = request_body(payload, image)
    owned = client is None
    http = client or httpx.AsyncClient(
        timeout=runtime.video_speech_gemini_timeout_seconds, trust_env=False
    )
    try:
        # ``hotspot_guide_gemini_base_url`` is pinned to the official host in Settings.
        base = runtime.hotspot_guide_gemini_base_url.rstrip("/")
        response = await http.post(
            f"{base}/v1beta/models/{model}:generateContent",
            json=body,
            headers={"x-goog-api-key": key, "User-Agent": USER_AGENT},
        )
        raise_for_status(response, "Gemini")
    except httpx.HTTPError as error:
        raise LocateError(
            502, "video_media_locate_failed", f"Gemini unreachable: {type(error).__name__}"
        ) from error
    except MediaUpstreamError as error:
        code = "video_media_upstream_busy" if error.kind == "busy" else "video_media_locate_failed"
        raise LocateError(
            429 if error.kind == "busy" else 502, code, error.message, error.retry_after
        ) from error
    finally:
        if owned:
            await http.aclose()
    answer = response.json()
    try:
        text = gemini_output_text(answer if isinstance(answer, dict) else {})
    except ValueError as error:
        raise LocateError(502, "video_media_locate_failed", f"locate 沒有回答：{error}") from error
    return LocateOut(boxes=boxes(text), width=image.width, height=image.height, model=model)
