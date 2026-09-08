"""Hotel workspace: scoped reads/imports and a narrow versioned catalog merge."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Query

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.models import TravelServiceConfig
from app.travel_services.admin import (
    audit,
    locked_catalog_config,
    overview_data,
    preview_import_data,
)
from app.travel_services.imports import commit_import
from app.travel_services.router import Session
from app.travel_services.schemas import CsvInput, HotelConfigPatch
from app.travel_services.service import fail

router = APIRouter(prefix="/admin/hotels", tags=["admin hotels"])


@router.get("")
async def overview(
    user: AdminUser,
    session: Session,
    destination_id: str | None = None,
    status: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(60, ge=1, le=100),
    offer_status: str | None = None,
    offer_brand_id: UUID | None = None,
    offer_review_due: bool = False,
    missing_options: bool = False,
) -> dict[str, Any]:
    return await overview_data(
        session,
        domain="hotels",
        destination_id=destination_id,
        status=status,
        offset=offset,
        limit=limit,
        offer_status=offer_status,
        offer_brand_id=offer_brand_id,
        offer_review_due=offer_review_due,
        missing_options=missing_options,
    )


@router.patch("/config")
async def patch_config(
    payload: HotelConfigPatch, user: AdminUser, session: Session
) -> dict[str, Any]:
    row = await locked_catalog_config(session)
    if payload.version != (row.version if row else 0):
        await session.rollback()
        raise fail("service_version_conflict", 409)
    data = dict(row.data) if row else {}
    patch = payload.model_dump(exclude_unset=True, exclude={"version"})
    if "hotel_enabled" in patch:
        kinds = [kind for kind in data.get("enabled_kinds", []) if kind != "hotel"]
        if patch.pop("hotel_enabled"):
            kinds.append("hotel")
        data["enabled_kinds"] = kinds
    if "hotel_quote_policies" in patch:
        # Provider policies not mentioned by this request retain their existing values.
        data["hotel_quote_policies"] = {
            **data.get("hotel_quote_policies", {}),
            **patch.pop("hotel_quote_policies"),
        }
    data.update(patch)
    if row:
        row.data = data
        row.version += 1
    else:
        row = TravelServiceConfig(id=1, data=data, version=1)
        session.add(row)
    audit(
        session,
        user,
        "hotel_config",
        "hotels",
        {"fields": sorted(payload.model_fields_set - {"version"})},
    )
    await session.commit()
    return {"version": row.version}


@router.post("/imports/preview")
async def preview_import(payload: CsvInput, user: AdminUser, session: Session) -> dict[str, Any]:
    return await preview_import_data(payload, user, session, hotel_only=True)


@router.post("/imports/{run_id}/commit")
async def apply_import(run_id: UUID, user: AdminUser, session: Session) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    result = await commit_import(
        session, run_id, settings.travelpayouts_project_id, required_kind="hotel",
        klook_affiliate_id=settings.klook_affiliate_id,
    )
    audit(session, user, "hotel_import_commit", str(run_id), result)
    await session.commit()
    return result
