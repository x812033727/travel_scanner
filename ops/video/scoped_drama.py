"""One reviewed wedding-competition media request, with isolated in-memory settings.

Run in the API environment with PYTHONPATH=apps/api. Preview is the default and
uses a read-only transaction. --execute needs --expected-manifest-sha (SHA-256
of the exact input bytes), --request, an active administrator with content.manage
AND settings.manage, and real approved VideoReview rows. A paired tool token is
not this authority. This tool never grants approvals or starts workers.

--schema prints the manifest schema without connecting. Artifact paths are relative
to --artifact-root, may not escape it, and are hashed as bytes. Both episode scripts
and measured edits are pinned even when generating one image. Review artifacts are
the actual script.md / characters/manifest.json / keyframes/manifest.json submitted
through the normal review workflow. Missing live reviews are a blocker, not an
invitation to fill in invented IDs. Look and storyboard judging stays in that workflow.

Every invocation executes at most one request/one poll. Use --first-shot with a
pilot clip to test regional/model availability. No model fallback or automatic retry
is allowed. A queued job or reservation without a job is uncertain: reconcile it
before doing anything else. Retakes require changed request bytes, a new reviewed
manifest, retake_of and a reason. Reserves are conservative exposure, NOT invoices;
vendor failure/refund flags never erase them. Keep invoices outside this tool.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import inspect, select, text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.auth.service import effective_admin_capabilities, user_is_suspended
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_automation.models import VideoAutomationSettings, VideoDramaDoc, VideoDramaSeries
from app.video_media import jobs, meter
from app.video_media.catalog import MediaModel, find_model
from app.video_media.models import VideoMediaJob
from app.video_media.schemas import ClipJobIn, ImageJobIn, MusicJobIn

SLUGS = ("wedding-reckoning-competition-e01", "wedding-reckoning-competition-e02")
PILOT_SLUG = "wedding-reckoning-pilot-voice-zh-tw"
SOURCE_SHA = "ef8b5993221a3c065850eb326e7259ea7688457267188b31c2a725aedd2d29f3"
SOURCE_OBJECT_SHA = "37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c"
CAMPAIGN = "wedding-reckoning-competition-20261002"
RESERVED = "video_scoped_drama_reserved"
RESULT = "video_scoped_drama_result"
LOCK_KEY = 2026100201350
SHA = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Slug = Literal["wedding-reckoning-competition-e01", "wedding-reckoning-competition-e02"]
Kind = Literal["image", "clip", "music"]
MODELS = {
    "image": "gemini-3-pro-image",
    "clip": "veo-3.1-lite-generate-preview",
    "music": "lyria-3.5",
}


class Refused(ValueError):
    """A fail-closed preflight or reconciliation requirement, safe to show operators."""


class ScopedSession(AsyncSession):
    """Guard submit_job's final model and dedupe SELECTs against concurrent writes.

    Ordinary HTTP callers do not share this campaign lock. An unexpectedly found
    row must never reach the service's implicit retry/advance branch, and a series
    override changed after preflight must never select an unreviewed image model.
    """

    async def scalar(self, *args: Any, **kwargs: Any) -> Any:
        result = await super().scalar(*args, **kwargs)
        if self.info.get("scoped_drama_new_only"):
            if isinstance(result, VideoMediaJob):
                raise Refused(
                    "another caller created this job; inspect/resume it, never retry here"
                )
            statement = args[0] if args else kwargs.get("statement")
            if (
                any(
                    column.get("expr") is VideoDramaSeries.image_model
                    for column in getattr(statement, "column_descriptions", ())
                )
                and result not in (None, "", MODELS["image"])
            ):
                raise Refused(
                    "series image override changed before submission; inspect reservation"
                )
        return result


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Artifact(Strict):
    path: str = Field(min_length=1)
    sha256: SHA


class Episode(Strict):
    slug: Slug
    script: Artifact
    edit: Artifact


class ReviewEvidence(Strict):
    id: UUID
    gate: Literal["script", "look", "storyboard"]
    artifact: Artifact
    subject: str | None = None


class SeriesEvidence(Strict):
    id: UUID
    kind: Literal["setting", "outline", "chapter"]
    chapter_number: int = Field(ge=0)
    # SHA of canonical JSON {body_md, body_json}; same canonical_hash helper as preview.
    body_sha256: SHA


class Request(Strict):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,59}$")
    kind: Kind
    phase: Literal["pilot", "episodes"]
    payload: dict[str, Any]
    # All on-screen characters, including when Lite accepts no referenceImages.
    characters: list[str] = Field(max_length=12)
    reviews: list[ReviewEvidence] = Field(min_length=1, max_length=20)
    retake_of: UUID | None = None
    retake_reason: str | None = Field(default=None, min_length=1, max_length=500)


class Budget(Strict):
    batch_cap_usd: Literal[350] = 350
    pilot_cap_usd: Literal[100] = 100
    # Voice, judging through normal HTTP, and other off-runner spending. Must be
    # raised before that exposure exceeds it; a later manifest cannot lower it.
    manual_reserve_usd: Decimal = Field(ge=10, le=350, allow_inf_nan=False)


class Manifest(Strict):
    schema_version: Literal[1]
    campaign: Literal["wedding-reckoning-competition-20261002"]
    locale: Literal["zh-TW"]
    source: Artifact
    series_documents: list[SeriesEvidence] = Field(min_length=3, max_length=3)
    episodes: list[Episode] = Field(min_length=2, max_length=2)
    budget: Budget
    requests: list[Request] = Field(min_length=1, max_length=200)

    @model_validator(mode="after")
    def scoped(self) -> Manifest:
        if self.source.sha256 != SOURCE_SHA:
            raise ValueError("source must be the fixed wedding-reckoning source revision")
        if {episode.slug for episode in self.episodes} != set(SLUGS):
            raise ValueError("both exact competition episodes must be pinned")
        if len({request.id for request in self.requests}) != len(self.requests):
            raise ValueError("request IDs must be unique")
        if {(doc.kind, doc.chapter_number) for doc in self.series_documents} != {
            ("setting", 0),
            ("outline", 0),
            ("chapter", 1),
        }:
            raise ValueError("pin the approved setting, outline and first chapter")
        return self


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact_bytes(root: Path, artifact: Artifact) -> bytes:
    relative = Path(artifact.path)
    if relative.is_absolute() or ".." in relative.parts:
        raise Refused("artifact paths must be relative and stay inside artifact-root")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise Refused("artifact is missing or escapes artifact-root")
    data = path.read_bytes()
    if sha256(data) != artifact.sha256:
        raise Refused(f"artifact hash differs: {artifact.path}")
    return data


def read_manifest(raw: bytes, root: Path, expected: str | None, execute: bool) -> Manifest:
    if execute and expected != sha256(raw):
        raise Refused("--execute requires --expected-manifest-sha of the exact input bytes")
    plan = Manifest.model_validate_json(raw)
    artifacts = [plan.source]
    for episode in plan.episodes:
        artifacts.extend((episode.script, episode.edit))
    artifacts.extend(review.artifact for request in plan.requests for review in request.reviews)
    for artifact in artifacts:
        artifact_bytes(root, artifact)
    for episode in plan.episodes:
        edit = json.loads(artifact_bytes(root, episode.edit))
        binding = edit.get("source_binding", {})
        if (
            binding.get("source_object_sha256") != SOURCE_OBJECT_SHA
            or binding.get("screenplay_sha256") != episode.script.sha256
        ):
            raise Refused("measured edit must bind the fixed source and exact episode script")
    return plan


def snapshot(row: VideoAutomationSettings) -> str:
    values = {column.name: getattr(row, column.name) for column in row.__table__.columns}
    return canonical_hash(values)


def canonical_hash(value: Any) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
        ).encode()
    )


async def check_series(session: AsyncSession, plan: Manifest) -> None:
    series = await session.scalar(
        select(VideoDramaSeries)
        .where(VideoDramaSeries.slug == "wedding-reckoning")
        .execution_options(populate_existing=True)
    )
    if series is None or series.kind != "series" or series.status != "active":
        raise Refused("the original wedding-reckoning series must be active, not paused/finished")
    for evidence in plan.series_documents:
        doc = await session.scalar(
            select(VideoDramaDoc)
            .where(
                VideoDramaDoc.series_id == series.id,
                VideoDramaDoc.kind == evidence.kind,
                VideoDramaDoc.chapter_number == evidence.chapter_number,
            )
            .order_by(VideoDramaDoc.version.desc())
            .execution_options(populate_existing=True)
        )
        if (
            doc is None
            or doc.id != evidence.id
            or doc.status != "approved"
            or doc.decided_at is None
            or canonical_hash({"body_md": doc.body_md, "body_json": doc.body_json})
            != evidence.body_sha256
        ):
            raise Refused("original series documents need real current source-bound approvals")
        if (
            doc.kind == "setting"
            and doc.body_json.get("production_design", {})
            .get("source_binding", {})
            .get("source_sha256")
            != SOURCE_OBJECT_SHA
        ):
            raise Refused("approved setting is not bound to the fixed production source")


def isolated_settings(row: VideoAutomationSettings) -> VideoAutomationSettings:
    if row.drama_enabled:
        raise Refused("global drama must remain OFF; this runner cannot isolate a live queue")
    values = {
        column.name: copy.deepcopy(getattr(row, column.name)) for column in row.__table__.columns
    }
    values.update(
        drama_enabled=True,
        drama_aspect="16:9",
        clip_resolution="1080p",
        clip_seconds_default=8,
        image_provider="gemini",
        image_model=MODELS["image"],
        clip_provider="gemini",
        clip_model=MODELS["clip"],
        music_provider="gemini",
        music_model=MODELS["music"],
    )
    clone = VideoAutomationSettings(**values)
    assert inspect(clone).transient
    return clone


async def active_actor(session: AsyncSession, actor_id: UUID) -> User:
    user = await session.scalar(
        select(User).where(User.id == actor_id).execution_options(populate_existing=True)
    )
    if user is None or not user.is_active or user.deleted_at is not None or user_is_suspended(user):
        raise Refused("an active administrator is required")
    capabilities = await effective_admin_capabilities(session, user)
    if not {"admin.access", "content.manage", "settings.manage"} <= capabilities:
        raise Refused("administrator needs content.manage AND settings.manage")
    return user


async def check_reviews(
    session: AsyncSession,
    root: Path,
    request: Request,
    episode: Episode,
    payload: ImageJobIn | ClipJobIn | MusicJobIn,
) -> None:
    project = await session.scalar(
        select(VideoProject)
        .where(VideoProject.slug == episode.slug)
        .execution_options(populate_existing=True)
    )
    if (
        project is None
        or project.format != "drama"
        or project.dropped_at is not None
        or project.series_slug != "wedding-reckoning"
        or project.episode_number != SLUGS.index(episode.slug) + 1
    ):
        raise Refused("a real drama project and its approved reviews are required")
    script_ok = False
    looks: dict[str, str] = {}
    boards: list[dict[str, Any]] = []
    for evidence in request.reviews:
        row = await session.get(VideoReview, evidence.id, populate_existing=True)
        if (
            row is None
            or row.project_id != project.id
            or row.gate != evidence.gate
            or row.subject != evidence.subject
            or row.status != "approved"
            or row.decided_at is None
            or row.content_sha256 != evidence.artifact.sha256
        ):
            raise Refused("review is missing, unapproved, or bound to different content/subject")
        latest = await session.scalar(
            select(VideoReview)
            .where(
                VideoReview.project_id == project.id,
                VideoReview.gate == row.gate,
                VideoReview.subject == row.subject,
            )
            .order_by(
                VideoReview.created_at.desc(), VideoReview.revision.desc(), VideoReview.id.desc()
            )
        )
        if latest is None or latest.id != row.id:
            raise Refused("a newer review exists for this gate/subject; resolve it first")
        data = artifact_bytes(root, evidence.artifact)
        if row.gate == "script":
            if row.subject is not None or evidence.artifact.sha256 != episode.script.sha256:
                raise Refused("script approval does not match this episode script")
            script_ok = True
        elif row.gate == "look":
            options = row.payload.get("options", [])
            option = next((item for item in options if item.get("key") == row.choice), None)
            if not isinstance(option, dict):
                raise Refused("look approval must select an existing reviewed option")
            chosen = next(
                (
                    item
                    for item in row.files
                    if option and item.get("role") == option.get("file_role")
                ),
                None,
            )
            characters = json.loads(data).get("characters", {})
            candidates = characters.get(row.subject, {}).get("candidates", [])
            if (
                not row.subject
                or not chosen
                or not any(
                    item.get("sha256") == chosen["sha256"] and item.get("n") == option.get("index")
                    for item in candidates
                )
            ):
                raise Refused("look approval must select its actual reviewed candidate")
            looks[row.subject] = str(chosen["sha256"])
        else:
            if row.subject is not None:
                raise Refused("storyboard review may not have a subject")
            board = json.loads(data)
            board["_review_shots"] = row.payload.get("shots", [])
            boards.append(board)
    if not script_ok:
        raise Refused("a current script approval is required before paid media")
    needs_look = isinstance(payload, ClipJobIn) or (
        isinstance(payload, ImageJobIn) and payload.purpose in ("keyframe", "thumbnail")
    )
    if needs_look and not set(request.characters) <= looks.keys():
        raise Refused("every on-screen character needs its current selected look approval")
    if isinstance(payload, ImageJobIn) and payload.references:
        if any(reference.sha256 not in looks.values() for reference in payload.references):
            raise Refused("image references must be the selected approved look candidates")
    if isinstance(payload, ClipJobIn):
        matching = [(board.get("shots", {}).get(payload.shot_id), board) for board in boards]
        if not any(
            isinstance(shot, dict)
            and shot.get("sha256") == payload.first_frame
            and shot.get("needs_review") is False
            and not shot.get("incomplete")
            and any(
                item.get("id") == payload.shot_id and item.get("needs_review") is False
                for item in board["_review_shots"]
            )
            and (
                not payload.last_frame
                or shot.get("end_frame", {}).get("sha256") == payload.last_frame
            )
            for shot, board in matching
        ):
            raise Refused("clip frames/shot must match an approved, complete storyboard")


@dataclass
class Prepared:
    request: Request
    payload: ImageJobIn | ClipJobIn | MusicJobIn
    model: MediaModel
    digest: str
    cost: Decimal
    existing: VideoMediaJob | None


def check_shot(
    root: Path, episode: Episode, request: Request, payload: ImageJobIn | ClipJobIn | MusicJobIn
) -> None:
    if not (
        isinstance(payload, ClipJobIn)
        or isinstance(payload, ImageJobIn)
        and payload.purpose in ("keyframe", "thumbnail")
    ):
        return
    edit = json.loads(artifact_bytes(root, episode.edit))
    matches = [shot for shot in edit.get("shots", []) if shot.get("scene_id") == payload.shot_id]
    if len(matches) != 1:
        raise Refused("request shot_id must identify one scene in the measured edit")
    data = matches[0].get("data", {})
    if not isinstance(data.get("characters"), list) or sorted(data["characters"]) != sorted(
        request.characters
    ):
        raise Refused("request cast must match the measured edit's complete on-screen cast")
    prompt = data.get("motion") if isinstance(payload, ClipJobIn) else data.get("prompt")
    camera = data.get("camera")
    if (
        not isinstance(prompt, str)
        or not prompt
        or not payload.prompt.startswith(prompt)
        or not isinstance(camera, str)
        or not camera
        or camera not in payload.prompt
    ):
        raise Refused("request prompt/motion and camera must match its reviewed edit shot")


async def prepare(
    ctx: jobs.MediaContext, plan: Manifest, root: Path, request_id: str, first_shot: bool
) -> Prepared:
    request = next((item for item in plan.requests if item.id == request_id), None)
    if request is None:
        raise Refused("--request must name exactly one manifest request")
    payload: ImageJobIn | ClipJobIn | MusicJobIn
    if request.kind == "image":
        payload = ImageJobIn.model_validate(request.payload)
    elif request.kind == "clip":
        payload = ClipJobIn.model_validate(request.payload)
    else:
        payload = MusicJobIn.model_validate(request.payload)
    if payload.slug not in SLUGS:
        raise Refused("request slug is outside the two authorized episodes")
    if request.phase == "pilot" and payload.slug != SLUGS[0]:
        raise Refused("the pilot belongs to episode 01")
    if first_shot and (request.kind != "clip" or request.phase != "pilot"):
        raise Refused("--first-shot requires one pilot clip")
    if isinstance(payload, ClipJobIn) and (
        payload.seconds != 8 or payload.resolution != "1080p" or payload.references
    ):
        raise Refused("Veo Lite requires 1080p, 8 seconds, and no referenceImages")
    if isinstance(payload, ImageJobIn) and (payload.aspect != "16:9" or not payload.shot_id):
        raise Refused("images require 16:9 and a stable shot_id (also for character sheets)")
    if request.kind == "music" and not ctx.row.music_enabled:
        raise Refused("music must already be enabled")
    if request.kind == "image":
        override = await jobs.series_image_model(ctx.session, payload.slug)
        if override and override != MODELS["image"]:
            raise Refused("series image override conflicts with the reviewed model")
    model = find_model("gemini", request.kind, MODELS[request.kind])
    if model is None or model.status == "retired":
        raise Refused("the pinned model is absent/retired; no fallback is permitted")
    fields = jobs._request_fields(payload, ctx.row, model)
    jobs._check_references(ctx.store, payload.slug, fields["references"])
    for reference in fields["references"]:
        path = ctx.store.path(payload.slug, reference["sha256"])
        if path is None or sha256(path.read_bytes()) != reference["sha256"]:
            raise Refused("media-store reference bytes differ from the reviewed hash")
    episode = next(item for item in plan.episodes if item.slug == payload.slug)
    check_shot(root, episode, request, payload)
    await check_reviews(ctx.session, root, request, episode, payload)
    digest = jobs.request_hash(
        {"kind": request.kind, "vendor": "gemini", "model": model.id, **fields}
    )
    existing = await ctx.session.scalar(
        select(VideoMediaJob).where(
            VideoMediaJob.slug == payload.slug, VideoMediaJob.request_hash == digest
        )
    )
    return Prepared(
        request,
        payload,
        model,
        digest,
        meter.usd_for(model, request.kind, int(fields.get("seconds") or 0)),
        existing,
    )


def money(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value))
    except Exception as error:
        raise Refused("invalid persisted cost; reconcile the ledger") from error
    if not amount.is_finite() or amount < 0:
        raise Refused("invalid persisted cost; reconcile the ledger")
    return amount


async def exposure(
    session: AsyncSession, manual: Decimal
) -> tuple[Decimal, Decimal, dict[tuple[str, str], dict[str, Any]]]:
    reserves: dict[tuple[str, str], dict[str, Any]] = {}
    costs: dict[tuple[str, str], Decimal] = {}
    phases: dict[tuple[str, str], str] = {}
    for audit in await session.scalars(
        select(AdminAuditLog).where(
            AdminAuditLog.action == RESERVED, AdminAuditLog.target == CAMPAIGN
        )
    ):
        entry = audit.metadata_json
        try:
            key = (entry["slug"], entry["request_sha256"])
            if (
                entry["schema_version"] != 1
                or key[0] not in SLUGS
                or entry["phase"] not in ("pilot", "episodes")
            ):
                raise KeyError("invalid reservation identity")
            manual = max(manual, money(entry["manual_reserve_usd"]))
            costs[key] = max(costs.get(key, Decimal(0)), money(entry["reserved_usd"]))
            if key in reserves:
                raise Refused("duplicate durable reservation; reconcile before proceeding")
            reserves[key] = entry
            phases[key] = entry["phase"]
        except (KeyError, TypeError) as error:
            raise Refused("invalid persisted reservation; reconcile the ledger") from error
    for job in await session.scalars(
        select(VideoMediaJob).where(VideoMediaJob.slug.in_((*SLUGS, PILOT_SLUG)))
    ):
        model = find_model(job.provider, job.kind, job.model)  # type: ignore[arg-type]
        if model is None or job.attempts < 1:
            raise Refused("unpriced prior media attempt; reconcile before proceeding")
        key = (job.slug, job.request_hash)
        # Failures retain full catalog exposure even if service refund reset usd_estimate.
        cost = max(money(job.usd_estimate), meter.usd_for(model, job.kind, job.seconds))
        costs[key] = max(costs.get(key, Decimal(0)), cost * job.attempts)
        # Any untracked historical job is conservatively charged to the pilot as well.
        phases.setdefault(key, "pilot")
    total = manual + sum(costs.values(), Decimal(0))
    pilot = manual + sum(
        (cost for key, cost in costs.items() if phases[key] == "pilot"), Decimal(0)
    )
    return total, pilot, reserves


async def check_retake(session: AsyncSession, prepared: Prepared, digest: str) -> None:
    request, payload = prepared.request, prepared.payload
    shot = getattr(payload, "shot_id", None)
    previous = list(
        await session.scalars(
            select(VideoMediaJob).where(
                VideoMediaJob.slug == payload.slug,
                VideoMediaJob.kind == request.kind,
                VideoMediaJob.shot_id == shot,
                VideoMediaJob.request_hash != prepared.digest,
            )
        )
    )
    if not previous and request.retake_of is None:
        return
    target = next((job for job in previous if job.id == request.retake_of), None)
    if (
        target is None
        or not request.retake_reason
        or any(job.status not in ("ready", "failed", "expired") for job in previous)
    ):
        raise Refused("retake requires explicit prior terminal job and reason; pending blocks it")
    # A retake must originate in this runner's durable, differently reviewed manifest.
    audits = list(
        await session.scalars(
            select(AdminAuditLog).where(
                AdminAuditLog.action == RESERVED, AdminAuditLog.target == CAMPAIGN
            )
        )
    )
    if not any(
        entry.metadata_json.get("slug") == payload.slug
        and entry.metadata_json.get("request_sha256") == target.request_hash
        and entry.metadata_json.get("manifest_sha256") != digest
        for entry in audits
    ):
        raise Refused("retake requires a new reviewed manifest and known prior reservation")


async def run_request(
    ctx: jobs.MediaContext,
    raw: bytes,
    root: Path,
    request_id: str,
    *,
    actor_id: UUID,
    execute: bool = False,
    expected: str | None = None,
    first_shot: bool = False,
) -> dict[str, Any]:
    """Caller owns the campaign advisory lock for execution, never an HTTP route."""
    if execute and (
        not isinstance(ctx.session, ScopedSession) or not ctx.session.info.get("scoped_drama_lock")
    ):
        raise Refused("execution requires the dedicated-connection campaign lock")
    plan = read_manifest(raw, root, expected, execute)
    actor = await active_actor(ctx.session, actor_id)
    global_row = await ctx.session.scalar(
        select(VideoAutomationSettings)
        .where(VideoAutomationSettings.id == 1)
        .execution_options(populate_existing=True)
    )
    if global_row is None:
        raise Refused("existing video settings are required; preview never initializes them")
    before = snapshot(global_row)
    ctx.row = isolated_settings(global_row)
    await check_series(ctx.session, plan)
    prepared = await prepare(ctx, plan, root, request_id, first_shot)
    request, payload, existing = prepared.request, prepared.payload, prepared.existing
    total, pilot, reserves = await exposure(ctx.session, plan.budget.manual_reserve_usd)
    key = (payload.slug, prepared.digest)
    prior_jobs = list(
        await ctx.session.scalars(select(VideoMediaJob).where(VideoMediaJob.slug.in_(SLUGS)))
    )
    known = {(job.slug, job.request_hash) for job in prior_jobs}
    if existing is None and (
        reserves.keys() - known or any(job.status in ("queued", "submitted") for job in prior_jobs)
    ):
        raise Refused("campaign has unknown/pending operations: reconcile or resume them first")
    if existing is None and key in reserves:
        raise Refused("reservation has no job: unknown vendor result; reconcile, never resubmit")
    if (
        existing is not None
        and existing.status != "ready"
        and not (existing.status == "submitted" and existing.vendor_ref)
    ):
        raise Refused("existing job is failed/expired/unknown; never resubmit this request")
    additional = prepared.cost if existing is None else Decimal(0)
    if existing is None and (
        total + additional > 350 or (request.phase == "pilot" and pilot + additional > 100)
    ):
        raise Refused("conservative exposure exceeds the USD 350 batch / USD 100 pilot cap")
    if existing is None:
        await check_retake(ctx.session, prepared, sha256(raw))
    report: dict[str, Any] = {
        "execute": execute,
        "manifest_sha256": sha256(raw),
        "request": request.id,
        "request_sha256": prepared.digest,
        "slug": payload.slug,
        "provider": "gemini",
        "model": prepared.model.id,
        "settings_before_sha256": before,
        "settings_after_sha256": before,
        "global_drama_enabled": False,
        "scope": "one request or one poll; workers untouched",
        "batch_exposure_usd": str(total + additional),
        "pilot_exposure_usd": str(pilot + (additional if request.phase == "pilot" else 0)),
        "new_reserve_usd": str(additional),
        "cost_basis": "conservative reserve, not actual bill",
        "actual_billed_usd": None,
        "operation": "return_ready"
        if existing and existing.status == "ready"
        else "resume_poll"
        if existing
        else "submit_once",
        "job_id": str(existing.id) if existing else None,
    }
    if existing is not None:
        report.update(
            status=existing.status,
            file_sha256=existing.file_sha256,
            attempts=existing.attempts,
            vendor_operation_recorded=bool(existing.vendor_ref),
        )
    if not execute or (existing is not None and existing.status == "ready"):
        return report
    if not jobs.key_for(ctx.runtime, "gemini"):
        raise Refused("the pinned provider is not configured; no credential may be supplied here")
    # Recheck live roles immediately before the durable paid-operation intent.
    await active_actor(ctx.session, actor.id)
    if existing is None:
        metadata = {
            "schema_version": 1,
            "manifest_sha256": sha256(raw),
            "request_id": request.id,
            "slug": payload.slug,
            "request_sha256": prepared.digest,
            "phase": request.phase,
            "reserved_usd": str(prepared.cost),
            "manual_reserve_usd": str(plan.budget.manual_reserve_usd),
            "settings_sha256": before,
            "provider": "gemini",
            "model": prepared.model.id,
            "source": plan.source.model_dump(),
            "series_documents": [doc.model_dump(mode="json") for doc in plan.series_documents],
            "episodes": [episode.model_dump() for episode in plan.episodes],
            "reviews": [review.model_dump(mode="json") for review in request.reviews],
            "retake_of": str(request.retake_of) if request.retake_of else None,
            "retake_reason": request.retake_reason,
        }
        ctx.session.add(
            AdminAuditLog(
                actor_user_id=actor.id, action=RESERVED, target=CAMPAIGN, metadata_json=metadata
            )
        )
        await ctx.session.commit()  # Survives provider exceptions and process loss.
        read_manifest(raw, root, expected, True)
        await active_actor(ctx.session, actor.id)
        await check_series(ctx.session, plan)
        episode = next(item for item in plan.episodes if item.slug == payload.slug)
        await check_reviews(ctx.session, root, request, episode, payload)
        current = await ctx.session.scalar(
            select(VideoAutomationSettings)
            .where(VideoAutomationSettings.id == 1)
            .execution_options(populate_existing=True)
        )
        if current is None or snapshot(current) != before:
            raise Refused("settings changed before submission; inspect the durable reservation")
        ctx.session.info["scoped_drama_new_only"] = True
        try:
            job, _ = await jobs.submit_job(ctx, request.kind, payload)
        finally:
            ctx.session.info.pop("scoped_drama_new_only", None)
    else:
        job = await jobs.advance_job(ctx, existing)  # submitted + vendor_ref only; never queued
    after = await ctx.session.scalar(
        select(VideoAutomationSettings)
        .where(VideoAutomationSettings.id == 1)
        .execution_options(populate_existing=True)
    )
    report.update(
        job_id=str(job.id),
        status=job.status,
        vendor_operation_recorded=bool(job.vendor_ref),
        attempts=job.attempts,
        file_sha256=job.file_sha256,
        error_code=job.error_code,
    )
    report["settings_after_sha256"] = snapshot(after) if after is not None else None
    ctx.session.add(
        AdminAuditLog(actor_user_id=actor.id, action=RESULT, target=CAMPAIGN, metadata_json=report)
    )
    await ctx.session.commit()
    if report["settings_after_sha256"] != before:
        raise Refused("global settings changed concurrently; stop and inspect the recorded result")
    return report


@asynccontextmanager
async def campaign_lock(connection: AsyncConnection) -> AsyncIterator[None]:
    if connection.dialect.name != "postgresql":
        raise Refused("execution requires PostgreSQL advisory locking")
    locked = await connection.scalar(text("SELECT pg_try_advisory_lock(:key)"), {"key": LOCK_KEY})
    await connection.commit()
    if not locked:
        raise Refused("another campaign operation holds the lock")
    try:
        yield
    finally:
        await connection.rollback()
        try:
            await connection.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": LOCK_KEY})
            await connection.commit()
        except BaseException:
            await connection.invalidate()  # Never return a still-locked connection to the pool.
            raise


async def invoke(args: argparse.Namespace, raw: bytes) -> dict[str, Any]:
    read_manifest(raw, args.artifact_root, args.expected_manifest_sha, args.execute)
    from app.admin.service import load_runtime_settings
    from app.config import get_settings
    from app.db import engine
    from app.infra import get_redis
    from app.video_media.admin_api import media_store
    from app.video_media.settings import get_media_settings

    async def call(connection: AsyncConnection, locked: bool) -> dict[str, Any]:
        async with ScopedSession(bind=connection, expire_on_commit=False) as session:
            if not locked:
                await session.execute(text("SET TRANSACTION READ ONLY"))
            session.info["scoped_drama_lock"] = locked
            email = args.actor_email
            if not email:
                emails = sorted(get_settings().admin_email_set)
                if len(emails) != 1:
                    raise Refused("select an authorized administrator with --actor-email")
                email = emails[0]
            actor = await session.scalar(select(User).where(User.email == email.strip().lower()))
            if actor is None:
                raise Refused("an existing authorized administrator is required")
            media = get_media_settings()
            ctx = jobs.MediaContext(
                session=session,
                redis=get_redis(),
                store=media_store(media),
                runtime=await load_runtime_settings(session),
                media=media,
                row=VideoAutomationSettings(),
            )
            return await run_request(
                ctx,
                raw,
                args.artifact_root,
                args.request,
                actor_id=actor.id,
                execute=args.execute,
                expected=args.expected_manifest_sha,
                first_shot=args.first_shot,
            )

    try:
        async with engine.connect() as connection:
            if args.execute:
                async with campaign_lock(connection):
                    return await call(connection, True)
            return await call(connection, False)
    finally:
        await engine.dispose()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--schema", action="store_true")
    result.add_argument("--input", type=Path)
    result.add_argument("--artifact-root", type=Path)
    result.add_argument("--request")
    result.add_argument("--execute", action="store_true")
    result.add_argument("--expected-manifest-sha")
    result.add_argument("--actor-email")
    result.add_argument("--first-shot", action="store_true")
    return result


def main() -> None:
    cli = parser()
    args = cli.parse_args()
    if args.schema:
        print(json.dumps(Manifest.model_json_schema(), ensure_ascii=False, indent=2))
        return
    if args.input is None or args.artifact_root is None or args.request is None:
        cli.error("--input, --artifact-root and --request are required")
    try:
        print(json.dumps(asyncio.run(invoke(args, args.input.read_bytes())), indent=2))
    except Exception as error:
        # Do not echo pydantic input values or provider/network exception text (secrets).
        message = str(error) if isinstance(error, Refused) else type(error).__name__
        cli.exit(1, f"Scoped drama refused: {message}\n")


if __name__ == "__main__":
    main()
