"""Hotel workspace: scoped reads/imports and a narrow versioned catalog merge."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import ValidationError

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser, CurrentUser, cached_admin_capabilities
from app.models import TravelServiceConfig, User
from app.travel_services.admin import (
    Stay22Provider,
    Stay22Readiness,
    audit,
    locked_catalog_config,
    overview_data,
    preview_import_data,
    require_stay22_management,
)
from app.travel_services.imports import commit_import
from app.travel_services.router import Session
from app.travel_services.schemas import CsvInput, HotelConfigPatch, Stay22Config
from app.travel_services.service import fail

router = APIRouter(prefix="/admin/hotels", tags=["admin hotels"])


async def hotel_config_user(payload: HotelConfigPatch, user: CurrentUser) -> User:
    from app.problems import AppError

    fields = payload.model_fields_set - {"version"}
    capabilities = cached_admin_capabilities(user)
    if "stay22" in fields:
        require_stay22_management(user)
    if (fields - {"stay22"} or not fields) and "content.manage" not in capabilities:
        raise AppError(403, "admin_capability_required", "目前管理員角色沒有這項操作權限")
    return user


HotelConfigUser = Annotated[User, Depends(hotel_config_user)]


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
    booking_provider: Stay22Provider | None = None,
    booking_readiness: Stay22Readiness | None = None,
) -> dict[str, Any]:
    result = await overview_data(
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
        booking_provider=booking_provider,
        booking_readiness=booking_readiness,
    )
    result["can_manage_stay22"] = "settings.manage" in cached_admin_capabilities(user)
    return result


@router.patch("/config")
async def patch_config(
    payload: HotelConfigPatch, user: HotelConfigUser, session: Session
) -> dict[str, Any]:
    if "stay22" in payload.model_fields_set:
        require_stay22_management(user)
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
    if "stay22" in patch:
        # Older clients know only Allez settings. Their save must not erase the
        # newer script mode/identity or reactivate an incomplete configuration.
        merged_stay22 = {**data.get("stay22", {}), **patch.pop("stay22")}
        try:
            Stay22Config.model_validate(merged_stay22)
        except ValidationError as exc:
            raise fail("stay22_config_invalid") from exc
        data["stay22"] = merged_stay22
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
