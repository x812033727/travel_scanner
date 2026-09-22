"""Structured decisions from Jev, TypeSafe's System One model.

Jev is the one AI vendor in this code base that cannot write a sentence. It answers
questions -- ``choice`` picks one option, ``score`` places the state on an ordered
scale, ``noul`` returns the probability that a statement holds -- and every answer
carries a calibrated probability distribution. That makes it useful exactly where a
generating model is being asked to do a classifier's job, and useless everywhere a
reader expects prose. It is deliberately absent from the planner and guide-search
provider rosters in ``app.ai.itinerary`` and ``app.hotspots.ai_search``: a vendor on
those lists that can never return a draft would fall through to the catalog forever.

TypeSafe publishes what Jev 1.13 is bad at, and two entries decide where it may be
pointed in a travel product. It "reads dates as text, not as ordered quantities", so
which of two dates comes first, how far apart they are, and whether one falls inside
a window are all unreliable -- most of what this product asks about dates. And it is
"not a calculator", does "not count reliably", and its "score levels are weak in
numerical calibration", so no price, duration or budget decision belongs here. What
is left is judgement about text: is this article about this place, is this listing
this shop, is this page a fare page.

Kept out of ``app.hotspots`` and ``app.foods`` so either can import it. The vendor
ships an SDK; this module is plain ``httpx`` like every other provider here, because
one POST does not earn a dependency whose own retry loop would fight the circuit
breaker this stack already has.
"""

from __future__ import annotations

import asyncio
import random
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field, ValidationError
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import Settings
from app.problems import AppError

SYSTEM_ONE_PATH = "/systemone"

# The vendor's ceilings, quoted so the settings that sit under them can be read
# against something. A request may carry 64k tokens in total, and state plus the
# longest single question may carry 32k.
VENDOR_MAX_REQUEST_TOKENS = 64_000
VENDOR_MAX_STATE_TOKENS = 32_000
# The score range is the vendor's: "ordered rubric levels (2-10 levels)". The choice
# cap is ours -- TypeSafe documents no maximum -- and exists because a question with
# hundreds of options is a retrieval problem wearing a classifier's clothes, and
# because accuracy is documented to fall as unrelated detail grows.
MAX_CHOICE_OPTIONS = 255
MIN_SCORE_LEVELS = 2
MAX_SCORE_LEVELS = 10
# TypeSafe bills input tokens only, at $0.042 per million; output is not billed at all.
# It lives beside the vendor's other published numbers rather than beside one of the tools
# that report a cost, because two tools with their own copy of a price eventually disagree.
USD_PER_INPUT_TOKEN = 0.042 / 1_000_000


class JevError(Exception):
    """Base class, so a caller can catch every Jev failure without catching httpx."""


class JevAuthError(JevError):
    """401. The key is wrong; retrying it only spends rate limit."""


class JevRequestInvalid(JevError, ValueError):
    """422, or a question this module refuses to send. Our bug, never retried."""


class JevRequestTooLarge(JevRequestInvalid):
    """The estimated token count exceeds a configured cap. Split the batch and retry."""


class ChoiceQuestion(BaseModel):
    type: Literal["choice"] = "choice"
    instructions: str
    criteria: dict[str, str]


class ScoreQuestion(BaseModel):
    type: Literal["score"] = "score"
    instructions: str
    criteria: list[str]


class NoulQuestion(BaseModel):
    type: Literal["noul"] = "noul"
    instructions: str
    # Optional on a noul, unlike choice and score where it is required: it clarifies
    # what yes and no are meant to cover when the statement alone is ambiguous.
    criteria: dict[str, str] | None = None


JevQuestion = ChoiceQuestion | ScoreQuestion | NoulQuestion


class ChoiceAnswer(BaseModel):
    type: Literal["choice"]
    choice: str
    confidence: float
    probabilities: dict[str, float] = Field(default_factory=dict)


class ScoreAnswer(BaseModel):
    type: Literal["score"]
    score: float
    confidence: float
    legend: dict[str, str] = Field(default_factory=dict)
    probabilities: dict[str, float] = Field(default_factory=dict)


class NoulAnswer(BaseModel):
    # A noul answer carries no `confidence`: its own value is the probability. Any
    # helper that reads `.confidence` off an answer has to branch on the type.
    type: Literal["noul"]
    noul: float


JevAnswer = ChoiceAnswer | ScoreAnswer | NoulAnswer

_ANSWER_TYPES: dict[str, type[BaseModel]] = {
    "choice": ChoiceAnswer,
    "score": ScoreAnswer,
    "noul": NoulAnswer,
}

# Han, kana and Hangul each carry far more meaning per codepoint than a Latin letter
# does, so they are counted one-for-one and everything else at roughly 3.5 characters
# per token. The estimate is meant to be pessimistic: this product's state is usually
# CJK, and over-estimating splits a batch one item early while under-estimating turns
# into a 422 from the far side.
_CJK = re.compile(r"[　-鿿豈-﫿＀-￯가-힯]")


def estimate_tokens(value: Any) -> int:
    text = value if isinstance(value, str) else repr(value)
    cjk = len(_CJK.findall(text))
    return cjk + int((len(text) - cjk) / 3.5) + 1


class JevClient:
    name = "jev"

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float,
        *,
        max_state_tokens: int = VENDOR_MAX_STATE_TOKENS,
        max_request_tokens: int = VENDOR_MAX_REQUEST_TOKENS,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.max_state_tokens = max_state_tokens
        self.max_request_tokens = max_request_tokens
        self._external_client = client
        self._client = client or httpx.AsyncClient(timeout=timeout_seconds)

    async def close(self) -> None:
        if self._external_client is None:
            await self._client.aclose()

    def _check_questions(self, questions: Mapping[str, JevQuestion]) -> None:
        if not questions:
            raise JevRequestInvalid("a System One call needs at least one question")
        for name, question in questions.items():
            if isinstance(question, ChoiceQuestion):
                if not 1 <= len(question.criteria) <= MAX_CHOICE_OPTIONS:
                    raise JevRequestInvalid(
                        f"question {name!r}: a choice takes 1-{MAX_CHOICE_OPTIONS} options, "
                        f"got {len(question.criteria)}"
                    )
            elif isinstance(question, ScoreQuestion):
                if not MIN_SCORE_LEVELS <= len(question.criteria) <= MAX_SCORE_LEVELS:
                    raise JevRequestInvalid(
                        f"question {name!r}: a score takes {MIN_SCORE_LEVELS}-"
                        f"{MAX_SCORE_LEVELS} ordered levels, got {len(question.criteria)}"
                    )

    def _check_size(self, state: Any, questions: Mapping[str, JevQuestion]) -> None:
        state_tokens = estimate_tokens(state)
        per_question = {
            name: estimate_tokens(question.model_dump(exclude_none=True))
            for name, question in questions.items()
        }
        longest = max(per_question.values())
        if state_tokens + longest > self.max_state_tokens:
            raise JevRequestTooLarge(
                f"state ({state_tokens}) plus the longest question ({longest}) is over "
                f"the {self.max_state_tokens} token cap; split the batch"
            )
        total = state_tokens + sum(per_question.values())
        if total > self.max_request_tokens:
            raise JevRequestTooLarge(
                f"the request is about {total} tokens, over the {self.max_request_tokens} "
                "token cap; split the batch"
            )

    async def ask(
        self,
        state: str | dict[str, Any] | list[Any],
        questions: Mapping[str, JevQuestion],
    ) -> tuple[dict[str, JevAnswer], dict[str, int]]:
        """Answer every question about one state in a single round trip.

        Batching is not an optimisation here: the vendor's own remedy for a 429 is to
        put the questions in one call, so taking a dict rather than one question is
        what keeps a caller from writing the loop that earns the rate limit.
        """
        self._check_questions(questions)
        self._check_size(state, questions)
        payload = {
            "model": self.model,
            "state": state,
            "questions": {
                name: question.model_dump(exclude_none=True)
                for name, question in questions.items()
            },
        }
        body = await self._send(payload, question_names=sorted(questions))
        answers: dict[str, JevAnswer] = {}
        raw_answers = body.get("answers")
        if not isinstance(raw_answers, dict):
            raise JevError("Jev returned no answers block")
        for name in questions:
            answer = raw_answers.get(name)
            if not isinstance(answer, dict):
                raise JevError(f"Jev returned no answer for question {name!r}")
            model_type = _ANSWER_TYPES.get(str(answer.get("type")))
            if model_type is None:
                raise JevError(f"Jev returned an unknown answer type for {name!r}")
            try:
                answers[name] = model_type.model_validate(answer)  # type: ignore[assignment]
            except ValidationError as exc:
                raise JevError(f"Jev answer for {name!r} did not match its type") from exc
        usage = body.get("usage")
        return answers, usage if isinstance(usage, dict) else {}

    async def _send(self, payload: dict[str, Any], *, question_names: list[str]) -> dict[str, Any]:
        """POST once, retrying only the statuses the vendor says are worth retrying.

        The key travels in the Authorization header and the path is a constant, so
        nothing here can put a credential in a URL that httpx then logs.
        """
        attempt = 0
        while True:
            try:
                response = await self._client.post(
                    f"{self.base_url}{SYSTEM_ONE_PATH}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
            except httpx.TimeoutException:
                if attempt >= 1:
                    raise
                await self._backoff(attempt, base=1.0, jitter=0.5)
                attempt += 1
                continue
            status = response.status_code
            if status in {401, 403}:
                # 403 is the vendor's "access was denied": the key is real but not
                # entitled to this model. Like 401, a second identical request cannot
                # change the answer, and the operator needs to see it.
                raise JevAuthError(
                    "Jev rejected the API key"
                    if status == 401
                    else "Jev denied this key access to the request"
                )
            if status in {400, 422}:
                # A validation failure means this module built an illegal question.
                # Retrying sends the same illegal question again.
                raise JevRequestInvalid(
                    f"Jev refused the request ({status}) for {', '.join(question_names)}: "
                    f"{_vendor_message(response)}"
                )
            if status == 429 and attempt < 2:
                await self._backoff(attempt, base=0.5, jitter=0.25, retry_after=response)
                attempt += 1
                continue
            if status == 529 and attempt < 3:
                await self._backoff(attempt, base=1.0, jitter=0.5, retry_after=response)
                attempt += 1
                continue
            if status >= 500 and attempt < 1:
                await self._backoff(attempt, base=1.0, jitter=0.5)
                attempt += 1
                continue
            response.raise_for_status()
            body = response.json()
            return body if isinstance(body, dict) else {}

    @staticmethod
    async def _backoff(
        attempt: int,
        *,
        base: float,
        jitter: float,
        retry_after: httpx.Response | None = None,
    ) -> None:
        header = retry_after.headers.get("Retry-After") if retry_after is not None else None
        if header:
            try:
                await asyncio.sleep(min(float(header), 30.0))
                return
            except ValueError:
                pass
        await asyncio.sleep(base * (2**attempt) + random.uniform(0, jitter))  # noqa: S311


def _vendor_message(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text[:120]
    if isinstance(body, dict):
        for key in ("message", "detail", "error"):
            value = body.get(key)
            if isinstance(value, str):
                return value[:160]
    return response.text[:120]


def jev_client(settings: Settings, client: httpx.AsyncClient | None = None) -> JevClient:
    if not settings.jev_configured or not settings.jev_api_key:
        raise AppError(503, "provider_unavailable", "尚未設定 Jev API 金鑰")
    return JevClient(
        settings.jev_api_key,
        settings.jev_api_base_url,
        settings.jev_model,
        settings.jev_timeout_seconds,
        max_state_tokens=settings.jev_max_state_tokens,
        max_request_tokens=settings.jev_max_request_tokens,
        client=client,
    )


async def consume_jev_call(redis: Redis, settings: Settings) -> bool:
    """Take one call off today's budget, or report that the budget is spent.

    Keyed on the UTC day rather than a billing calendar: TypeSafe publishes no billing
    timezone, and a day boundary this code invents would only be right by accident.
    """
    key = f"jev-quota:{datetime.now(UTC).date().isoformat()}"
    script = (
        "local current=tonumber(redis.call('GET',KEYS[1]) or '0'); "
        "if current>=tonumber(ARGV[1]) then return -1 end; "
        "local n=redis.call('INCR',KEYS[1]); "
        "if n==1 then redis.call('EXPIRE',KEYS[1],172800) end; return n"
    )
    try:
        count = await redis.eval(script, 1, key, str(settings.jev_daily_call_budget))
    except RedisError:
        return False
    return int(count) >= 0


Tier = Literal["act", "confirm", "hold"]


def route(
    answer: JevAnswer,
    *,
    act_at: float,
    flag_at: float,
    locale: str = "en",
    cjk_autopilot: bool = False,
) -> Tier:
    """Turn one answer into act / confirm / hold.

    Two things live here rather than in a comment. A noul answer has no ``confidence``
    -- its own value is the probability -- so it needs thresholds chosen for noul and
    not borrowed from a choice. And while ``cjk_autopilot`` is off, a confident answer
    about non-English state is downgraded to ``confirm``. TypeSafe states that
    "English is the primary training language and where accuracy is currently best"
    and publishes no accuracy figures for any other language; this product is written
    in five. Until our own numbers say otherwise, that gap is a default-closed switch.
    """
    certainty = answer.noul if isinstance(answer, NoulAnswer) else answer.confidence
    if certainty >= act_at:
        tier: Tier = "act"
    elif certainty >= flag_at:
        tier = "confirm"
    else:
        tier = "hold"
    if tier == "act" and locale != "en" and not cjk_autopilot:
        return "confirm"
    return tier


def route_answer(answer: JevAnswer, settings: Settings, *, locale: str = "en") -> Tier:
    """``route`` with this deployment's thresholds already applied.

    Callers should reach for this rather than ``route``: the three settings are the
    operator's, and a call site that passed its own numbers could quietly opt out of
    the non-English downgrade that ``jev_cjk_autopilot_enabled`` exists to enforce.
    """
    return route(
        answer,
        act_at=settings.jev_act_confidence,
        flag_at=settings.jev_flag_confidence,
        locale=locale,
        cjk_autopilot=settings.jev_cjk_autopilot_enabled,
    )


async def probe(settings: Settings, client: httpx.AsyncClient | None = None) -> str:
    """The cheapest call that proves the key, the host, the model id and the shape.

    TypeSafe documents no models endpoint, so the list-models probe every other vendor
    on the admin card uses has nothing to call here, and a 405 from a gateway would
    arrive before the key was ever checked. One real noul question over a four-word
    state is about forty input tokens; output is not billed at all.
    """
    jev = jev_client(settings, client)
    try:
        answers, _ = await jev.ask(
            "The sky is blue.",
            {"ok": NoulQuestion(instructions="The statement is true.")},
        )
    finally:
        await jev.close()
    answer = answers["ok"]
    value = answer.noul if isinstance(answer, NoulAnswer) else 0.0
    return f"Jev ✓（{settings.jev_model}；noul={value:.2f}）"
