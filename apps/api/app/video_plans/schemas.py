from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

PlanCatalog = Literal["season1", "season2", "season3", "brand-stories", "ai-terms"]
PlanStage = Literal[
    "REVIEWED_OUTLINE_NOT_MEDIA",
    "CHECKED_CANDIDATE_REQUIRES_OUTLINE",
    "REVIEWED_STORY_PLAN_NOT_MEDIA",
    "TERM_PLAN_NOT_MEDIA",
    "COVERED_DO_NOT_REMAKE",
]
DetailLabel = Literal["source_record", "source_package", "effective_inputs", "effective_chapters"]
NonEmptyText = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
Sha256 = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]

CATALOG_COUNTS: dict[PlanCatalog, int] = {
    "season1": 100,
    "season2": 92,
    "season3": 100,
    "brand-stories": 100,
    "ai-terms": 81,
}
STAGES: tuple[PlanStage, ...] = (
    "REVIEWED_OUTLINE_NOT_MEDIA",
    "CHECKED_CANDIDATE_REQUIRES_OUTLINE",
    "REVIEWED_STORY_PLAN_NOT_MEDIA",
    "TERM_PLAN_NOT_MEDIA",
    "COVERED_DO_NOT_REMAKE",
)
CATALOG_STAGES: dict[PlanCatalog, tuple[PlanStage, ...]] = {
    "season1": ("REVIEWED_OUTLINE_NOT_MEDIA",),
    "season2": ("REVIEWED_OUTLINE_NOT_MEDIA",),
    "season3": ("CHECKED_CANDIDATE_REQUIRES_OUTLINE",),
    "brand-stories": ("REVIEWED_STORY_PLAN_NOT_MEDIA",),
    "ai-terms": ("TERM_PLAN_NOT_MEDIA", "COVERED_DO_NOT_REMAKE"),
}


class CatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class PlanDetail(CatalogModel):
    label: DetailLabel
    text: NonEmptyText


class PlanEntry(CatalogModel):
    catalog: PlanCatalog
    id: NonEmptyText
    video_slug: NonEmptyText
    title: NonEmptyText
    source_status: NonEmptyText
    stage: PlanStage
    target_duration_seconds: Literal[600, 780]
    min_duration_seconds: Literal[480]
    source_path: NonEmptyText
    source_sha256: Sha256
    source_record_sha256: Sha256
    source_package_path: NonEmptyText | None
    source_package_sha256: Sha256 | None
    details: list[PlanDetail] = Field(min_length=1)

    @field_validator("target_duration_seconds", "min_duration_seconds", mode="before")
    @classmethod
    def validate_integer_duration(cls, value: object) -> object:
        # Literal uses equality, so strict=True alone accepts 600.0 as Literal[600].
        if type(value) is not int:
            raise ValueError("duration seconds must be integers")
        return value

    @model_validator(mode="after")
    def validate_source_plan(self) -> Self:
        expected_target = 780 if self.catalog == "brand-stories" else 600
        if self.target_duration_seconds != expected_target:
            raise ValueError("target duration does not match the catalog's reviewed plan")
        if self.stage not in CATALOG_STAGES[self.catalog]:
            raise ValueError("stage does not match the source catalog")
        if self.catalog == "ai-terms" and (
            (self.stage == "COVERED_DO_NOT_REMAKE") != (self.source_status == "covered")
        ):
            raise ValueError("covered source status must retain the covered planning stage")
        if (self.source_package_path is None) != (self.source_package_sha256 is None):
            raise ValueError("source package path and hash must be present together")
        for path in (self.source_path, self.source_package_path):
            if path is not None and (
                PurePosixPath(path).is_absolute()
                or ".." in PurePosixPath(path).parts
                or "\\" in path
                or ":" in path
                or not path.startswith("docs/videos/")
            ):
                raise ValueError("source paths must be repository-relative video documents")
        labels = [detail.label for detail in self.details]
        if len(labels) != len(set(labels)) or "source_record" not in labels:
            raise ValueError("details must include a unique source_record section")
        if ("source_package" in labels) != (self.source_package_path is not None):
            raise ValueError("source package detail must match its provenance")
        if self.catalog in ("season1", "season2") and not {
            "source_package",
            "effective_inputs",
        }.issubset(labels):
            raise ValueError("reviewed outline plans must preserve original and effective text")
        if self.catalog == "season2" and "effective_chapters" not in labels:
            raise ValueError("season two must preserve the revised ten-minute chapters")
        return self


class CatalogBundle(CatalogModel):
    format_version: Literal[1]
    plans_sha256: Sha256
    catalog_counts: dict[PlanCatalog, int]
    entries: list[PlanEntry]

    @field_validator("format_version", mode="before")
    @classmethod
    def validate_integer_version(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError("format version must be an integer")
        return value

    @model_validator(mode="after")
    def validate_complete_catalog(self) -> Self:
        actual_counts = Counter(entry.catalog for entry in self.entries)
        if self.catalog_counts != CATALOG_COUNTS or actual_counts != CATALOG_COUNTS:
            raise ValueError("catalog must contain all 473 source plans with exact catalog counts")
        covered = [entry for entry in self.entries if entry.stage == "COVERED_DO_NOT_REMAKE"]
        if len(covered) != 1 or covered[0].id != "ai-agent":
            raise ValueError(
                "the catalog must preserve the covered ai-agent reference exactly once"
            )
        identities = {(entry.catalog, entry.id) for entry in self.entries}
        slugs = {entry.video_slug for entry in self.entries}
        if len(identities) != len(self.entries) or len(slugs) != len(self.entries):
            raise ValueError("plan identities and video slugs must be unique")
        source_hashes: dict[str, str] = {}
        for entry in self.entries:
            for path, digest in (
                (entry.source_path, entry.source_sha256),
                (entry.source_package_path, entry.source_package_sha256),
            ):
                if path is not None and digest is not None:
                    if path in source_hashes and source_hashes[path] != digest:
                        raise ValueError("the same source path cannot have conflicting hashes")
                    source_hashes[path] = digest
        return self


class CatalogCount(CatalogModel):
    catalog: PlanCatalog
    count: int = Field(ge=0)


class StageCount(CatalogModel):
    stage: PlanStage
    count: int = Field(ge=0)


class PlanPage(CatalogModel):
    items: list[PlanEntry]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    catalogs: list[CatalogCount]
    stages: list[StageCount]
    catalog_total: int = Field(ge=0)
    plans_sha256: Sha256
