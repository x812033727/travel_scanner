"""The judge: Gemini looks at a sheet, a keyframe or a clip and scores it against a rubric.

This is how the pipeline retakes a bad generation without a human: every character sheet,
keyframe and clip is scored (identity against the reference sheet, prompt adherence, style,
artifacts), and a score under the owner's threshold means another seed, not a viewer seeing
six fingers. The verdict is JSON with a fixed schema; the overall is recomputed here from the
per-criterion scores and weights, so the model's arithmetic cannot pass something its own
scores would fail.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from app.ai.structured_output import gemini_output_text
from app.config import Settings
from app.video_media.providers import USER_AGENT, MediaUpstreamError, raise_for_status
from app.video_media.schemas import JudgeIn, JudgeOut
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

MIN_CRITERION = 4.0
SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "scores": {"type": "object", "additionalProperties": {"type": "number"}},
        "problems": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "string"},
    },
    "required": ["scores", "problems", "notes"],
}
INSTRUCTIONS = """You are the quality judge of an AI anime-drama pipeline. Score the media you are
shown against each rubric criterion from 0 (fails completely) to 10 (flawless). Be strict: a wrong
number of fingers, a warped face, a character whose face, hair, clothing or build differ from
the reference sheet, text or watermarks in the picture, or a cut inside a clip are serious
faults. Answer with JSON only: {"scores": {<criterion key>: <0-10>, ...}, "problems": [<short,
concrete faults a director would fix>], "notes": <one or two sentences>}. Every rubric key must
appear in scores."""


class JudgeError(Exception):
    def __init__(self, status: int, code: str, detail: str, retry_after: str | None = None) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.retry_after = retry_after


def _parts(store: MediaStore, media: MediaSettings, payload: JudgeIn) -> list[dict[str, Any]]:
    import base64

    parts: list[dict[str, Any]] = []
    total = 0
    for file in payload.files:
        path = store.path(payload.slug, file.sha256)
        if path is None:
            raise JudgeError(404, "video_media_file_not_found", f"{file.label} 不在媒體庫裡")
        data = path.read_bytes()
        total += len(data)
        if total > media.video_media_inline_judge_bytes:
            raise JudgeError(
                413,
                "video_media_judge_too_large",
                f"送給 judge 的檔案合計超過 {media.video_media_inline_judge_bytes} 位元組；"
                "片段請先縮成 720p 的代理檔",
            )
        parts.append({"text": f"[{file.label}]"})
        parts.append(
            {
                "inline_data": {
                    "mime_type": store.content_type_of(path),
                    "data": base64.b64encode(data).decode("ascii"),
                }
            }
        )
    return parts


def request_body(
    model: str, store: MediaStore, media: MediaSettings, payload: JudgeIn
) -> dict[str, Any]:
    rubric = "\n".join(f"- {c.key} (weight {c.weight:g}): {c.question}" for c in payload.rubric)
    context = json.dumps(payload.context, ensure_ascii=False) if payload.context else "{}"
    lead = (
        f"Kind of review: {payload.kind}.\nRubric:\n{rubric}\nContext: {context}\n"
        "The media follow, each preceded by its label."
    )
    parts = [{"text": lead}, *_parts(store, media, payload)]
    return {
        "system_instruction": {"parts": [{"text": INSTRUCTIONS}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
            "responseSchema": SCHEMA,
        },
    }


def verdict(text: str, payload: JudgeIn, min_score: int, model: str) -> JudgeOut:
    """The model's JSON as a verdict: scores clamped to 0-10, the overall recomputed from them."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise JudgeError(
            502, "video_media_judge_failed", f"judge 回的不是 JSON：{error}"
        ) from error
    raw = data.get("scores") if isinstance(data, dict) else None
    if not isinstance(raw, dict):
        raise JudgeError(502, "video_media_judge_failed", "judge 沒有給分數")
    scores: dict[str, float] = {}
    for criterion in payload.rubric:
        value = raw.get(criterion.key)
        number = (
            float(value) if isinstance(value, int | float) and not isinstance(value, bool) else 0.0
        )
        scores[criterion.key] = round(min(max(number, 0.0), 10.0), 2)
    weights = sum(criterion.weight for criterion in payload.rubric)
    overall = round(sum(scores[c.key] * c.weight for c in payload.rubric) / weights, 2)
    problems = [str(item)[:300] for item in data.get("problems") or [] if str(item).strip()][:20]
    notes = str(data.get("notes") or "")[:1000]
    passed = overall >= min_score and all(score >= MIN_CRITERION for score in scores.values())
    return JudgeOut(
        scores=scores, overall=overall, passed=passed, problems=problems, notes=notes, model=model
    )


async def judge(
    runtime: Settings,
    media: MediaSettings,
    store: MediaStore,
    payload: JudgeIn,
    min_score: int,
    client: httpx.AsyncClient | None = None,
) -> JudgeOut:
    key = runtime.hotspot_guide_gemini_api_key
    if not key:
        raise JudgeError(
            503, "video_media_judge_unavailable", "網站的 Gemini 金鑰還沒設定，judge 不能用"
        )
    model = runtime.hotspot_guide_gemini_model
    body = request_body(model, store, media, payload)
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
        raise JudgeError(
            502, "video_media_judge_failed", f"Gemini unreachable: {type(error).__name__}"
        ) from error
    except MediaUpstreamError as error:
        code = "video_media_upstream_busy" if error.kind == "busy" else "video_media_judge_failed"
        raise JudgeError(
            429 if error.kind == "busy" else 502, code, error.message, error.retry_after
        ) from error
    finally:
        if owned:
            await http.aclose()
    answer = response.json()
    try:
        text = gemini_output_text(answer if isinstance(answer, dict) else {})
    except ValueError as error:
        raise JudgeError(502, "video_media_judge_failed", f"judge 沒有回答：{error}") from error
    return verdict(text, payload, min_score, model)
