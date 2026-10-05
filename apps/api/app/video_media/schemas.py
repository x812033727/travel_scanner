"""Request and response shapes of ``/video/media`` (docs/videos/DRAMA.md).

The tool side (tools/video/media, ticket 2026-09-26-video-drama-media-client) is written to
these: a job is submitted, polled by id until ``ready``, and its file fetched by SHA-256.
Reference images are always files already in the media store, named by their SHA-256, never
bytes in the request.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.video_automation.schemas import MediaOptionsView, MediaProvider
from app.video_reviews.schemas import SHA256_PATTERN

JobKind = Literal["image", "clip", "music"]
JobStatus = Literal["queued", "submitted", "ready", "failed", "expired"]
ImagePurpose = Literal["character_sheet", "style_frame", "keyframe", "thumbnail"]
ReferenceRole = Literal["character", "style", "previous_frame"]
Aspect = Literal["16:9", "9:16", "1:1"]
# The size a picture is asked at: the vendors' 1K default, or 2K for a still that fills the
# frame under a camera move (docs/videos/ILLUSTRATED.md); priced with the model's 2K price.
ImageSize = Literal["1K", "2K"]
JudgeKind = Literal["look", "keyframe", "clip", "continuity"]
# Stock photo sources (stock.py, docs/videos/ILLUSTRATED.md §圖庫照片): real photographs under
# licences that allow commercial use, searched and fetched by the server with its own keys.
StockProvider = Literal["pexels", "pixabay"]
StockOrientation = Literal["landscape", "portrait", "square"]
SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"
SHOT_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
# Both vendors number their photos; the id is sent back to them in a URL or a query.
STOCK_ID_PATTERN = r"^[0-9]{1,20}$"
MAX_REFERENCES = 4
MAX_PROMPT_CHARS = 4000
MAX_CONTEXT_BYTES = 64 * 1024
MAX_JUDGE_FILES = 6
MAX_RUBRIC = 12
MAX_LOCATE_LABELS = 8
# Pixabay caps a query at 100 characters; Pexels takes up to 80 results a page, Pixabay 200.
MAX_STOCK_QUERY_CHARS = 100
MAX_STOCK_PER_PAGE = 40


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Reference(StrictModel):
    sha256: str = Field(pattern=SHA256_PATTERN)
    # character: a chosen character sheet; style: a style frame; previous_frame: the last frame
    # of the shot before, for a clip that continues its action.
    role: ReferenceRole = "character"


class _JobIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)
    prompt: str = Field(min_length=1, max_length=MAX_PROMPT_CHARS)
    negative_prompt: str | None = Field(default=None, max_length=1000)
    seed: int | None = Field(default=None, ge=0, le=2_147_483_647)
    # The tool's own cache key, kept for the logs; the request hash is what dedupes.
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=80)


class ImageJobIn(_JobIn):
    purpose: ImagePurpose
    aspect: Aspect = "16:9"
    references: list[Reference] = Field(default_factory=list, max_length=MAX_REFERENCES)
    shot_id: str | None = Field(default=None, pattern=SHOT_PATTERN, max_length=60)
    # 2K is refused for a model the catalog prices at 1K only.
    size: ImageSize | None = None


class ClipJobIn(_JobIn):
    shot_id: str = Field(pattern=SHOT_PATTERN, max_length=60)
    first_frame: str = Field(pattern=SHA256_PATTERN)
    last_frame: str | None = Field(default=None, pattern=SHA256_PATTERN)
    references: list[Reference] = Field(default_factory=list, max_length=MAX_REFERENCES)
    seconds: int = Field(ge=3, le=15)
    # Defaults to the settings row's clip_resolution.
    resolution: str | None = Field(default=None, pattern=r"^(?:\d{3,4}p|2k|4k)$")
    native_audio: bool = False


class MusicJobIn(_JobIn):
    seconds: int = Field(ge=10, le=600)


class JobFile(StrictModel):
    sha256: str
    size: int
    content_type: str


class JobError(StrictModel):
    code: str
    detail: str


class JobOut(StrictModel):
    id: UUID
    slug: str
    kind: JobKind
    status: JobStatus
    provider: MediaProvider
    model: str
    seconds: int
    file: JobFile | None
    error: JobError | None
    # How long the tool should wait before asking again; 0 once the job is terminal.
    retry_after_seconds: int
    attempts: int
    polls: int
    usd_estimate: float
    created_at: datetime
    submitted_at: datetime | None
    ready_at: datetime | None
    expires_at: datetime | None


class JudgeFile(StrictModel):
    sha256: str = Field(pattern=SHA256_PATTERN)
    label: str = Field(min_length=1, max_length=80)


class JudgeCriterion(StrictModel):
    key: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    question: str = Field(min_length=1, max_length=400)
    weight: float = Field(default=1.0, gt=0, le=10)
    # Set on a fault check: the question names one fault, the judge answers whether it is
    # there, and the criterion scores 10 without it and 10 - cost with it. A cost above 6
    # leaves the criterion under the floor of 4, so that fault alone fails the take; a smaller
    # one only weighs on the overall. Without a cost the judge gives the criterion a score.
    cost: float | None = Field(default=None, gt=0, le=10)


class JudgeIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)
    kind: JudgeKind
    # Images to look at together (a keyframe and its character sheets), or one clip.
    files: list[JudgeFile] = Field(min_length=1, max_length=MAX_JUDGE_FILES)
    rubric: list[JudgeCriterion] = Field(min_length=1, max_length=MAX_RUBRIC)
    # Free-form facts the judge needs: the characters' descriptions, the shot's prompt.
    context: dict[str, Any] = Field(default_factory=dict)
    # A higher bar for this call than the settings row's judge_min_score; a lower one is
    # ignored, since the owner's setting is the floor (no tool sends this today).
    min_score: int | None = Field(default=None, ge=0, le=10)

    @field_validator("context")
    @classmethod
    def _small(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(json.dumps(value, ensure_ascii=False).encode()) > MAX_CONTEXT_BYTES:
            raise ValueError(f"context is larger than {MAX_CONTEXT_BYTES} bytes")
        return value

    @model_validator(mode="after")
    def _one_kind_of_answer(self) -> JudgeIn:
        # The judge is asked one way per call: a score for every criterion, or yes/no for every one.
        if len({criterion.cost is None for criterion in self.rubric}) > 1:
            raise ValueError("a rubric is all fault checks (every criterion has a cost) or none")
        return self

    @property
    def checks(self) -> bool:
        return self.rubric[0].cost is not None


class JudgeOut(StrictModel):
    # 0-10 per rubric key, the weighted overall, and whether it clears the threshold with no
    # criterion under 4.
    scores: dict[str, float]
    overall: float
    passed: bool
    problems: list[str]
    notes: str
    model: str


class LocateIn(StrictModel):
    """One stored picture to find the subjects in (``POST /locate``, locate.py)."""

    slug: str = Field(pattern=SLUG_PATTERN)
    # A png, jpeg or webp in the media store; a clip is refused, the tool extracts a frame first.
    sha256: str = Field(pattern=SHA256_PATTERN)
    # What to look for, in the words of the script ("Jingwei", "the boat"); without any, the
    # characters in the picture and its most prominent subjects.
    labels: list[Annotated[str, Field(min_length=1, max_length=80)]] = Field(
        default_factory=list, max_length=MAX_LOCATE_LABELS
    )


class SubjectBox(StrictModel):
    label: str
    # [ymin, xmin, ymax, xmax] on a 0-1000 scale of the picture's height and width, the way
    # Gemini answers ``box_2d``; multiply by height / 1000 and width / 1000 for pixels.
    box: tuple[int, int, int, int]
    # 0-1, how sure the model is that the box holds that subject.
    score: float


class LocateOut(StrictModel):
    # In the order the model gave them; empty when nothing asked for is in the picture.
    boxes: list[SubjectBox]
    # The stored picture's pixel size, read from its header, so the tool can scale the boxes.
    width: int
    height: int
    model: str


class StockSearchIn(StrictModel):
    """Photos to choose from (``POST /stock/search``, stock.py); nothing is downloaded yet."""

    query: str = Field(min_length=1, max_length=MAX_STOCK_QUERY_CHARS)
    # One vendor, or every vendor the site has a key for.
    provider: StockProvider | None = None
    # Pexels filters all three; Pixabay knows horizontal and vertical only, so ``square`` is
    # not filtered there (the candidates carry their sizes).
    orientation: StockOrientation | None = None
    per_page: int = Field(default=15, ge=1, le=MAX_STOCK_PER_PAGE)
    page: int = Field(default=1, ge=1, le=50)

    @field_validator("query")
    @classmethod
    def _words(cls, value: str) -> str:
        words = " ".join(value.split())
        if not words:
            raise ValueError("query is blank")
        return words


class StockCredit(StrictModel):
    """What the description must say for one photo (docs/videos/ILLUSTRATED.md §圖庫照片)."""

    provider: StockProvider
    # The photographer's name as the vendor gives it, and their page there.
    author: str
    author_url: str | None
    # The photo's own page on the vendor's site: the link a credit points at.
    url: str
    # The vendor's licence by name, and where it is written.
    license: str
    license_url: str
    # The credit line the vendor asks for, ready to paste: "Photo by … on Pexels".
    text: str


class StockCandidate(StrictModel):
    provider: StockProvider
    id: str
    width: int
    height: int
    # Vendor-hosted previews for choosing, never stored: a small one and a larger one (Pixabay's
    # expire after a day).
    thumbnail: str
    preview: str
    # The vendor's description or tags, for the judge or a reader.
    alt: str | None
    credit: StockCredit


class StockSearchOut(StrictModel):
    query: str
    # Vendor by vendor, each in the vendor's order, at most ``per_page`` from each.
    candidates: list[StockCandidate]
    # How many the vendor says match in all, per vendor asked.
    total: dict[str, int]
    # A vendor that failed while another answered; empty when every vendor answered.
    problems: list[str]


class StockFetchIn(StrictModel):
    """One photo to download into the media store (``POST /stock/fetch``)."""

    slug: str = Field(pattern=SLUG_PATTERN)
    provider: StockProvider
    id: str = Field(pattern=STOCK_ID_PATTERN)


class StockFetchOut(StrictModel):
    # The stored file, named by its bytes like any media file, and its real pixel size read
    # from those bytes (not the vendor's word for it).
    sha256: str
    size: int
    content_type: str
    width: int
    height: int
    credit: StockCredit


class BudgetView(StrictModel):
    unit: str
    limit: int
    used: int
    remaining: int


class StoreView(StrictModel):
    used_bytes: int
    max_file_bytes: int
    max_total_bytes: int
    writable: bool


class ChoiceView(StrictModel):
    provider: MediaProvider
    model: str
    configured: bool
    resolution: str | None = None
    seconds: int | None = None
    # Image choices: what one 2K picture costs, or None when the model draws at 1K only; the
    # tool's media/stages.mjs asks for 2K stills when this is set.
    usd_per_image_2k: float | None = None


class MediaStatus(StrictModel):
    enabled: bool
    music_enabled: bool
    image: ChoiceView
    clip: ChoiceView
    music: ChoiceView
    # Illustrated slides (docs/videos/ILLUSTRATED.md): their own switch, image choice, cap,
    # storyboard rule and the owner's licensed music file and sound-effect set; the tool's
    # media/stages.mjs reads the first three.
    slides_enabled: bool = False
    slides_image: ChoiceView | None = None
    slides_max_usd_per_video: int | None = None
    slides_auto_approve_storyboard: bool = True
    slides_music_track: str | None = None
    slides_sfx_set: str | None = None
    # Stock photo vendors by name and whether the site holds a key for each; a tool offers a
    # stock photo only when at least one is true.
    stock: dict[str, bool] = Field(default_factory=dict)
    models: MediaOptionsView
    budgets: dict[str, BudgetView]
    # This month's jobs priced with the catalog, submitted or ready.
    estimated_usd: float
    max_usd_per_video: int
    max_clips_per_video: int
    max_retakes_per_shot: int
    judge_min_score: int
    style_preset: str
    store: StoreView
    limits: dict[str, int]


class PruneOut(StrictModel):
    expired_jobs: int
    deleted_files: int
    freed_bytes: int
