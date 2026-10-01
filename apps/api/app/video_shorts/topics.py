"""The topic library (docs/videos/SHORTS.md §三條內容線, §資料模型): what a topic needs before
it can be made, the fifteen-topic campaign's import, the topics the planner and the owner
write, and the ones the server makes itself from a public tutorial or an approved episode.

A topic's status follows from what it holds, except once the worker took it (``making``,
``made``) or someone gave it up (``dropped``): ``settle`` says which of ``idea``,
``needs_assets`` and ``ready`` it is, and why. The pure rules come first; the functions below
them load the rows and apply them. The module raises ``ShortsRefused``; the routes in
``admin_automation_api`` turn it into the API's errors.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsAsset, VideoShortsTopic
from app.video_shorts.schemas import (
    TEST_PROTOCOL_FIELDS,
    AssetOut,
    CampaignIn,
    CampaignTopic,
    TopicBrief,
    TopicIn,
    TopicOut,
    TopicPatch,
    TopicResult,
    TopicSummary,
    TopicsWrittenOut,
)
from app.video_shorts.settings import settings_row

# What the server cannot do for an experiment yet, and what it would take. The subscription
# runner (app.video_automation.subscription) turns every tool off and takes text only, so a
# model that must look at a photo needs a vision model on one of the site's keys; a program a
# model wrote must run somewhere isolated to be recorded on a phone screen.
UNSUPPORTED: dict[str, str] = {
    "vision": "受測模型要看圖：要接一個有金鑰的視覺模型，訂閱帳號的執行環境只收文字",
    "image_edit": "受測模型要修圖：要接一個有金鑰的修圖模型，訂閱帳號的執行環境只收文字",
    "sandbox": "要真的執行模型寫的程式並錄下手機操作：要先有隔離的執行環境",
}
# A generated picture costs money: such a topic is made only while the budget allows paid work.
PAID_REQUIREMENTS = frozenset({"image_generation"})
# The campaign's topics that need more than text (docs/videos/SHORTS.md §三條內容線): the owner's
# photos or sketch, a tool the site lacks, or a paid picture. campaign.json does not say this
# itself, so the import adds it by slug.
CAMPAIGN_NEEDS: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
    "shorts-taiwan-location": (
        [
            {
                "key": "landmarks",
                "label": "三張自己拍或已授權的公開景點照片（近景、遠景、易混淆的各一張），"
                "附拍攝者、日期與官方景點網址",
                "count": 3,
            }
        ],
        ["vision"],
    ),
    "shorts-photo-repair": (
        [{"key": "still-life", "label": "自己拍的文具靜物原片（三支筆、AB27 卡片、五元硬幣）"}],
        ["image_edit"],
    ),
    "shorts-menu-glare": (
        [{"key": "menu", "label": "自製虛構菜單的清晰版與反光版照片", "count": 2}],
        ["vision"],
    ),
    "shorts-sketch-website": (
        [{"key": "sketch", "label": "原創手繪網頁線稿的照片"}],
        ["vision", "sandbox"],
    ),
    "shorts-boba-game": ([], ["sandbox"]),
    "shorts-image-specificity": ([], ["image_generation"]),
}
# A public tutorial gives up to two highlights, a drama episode one vertical short; only the
# ones that went public or were approved within these days, so the first deploy does not turn
# the whole back catalogue into topics.
CUTS_PER_TUTORIAL = 2
AUTO_SINCE_DAYS = 60
LIST_LIMIT = 500
LINE_NAMES = {"lab": "實測", "cut": "長片精華", "drama": "漫劇直式短篇"}


# --- the rules ----------------------------------------------------------------------------------


def brief_problems(line: str, brief: Mapping[str, Any], source_slug: str | None) -> list[str]:
    """What the spec still lacks before the topic can be made; empty when it is complete.

    An experiment needs the seven protocol fields, a truth check and an acceptance list; a
    highlight or a drama short needs the video it is cut from.
    """
    if line != "lab":
        return [] if source_slug else ["還沒有來源影片"]
    protocol = brief.get("test_protocol") or {}
    problems = [
        f"測試規格缺 {field}"
        for field in TEST_PROTOCOL_FIELDS
        if not str(protocol.get(field) or "").strip()
    ]
    if not brief.get("truth_check"):
        problems.append("缺真值核對")
    if not brief.get("acceptance"):
        problems.append("缺完成條件")
    return problems


@dataclass(frozen=True)
class AssetFacts:
    need: str


def missing_assets(needed: Sequence[Mapping[str, Any]], assets: Iterable[AssetFacts]) -> list[str]:
    """The owner's material still missing, each as its label and how many more."""
    have: dict[str, int] = {}
    for asset in assets:
        have[asset.need] = have.get(asset.need, 0) + 1
    missing: list[str] = []
    for need in needed:
        count = int(need.get("count") or 1)
        short = count - have.get(str(need.get("key")), 0)
        if short > 0:
            label = str(need.get("label") or need.get("key"))
            missing.append(f"缺素材：{label}" + (f"（還差 {short} 個）" if count > 1 else ""))
    return missing


def unsupported(brief: Mapping[str, Any]) -> list[str]:
    return [UNSUPPORTED[name] for name in brief.get("requires") or [] if name in UNSUPPORTED]


def is_paid(line: str, brief: Mapping[str, Any]) -> bool:
    """Whether making the topic costs money: a drama short's pictures and clips, or an
    experiment that generates a picture."""
    return line == "drama" or bool(PAID_REQUIREMENTS & set(brief.get("requires") or []))


def settle(
    status: str,
    *,
    line: str,
    brief: Mapping[str, Any],
    source_slug: str | None,
    assets_needed: Sequence[Mapping[str, Any]],
    assets: Iterable[AssetFacts],
) -> tuple[str, list[str]]:
    """The status the topic's content gives it, and why it cannot be made yet.

    A topic the worker took or someone gave up keeps its status. Otherwise a spec with gaps
    is an ``idea``; a complete one waiting for the owner's files or for a tool the site does
    not have is ``needs_assets``; anything else is ``ready``.
    """
    problems = brief_problems(line, brief, source_slug)
    waiting = missing_assets(assets_needed, assets) + unsupported(brief)
    if status in ("making", "made", "dropped"):
        return status, problems + waiting
    if problems:
        return "idea", problems + waiting
    if waiting:
        return "needs_assets", waiting
    return "ready", []


def derived_slug(base: str, suffix: str) -> str:
    """A slug made from another one and a suffix, inside the 80 characters a slug may take:
    a long base is shortened and given a hash so two long bases cannot meet."""
    head = base if base[:1].isalpha() else f"s-{base}"
    slug = f"{head}-{suffix}"
    if len(slug) <= 80:
        return slug
    digest = hashlib.sha256(base.encode()).hexdigest()[:6]
    keep = 80 - len(suffix) - len(digest) - 2
    return f"{head[:keep].rstrip('-')}-{digest}-{suffix}"


def series_from(slug: str) -> str:
    """A source video's slug as a series name (40 characters at most)."""
    return slug[:40].rstrip("-") or slug[:1]


def campaign_brief(topic: CampaignTopic, requires: Sequence[str]) -> dict[str, Any]:
    protocol = topic.test_protocol
    brief = TopicBrief.model_validate(
        {
            "test_protocol": {
                field: (getattr(protocol, f"{field}_zh", None) or None) if protocol else None
                for field in TEST_PROTOCOL_FIELDS
            },
            "truth_check": [item for item in topic.truth_check if item.strip()],
            "acceptance": [item for item in topic.acceptance if item.strip()],
            "narration_outline": [
                {"seconds": beat.seconds, "voice": beat.voice_zh, "visual": beat.visual_zh}
                for beat in topic.narration_outline
            ],
            "titles": [title for title in topic.provisional_titles if title.strip()],
            "source_material": [item for item in topic.source_material if item.strip()],
            "source_ids": topic.source_ids,
            "estimated_seconds": topic.estimated_seconds,
            "requires": list(requires),
        }
    )
    return brief.model_dump(mode="json")


# --- reading ------------------------------------------------------------------------------------


def download_path(topic_slug: str, sha256: str) -> str:
    return f"video/media/files/{topic_slug}/{sha256}"


def asset_out(row: VideoShortsAsset) -> AssetOut:
    return AssetOut(
        id=row.id,
        need=row.need,
        sha256=row.sha256,
        filename=row.filename,
        content_type=row.content_type,
        size=int(row.size),
        author=row.author,
        taken_on=row.taken_on,
        rights_note=row.rights_note,
        created_at=row.created_at,
        download_path=download_path(row.topic_slug, row.sha256),
    )


def topic_out(row: VideoShortsTopic, assets: Sequence[VideoShortsAsset] = ()) -> TopicOut:
    _status, waiting = settle(
        row.status,
        line=row.line,
        brief=row.brief or {},
        source_slug=row.source_slug,
        assets_needed=row.assets_needed or [],
        assets=[AssetFacts(asset.need) for asset in assets],
    )
    return TopicOut(
        slug=row.slug,
        line=cast(Any, row.line),
        series=row.series,
        title=row.title,
        hook=row.hook,
        status=cast(Any, row.status),
        brief=dict(row.brief or {}),
        source_slug=row.source_slug,
        origin=cast(Any, row.origin),
        release_order=row.release_order,
        assets_needed=list(row.assets_needed or []),
        assets=[asset_out(asset) for asset in assets],
        waiting_for=[] if row.status in ("making", "made", "dropped") else waiting,
        paid=is_paid(row.line, row.brief or {}),
        project_slug=row.project_slug,
        started_at=row.started_at,
        finished_at=row.finished_at,
        note=row.note,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def topic_summary(row: VideoShortsTopic) -> TopicSummary:
    return TopicSummary(
        slug=row.slug,
        line=cast(Any, row.line),
        series=row.series,
        title=row.title,
        hook=row.hook,
        status=cast(Any, row.status),
        origin=cast(Any, row.origin),
        release_order=row.release_order,
        paid=is_paid(row.line, row.brief or {}),
    )


def order_key(row: VideoShortsTopic) -> tuple[bool, int, datetime, str]:
    """The pool's order: the owner's or the campaign's release order first, then the oldest."""
    return (
        row.release_order is None,
        row.release_order or 0,
        row.created_at,
        row.slug,
    )


async def assets_of(
    session: AsyncSession, slugs: Sequence[str]
) -> dict[str, list[VideoShortsAsset]]:
    if not slugs:
        return {}
    rows = await session.scalars(
        select(VideoShortsAsset)
        .where(VideoShortsAsset.topic_slug.in_(list(slugs)))
        .order_by(VideoShortsAsset.created_at)
    )
    found: dict[str, list[VideoShortsAsset]] = {}
    for row in rows:
        found.setdefault(row.topic_slug, []).append(row)
    return found


async def topic_row(session: AsyncSession, slug: str, *, lock: bool = False) -> VideoShortsTopic:
    statement = select(VideoShortsTopic).where(VideoShortsTopic.slug == slug)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        raise ShortsRefused(404, "video_shorts_topic_not_found", "找不到這個題目")
    return row


async def topic_view(session: AsyncSession, row: VideoShortsTopic) -> TopicOut:
    return topic_out(row, (await assets_of(session, [row.slug])).get(row.slug, []))


async def list_topics(
    session: AsyncSession, *, line: str | None = None, status: str | None = None
) -> list[TopicOut]:
    """The library in the pool's order; the tab groups it by line."""
    statement = select(VideoShortsTopic)
    if line is not None:
        statement = statement.where(VideoShortsTopic.line == line)
    if status is not None:
        statement = statement.where(VideoShortsTopic.status == status)
    rows = sorted(await session.scalars(statement.limit(LIST_LIMIT)), key=order_key)
    found = await assets_of(session, [row.slug for row in rows])
    return [topic_out(row, found.get(row.slug, [])) for row in rows]


# --- writing ------------------------------------------------------------------------------------


async def resettle(session: AsyncSession, row: VideoShortsTopic) -> None:
    """Give the topic the status its content and its files say. The caller commits."""
    with session.no_autoflush:
        assets = (await assets_of(session, [row.slug])).get(row.slug, [])
    status, _waiting = settle(
        row.status,
        line=row.line,
        brief=row.brief or {},
        source_slug=row.source_slug,
        assets_needed=row.assets_needed or [],
        assets=[AssetFacts(asset.need) for asset in assets],
    )
    row.status = status


def _new_topic(
    *,
    slug: str,
    payload: TopicIn,
    origin: str,
    now: datetime,
    actor: User | None = None,
    dedupe_key: str | None = None,
) -> VideoShortsTopic:
    brief = payload.brief.model_dump(mode="json")
    needed = [need.model_dump() for need in payload.assets_needed]
    status, _waiting = settle(
        "idea",
        line=payload.line,
        brief=brief,
        source_slug=payload.source_slug,
        assets_needed=needed,
        assets=[],
    )
    return VideoShortsTopic(
        id=uuid4(),
        slug=slug,
        line=payload.line,
        series=payload.series,
        title=payload.title,
        hook=payload.hook or None,
        status=status,
        brief=brief,
        source_slug=payload.source_slug,
        origin=origin,
        release_order=payload.release_order,
        assets_needed=needed,
        dedupe_key=dedupe_key,
        created_by_user_id=actor.id if actor else None,
        created_at=now,
        updated_at=now,
    )


async def _taken(session: AsyncSession, slugs: Sequence[str]) -> set[str]:
    """Which of these slugs a topic or a video already uses."""
    if not slugs:
        return set()
    topics = await session.scalars(
        select(VideoShortsTopic.slug).where(VideoShortsTopic.slug.in_(list(slugs)))
    )
    videos = await session.scalars(
        select(VideoProject.slug).where(VideoProject.slug.in_(list(slugs)))
    )
    return set(topics) | set(videos)


async def add_idea(
    session: AsyncSession, actor: User, payload: TopicIn, now: datetime | None = None
) -> TopicOut:
    """The owner's idea: a line and a sentence, kept as an ``idea`` the planner completes on
    its next round (or ready at once when the owner wrote the whole spec)."""
    moment = now or datetime.now(UTC)
    slug = payload.slug or f"idea-{moment:%Y%m%d}-{uuid4().hex[:6]}"
    if await _taken(session, [slug]):
        raise ShortsRefused(409, "video_shorts_topic_exists", "這個代號已經有題目或影片在用")
    row = _new_topic(slug=slug, payload=payload, origin="owner", now=moment, actor=actor)
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_topic_added",
            target=f"video_shorts_topic:{slug}",
            metadata_json={"line": row.line, "status": row.status},
        )
    )
    await session.commit()
    return topic_out(row)


async def write_planner_topics(
    session: AsyncSession, topics: Sequence[TopicIn], now: datetime | None = None
) -> TopicsWrittenOut:
    """The planner's new topics, and its completion of ideas still in the pool.

    A slug no topic or video uses is a new topic (``planner``); a slug of a topic that is
    still an ``idea`` takes the planner's spec in its place; any other slug is left as it
    is. Each is ``ready`` only when its spec is complete. The round is recorded so the
    planner is not asked again at once (``jobs``).
    """
    moment = now or datetime.now(UTC)
    slugs = [str(topic.slug) for topic in topics]
    with session.no_autoflush:
        existing = {
            row.slug: row
            for row in await session.scalars(
                select(VideoShortsTopic).where(VideoShortsTopic.slug.in_(slugs)).with_for_update()
            )
        }
        videos = set(
            await session.scalars(select(VideoProject.slug).where(VideoProject.slug.in_(slugs)))
        )
    items: list[TopicResult] = []
    for payload in topics:
        slug = str(payload.slug)
        row = existing.get(slug)
        if row is None and slug in videos:
            items.append(TopicResult(slug=slug, result="exists"))
            continue
        if row is None:
            row = _new_topic(slug=slug, payload=payload, origin="planner", now=moment)
            session.add(row)
            items.append(TopicResult(slug=slug, result="created", status=cast(Any, row.status)))
            continue
        if row.status != "idea":
            items.append(TopicResult(slug=slug, result="exists", status=cast(Any, row.status)))
            continue
        row.title = payload.title
        row.hook = payload.hook or row.hook
        row.series = payload.series or row.series
        row.brief = payload.brief.model_dump(mode="json")
        row.source_slug = payload.source_slug or row.source_slug
        if payload.assets_needed:
            row.assets_needed = [need.model_dump() for need in payload.assets_needed]
        row.updated_at = moment
        await resettle(session, row)
        items.append(TopicResult(slug=slug, result="updated", status=cast(Any, row.status)))
    settings = await settings_row(session, lock=True)
    settings.last_brief_at = moment
    await session.commit()
    return TopicsWrittenOut(
        created=sum(1 for item in items if item.result == "created"),
        updated=sum(1 for item in items if item.result == "updated"),
        skipped=sum(1 for item in items if item.result == "exists"),
        items=items,
    )


async def import_campaign(
    session: AsyncSession, actor: User, payload: CampaignIn, now: datetime | None = None
) -> TopicsWrittenOut:
    """The campaign's topics (campaign.json, sent as it is) as ``campaign`` topics.

    A topic already in the library under the same slug is left alone, so importing twice
    adds nothing; a topic the owner later edits keeps the edit.
    """
    moment = now or datetime.now(UTC)
    slugs = [topic.slug for topic in payload.topics]
    if len(set(slugs)) != len(slugs):
        raise ShortsRefused(
            422, "video_shorts_campaign_invalid", "campaign.json 裡有重複的題目代號"
        )
    with session.no_autoflush:
        taken = await _taken(session, slugs)
    items: list[TopicResult] = []
    for topic in payload.topics:
        if topic.slug in taken:
            current = await session.scalar(
                select(VideoShortsTopic.status).where(VideoShortsTopic.slug == topic.slug)
            )
            items.append(TopicResult(slug=topic.slug, result="exists", status=cast(Any, current)))
            continue
        needed, requires = CAMPAIGN_NEEDS.get(topic.slug, ([], []))
        row = _new_topic(
            slug=topic.slug,
            payload=TopicIn(
                slug=topic.slug,
                line="lab",
                series=topic.series or topic.series_id,
                title=topic.topic_zh,
                hook=(topic.hook_zh or "")[:300] or None,
                brief=TopicBrief.model_validate(campaign_brief(topic, requires)),
                assets_needed=cast(Any, needed),
                release_order=topic.release_order,
            ),
            origin="campaign",
            now=moment,
            actor=actor,
            dedupe_key=f"campaign:{topic.slug}",
        )
        session.add(row)
        items.append(TopicResult(slug=topic.slug, result="created", status=cast(Any, row.status)))
    created = sum(1 for item in items if item.result == "created")
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_campaign_imported",
            target="video_shorts_topics",
            metadata_json={
                "campaign_id": payload.campaign_id,
                "created": created,
                "skipped": len(items) - created,
            },
        )
    )
    await session.commit()
    return TopicsWrittenOut(created=created, skipped=len(items) - created, items=items)


EDITABLE = ("idea", "ready", "needs_assets")


async def patch_topic(
    session: AsyncSession,
    actor: User,
    slug: str,
    payload: TopicPatch,
    now: datetime | None = None,
) -> TopicOut:
    """The owner's change: the wording, the spec, the material it needs, its place in the
    pool, giving it up or taking it back. A topic the worker took is changed no more."""
    moment = now or datetime.now(UTC)
    row = await topic_row(session, slug, lock=True)
    fields = payload.model_fields_set - {"note", "dropped"}
    # A topic in the making can still be given up (its video dropped, say), and taken back
    # later to be made again under a new video; a made one is history.
    if (row.status == "making" and (fields or payload.dropped is False)) or (
        row.status == "made" and (fields or payload.dropped is not None)
    ):
        raise ShortsRefused(
            409,
            "video_shorts_topic_taken",
            "這個題目已經在做或做完了，不能再改；在做的可以放棄",
        )
    if row.status == "dropped" and fields and payload.dropped is not False:
        raise ShortsRefused(409, "video_shorts_topic_dropped", "這個題目已經放棄了，先取回再改")
    before = row.status
    if payload.title is not None:
        row.title = payload.title
    if "hook" in payload.model_fields_set:
        row.hook = payload.hook or None
    if "series" in payload.model_fields_set:
        row.series = payload.series
    if payload.brief is not None:
        row.brief = payload.brief.model_dump(mode="json")
    if payload.assets_needed is not None:
        row.assets_needed = [need.model_dump() for need in payload.assets_needed]
    if "release_order" in payload.model_fields_set:
        row.release_order = payload.release_order
    if "note" in payload.model_fields_set:
        row.note = payload.note or None
    if payload.dropped is True:
        row.status = "dropped"
    elif payload.dropped is False and row.status == "dropped":
        row.status = "idea"
    if row.status in EDITABLE:
        row.status = "idea"
        await resettle(session, row)
    row.updated_at = moment
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_topic_changed",
            target=f"video_shorts_topic:{slug}",
            metadata_json={
                "changed": sorted(payload.model_fields_set),
                "before": before,
                "status": row.status,
            },
        )
    )
    await session.commit()
    return await topic_view(session, row)


# --- the server's own topics --------------------------------------------------------------------


def _cut_topic(project: VideoProject, number: int, now: datetime) -> VideoShortsTopic:
    other = "，跟另一支精華講不同的事" if number > 1 else ""
    payload = TopicIn(
        line="cut",
        series=series_from(project.slug),
        title=f"{project.title}（精華 {number}）"[:200],
        brief=TopicBrief(
            notes=f"從這支已公開的長片挑一段（鉤子到結論在 55 秒內）改寫成直式字卡{other}；"
            "結尾導回完整影片。找不到值得單獨成片的段落時放棄這個題目。"
        ),
        source_slug=project.slug,
    )
    return _new_topic(
        slug=derived_slug(project.slug, f"cut-{number}"),
        payload=payload,
        origin="auto",
        now=now,
        dedupe_key=f"cut:{project.slug}:{number}",
    )


def _drama_topic(project: VideoProject, now: datetime) -> VideoShortsTopic:
    payload = TopicIn(
        line="drama",
        series=series_from(project.series_slug or project.slug),
        title=f"{project.title}（直式短篇）"[:200],
        brief=TopicBrief(
            notes="從這一集挑鉤子與懸念的鏡頭與台詞，每鏡用原關鍵影格重畫成 9:16；"
            "結尾導回完整的一集。",
            requires=["image_generation"],
        ),
        source_slug=project.slug,
    )
    return _new_topic(
        slug=derived_slug(project.slug, "vertical"),
        payload=payload,
        origin="auto",
        now=now,
        dedupe_key=f"drama:{project.slug}",
    )


async def ensure_auto_topics(session: AsyncSession, now: datetime | None = None) -> int:
    """Topics the server writes itself: up to two highlights for each tutorial that went
    public (a video id and a publish time that has passed), one vertical short for each drama
    episode whose final cut was approved. A source gives its topics once, whatever became of
    them. The caller commits."""
    moment = now or datetime.now(UTC)
    since = moment - timedelta(days=AUTO_SINCE_DAYS)
    with session.no_autoflush:
        tutorials = list(
            await session.scalars(
                select(VideoProject).where(
                    VideoProject.format == "slides",
                    VideoProject.shorts_line.is_(None),
                    VideoProject.dropped_at.is_(None),
                    VideoProject.youtube_removed_at.is_(None),
                    VideoProject.youtube_video_id.is_not(None),
                    VideoProject.youtube_publish_at <= moment,
                    VideoProject.youtube_publish_at >= since,
                )
            )
        )
        approved = (
            select(VideoReview.project_id)
            .where(
                VideoReview.gate == "final",
                VideoReview.status == "approved",
                VideoReview.decided_at >= since,
            )
            .subquery()
        )
        episodes = list(
            await session.scalars(
                select(VideoProject)
                .join(approved, approved.c.project_id == VideoProject.id)
                .where(
                    and_(
                        VideoProject.format == "drama",
                        VideoProject.shorts_line.is_(None),
                        VideoProject.dropped_at.is_(None),
                    )
                )
                .distinct()
            )
        )
        wanted: list[tuple[str, VideoShortsTopic]] = []
        for project in tutorials:
            for number in range(1, CUTS_PER_TUTORIAL + 1):
                wanted.append((f"cut:{project.slug}:{number}", _cut_topic(project, number, moment)))
        for project in episodes:
            wanted.append((f"drama:{project.slug}", _drama_topic(project, moment)))
        if not wanted:
            return 0
        keys = [key for key, _row in wanted]
        known = set(
            await session.scalars(
                select(VideoShortsTopic.dedupe_key).where(VideoShortsTopic.dedupe_key.in_(keys))
            )
        )
        fresh = [row for key, row in wanted if key not in known]
        taken = await _taken(session, [row.slug for row in fresh])
    for row in fresh:
        if row.slug in taken:
            digest = hashlib.sha256(str(row.dedupe_key).encode()).hexdigest()[:6]
            row.slug = derived_slug(row.slug[:60].rstrip("-"), digest)
        session.add(row)
    return len(fresh)
