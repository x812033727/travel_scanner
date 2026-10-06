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
import re
from typing import Any

import httpx

from app.ai.structured_output import gemini_output_text
from app.config import Settings
from app.video_media.providers import USER_AGENT, MediaUpstreamError, raise_for_status
from app.video_media.schemas import JudgeIn, JudgeOut
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

MIN_CRITERION = 4.0
# A problem is one line "<criterion key>: <what is wrong and where> → <one change to the prompt>"
# (docs/videos/ILLUSTRATED.md §judge 的 problems): accurate (it points at the place), complete
# (every failed criterion has a line, and the line was written after looking for the same fault
# everywhere) and constructive (the clause after the arrow is prompt text the next take can be
# asked with). The judge is asked for that form; ``problems()`` holds it to it.
FIX_ARROW = " → "
# After the arrow on a line the judge gave no fix for, and on the line added for a criterion it
# failed without a word. It is a note to whoever rewrites the prompt, not prompt text, and the
# tool's retake loop leaves it out of the next take (tools/video/media/keyframes.mjs
# PLACEHOLDER_FIX): both sides spell it the same.
PLACEHOLDER_FIX = "write the correction into the prompt"
UNDESCRIBED = "the judge found it but did not say what or where"
MAX_PROBLEMS = 20
MAX_PROBLEM_CHARS = 400
MAX_FIX_CHARS = 200
# "key: …", with the key as the rubric writes it or dressed up a little (`key`, **key**, Key -),
# or "key → …" when the judge went straight to the fix.
_KEYED = re.compile(
    r"^\s*[`\"'*\[(]*\s*([A-Za-z][A-Za-z0-9_ -]{0,39}?)\s*[`\"'*\])]*"
    r"\s*(:|：|\s[-–—]\s|\s*(?:→|->)\s*)(.*)$",
    re.DOTALL,
)
_ARROW = re.compile(r"\s*(?:→|->)\s*")
PROBLEM_FORMAT = (
    'in the form "<criterion key>: <what is wrong and where> → <the one change to the prompt '
    'that would prevent it, as the words to put in the prompt>": name the criterion by its key '
    "as the rubric writes it, point at the place, look for the same fault everywhere before "
    "writing the line, and put the most serious first"
)
SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "scores": {"type": "object", "additionalProperties": {"type": "number"}},
        "problems": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "string"},
    },
    "required": ["scores", "problems", "notes"],
}
INSTRUCTIONS = f"""You are the quality judge of an AI anime-drama pipeline. Score the media you are
shown against each rubric criterion from 0 (fails completely) to 10 (flawless). Be strict: a wrong
number of fingers, a warped face, a character whose face, hair, clothing or build differ from
the reference sheet, text or watermarks in the picture, or a cut inside a clip are serious
faults. Score every rubric criterion; "problems" is one line per fault you took points off for,
{PROBLEM_FORMAT}; "notes" is one or two sentences."""
# Fault checks (JudgeCriterion.cost): the judge is asked whether one named fault is there, not
# how good the media are. Asked for a score, the model gives "nothing wrong" a 7 and never goes
# higher, whatever the request or this instruction says about the scale; asked for a grade or a
# deduction it settles in the middle the same way (docs/videos/ILLUSTRATED.md §judge 的刻度與判定
# 沿用, measured 2026-10-04). A yes/no question about one concrete fault it answers plainly, and
# the scores are then computed here. One line, as it was measured.
CHECK_INSTRUCTIONS = (
    "You are the quality judge of an AI anime-drama pipeline. Each rubric criterion names one "
    "fault. Look at the media for that fault and answer true when it is there and false when it "
    "is not. Judge as the viewer meets it: the viewer sees the result for a few seconds and never "
    'reads the prompt. Answer every rubric criterion; "problems" is one line for each fault you '
    f'answered true for and nothing else, {PROBLEM_FORMAT}; "notes" is one or two sentences.'
)


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
    # A check's weight and cost are this module's arithmetic; the judge only sees the question.
    rubric = "\n".join(
        f"- {c.key}: {c.question}"
        if payload.checks
        else f"- {c.key} (weight {c.weight:g}): {c.question}"
        for c in payload.rubric
    )
    context = json.dumps(payload.context, ensure_ascii=False) if payload.context else "{}"
    lead = (
        f"Kind of review: {payload.kind}.\nRubric:\n{rubric}\nContext: {context}\n"
        "The media follow, each preceded by its label."
    )
    parts = [{"text": lead}, *_parts(store, media, payload)]
    keys = [criterion.key for criterion in payload.rubric]
    answers = {
        "type": "object",
        "properties": {key: {"type": "boolean" if payload.checks else "number"} for key in keys},
        "required": keys,
    }
    answer = "faults" if payload.checks else "scores"
    schema = {
        "type": "object",
        "properties": {
            answer: answers,
            "problems": SCHEMA["properties"]["problems"],
            "notes": SCHEMA["properties"]["notes"],
        },
        "required": [answer, "problems", "notes"],
    }
    return {
        "system_instruction": {
            "parts": [{"text": CHECK_INSTRUCTIONS if payload.checks else INSTRUCTIONS}]
        },
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
            "responseSchema": schema,
        },
    }


def _line(key: str, fault: str, fix: str) -> str:
    """One problem line in the form, cut to size: the fix keeps its place, the fault gives way."""
    fault = " ".join(fault.split()) or UNDESCRIBED
    fix = " ".join(fix.split())[:MAX_FIX_CHARS] or PLACEHOLDER_FIX
    head = f"{key}: "
    room = MAX_PROBLEM_CHARS - len(head) - len(FIX_ARROW) - len(fix)
    return f"{head}{fault[:room].rstrip()}{FIX_ARROW}{fix}"


def failed_criteria(payload: JudgeIn, scores: dict[str, float], min_score: int) -> list[str]:
    """The criteria that count against the take, in rubric order.

    A fault check failed when the fault was found (the score is under 10). A scored criterion
    failed when it is under the bar the take is held to, or under the floor of 4 that fails a
    take whatever the overall: a take under the bar always has one, since the overall is the
    weighted mean of the criteria.
    """
    if payload.checks:
        return [c.key for c in payload.rubric if scores[c.key] < 10.0]
    bar = max(float(min_score), MIN_CRITERION)
    return [c.key for c in payload.rubric if scores[c.key] < bar]


def problems(raw: Any, payload: JudgeIn, failed: list[str]) -> list[str]:
    """The judge's problems held to the form, one line per failed criterion at least.

    A line that names no criterion, or one that did not fail, is dropped: it is not a reason the
    take is where it is, and a retake asked with it would chase nothing. A line with no fix gets
    ``PLACEHOLDER_FIX``. A failed criterion no line names gets a line of its own, with its
    question, so the reader knows every reason and the retake loop knows which fix is missing.
    """
    keys = {c.key: c for c in payload.rubric}
    wanted = set(failed)
    kept: list[str] = []
    named: set[str] = set()
    for item in raw if isinstance(raw, list) else []:
        match = _KEYED.match(str(item))
        if not match:
            continue
        key = re.sub(r"[\s-]+", "_", match.group(1).strip().lower())
        if key not in keys or key not in wanted:
            continue
        if _ARROW.fullmatch(match.group(2)):
            parts = ["", match.group(3)]
        else:
            parts = _ARROW.split(match.group(3), maxsplit=1)
        line = _line(key, parts[0], parts[1] if len(parts) > 1 else "")
        if line not in kept:
            kept.append(line)
            named.add(key)
        if len(kept) >= MAX_PROBLEMS:
            break
    for key in failed:
        if key not in named:
            kept.append(_line(key, f"{UNDESCRIBED} (asked: {keys[key].question})", PLACEHOLDER_FIX))
    return kept


def verdict(text: str, payload: JudgeIn, min_score: int, model: str) -> JudgeOut:
    """The model's JSON as a verdict: scores clamped to 0-10, the overall recomputed from them.

    For fault checks the answer is true or false per criterion and the score is computed: 10
    without the fault, 10 less the criterion's cost with it. The problems are held to one line
    per failed criterion in the form ``problems()`` describes.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise JudgeError(
            502, "video_media_judge_failed", f"judge 回的不是 JSON：{error}"
        ) from error
    raw = data.get("faults" if payload.checks else "scores") if isinstance(data, dict) else None
    if not isinstance(raw, dict):
        raise JudgeError(502, "video_media_judge_failed", "judge 沒有給分數")
    scores: dict[str, float] = {}
    for criterion in payload.rubric:
        value = raw.get(criterion.key)
        if criterion.cost is not None:
            # Anything but a plain false counts as the fault: no check passes unanswered.
            scores[criterion.key] = 10.0 if value is False else round(10.0 - criterion.cost, 2)
            continue
        number = (
            float(value) if isinstance(value, int | float) and not isinstance(value, bool) else 0.0
        )
        scores[criterion.key] = round(min(max(number, 0.0), 10.0), 2)
    weights = sum(criterion.weight for criterion in payload.rubric)
    overall = round(sum(scores[c.key] * c.weight for c in payload.rubric) / weights, 2)
    notes = str(data.get("notes") or "")[:1000]
    passed = overall >= min_score and all(score >= MIN_CRITERION for score in scores.values())
    failed = failed_criteria(payload, scores, min_score)
    return JudgeOut(
        scores=scores,
        overall=overall,
        passed=passed,
        problems=problems(data.get("problems"), payload, failed),
        notes=notes,
        model=model,
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
