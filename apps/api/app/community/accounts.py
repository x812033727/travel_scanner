from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import encrypt_secrets
from app.auth.service import CurrentUser, find_user_by_email, hash_password, is_admin_user
from app.community.models import AccountToken, Job, Post, Profile
from app.community.policy import aware, fail
from app.community.schemas import DeleteAccountInput, EmailRequest, ResetInput, TokenInput
from app.config import get_settings
from app.db import get_session
from app.infra import client_ip, enforce_named_rate_limit
from app.models import TripPlan, TripShare, User

router = APIRouter(prefix="/auth", tags=["account safety"])
Session = Annotated[AsyncSession, Depends(get_session)]


def smtp_ready() -> bool:
    settings = get_settings()
    return bool(settings.community_smtp_host and settings.community_mail_from)


async def request_mail(session: AsyncSession, user: User, purpose: str, locale: str) -> None:
    if not smtp_ready():
        raise fail("community_mail_unavailable", 503)
    now = datetime.now(UTC)
    await session.execute(
        update(AccountToken)
        .where(
            AccountToken.user_id == user.id,
            AccountToken.purpose == purpose,
            AccountToken.consumed_at.is_(None),
        )
        .values(consumed_at=now)
    )
    token = secrets.token_urlsafe(32)
    session.add(
        AccountToken(
            user_id=user.id,
            purpose=purpose,
            digest=hashlib.sha256(token.encode()).hexdigest(),
            auth_version=user.auth_version,
            expires_at=now + timedelta(minutes=30),
        )
    )
    origin = get_settings().next_public_site_url.rstrip("/")
    # Fragments are not sent in HTTP requests, access logs or Referer headers.
    url = f"{origin}/{locale}/account/confirm?purpose={purpose}#token={token}"
    session.add(
        Job(
            kind="mail",
            user_id=user.id,
            payload_encrypted=encrypt_secrets(
                {
                    "to": user.email,
                    "url": url,
                    "purpose": purpose,
                    "locale": locale,
                }
            ),
        )
    )
    await session.commit()
    from app.community.jobs import enqueue_jobs

    enqueue_jobs()


async def consume(session: AsyncSession, token: str, purpose: str) -> tuple[AccountToken, User]:
    row = await session.scalar(
        select(AccountToken)
        .where(
            AccountToken.digest == hashlib.sha256(token.encode()).hexdigest(),
            AccountToken.purpose == purpose,
        )
        .with_for_update()
    )
    if row is None or row.consumed_at is not None or aware(row.expires_at) <= datetime.now(UTC):
        raise fail("community_token_invalid", 400)
    user = await session.scalar(select(User).where(User.id == row.user_id).with_for_update())
    if user is None or not user.is_active or row.auth_version != user.auth_version:
        raise fail("community_token_invalid", 400)
    row.consumed_at = datetime.now(UTC)
    return row, user


@router.get("/account-capabilities")
async def account_capabilities(response: Response) -> dict[str, bool]:
    response.headers["Cache-Control"] = "no-store"
    return {"email_available": smtp_ready()}


@router.post("/request-verification", status_code=202)
async def verification_request(user: CurrentUser, session: Session) -> dict[str, bool]:
    await enforce_named_rate_limit("verification", str(user.id), limit=3, window_seconds=3600)
    if user.email_verified_at is None:
        await request_mail(session, user, "verify", user.preferred_locale)
    return {"accepted": True}


@router.post("/verify-email")
async def verify_email(payload: TokenInput, session: Session) -> dict[str, bool]:
    _, user = await consume(session, payload.token, "verify")
    user.email_verified_at = datetime.now(UTC)
    await session.commit()
    return {"verified": True}


@router.post("/forgot-password", status_code=202)
async def forgot_password(
    payload: EmailRequest, request: Request, session: Session
) -> dict[str, bool]:
    if not smtp_ready():
        raise fail("community_mail_unavailable", 503)
    await enforce_named_rate_limit("reset-ip", client_ip(request), limit=10, window_seconds=3600)
    await enforce_named_rate_limit(
        "reset-email", str(payload.email).lower(), limit=3, window_seconds=3600
    )
    user = await find_user_by_email(session, str(payload.email))
    if user is not None and user.is_active and user.password_hash:
        await request_mail(session, user, "reset", payload.locale)
    # Never disclose whether an account exists or uses a password.
    return {"accepted": True}


@router.post("/reset-password")
async def reset_password(
    payload: ResetInput, response: Response, session: Session
) -> dict[str, bool]:
    _, user = await consume(session, payload.token, "reset")
    user.password_hash = hash_password(payload.password)
    user.auth_version += 1
    await session.commit()
    response.delete_cookie("travel_access", path="/")
    return {"reset": True}


@router.post("/request-deletion", status_code=202)
async def deletion_request(user: CurrentUser, session: Session) -> dict[str, bool]:
    # Existing administrator self-suspension restrictions still apply.
    if is_admin_user(user):
        raise fail("community_admin_deletion", 403)
    await enforce_named_rate_limit("delete-account", str(user.id), limit=3, window_seconds=3600)
    await request_mail(session, user, "delete", user.preferred_locale)
    return {"accepted": True}


@router.post("/delete-account", status_code=202)
async def delete_account(
    payload: DeleteAccountInput, response: Response, session: Session
) -> dict[str, Any]:
    _, user = await consume(session, payload.token, "delete")
    if is_admin_user(user):
        raise fail("community_admin_deletion", 403)
    now = datetime.now(UTC)
    user.is_active = False
    user.deleted_at = now
    user.auth_version += 1
    profile = await session.get(Profile, user.id)
    if profile:
        profile.deleted_at = now
    await session.execute(update(Post).where(Post.author_id == user.id).values(state="deleted"))
    await session.execute(
        update(TripShare)
        .where(
            TripShare.trip_plan_id.in_(select(TripPlan.id).where(TripPlan.user_id == user.id)),
        )
        .values(revoked_at=now)
    )
    session.add(Job(kind="delete_account", user_id=user.id))
    await session.commit()
    response.delete_cookie("travel_access", path="/")
    from app.community.jobs import enqueue_jobs

    enqueue_jobs()
    return {"accepted": True}
