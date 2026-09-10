"""Bounded candidate collection and explicit supplemental Google identity review."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from redis.asyncio import Redis
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.maps import build_map_links
from app.hotspots.places import automatic_refresh_allowed
from app.locations.coordinates import valid_coordinate_pair
from app.locations.map_identity import (
    CatalogPlace,
    MapIdentity,
    catalog_country_code,
    catalog_google_place_id,
    catalog_map_identities,
    catalog_map_verified,
    catalog_naver_map_url,
    identity_metadata,
    set_identity_metadata,
)
from app.models import AdminAuditLog, FoodMerchant, TravelHotspot, TravelServiceProduct
from app.places.google import GoogleTravelService
from app.problems import AppError

CatalogKind = Literal["hotspot", "merchant", "hotel"]
COMPARISON_TTL_SECONDS = 900
BATCH_TTL_SECONDS = 7 * 86_400
CATALOG_MODELS: dict[
    CatalogKind, type[TravelHotspot] | type[FoodMerchant] | type[TravelServiceProduct]
] = {"hotspot": TravelHotspot, "merchant": FoodMerchant, "hotel": TravelServiceProduct}


class CatalogReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: CatalogKind
    id: UUID


class IdentityReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["confirm", "reject"]
    expected_revision: int = Field(ge=0)
    expected_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    snapshot_id: UUID
    place_id: str = Field(pattern=r"^[A-Za-z0-9_-]{5,255}$")
    note: str = Field(min_length=1, max_length=500)


def review_state(row: CatalogPlace) -> dict[str, Any]:
    value = identity_metadata(row).get("map_identity_review")
    return dict(value) if isinstance(value, dict) else {}


def revision(row: CatalogPlace) -> int:
    value = review_state(row).get("revision", 0)
    return value if isinstance(value, int) and value >= 0 else 0


def canonical_values(row: CatalogPlace) -> dict[str, Any]:
    if isinstance(row, TravelServiceProduct):
        name = row.title
        local_name = row.names_json.get("ko") or name
        address = None
        latitude, longitude = row.facts.get("latitude"), row.facts.get("longitude")
        source_url = row.facts.get("coordinate_source_url")
    else:
        name = row.name
        local_name = (
            str((row.metadata_json or {}).get("local_name") or name)
            if isinstance(row, TravelHotspot)
            else row.local_name
        )
        address = (
            (row.metadata_json or {}).get("address")
            if isinstance(row, TravelHotspot)
            else row.address
        )
        latitude, longitude = row.latitude, row.longitude
        source_url = row.coordinate_source_url
    return {
        "name": name,
        "local_name": local_name,
        "address": address,
        "latitude": float(latitude) if latitude is not None else None,
        "longitude": float(longitude) if longitude is not None else None,
        "coordinate_source_url": source_url,
        "destination_id": row.destination_id,
        "country_code": catalog_country_code(row),
        "google_place_id": catalog_google_place_id(row),
        "naver_map_url": catalog_naver_map_url(row),
    }


def canonical_fingerprint(row: CatalogPlace) -> str:
    return hashlib.sha256(json.dumps(canonical_values(row), sort_keys=True).encode()).hexdigest()


def item_payload(kind: CatalogKind, row: CatalogPlace) -> dict[str, Any]:
    values = canonical_values(row)
    identities = catalog_map_identities(row)
    state = review_state(row)
    return {
        "kind": kind,
        "id": str(row.id),
        **values,
        "revision": revision(row),
        "canonical_fingerprint": canonical_fingerprint(row),
        "map_identities": identities,
        "review": {
            key: state[key]
            for key in ("status", "candidate_place_ids", "generated_at", "reviewed_at", "note")
            if key in state
        },
        "map_links": build_map_links(
            name=values["name"],
            local_name=values["local_name"],
            city_name=row.destination_id,
            country_code=values["country_code"],
            latitude=values["latitude"],
            longitude=values["longitude"],
            google_place_id=values["google_place_id"],
            naver_map_url=values["naver_map_url"],
            map_match_status="verified" if catalog_map_verified(row) else "unverified",
            map_identities=identities,
        ),
    }


async def load_catalog_place(
    session: AsyncSession, reference: CatalogReference, *, lock: bool = False
) -> CatalogPlace:
    model = CATALOG_MODELS[reference.kind]
    statement = select(model).where(model.id == reference.id)
    if lock:
        statement = statement.with_for_update().execution_options(populate_existing=True)
    row = cast(CatalogPlace | None, await session.scalar(statement))
    if row is None or (isinstance(row, TravelServiceProduct) and row.kind != "hotel"):
        raise AppError(404, "catalog_place_not_found", "找不到這筆目錄地點")
    if catalog_country_code(row) != "KR":
        raise AppError(422, "korean_place_required", "雙地圖配對目前只處理韓國目錄地點")
    return row


def comparison_key(reference: CatalogReference) -> str:
    return f"map-identities:comparison:{reference.kind}:{reference.id}"


def snapshot_key(snapshot_id: UUID) -> str:
    return f"map-identities:snapshot:{snapshot_id}"


async def collect_candidates(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    reference: CatalogReference,
    actor_id: UUID,
    *,
    service: GoogleTravelService | None = None,
) -> dict[str, Any]:
    row = await load_catalog_place(session, reference)
    before_fingerprint = canonical_fingerprint(row)
    before_revision = revision(row)
    values = canonical_values(row)
    google = service or GoogleTravelService(redis, settings, locale="ko")
    if not google.configured:
        raise AppError(503, "google_maps_not_configured", "Google 地點配對服務尚未設定")
    if not await automatic_refresh_allowed(redis, settings):
        raise AppError(429, "google_maps_usage_guard", "Google 地點配對已達用量保護門檻")
    query = " ".join(
        dict.fromkeys(
            str(value)
            for value in (
                values["local_name"],
                values["name"],
                values["address"],
                row.destination_id,
            )
            if value
        )
    )
    candidates = await google.search_place_candidates(
        query, values["latitude"], values["longitude"], region_code="KR", limit=5
    )
    # A regionCode biases the provider; it is not a hard geographic restriction.
    candidates = [
        candidate
        for candidate in candidates
        if (
            candidate.get("country_code") == "KR"
            and valid_coordinate_pair(candidate.get("latitude"), candidate.get("longitude"))
            and 32 <= float(candidate["latitude"]) <= 39.8
            and 124 <= float(candidate["longitude"]) <= 132
        )
    ]
    row = await load_catalog_place(session, reference, lock=True)
    if canonical_fingerprint(row) != before_fingerprint or revision(row) != before_revision:
        raise AppError(409, "map_identity_changed", "目錄地點已更新，請重新取得配對候選")
    now = datetime.now(UTC)
    ids = list(dict.fromkeys(str(candidate["place_id"]) for candidate in candidates))
    state = {
        "revision": before_revision + 1,
        "status": "pending" if ids else "unmatched",
        "candidate_place_ids": ids,
        "generated_at": now.isoformat(),
        "canonical_fingerprint": before_fingerprint,
    }
    metadata = identity_metadata(row)
    metadata["map_identity_review"] = state
    set_identity_metadata(row, metadata)
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="map_identity.candidates_collected",
            target=f"{reference.kind}:{reference.id}",
            metadata_json={"candidate_place_ids": ids, "revision": state["revision"]},
        )
    )
    await session.commit()
    # These are comparison-only provider fields and expire instead of entering the database.
    comparison = {
        "candidates": candidates,
        "revision": state["revision"],
        "canonical_fingerprint": before_fingerprint,
        "expires_at": (now + timedelta(seconds=COMPARISON_TTL_SECONDS)).isoformat(),
    }
    await redis.set(comparison_key(reference), json.dumps(comparison), ex=COMPARISON_TTL_SECONDS)
    return {"item": item_payload(reference.kind, row), **comparison}


async def candidate_snapshot(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    reference: CatalogReference,
    actor_id: UUID,
) -> dict[str, Any]:
    row = await load_catalog_place(session, reference)
    raw = await redis.get(comparison_key(reference))
    comparison = json.loads(raw) if raw else None
    if not isinstance(comparison, dict) or (
        comparison.get("revision") != revision(row)
        or comparison.get("canonical_fingerprint") != canonical_fingerprint(row)
    ):
        fresh = await collect_candidates(session, redis, settings, reference, actor_id)
        comparison = {key: value for key, value in fresh.items() if key != "item"}
        row = await load_catalog_place(session, reference)
    snapshot_id = uuid4()
    expires_at = datetime.fromisoformat(comparison["expires_at"])
    remaining = max(1, int((expires_at - datetime.now(UTC)).total_seconds()))
    await redis.set(
        snapshot_key(snapshot_id),
        json.dumps(
            {
                "actor_id": str(actor_id),
                "kind": reference.kind,
                "id": str(reference.id),
                **comparison,
            }
        ),
        ex=remaining,
    )
    return {
        "item": item_payload(reference.kind, row),
        "snapshot_id": str(snapshot_id),
        "candidates": comparison["candidates"],
        "expires_at": comparison["expires_at"],
    }


async def duplicate_owner(
    session: AsyncSession, reference: CatalogReference, place_id: str
) -> bool:
    if session.bind is not None and session.bind.dialect.name == "postgresql":
        # Two reviewers can confirm different rows concurrently. Hotel IDs live in
        # JSON, so serialize the duplicate check as well as locking each target row.
        lock_key = int.from_bytes(
            hashlib.sha256(f"map-identity:{place_id}".encode()).digest()[:8],
            "big",
            signed=True,
        )
        await session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_key})
    checks = [
        ("hotspot", select(TravelHotspot.id).where(TravelHotspot.google_place_id == place_id)),
        ("merchant", select(FoodMerchant.id).where(FoodMerchant.google_place_id == place_id)),
        (
            "hotel",
            select(TravelServiceProduct.id).where(
                TravelServiceProduct.kind == "hotel",
                TravelServiceProduct.facts["google_place_id"].as_string() == place_id,
            ),
        ),
    ]
    for kind, statement in checks:
        if kind == reference.kind:
            statement = statement.where(statement.selected_columns[0] != reference.id)
        if await session.scalar(statement) is not None:
            return True
    return False


async def review_identity(
    session: AsyncSession,
    redis: Redis,
    reference: CatalogReference,
    payload: IdentityReviewRequest,
    actor_id: UUID,
) -> dict[str, Any]:
    raw = await redis.get(snapshot_key(payload.snapshot_id))
    snapshot = json.loads(raw) if raw else {}
    if (
        snapshot.get("actor_id") != str(actor_id)
        or snapshot.get("kind") != reference.kind
        or snapshot.get("id") != str(reference.id)
        or snapshot.get("revision") != payload.expected_revision
        or snapshot.get("canonical_fingerprint") != payload.expected_fingerprint
        or not any(
            candidate.get("place_id") == payload.place_id
            for candidate in snapshot.get("candidates", [])
        )
    ):
        raise AppError(409, "map_identity_snapshot_expired", "配對比較已過期，請重新取得候選")
    row = await load_catalog_place(session, reference, lock=True)
    if (
        revision(row) != payload.expected_revision
        or canonical_fingerprint(row) != payload.expected_fingerprint
    ):
        raise AppError(409, "map_identity_changed", "目錄地點或候選已更新，請重新確認")
    state = review_state(row)
    if payload.place_id not in state.get("candidate_place_ids", []):
        raise AppError(409, "map_identity_changed", "配對候選已更新，請重新確認")
    if payload.action == "confirm" and await duplicate_owner(session, reference, payload.place_id):
        raise AppError(409, "map_identity_duplicate", "此 Google 地點已由其他目錄項目使用")
    now = datetime.now(UTC)
    previous_google_place_id = catalog_google_place_id(row)
    metadata = identity_metadata(row)
    if payload.action == "confirm":
        identities = dict(metadata.get("map_identities") or {})
        identities["google_places"] = MapIdentity(
            provider="google_places",
            place_id=payload.place_id,
            status="verified",
            verified_at=now,
            verified_by_user_id=actor_id,
        ).model_dump(mode="json")
        metadata["map_identities"] = identities
        if isinstance(row, TravelServiceProduct):
            metadata["google_place_id"] = payload.place_id
            row.version += 1
        else:
            row.google_place_id = payload.place_id
    metadata["map_identity_review"] = {
        **state,
        "revision": payload.expected_revision + 1,
        "status": "confirmed" if payload.action == "confirm" else "rejected",
        "reviewed_at": now.isoformat(),
        "note": payload.note.strip(),
    }
    set_identity_metadata(row, metadata)
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action=f"map_identity.{payload.action}",
            target=f"{reference.kind}:{reference.id}",
            metadata_json={
                "place_id": payload.place_id,
                "previous_google_place_id": previous_google_place_id,
                "revision": payload.expected_revision + 1,
                "note": payload.note.strip(),
                "canonical_fingerprint": payload.expected_fingerprint,
            },
        )
    )
    # No publication state, NAVER identity or coordinate/provenance field is changed.
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise AppError(409, "map_identity_duplicate", "此 Google 地點已由其他目錄項目使用") from exc
    await redis.delete(snapshot_key(payload.snapshot_id), comparison_key(reference))
    return item_payload(reference.kind, row)
