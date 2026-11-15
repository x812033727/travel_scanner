from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

SeriesKey = Literal[
    "tai-nainai", "zhong-tian-qu-qi", "ou-de-jianghu", "zero-root-yaozu", "xiuxian-jiangli"
]
DocKind = Literal["brief", "script", "storyboard", "review"]
NonEmptyText = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
Slug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9-]+-e\d{3}(?:-r\d+)?$")]
DocId = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9_-]+$")]
Sha256 = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]


class DramaModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class EpisodeDoc(DramaModel):
    kind: DocKind
    bytes: Annotated[int, Field(ge=1)]


class EpisodeSummary(DramaModel):
    slug: Slug
    number: Annotated[int, Field(ge=1)]
    variant: str | None
    title: NonEmptyText
    target_minutes: float | list[float] | None
    docs: list[EpisodeDoc]


class SeriesDocument(DramaModel):
    id: DocId
    path: NonEmptyText
    title: NonEmptyText
    bytes: Annotated[int, Field(ge=1)]


class SeriesCounts(DramaModel):
    episodes: int
    brief: int
    script: int
    storyboard: int
    review: int


class SeriesIndex(DramaModel):
    key: SeriesKey
    name: NonEmptyText
    counts: SeriesCounts
    episodes: list[EpisodeSummary]
    documents: list[SeriesDocument]
    content_sha256: Sha256

    @model_validator(mode="after")
    def _counts_match(self) -> Self:
        if self.counts.episodes != len(self.episodes):
            raise ValueError("episode count does not match the episodes")
        if len({episode.slug for episode in self.episodes}) != len(self.episodes):
            raise ValueError("duplicate episode slug")
        if len({document.id for document in self.documents}) != len(self.documents):
            raise ValueError("duplicate document id")
        return self


class DramaIndex(DramaModel):
    schema_version: Literal[1]
    status: Literal["AUTHORED_TEXT_NOT_PRODUCTION_STATE"]
    series: list[SeriesIndex]


class SeriesContent(DramaModel):
    key: SeriesKey
    episodes: dict[str, dict[DocKind, str]]
    documents: dict[str, str]


class EpisodeText(DramaModel):
    kind: DocKind
    markdown: str


class EpisodeDetail(DramaModel):
    series: SeriesKey
    slug: str
    title: str
    docs: list[EpisodeText]


class DocumentDetail(DramaModel):
    series: SeriesKey
    id: str
    path: str
    title: str
    markdown: str
