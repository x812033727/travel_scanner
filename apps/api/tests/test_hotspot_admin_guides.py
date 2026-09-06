from decimal import Decimal
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from app.config import get_settings
from app.hotspots import admin_router
from app.hotspots.admin_router import ManualGuideRequest, add_manual_guide
from app.hotspots.guides import GuideCandidate
from app.models import HotspotGuide


class FakeSession:
    def __init__(self, hotspot_id: UUID) -> None:
        self.hotspot_id = hotspot_id
        self.added: list[object] = []
        self.flushes = 0
        self.commits = 0

    async def get(self, model: type, key: UUID) -> SimpleNamespace | None:
        return SimpleNamespace(id=key) if key == self.hotspot_id else None

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        self.flushes += 1

    async def commit(self) -> None:
        self.commits += 1


class FakeYouTube:
    def __init__(self, api_key: str, redis: object | None = None) -> None:
        self.api_key = api_key

    async def import_video(self, url: str, locale: str) -> GuideCandidate:
        return GuideCandidate(
            content_type="video",
            provider="youtube",
            locale="ja",
            title="浅草を歩く",
            creator_name="旅チャンネル",
            canonical_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            provider_content_id="dQw4w9WgXcQ",
            view_count=12345,
            language_confidence=Decimal("0.900"),
        )

    async def close(self) -> None:
        return None


def guide_from(candidate: GuideCandidate, hotspot_id: UUID, **overrides: object) -> HotspotGuide:
    values: dict[str, object] = {
        "id": uuid4(),
        "hotspot_id": hotspot_id,
        "content_type": candidate.content_type,
        "provider": candidate.provider,
        "locale": candidate.locale,
        "title": candidate.title,
        "creator_name": candidate.creator_name,
        "canonical_url": candidate.canonical_url,
        "review_status": "pending",
        "metadata_json": dict(candidate.metadata),
    }
    values.update(overrides)
    return HotspotGuide(**values)


@pytest.fixture
def stack(monkeypatch):
    hotspot_id = uuid4()
    session = FakeSession(hotspot_id)
    user = SimpleNamespace(id=uuid4())
    captured: dict[str, object] = {}
    settings = get_settings().model_copy(update={"hotspot_guide_youtube_api_key": "yt-key"})

    async def fake_settings(_session: object) -> object:
        return settings

    monkeypatch.setattr(admin_router, "load_runtime_settings", fake_settings)
    monkeypatch.setattr(admin_router, "YouTubeGuideProvider", FakeYouTube)
    return SimpleNamespace(hotspot_id=hotspot_id, session=session, user=user, captured=captured)


def install_upsert(monkeypatch, stack, existing: HotspotGuide | None = None) -> None:
    async def fake_upsert(
        session: object, hotspot_id: UUID, candidate: GuideCandidate
    ) -> tuple[HotspotGuide, bool]:
        stack.captured["candidate"] = candidate
        if existing is not None:
            return existing, False
        return guide_from(candidate, hotspot_id), True

    monkeypatch.setattr(admin_router, "upsert_guide", fake_upsert)


def test_manual_requests_approve_by_default() -> None:
    request = ManualGuideRequest(
        hotspot_id=uuid4(), locale="zh-TW", content_type="article", url="https://example.com/post"
    )
    assert request.approve is True


@pytest.mark.asyncio
async def test_manual_video_keeps_the_chosen_locale_and_is_approved(monkeypatch, stack) -> None:
    install_upsert(monkeypatch, stack)
    payload = ManualGuideRequest(
        hotspot_id=stack.hotspot_id,
        locale="zh-TW",
        content_type="video",
        url="https://youtu.be/dQw4w9WgXcQ",
    )

    result = await add_manual_guide(payload, stack.user, stack.session, object())

    candidate = stack.captured["candidate"]
    assert isinstance(candidate, GuideCandidate)
    assert candidate.provider == "youtube"
    assert candidate.locale == "zh-TW"
    assert candidate.language_confidence == Decimal("1.000")
    assert candidate.metadata == {
        "discovery_method": "manual",
        "requested_locale": "zh-TW",
        "detected_locale": "ja",
    }
    assert result["created"] == 1
    assert result["review_status"] == "approved"
    assert result["locale"] == "zh-TW"
    audit = stack.session.added[-1]
    assert audit.action == "hotspot_guide_manual_added"
    assert audit.metadata_json["approve"] is True
    assert stack.session.flushes == 1
    assert stack.session.commits == 1


@pytest.mark.asyncio
async def test_existing_link_is_relocalised_and_approved(monkeypatch, stack) -> None:
    existing = guide_from(
        GuideCandidate(
            content_type="article",
            provider="brave",
            locale="en",
            title="Old title",
            creator_name="blog.example",
            canonical_url="https://blog.example/asakusa",
        ),
        stack.hotspot_id,
        review_status="rejected",
    )
    install_upsert(monkeypatch, stack, existing)
    payload = ManualGuideRequest(
        hotspot_id=stack.hotspot_id,
        locale="zh-TW",
        content_type="article",
        url="https://blog.example/asakusa",
        title="淺草寺散步",
        creator_name="blog.example",
        summary="一日遊路線",
    )

    result = await add_manual_guide(payload, stack.user, stack.session, object())

    candidate = stack.captured["candidate"]
    assert isinstance(candidate, GuideCandidate)
    assert candidate.provider == "manual"
    assert candidate.summary == "一日遊路線"
    assert candidate.metadata == {"discovery_method": "manual", "requested_locale": "zh-TW"}
    assert result == {
        "created": 0,
        "guide_id": str(existing.id),
        "review_status": "approved",
        "locale": "zh-TW",
    }
    assert existing.reviewed_by_user_id == stack.user.id
    assert existing.reviewed_at is not None
    assert existing.review_reason is None


@pytest.mark.asyncio
async def test_manual_article_can_stay_pending(monkeypatch, stack) -> None:
    install_upsert(monkeypatch, stack)
    payload = ManualGuideRequest(
        hotspot_id=stack.hotspot_id,
        locale="ko",
        content_type="article",
        url="https://blog.example/seoul",
        title="서울 여행",
        creator_name="blog.example",
        approve=False,
    )

    result = await add_manual_guide(payload, stack.user, stack.session, object())

    assert result["created"] == 1
    assert result["review_status"] == "pending"
    assert result["locale"] == "ko"


@pytest.mark.asyncio
async def test_manual_article_requires_title_and_creator(monkeypatch, stack) -> None:
    install_upsert(monkeypatch, stack)
    payload = ManualGuideRequest(
        hotspot_id=stack.hotspot_id,
        locale="en",
        content_type="article",
        url="https://blog.example/tokyo",
    )
    with pytest.raises(admin_router.AppError) as error:
        await add_manual_guide(payload, stack.user, stack.session, object())
    assert error.value.code == "hotspot_guide_metadata_required"


def _provider_check(table: object) -> str:
    """The SQL text of a table's provider CHECK, as the model declares it."""
    from sqlalchemy import CheckConstraint

    for constraint in table.constraints:  # type: ignore[attr-defined]
        if isinstance(constraint, CheckConstraint) and "provider" in constraint.name:
            return str(constraint.sqltext)
    raise AssertionError("no provider check constraint")


def test_every_provider_the_router_accepts_passes_the_run_check() -> None:
    """The setting, the payload and AIProviderName all grew a fourth provider in #204.

    The table did not, so choosing Gemini answered 500 from the INSERT. Checking the whole
    Literal rather than gemini alone is what stops the next provider slipping through.
    """
    from app.hotspots.ai_search import AI_PROVIDER_NAMES
    from app.models import HotspotGuideAISearchRun, HotspotIntroRun

    for table in (HotspotGuideAISearchRun.__table__, HotspotIntroRun.__table__):
        check = _provider_check(table)
        for provider in AI_PROVIDER_NAMES:
            assert f"'{provider}'" in check, f"{table.name} rejects {provider}"


def test_the_guide_run_check_matches_the_migration_that_widened_it() -> None:
    """models.py and the migration have to agree, or new and upgraded databases differ."""
    from pathlib import Path

    from app.models import HotspotGuideAISearchRun

    widened = "provider IN ('minimax', 'openai', 'anthropic', 'gemini')"
    versions = Path(__file__).resolve().parents[1] / "migrations/versions"
    migration = versions / "0051_guide_run_gemini.py"
    assert widened in migration.read_text("utf-8")
    assert _provider_check(HotspotGuideAISearchRun.__table__) == widened
