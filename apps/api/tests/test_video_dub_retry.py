"""Asking for a skipped dub track again (docs/videos/DUBS.md §再做一次).

First the record's own rules, as pure functions over dicts and review rows
(app/video_reviews/dub_retry.py). Then the service on real rows in SQLite: the owner's request
and its refusals, the worker's echo in its report, the languages batch that closes a request,
and what the page and the worker's list read at each moment. The PostgreSQL round trip is in
test_video_reviews_integration.py.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast, get_args
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.models import AdminAuditLog, VideoProject, VideoReview
from app.problems import AppError
from app.video_reviews import admin_service as service
from app.video_reviews import dub_retry
from app.video_reviews.schemas import (
    DubLocale,
    DubLocalesIn,
    DubRetryBlocker,
    LocalesIn,
    ProjectIn,
    ProjectOut,
    ReviewIn,
)
from tests.test_video_review_renewal import SLUG, Site, _audits, _decide, _file, _rows, _submit
from tests.test_video_review_renewal import site as _site

site = _site  # The renewal tests' real SQLite database, without collecting their tests here.

REPO = Path(__file__).resolve().parents[3]
NOW = datetime(2026, 10, 10, 12, 40, 3, 118203, tzinfo=UTC)
LATER = NOW + timedelta(minutes=4)
OWNER = uuid4()
SKIP = "k7p2 does not fit its window even at 1.15x after 2 shortening rounds"
AGAIN = "k7p2 還是塞不進它的時間窗"
TIDIED_AT = "2026-10-08T03:00:00.000Z"
# What the worker answers for a part ticked after the work files were cleared (flow.mjs
# tidiedLanguages): a skip no retry can fix, known from its opening words.
TIDIED_SKIP = (
    "工作檔已在 2026-10-08 清掉，成片與旁白都不在了，"
    "清理後才勾的部件做不出來；要這個語言得重做影片"
)


def _entry(status: str = "requested", *, at: datetime = NOW, **more: Any) -> dict[str, Any]:
    entry = dub_retry.new_request(user_id=OWNER, reason=SKIP, characters=6120, now=at)
    return {**entry, "status": status, **more}


def _finished(
    locale: str, entry: dict[str, Any], outcome: str, reason: str | None, via: str
) -> dub_retry.Event:
    return dub_retry.Event(
        "video_dub_retry_finished",
        {
            "locale": locale,
            "request_id": entry["id"],
            "outcome": outcome,
            "reason": reason,
            "via": via,
        },
    )


# --- the record: pure functions --------------------------------------------------------------


def test_a_new_request_records_who_asked_when_and_what_it_replaces() -> None:
    entry = dub_retry.new_request(user_id=OWNER, reason=SKIP, characters=6120, now=NOW)
    assert UUID(entry["id"]).version == 4
    assert {key: value for key, value in entry.items() if key != "id"} == {
        "status": "requested",
        "requested_at": "2026-10-10T12:40:03.118203+00:00",
        "requested_by": str(OWNER),
        "replaced_reason": SKIP,
        "estimated_characters": 6120,
        "taken_at": None,
        "finished_at": None,
        "reason": None,
    }
    assert json.loads(json.dumps(entry)) == entry, "it is stored in a JSON column as it is"
    other = dub_retry.new_request(user_id=OWNER, reason=None, characters=1, now=NOW)
    assert other["id"] != entry["id"] and other["replaced_reason"] is None

    out = dub_retry.view(entry, NOW)
    assert out is not None
    assert (out.id, out.status, out.open, out.stalled) == (
        UUID(entry["id"]),
        "requested",
        True,
        False,
    )
    assert out.requested_at == NOW and out.replaced_reason == SKIP
    assert out.taken_at is None and out.finished_at is None and out.reason is None

    # Anything that is not a record with an id, a known status and a time reads as no request.
    unreadable: list[Any] = [
        None,
        "requested",
        [],
        {},
        {**entry, "id": "not-a-uuid"},
        {**entry, "id": None},
        {**entry, "status": "expired"},
        {**entry, "status": "withdrawn"},
        {**entry, "requested_at": "yesterday"},
        {**entry, "requested_at": None},
    ]
    for bad in unreadable:
        assert dub_retry.view(bad, NOW) is None, bad
        assert not dub_retry.reads_working(bad), bad

    # Only the dubs chosen now show their request; the others are hidden, not gone.
    retries = {"ja": entry, "ko": _entry("taken"), "en": {"id": "broken"}}
    assert list(dub_retry.views(retries, ["en", "ja"], NOW)) == ["ja"]
    assert list(dub_retry.views(retries, ["ja", "ko"], NOW)) == ["ja", "ko"]
    assert dub_retry.views(retries, [], NOW) == {}


def test_a_request_nobody_took_for_a_day_reads_expired_and_closed() -> None:
    entry = _entry()
    edge = dub_retry.view(entry, NOW + dub_retry.REQUEST_TTL)
    assert edge is not None and (edge.status, edge.open, edge.stalled) == (
        "requested",
        True,
        True,
    )
    late = dub_retry.view(entry, NOW + dub_retry.REQUEST_TTL + timedelta(seconds=1))
    assert late is not None and (late.status, late.open, late.stalled) == (
        "expired",
        False,
        False,
    )
    assert late.requested_at == NOW and late.replaced_reason == SKIP
    assert entry["status"] == "requested", "expiry is read, never stored"
    assert dub_retry.REQUEST_TTL == timedelta(hours=24)
    # The worker's "taken" no longer takes it: the answer shows it expired and nothing starts.
    retries = {"ja": entry}
    echo = {"ja": {"id": entry["id"], "status": "taken"}}
    applied = dub_retry.apply_worker(retries, echo, NOW + timedelta(hours=25))
    assert applied.retries is retries and applied.events == []


def test_a_taken_request_never_expires_and_reads_stalled_after_two_hours() -> None:
    taken_at = NOW + timedelta(minutes=5)
    entry = _entry("taken", taken_at=taken_at.isoformat())
    assert dub_retry.reads_working(entry)
    fresh = dub_retry.view(entry, taken_at + dub_retry.TAKEN_STALL)
    assert fresh is not None and (fresh.status, fresh.open, fresh.stalled) == (
        "taken",
        True,
        False,
    )
    assert fresh.taken_at == taken_at
    late = dub_retry.view(entry, taken_at + dub_retry.TAKEN_STALL + timedelta(seconds=1))
    assert late is not None and (late.status, late.open, late.stalled) == ("taken", True, True)
    month = dub_retry.view(entry, NOW + timedelta(days=30))
    assert month is not None and (month.status, month.open) == ("taken", True), "no timer"
    assert dub_retry.TAKEN_STALL == timedelta(hours=2)
    # A record without its take time is counted from the request.
    bare = dub_retry.view(_entry("taken"), NOW + timedelta(hours=2, seconds=1))
    assert bare is not None and bare.taken_at is None and bare.stalled


def test_a_requested_one_reads_stalled_after_thirty_minutes() -> None:
    entry = _entry()
    assert not dub_retry.reads_working(entry), "asked is not being made"
    fresh = dub_retry.view(entry, NOW + dub_retry.REQUEST_STALL)
    assert fresh is not None and (fresh.status, fresh.open, fresh.stalled) == (
        "requested",
        True,
        False,
    )
    late = dub_retry.view(entry, NOW + dub_retry.REQUEST_STALL + timedelta(seconds=1))
    assert late is not None and (late.status, late.open, late.stalled) == (
        "requested",
        True,
        True,
    )
    assert dub_retry.REQUEST_STALL == timedelta(minutes=30)
    # A request that ended is never open or stalled, however old.
    for status in ("made", "skipped", "refused"):
        ended = _entry(status, finished_at=LATER.isoformat(), reason="r")
        out = dub_retry.view(ended, NOW + timedelta(days=3))
        assert out is not None and (out.status, out.open, out.stalled) == (status, False, False)
        assert out.finished_at == LATER and out.reason == "r"
        assert not dub_retry.reads_working(ended)


def test_the_worker_s_taken_moves_only_a_live_request_with_the_same_id() -> None:
    entry = _entry()
    retries = {"ja": entry}
    echo = {"ja": {"id": entry["id"], "status": "taken"}}
    applied = dub_retry.apply_worker(retries, echo, LATER)
    assert applied.retries is not retries and retries == {"ja": entry}, "the input is not touched"
    assert applied.retries["ja"] == {**entry, "status": "taken", "taken_at": LATER.isoformat()}
    assert applied.events == [
        dub_retry.Event("video_dub_retry_taken", {"locale": "ja", "request_id": entry["id"]})
    ]
    # The same echo again (a lost answer, a second lane) is a no-op.
    again = dub_retry.apply_worker(applied.retries, echo, LATER + timedelta(minutes=1))
    assert again.retries is applied.retries and again.events == []

    stale = {"ja": {"id": str(uuid4()), "status": "taken"}}
    elsewhere = {"ko": {"id": entry["id"], "status": "taken"}}
    cases: list[tuple[dict[str, Any], dict[str, Any]]] = [
        (retries, stale),
        (retries, elsewhere),
        ({}, echo),
        ({"ja": {**entry, "requested_at": "?"}}, echo),
        ({"ja": {**entry, "status": "made"}}, echo),
        ({"ja": {**entry, "status": "skipped"}}, echo),
        ({"ja": {**entry, "status": "refused"}}, echo),
    ]
    for stored, said in cases:
        left = dub_retry.apply_worker(stored, said, LATER)
        assert left.retries is stored and left.events == [], (stored, said)


def test_a_refusal_closes_a_requested_or_taken_request_once_with_its_reason_cut_to_500() -> None:
    long = "成" * 600
    for status in ("requested", "taken"):
        entry = _entry(status)
        retries = {"ja": entry, "ko": _entry()}
        said = {"ja": {"id": entry["id"], "status": "refused", "reason": long}}
        applied = dub_retry.apply_worker(retries, said, LATER)
        closed = applied.retries["ja"]
        assert closed == {
            **entry,
            "status": "refused",
            "finished_at": LATER.isoformat(),
            "reason": "成" * dub_retry.REASON_MAX,
        }
        assert applied.retries["ko"] is retries["ko"], "another locale's request is not touched"
        assert applied.events == [_finished("ja", entry, "refused", "成" * 500, "report")]
        out = dub_retry.view(closed, LATER)
        assert out is not None and (out.status, out.open, out.reason) == (
            "refused",
            False,
            "成" * 500,
        )
        assert not dub_retry.reads_working(closed)
        # The first ending stands: a second refusal or a late "taken" changes nothing.
        for word in ("refused", "taken"):
            late = {"ja": {"id": entry["id"], "status": word, "reason": "another"}}
            again = dub_retry.apply_worker(applied.retries, late, LATER + timedelta(minutes=1))
            assert again.retries is applied.retries and again.events == []
    assert dub_retry.REASON_MAX == 500
    # A refusal without a sentence still ends the request; so does one for a request that had
    # already run out its day, whose stored status is still "requested".
    silent = _entry(at=NOW - timedelta(days=2))
    applied = dub_retry.apply_worker(
        {"ja": silent}, {"ja": {"id": silent["id"], "status": "refused", "reason": 7}}, LATER
    )
    assert (applied.retries["ja"]["status"], applied.retries["ja"]["reason"]) == ("refused", None)
    assert applied.events == [_finished("ja", silent, "refused", None, "report")]


def test_an_echo_that_is_not_understood_changes_nothing() -> None:
    entry = _entry()
    retries = {"ja": entry}
    named = {"id": entry["id"], "status": "taken"}
    echoes: list[Any] = [
        None,
        "taken",
        [],
        7,
        {},
        {"ja": "taken"},
        {"ja": None},
        {"ja": {}},
        {"ja": {"status": "taken"}},
        {"ja": {"id": 5, "status": "taken"}},
        {"ja": {"id": entry["id"]}},
        {"ja": {"id": entry["id"], "status": "made"}},
        {"ja": {"id": entry["id"], "status": "skipped"}},
        {"ja": {"id": entry["id"], "status": "requested"}},
        {"ja": {"id": entry["id"], "status": ["taken"]}},
        {"fr": named},
        {"zh-CN": named},
        {"zh-TW": named},
    ]
    for said in echoes:
        applied = dub_retry.apply_worker(retries, said, LATER)
        assert applied.retries is retries and applied.events == [], said
    # Stored data that is not a record neither raises nor moves.
    garbage: list[dict[str, Any]] = [
        {"ja": None},
        {"ja": "x"},
        {"ja": {"id": entry["id"]}},
        {"ja": {**entry, "status": 3}},
    ]
    for stored in garbage:
        applied = dub_retry.apply_worker(stored, {"ja": named}, LATER)
        assert applied.retries is stored and applied.events == [], stored
        closed = dub_retry.close_on_batch(stored, {"ja": ("ready", None)}, LATER)
        assert closed.retries is stored and closed.events == [], stored
    # The report's field is as lenient: a malformed echo must not refuse the whole report.
    assert ProjectIn(title="t", stage="s").dub_retries is None
    for raw in ("taken", ["ja"], 3, None):
        report = ProjectIn.model_validate({"title": "t", "stage": "s", "dub_retries": raw})
        assert report.dub_retries is None, raw
    kept = ProjectIn.model_validate({"title": "t", "stage": "s", "dub_retries": {"ja": 1}})
    assert kept.dub_retries == {"ja": 1}


def test_a_batch_with_the_track_closes_an_open_request_as_made() -> None:
    for status in ("requested", "taken"):
        entry = _entry(status)
        retries = {"ja": entry, "ko": _entry("taken")}
        applied = dub_retry.close_on_batch(
            retries, {"ja": ("ready", None), "en": ("ready", None)}, LATER
        )
        assert applied.retries is not retries and retries["ja"] is entry
        assert applied.retries["ja"] == {
            **entry,
            "status": "made",
            "finished_at": LATER.isoformat(),
            "reason": None,
        }
        assert applied.retries["ko"] is retries["ko"], "a dub the batch does not name stays open"
        assert applied.events == [_finished("ja", entry, "made", None, "batch")]
        out = dub_retry.view(applied.retries["ja"], LATER)
        assert out is not None and (out.status, out.open, out.finished_at) == (
            "made",
            False,
            LATER,
        )
    # A worker that never echoed, on a request past its day, still made the track.
    old = _entry(at=NOW - timedelta(days=3))
    applied = dub_retry.close_on_batch({"ja": old}, {"ja": ("ready", None)}, LATER)
    assert applied.retries["ja"]["status"] == "made"
    # A request that already ended, a batch that does not name the dub, a state that is not an
    # answer: nothing changes, and the same object comes back.
    for ended in ("made", "skipped", "refused"):
        stored = {"ja": _entry(ended)}
        left = dub_retry.close_on_batch(stored, {"ja": ("ready", None)}, LATER)
        assert left.retries is stored and left.events == []
    taken = {"ja": _entry("taken")}
    silent: list[dict[str, tuple[str | None, str | None]]] = [
        {},
        {"ko": ("ready", None)},
        {"ja": (None, None)},
        {"ja": ("working", None)},
        {"ja": ("uploaded", None)},
    ]
    for reported in silent:
        left = dub_retry.close_on_batch(taken, reported, LATER)
        assert left.retries is taken and left.events == [], reported


def test_a_batch_that_skips_the_dub_closes_a_taken_request_and_leaves_a_requested_one() -> None:
    taken, waiting = _entry("taken"), _entry()
    retries = {"ja": taken, "ko": waiting}
    applied = dub_retry.close_on_batch(
        retries, {"ja": ("skipped", AGAIN), "ko": ("skipped", SKIP)}, LATER
    )
    assert applied.retries["ja"] == {
        **taken,
        "status": "skipped",
        "finished_at": LATER.isoformat(),
        "reason": AGAIN,
    }
    assert applied.retries["ko"] is waiting, "before the take that is the old skip, restated"
    assert applied.events == [_finished("ja", taken, "skipped", AGAIN, "batch")]
    out = dub_retry.view(applied.retries["ja"], LATER)
    assert out is not None and (out.status, out.open, out.reason, out.replaced_reason) == (
        "skipped",
        False,
        AGAIN,
        SKIP,
    )
    alone = {"ko": waiting}
    left = dub_retry.close_on_batch(alone, {"ko": ("skipped", SKIP)}, LATER)
    assert left.retries is alone and left.events == []
    # Whether the review counts does not matter for a skip, and a skip without a reason closes.
    for counted in (True, False):
        bare = dub_retry.close_on_batch(
            {"ja": taken}, {"ja": ("skipped", None)}, LATER, counted=counted
        )
        assert (bare.retries["ja"]["status"], bare.retries["ja"]["reason"]) == ("skipped", None)


def test_unticking_withdraws_only_requested_entries_of_the_locales_dropped() -> None:
    waiting, old = _entry(), _entry(at=NOW - timedelta(days=2))
    taken, made = _entry("taken"), _entry("made")
    retries = {"en": waiting, "ja": taken, "ko": old}
    kept, withdrawn = dub_retry.withdraw_unchosen(retries, ["ja"])
    assert withdrawn == ["en", "ko"], "an expired request is still a requested entry"
    assert kept == {"ja": taken} and kept is not retries
    assert retries == {"en": waiting, "ja": taken, "ko": old}, "the input is not touched"
    kept, withdrawn = dub_retry.withdraw_unchosen(retries, [])
    assert (kept, withdrawn) == ({"ja": taken}, ["en", "ko"]), "a taken one stays, un-ticked"
    kept, withdrawn = dub_retry.withdraw_unchosen(retries, ["en"])
    assert (kept, withdrawn) == ({"en": waiting, "ja": taken}, ["ko"])
    same, none = dub_retry.withdraw_unchosen(retries, ["en", "ja", "ko"])
    assert same is retries and none == []
    ended = {"en": made, "ja": taken, "ko": _entry("refused")}
    same, none = dub_retry.withdraw_unchosen(ended, [])
    assert same is ended and none == [], "only a waiting request is withdrawn"
    empty: dict[str, Any] = {}
    assert dub_retry.withdraw_unchosen(empty, [])[0] is empty


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ({}, None),
        ({"producer": "unavailable"}, None),
        ({"producer": "registered"}, None),
        ({"producer": "done", "stage": "languages"}, None),
        (
            {
                "reason": dub_retry.NARRATION_DUB_SKIP,
                "tidied_at": TIDIED_AT,
                "publish_usable": False,
                "producer": "blocked",
                "stage": "blocked",
            },
            "narration",
        ),
        ({"reason": dub_retry.NARRATION_DUB_SKIP_RENEWED, "producer": "stopped"}, "narration"),
        ({"tidied_at": TIDIED_AT, "publish_usable": False, "producer": "blocked"}, "tidied"),
        ({"reason": TIDIED_SKIP, "publish_usable": False, "producer": "stopped"}, "tidied"),
        ({"reason": None, "tidied_at": TIDIED_AT}, "tidied"),
        ({"tidied_at": ""}, None),
        ({"publish_usable": False, "producer": "not_adopted"}, "publish_pending"),
        ({"publish_usable": False, "producer": "blocked", "stage": "blocked"}, "publish_pending"),
        ({"publish_usable": False}, "publish_pending"),
        ({"producer": "not_adopted", "stage": "blocked"}, "not_adopted"),
        ({"producer": "dropped"}, "not_adopted"),
        ({"producer": "blocked"}, "blocked"),
        ({"producer": "stopped", "stage": "blocked"}, "blocked"),
        ({"producer": None, "stage": "blocked"}, "blocked"),
        ({"producer": "unavailable", "stage": "blocked"}, "blocked"),
        ({"producer": "stopped"}, "stopped"),
    ],
)
def test_the_blocker_reads_narration_tidied_publish_worker_in_that_order(
    given: dict[str, Any], expected: str | None
) -> None:
    base: dict[str, Any] = {
        "reason": SKIP,
        "tidied_at": None,
        "producer": None,
        "stage": "done",
        "publish_usable": True,
    }
    assert dub_retry.blocker(**{**base, **given}) == expected
    assert expected is None or expected in get_args(DubRetryBlocker)


def _confirmation(status: str, day: int, subject: str | None = None) -> VideoReview:
    return VideoReview(
        id=uuid4(),
        gate="publish",
        subject=subject,
        status=status,
        content_sha256=f"{day:02d}" * 32,
        summary="上傳包",
        payload={},
        files=[],
        created_at=datetime(2026, 10, day, tzinfo=UTC),
    )


def test_a_batch_can_be_bound_only_to_an_approved_or_waiting_newest_confirmation() -> None:
    def usable(rows: list[VideoReview], on_youtube: bool) -> bool:
        forwards = dub_retry.publish_usable(rows, on_youtube=on_youtube)
        backwards = dub_retry.publish_usable(reversed(rows), on_youtube=on_youtube)
        assert forwards == backwards, "the rows may come in any order"
        return forwards

    approved, older = _confirmation("approved", 3), _confirmation("approved", 1)
    # The newest is approved; or it waits beside an older approved one; or it waits on a video
    # that is on YouTube already.
    assert usable([approved], False) and usable([approved], True)
    assert usable([older, _confirmation("pending", 5)], False)
    assert usable([_confirmation("pending", 5)], True)
    # The newest was sent back, although an older one is approved: the producer binds no batch.
    for on_youtube in (False, True):
        assert not usable([older, approved, _confirmation("rejected", 5)], on_youtube)
        assert not usable([approved, _confirmation("superseded", 5)], on_youtube)
        assert not usable([], on_youtube), "no confirmation on the site at all"
    # It waits, none was ever approved, and the video is not on YouTube.
    assert not usable([_confirmation("pending", 5)], False)
    assert not usable([_confirmation("rejected", 1), _confirmation("pending", 5)], False)
    # A review with a subject is not an upload confirmation, newest or approved.
    assert usable([approved, _confirmation("rejected", 7, subject="style")], False)
    assert not usable([_confirmation("approved", 7, subject="style")], True)
    assert not usable(
        [_confirmation("approved", 1, subject="style"), _confirmation("pending", 5)], False
    )
    # Other gates are not confirmations either.
    final = VideoReview(
        id=uuid4(), gate="final", status="approved", content_sha256="f" * 64, created_at=NOW
    )
    assert not usable([final], True) and usable([final, approved], False)


def test_a_ready_batch_the_site_answers_with_a_sent_back_review_refuses_a_taken_request() -> None:
    taken, waiting = _entry("taken"), _entry()
    retries = {"ja": taken, "ko": waiting, "en": _entry("taken")}
    applied = dub_retry.close_on_batch(
        retries,
        {"ja": ("ready", None), "ko": ("ready", None), "en": ("skipped", AGAIN)},
        LATER,
        counted=False,
    )
    assert applied.retries["ja"] == {
        **taken,
        "status": "refused",
        "finished_at": LATER.isoformat(),
        "reason": dub_retry.SAME_AS_SENT_BACK,
    }
    assert applied.retries["ko"] is waiting, "nothing was taken yet; the worker still takes it"
    assert applied.retries["en"]["status"] == "skipped", "a skip closes whatever the review is"
    assert applied.events == [
        _finished("ja", taken, "refused", dub_retry.SAME_AS_SENT_BACK, "batch"),
        _finished("en", retries["en"], "skipped", AGAIN, "batch"),
    ]
    out = dub_retry.view(applied.retries["ja"], LATER)
    assert out is not None and (out.status, out.open, out.reason) == (
        "refused",
        False,
        dub_retry.SAME_AS_SENT_BACK,
    )
    assert dub_retry.SAME_AS_SENT_BACK == (
        "重做出來的音軌和先前那一批語言審核一模一樣，那一批已經被退回或被取代，"
        "網站沒有再開新的審核卡；翻譯或規則沒變之前，再做一次也會一樣"
    )
    # The same batch on a review that counts is a made track.
    counted = dub_retry.close_on_batch({"ja": taken}, {"ja": ("ready", None)}, LATER)
    assert counted.retries["ja"]["status"] == "made"


def test_every_blocker_code_has_a_sentence_in_the_admin_catalog() -> None:
    """The page prints ``dubRetryBlocked.<code>`` for the code the API sends, and prints nothing
    for a code it has no sentence for: the two sets must be one."""
    path = REPO / "apps" / "web" / "messages" / "en" / "admin.json"
    if not path.is_file():
        pytest.skip("the web catalog is not in this checkout")
    catalog = json.loads(path.read_text(encoding="utf-8"))
    sentences = catalog["videoReviews"].get("dubRetryBlocked") or {}
    assert set(get_args(DubRetryBlocker)) == set(sentences)
    assert all(isinstance(text, str) and text.strip() for text in sentences.values())


def test_the_estimate_counts_caption_text_only_and_falls_back_without_a_file() -> None:
    srt = (
        "1\n00:00:01,000 --> 00:00:03,000\nこんにちは、世界\n\n"
        "2\n00:00:03,500 --> 00:00:05,000\n  二行目です  \n3 つ目\n"
    )
    expected = len("こんにちは、世界") + len("二行目です") + len("3 つ目")
    assert dub_retry.estimate_characters(srt) == expected == 17
    assert dub_retry.estimate_characters(srt.replace("\n", "\r\n")) == expected
    assert dub_retry.estimate_characters("") == 0
    assert dub_retry.estimate_characters(None) == dub_retry.FALLBACK_CHARACTERS == 10_000

    # The file is the locale's captions in the newest batch that counts and has one.
    def batch(status: str, day: int, files: list[dict[str, Any]]) -> VideoReview:
        return VideoReview(
            id=uuid4(),
            gate="languages",
            status=status,
            content_sha256=f"{day:02d}" * 32,
            payload={},
            files=files,
            created_at=datetime(2026, 10, day, tzinfo=UTC),
        )

    def captions(locale: str, sha: str) -> dict[str, Any]:
        return {"role": f"captions_{locale}", "sha256": sha * 64}

    rows = [
        batch("approved", 1, [captions("ja", "1"), captions("en", "e")]),
        batch("approved", 3, [captions("ja", "3")]),
        batch("pending", 5, [captions("en", "5")]),
        batch("rejected", 7, [captions("ja", "7")]),
        batch("superseded", 8, [captions("ja", "8")]),
        VideoReview(
            gate="publish",
            status="approved",
            content_sha256="9" * 64,
            files=[captions("ja", "9")],
            created_at=datetime(2026, 10, 9, tzinfo=UTC),
        ),
    ]
    for order in (rows, rows[::-1]):
        assert dub_retry.caption_sha(order, "ja") == "3" * 64
        assert dub_retry.caption_sha(order, "en") == "5" * 64
        assert dub_retry.caption_sha(order, "ko") is None
    assert dub_retry.caption_sha([], "ja") is None
    assert dub_retry.CAPTION_BYTES_MAX == 1024 * 1024


def test_the_narration_sentence_is_the_one_the_worker_writes() -> None:
    """The narration's own language is told from the skip reason alone, so the sentence here
    must be the producer's, character for character."""
    path = REPO / "tools" / "video" / "review" / "sync.mjs"
    if not path.is_file():
        pytest.skip("the video tools are not in this checkout")
    source = path.read_text(encoding="utf-8")
    assert f'const NARRATION_DUB_SKIP = "{dub_retry.NARRATION_DUB_SKIP}";' in source
    # A video whose final cut was renewed sends the same skip in another sentence.
    renewed = (REPO / "tools" / "video" / "review" / "renewal.mjs").read_text(encoding="utf-8")
    assert f'reason: "{dub_retry.NARRATION_DUB_SKIP_RENEWED}"' in renewed
    assert dub_retry.NARRATION_DUB_SKIPS == (
        dub_retry.NARRATION_DUB_SKIP,
        dub_retry.NARRATION_DUB_SKIP_RENEWED,
    )


def test_the_tidied_prefix_is_how_the_worker_starts_that_skip_reason() -> None:
    path = REPO / "tools" / "video" / "automation" / "flow.mjs"
    if not path.is_file():
        pytest.skip("the video tools are not in this checkout")
    # The skip reason of tidiedLanguages itself: flow.mjs has a second sentence with the same
    # opening (the refusal of a retry), which the API never reads by its prefix.
    opening = f"`{dub_retry.TIDIED_SKIP_PREFIX}${{day}} 清掉，成片與旁白都不在了"
    assert opening in path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_automation_is_on_only_with_an_enabled_settings_row() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    assert await service._automation_enabled(session) is False, "no settings row yet"
    for enabled in (False, True):
        row = AsyncMock()
        row.enabled = enabled
        session.scalar = AsyncMock(return_value=row)
        assert await service._automation_enabled(session) is enabled


# --- the service, on real rows ---------------------------------------------------------------

CAPTIONS = (
    "1\n00:00:01,000 --> 00:00:03,000\nこんにちは、世界\n\n"
    "2\n00:00:03,500 --> 00:00:05,000\nテスト\n"
)
CAPTION_CHARACTERS = len("こんにちは、世界") + len("テスト")
VIDEO_ID = "dQw4w9WgXcQ"
ROOM = dub_retry.SpeechRoom(configured=True, limit=300_000, used=1_000, available=True)


@pytest.fixture
def work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The worker's work directory, beside the review store. The SQLite fixture has neither the
    media-spend table nor the automation settings, so both reads are stood in for."""
    monkeypatch.setattr(service, "spend_by_slug", AsyncMock(return_value={}))
    monkeypatch.setattr(service, "_automation_enabled", AsyncMock(return_value=True))
    path = tmp_path / "work"
    path.mkdir()
    return path


def _auto(work: Path, status: str = "done", **more: Any) -> None:
    folder = work / SLUG
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "auto.json").write_text(
        json.dumps({"slug": SLUG, "status": status, **more}), encoding="utf-8"
    )


async def _seed(
    site: Site,
    *,
    locales: tuple[str, ...] = ("ja",),
    publish: str | None = "approved",
    youtube: str | None = None,
) -> None:
    """The fixture's project as a finished slides video with dubs chosen, and its upload
    confirmation in the given state (None: the site has none)."""
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format, project.shorts_line = "slides", None
        project.title, project.stage = "AI 模型怎麼挑", "done"
        project.locales = {
            locale: {"metadata": True, "captions": True, "dub": True} for locale in locales
        }
        project.locales_decided_at = datetime.now(UTC)
        project.youtube_video_id = youtube
        await session.commit()
    if publish is None:
        return
    package = await _submit(
        site, ReviewIn(gate="publish", content_sha256="5" * 64, summary="上傳包", payload={})
    )
    if publish == "approved":
        await _decide(site, package.id, "approve", "")
    elif publish == "rejected":
        await _decide(site, package.id, "reject", "標題要改")


def _skipped(
    site: Site,
    *,
    sha: str = "6" * 64,
    reason: str = SKIP,
    locales: tuple[str, ...] = ("ja",),
) -> ReviewIn:
    """A languages batch that gives every locale's dub up, with the captions the dub reads."""
    return ReviewIn(
        gate="languages",
        content_sha256=sha,
        summary="語言：配音跳過",
        payload={
            "locales": {
                locale: {
                    "metadata": "ready",
                    "captions": "ready",
                    "dub": {"status": "skipped", "reason": reason},
                }
                for locale in locales
            }
        },
        files=[
            _file(site, CAPTIONS.encode(), f"captions_{locale}", "text/plain")
            for locale in locales
        ],
    )


def _made(site: Site, *, sha: str = "7" * 64, track: bytes = b"ja track, made again") -> ReviewIn:
    """The batch of a ja dub that was made: the track under its role, as review-push sends it."""
    return ReviewIn(
        gate="languages",
        content_sha256=sha,
        summary="語言：ja 配音",
        payload={
            "locales": {
                "ja": {
                    "metadata": "ready",
                    "captions": "ready",
                    "dub": "ready",
                    "file": "ja.m4a",
                    "format": "m4a",
                    "file_role": "dub_ja",
                    "kept_lines": ["k7p2"],
                }
            }
        },
        files=[
            _file(site, CAPTIONS.encode(), "captions_ja", "text/plain"),
            _file(site, track, "dub_ja", "audio/mp4"),
        ],
    )


async def _ready(site: Site, work: Path) -> None:
    """A video whose ja dub was given up and can be asked for again."""
    await _seed(site)
    await _submit(site, _skipped(site))
    _auto(work)


async def _ask(
    site: Site,
    work: Path,
    *,
    locale: DubLocale = "ja",
    speech: dub_retry.SpeechRoom = ROOM,
) -> ProjectOut:
    async with site.factory() as session:
        return await service.request_dub_retry(
            session, site.store, SLUG, site.owner, locale, work_dir=str(work), speech=speech
        )


async def _report(site: Site, echo: dict[str, Any] | None = None) -> ProjectOut:
    """The worker's report, as PUT /video/reviews/{slug} takes it; the answer is what it reads."""
    async with site.factory() as session:
        return await service.upsert_project(
            session,
            site.store,
            SLUG,
            ProjectIn(title="AI 模型怎麼挑", stage="done", dub_retries=echo),
        )


async def _take(site: Site, request_id: UUID, locale: str = "ja") -> ProjectOut:
    return await _report(site, {locale: {"id": str(request_id), "status": "taken"}})


async def _page(site: Site, work: Path | None = None) -> ProjectOut:
    async with site.factory() as session:
        return await service.project_view(session, SLUG, str(work) if work is not None else None)


async def _project_row(site: Site) -> VideoProject:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        return project


async def _stored(site: Site) -> dict[str, Any]:
    return dict((await _project_row(site)).dub_retries or {})


async def _retry_audits(site: Site) -> list[AdminAuditLog]:
    return [row for row in await _audits(site) if row.action.startswith("video_dub_retry_")]


@pytest.mark.asyncio
async def test_a_skipped_dub_is_asked_again_with_one_audit_row_and_stays_skipped_until_taken(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    long_ago = datetime.now(UTC) - timedelta(days=30)
    async with site.factory() as session:
        row = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert row is not None
        row.last_synced_at = long_ago  # an old video, far down the worker's list
        await session.commit()
    before = await _page(site, work)
    assert (before.languages["ja"]["dub"].state, before.languages["ja"]["dub"].reason) == (
        "skipped",
        SKIP,
    )
    assert before.dub_retries == {} and before.dub_retry_blocked == {}
    assert before.last_synced_at == long_ago

    asked = await _ask(site, work)
    request = asked.dub_retries["ja"]
    assert (request.status, request.open, request.stalled) == ("requested", True, False)
    assert request.replaced_reason == SKIP and request.reason is None
    assert request.taken_at is None and request.finished_at is None
    # Asking touches nothing else: the dub still reads skipped, with its reason, so an older
    # worker sees no part to make and nothing is held for a request nobody may take.
    assert (asked.languages["ja"]["dub"].state, asked.languages["ja"]["dub"].reason) == (
        "skipped",
        SKIP,
    )
    assert asked.dub_retry_blocked == {}
    assert asked.ready_to_upload == before.ready_to_upload
    assert asked.pending == before.pending == 0
    assert asked.worker_state == "done", "read with the work directory, as the page reads it"
    # The worker's list is the newest 200 by this column: the request moves the row to its top.
    assert asked.last_synced_at == request.requested_at > long_ago + timedelta(days=29)

    project = await _project_row(site)
    stored = (project.dub_retries or {})["ja"]
    assert stored == {
        "id": str(request.id),
        "status": "requested",
        "requested_at": stored["requested_at"],
        "requested_by": str(site.owner.id),
        "replaced_reason": SKIP,
        "estimated_characters": CAPTION_CHARACTERS,
        "taken_at": None,
        "finished_at": None,
        "reason": None,
    }
    assert datetime.fromisoformat(stored["requested_at"]) == request.requested_at
    audits = await _retry_audits(site)
    assert [row.action for row in audits] == ["video_dub_retry_requested"]
    assert audits[0].actor_user_id == site.owner.id
    assert audits[0].target == f"video_project:{project.id}"
    assert audits[0].metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(request.id),
        "replaced_reason": SKIP,
        "estimated_characters": CAPTION_CHARACTERS,
        "speech_used": 1_000,
        "speech_limit": 300_000,
        "previous": None,
    }


@pytest.mark.asyncio
async def test_a_second_click_returns_the_open_request_without_another_audit_row(
    site: Site, work: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _ready(site, work)
    first = await _ask(site, work)
    # Whatever would refuse a new request no longer matters: the open one is simply shown.
    monkeypatch.setattr(service, "_automation_enabled", AsyncMock(return_value=False))
    empty = dub_retry.SpeechRoom(configured=False, limit=10, used=None, available=False)
    second = await _ask(site, work, speech=empty)
    assert second.dub_retries["ja"].id == first.dub_retries["ja"].id
    assert second.dub_retries["ja"].requested_at == first.dub_retries["ja"].requested_at
    assert (await _stored(site))["ja"]["id"] == str(first.dub_retries["ja"].id)
    assert [row.action for row in await _retry_audits(site)] == ["video_dub_retry_requested"]
    # A taken request is as open as a waiting one.
    await _take(site, first.dub_retries["ja"].id)
    third = await _ask(site, work, speech=empty)
    assert (third.dub_retries["ja"].id, third.dub_retries["ja"].status) == (
        first.dub_retries["ja"].id,
        "taken",
    )
    assert [row.action for row in await _retry_audits(site)] == [
        "video_dub_retry_requested",
        "video_dub_retry_taken",
    ]


@pytest.mark.asyncio
async def test_a_dub_that_is_not_skipped_or_not_chosen_is_refused(
    site: Site, work: Path
) -> None:
    async def refused(locale: DubLocale = "ja") -> AppError:
        with pytest.raises(AppError) as error:
            await _ask(site, work, locale=locale)
        return error.value

    await _seed(site)
    _auto(work)
    # No batch yet: the dub is still in the making.
    assert (await _page(site, work)).languages["ja"]["dub"].state == "working"
    making = await refused()
    assert (making.status, making.code, making.detail) == (
        409,
        "video_dub_retry_not_skipped",
        "只有跳過的配音可以再做一次",
    )
    await _submit(site, _skipped(site))
    not_chosen = await refused("ko")
    assert (not_chosen.status, not_chosen.code) == (409, "video_dub_retry_not_skipped")
    # A track that was made is not skipped either.
    await _submit(site, _made(site))
    assert (await _page(site, work)).languages["ja"]["dub"].state == "ready"
    assert (await refused()).code == "video_dub_retry_not_skipped"
    assert (await _page(site, work)).dub_retry_blocked == {}, "nothing to explain on a made dub"

    # A Short has no language panel, whatever its row holds; a dropped video takes nothing.
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        for review in await session.scalars(select(VideoReview)):
            if review.gate == "languages" and review.status == "pending":
                review.status = "superseded"
        project.shorts_line = "lab"
        await session.commit()
    short = await _page(site, work)
    assert short.languages["ja"]["dub"].state == "skipped"
    assert short.dub_retries == {} and short.dub_retry_blocked == {}
    assert (await refused()).code == "video_dub_retry_not_skipped"
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.shorts_line, project.dropped_at = None, datetime.now(UTC)
        await session.commit()
    dropped = await refused()
    assert (dropped.status, dropped.code) == (409, "video_project_dropped")
    async with site.factory() as session:
        with pytest.raises(AppError) as missing:
            await service.request_dub_retry(
                session, site.store, "no-such-video", site.owner, "ja", work_dir=None, speech=ROOM
            )
    assert (missing.value.status, missing.value.code) == (404, "video_project_not_found")
    assert await _stored(site) == {} and await _retry_audits(site) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("case", "blocked", "refusal", "says"),
    [
        ("tidied", "tidied", "video_dub_retry_tidied", "工作檔已經清掉（2026-10-08）"),
        ("publish_waiting", "publish_pending", "video_dub_retry_publish_pending", "上架確認"),
        ("youtube_rejected", "publish_pending", "video_dub_retry_publish_pending", "上架確認"),
        ("youtube_unconfirmed", "publish_pending", "video_dub_retry_publish_pending", "上架確認"),
        ("not_adopted", "not_adopted", "video_dub_retry_worker_absent", "不在工人的工作區"),
        ("blocked", "blocked", "video_dub_retry_video_blocked", "重試這支影片"),
        ("stop_file", "stopped", "video_dub_retry_worker_stopped", "STOP"),
        ("unreadable_mount", None, None, None),
    ],
)
async def test_each_blocker_refuses_with_its_own_code(
    site: Site,
    work: Path,
    case: str,
    blocked: str | None,
    refusal: str | None,
    says: str | None,
) -> None:
    publish = {"publish_waiting": "pending", "youtube_unconfirmed": None}.get(case, "approved")
    await _seed(site, publish=publish, youtube=VIDEO_ID if case.startswith("youtube") else None)
    if case == "youtube_rejected":
        # An older confirmation is approved; the newest one was sent back.
        newer = await _submit(
            site, ReviewIn(gate="publish", content_sha256="4" * 64, summary="新上傳包", payload={})
        )
        await _decide(site, newer.id, "reject", "標題要改")
    await _submit(site, _skipped(site))
    mount = work
    if case == "tidied":
        _auto(work, tidied_at=TIDIED_AT)
    elif case == "blocked":
        _auto(work, "blocked")
    elif case == "unreadable_mount":
        mount = work / "absent"
    elif case != "not_adopted":
        _auto(work)
    if case == "stop_file":
        (work / "STOP").touch()

    # What the page reads before any click: the reason in place of the button.
    before = await _page(site, mount)
    assert before.languages["ja"]["dub"].state == "skipped"
    assert before.dub_retry_blocked == ({"ja": blocked} if blocked else {})
    if refusal is None:
        asked = await _ask(site, mount)
        assert asked.dub_retries["ja"].open and asked.dub_retry_blocked == {}
        assert asked.worker_state == "unavailable", "a mount the API cannot read proves nothing"
        assert (await _page(site, mount)).dub_retry_blocked == {}, "and again once it is open"
        return
    with pytest.raises(AppError) as error:
        await _ask(site, mount)
    assert (error.value.status, error.value.code) == (409, refusal)
    assert says is not None and says in error.value.detail
    assert await _stored(site) == {} and await _retry_audits(site) == []
    assert (await _page(site, mount)).dub_retry_blocked == {"ja": blocked}


@pytest.mark.asyncio
async def test_the_narration_s_own_language_and_a_tidied_skip_are_told_from_the_reason(
    site: Site, work: Path
) -> None:
    """Two skips no retry can fix are known from the batch alone, also without a readable
    work directory: the narration's language, and a part ticked after the files were cleared."""
    await _seed(site, locales=("en", "ja"))
    batch = _skipped(site, locales=("en", "ja"))
    batch.payload["locales"]["en"]["dub"]["reason"] = dub_retry.NARRATION_DUB_SKIP
    batch.payload["locales"]["ja"]["dub"]["reason"] = TIDIED_SKIP
    await _submit(site, batch)
    page = await _page(site)
    assert page.worker_state == "unavailable"
    assert page.dub_retry_blocked == {"en": "narration", "ja": "tidied"}
    with pytest.raises(AppError) as narration:
        await _ask(site, work / "absent", locale="en")
    assert (narration.value.status, narration.value.code, narration.value.detail) == (
        409,
        "video_dub_retry_narration",
        "這個語言就是影片原本的旁白，沒有另一條配音可做",
    )
    with pytest.raises(AppError) as cleared:
        await _ask(site, work / "absent", locale="ja")
    assert (cleared.value.status, cleared.value.code, cleared.value.detail) == (
        409,
        "video_dub_retry_tidied",
        "這支影片的工作檔已經清掉，成片與配音的錄音都不在了，這裡沒辦法再做一次",
    )


@pytest.mark.asyncio
async def test_automation_off_is_refused(
    site: Site, work: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _ready(site, work)
    monkeypatch.setattr(service, "_automation_enabled", AsyncMock(return_value=False))
    with pytest.raises(AppError) as off:
        await _ask(site, work)
    assert (off.value.status, off.value.code, off.value.detail) == (
        409,
        "video_automation_disabled",
        "影片自動化還沒開啟：先在影片審核的設定分頁打開「自動產生草稿」",
    )
    assert await _stored(site) == {} and await _retry_audits(site) == []
    # Being off is not a property of the video, so the cell keeps its button.
    assert (await _page(site, work)).dub_retry_blocked == {}


@pytest.mark.asyncio
async def test_the_speech_month_is_checked_before_the_request_is_taken(
    site: Site, work: Path
) -> None:
    await _ready(site, work)

    async def refused(speech: dub_retry.SpeechRoom) -> AppError:
        with pytest.raises(AppError) as error:
            await _ask(site, work, speech=speech)
        assert await _stored(site) == {} and await _retry_audits(site) == []
        return error.value

    short = await refused(
        dub_retry.SpeechRoom(configured=True, limit=5_000, used=4_995, available=True)
    )
    assert (short.status, short.code) == (429, "video_speech_budget_exhausted")
    assert short.detail == (
        "本月的 Gemini 語音字數預算（5000 字）只剩 5 字，"
        f"不夠再做一條配音（約 {CAPTION_CHARACTERS} 字）；"
        "可調高 VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT，或等下個月"
    )
    over = await refused(
        dub_retry.SpeechRoom(configured=True, limit=5_000, used=9_000, available=True)
    )
    assert "只剩 0 字" in over.detail, "a month already over its limit has nothing left, not less"
    for meter in (
        dub_retry.SpeechRoom(configured=True, limit=5_000, used=None, available=False),
        dub_retry.SpeechRoom(configured=True, limit=5_000, used=None, available=True),
        dub_retry.SpeechRoom(configured=True, limit=5_000, used=100, available=False),
    ):
        away = await refused(meter)
        assert (away.status, away.code, away.detail) == (
            503,
            "video_speech_meter_unavailable",
            "讀不到本月的語音用量，先不接受這個要求；稍後再試",
        )
    no_key = await refused(
        dub_retry.SpeechRoom(configured=False, limit=0, used=0, available=True)
    )
    assert (no_key.status, no_key.code) == (503, "video_speech_not_configured")
    assert no_key.detail == "網站的 Gemini 金鑰還沒設定：請在「AI 設定 → API 金鑰」填 Gemini 金鑰"

    # Exactly enough room is room; and without a caption file to read, a whole track is assumed.
    exact = dub_retry.SpeechRoom(
        configured=True, limit=5_000, used=5_000 - CAPTION_CHARACTERS, available=True
    )
    captions = dub_retry.caption_sha(await _rows(site), "ja")
    assert captions is not None
    path = site.store.path(SLUG, captions)
    assert path is not None
    path.unlink()
    unread = await refused(exact)
    assert unread.code == "video_speech_budget_exhausted" and "約 10000 字" in unread.detail
    path.write_bytes(b"\xff\xfe not text")
    assert "約 10000 字" in (await refused(exact)).detail, "an unreadable file is no file"
    path.write_bytes(CAPTIONS.encode())
    taken = await _ask(site, work, speech=exact)
    first = taken.dub_retries["ja"]
    assert first.open
    assert (await _stored(site))["ja"]["estimated_characters"] == CAPTION_CHARACTERS
    audit = (await _retry_audits(site))[0].metadata_json
    assert (audit["speech_used"], audit["speech_limit"]) == (5_000 - CAPTION_CHARACTERS, 5_000)

    # A limit of 0 counts without blocking: the request is taken without a meter to read.
    await _report(site, {"ja": {"id": str(first.id), "status": "refused", "reason": "先不做"}})
    unlimited = dub_retry.SpeechRoom(configured=True, limit=0, used=None, available=False)
    again = await _ask(site, work, speech=unlimited)
    assert again.dub_retries["ja"].id != first.id and again.dub_retries["ja"].open
    audit = (await _retry_audits(site))[-1].metadata_json
    assert (audit["speech_used"], audit["speech_limit"]) == (None, 0)
    assert audit["previous"] == {"id": str(first.id), "status": "refused"}


@pytest.mark.asyncio
async def test_the_worker_s_report_takes_the_request_and_the_dub_reads_working(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    request = (await _ask(site, work)).dub_retries["ja"]
    # A report without the key, or one that names another request, takes nothing.
    assert (await _report(site)).dub_retries["ja"].status == "requested"
    other = await _take(site, uuid4())
    assert other.dub_retries["ja"].status == "requested"
    assert other.languages["ja"]["dub"].state == "skipped"

    # The answer to the echo is the compare-and-set: the worker reads its own take in it.
    answer = await _take(site, request.id)
    taken = answer.dub_retries["ja"]
    assert (taken.id, taken.status, taken.open, taken.stalled) == (
        request.id,
        "taken",
        True,
        False,
    )
    assert taken.taken_at is not None and taken.taken_at >= taken.requested_at
    assert taken.replaced_reason == SKIP
    assert (answer.languages["ja"]["dub"].state, answer.languages["ja"]["dub"].reason) == (
        "working",
        None,
    )
    assert answer.languages["ja"]["captions"].state == "ready", "only the dub is in the making"
    assert answer.dub_retry_blocked == {}
    project = await _project_row(site)
    audits = await _retry_audits(site)
    assert [row.action for row in audits] == ["video_dub_retry_requested", "video_dub_retry_taken"]
    assert audits[1].actor_user_id is None
    assert audits[1].target == f"video_project:{project.id}"
    assert audits[1].metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(request.id),
    }
    # The same echo again, as after a lost answer, is a no-op with the same answer.
    again = await _take(site, request.id)
    assert again.dub_retries["ja"].taken_at == taken.taken_at
    assert len(await _retry_audits(site)) == 2


@pytest.mark.asyncio
async def test_a_request_past_its_day_is_not_taken_and_the_next_click_replaces_it(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    request = (await _ask(site, work)).dub_retries["ja"]
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        aged = datetime.now(UTC) - timedelta(hours=25)
        project.dub_retries = {
            "ja": {**project.dub_retries["ja"], "requested_at": aged.isoformat()}
        }
        await session.commit()
    answer = await _take(site, request.id)
    expired = answer.dub_retries["ja"]
    assert (expired.id, expired.status, expired.open) == (request.id, "expired", False)
    assert answer.languages["ja"]["dub"].state == "skipped", "the worker starts nothing"
    assert (await _stored(site))["ja"]["status"] == "requested", "expiry is never stored"
    # The button is back, and the new request records what it replaced.
    renewed = (await _ask(site, work)).dub_retries["ja"]
    assert renewed.id != request.id and (renewed.status, renewed.open) == ("requested", True)
    audits = await _retry_audits(site)
    assert [row.action for row in audits] == ["video_dub_retry_requested"] * 2
    assert audits[1].metadata_json["previous"] == {"id": str(request.id), "status": "expired"}


@pytest.mark.asyncio
async def test_an_identical_batch_still_closes_a_taken_request_as_skipped(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    first = (await _rows(site))[-1]
    assert (first.gate, first.status) == ("languages", "approved")
    request = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, request.id)
    count = len(await _rows(site))
    # The retry gave up for the same reason and nothing else changed: the same bytes, so the
    # site answers with the approved review and adds none. The request must still end.
    answer = await _submit(site, _skipped(site))
    assert (answer.id, answer.status) == (first.id, "approved")
    assert len(await _rows(site)) == count
    stored = (await _stored(site))["ja"]
    assert (stored["status"], stored["reason"]) == ("skipped", SKIP)
    assert stored["finished_at"] is not None and stored["taken_at"] is not None
    page = await _page(site, work)
    closed = page.dub_retries["ja"]
    assert (closed.id, closed.status, closed.open, closed.reason) == (
        request.id,
        "skipped",
        False,
        SKIP,
    )
    assert (page.languages["ja"]["dub"].state, page.languages["ja"]["dub"].reason) == (
        "skipped",
        SKIP,
    )
    assert page.dub_retry_blocked == {} and page.pending == 0
    last = (await _retry_audits(site))[-1]
    assert (last.action, last.actor_user_id) == ("video_dub_retry_finished", None)
    assert last.metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(request.id),
        "outcome": "skipped",
        "reason": SKIP,
        "via": "batch",
    }
    # The same batch once more finds nothing open.
    await _submit(site, _skipped(site))
    assert len(await _retry_audits(site)) == 3


@pytest.mark.asyncio
async def test_a_batch_that_restates_the_old_skip_leaves_a_request_nobody_took(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    request = (await _ask(site, work)).dub_retries["ja"]
    await _submit(site, _skipped(site))
    assert (await _page(site, work)).dub_retries["ja"].status == "requested"
    # A changed reason is a new batch, approved on arrival; it is still the old skip.
    renewed = await _submit(site, _skipped(site, sha="8" * 64, reason=AGAIN))
    assert renewed.status == "approved"
    page = await _page(site, work)
    assert (page.dub_retries["ja"].id, page.dub_retries["ja"].status) == (request.id, "requested")
    assert page.languages["ja"]["dub"].reason == AGAIN
    assert [row.action for row in await _retry_audits(site)] == ["video_dub_retry_requested"]


@pytest.mark.asyncio
async def test_a_batch_identical_to_one_the_owner_sent_back_ends_the_request_as_refused_without_a_card(  # noqa: E501
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    first = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, first.id)
    card = await _submit(site, _made(site))
    assert card.status == "pending"
    assert (await _stored(site))["ja"]["status"] == "made"
    # The owner sends the card back: the batch counts for nothing, so the dub reads skipped
    # again with the earlier reason, while the request stays as it ended.
    await _decide(site, card.id, "reject", "聽起來不對")
    back = await _page(site, work)
    assert (back.languages["ja"]["dub"].state, back.languages["ja"]["dub"].reason) == (
        "skipped",
        SKIP,
    )
    assert (back.dub_retries["ja"].id, back.dub_retries["ja"].status) == (first.id, "made")
    assert back.dub_retry_blocked == {}, "the button is offered again"

    second = (await _ask(site, work)).dub_retries["ja"]
    assert second.id != first.id and second.status == "requested"
    await _take(site, second.id)
    count = len(await _rows(site))
    # Re-made from the cached takes: the same bytes. The site answers with the sent-back review.
    answer = await _submit(site, _made(site))
    assert (answer.id, answer.status) == (card.id, "rejected")
    assert len(await _rows(site)) == count, "no card is added"
    page = await _page(site, work)
    ended = page.dub_retries["ja"]
    assert (ended.id, ended.status, ended.open, ended.reason) == (
        second.id,
        "refused",
        False,
        dub_retry.SAME_AS_SENT_BACK,
    )
    assert (page.languages["ja"]["dub"].state, page.languages["ja"]["dub"].reason) == (
        "skipped",
        SKIP,
    )
    assert page.pending == 0
    last = (await _retry_audits(site))[-1]
    assert last.action == "video_dub_retry_finished" and last.actor_user_id is None
    assert last.metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(second.id),
        "outcome": "refused",
        "reason": dub_retry.SAME_AS_SENT_BACK,
        "via": "batch",
    }
    # Other bytes (the rules or the translation changed) are a new card and a made track.
    third = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, third.id)
    fresh = await _submit(site, _made(site, sha="9" * 64, track=b"ja track, other takes"))
    assert fresh.status == "pending" and fresh.id != card.id
    assert (await _page(site, work)).dub_retries["ja"].status == "made"


@pytest.mark.asyncio
async def test_a_made_track_sent_back_after_a_card_that_still_waited_leaves_no_batch_that_counts(
    site: Site, work: Path
) -> None:
    """Asked while the first languages card still waits (another language's track nobody has
    confirmed), the re-made batch replaces that card. Sent back, no batch counts any more:
    every part reads "working", the request stays as it ended, and the click is refused, so
    the page says so in a line of its own instead of the skip reason and the button."""
    await _seed(site, locales=("en", "ja"))
    _auto(work)
    en_track = _file(site, b"en track", "dub_en", "audio/mp4")
    waiting = await _submit(
        site,
        ReviewIn(
            gate="languages",
            content_sha256="a" * 64,
            summary="語言：en 配音，ja 跳過",
            payload={
                "locales": {
                    "en": {"metadata": "ready", "captions": "ready", "dub": "ready"},
                    "ja": {
                        "metadata": "ready",
                        "captions": "ready",
                        "dub": {"status": "skipped", "reason": SKIP},
                    },
                }
            },
            files=[en_track],
        ),
    )
    assert waiting.status == "pending", "the en track waits for the owner"
    request = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, request.id)
    card = await _submit(
        site,
        ReviewIn(
            gate="languages",
            content_sha256="b" * 64,
            summary="語言：en、ja 配音",
            payload={
                "locales": {
                    "en": {"metadata": "ready", "captions": "ready", "dub": "ready"},
                    "ja": {"metadata": "ready", "captions": "ready", "dub": "ready"},
                }
            },
            files=[en_track, _file(site, b"ja track", "dub_ja", "audio/mp4")],
        ),
    )
    statuses = {row.id: row.status for row in await _rows(site) if row.gate == "languages"}
    assert statuses == {waiting.id: "superseded", card.id: "pending"}
    made = await _page(site, work)
    assert made.dub_retries["ja"].status == "made"
    assert made.languages["en"]["dub"].state == "ready", "nobody confirmed the en track"
    assert made.languages["ja"]["dub"].state == "ready"

    await _decide(site, card.id, "reject", "聽起來不對")
    back = await _page(site, work)
    assert {
        (locale, part): state.state
        for locale, parts in back.languages.items()
        for part, state in parts.items()
    } == {
        (locale, part): "working"
        for locale in ("en", "ja")
        for part in ("metadata", "captions", "dub")
    }
    ended = back.dub_retries["ja"]
    assert (ended.id, ended.status, ended.open) == (request.id, "made", False)
    assert back.dub_retry_blocked == {}, "a blocker is named only for a skipped dub"
    with pytest.raises(AppError) as error:
        await _ask(site, work)
    assert (error.value.status, error.value.code) == (409, "video_dub_retry_not_skipped")
    assert (await _stored(site))["ja"]["id"] == str(request.id)


@pytest.mark.asyncio
async def test_a_stored_value_that_is_not_an_object_reads_as_no_request_at_the_click(
    site: Site, work: Path
) -> None:
    """No writer stores anything but an object; a row repaired by hand may hold something else.
    Every reader takes that as no request, and so does the click, which then writes a clean
    object over it."""
    await _ready(site, work)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.dub_retries = cast(Any, ["ja"])
        await session.commit()
    before = await _page(site, work)
    assert before.dub_retries == {} and before.languages["ja"]["dub"].state == "skipped"
    asked = await _ask(site, work)
    assert asked.dub_retries["ja"].status == "requested"
    stored = (await _project_row(site)).dub_retries
    assert isinstance(stored, dict) and list(stored) == ["ja"]


@pytest.mark.asyncio
async def test_a_batch_with_the_track_closes_the_request_as_made_and_waits_for_the_owner(
    site: Site, work: Path
) -> None:
    await _ready(site, work)
    request = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, request.id)
    assert (await _page(site, work)).languages["ja"]["dub"].state == "working"
    card = await _submit(site, _made(site))
    assert card.status == "pending", "a track waits for the owner to upload it in Studio"
    assert card.payload["locales"]["ja"]["kept_lines"] == ["k7p2"], "the card reads it from here"
    page = await _page(site, work)
    made = page.dub_retries["ja"]
    assert (made.id, made.status, made.open, made.reason) == (request.id, "made", False, None)
    assert made.finished_at is not None and made.replaced_reason == SKIP
    assert (page.languages["ja"]["dub"].state, page.pending) == ("ready", 1)
    last = (await _retry_audits(site))[-1]
    assert last.metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(request.id),
        "outcome": "made",
        "reason": None,
        "via": "batch",
    }
    # The same batch sent again while it waits replaces it in place and closes nothing twice.
    await _submit(site, _made(site))
    assert len(await _retry_audits(site)) == 3
    await _decide(site, card.id, "approve", "已在 Studio 上傳")
    done = await _page(site, work)
    assert done.languages["ja"]["dub"].state == "uploaded"
    assert done.dub_retries["ja"].status == "made"


@pytest.mark.asyncio
async def test_a_confirmed_track_stays_uploaded_when_a_pending_batch_restates_the_same_file(
    site: Site, work: Path
) -> None:
    await _seed(site, locales=("en", "ja"))
    _auto(work)

    def batch(sha: str, english: bytes, japanese: bytes | None) -> ReviewIn:
        en_track = _file(site, english, "dub_en", "audio/mp4")
        entries: dict[str, Any] = {
            "en": {"metadata": "ready", "captions": "ready", "dub": "ready", "file_role": "dub_en"}
        }
        files = [en_track]
        if japanese is None:
            entries["ja"] = {
                "metadata": "ready",
                "captions": "ready",
                "dub": {"status": "skipped", "reason": SKIP},
            }
        else:
            # No file_role on this entry: the role review-push gives a dub is assumed.
            entries["ja"] = {"metadata": "ready", "captions": "ready", "dub": "ready"}
            files.append(_file(site, japanese, "dub_ja", "audio/mp4"))
        return ReviewIn(
            gate="languages",
            content_sha256=sha,
            summary="語言：en、ja",
            payload={"locales": entries},
            files=files,
        )

    first = await _submit(site, batch("a" * 64, b"en track", None))
    await _decide(site, first.id, "approve", "已在 Studio 上傳")
    page = await _page(site, work)
    assert page.languages["en"]["dub"].state == "uploaded"
    assert page.languages["ja"]["dub"].state == "skipped"

    # The ja dub is made again: the batch lists the en track again, the same file.
    request = (await _ask(site, work)).dub_retries["ja"]
    await _take(site, request.id)
    second = await _submit(site, batch("b" * 64, b"en track", b"ja track"))
    assert second.status == "pending"
    page = await _page(site, work)
    assert page.languages["en"]["dub"].state == "uploaded", "nothing of en is new"
    assert page.languages["ja"]["dub"].state == "ready", "only this track is new"
    assert page.dub_retries["ja"].status == "made" and page.pending == 1
    async with site.factory() as session:
        listed = await service.list_projects(session, shorts="exclude", work_dir=str(work))
    assert listed[0].languages["en"]["dub"].state == "uploaded", "the list reads the same"
    assert listed[0].languages["ja"]["dub"].state == "ready"

    # A pending batch whose en file differs carries a track the owner has not confirmed.
    third = await _submit(site, batch("c" * 64, b"en track, made again", b"ja track"))
    assert third.status == "pending"
    page = await _page(site, work)
    assert page.languages["en"]["dub"].state == "ready"
    assert page.languages["ja"]["dub"].state == "ready"
    # The site still waits for the owner on a batch that carries a track.
    assert service.languages_need_owner(third.payload)


@pytest.mark.asyncio
async def test_the_worker_s_refusal_is_recorded_with_its_reason(site: Site, work: Path) -> None:
    await _ready(site, work)
    request = (await _ask(site, work)).dub_retries["ja"]
    reason = (
        "成片不在了，或它的檢查記錄比現在的腳本和畫面舊，"
        "上傳包寫不出來，做了配音也送不出語言審核；這條配音先不做"
    )
    answer = await _report(
        site, {"ja": {"id": str(request.id), "status": "refused", "reason": reason}}
    )
    refused = answer.dub_retries["ja"]
    assert (refused.id, refused.status, refused.open, refused.reason) == (
        request.id,
        "refused",
        False,
        reason,
    )
    assert refused.finished_at is not None and refused.taken_at is None
    assert answer.languages["ja"]["dub"].state == "skipped", "nothing was cleared or bought"
    last = (await _retry_audits(site))[-1]
    assert (last.action, last.actor_user_id) == ("video_dub_retry_finished", None)
    assert last.metadata_json == {
        "slug": SLUG,
        "locale": "ja",
        "request_id": str(request.id),
        "outcome": "refused",
        "reason": reason,
        "via": "report",
    }
    # The first ending stands: a late "taken" for the same request starts nothing.
    late = await _take(site, request.id)
    assert late.dub_retries["ja"].status == "refused"
    assert late.languages["ja"]["dub"].state == "skipped"
    assert len(await _retry_audits(site)) == 2
    assert (await _page(site, work)).dub_retry_blocked == {}, "the button is offered again"

    # A request the worker had taken can be refused too (the files were cleared meanwhile):
    # the dub stops reading "working".
    second = (await _ask(site, work)).dub_retries["ja"]
    assert (await _take(site, second.id)).languages["ja"]["dub"].state == "working"
    gone = await _report(
        site, {"ja": {"id": str(second.id), "status": "refused", "reason": "成" * 600}}
    )
    assert gone.dub_retries["ja"].status == "refused"
    assert gone.dub_retries["ja"].reason == "成" * 500
    assert gone.dub_retries["ja"].taken_at is not None
    assert gone.languages["ja"]["dub"].state == "skipped"
    audit = (await _retry_audits(site))[-1].metadata_json
    assert (audit["outcome"], audit["via"], audit["reason"]) == ("refused", "report", "成" * 500)
    assert len(await _retry_audits(site)) == 5


@pytest.mark.asyncio
async def test_saving_the_languages_without_the_dub_withdraws_a_requested_retry_and_keeps_a_taken_one(  # noqa: E501
    site: Site, work: Path
) -> None:
    await _seed(site, locales=("en", "ja"))
    await _submit(site, _skipped(site, locales=("en", "ja")))
    _auto(work)
    waiting = (await _ask(site, work, locale="en")).dub_retries["en"]
    taken = (await _ask(site, work, locale="ja")).dub_retries["ja"]
    await _take(site, taken.id)

    async def save(choice: dict[str, Any]) -> ProjectOut:
        async with site.factory() as session:
            return await service.set_locales(
                session, SLUG, site.owner, LocalesIn.model_validate({"locales": choice})
            )

    async def last_save() -> dict[str, Any]:
        rows = [row for row in await _audits(site) if row.action == "video_locales_set"]
        return rows[-1].metadata_json

    without = {"metadata": True, "captions": True, "dub": False}
    with_dub = {"metadata": True, "captions": True, "dub": True}
    saved = await save({"en": without, "ja": without})
    assert saved.dub_retries == {}, "the taken one is hidden while its dub is not chosen"
    assert "dub" not in saved.languages["ja"] and "dub" not in saved.languages["en"]
    stored = await _stored(site)
    assert list(stored) == ["ja"] and stored["ja"]["status"] == "taken"
    assert stored["ja"]["id"] == str(taken.id)
    assert str(waiting.id) not in json.dumps(stored), "the waiting one went with its dub"
    assert (await last_save())["dub_retries_withdrawn"] == ["en"]

    # Ticked again, the taken request goes on; the withdrawn one is simply gone.
    back = await save({"en": with_dub, "ja": with_dub})
    assert list(back.dub_retries) == ["ja"]
    assert (back.dub_retries["ja"].id, back.dub_retries["ja"].status) == (taken.id, "taken")
    assert back.languages["ja"]["dub"].state == "working"
    assert back.languages["en"]["dub"].state == "skipped"
    assert "dub_retries_withdrawn" not in await last_save(), "this save withdrew nothing"
    actions = [row.action for row in await _retry_audits(site)]
    assert actions == [
        "video_dub_retry_requested",
        "video_dub_retry_requested",
        "video_dub_retry_taken",
    ], "a withdrawal is on the save's own audit row"

    # The older page's dub checkboxes go through the same record.
    async with site.factory() as session:
        en_again = await service.request_dub_retry(
            session, site.store, SLUG, site.owner, "en", work_dir=str(work), speech=ROOM
        )
    assert en_again.dub_retries["en"].status == "requested"
    async with site.factory() as session:
        older = await service.set_dub_locales(
            session, SLUG, site.owner, DubLocalesIn.model_validate({"locales": ["ja"]})
        )
    assert list(older.dub_retries) == ["ja"]
    assert (await last_save())["dub_retries_withdrawn"] == ["en"]


@pytest.mark.asyncio
async def test_the_tool_s_list_row_carries_the_request(site: Site, work: Path) -> None:
    await _ready(site, work)

    async def row() -> dict[str, Any]:
        # GET /video/automation/videos?shorts=exclude: no work directory on the tool's route.
        async with site.factory() as session:
            listed = await service.list_projects(session, shorts="exclude")
        assert [item.slug for item in listed] == [SLUG]
        return listed[0].model_dump(mode="json")

    before = await row()
    assert before["dub_retries"] == {} and before["dub_retry_blocked"] == {}
    request = (await _ask(site, work)).dub_retries["ja"]
    asked = await row()
    assert asked["dub_retries"]["ja"] == {
        "id": str(request.id),
        "status": "requested",
        "open": True,
        "stalled": False,
        "requested_at": asked["dub_retries"]["ja"]["requested_at"],
        "taken_at": None,
        "finished_at": None,
        "reason": None,
        "replaced_reason": SKIP,
    }
    assert asked["languages"]["ja"]["dub"] == {"state": "skipped", "reason": SKIP}
    assert asked["locales"]["ja"]["dub"] is True
    assert asked["worker_state"] == "unavailable" and asked["dub_retry_blocked"] == {}
    assert asked["ready_to_upload"], "a request nobody took holds nothing back"
    await _take(site, request.id)
    taken = await row()
    assert (taken["dub_retries"]["ja"]["status"], taken["dub_retries"]["ja"]["open"]) == (
        "taken",
        True,
    )
    assert taken["languages"]["ja"]["dub"] == {"state": "working", "reason": None}
    assert not taken["ready_to_upload"]
    await _submit(site, _skipped(site, sha="8" * 64, reason=AGAIN))
    closed = await row()
    assert (closed["dub_retries"]["ja"]["status"], closed["dub_retries"]["ja"]["open"]) == (
        "skipped",
        False,
    )
    assert closed["dub_retries"]["ja"]["reason"] == AGAIN
    assert closed["languages"]["ja"]["dub"] == {"state": "skipped", "reason": AGAIN}
    # The admin list reads the work directory, and keeps the approximation for the upload
    # confirmation: it shows no panel, so only the page computes the producer's rule.
    _auto(work, tidied_at=TIDIED_AT)
    async with site.factory() as session:
        admin = await service.list_projects(session, work_dir=str(work))
        browsed = await service.browse_projects(session, work_dir=str(work))
    assert admin[0].dub_retry_blocked == {"ja": "tidied"}
    assert browsed.items[0].dub_retry_blocked == {"ja": "tidied"}
