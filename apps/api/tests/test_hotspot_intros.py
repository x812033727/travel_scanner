"""First-party introductions: the draft seam, the reader's view and the review queue.

The rule these tests exist for is the one that costs a person's work if it breaks:
a generated draft must never quietly overwrite a paragraph an administrator already
approved.
"""

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from uuid import UUID, uuid4

import pytest

from app.hotspots.admin_router import (
    IntroReviewRequest,
    IntroUpdatePayload,
    ManualIntroRequest,
    add_hotspot_intro,
    review_hotspot_intros,
    update_hotspot_intro,
)
from app.hotspots.intros import (
    INTRO_BODY_MAX_CHARS,
    clean_intro_body,
    intro_coverage,
    load_public_intros,
    upsert_hotspot_intro_draft,
)
from app.models import AdminAuditLog, HotspotIntro, TravelHotspot
from app.problems import AppError

USER = SimpleNamespace(id=uuid4())
STAMP = datetime(2026, 9, 7, tzinfo=UTC)


def intro(
    hotspot_id: UUID,
    locale: str,
    *,
    status: str = "approved",
    body: str = "淺草寺是東京最古老的寺院。",
    source: str = "manual",
) -> HotspotIntro:
    row = HotspotIntro(
        hotspot_id=hotspot_id,
        locale=locale,
        body=body,
        review_status=status,
        source=source,
        metadata_json={},
    )
    row.id = uuid4()
    row.created_at = STAMP
    row.updated_at = STAMP
    return row


def _bound(params: dict[str, Any], prefix: str) -> set[Any]:
    """Values bound to parameters whose name starts with ``prefix``.

    An ``IN`` clause compiles to one expanding parameter holding a list, so the
    values have to be flattened before they can go in a set.
    """

    values: set[Any] = set()
    for key, value in params.items():
        if not key.startswith(prefix):
            continue
        if isinstance(value, list | tuple):
            values.update(value)
        else:
            values.add(value)
    return values


class FakeSession:
    """Serves the single-row lookups and the list queries the intro code makes."""

    def __init__(
        self,
        *,
        rows: list[HotspotIntro] | None = None,
        hotspot: TravelHotspot | None = None,
    ) -> None:
        self.rows = rows or []
        self.hotspot = hotspot
        self.added: list[Any] = []
        self.commits = 0

    async def get(self, model: type, key: UUID) -> Any:
        if model is TravelHotspot:
            return self.hotspot if self.hotspot and self.hotspot.id == key else None
        return next((row for row in self.rows if row.id == key), None)

    async def scalar(self, statement: Any) -> Any:
        params = statement.compile().params
        locale = next((v for k, v in params.items() if k.startswith("locale")), None)
        hotspot_id = next((v for k, v in params.items() if k.startswith("hotspot_id")), None)
        return next(
            (row for row in self.rows if row.hotspot_id == hotspot_id and row.locale == locale),
            None,
        )

    async def scalars(self, statement: Any) -> Any:
        params = statement.compile().params
        wanted = _bound(params, "locale")
        statuses = _bound(params, "review_status")
        hotspot_ids = _bound(params, "hotspot_id")
        ids = _bound(params, "id_") | _bound(params, "param")
        rows = [
            row
            for row in self.rows
            if (not wanted or row.locale in wanted)
            and (not statuses or row.review_status in statuses)
            and (not hotspot_ids or row.hotspot_id in hotspot_ids)
            and (not ids or row.id in ids)
        ]
        return SimpleNamespace(all=lambda: rows)

    def add(self, item: Any) -> None:
        self.added.append(item)
        if isinstance(item, HotspotIntro):
            if getattr(item, "id", None) is None:
                item.id = uuid4()
            item.created_at = item.updated_at = STAMP
            self.rows.append(item)

    async def flush(self) -> None:
        return None

    async def commit(self) -> None:
        self.commits += 1


def audit(session: FakeSession) -> AdminAuditLog:
    return next(item for item in session.added if isinstance(item, AdminAuditLog))


def test_body_must_be_present_and_bounded() -> None:
    assert clean_intro_body("  一段介紹  ") == "一段介紹"
    with pytest.raises(AppError) as empty:
        clean_intro_body("   ")
    assert empty.value.code == "hotspot_intro_body_required"
    with pytest.raises(AppError):
        clean_intro_body("字" * (INTRO_BODY_MAX_CHARS + 1))


@pytest.mark.asyncio
async def test_a_draft_lands_as_pending_for_review() -> None:
    hotspot_id = uuid4()
    session = FakeSession()

    row, written = await upsert_hotspot_intro_draft(
        session,  # type: ignore[arg-type]
        hotspot_id=hotspot_id,
        locale="zh-TW",
        body="  雷門前總是排著隊。  ",
        source="ai",
        ai_provider="gemini",
        ai_model="gemini-3.8-flash",
        metadata={"run_id": "abc"},
    )

    assert written is True
    assert row.review_status == "pending"
    assert row.body == "雷門前總是排著隊。"
    assert (row.ai_provider, row.ai_model) == ("gemini", "gemini-3.8-flash")
    assert row.generated_at is not None
    assert row.metadata_json["run_id"] == "abc"


@pytest.mark.asyncio
async def test_a_draft_never_silently_replaces_an_approved_paragraph() -> None:
    """The whole point of the review queue: somebody said yes to that text."""
    hotspot_id = uuid4()
    approved = intro(hotspot_id, "zh-TW", status="approved", body="人工審核過的介紹。")
    session = FakeSession(rows=[approved])

    row, written = await upsert_hotspot_intro_draft(
        session,  # type: ignore[arg-type]
        hotspot_id=hotspot_id,
        locale="zh-TW",
        body="AI 又寫了一段。",
        source="ai",
    )

    assert written is False
    assert row.body == "人工審核過的介紹。"
    assert row.review_status == "approved"


@pytest.mark.asyncio
async def test_replacing_an_approved_paragraph_keeps_the_old_text() -> None:
    hotspot_id = uuid4()
    approved = intro(hotspot_id, "zh-TW", status="approved", body="舊的介紹。")
    session = FakeSession(rows=[approved])

    row, written = await upsert_hotspot_intro_draft(
        session,  # type: ignore[arg-type]
        hotspot_id=hotspot_id,
        locale="zh-TW",
        body="新的介紹。",
        source="ai",
        replace_approved=True,
    )

    assert written is True
    assert row.body == "新的介紹。"
    # Back to pending: a replacement has not been reviewed either.
    assert row.review_status == "pending"
    assert row.metadata_json["previous_body"] == "舊的介紹。"


@pytest.mark.asyncio
async def test_a_rejected_draft_is_replaced_and_looked_at_again() -> None:
    hotspot_id = uuid4()
    rejected = intro(hotspot_id, "ja", status="rejected", body="没", source="ai")
    rejected.review_reason = "内容が薄い"
    session = FakeSession(rows=[rejected])

    row, written = await upsert_hotspot_intro_draft(
        session,  # type: ignore[arg-type]
        hotspot_id=hotspot_id,
        locale="ja",
        body="浅草寺は東京最古の寺です。",
        source="ai",
    )

    assert written is True
    assert row.review_status == "pending"
    assert row.review_reason is None


@pytest.mark.asyncio
async def test_readers_only_see_approved_text_in_their_own_language() -> None:
    first, second = uuid4(), uuid4()
    session = FakeSession(
        rows=[
            intro(first, "zh-TW", status="approved", body="繁體介紹。"),
            intro(first, "ja", status="approved", body="日本語の紹介。"),
            intro(second, "ja", status="pending", body="まだ審査中。"),
        ]
    )

    zh = await load_public_intros(session, [first, second], "zh-TW")  # type: ignore[arg-type]
    assert zh[first]["body"] == "繁體介紹。"
    # Only pending for the second hotspot, so it has nothing to show.
    assert second not in zh

    ja = await load_public_intros(session, [first, second], "ja")  # type: ignore[arg-type]
    assert ja[first]["body"] == "日本語の紹介。"
    assert second not in ja


@pytest.mark.asyncio
async def test_simplified_falls_back_to_traditional_but_english_does_not() -> None:
    hotspot_id = uuid4()
    session = FakeSession(rows=[intro(hotspot_id, "zh-TW", status="approved", body="繁體介紹。")])

    simplified = await load_public_intros(session, [hotspot_id], "zh-CN")  # type: ignore[arg-type]
    assert simplified[hotspot_id]["body"] == "繁體介紹。"
    # The payload says which language the reader is actually getting.
    assert simplified[hotspot_id]["locale"] == "zh-TW"

    english = await load_public_intros(session, [hotspot_id], "en")  # type: ignore[arg-type]
    assert english == {}


@pytest.mark.asyncio
async def test_no_hotspots_asks_the_database_nothing() -> None:
    session = FakeSession(rows=[])
    assert await load_public_intros(session, [], "zh-TW") == {}  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_coverage_lists_every_locale_including_the_missing_ones() -> None:
    hotspot_id = uuid4()
    session = FakeSession(rows=[intro(hotspot_id, "zh-TW", status="approved")])

    coverage = await intro_coverage(session, hotspot_id)  # type: ignore[arg-type]

    assert [item["locale"] for item in coverage] == ["en", "ja", "ko", "zh-TW", "zh-CN"]
    by_locale = {item["locale"]: item for item in coverage}
    assert by_locale["zh-TW"]["status"] == "approved"
    assert by_locale["en"]["status"] is None
    assert by_locale["en"]["body"] is None


@pytest.mark.asyncio
async def test_reviewing_stamps_the_reviewer_and_writes_an_audit_row() -> None:
    hotspot_id = uuid4()
    first = intro(hotspot_id, "zh-TW", status="pending")
    second = intro(hotspot_id, "ja", status="pending")
    session = FakeSession(rows=[first, second])

    result = await review_hotspot_intros(
        IntroReviewRequest(ids=[first.id, second.id], action="approve", reason="讀起來沒問題"),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
    )

    assert result == {"updated": 2, "status": "approved"}
    assert first.review_status == second.review_status == "approved"
    assert first.reviewed_by_user_id == USER.id
    assert first.reviewed_at is not None
    entry = audit(session)
    assert entry.action == "hotspot_intros_reviewed"
    assert entry.metadata_json["action"] == "approve"
    assert session.commits == 1


@pytest.mark.asyncio
async def test_reviewing_an_id_that_does_not_exist_changes_nothing() -> None:
    hotspot_id = uuid4()
    row = intro(hotspot_id, "zh-TW", status="pending")
    session = FakeSession(rows=[row])

    with pytest.raises(AppError) as missing:
        await review_hotspot_intros(
            IntroReviewRequest(ids=[row.id, uuid4()], action="approve"),
            USER,  # type: ignore[arg-type]
            session,  # type: ignore[arg-type]
        )

    assert missing.value.status == 404
    assert missing.value.code == "hotspot_intro_not_found"
    assert row.review_status == "pending"
    assert session.commits == 0


@pytest.mark.asyncio
async def test_editing_the_text_records_who_wrote_it() -> None:
    hotspot_id = uuid4()
    row = intro(hotspot_id, "zh-TW", status="pending", source="ai")
    session = FakeSession(rows=[row])

    await update_hotspot_intro(
        row.id,
        IntroUpdatePayload(body="  管理員改寫過的介紹。  ", review_status="approved"),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
    )

    assert row.body == "管理員改寫過的介紹。"
    assert row.review_status == "approved"
    assert row.metadata_json["edited_by_user_id"] == str(USER.id)
    assert audit(session).action == "hotspot_intro_updated"


@pytest.mark.asyncio
async def test_an_edit_must_actually_change_something() -> None:
    with pytest.raises(ValueError, match="nothing to update"):
        IntroUpdatePayload(reason="只寫理由不算")


@pytest.mark.asyncio
async def test_a_manual_paragraph_is_approved_on_arrival() -> None:
    """An administrator typing the text has already reviewed it."""
    hotspot = TravelHotspot(slug="sensoji", name="淺草寺", category="culture")
    hotspot.id = uuid4()
    session = FakeSession(hotspot=hotspot)

    result = await add_hotspot_intro(
        hotspot.id,
        ManualIntroRequest(locale="zh-TW", body="雷門是淺草的門面。"),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
    )

    assert result["status"] == "approved"
    assert result["source"] == "manual"
    assert result["hotspot_name"] == "淺草寺"
    row = next(item for item in session.added if isinstance(item, HotspotIntro))
    assert row.reviewed_by_user_id == USER.id
    assert row.generated_at is None
    assert audit(session).action == "hotspot_intro_manual_added"


@pytest.mark.asyncio
async def test_a_manual_paragraph_can_be_filed_for_someone_else_to_check() -> None:
    hotspot = TravelHotspot(slug="sensoji", name="淺草寺", category="culture")
    hotspot.id = uuid4()
    session = FakeSession(hotspot=hotspot)

    result = await add_hotspot_intro(
        hotspot.id,
        ManualIntroRequest(locale="ja", body="雷門は浅草の顔です。", approve=False),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
    )

    assert result["status"] == "pending"


@pytest.mark.asyncio
async def test_adding_a_paragraph_to_a_missing_hotspot_is_not_found() -> None:
    session = FakeSession(hotspot=None)

    with pytest.raises(AppError) as missing:
        await add_hotspot_intro(
            uuid4(),
            ManualIntroRequest(locale="zh-TW", body="不會被寫入。"),
            USER,  # type: ignore[arg-type]
            session,  # type: ignore[arg-type]
        )

    assert missing.value.status == 404
    assert missing.value.code == "hotspot_not_found"
    assert session.commits == 0
