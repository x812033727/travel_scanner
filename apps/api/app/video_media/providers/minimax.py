"""MiniMax image-01 and the Hailuo video models.

Images are synchronous and come back in the answer itself: the adapter asks for
``response_format: base64`` and ``submit`` returns the bytes, as the Gemini image adapter
does. Asked for a link instead, image-01 handed back one that ``check_download`` refuses, so
until 2026-10-04 no picture was ever stored. An answer that carries only links (a vendor that
ignored the parameter) still goes down the download path, through the same check. Video is a
task to poll, whose result is a file id exchanged for a download URL. Downloads are on
MiniMax's CDN and need no key, so ``fetch`` sends none. ``base_resp.status_code`` carries the
vendor's own verdicts (quota, balance, sensitive content) inside an HTTP 200, so every answer
is checked for it.

MiniMax-H3 is served only by the v2 video API (read 2026-10-05:
https://platform.minimax.io/docs/api-reference/video-generation-v2-create and
.../video-generation-v2-query; the China pages at platform.minimaxi.com describe the same
paths and body). Its request is ``POST /v2/video_generation`` with a ``content[]`` array,
its task is read at ``GET /v2/query/video_generation/{task_id}``, which hands back the video
URL itself, and a refusal is a real HTTP status whose OpenAI-style body ends its message with
MiniMax's own code (``… (2013)``). The v1 model list (.../video-generation-i2v) has no H3, so
the v1 request every other model keeps would never have made an H3 clip. The configured base
names the v1 API (``…/v1``); the v2 paths hang off the same host. An H3 task's ``vendor_ref``
carries a ``v2:`` prefix so that ``poll``, which sees only the reference, asks the v2 query.

The same v2 request has two shapes (the create page and .../guides/video-generation, read
2026-10-05; the China page platform.minimax.cn/docs/api-reference/video-generation-v2-create
states the same rules): image-to-video, where ``content[]`` carries the text and the first
frame (an optional last one too), and reference-to-video, where it carries the text and up to
nine ``reference_image`` items (reference videos and audio exist too, three each; nothing here
sends them). The two are mutually exclusive, so a request with a frame and a reference image
is refused before the paid call rather than having either dropped. Which shape a request takes
follows from what it carries: frames, or reference images and no frame.
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from app.video_media.providers import (
    USER_AGENT,
    Download,
    MediaRequest,
    MediaUpstreamError,
    Polled,
    ReferenceImage,
    Submitted,
    check_download,
    data_url,
    get_json,
    post_json,
    raise_for_status,
)
from app.video_media.storage import sniff_type

# MiniMax's own status codes, as documented on 2026-09-26.
BUSY = {1002, 1039}
KEY = {1004, 1008, 2049}
BLOCKED = {1026, 1027}
INVALID = {2013}
IMAGE_PROMPT_LIMIT = 1500
# The clip models the v2 API serves. MiniMax-H3-Max is v2-only too, but it is not in the
# catalog; every model not named here keeps the v1 request unchanged.
V2_VIDEO_MODELS = frozenset({"MiniMax-H3"})
V2_REF_PREFIX = "v2:"
# The v2 create page (read 2026-10-05): "reference images ≤ 9" in reference-to-video, and
# ``ratio`` is one of these (``adaptive`` is the default; image-to-video ignores it and always
# follows the first frame). A reference-to-video request has no frame to follow, so it names
# the ratio the clip is for.
V2_MAX_REFERENCE_IMAGES = 9
V2_RATIOS = frozenset({"adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"})
# The code MiniMax puts at the end of a v2 error message: "invalid params, … (2013)".
_V2_ERROR_CODE = re.compile(r"\((\d{1,6})\)\s*$")


def decode_image(encoded: object) -> bytes:
    """One entry of ``data.image_base64`` as the picture's bytes.

    The messages are fixed: what the vendor sent in place of a picture never reaches a job's
    error. Line breaks are legal in base64 and carry nothing, so they are dropped; any other
    character outside the alphabet, or a broken padding, is refused rather than skipped.
    """
    if not isinstance(encoded, str):
        raise MediaUpstreamError(502, "MiniMax's image is not a base64 string", "failed")
    try:
        data = base64.b64decode("".join(encoded.split()), validate=True)
    except ValueError as error:  # binascii.Error is one
        raise MediaUpstreamError(502, "MiniMax's image is not valid base64", "failed") from error
    if not data:
        raise MediaUpstreamError(502, "MiniMax returned an empty image", "failed")
    return data


def check_base_resp(payload: dict[str, Any]) -> None:
    base = payload.get("base_resp")
    if not isinstance(base, dict):
        return
    code = base.get("status_code")
    if code in (None, 0):
        return
    message = str(base.get("status_msg") or code)
    if code in BUSY:
        raise MediaUpstreamError(429, f"MiniMax is busy ({message})", "busy")
    if code in KEY:
        raise MediaUpstreamError(502, f"MiniMax rejected the key or balance ({message})", "key")
    if code in INVALID:
        raise MediaUpstreamError(422, f"MiniMax rejected the parameters ({message})", "invalid")
    if code in BLOCKED:
        raise MediaUpstreamError(422, f"MiniMax refused the content ({message})", "blocked")
    raise MediaUpstreamError(502, f"MiniMax answered {code}: {message}", "failed")


def api_root(base_url: str) -> str:
    """The configured base without its ``/v1``: where the v2 paths start."""
    root = base_url.rstrip("/")
    return root.removesuffix("/v1")


def v2_image(image: ReferenceImage, role: str) -> dict[str, Any]:
    """One picture of a v2 ``content[]`` array, in the documented data-URI form."""
    return {"type": "image_url", "image_url": {"url": data_url(image)}, "role": role}


def _digits(value: object) -> int | None:
    text = str(value) if isinstance(value, int | str) and not isinstance(value, bool) else ""
    return int(text) if text.isascii() and text.isdigit() and len(text) <= 6 else None


def _v2_error_code(response: httpx.Response) -> int | None:
    """MiniMax's own code from a v2 error body; the vendor's text itself is never kept."""
    try:
        payload = response.json()
    except ValueError:  # not JSON, or not text
        return None
    error = payload.get("error") if isinstance(payload, dict) else None
    message = error.get("message") if isinstance(error, dict) else None
    if not isinstance(message, str):
        return None
    found = _V2_ERROR_CODE.search(message[-32:])
    return int(found.group(1)) if found else None


def raise_for_v2(response: httpx.Response) -> None:
    """Map a v2 refusal to who can fix it; 2xx passes.

    The documented statuses: 400 invalid parameters, 401 key, 402 balance, 422 sensitive
    content, 429 rate limit, 529 overloaded, 500 server error. The code at the end of the
    message decides first, through the same sets as ``base_resp``; the status is the fallback.
    """
    status = response.status_code
    if 200 <= status < 300:
        return
    if status in (429, 529):
        retry = response.headers.get("Retry-After")
        raise MediaUpstreamError(429, f"MiniMax is busy (HTTP {status})", "busy", retry)
    code = _v2_error_code(response)
    if code is not None and code in BUSY | KEY | INVALID | BLOCKED:
        check_base_resp({"base_resp": {"status_code": code, "status_msg": str(code)}})
    if status == 400:
        raise MediaUpstreamError(422, "MiniMax rejected the parameters (HTTP 400)", "invalid")
    if status == 402:
        raise MediaUpstreamError(502, "MiniMax rejected the key or balance (HTTP 402)", "key")
    if status == 422:
        raise MediaUpstreamError(422, "MiniMax refused the content (HTTP 422)", "blocked")
    raise_for_status(response, "MiniMax")


async def _v2_json(
    client: httpx.AsyncClient, url: str, headers: dict[str, str], body: dict[str, Any] | None
) -> dict[str, Any]:
    """POST ``body`` (or GET when there is none) to a v2 path and read the JSON answer."""
    headers = {**headers, "User-Agent": USER_AGENT}
    try:
        if body is None:
            response = await client.get(url, headers=headers)
        else:
            response = await client.post(url, json=body, headers=headers)
    except httpx.HTTPError as error:
        raise MediaUpstreamError(
            502, f"MiniMax unreachable: {type(error).__name__}", "failed"
        ) from error
    raise_for_v2(response)
    try:
        payload = response.json()
    except ValueError as error:
        raise MediaUpstreamError(502, "MiniMax answered without JSON", "failed") from error
    payload = payload if isinstance(payload, dict) else {}
    check_base_resp(payload)
    return payload


@dataclass(frozen=True)
class MiniMaxImages:
    base_url: str
    key: str
    name: str = "minimax"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.key}"}

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        prompt = (
            request.prompt
            if not request.negative_prompt
            else f"{request.prompt}. Avoid: {request.negative_prompt}"
        )
        # Validate the actual vendor body, including the appended avoidance text.
        # The live endpoint rejects a length >= 1500; do not truncate source constraints.
        if len(prompt) >= IMAGE_PROMPT_LIMIT:
            raise MediaUpstreamError(
                422,
                "MiniMax image prompt, including avoidance text, "
                "must be shorter than 1500 characters",
                "invalid",
            )
        body: dict[str, Any] = {
            "model": request.model,
            "prompt": prompt,
            "aspect_ratio": request.aspect,
            "response_format": "base64",
            "n": 1,
            "prompt_optimizer": False,
        }
        subject = next((image for image in request.references if image.role == "character"), None)
        if subject is not None:
            body["subject_reference"] = [{"type": "character", "image_file": data_url(subject)}]
        return body

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        url = f"{self.base_url.rstrip('/')}/image_generation"
        payload = await post_json(
            client, url, self.request_body(request), self._headers(), "MiniMax"
        )
        check_base_resp(payload)
        data = payload.get("data")
        if not isinstance(data, dict):
            data = {}
        encoded = data.get("image_base64")
        if isinstance(encoded, list) and encoded:
            picture = decode_image(encoded[0])
            # MiniMax documents no format (its guide saves ``.jpeg``), so the type is read from
            # the bytes, with the store's own reader; the store reads it again and refuses a
            # file that is none of its types.
            return Submitted(inline=picture, content_type=sniff_type(picture[:16]))
        urls = data.get("image_urls")
        if isinstance(urls, list) and urls and isinstance(urls[0], str):
            # The vendor ignored ``response_format``: the link is fetched as before, and
            # ``fetch`` still refuses one that is not https on a public host.
            return Submitted(download=Download(url=urls[0], content_type_hint="image/jpeg"))
        raise MediaUpstreamError(502, "MiniMax returned no image", "failed")

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        raise MediaUpstreamError(502, "MiniMax images are synchronous; nothing to poll", "invalid")

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        return check_download(download), {}


@dataclass(frozen=True)
class MiniMaxVideo:
    base_url: str
    key: str
    name: str = "minimax"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.key}"}

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        if request.model in V2_VIDEO_MODELS:
            return self._v2_body(request)
        if request.first_frame is None:
            raise MediaUpstreamError(422, "a clip needs its first frame", "invalid")
        body: dict[str, Any] = {
            "model": request.model,
            "prompt": request.prompt
            if not request.negative_prompt
            else f"{request.prompt}. Avoid: {request.negative_prompt}",
            "first_frame_image": data_url(request.first_frame),
            "duration": request.seconds,
            "prompt_optimizer": False,
        }
        if request.resolution:
            body["resolution"] = request.resolution.upper()
        if request.last_frame is not None:
            body["last_frame_image"] = data_url(request.last_frame)
        characters = [image for image in request.references if image.role == "character"]
        if characters:
            body["subject_reference"] = [
                {"type": "character", "image": [data_url(image) for image in characters]}
            ]
        return body

    def _v2_body(self, request: MediaRequest) -> dict[str, Any]:
        """H3's v2 request: image-to-video from its frames, or reference-to-video from its
        reference images.

        The v2 API makes the two mutually exclusive: no ``reference_image``/``reference_video``/
        ``reference_audio`` item may sit next to a ``first_frame`` or ``last_frame``. A request
        carrying both is refused here, before the paid call, rather than having either dropped
        (the jobs layer refuses it earlier still: the catalog gives H3 no reference image beside
        the first frame every clip job has). Image-to-video sends the prompt and the frames and
        nothing else: the ratio always follows the first frame (``adaptive``), and v2 has no
        ``prompt_optimizer`` (H3-Max alone takes ``extra``). Reference-to-video sends every
        reference image, whatever its role, in the order given, since the text names them by
        number (the guide's example: "follows reference images 1 and 2"; the official H3
        prompt guide writes ``<Picture N>``), and the ratio the clip is for, since no frame
        sets it. The prompt is sent as written either way.
        """
        if not request.resolution:
            raise MediaUpstreamError(422, "MiniMax H3 needs a resolution (768P or 2K)", "invalid")
        frames = request.first_frame is not None or request.last_frame is not None
        if frames and request.references:
            raise MediaUpstreamError(
                422, "MiniMax H3 takes a first frame or reference images, not both", "invalid"
            )
        prompt = (
            request.prompt
            if not request.negative_prompt
            else f"{request.prompt}. Avoid: {request.negative_prompt}"
        )
        content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
        body: dict[str, Any] = {
            "model": request.model,
            "content": content,
            "resolution": request.resolution.upper(),
            "duration": request.seconds,
        }
        if request.first_frame is not None:
            content.append(v2_image(request.first_frame, "first_frame"))
            if request.last_frame is not None:
                content.append(v2_image(request.last_frame, "last_frame"))
            return body
        if not request.references:
            # A last frame alone pairs with nothing: the page says it goes with a first frame.
            raise MediaUpstreamError(
                422, "a clip needs its first frame or its reference images", "invalid"
            )
        if len(request.references) > V2_MAX_REFERENCE_IMAGES:
            raise MediaUpstreamError(
                422,
                f"MiniMax H3 takes at most {V2_MAX_REFERENCE_IMAGES} reference images",
                "invalid",
            )
        if request.aspect not in V2_RATIOS:
            raise MediaUpstreamError(
                422,
                f"MiniMax H3 has no {request.aspect} ratio for reference-to-video",
                "invalid",
            )
        content.extend(v2_image(image, "reference_image") for image in request.references)
        body["ratio"] = request.aspect
        return body

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        if request.model in V2_VIDEO_MODELS:
            payload = await _v2_json(
                client,
                f"{api_root(self.base_url)}/v2/video_generation",
                self._headers(),
                self.request_body(request),
            )
            # The documented id is a string; a number is taken too, since by now the task runs
            # and is paid for, and losing its id would lose the clip.
            task_id = payload.get("task_id")
            if isinstance(task_id, int) and not isinstance(task_id, bool):
                task_id = str(task_id)
            if not isinstance(task_id, str) or not task_id:
                raise MediaUpstreamError(502, "MiniMax returned no task id", "failed")
            return Submitted(vendor_ref=f"{V2_REF_PREFIX}{task_id}")
        url = f"{self.base_url.rstrip('/')}/video_generation"
        payload = await post_json(
            client, url, self.request_body(request), self._headers(), "MiniMax"
        )
        check_base_resp(payload)
        task = payload.get("task_id")
        if not isinstance(task, str) or not task:
            raise MediaUpstreamError(502, "MiniMax returned no task id", "failed")
        return Submitted(vendor_ref=task)

    async def _poll_v2(self, task_id: str, client: httpx.AsyncClient) -> Polled:
        payload = await _v2_json(
            client,
            f"{api_root(self.base_url)}/v2/query/video_generation/{quote(task_id, safe='')}",
            self._headers(),
            None,
        )
        task = payload.get("task")
        task = task if isinstance(task, dict) else {}
        status = str(task.get("status") or "")
        if status in ("queued", "running", ""):
            # The v2 guide polls every 10 seconds.
            return Polled("running", retry_after=10)
        if status == "succeeded":
            content = task.get("content")
            url = content.get("url") if isinstance(content, dict) else None
            if not isinstance(url, str) or not url:
                return Polled("failed", reason="MiniMax task succeeded without a video URL")
            return Polled("done", download=Download(url=url, content_type_hint="video/mp4"))
        error = task.get("error")
        code = _digits(error.get("code")) if isinstance(error, dict) else None
        if status == "failed" and code in BLOCKED:
            # A refused prompt or picture, as the v1 ``base_resp`` would say: a retake may pass.
            raise MediaUpstreamError(422, f"MiniMax refused the content ({code})", "blocked")
        named = status if status in ("failed", "cancelled") else "in an unknown state"
        return Polled(
            "failed", reason=f"MiniMax task {named}" + (f" ({code})" if code is not None else "")
        )

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        if vendor_ref.startswith(V2_REF_PREFIX):
            return await self._poll_v2(vendor_ref.removeprefix(V2_REF_PREFIX), client)
        base = self.base_url.rstrip("/")
        payload = await get_json(
            client,
            f"{base}/query/video_generation?task_id={quote(vendor_ref)}",
            self._headers(),
            "MiniMax",
        )
        check_base_resp(payload)
        status = str(payload.get("status") or "")
        if status in ("Preparing", "Queueing", "Processing", ""):
            return Polled("running", retry_after=15)
        if status != "Success":
            return Polled("failed", reason=f"MiniMax task {status}")
        file_id = payload.get("file_id")
        if not file_id:
            return Polled("failed", reason="MiniMax task succeeded without a file id")
        found = await get_json(
            client,
            f"{base}/files/retrieve?file_id={quote(str(file_id))}",
            self._headers(),
            "MiniMax",
        )
        check_base_resp(found)
        url = (found.get("file") or {}).get("download_url")
        if not isinstance(url, str) or not url:
            return Polled("failed", reason="MiniMax gave no download URL for the file")
        return Polled("done", download=Download(url=url, content_type_hint="video/mp4"))

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        return check_download(download), {}
