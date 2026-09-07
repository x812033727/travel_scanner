"""Durable account work. RQ wakes it promptly; the sweeper retries missed wakeups."""

from __future__ import annotations

import asyncio
import smtplib
import ssl
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage
from uuid import UUID

from redis import Redis as SyncRedis
from redis.exceptions import RedisError
from rq import Queue, Retry
from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import decrypt_secrets
from app.community.media import raw_key, storage
from app.community.models import (
    AccountToken,
    Collection,
    CollectionItem,
    Comment,
    CommunityMetric,
    Event,
    Job,
    Media,
    Notification,
    Post,
    PostRevision,
    Profile,
    Reaction,
    Relationship,
    Report,
    Translation,
)
from app.community.pet_models import PetReport
from app.community.policy import digest
from app.config import get_settings
from app.db import Base, SessionFactory, engine
from app.models import (
    FlightStatusLookup,
    LineConnection,
    PriceAlert,
    SearchRequest,
    TripDayNote,
    TripPlan,
    TripPlanItem,
    User,
    UserAuthIdentity,
)

MAIL_COPY = {
    "zh-TW": (
        "Mokaair 帳號確認",
        "請開啟下方連結完成帳號操作。連結將在 30 分鐘後失效。",
        "若不是你提出的請求，請忽略這封信。",
    ),
    "zh-CN": (
        "Mokaair 账号确认",
        "请打开下方链接完成账号操作。链接将在 30 分钟后失效。",
        "如果不是你提出的请求，请忽略此邮件。",
    ),
    "en": (
        "Confirm your Mokaair account request",
        "Open the link below to finish your account request. It expires in 30 minutes.",
        "If you did not request this, ignore this email.",
    ),
    "ja": (
        "Mokaair アカウントの確認",
        "以下のリンクからアカウント操作を完了してください。有効期限は30分です。",
        "お心当たりがない場合は、このメールを無視してください。",
    ),
    "ko": (
        "Mokaair 계정 요청 확인",
        "아래 링크를 열어 계정 요청을 완료하세요. 링크는 30분 후 만료됩니다.",
        "본인이 요청하지 않았다면 이 이메일을 무시하세요.",
    ),
}


def enqueue_jobs() -> bool:
    try:
        with SyncRedis.from_url(get_settings().redis_url) as connection:
            Queue("community", connection=connection).enqueue(
                "app.community.jobs.run_jobs",
                job_timeout=300,
                retry=Retry(max=5, interval=[60, 300, 900, 3600, 7200]),
            )
        return True
    except RedisError:
        return False


def send_mail(encrypted: str) -> None:
    settings = get_settings()
    values = decrypt_secrets(encrypted)
    subject, instruction, ignore = MAIL_COPY.get(values["locale"], MAIL_COPY["en"])
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = settings.community_mail_from
    email["To"] = values["to"]
    email.set_content(f"{instruction}\n\n{values['url']}\n\n{ignore}")
    if not settings.community_smtp_host:
        raise RuntimeError("community_mail_unavailable")
    if settings.production and not settings.community_smtp_starttls:
        raise RuntimeError("community_mail_requires_tls")
    with smtplib.SMTP(
        settings.community_smtp_host, settings.community_smtp_port, timeout=15
    ) as smtp:
        if settings.community_smtp_starttls:
            smtp.starttls(context=ssl.create_default_context())
        if settings.community_smtp_username:
            smtp.login(settings.community_smtp_username, settings.community_smtp_password or "")
        smtp.send_message(email)


async def erase_account(session: AsyncSession, user_id: UUID) -> None:
    # Serialize erasure with post-provider translation cache writes, so an
    # in-flight translation cannot recreate personal content after cleanup.
    user = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if user is None or user.deleted_at is None:
        return
    media = (await session.scalars(select(Media).where(Media.owner_id == user_id))).all()
    if media:
        client, bucket = storage(), get_settings().community_s3_bucket
        for item in media:
            for key in (item.object_key, item.thumbnail_key, raw_key(item)):
                await asyncio.to_thread(client.delete_object, Bucket=bucket, Key=key)
            item.deleted_at = datetime.now(UTC)
            item.alt = ""
    profile = await session.get(Profile, user_id)
    if profile:
        profile.handle = f"deleted_{user_id.hex[:22]}"
        profile.display_name = ""
        profile.bio = ""
        profile.languages = []
        profile.destinations = []
        profile.avatar_id = None
        profile.notification_preferences = {}
    # Retain FK identities for ledger and already-delivered conversations; erase PII.
    user.email = f"{user.id.hex}@deleted.invalid"
    user.password_hash = None
    user.email_verified_at = None
    for identity in (
        await session.scalars(
            select(UserAuthIdentity).where(
                UserAuthIdentity.user_id == user_id,
            )
        )
    ).all():
        identity.revoked_at = datetime.now(UTC)
        identity.revocation_pending = bool(
            identity.provider == "apple" and identity.refresh_token_encrypted
        )
        identity.provider_email = None
        identity.subject = f"deleted:{identity.id}"
        if not identity.revocation_pending:
            identity.refresh_token_encrypted = None
    post_ids = select(Post.id).where(Post.author_id == user_id)
    fingerprints = [
        digest([revision.locale, revision.title + "\n\n" + revision.body])
        for revision in (
            await session.scalars(select(PostRevision).where(PostRevision.post_id.in_(post_ids)))
        ).all()
    ]
    fingerprints.extend(
        digest([comment.locale, comment.body])
        for comment in (
            await session.scalars(select(Comment).where(Comment.author_id == user_id))
        ).all()
    )
    if fingerprints:
        await session.execute(delete(Translation).where(Translation.source_hash.in_(fingerprints)))
    await session.execute(
        update(PostRevision)
        .where(PostRevision.post_id.in_(post_ids))
        .values(
            title="",
            body="",
            destination="",
            topics=[],
            place_ids=[],
            place_refs=[],
            media_ids=[],
            itinerary=None,
            allow_fork=False,
        )
    )
    await session.execute(
        update(Comment)
        .where(Comment.author_id == user_id)
        .values(body="", deleted_at=datetime.now(UTC))
    )
    collections = select(Collection.id).where(Collection.user_id == user_id)
    await session.execute(
        delete(CollectionItem).where(CollectionItem.collection_id.in_(collections))
    )
    await session.execute(delete(Collection).where(Collection.user_id == user_id))
    await session.execute(
        delete(Relationship).where(
            or_(
                Relationship.actor_id == user_id,
                Relationship.target_id == user_id,
            )
        )
    )
    await session.execute(delete(Reaction).where(Reaction.user_id == user_id))
    await session.execute(
        update(PetReport)
        .where(PetReport.reporter_id == user_id)
        .values(
            body="",
            source_url=None,
            visited_on=None,
            media_ids=[],
            proposed_policies=[],
            status="rejected",
        )
    )
    await session.execute(
        update(Report).where(Report.reporter_id == user_id).values(reason="", evidence={})
    )
    for name in (
        "food_favorites",
        "food_merchant_favorites",
        "hotspot_favorites",
        "restaurant_favorites",
    ):
        table = Base.metadata.tables[name]
        await session.execute(delete(table).where(table.c.user_id == user_id))
    await session.execute(
        update(Job)
        .where(Job.user_id == user_id, Job.kind == "mail")
        .values(payload_encrypted=None, status="completed")
    )
    await session.execute(delete(AccountToken).where(AccountToken.user_id == user_id))
    await session.execute(delete(CommunityMetric).where(CommunityMetric.user_id == user_id))
    await session.execute(delete(Event).where(Event.recipient_id == user_id))
    await session.execute(delete(Notification).where(Notification.recipient_id == user_id))
    await session.execute(
        update(Notification).where(Notification.actor_id == user_id).values(actor_id=None)
    )
    trips = select(TripPlan.id).where(TripPlan.user_id == user_id)
    # These are personal travel records, not the platform usage ledger. Retain
    # only a de-identified trip shell for already-recorded fork references.
    for name in (
        "trip_route_segments",
        "trip_route_day_settings",
        "trip_place_candidates",
        "trip_expenses",
        "optimization_scores",
        "price_components",
    ):
        table = Base.metadata.tables[name]
        await session.execute(delete(table).where(table.c.trip_plan_id.in_(trips)))
    await session.execute(delete(TripDayNote).where(TripDayNote.trip_plan_id.in_(trips)))
    await session.execute(
        update(TripPlanItem)
        .where(TripPlanItem.trip_plan_id.in_(trips))
        .values(
            notes=None,
            data={},
            title="",
            location_name="",
            names_json={},
            day_date=None,
            start_time=None,
            end_time=None,
            latitude=None,
            longitude=None,
            coordinate_source_url=None,
            coordinate_source_type=None,
            coordinate_verified_at=None,
            provider_place_id=None,
            offer_id=None,
            location_source=None,
        )
    )
    await session.execute(
        update(TripPlan)
        .where(TripPlan.user_id == user_id)
        .values(
            name="",
            notes=None,
            data={},
            cover_image_url=None,
            destination_name=None,
            destination_place_id=None,
            start_date=None,
            end_date=None,
            total_price=0,
            budget_amount=None,
        )
    )
    await session.execute(
        update(SearchRequest)
        .where(SearchRequest.user_id == user_id)
        .values(request_json={}, result_json={}, warnings_json=[])
    )
    await session.execute(
        update(FlightStatusLookup)
        .where(FlightStatusLookup.user_id == user_id)
        .values(query_json={}, result_json={})
    )
    searches = select(SearchRequest.id).where(SearchRequest.user_id == user_id)
    for name in ("flight_offers", "hotel_offers", "activity_offers", "transport_offers"):
        table = Base.metadata.tables[name]
        await session.execute(update(table).where(table.c.search_id.in_(searches)).values(data={}))
    table = Base.metadata.tables["search_constraints"]
    await session.execute(delete(table).where(table.c.search_id.in_(searches)))
    alerts = select(PriceAlert.id).where(PriceAlert.user_id == user_id)
    for name in ("alert_notification_deliveries", "price_alert_checks"):
        table = Base.metadata.tables[name]
        await session.execute(delete(table).where(table.c.alert_id.in_(alerts)))
    await session.execute(
        update(PriceAlert).where(PriceAlert.user_id == user_id).values(active=False, monitor_key={})
    )
    for line in (
        await session.scalars(select(LineConnection).where(LineConnection.user_id == user_id))
    ).all():
        line.friend_status = False
        line.display_name = ""
        line.last_delivery_error = None
        line.line_user_id = f"deleted:{line.id}"


async def drain_jobs() -> None:
    for _ in range(25):
        async with SessionFactory() as session:
            row = await session.scalar(
                select(Job)
                .where(
                    Job.status == "pending",
                    Job.available_at <= datetime.now(UTC),
                )
                .order_by(Job.created_at)
                .with_for_update(skip_locked=True)
                .limit(1)
            )
            if row is None:
                break
            try:
                async with session.begin_nested():
                    if row.kind == "mail" and row.payload_encrypted:
                        user = await session.get(User, row.user_id)
                        if (
                            user
                            and user.is_active
                            and datetime.now(UTC) - row.created_at.replace(tzinfo=UTC)
                            < timedelta(minutes=30)
                        ):
                            await asyncio.to_thread(send_mail, row.payload_encrypted)
                    elif row.kind == "delete_account":
                        await erase_account(session, row.user_id)
                row.status = "completed"
                row.payload_encrypted = None
            except Exception:
                # Never log mail bodies, tokens or storage credentials. The durable
                # status and attempt count are visible in the administration queue.
                row.attempts += 1
                row.available_at = datetime.now(UTC) + timedelta(
                    seconds=min(3600, 60 * 2 ** min(row.attempts, 6))
                )
                if row.kind == "mail" and row.attempts >= 5:
                    row.status = "failed"
                    row.payload_encrypted = None
            await session.commit()
    # Revocation jobs must be enqueued after the pending flag commits. A failed
    # Redis wakeup is retried on the next durable sweep.
    async with SessionFactory() as session:
        identities = (
            await session.scalars(
                select(UserAuthIdentity)
                .join(User, User.id == UserAuthIdentity.user_id)
                .where(User.deleted_at.is_not(None), UserAuthIdentity.revocation_pending.is_(True))
                .limit(100)
            )
        ).all()
        from app.auth.jobs import enqueue_provider_revocation

        for identity in identities:
            enqueue_provider_revocation(identity.id)


def run_jobs() -> None:
    async def run() -> None:
        try:
            await drain_jobs()
        finally:
            await engine.dispose()

    asyncio.run(run())


async def sweep() -> None:
    while True:
        enqueue_jobs()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(sweep())
