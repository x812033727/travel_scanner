"""The owner's request to make a skipped dub track again (docs/videos/DUBS.md §再做一次).

``video_projects.dub_retries`` (migration 0131) holds, per locale, the latest request and how it
ended. This module owns every transition of that record and every rule that reads it, as pure
functions over the stored dicts, the review rows and ``now``; admin_service.py does the reading,
the writing, the audit rows and the refusals, so nothing here raises.

    requested   the owner asked; nothing else changed, the dub still reads "skipped"
    taken       the worker said it starts and the site agreed; the dub reads "working"
    made        a languages batch that counts carries the track
    skipped     the worker gave the dub up again, with the batch's reason
    refused     the worker would not start, or the re-made batch equalled one that was sent back

"expired" is a request nobody took within REQUEST_TTL. It is read from ``requested_at`` and never
stored, so ending a request that touched nothing needs no writer.

Every function that changes the record returns a new dict, and the dict it was given, the same
object, when nothing changes: the column is JSON, which does not track a change made in place.
Stored and echoed data may be anything; what cannot be read counts as no request.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, NamedTuple, cast, get_args
from uuid import UUID, uuid4

from app.models import VideoReview
from app.video_reviews.schemas import (
    DUB_LOCALES,
    DubRetryBlocker,
    DubRetryOut,
    DubRetryStatus,
)

# A request the worker has not taken ends by itself after a day: nothing was touched or bought.
REQUEST_TTL = timedelta(hours=24)
# When the page stops saying "waiting" and says the worker may be busy or away, and when a taken
# request has gone long enough without a result to point at the video's own wait or block note.
REQUEST_STALL = timedelta(minutes=30)
TAKEN_STALL = timedelta(hours=2)
# The speech a track is assumed to need when no caption file can be read: about what a
# ten-minute English track sends (docs/videos/DUBS.md §成本).
FALLBACK_CHARACTERS = 10_000
CAPTION_BYTES_MAX = 1024 * 1024
REASON_MAX = 500
# The two skips no retry can fix, as the worker writes them: the narration's own language
# (tools/video/review/sync.mjs NARRATION_DUB_SKIP, or the sentence tools/video/review/renewal.mjs
# puts in its place on every batch of a video whose final cut was renewed) and a part ticked
# after the work files were cleared (tools/video/automation/flow.mjs tidiedLanguages).
NARRATION_DUB_SKIP = "這是影片原本旁白的語言，不另做重複配音"
NARRATION_DUB_SKIP_RENEWED = (
    "This language is the original narration; no duplicate dub is generated."
)
NARRATION_DUB_SKIPS = (NARRATION_DUB_SKIP, NARRATION_DUB_SKIP_RENEWED)
TIDIED_SKIP_PREFIX = "工作檔已在 "
# How the site ends a taken request whose re-made batch is byte-identical to one that was sent
# back or superseded: submit_review answers with that review and creates none, so no card
# appears and the track counts for nothing.
SAME_AS_SENT_BACK = (
    "重做出來的音軌和先前那一批語言審核一模一樣，那一批已經被退回或被取代，"
    "網站沒有再開新的審核卡；翻譯或規則沒變之前，再做一次也會一樣"
)

# What the column holds; DubRetryStatus adds the derived "expired".
StoredStatus = Literal["requested", "taken", "made", "skipped", "refused"]
STORED: tuple[StoredStatus, ...] = get_args(StoredStatus)
EPOCH = datetime.min.replace(tzinfo=UTC)


class SpeechRoom(NamedTuple):
    """The month's Gemini speech meter as the route read it, for the check at the click."""

    configured: bool
    limit: int
    used: int | None
    available: bool


class Event(NamedTuple):
    """An audit row a transition asks for; ``details`` is its metadata without the slug."""

    action: str
    details: dict[str, Any]


class Applied(NamedTuple):
    """The record after a transition and the audit rows it asks for. ``retries`` is the object
    that was passed in when ``events`` is empty."""

    retries: dict[str, Any]
    events: list[Event]


def _time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _id(value: Any) -> UUID | None:
    if not isinstance(value, str):
        return None
    try:
        return UUID(value)
    except ValueError:
        return None


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


class _Stored(NamedTuple):
    id: UUID
    status: StoredStatus
    requested_at: datetime


def _stored(entry: Any) -> _Stored | None:
    """A stored record's identity, or None for anything that is not one: a dict with a parsable
    id, a known status and a parsable request time."""
    if not isinstance(entry, dict):
        return None
    request_id = _id(entry.get("id"))
    status = entry.get("status")
    requested_at = _time(entry.get("requested_at"))
    if request_id is None or requested_at is None or status not in STORED:
        return None
    return _Stored(request_id, cast(StoredStatus, status), requested_at)


def _expired(stored: _Stored, now: datetime) -> bool:
    return stored.status == "requested" and now - stored.requested_at > REQUEST_TTL


def new_request(
    *, user_id: UUID, reason: str | None, characters: int, now: datetime
) -> dict[str, Any]:
    """The record of a fresh request: who asked, when, the skip reason it replaces and the
    speech it was estimated to need at the click."""
    return {
        "id": str(uuid4()),
        "status": "requested",
        "requested_at": now.isoformat(),
        "requested_by": str(user_id),
        "replaced_reason": reason,
        "estimated_characters": characters,
        "taken_at": None,
        "finished_at": None,
        "reason": None,
    }


def view(entry: Any, now: datetime) -> DubRetryOut | None:
    """A stored record as the page and the worker read it, or None when there is none."""
    stored = _stored(entry)
    if stored is None:
        return None
    status: DubRetryStatus = "expired" if _expired(stored, now) else stored.status
    taken_at = _time(entry.get("taken_at"))
    is_open = status in ("requested", "taken")
    if status == "requested":
        stalled = now - stored.requested_at > REQUEST_STALL
    elif status == "taken":
        stalled = now - (taken_at or stored.requested_at) > TAKEN_STALL
    else:
        stalled = False
    return DubRetryOut(
        id=stored.id,
        status=status,
        open=is_open,
        stalled=stalled,
        requested_at=stored.requested_at,
        taken_at=taken_at,
        finished_at=_time(entry.get("finished_at")),
        reason=_text(entry.get("reason")),
        replaced_reason=_text(entry.get("replaced_reason")),
    )


def views(
    retries: dict[str, Any], dub_locales: Iterable[str], now: datetime
) -> dict[str, DubRetryOut]:
    """The requests of the dubs chosen now, by locale. A request for a dub that is no longer
    chosen is not shown: it is paused, not ended, and comes back when the dub is ticked again."""
    if not isinstance(retries, dict):
        return {}
    shown: dict[str, DubRetryOut] = {}
    for locale in dub_locales:
        out = view(retries.get(locale), now)
        if out is not None:
            shown[locale] = out
    return shown


def reads_working(entry: Any) -> bool:
    """Whether this record makes its dub read "working": the worker took it and has not answered.
    A request that is only asked changes nothing, so an older worker never sees a part to make."""
    stored = _stored(entry)
    return stored is not None and stored.status == "taken"


def apply_worker(retries: dict[str, Any], said: Any, now: datetime) -> Applied:
    """The worker's echo in its report: ``{"ja": {"id", "status": "taken"}}`` or
    ``{"id", "status": "refused", "reason"}``.

    An echo moves only the request it names by id. "taken" takes a request that is still waiting
    and not expired; "refused" ends one that is waiting or taken, once. A request that already
    ended keeps its first ending, and anything not understood is ignored.
    """
    if not isinstance(said, dict) or not isinstance(retries, dict):
        return Applied(retries, [])
    changed: dict[str, Any] = {}
    events: list[Event] = []
    for locale in DUB_LOCALES:
        echo = said.get(locale)
        stored = _stored(retries.get(locale))
        if not isinstance(echo, dict) or stored is None or _id(echo.get("id")) != stored.id:
            continue
        status = echo.get("status")
        base = {"locale": locale, "request_id": str(stored.id)}
        if status == "taken" and stored.status == "requested" and not _expired(stored, now):
            changed[locale] = {**retries[locale], "status": "taken", "taken_at": now.isoformat()}
            events.append(Event("video_dub_retry_taken", base))
        elif status == "refused" and stored.status in ("requested", "taken"):
            reason = _text(echo.get("reason"))
            reason = reason[:REASON_MAX] if reason is not None else None
            changed[locale] = {
                **retries[locale],
                "status": "refused",
                "finished_at": now.isoformat(),
                "reason": reason,
            }
            events.append(
                Event(
                    "video_dub_retry_finished",
                    {**base, "outcome": "refused", "reason": reason, "via": "report"},
                )
            )
    if not events:
        return Applied(retries, [])
    return Applied({**retries, **changed}, events)


def close_on_batch(
    retries: dict[str, Any],
    reported: dict[str, tuple[str | None, str | None]],
    now: datetime,
    *,
    counted: bool = True,
) -> Applied:
    """What a languages batch does to the requests of the dubs it names.

    ``reported`` is, per locale, the dub's state in the batch ("ready" or "skipped") and a
    skip's reason. ``counted`` says whether the review the site answers with is one the states
    are read from (pending or approved); it is false when the batch equals one that was sent
    back or superseded, which creates no review.

    A track that counts ends an open request as made, taken or not: a worker that never echoed
    still made it. A track that does not count ends a taken request as refused, with
    SAME_AS_SENT_BACK. A skip ends a taken request as skipped with its reason; before the take
    it is only the old skip, restated, and changes nothing.
    """
    if not isinstance(retries, dict):
        return Applied(retries, [])
    changed: dict[str, Any] = {}
    events: list[Event] = []
    for locale, (state, why) in reported.items():
        stored = _stored(retries.get(locale))
        if stored is None or stored.status not in ("requested", "taken"):
            continue
        outcome: StoredStatus | None = None
        reason: str | None = None
        if state == "ready" and counted:
            outcome = "made"
        elif state == "ready" and stored.status == "taken":
            outcome, reason = "refused", SAME_AS_SENT_BACK
        elif state == "skipped" and stored.status == "taken":
            outcome, reason = "skipped", _text(why)
        if outcome is None:
            continue
        changed[locale] = {
            **retries[locale],
            "status": outcome,
            "finished_at": now.isoformat(),
            "reason": reason,
        }
        events.append(
            Event(
                "video_dub_retry_finished",
                {
                    "locale": locale,
                    "request_id": str(stored.id),
                    "outcome": outcome,
                    "reason": reason,
                    "via": "batch",
                },
            )
        )
    if not events:
        return Applied(retries, [])
    return Applied({**retries, **changed}, events)


def withdraw_unchosen(
    retries: dict[str, Any], dub_locales: Iterable[str]
) -> tuple[dict[str, Any], list[str]]:
    """The record without the waiting requests of dubs that are no longer chosen, and their
    locales. A waiting request touched nothing, expired or not, so it simply goes; a taken one
    stays, hidden until its dub is ticked again."""
    if not isinstance(retries, dict):
        return retries, []
    kept = set(dub_locales)
    withdrawn = sorted(
        locale
        for locale, entry in retries.items()
        if locale not in kept and isinstance(entry, dict) and entry.get("status") == "requested"
    )
    if not withdrawn:
        return retries, []
    return {
        locale: entry for locale, entry in retries.items() if locale not in withdrawn
    }, withdrawn


def blocker(
    *,
    reason: str | None,
    tidied_at: str | None,
    producer: str | None,
    stage: str | None,
    publish_usable: bool,
) -> DubRetryBlocker | None:
    """Why a skipped dub cannot be asked for again now, or None: the first that applies.

    ``reason`` is the skip's reason on the panel, ``tidied_at`` and ``producer`` what the
    worker's auto.json says (producer_state.worker_view), ``stage`` the video's reported stage.
    A work directory the API cannot read ("unavailable", or no producer at all) blocks nothing:
    it is not evidence of anything.
    """
    if reason in NARRATION_DUB_SKIPS:
        return "narration"
    if tidied_at or (reason or "").startswith(TIDIED_SKIP_PREFIX):
        return "tidied"
    if not publish_usable:
        return "publish_pending"
    if producer in ("not_adopted", "dropped"):
        return "not_adopted"
    if producer == "blocked" or stage == "blocked":
        return "blocked"
    if producer == "stopped":
        return "stopped"
    return None


def publish_usable(reviews: Iterable[VideoReview], *, on_youtube: bool) -> bool:
    """Whether a languages batch made now could be bound and used.

    The producer binds a batch to the site's newest upload confirmation and refuses unless that
    one is approved or waiting (languageSource, tools/video/review/sync.mjs), whatever came
    before it; and a batch is read for YouTube only once a confirmation was approved, which a
    video the owner linked to YouTube by hand may never have had on the site. So: the newest
    confirmation exists and is approved or pending, and the video is on YouTube or some
    confirmation is approved. A review with a subject is not an upload confirmation.
    """
    confirmations = [
        review for review in reviews if review.gate == "publish" and review.subject is None
    ]
    if not confirmations:
        return False
    newest = max(confirmations, key=lambda review: review.created_at or EPOCH)
    if newest.status not in ("approved", "pending"):
        return False
    return on_youtube or any(review.status == "approved" for review in confirmations)


def caption_sha(reviews: Iterable[VideoReview], locale: str) -> str | None:
    """The SHA-256 of the locale's caption file in the newest languages batch that counts and
    has one: the text a dub reads, and so the size of a track."""
    role = f"captions_{locale}"
    batches = sorted(
        (
            review
            for review in reviews
            if review.gate == "languages" and review.status in ("pending", "approved")
        ),
        key=lambda review: review.created_at or EPOCH,
        reverse=True,
    )
    for review in batches:
        for item in review.files or []:
            if isinstance(item, dict) and item.get("role") == role:
                sha = item.get("sha256")
                if isinstance(sha, str) and sha:
                    return sha
    return None


def estimate_characters(srt: str | None) -> int:
    """About how many characters of speech a track of these captions sends: the text lines of
    the SRT, without the cue numbers and the timings. FALLBACK_CHARACTERS without a file."""
    if srt is None:
        return FALLBACK_CHARACTERS
    total = 0
    for line in srt.splitlines():
        text = line.strip()
        if not text or text.isdigit() or "-->" in text:
            continue
        total += len(text)
    return total
