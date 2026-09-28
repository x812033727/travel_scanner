"""Send one video to the linked channel: the mp4, the details, the captions and the thumbnail.

docs/videos/HANDS-OFF.md §YouTube API. The owner sends a video from the "ready to upload" card on
/admin/videos: either the site uploads the approved mp4 itself (``upload``; until the Cloud
project passes YouTube's API audit such an upload is locked private), or the owner uploaded it in
Studio as a private video and pastes its address (``studio``). The site then writes, from the
approved upload package:

- ``details``: videos.update with the title and description (the owner may have rewritten the
  zh-TW ones), the four other locales, the tags, the category, the made-for-kids and synthetic
  media answers, and the visibility. A scheduled video stays private and carries ``publishAt``,
  so YouTube publishes it at the owner's time; the site never makes a video public itself, and it
  refuses to touch one that already is.
- ``captions``: one captions.insert per locale the video has no uploaded track for yet.
- ``thumbnail``: thumbnails.set.

The package is read from the review store, which only the API container mounts, so the run is an
asyncio task in the API process. It holds a lease on the project's ``youtube_sync`` and renews it
while it works; if the process restarts mid-run the lease lapses, the card shows the run as
interrupted, and a retry picks up where it stopped (the mp4 through its resumable session).
"""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.admin.service import load_runtime_settings
from app.db import SessionFactory
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectOut
from app.video_reviews.storage import ReviewStore
from app.video_youtube import connection
from app.video_youtube.client import (
    AuthorizationLost,
    UploadInterrupted,
    UploadState,
    YoutubeClient,
    YoutubeError,
)
from app.video_youtube.errors import Refused
from app.video_youtube.requests import (
    CAPTION_NAME,
    as_dict,
    caption_languages,
    insert_body,
    language_key,
    locale_of_role,
    text_problem,
    update_body,
)
from app.video_youtube.schemas import PublishIn
from app.video_youtube.state import new_state, now_text, parse_time, retried, running, step

logger = logging.getLogger(__name__)

LEASE = timedelta(minutes=5)
HEARTBEAT_SECONDS = 60.0
# 8 MiB: the resumable protocol wants every chunk but the last to be a multiple of 256 KiB.
CHUNK_BYTES = 32 * 256 * 1024
# A chunk that does not arrive is retried after these pauses; then the run stops, and a retry
# resumes from the byte YouTube last kept.
BACKOFF_SECONDS = (2.0, 10.0, 30.0, 60.0)
# The publish time has to be ahead of the run, with room for the upload before it.
MIN_LEAD = timedelta(minutes=5)
# An access token lives an hour; a long upload asks for a new one before that.
TOKEN_AGE = timedelta(minutes=40)
QUOTA_REASONS = frozenset({"quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded"})
_TASKS: set[asyncio.Task[None]] = set()


class StepFailed(Exception):
    """A step YouTube or the package would not let through; ``detail`` is what the card shows."""


class LeaseLost(Exception):
    """Another run holds this video now, or its state was replaced; this one stops quietly."""


@dataclass(frozen=True)
class PackageFile:
    sha256: str
    size: int
    content_type: str


@dataclass(frozen=True)
class Package:
    review_id: str
    sha256: str
    metadata: dict[str, Any]
    final: PackageFile | None
    thumbnail: PackageFile | None
    captions: dict[str, PackageFile] = field(default_factory=dict)


# --- the approved package ------------------------------------------------------------------------


def approved_confirmation(rows: list[VideoReview]) -> VideoReview | None:
    """The newest approved upload confirmation; reviews come newest first."""
    return next((row for row in rows if row.gate == "publish" and row.status == "approved"), None)


def _file(item: dict[str, Any]) -> PackageFile:
    return PackageFile(str(item["sha256"]), int(item["size"]), str(item["content_type"]))


def read_package(store: ReviewStore, slug: str, review: VideoReview) -> Package:
    """The package of an approved confirmation, from the review store, checked against it.

    The confirmation is bound to the SHA-256 of metadata.json, and every file the store holds is
    named by its own SHA-256, so what is sent is exactly what was approved.
    """
    files = [item for item in review.files if isinstance(item, dict) and item.get("sha256")]
    by_role = {str(item.get("role")): item for item in files}
    meta = by_role.get("metadata")
    if meta is None or meta.get("sha256") != review.content_sha256:
        raise Refused(
            409, "video_youtube_package_invalid", "核准的上傳包裡沒有對得上的 metadata.json"
        )
    path = store.path(slug, review.content_sha256)
    if path is None:
        raise Refused(409, "video_youtube_package_missing", "審核區已經找不到這份上傳包")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != review.content_sha256:
        raise Refused(409, "video_youtube_package_invalid", "上傳包和核准的那一份不一樣")
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Refused(409, "video_youtube_package_invalid", "metadata.json 讀不懂") from exc
    if not isinstance(metadata, dict) or not isinstance(metadata.get("title"), str):
        raise Refused(409, "video_youtube_package_invalid", "metadata.json 沒有標題")
    final = by_role.get("final")
    if final is not None and metadata.get("final_sha256") not in (None, final["sha256"]):
        raise Refused(
            409, "video_youtube_package_invalid", "上傳包的 mp4 不是 metadata.json 記的那一支"
        )
    payload_locales = review.payload.get("locales") if isinstance(review.payload, dict) else None
    locales = [str(item) for item in payload_locales] if isinstance(payload_locales, list) else []
    captions = {
        locale_of_role(role, "captions_", locales): _file(item)
        for role, item in by_role.items()
        if role.startswith("captions_")
    }
    thumbnail = by_role.get("thumbnail")
    return Package(
        review_id=str(review.id),
        sha256=review.content_sha256,
        metadata=metadata,
        final=_file(final) if final is not None else None,
        thumbnail=_file(thumbnail) if thumbnail is not None else None,
        captions=dict(sorted(captions.items())),
    )


# --- the owner's request -------------------------------------------------------------------------


async def _locked_project(session: AsyncSession, slug: str) -> VideoProject:
    project = await session.scalar(
        select(VideoProject).where(VideoProject.slug == slug).with_for_update()
    )
    if project is None:
        raise Refused(404, "video_project_not_found", "找不到這支影片")
    if project.dropped_at is not None:
        raise Refused(409, "video_project_dropped", "站主已經放棄這支影片")
    return project


async def _project_reviews(session: AsyncSession, project: VideoProject) -> list[VideoReview]:
    rows = await session.scalars(
        select(VideoReview)
        .where(VideoReview.project_id == project.id)
        .order_by(VideoReview.created_at.desc())
    )
    return list(rows)


async def _linked_connection(session: AsyncSession) -> Any:
    row = await connection.connection_row(session)
    if not connection.linked(row):
        raise Refused(409, "video_youtube_not_linked", "還沒有連結 YouTube 頻道：到設定分頁連結")
    if row.problem:
        raise Refused(409, "video_youtube_grant_lost", row.problem)
    return row


def launch(slug: str) -> None:
    """Run the video's sync in this process; the task is kept so it is not collected midway."""
    task = asyncio.get_running_loop().create_task(run_sync(slug))
    _TASKS.add(task)
    task.add_done_callback(_TASKS.discard)


def _audit(session: AsyncSession, user: User, action: str, slug: str, **metadata: Any) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=action,
            target=f"video_project:{slug}",
            metadata_json={"slug": slug, **metadata},
        )
    )


async def request_sync(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    user: User,
    payload: PublishIn,
    *,
    on_behalf: dict[str, Any] | None = None,
) -> ProjectOut:
    """Check the owner's request against the package and the channel, record it, and start it.

    ``on_behalf`` is set when the site sends a Short under the owner's standing consent
    (docs/videos/SHORTS.md): ``user`` is then who gave the consent, and what is passed here
    (that it was automatic, and the consent's id) goes into the audit entry with the rest.
    """
    row = await _linked_connection(session)
    project = await _locked_project(session, slug)
    if running(project.youtube_sync):
        raise Refused(409, "video_youtube_sync_running", "這支影片正在送 YouTube，等它跑完再送")
    review = approved_confirmation(await _project_reviews(session, project))
    if review is None:
        raise Refused(409, "video_youtube_not_ready", "這支影片還沒有核准的上傳包")
    package = read_package(store, slug, review)
    title = payload.title if payload.title is not None else str(package.metadata["title"])
    description = (
        payload.description
        if payload.description is not None
        else str(package.metadata.get("description") or "")
    )
    problem = text_problem(title, description)
    if problem:
        raise Refused(422, "video_youtube_text_invalid", problem)
    publish_at = payload.publish_at if payload.visibility == "scheduled" else None
    if payload.visibility == "scheduled":
        if publish_at is None:
            raise Refused(422, "video_youtube_publish_at_missing", "排程上架要選上架時間")
        if publish_at < datetime.now(UTC) + MIN_LEAD:
            raise Refused(422, "video_youtube_publish_at_past", "上架時間要在現在的五分鐘之後")
    video_id: str | None = None
    if payload.mode == "studio":
        video_id = reviews.youtube_video_id(payload.url or "")
        if video_id is None:
            raise Refused(
                422,
                "video_youtube_url_invalid",
                "看不出影片 id：貼上 youtu.be、watch?v=、shorts 或 Studio 的網址，"
                "或 11 個字元的 id",
            )
    else:
        if project.youtube_video_id:
            raise Refused(
                409,
                "video_youtube_already_uploaded",
                f"這支已經在 YouTube 上了（{project.youtube_video_id}），改資料請用「重新送出」",
            )
        if package.final is None or store.path(slug, package.final.sha256) is None:
            raise Refused(
                409, "video_youtube_mp4_missing", "審核區已經沒有這支的 mp4，請在 Studio 上傳"
            )
        if not row.audited and not payload.accept_private_lock:
            raise Refused(
                422,
                "video_youtube_private_lock",
                "API 稽核還沒通過：網站上傳的影片會被 YouTube 鎖成私人、不能公開。"
                "只是測試的話請勾選確認",
            )
    request = {
        "mode": payload.mode,
        "visibility": payload.visibility,
        "publish_at": publish_at.isoformat() if publish_at else None,
        "title": title,
        "description": description,
        "video_id": video_id,
        "accept_private_lock": payload.accept_private_lock,
        "review_id": package.review_id,
        "package_sha256": package.sha256,
    }
    project.youtube_sync = new_state(request)
    project.updated_at = datetime.now(UTC)
    _audit(
        session,
        user,
        "video_youtube_sync_requested",
        slug,
        mode=payload.mode,
        visibility=payload.visibility,
        publish_at=request["publish_at"],
        video_id=video_id,
        package_sha256=package.sha256,
        **(on_behalf or {}),
    )
    await session.commit()
    launch(slug)
    return await reviews.project_view(session, slug)


async def retry_sync(
    session: AsyncSession, slug: str, user: User, *, on_behalf: dict[str, Any] | None = None
) -> ProjectOut:
    """Run the last request again: finished steps stay finished, the rest start over.
    ``on_behalf`` is what it is for ``request_sync``."""
    await _linked_connection(session)
    project = await _locked_project(session, slug)
    state = project.youtube_sync
    if not state:
        raise Refused(409, "video_youtube_sync_missing", "這支影片還沒有送過 YouTube")
    if running(state):
        raise Refused(409, "video_youtube_sync_running", "這支影片正在送 YouTube，等它跑完再送")
    if state.get("status") == "done":
        raise Refused(409, "video_youtube_sync_done", "上一次已經全部完成；要改資料請重新送出")
    project.youtube_sync = retried(state)
    project.updated_at = datetime.now(UTC)
    _audit(session, user, "video_youtube_sync_retried", slug, **(on_behalf or {}))
    await session.commit()
    launch(slug)
    return await reviews.project_view(session, slug)


# --- the run -------------------------------------------------------------------------------------


Factory = async_sessionmaker[AsyncSession]


@dataclass
class Run:
    slug: str
    token: str
    factory: Factory
    http: httpx.AsyncClient
    store: ReviewStore
    package: Package
    request: dict[str, Any]
    channel_id: str
    audited: bool
    access: str = ""
    access_at: datetime | None = None

    async def update(self, mutate: Callable[[dict[str, Any], VideoProject], None]) -> None:
        """Change the state under a row lock, if this run still holds it; renews the lease."""
        async with self.factory() as session:
            project = await session.scalar(
                select(VideoProject).where(VideoProject.slug == self.slug).with_for_update()
            )
            if project is None or not project.youtube_sync:
                raise LeaseLost(self.slug)
            state = copy.deepcopy(project.youtube_sync)
            if state.get("run") != self.token:
                raise LeaseLost(self.slug)
            mutate(state, project)
            if state.get("status") == "running":
                state["lease_until"] = now_text(datetime.now(UTC) + LEASE)
            project.youtube_sync = state
            await session.commit()

    async def mark(self, step_id: str, state_name: str, detail: str = "") -> None:
        def change(state: dict[str, Any], _project: VideoProject) -> None:
            item = step(state, step_id)
            if item is not None:
                item.update(state=state_name, detail=detail, at=now_text())

        await self.update(change)

    async def client(self) -> YoutubeClient:
        moment = datetime.now(UTC)
        if not self.access or self.access_at is None or moment - self.access_at > TOKEN_AGE:
            async with self.factory() as session:
                try:
                    self.access = await connection.access_token(session, self.http)
                except Refused as refused:
                    raise StepFailed(refused.detail) from refused
            self.access_at = moment
        return YoutubeClient(self.http, self.access)

    def file(self, item: PackageFile) -> Path:
        path = self.store.path(self.slug, item.sha256)
        if path is None:
            raise StepFailed("審核區已經找不到上傳包裡的檔案，請重新產生上傳包")
        return path


def describe(error: YoutubeError) -> str:
    """A refusal from YouTube in the owner's words, with what to do about it."""
    if error.reason in QUOTA_REASONS:
        return "今天的 YouTube API 配額用完了（每天太平洋時間午夜重置），明天再按重試"
    if error.reason == "uploadLimitExceeded":
        return "這個頻道今天的上傳次數到上限了，明天再按重試"
    if isinstance(error, AuthorizationLost) or error.status == 401:
        return connection.LOST_GRANT
    return f"YouTube 回覆 {error.status} {error.reason}：{error.message}"


def _read_chunk(path: Path, offset: int, size: int) -> bytes:
    with path.open("rb") as handle:
        handle.seek(offset)
        return handle.read(size)


def _session_of(stored: str | None, sha256: str) -> str | None:
    """The stored upload session, when it is for this very mp4 (stored as "<sha256> <uri>")."""
    if not stored:
        return None
    sha, _, uri = stored.partition(" ")
    return uri if sha == sha256 and uri else None


async def _upload(run: Run) -> str:
    """videos.insert through a resumable session; returns the new video's id."""
    async with run.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == run.slug))
        existing = project.youtube_video_id if project else None
        stored = project.youtube_upload_session if project else None
    if existing:
        return existing
    final = run.package.final
    if final is None:
        raise StepFailed("上傳包裡沒有 mp4")
    path = run.file(final)
    size = path.stat().st_size
    client = await run.client()
    session_uri = _session_of(stored, final.sha256)
    state: UploadState | None = None
    if session_uri:
        state = await _status(client, session_uri, size)
        if state.kind == "gone":
            session_uri = None
    if session_uri is None:
        body = insert_body(run.package.metadata, run.request["title"], run.request["description"])
        session_uri = await client.start_upload(body, size=size, content_type=final.content_type)
        uri = session_uri

        def keep_session(_state: dict[str, Any], project: VideoProject) -> None:
            project.youtube_upload_session = f"{final.sha256} {uri}"

        await run.update(keep_session)
        state = UploadState("partial", 0)
    assert state is not None
    failures = 0
    while state.kind != "done":
        if state.kind == "gone":
            raise StepFailed("YouTube 的上傳工作階段過期了，按重試會重新上傳")
        offset = state.offset
        await run.update(_progress(offset, size))
        chunk = await asyncio.to_thread(_read_chunk, path, offset, CHUNK_BYTES)
        client = await run.client()
        try:
            state = await client.upload_chunk(
                session_uri, offset=offset, data=chunk, size=size, content_type=final.content_type
            )
            failures = 0
        except UploadInterrupted:
            if failures >= len(BACKOFF_SECONDS):
                raise StepFailed(
                    "上傳一直中斷，已經停下來；按重試會從 YouTube 收到的地方接著傳"
                ) from None
            await asyncio.sleep(BACKOFF_SECONDS[failures])
            failures += 1
            state = await _status(client, session_uri, size)
    video = state.video or {}
    video_id = str(video.get("id") or "")
    if not video_id:
        raise StepFailed("YouTube 說上傳完成，卻沒有給影片 id")

    def uploaded(state_: dict[str, Any], project: VideoProject) -> None:
        project.youtube_video_id = video_id
        project.youtube_upload_session = None
        state_["request"]["video_id"] = video_id
        state_["progress"] = {"sent": size, "total": size}

    await run.update(uploaded)
    return video_id


def _progress(sent: int, total: int) -> Callable[[dict[str, Any], VideoProject], None]:
    def change(state: dict[str, Any], _project: VideoProject) -> None:
        state["progress"] = {"sent": sent, "total": total}

    return change


async def _status(client: YoutubeClient, session_uri: str, size: int) -> UploadState:
    for pause in (*BACKOFF_SECONDS, None):
        try:
            return await client.upload_status(session_uri, size=size)
        except UploadInterrupted:
            if pause is None:
                break
            await asyncio.sleep(pause)
    raise StepFailed("問不到 YouTube 收到多少，已經停下來；稍後按重試")


def _visibility_text(request: dict[str, Any]) -> str:
    if request["visibility"] == "scheduled":
        return f"私人，排定 {request['publish_at']} 公開"
    return "不公開" if request["visibility"] == "unlisted" else "私人"


async def _details(run: Run, video_id: str) -> str:
    client = await run.client()
    video = await client.video(video_id)
    if video is None:
        raise StepFailed("找不到這支影片：網址對嗎？影片要在連結的頻道裡")
    snippet = as_dict(video.get("snippet"))
    status = as_dict(video.get("status"))
    if snippet.get("channelId") != run.channel_id:
        raise StepFailed("這支影片不在連結的頻道裡；確認網址，或到設定分頁換成影片所在的頻道")
    privacy = status.get("privacyStatus")
    if privacy == "public":
        raise StepFailed("這支影片已經公開了；網站不改已經公開的影片，要改請在 Studio 改")
    if run.request["visibility"] == "scheduled" and privacy != "private":
        raise StepFailed("排程上架要影片先是「私人」：請在 Studio 改成私人，再按重試")
    publish_at = parse_time(run.request.get("publish_at"))
    body = update_body(
        video,
        run.package.metadata,
        title=run.request["title"],
        description=run.request["description"],
        visibility=run.request["visibility"],
        publish_at=publish_at,
    )
    try:
        await client.update_video(body)
    except YoutubeError as error:
        if error.reason == "invalidPublishAt":
            raise StepFailed(
                "YouTube 不接受這個上架時間：影片要是私人、從來沒有公開過，時間也要在未來"
            ) from error
        raise

    def recorded(_state: dict[str, Any], project: VideoProject) -> None:
        project.youtube_video_id = video_id
        project.youtube_publish_at = publish_at
        project.updated_at = datetime.now(UTC)

    await run.update(recorded)
    locales = len(body["localizations"]) + 1
    tags = len(body["snippet"].get("tags") or [])
    return (
        f"標題、說明、{locales} 個語系、{tags} 個標籤、分類與揭露；{_visibility_text(run.request)}"
    )


async def _captions(run: Run, video_id: str) -> tuple[str, str]:
    """Returns (state, detail): one captions.insert per locale the video has no track for."""
    if not run.package.captions:
        return "skipped", "上傳包沒有字幕檔"
    client = await run.client()
    have = caption_languages(await client.captions(video_id))
    done: list[str] = []
    failed: list[str] = []
    for locale, item in run.package.captions.items():
        if language_key(locale) in have:
            done.append(f"{locale} 已經有了")
            continue
        data = run.file(item).read_bytes()
        try:
            await client.insert_caption(video_id, language=locale, name=CAPTION_NAME, data=data)
        except YoutubeError as error:
            if error.reason == "captionExists":
                done.append(f"{locale} 已經有了")
                continue
            if error.reason in QUOTA_REASONS:
                raise
            failed.append(f"{locale}：{describe(error)}")
            continue
        have.add(language_key(locale))
        done.append(f"{locale} 已上傳")
    if failed:
        raise StepFailed("；".join([*failed, *done]))
    return "done", "、".join(done)


async def _thumbnail(run: Run, video_id: str) -> tuple[str, str]:
    item = run.package.thumbnail
    if item is None:
        return "skipped", "上傳包沒有縮圖"
    client = await run.client()
    try:
        await client.set_thumbnail(video_id, run.file(item).read_bytes(), item.content_type)
    except YoutubeError as error:
        if error.reason == "forbidden" or error.status == 403:
            raise StepFailed(
                "YouTube 不讓這個頻道用自訂縮圖：頻道要先完成電話驗證（Studio → 設定 → 頻道 → "
                "功能使用資格），完成後按重試"
            ) from error
        raise
    return "done", "縮圖已設定"


async def _claim(factory: Factory, slug: str) -> dict[str, Any] | None:
    """Take the video's queued run, or None when there is none or another run holds it."""
    async with factory() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == slug).with_for_update()
        )
        state = copy.deepcopy(project.youtube_sync) if project and project.youtube_sync else None
        if state is None or state.get("status") not in ("queued", "running"):
            return None
        lease = parse_time(state.get("lease_until"))
        if state.get("status") == "running" and lease is not None and lease > datetime.now(UTC):
            return None
        moment = datetime.now(UTC)
        state.update(
            status="running",
            run=uuid.uuid4().hex,
            started_at=now_text(moment),
            lease_until=now_text(moment + LEASE),
            attempts=int(state.get("attempts") or 0) + 1,
            error=None,
        )
        assert project is not None
        project.youtube_sync = state
        await session.commit()
        return state


async def _heartbeat(run: Run) -> None:
    while True:
        await asyncio.sleep(HEARTBEAT_SECONDS)
        try:
            await run.update(lambda _state, _project: None)
        except LeaseLost:
            return


async def _prepare(factory: Factory, slug: str, state: dict[str, Any]) -> tuple[Any, ...]:
    request = state["request"]
    async with factory() as session:
        store = reviews.review_store(await load_runtime_settings(session))
        row = await connection.connection_row(session)
        channel_id, audited = row.channel_id or "", row.audited
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
        if project is None:
            raise StepFailed("找不到這支影片")
        review = approved_confirmation(await _project_reviews(session, project))
        await session.commit()
    if review is None or str(review.id) != request.get("review_id"):
        raise StepFailed("核准的上傳包換了一份：請重新送出，讓網站用新的那一份")
    try:
        package = read_package(store, slug, review)
    except Refused as refused:
        raise StepFailed(refused.detail) from refused
    if package.sha256 != request.get("package_sha256"):
        raise StepFailed("上傳包和送出時的那一份不一樣：請重新送出")
    return store, package, channel_id, audited


async def run_sync(slug: str, factory: Factory | None = None) -> None:
    """The task ``launch`` starts: every step not done yet, in order, recorded as it goes."""
    factory = factory or SessionFactory
    state = await _claim(factory, slug)
    if state is None:
        return
    token = str(state["run"])
    current: str | None = None
    async with connection.http_client() as http:
        run: Run | None = None
        heartbeat: asyncio.Task[None] | None = None
        try:
            store, package, channel_id, audited = await _prepare(factory, slug, state)
            run = Run(
                slug=slug,
                token=token,
                factory=factory,
                http=http,
                store=store,
                package=package,
                request=state["request"],
                channel_id=channel_id,
                audited=audited,
            )
            heartbeat = asyncio.create_task(_heartbeat(run))
            video_id = str(state["request"].get("video_id") or "")
            for item in state["steps"]:
                current = str(item["id"])
                if item.get("state") in ("done", "skipped"):
                    continue
                await run.mark(current, "running")
                if current == "upload":
                    video_id = await _upload(run)
                    lock = "" if audited else "（專案還沒通過稽核，YouTube 會鎖成私人）"
                    await run.mark(current, "done", f"已上傳，影片 ID {video_id}{lock}")
                elif current == "details":
                    await run.mark(current, "done", await _details(run, video_id))
                elif current == "captions":
                    await run.mark(current, *await _captions(run, video_id))
                elif current == "thumbnail":
                    await run.mark(current, *await _thumbnail(run, video_id))
            await _finish(factory, slug, token, None, None)
        except LeaseLost:
            logger.info("YouTube sync of %s stopped: another run holds it", slug)
        except StepFailed as failure:
            await _finish(factory, slug, token, current, str(failure))
        except YoutubeError as error:
            await _finish(factory, slug, token, current, describe(error))
        except httpx.HTTPError as error:
            logger.warning("YouTube sync of %s could not reach Google: %s", slug, error)
            await _finish(factory, slug, token, current, "連不到 YouTube，稍後按重試")
        except Exception:
            logger.exception("YouTube sync of %s failed", slug)
            await _finish(factory, slug, token, current, "網站這邊出錯了（已記在日誌），稍後按重試")
        finally:
            if heartbeat is not None:
                heartbeat.cancel()


async def _finish(
    factory: Factory, slug: str, token: str, step_id: str | None, error: str | None
) -> None:
    async with factory() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == slug).with_for_update()
        )
        if project is None or not project.youtube_sync:
            return
        state = copy.deepcopy(project.youtube_sync)
        if state.get("run") != token:
            return
        if error is not None and step_id is not None:
            item = step(state, step_id)
            if item is not None:
                item.update(state="failed", detail=error, at=now_text())
        state.update(
            status="failed" if error else "done",
            error=error,
            finished_at=now_text(),
            lease_until=None,
        )
        project.youtube_sync = state
        await session.commit()
