from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.i18n import Locale
from app.infra import get_redis
from app.ui_text.schemas import (
    KEY_PATTERN,
    NAMESPACE_PATTERN,
    UI_TEXT_KEY_MAX_LENGTH,
    PublicUiText,
    UiTextBatchWrite,
    UiTextSnapshot,
    UiTextWrite,
)
from app.ui_text.service import (
    batch_ui_text,
    public_ui_text,
    reset_ui_text,
    ui_text_snapshot,
    upsert_ui_text,
)

admin_router = APIRouter(prefix="/admin/ui-text", tags=["admin ui text"])
runtime_router = APIRouter(prefix="/runtime", tags=["runtime configuration"])
Session = Annotated[AsyncSession, Depends(get_session)]
NamespacePath = Annotated[str, Path(pattern=NAMESPACE_PATTERN, max_length=64)]
KeyPath = Annotated[str, Path(pattern=KEY_PATTERN, max_length=UI_TEXT_KEY_MAX_LENGTH)]
NamespaceQuery = Annotated[str | None, Query(pattern=NAMESPACE_PATTERN, max_length=64)]


@runtime_router.get("/ui-text", response_model=PublicUiText)
async def get_public_ui_text(
    response: Response, session: Session, locale: Locale = "zh-TW"
) -> PublicUiText:
    # Anonymous like site-visibility: the web server merges this into every page render.
    response.headers["Cache-Control"] = "no-store"
    return await public_ui_text(session, get_redis(), locale)


@admin_router.get("", response_model=UiTextSnapshot)
async def get_ui_text(
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
    namespace: NamespaceQuery = None,
) -> UiTextSnapshot:
    _ = user
    return await ui_text_snapshot(session, locale, namespace)


@admin_router.put("/{locale}/{namespace}/{key}", response_model=UiTextSnapshot)
async def put_ui_text(
    locale: Locale,
    namespace: NamespacePath,
    key: KeyPath,
    payload: UiTextWrite,
    user: AdminUser,
    session: Session,
) -> UiTextSnapshot:
    return await upsert_ui_text(session, get_redis(), user, locale, namespace, key, payload)


@admin_router.delete("/{locale}/{namespace}/{key}", response_model=UiTextSnapshot)
async def delete_ui_text(
    locale: Locale,
    namespace: NamespacePath,
    key: KeyPath,
    user: AdminUser,
    session: Session,
) -> UiTextSnapshot:
    return await reset_ui_text(session, get_redis(), user, locale, namespace, key)


@admin_router.post("/batch", response_model=UiTextSnapshot)
async def post_ui_text_batch(
    payload: UiTextBatchWrite, user: AdminUser, session: Session
) -> UiTextSnapshot:
    return await batch_ui_text(session, get_redis(), user, payload)
