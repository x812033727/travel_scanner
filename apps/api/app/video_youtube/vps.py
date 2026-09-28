"""Bridge to the independent Studio uploader. No Google credentials or YouTube API calls.

Each staging request forwards at most one 4 MiB chunk from the approved local package.
The service owns durable jobs; once queued it works without the website/browser staying open.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import Settings
from app.models import User, VideoProject
from app.video_reviews import admin_service as reviews
from app.video_reviews.storage import ReviewStore, valid_slug
from app.video_youtube import sync
from app.video_youtube.errors import Refused
from app.video_youtube.requests import text_problem
from app.video_youtube.state import running

CHUNK = 4 * 1024 * 1024
ACTIVE = {"staging", "queued", "running", "needs_action"}
HASH = re.compile(r"^[a-f0-9]{64}$")
CHANNEL = re.compile(r"^UC[A-Za-z0-9_-]{22}$")


class StartIn(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    url: str | None = Field(default=None, max_length=500)


class ResumeIn(BaseModel):
    url: str | None = Field(default=None, max_length=500)


@dataclass(frozen=True)
class Config:
    url: str
    secret: str
    channel: str


def config() -> Config | None:
    """Operator-owned deployment config; never returned to the browser or written to logs."""
    url = os.getenv("MOKAAIR_VPS_UPLOADER_URL", "").rstrip("/")
    if not url:
        return None
    parsed = urlsplit(url)
    channel = os.getenv("MOKAAIR_VPS_UPLOADER_CHANNEL_ID", "")
    try:
        secret = Path(os.environ["MOKAAIR_VPS_UPLOADER_SECRET_FILE"]).read_text().strip()
    except (KeyError, OSError):
        raise Refused(503, "vps_not_configured", "VPS 上傳服務尚未完成設定") from None
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path
        or len(secret) < 32
        or not CHANNEL.fullmatch(channel)
    ):
        raise Refused(503, "vps_not_configured", "VPS 上傳服務設定不完整")
    return Config(url, secret, channel)


def http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=25, follow_redirects=False)


async def remote(method: str, route: str, **kwargs: Any) -> dict[str, Any]:
    settings = config()
    if settings is None:
        raise Refused(503, "vps_not_configured", "VPS 上傳服務尚未啟用")
    try:
        async with http_client() as client:
            response = await client.request(
                method,
                settings.url + route,
                headers={"Authorization": f"Bearer {settings.secret}"},
                **kwargs,
            )
        if len(response.content) > 100_000:
            raise ValueError("oversized response")
        value = response.json()
        if not isinstance(value, dict):
            raise ValueError("invalid response")
        if not response.is_success:
            # Upstream text can contain operational details; only report bounded known codes.
            code = str(value.get("code", ""))
            messages = {
                "request_changed": "這份上傳包已有不同設定的工作，請先完成或取消原工作",
                "project_busy": "這支影片已有 VPS 工作，請查看進度或繼續原工作",
                "video_id_required": "上次可能已建立影片，請先在 Studio 核對並貼上影片網址",
                "existing_video_required": "VPS 已有這支影片的連結，請先記錄上傳結果",
                "file_hash_mismatch": "檔案內容與核准的雜湊不符，請重新確認上傳包",
                "files_incomplete": "檔案尚未完整送到 VPS，請繼續傳送",
                "private_required": "請先確認 Studio 的影片為私人",
            }
            raise Refused(
                409 if response.status_code == 409 else 502,
                "vps_request_refused",
                messages.get(code, "VPS 未接受這次操作，請重新整理進度後再試"),
            )
        return value
    except Refused:
        raise
    except (httpx.HTTPError, ValueError, TypeError):
        raise Refused(503, "vps_unavailable", "暫時無法連線到 VPS，工作紀錄會保留") from None


async def latest(slug: str) -> dict[str, Any] | None:
    if not valid_slug(slug):
        raise Refused(422, "vps_invalid_slug", "影片識別資料不正確")
    settings = config()
    value = (await remote("GET", f"/projects/{slug}")).get("job")
    if value is not None and not isinstance(value, dict):
        raise Refused(502, "vps_invalid_response", "VPS 回覆格式不正確")
    if value and (
        value.get("slug") != slug
        or value.get("channel_id") != (settings.channel if settings else None)
        or not HASH.fullmatch(str(value.get("id", "")))
        or not HASH.fullmatch(str(value.get("review_sha256", "")))
    ):
        raise Refused(502, "vps_invalid_response", "VPS 回覆與影片不符")
    return value


async def assert_idle(slug: str, *, upload: bool = False) -> None:
    """Called under the project row lock by the existing API sender as well."""
    if config() is None:
        return
    job = await latest(slug)
    if job and (job.get("state") in ACTIVE or (upload and job.get("video_id"))):
        raise Refused(409, "vps_job_exists", "這支影片已有 VPS 工作，請先查看或記錄它的結果")


async def status(session: AsyncSession, slug: str) -> dict[str, Any]:
    project = await reviews.project_view(session, slug)
    settings = config()
    if settings is None:
        return {"configured": False, "job": None, "linked": False}
    job = await latest(slug)
    return {
        "configured": True,
        "job": job,
        "linked": bool(job and job.get("video_id") and job["video_id"] == project.youtube_video_id),
    }


async def package(session: AsyncSession, slug: str) -> tuple[Settings, ReviewStore, sync.Package]:
    runtime = await load_runtime_settings(session)
    store = reviews.review_store(runtime)
    # The caller already holds the project's row lock for mutations.
    project = await sync._locked_project(session, slug)
    review = sync.approved_confirmation(await sync._project_reviews(session, project))
    if review is None:
        raise Refused(409, "vps_not_ready", "這支影片還沒有已核准的上傳包")
    return runtime, store, sync.read_package(store, slug, review)


async def assets(
    session: AsyncSession,
    slug: str,
    pack: sync.Package,
    runtime: Settings,
    store: ReviewStore,
    *,
    need_video: bool,
) -> list[tuple[dict[str, Any], Path]]:
    result: list[tuple[dict[str, Any], Path]] = []
    entries = {f"captions_{locale}": value for locale, value in pack.captions.items()}
    if pack.thumbnail:
        entries["thumbnail"] = pack.thumbnail
    if need_video and pack.final:
        entries["final"] = pack.final
    for role, item in entries.items():
        file = store.path(slug, item.sha256)
        if file is None or file.stat().st_size != item.size:
            raise Refused(409, "vps_file_missing", "核准的檔案不在審核區，請重新產生上傳包")
        result.append(
            (
                {
                    "role": role,
                    "sha256": item.sha256,
                    "size": item.size,
                    "content_type": item.content_type,
                },
                file,
            )
        )
    if need_video and not pack.final:
        sha = str(pack.metadata.get("final_sha256", ""))
        if not pack.metadata.get("compilation") or not HASH.fullmatch(sha):
            raise Refused(409, "vps_video_missing", "沒有核准的完整影片可送到 VPS")
        file = await reviews.download_path(session, runtime.video_work_dir, slug)
        result.append(
            (
                {
                    "role": "final",
                    "sha256": sha,
                    "size": file.stat().st_size,
                    "content_type": "video/mp4",
                },
                file,
            )
        )
    return result


async def start(session: AsyncSession, slug: str, user: User, payload: StartIn) -> dict[str, Any]:
    settings = config()
    if settings is None:
        raise Refused(503, "vps_not_configured", "VPS 上傳服務尚未啟用")
    project = await sync._locked_project(session, slug)
    if running(project.youtube_sync):
        raise Refused(409, "vps_api_running", "API 同步還在進行，請等它停止")
    runtime, store, pack = await package(session, slug)
    old = await latest(slug)
    if old and old.get("state") in ACTIVE:
        if old.get("review_sha256") != pack.sha256:
            raise Refused(409, "vps_package_changed", "舊版 VPS 工作尚未結束，請先處理原工作")
        return {
            "configured": True,
            "job": old,
            "linked": bool(old.get("video_id") and old["video_id"] == project.youtube_video_id),
        }
    if old and old.get("state") == "done" and old.get("review_sha256") == pack.sha256:
        return {
            "configured": True,
            "job": old,
            "linked": bool(old.get("video_id") and old["video_id"] == project.youtube_video_id),
        }
    supplied_id = reviews.youtube_video_id(payload.url or "")
    if payload.url and not supplied_id:
        raise Refused(422, "vps_video_invalid", "請貼上有效的 YouTube 影片網址")
    known_id = project.youtube_video_id or (old or {}).get("video_id")
    if known_id and supplied_id and known_id != supplied_id:
        raise Refused(409, "vps_video_changed", "影片網址與已記錄的影片不同")
    video_id = known_id or supplied_id
    if not video_id and project.youtube_upload_session:
        raise Refused(
            409,
            "vps_video_uncertain",
            "API 曾開始上傳，請先到 Studio 核對並貼上原影片網址，避免重複上傳",
        )
    m = dict(pack.metadata)
    title = payload.title if payload.title is not None else m.get("title", "")
    description = (
        payload.description if payload.description is not None else m.get("description", "")
    )
    problem = text_problem(title, description)
    if problem:
        raise Refused(422, "vps_text_invalid", problem)
    if not isinstance(m.get("made_for_kids"), bool) or not isinstance(
        m.get("contains_synthetic_media"), bool
    ):
        raise Refused(422, "vps_settings_missing", "上傳包必須明確指定目標觀眾與合成內容設定")
    files = await assets(session, slug, pack, runtime, store, need_video=not video_id)
    localizations = m.get("localizations", {})
    if not isinstance(localizations, dict):
        raise Refused(422, "vps_settings_missing", "上傳包的翻譯文字格式不正確")
    metadata = {
        "title": title,
        "description": description,
        "tags": m.get("tags", []),
        "default_language": m.get("default_language", "zh-TW"),
        "category_id": str(m.get("category_id", "")),
        "made_for_kids": m["made_for_kids"],
        "contains_synthetic_media": m["contains_synthetic_media"],
        "localizations": {
            locale: entry
            for locale, entry in localizations.items()
            if locale != m.get("default_language", "zh-TW")
        },
    }
    key = hashlib.sha256(f"{slug}:{pack.sha256}".encode()).hexdigest()
    job = await remote(
        "PUT",
        f"/jobs/{key}",
        json={
            "version": 1,
            "slug": slug,
            "review_sha256": pack.sha256,
            "channel_id": settings.channel,
            "video_id": video_id,
            "metadata": metadata,
            "files": [entry for entry, _ in files],
        },
    )
    sync._audit(session, user, "video_vps_requested", slug, job_id=key, package_sha256=pack.sha256)
    await session.commit()
    return {"configured": True, "job": job, "linked": False}


async def current_job(session: AsyncSession, slug: str) -> tuple[VideoProject, dict[str, Any]]:
    project = await sync._locked_project(session, slug)
    if running(project.youtube_sync):
        raise Refused(409, "vps_api_running", "API 同步還在進行，請等它停止")
    job = await latest(slug)
    if not job:
        raise Refused(404, "vps_job_missing", "這支影片尚未建立 VPS 工作")
    return project, job


def read_chunk(file: Path, offset: int) -> bytes:
    with file.open("rb") as stream:
        stream.seek(offset)
        return stream.read(CHUNK)


async def stage(session: AsyncSession, slug: str) -> dict[str, Any]:
    _, job = await current_job(session, slug)
    if job.get("state") != "staging":
        return {"configured": True, "job": job, "linked": False}
    runtime, store, pack = await package(session, slug)
    if job["review_sha256"] != pack.sha256:
        raise Refused(409, "vps_package_changed", "核准的上傳包已變更，請先取消舊工作")
    sources = await assets(session, slug, pack, runtime, store, need_video=not job.get("video_id"))
    for entry in job.get("files", []):
        source = next(
            (
                file
                for info, file in sources
                if all(
                    info.get(key) == entry.get(key)
                    for key in ("role", "sha256", "size", "content_type")
                )
            ),
            None,
        )
        if source is None:
            raise Refused(409, "vps_files_changed", "VPS 工作與已核准檔案不一致")
        offset = entry.get("received")
        if not isinstance(offset, int) or offset < 0 or offset > entry["size"]:
            raise Refused(502, "vps_invalid_progress", "VPS 檔案進度不正確")
        if offset < entry["size"]:
            job = await remote(
                "PUT",
                f"/jobs/{job['id']}/files/{entry['sha256']}?offset={offset}",
                content=read_chunk(source, offset),
            )
            return {"configured": True, "job": job, "linked": False}
    job = await remote("POST", f"/jobs/{job['id']}/queue")
    return {"configured": True, "job": job, "linked": False}


async def action(
    session: AsyncSession,
    slug: str,
    user: User,
    name: str,
    payload: ResumeIn,
) -> dict[str, Any]:
    project, job = await current_job(session, slug)
    if name == "record":
        video_id = reviews.youtube_video_id(str(job.get("video_id") or ""))
        if job.get("state") != "done" or not video_id:
            raise Refused(409, "vps_not_done", "VPS 還沒有確認上傳完成")
        if project.youtube_video_id not in (None, video_id):
            raise Refused(409, "vps_video_changed", "結果與網站已記錄的影片不同")
        _, _, pack = await package(session, slug)
        if job["review_sha256"] != pack.sha256:
            raise Refused(409, "vps_package_changed", "結果來自舊版上傳包，請先人工核對")
        if project.youtube_video_id is None:
            await reviews.link_youtube(session, slug, user, video_id, None)
        return {"configured": True, "job": job, "linked": True}
    if name not in {"resume", "cancel"}:
        raise Refused(404, "vps_action_missing", "找不到這個操作")
    video_id = reviews.youtube_video_id(payload.url or "")
    if payload.url and not video_id:
        raise Refused(422, "vps_video_invalid", "請貼上有效的 YouTube 影片網址")
    if name == "resume":
        _, _, pack = await package(session, slug)
        if job["review_sha256"] != pack.sha256:
            raise Refused(409, "vps_package_changed", "上傳包已變更，請先處理原工作")
    result = await remote("POST", f"/jobs/{job['id']}/{name}", json={"video_id": video_id})
    sync._audit(session, user, f"video_vps_{name}", slug, job_id=job["id"])
    await session.commit()
    return {"configured": True, "job": result, "linked": False}
