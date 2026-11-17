from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

SeriesKey = Literal["curio", "so-thats-why"]
ThemeStatus = Literal["producible", "reserve", "short", "all"]
ThemeSort = Literal["rank", "id"]
CoreStatus = Literal["passing", "scored", "unscored", "all"]
EpisodeStatus = Literal["published", "unpublished", "all"]
MaterialVerdict = Literal["ready", "merge", "reserve", "drop"]
NonEmptyText = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
Sha256 = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]
Day = Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")]
Score = Annotated[float, Field(ge=1, le=10)]


class PoolModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class AudienceRound(PoolModel):
    score: Score
    comment: NonEmptyText
    changes: NonEmptyText
    reviewed_on: Day


class Audience(PoolModel):
    score: Score
    rank: Annotated[int, Field(ge=1)]
    of: Annotated[int, Field(ge=1)]
    click: Score
    hook: Score
    surprise: Score
    payoff: Score
    share: Score
    # Demand (2026-11-17): the sixth item folded into score, and the five-item mean
    # before it. Both are null until the theme is scored for demand.
    demand: Score | None
    base: Score | None
    comment: NonEmptyText
    reviewed_on: Day
    rounds: list[AudienceRound]

    @model_validator(mode="after")
    def _rank_within_total(self) -> Self:
        if self.rank > self.of:
            raise ValueError("audience rank exceeds the scored total")
        if (self.demand is None) != (self.base is None):
            raise ValueError("audience demand and base come together")
        return self


class Material(PoolModel):
    verdict: MaterialVerdict
    missing: str | None


class Chapter(PoolModel):
    title: NonEmptyText
    seconds: Annotated[int, Field(ge=1)]
    new_information: NonEmptyText


class ThemeSummary(PoolModel):
    id: NonEmptyText
    title: NonEmptyText
    category: str | None
    core_question: NonEmptyText
    target_minutes: Annotated[float, Field(gt=0)]
    long: bool
    producible: bool
    material: Material | None
    candidates: Annotated[int, Field(ge=1)]
    audience: Audience | None


class ThemeDetail(ThemeSummary):
    chapters: list[Chapter]
    boredom_risk: NonEmptyText
    drop_if: NonEmptyText
    evidence_gaps: NonEmptyText


class CoreSummary(PoolModel):
    """A selected topic that carries an episode on its own; it sits in no theme."""

    id: NonEmptyText
    category: str | None
    question: NonEmptyText
    hook: str
    payoff: str
    minutes: tuple[Annotated[float, Field(gt=0)], Annotated[float, Field(gt=0)]]
    audience: Audience | None
    demand: Score | None
    produced: bool


class Expansion(PoolModel):
    batch_id: NonEmptyText
    created_on: Day | None
    scope: str
    candidates: Annotated[int, Field(ge=0)]
    selected: Annotated[int, Field(ge=0)]
    not_added: Annotated[int, Field(ge=0)]
    sources: Annotated[int, Field(ge=0)]


class Checkpoint(PoolModel):
    name: NonEmptyText
    revision: str | None
    selected: int | None
    raw: int | None


class EpisodeCatalog(PoolModel):
    youtube_id: str | None
    privacy: str | None
    status: str | None
    version: str | None
    final_date: str | None


class PoolEpisode(PoolModel):
    key: NonEmptyText
    code: str | None
    title: NonEmptyText
    category: str | None
    slugs: list[NonEmptyText]
    candidate_ids: list[NonEmptyText]
    catalog: EpisodeCatalog


class SeriesCounts(PoolModel):
    raw_records: Annotated[int, Field(ge=0)]
    selected: Annotated[int, Field(ge=0)]
    themes: Annotated[int, Field(ge=0)]
    long_themes: Annotated[int, Field(ge=0)]
    producible: Annotated[int, Field(ge=0)]
    long_reserve: Annotated[int, Field(ge=0)]
    scored: Annotated[int, Field(ge=0)]
    improved: Annotated[int, Field(ge=0)]
    cores: Annotated[int, Field(ge=0)]
    cores_scored: Annotated[int, Field(ge=0)]
    cores_passing: Annotated[int, Field(ge=0)]


class SourceHashes(PoolModel):
    themes_sha256: Sha256
    manifest_sha256: Sha256


class SeriesBundle(PoolModel):
    key: SeriesKey
    name: NonEmptyText
    revision: NonEmptyText
    counts: SeriesCounts
    audience_min: Annotated[float, Field(ge=1, le=10)]
    themes: list[ThemeDetail]
    cores: list[CoreSummary]
    episodes: list[PoolEpisode]
    expansions: list[Expansion]
    checkpoints: list[Checkpoint]
    sources: SourceHashes

    @model_validator(mode="after")
    def _counts_match_themes(self) -> Self:
        if self.counts.themes != len(self.themes):
            raise ValueError("theme count does not match the themes")
        if self.counts.producible != sum(theme.producible for theme in self.themes):
            raise ValueError("producible count does not match the themes")
        if len({theme.id for theme in self.themes}) != len(self.themes):
            raise ValueError("duplicate theme id")
        return self

    @model_validator(mode="after")
    def _counts_match_cores(self) -> Self:
        scored = [core for core in self.cores if core.audience is not None]
        passing = [
            core for core in scored if core.audience and core.audience.score >= self.audience_min
        ]
        if (self.counts.cores, self.counts.cores_scored, self.counts.cores_passing) != (
            len(self.cores),
            len(scored),
            len(passing),
        ):
            raise ValueError("core counts do not match the cores")
        if len({core.id for core in self.cores}) != len(self.cores):
            raise ValueError("duplicate core id")
        return self


class PoolBundle(PoolModel):
    schema_version: Literal[1]
    status: Literal["EDITORIAL_THEMES_NOT_SCRIPTS"]
    series: list[SeriesBundle]

    @model_validator(mode="after")
    def _one_entry_per_series(self) -> Self:
        if sorted(series.key for series in self.series) != ["curio", "so-thats-why"]:
            raise ValueError("the bundle needs exactly the two explainer series")
        return self


class SeriesOverview(PoolModel):
    key: SeriesKey
    name: str
    revision: str
    counts: SeriesCounts
    audience_min: float
    themes_sha256: str


class PoolOverview(PoolModel):
    series: list[SeriesOverview]


class CategoryCount(PoolModel):
    category: str
    count: int


class ThemePage(PoolModel):
    items: list[ThemeSummary]
    total: int
    page: int
    page_size: int
    categories: list[CategoryCount]


class CorePage(PoolModel):
    items: list[CoreSummary]
    total: int
    page: int
    page_size: int
    categories: list[CategoryCount]


class ExpansionPage(PoolModel):
    expansions: list[Expansion]
    checkpoints: list[Checkpoint]


class EpisodeStatusRow(PoolModel):
    key: str
    code: str | None
    title: str
    category: str | None
    slugs: list[str]
    candidate_ids: list[str]
    published: bool
    youtube_id: str | None
    youtube_url: str | None
    youtube_source: Literal["site", "catalog"] | None
    site_slug: str | None
    publish_at: datetime | None
    stage: str | None
    dropped: bool
    privacy: str | None


class EpisodePage(PoolModel):
    items: list[EpisodeStatusRow]
    total: int
    published: int
    unpublished: int
