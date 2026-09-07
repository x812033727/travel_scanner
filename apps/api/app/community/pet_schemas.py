from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import Field, HttpUrl, field_validator, model_validator

from app.community.schemas import Input, ResolveReportInput


class PetRule(Input):
    species: str = Field(min_length=1, max_length=40)
    status: Literal["allowed", "conditional", "not_allowed", "unknown"] = "unknown"
    weight_limit: Literal["unknown", "none", "limited"] = "unknown"
    max_weight_kg: float | None = Field(default=None, gt=0, le=200)
    count_limit: Literal["unknown", "none", "limited"] = "unknown"
    max_count: int | None = Field(default=None, ge=1, le=100)
    ground_allowed: bool | None = None
    leash_required: bool | None = None
    carrier_required: bool | None = None
    stroller_required: bool | None = None
    stroller_allowed: bool | None = None
    diaper_required: bool | None = None
    indoor_allowed: bool | None = None
    outdoor_allowed: bool | None = None
    reservation_required: bool | None = None
    overnight_allowed: bool | None = None
    fee_amount: float | None = Field(default=None, ge=0, le=1_000_000)
    fee_currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    notes: str = Field(default="", max_length=2000)

    @field_validator("species")
    @classmethod
    def normalized_species(cls, value: str) -> str:
        aliases = {
            "狗": "dog",
            "犬": "dog",
            "개": "dog",
            "dogs": "dog",
            "貓": "cat",
            "猫": "cat",
            "고양이": "cat",
            "cats": "cat",
        }
        return aliases.get(value.strip().casefold(), value.strip().casefold())

    @model_validator(mode="after")
    def consistent_limits(self) -> PetRule:
        if (self.weight_limit == "limited") != (self.max_weight_kg is not None):
            raise ValueError("limited weight requires a numeric maximum")
        if (self.count_limit == "limited") != (self.max_count is not None):
            raise ValueError("limited count requires a numeric maximum")
        if (self.fee_amount is None) != (self.fee_currency is None):
            raise ValueError("fee requires a currency")
        return self


class PetRequirements(Input):
    species: str = Field(min_length=1, max_length=40)
    count: int = Field(default=1, ge=1, le=20)
    weight_kg: float = Field(gt=0, le=200)
    area: Literal["any", "indoor", "outdoor"] = "any"
    ground_required: bool = False
    has_leash: bool = True
    has_carrier: bool = False
    has_stroller: bool = False
    has_diaper: bool = False
    overnight: bool = False

    @field_validator("species")
    @classmethod
    def normalized_species(cls, value: str) -> str:
        return PetRule.normalized_species(value)


class PlaceInput(Input):
    name: str = Field(min_length=1, max_length=160)
    names: dict[str, str] = Field(default_factory=dict)
    kind: Literal["restaurant", "cafe", "shop", "lodging", "attraction"]
    country: str = Field(pattern=r"^[A-Z]{2}$")
    destination: str = Field(min_length=1, max_length=160)
    address: str = Field(default="", max_length=400)
    official_url: HttpUrl | None = None
    reference_kind: Literal["hotspot", "merchant", "restaurant", "hotel"] | None = None
    reference_id: str | None = Field(default=None, max_length=160)

    @model_validator(mode="after")
    def paired_reference(self) -> PlaceInput:
        if (self.reference_kind is None) != (self.reference_id is None):
            raise ValueError("reference kind and id are required together")
        if any(
            key not in {"zh-TW", "zh-CN", "en", "ja", "ko"} or not value.strip() or len(value) > 160
            for key, value in self.names.items()
        ):
            raise ValueError("invalid localized place names")
        return self


class PetReportInput(Input):
    body: str = Field(min_length=3, max_length=2000)
    source_url: HttpUrl | None = None
    visited_on: date | None = None
    media_ids: list[UUID] = Field(default_factory=list, max_length=5)
    proposed_policies: list[PetRule] = Field(default_factory=list, max_length=10)


class PetReference(Input):
    kind: Literal["hotspot", "merchant", "restaurant", "hotel"]
    id: str = Field(min_length=1, max_length=160)


class PetResolveInput(ResolveReportInput):
    flag_conflict: bool = False


class PetReview(Input):
    version: int = Field(ge=1)
    status: Literal["approved", "rejected", "disabled"]
    policies: list[PetRule] = Field(max_length=10)
    source_url: HttpUrl
    reason: str = Field(min_length=3, max_length=1000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    coordinate_source_url: HttpUrl | None = None
    identity_key: str | None = Field(default=None, max_length=200)
    report_ids: list[UUID] = Field(default_factory=list, max_length=100)
    references: list[PetReference] | None = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def reviewed_identity(self) -> PetReview:
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("coordinates must be a pair")
        if self.latitude is not None and self.coordinate_source_url is None:
            raise ValueError("coordinates require an independent source")
        species = [rule.species for rule in self.policies]
        if len(set(species)) != len(species):
            raise ValueError("one policy per species")
        if self.references and len({(ref.kind, ref.id) for ref in self.references}) != len(
            self.references
        ):
            raise ValueError("duplicate references")
        return self
