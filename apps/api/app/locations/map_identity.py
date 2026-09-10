"""Provider identities attached to one editorial place, independent of its coordinates.

Only provider IDs and our own review decisions are durable. Provider descriptions and
coordinates belong in a short lived comparison cache, never this metadata.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Literal
from urllib.parse import urlencode
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.destinations.catalog import destination_for_id
from app.models import FoodMerchant, TravelHotspot, TravelServiceProduct

CatalogPlace = TravelHotspot | FoodMerchant | TravelServiceProduct
IdentityProvider = Literal["google_places", "naver_maps"]
IdentityStatus = Literal["unverified", "pending", "verified", "rejected"]
NAVER_PLACE_PATTERN = re.compile(
    r"https://map\.naver\.com/(?:p|v5)/entry/place/(\d+)/?(?:\?[^#]*)?(?:#.*)?"
)


class MapIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: IdentityProvider
    place_id: str | None = Field(default=None, max_length=255)
    map_url: str | None = Field(default=None, max_length=2048)
    status: IdentityStatus = "unverified"
    verified_at: datetime | None = None
    verified_by_user_id: UUID | None = None
    evidence_url: str | None = Field(default=None, max_length=2048)


def naver_place_id(url: str | None) -> str | None:
    match = NAVER_PLACE_PATTERN.fullmatch(url or "")
    return match.group(1) if match else None


def google_place_url(place_id: str) -> str:
    return "https://www.google.com/maps/search/?" + urlencode(
        {"api": "1", "query": "Place", "query_place_id": place_id}
    )


def identity_metadata(row: CatalogPlace) -> dict[str, Any]:
    if isinstance(row, TravelHotspot):
        return dict(row.metadata_json or {})
    if isinstance(row, FoodMerchant):
        return dict(row.map_identity_metadata or {})
    return dict(row.facts or {})


def set_identity_metadata(row: CatalogPlace, metadata: dict[str, Any]) -> None:
    if isinstance(row, TravelHotspot):
        row.metadata_json = metadata
    elif isinstance(row, FoodMerchant):
        row.map_identity_metadata = metadata
    else:
        row.facts = metadata


def catalog_country_code(row: CatalogPlace) -> str:
    if not isinstance(row, TravelServiceProduct):
        return row.country_code.upper()
    destination = destination_for_id(row.destination_id)
    if destination and destination.timezone == "Asia/Seoul":
        return "KR"
    return {"Japan": "JP", "Thailand": "TH", "Taiwan": "TW"}.get(
        destination.country if destination else "", ""
    )


def catalog_google_place_id(row: CatalogPlace) -> str | None:
    value = (
        row.facts.get("google_place_id")
        if isinstance(row, TravelServiceProduct)
        else row.google_place_id
    )
    return str(value) if value else None


def catalog_naver_map_url(row: CatalogPlace) -> str | None:
    value = (
        row.facts.get("naver_map_url")
        if isinstance(row, TravelServiceProduct)
        else row.naver_map_url
    )
    return str(value) if value else None


def catalog_map_verified(row: CatalogPlace) -> bool:
    if isinstance(row, TravelServiceProduct):
        return bool(row.facts.get("map_verified"))
    return row.map_match_status == "verified"


def normalize_map_identities(value: object) -> dict[str, dict[str, Any]]:
    """Validate and redact identities before putting them on any public response."""
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(value, dict):
        return result
    for provider in ("naver_maps", "google_places"):
        raw = value.get(provider)
        if not isinstance(raw, dict):
            continue
        try:
            identity = MapIdentity.model_validate(raw)
        except ValidationError:
            continue
        if identity.provider != provider:
            continue
        # URLs are generated from validated IDs, never supplied navigation targets.
        if provider == "naver_maps":
            exact = naver_place_id(identity.map_url)
            identity.place_id = exact
            identity.map_url = f"https://map.naver.com/p/entry/place/{exact}" if exact else None
        else:
            if not identity.place_id or not re.fullmatch(
                r"[A-Za-z0-9_-]{5,255}", identity.place_id
            ):
                continue
            identity.map_url = google_place_url(identity.place_id)
        result[provider] = identity.model_dump(
            mode="json", exclude={"verified_by_user_id", "evidence_url"}
        )
    return result


def verified_google_place_id(identities: object, place_id: str | None = None) -> str | None:
    identity = normalize_map_identities(identities).get("google_places", {})
    value = identity.get("place_id")
    if identity.get("status") != "verified" or not value:
        return None
    if place_id is not None and value != place_id:
        return None
    return str(value)


def catalog_map_identities(row: CatalogPlace) -> dict[str, dict[str, Any]]:
    """Legacy primary identity stays usable; supplemental KR Google needs its own review."""
    metadata = identity_metadata(row)
    result = normalize_map_identities(metadata.get("map_identities"))
    google_id = catalog_google_place_id(row)
    google = result.get("google_places")
    if google and google.get("place_id") != google_id:
        result.pop("google_places")
    if google_id and "google_places" not in result:
        result["google_places"] = MapIdentity(
            provider="google_places",
            place_id=google_id,
            map_url=google_place_url(google_id),
            status="verified"
            if catalog_country_code(row) != "KR" and catalog_map_verified(row)
            else "unverified",
        ).model_dump(mode="json", exclude={"verified_by_user_id", "evidence_url"})
    naver_url = catalog_naver_map_url(row)
    naver_id = naver_place_id(naver_url)
    naver = result.get("naver_maps")
    raw_identities = metadata.get("map_identities")
    legacy_naver = "map_identities" not in metadata or (
        isinstance(raw_identities, dict) and "naver_maps" not in raw_identities
    )
    # Keep provider-specific review facts only for the same canonical NAVER place.
    # A changed or malformed explicit identity must not inherit legacy verification.
    if not naver_id:
        result.pop("naver_maps", None)
    elif not naver or naver.get("place_id") != naver_id:
        legacy_verified = legacy_naver and catalog_map_verified(row)
        result["naver_maps"] = MapIdentity(
            provider="naver_maps",
            place_id=naver_id,
            map_url=f"https://map.naver.com/p/entry/place/{naver_id}",
            status="verified" if legacy_verified else "unverified",
            verified_at=row.map_verified_at
            if legacy_verified and isinstance(row, TravelHotspot)
            else None,
        ).model_dump(mode="json", exclude={"verified_by_user_id", "evidence_url"})
    return result
