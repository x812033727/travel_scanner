from __future__ import annotations

import unicodedata
from datetime import UTC, date, datetime, timedelta
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import and_, delete, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, CurrentUser, OptionalCurrentUser
from app.community.media import check_media
from app.community.pet_models import PetHistory, PetPlace, PetReport, PlaceReference
from app.community.pet_schemas import (
    PetReportInput,
    PetRequirements,
    PetResolveInput,
    PetReview,
    PetRule,
    PlaceInput,
)
from app.community.policy import (
    audit,
    aware,
    cursor_decode,
    cursor_encode,
    digest,
    fail,
    member,
    notify,
    rate,
    require_open,
    settings_for,
)
from app.community.router import OpenSession, Session
from app.db import escape_like
from app.i18n import LOCALES
from app.models import HotelProperty

router = APIRouter(prefix="/pet-friendly", tags=["pet-friendly places"])
admin_router = APIRouter(prefix="/admin/pet-friendly", tags=["pet-friendly administration"])


def fresh(place: PetPlace, days: int, now: datetime | None = None) -> bool:
    return bool(
        place.status == "approved"
        and not place.disputed
        and place.verified_at
        and aware(place.verified_at) >= (now or datetime.now(UTC)) - timedelta(days=days)
        and place.source_url
    )


def eligibility(place: PetPlace, requirements: PetRequirements, days: int) -> list[str]:
    """An empty list means confirmed compatible; missing constraints never mean unrestricted."""
    if not fresh(place, days):
        return ["verification_required"]
    rule_data = next(
        (
            row
            for row in place.policies
            if row.get("species", "").casefold() == requirements.species.casefold()
        ),
        None,
    )
    if rule_data is None:
        return ["species_unknown"]
    rule = PetRule.model_validate(rule_data)
    reasons = []
    if rule.status not in {"allowed", "conditional"}:
        reasons.append("not_allowed" if rule.status == "not_allowed" else "status_unknown")
    if rule.weight_limit == "unknown":
        reasons.append("weight_unknown")
    elif rule.max_weight_kg is not None and requirements.weight_kg > rule.max_weight_kg:
        reasons.append("weight_exceeded")
    if rule.count_limit == "unknown":
        reasons.append("count_unknown")
    elif rule.max_count is not None and requirements.count > rule.max_count:
        reasons.append("count_exceeded")
    if requirements.area == "any":
        if rule.indoor_allowed is not True and rule.outdoor_allowed is not True:
            reasons.append("area_unknown")
    elif getattr(rule, f"{requirements.area}_allowed") is not True:
        reasons.append("area_unavailable")
    if requirements.ground_required and rule.ground_allowed is not True:
        reasons.append("ground_unavailable")
    if requirements.has_stroller and rule.stroller_allowed is not True:
        reasons.append("stroller_unavailable")
    for equipment in ("leash", "carrier", "stroller", "diaper"):
        required = getattr(rule, f"{equipment}_required")
        if not getattr(requirements, f"has_{equipment}") and required is not False:
            reasons.append(f"{equipment}_required" if required else f"{equipment}_unknown")
    if requirements.overnight and rule.overnight_allowed is not True:
        reasons.append("overnight_unavailable")
    return reasons


def public_place(row: PetPlace, days: int) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "name": row.name,
        "names": row.names,
        "kind": row.kind,
        "country": row.country,
        "destination": row.destination,
        "address": row.address,
        "official_url": row.official_url,
        "latitude": row.latitude,
        "longitude": row.longitude,
        "coordinate_source_url": row.coordinate_source_url,
        "policies": row.policies,
        "source_url": row.source_url,
        "verified_at": row.verified_at,
        "verification_current": fresh(row, days),
        "disputed": row.disputed,
    }


async def get_place(session: AsyncSession, identifier: UUID) -> PetPlace:
    row = await session.get(PetPlace, identifier)
    if row is None or row.status != "approved":
        raise fail("community_not_found", 404)
    return row


@router.get("/places")
async def places(
    session: OpenSession,
    q: str = "",
    destination: str = "",
    kind: Literal["restaurant", "cafe", "shop", "lodging", "attraction"] | None = None,
    species: Annotated[str | None, Query(max_length=40)] = None,
    weight_kg: Annotated[float | None, Query(gt=0, le=200)] = None,
    count: Annotated[int, Query(ge=1, le=20)] = 1,
    area: Literal["any", "indoor", "outdoor"] = "any",
    ground_required: bool = False,
    has_leash: bool = True,
    has_carrier: bool = False,
    has_stroller: bool = False,
    has_diaper: bool = False,
    overnight: bool = False,
    include_uncertain: bool = False,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict[str, Any]:
    if max(len(q), len(destination)) > 160 or (species is not None and weight_kg is None):
        raise fail("validation_error", 422)
    requirements = (
        PetRequirements(
            species=species,
            weight_kg=weight_kg,
            count=count,
            area=area,
            ground_required=ground_required,
            has_leash=has_leash,
            has_carrier=has_carrier,
            has_stroller=has_stroller,
            has_diaper=has_diaper,
            overnight=overnight,
        )
        if species and weight_kg
        else None
    )
    settings = await settings_for(session)
    query = select(PetPlace).where(PetPlace.status == "approved")
    if q:
        query = query.where(
            or_(
                PetPlace.name.ilike(f"%{escape_like(q)}%", escape="\\"),
                PetPlace.address.ilike(f"%{escape_like(q)}%", escape="\\"),
                *[
                    PetPlace.names[language].as_string().ilike(f"%{escape_like(q)}%", escape="\\")
                    for language in LOCALES
                ],
            )
        )
    if destination:
        query = query.where(
            PetPlace.destination.ilike(f"%{escape_like(destination)}%", escape="\\")
        )
    if kind:
        query = query.where(PetPlace.kind == kind)
    boundary = cursor_decode(cursor)
    if boundary:
        moment, identifier = boundary
        query = query.where(
            or_(
                PetPlace.created_at > moment,
                and_(PetPlace.created_at == moment, PetPlace.id > identifier),
            )
        )
    # Scan in bounded batches. The cursor tracks examined rows, not just matches.
    rows = (
        await session.scalars(query.order_by(PetPlace.created_at, PetPlace.id).limit(501))
    ).all()
    items = []
    last = None
    for row in rows[:500]:
        last = row
        reasons = (
            eligibility(row, requirements, settings.pet_verification_days)
            if requirements
            else (
                []
                if fresh(row, settings.pet_verification_days)
                and any(
                    policy.get("status") in {"allowed", "conditional"} for policy in row.policies
                )
                else ["verification_required"]
            )
        )
        if not reasons or include_uncertain:
            items.append(
                {**public_place(row, settings.pet_verification_days), "conflicts": reasons}
            )
        if len(items) == limit:
            break
    more = last is not None and (last.id != rows[-1].id or len(rows) > 500)
    return {
        "items": items,
        "next_cursor": cursor_encode(last.created_at, last.id) if more and last else None,
    }


@router.get("/places/{identifier}")
async def place_detail(
    identifier: UUID, session: OpenSession, viewer: OptionalCurrentUser
) -> dict[str, Any]:
    from app.community.policy import visible_profile
    from app.problems import AppError

    row = await get_place(session, identifier)
    days = (await settings_for(session)).pet_verification_days
    reports = (
        await session.scalars(
            select(PetReport)
            .where(PetReport.place_id == row.id, PetReport.status == "approved")
            .order_by(PetReport.created_at.desc())
            .limit(50)
        )
    ).all()
    experiences = []
    for report in reports:
        try:
            profile = await visible_profile(session, report.reporter_id, viewer)
        except AppError:
            continue
        experiences.append(
            {
                "id": str(report.id),
                "body": report.body,
                "source_url": report.source_url,
                "visited_on": report.visited_on,
                "media_ids": report.media_ids,
                "author": {"handle": profile.handle, "display_name": profile.display_name},
            }
        )
    references = (
        await session.scalars(select(PlaceReference).where(PlaceReference.place_id == row.id))
    ).all()
    return {
        **public_place(row, days),
        "experiences": experiences,
        "references": [{"kind": ref.kind, "id": ref.target} for ref in references],
    }


@router.post("/places/{identifier}/match")
async def match_place(
    identifier: UUID, payload: PetRequirements, session: OpenSession
) -> dict[str, Any]:
    row = await get_place(session, identifier)
    conflicts = eligibility(row, payload, (await settings_for(session)).pet_verification_days)
    return {"compatible": not conflicts, "conflicts": conflicts}


@router.post("/places", status_code=201)
async def suggest_place(
    payload: PlaceInput, user: CurrentUser, session: OpenSession
) -> dict[str, str]:
    await require_open(session, "pet_reports_enabled")
    await member(session, user, verified=True)
    await rate(session, user)
    if payload.reference_kind and payload.reference_id:
        await validate_reference(session, payload.reference_kind, payload.reference_id)
        existing = await session.scalar(
            select(PlaceReference).where(
                PlaceReference.kind == payload.reference_kind,
                PlaceReference.target == payload.reference_id,
            )
        )
        if existing:
            return {"id": str(existing.place_id)}

    def normalize(value: str) -> str:
        return " ".join(unicodedata.normalize("NFKC", value).casefold().split())

    identity = "candidate:" + digest(
        [
            payload.country,
            normalize(payload.destination),
            normalize(payload.name),
            normalize(payload.address),
        ]
    )
    existing_place = await session.scalar(select(PetPlace).where(PetPlace.identity_key == identity))
    if existing_place:
        return {"id": str(existing_place.id)}
    place = PetPlace(
        identity_key=identity,
        name=payload.name,
        names=payload.names,
        kind=payload.kind,
        country=payload.country,
        destination=payload.destination,
        address=payload.address,
        official_url=str(payload.official_url) if payload.official_url else None,
    )
    try:
        session.add(place)
        await session.flush()
        if payload.reference_kind and payload.reference_id:
            session.add(
                PlaceReference(
                    place_id=place.id, kind=payload.reference_kind, target=payload.reference_id
                )
            )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise fail("community_version_conflict", 409) from exc
    return {"id": str(place.id)}


async def validate_reference(session: AsyncSession, kind: str, target: str) -> None:
    from app.saved.router import _hotspot, _merchant, _restaurant

    if kind == "hotel":
        try:
            hotel = await session.get(HotelProperty, UUID(target))
        except ValueError as exc:
            raise fail("community_not_found", 404) from exc
        if hotel is None:
            raise fail("community_not_found", 404)
    else:
        await {"hotspot": _hotspot, "merchant": _merchant, "restaurant": _restaurant}[kind](
            session, target
        )


async def place_references(session: AsyncSession, identifier: UUID) -> list[dict[str, str]]:
    return [
        {"kind": ref.kind, "id": ref.target}
        for ref in (
            await session.scalars(
                select(PlaceReference).where(PlaceReference.place_id == identifier)
            )
        ).all()
    ]


@router.post("/places/{identifier}/reports", status_code=201)
async def submit_report(
    identifier: UUID, payload: PetReportInput, user: CurrentUser, session: OpenSession
) -> dict[str, str]:
    await require_open(session, "pet_reports_enabled")
    await member(session, user, verified=True)
    await rate(session, user)
    row = await session.get(PetPlace, identifier)
    if row is None or row.status not in {"approved", "pending"}:
        raise fail("community_not_found", 404)
    if payload.visited_on and payload.visited_on > date.today():
        raise fail("validation_error", 422)
    await check_media(session, user, payload.media_ids)
    report = PetReport(
        place_id=identifier,
        reporter_id=user.id,
        body=payload.body,
        source_url=str(payload.source_url) if payload.source_url else None,
        visited_on=payload.visited_on,
        media_ids=[str(value) for value in payload.media_ids],
        proposed_policies=[rule.model_dump() for rule in payload.proposed_policies],
    )
    session.add(report)
    await session.commit()
    return {"id": str(report.id)}


@admin_router.get("/places")
async def admin_places(
    admin: AdminUser,
    session: Session,
    state: Literal["all", "pending", "approved", "rejected", "disabled"] = "pending",
) -> dict[str, Any]:
    query = select(PetPlace)
    if state != "all":
        query = query.where(PetPlace.status == state)
    rows = (await session.scalars(query.order_by(PetPlace.updated_at.desc()).limit(100))).all()
    days = (await settings_for(session)).pet_verification_days
    return {
        "items": [
            {
                **public_place(row, days),
                "status": row.status,
                "version": row.version,
                "identity_key": row.identity_key,
                "references": await place_references(session, row.id),
            }
            for row in rows
        ]
    }


@admin_router.put("/places/{identifier}")
async def review_place(
    identifier: UUID, payload: PetReview, admin: AdminUser, session: Session
) -> dict[str, Any]:
    row = await session.get(PetPlace, identifier, with_for_update=True)
    if row is None:
        raise fail("community_not_found", 404)
    if row.version != payload.version:
        raise fail("community_version_conflict", 409)
    days = (await settings_for(session)).pet_verification_days
    before = {
        **public_place(row, days),
        "status": row.status,
        "references": await place_references(session, row.id),
    }
    # JSON audit timestamps are explicit ISO strings, not driver-dependent objects.
    before["verified_at"] = aware(row.verified_at).isoformat() if row.verified_at else None
    reports = (
        await session.scalars(
            select(PetReport).where(
                PetReport.id.in_(payload.report_ids), PetReport.place_id == row.id
            )
        )
    ).all()
    if len(reports) != len(set(payload.report_ids)):
        raise fail("community_not_found", 404)
    row.status = payload.status
    if payload.references is not None:
        for reference in payload.references:
            await validate_reference(session, reference.kind, reference.id)
            assigned = await session.scalar(
                select(PlaceReference).where(
                    PlaceReference.kind == reference.kind,
                    PlaceReference.target == reference.id,
                    PlaceReference.place_id != row.id,
                )
            )
            if assigned:
                raise fail("pet_duplicate_identity", 409)
        await session.execute(delete(PlaceReference).where(PlaceReference.place_id == row.id))
        await session.flush()
        for reference in payload.references:
            session.add(PlaceReference(place_id=row.id, kind=reference.kind, target=reference.id))
    row.policies = [rule.model_dump() for rule in payload.policies]
    row.source_url = str(payload.source_url)
    row.latitude, row.longitude = payload.latitude, payload.longitude
    row.coordinate_source_url = (
        str(payload.coordinate_source_url) if payload.coordinate_source_url else None
    )
    if payload.identity_key:
        row.identity_key = payload.identity_key
    row.verified_at = datetime.now(UTC)
    row.verified_by = admin.id
    row.disputed = False
    row.version += 1
    after = {
        **public_place(row, days),
        "status": row.status,
        "references": await place_references(session, row.id),
    }
    after["verified_at"] = row.verified_at.isoformat()
    session.add(
        PetHistory(
            place_id=row.id, actor_id=admin.id, before=before, after=after, reason=payload.reason
        )
    )
    for report in reports:
        report.status = "approved"
        await notify(session, report.reporter_id, None, "review", str(row.id))
    audit(
        session,
        admin,
        "pet_policy_reviewed",
        str(row.id),
        reason=payload.reason,
        before=before,
        after=after,
    )
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise fail("pet_duplicate_identity", 409) from exc
    return {**after, "version": row.version}


@admin_router.get("/places/{identifier}/history")
async def history(identifier: UUID, admin: AdminUser, session: Session) -> dict[str, Any]:
    rows = (
        await session.scalars(
            select(PetHistory)
            .where(PetHistory.place_id == identifier)
            .order_by(PetHistory.created_at.desc())
            .limit(100)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "actor_id": str(row.actor_id),
                "before": row.before,
                "after": row.after,
                "reason": row.reason,
                "created_at": row.created_at,
            }
            for row in rows
        ]
    }


@admin_router.get("/reports")
async def review_reports(admin: AdminUser, session: Session) -> dict[str, Any]:
    rows = (
        await session.scalars(
            select(PetReport)
            .where(PetReport.status == "pending")
            .order_by(PetReport.created_at)
            .limit(100)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(row.id),
                "place_id": str(row.place_id),
                "body": row.body,
                "source_url": row.source_url,
                "visited_on": row.visited_on,
                "media_ids": row.media_ids,
                "proposed_policies": row.proposed_policies,
            }
            for row in rows
        ]
    }


@admin_router.put("/reports/{identifier}")
async def resolve_pet_report(
    identifier: UUID, payload: PetResolveInput, admin: AdminUser, session: Session
) -> dict[str, str]:
    report = await session.get(PetReport, identifier)
    if report is None:
        raise fail("community_not_found", 404)
    # Policy reviews lock the place before reports; preserve that order here.
    place = await session.get(PetPlace, report.place_id, with_for_update=True)
    report = await session.get(PetReport, identifier, with_for_update=True, populate_existing=True)
    assert report is not None
    before = {"status": report.status, "disputed": bool(place and place.disputed)}
    report.status = "approved" if payload.status == "resolved" else "rejected"
    # Accepting a conflicting experience flags the policy; it never overwrites it.
    if (
        report.status == "approved"
        and place
        and not place.disputed
        and (
            payload.flag_conflict
            or (
                report.proposed_policies
                and digest(place.policies) != digest(report.proposed_policies)
            )
        )
    ):
        place.disputed = True
        place.version += 1
        session.add(
            PetHistory(
                place_id=place.id,
                actor_id=admin.id,
                before={"disputed": False, "policies": place.policies},
                after={"disputed": True, "policies": place.policies, "report_id": str(report.id)},
                reason=payload.reason,
            )
        )
    audit(
        session,
        admin,
        "pet_report_reviewed",
        str(report.id),
        reason=payload.reason,
        before=before,
        after={"status": report.status, "disputed": bool(place and place.disputed)},
    )
    await notify(session, report.reporter_id, None, "review", str(report.place_id))
    await session.commit()
    return {"status": report.status}


@admin_router.get("/coverage")
async def coverage(admin: AdminUser, session: Session) -> dict[str, Any]:
    rows = (await session.scalars(select(PetPlace).where(PetPlace.status == "approved"))).all()
    days = (await settings_for(session)).pet_verification_days
    valid = sum(fresh(row, days) for row in rows)
    return {
        "approved": len(rows),
        "verified_current": valid,
        "validity_rate": valid / len(rows) if rows else None,
        "verification_days": days,
    }
