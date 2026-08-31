from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.alerts.monitoring import ResourceType, automatic_monitoring_supported
from app.alerts.policy import evaluate_price_trigger
from app.config import get_settings
from app.db import SessionFactory
from app.infra import get_redis
from app.line.client import LineApiError, LineMessagingClient
from app.models import (
    AlertNotificationDelivery,
    FlightOfferRecord,
    HotelOfferRecord,
    LineConnection,
    PriceAlert,
    PriceAlertCheck,
    PriceSnapshot,
    SearchRequest,
)
from app.providers.flight_keys import ensure_itinerary_key
from app.providers.registry import build_flight_provider, build_hotel_provider
from app.providers.schemas import FlightOffer, HotelOffer
from app.search.schemas import SearchCreate, SearchModule


@dataclass(frozen=True)
class PriceObservation:
    price: Decimal
    currency: str
    provider: str
    title: str
    subtitle: str | None


def _flight_key(offer: FlightOffer) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (
            segment.origin,
            segment.destination,
            segment.departure_time.isoformat(),
            segment.flight_number,
        )
        for segment in offer.segments
    )


def _travel_date(data: dict[str, object], resource_type: str) -> date | None:
    value = data.get("departure_time" if resource_type == "flight" else "check_in")
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


async def _flight_observation(
    session: AsyncSession, alert: PriceAlert, record: FlightOfferRecord
) -> PriceObservation | None:
    search = await session.get(SearchRequest, record.search_id)
    if search is None or not alert.provider:
        return None
    query = SearchCreate.model_validate(search.request_json).model_copy(
        update={"modules": [SearchModule.FLIGHT]}
    )
    settings = await load_runtime_settings(session)
    provider = build_flight_provider(get_redis(), settings, provider_name=alert.provider)
    if provider is None:
        return None
    original = ensure_itinerary_key(FlightOffer.model_validate(record.data))
    selected: FlightOffer | None = None
    try:
        refreshed = await provider.refresh_offer(original, query)
        if refreshed.still_available and refreshed.offer is not None:
            selected = refreshed.offer
        if selected is None:
            offers = [
                ensure_itinerary_key(item)
                for item in await provider.search_flights(query)
            ]
            matches = [
                item
                for item in offers
                if (
                    original.itinerary_key
                    and item.itinerary_key == original.itinerary_key
                    or _flight_key(item) == _flight_key(original)
                )
                and item.cabin_class == original.cabin_class
            ]
            selected = min(matches, key=lambda item: item.total_price, default=None)
    except ConnectionError:
        raise
    if selected is None or selected.currency != alert.currency:
        return None
    airline = selected.marketing_airline or selected.airline
    return PriceObservation(
        selected.total_price,
        selected.currency,
        selected.provider,
        airline,
        f"{selected.origin} → {selected.destination}",
    )


async def _hotel_observation(
    session: AsyncSession, alert: PriceAlert, record: HotelOfferRecord
) -> PriceObservation | None:
    search = await session.get(SearchRequest, record.search_id)
    if search is None or not alert.provider:
        return None
    query = SearchCreate.model_validate(search.request_json).model_copy(
        update={"modules": [SearchModule.HOTEL]}
    )
    settings = await load_runtime_settings(session)
    provider = build_hotel_provider(get_redis(), settings, provider_name=alert.provider)
    if provider is None:
        return None
    original = HotelOffer.model_validate(record.data)
    offers = await provider.search_hotels(query)
    matches = [
        item
        for item in offers
        if item.hotel_id == original.hotel_id
        and item.check_in.date() == original.check_in.date()
        and item.check_out.date() == original.check_out.date()
        and (not original.refundable or item.refundable)
        and (not original.breakfast_included or item.breakfast_included)
        and item.currency == alert.currency
    ]
    selected = min(matches, key=lambda item: item.total_price, default=None)
    if selected is None:
        return None
    return PriceObservation(
        selected.total_price,
        selected.currency,
        selected.provider,
        selected.hotel_name,
        f"{selected.check_in:%Y-%m-%d} 至 {selected.check_out:%Y-%m-%d}",
    )


async def _load_record(
    session: AsyncSession, alert: PriceAlert
) -> FlightOfferRecord | HotelOfferRecord | None:
    if alert.resource_type == "flight":
        return cast(
            FlightOfferRecord | None,
            await session.scalar(
                select(FlightOfferRecord)
                .join(SearchRequest, SearchRequest.id == FlightOfferRecord.search_id)
                .where(
                    FlightOfferRecord.public_offer_id == alert.resource_id,
                    SearchRequest.user_id == alert.user_id,
                )
                .order_by(FlightOfferRecord.updated_at.desc())
                .limit(1)
            ),
        )
    if alert.resource_type == "hotel":
        return cast(
            HotelOfferRecord | None,
            await session.scalar(
                select(HotelOfferRecord)
                .join(SearchRequest, SearchRequest.id == HotelOfferRecord.search_id)
                .where(
                    HotelOfferRecord.public_offer_id == alert.resource_id,
                    SearchRequest.user_id == alert.user_id,
                )
                .order_by(HotelOfferRecord.updated_at.desc())
                .limit(1)
            ),
        )
    return None


async def refresh_alert(alert_id: UUID) -> UUID | None:
    settings = get_settings()
    async with SessionFactory() as session:
        alert = await session.get(PriceAlert, alert_id)
        if alert is None or not alert.active or alert.monitoring_mode != "automatic":
            return None
        now = datetime.now(UTC)
        record = await _load_record(session, alert)
        if record is None or not automatic_monitoring_supported(
            cast(ResourceType, alert.resource_type), alert.provider
        ):
            alert.monitoring_mode = "manual_only"
            alert.monitoring_status = "manual_only"
            alert.next_check_at = None
            await session.commit()
            return None
        if (travel_date := _travel_date(record.data, alert.resource_type)) and (
            travel_date < now.date()
        ):
            alert.active = False
            alert.monitoring_status = "completed"
            alert.completed_at = now
            alert.next_check_at = None
            await session.commit()
            return None
        previous = alert.last_observed_price or alert.baseline_price
        try:
            observation = (
                await _flight_observation(session, alert, record)
                if isinstance(record, FlightOfferRecord)
                else await _hotel_observation(session, alert, record)
            )
        except (ConnectionError, ValueError) as exc:
            alert.monitoring_status = "error"
            alert.consecutive_failures += 1
            alert.last_checked_at = now
            alert.next_check_at = now + timedelta(
                seconds=settings.price_alert_check_interval_seconds
            )
            session.add(
                PriceAlertCheck(
                    alert_id=alert.id,
                    status="error",
                    previous_price=previous,
                    currency=alert.currency,
                    provider=alert.provider,
                    detail=str(exc)[:1000],
                    checked_at=now,
                )
            )
            await session.commit()
            return None
        if observation is None:
            alert.monitoring_status = "unavailable"
            alert.consecutive_failures += 1
            alert.last_checked_at = now
            alert.next_check_at = now + timedelta(
                seconds=settings.price_alert_check_interval_seconds
            )
            session.add(
                PriceAlertCheck(
                    alert_id=alert.id,
                    status="unavailable",
                    previous_price=previous,
                    currency=alert.currency,
                    provider=alert.provider,
                    detail="原供應商未回傳可比較的相同商品",
                    checked_at=now,
                )
            )
            await session.commit()
            return None
        decision = evaluate_price_trigger(
            target_price=alert.target_price,
            baseline_price=alert.baseline_price,
            last_notified_price=alert.last_notified_price,
            armed=alert.armed,
            observed_price=observation.price,
        )
        alert.monitoring_status = "scheduled"
        alert.consecutive_failures = 0
        alert.last_observed_price = observation.price
        alert.last_checked_at = now
        alert.next_check_at = now + timedelta(seconds=settings.price_alert_check_interval_seconds)
        session.add(
            PriceSnapshot(
                resource_type=alert.resource_type,
                resource_id=alert.resource_id,
                price=observation.price,
                currency=observation.currency,
                captured_at=now,
            )
        )
        session.add(
            PriceAlertCheck(
                alert_id=alert.id,
                status="triggered" if decision.should_notify else "checked",
                previous_price=previous,
                observed_price=observation.price,
                currency=observation.currency,
                provider=observation.provider,
                checked_at=now,
            )
        )
        connection = await session.scalar(
            select(LineConnection).where(
                LineConnection.user_id == alert.user_id,
                LineConnection.friend_status.is_(True),
            )
        )
        delivery: AlertNotificationDelivery | None = None
        if decision.should_notify and decision.event_type and connection is not None:
            delivery = AlertNotificationDelivery(
                alert_id=alert.id,
                line_connection_id=connection.id,
                dedupe_key=(
                    f"{alert.id}:{decision.event_type}:{now:%Y%m%d%H%M}:"
                    f"{observation.price}"
                ),
                event_type=decision.event_type,
                observed_price=observation.price,
                status="pending",
                attempts=0,
                next_attempt_at=now,
                created_at=now,
            )
            session.add(delivery)
            alert.armed = decision.next_armed
            alert.last_notified_price = observation.price
        elif not decision.should_notify:
            alert.armed = decision.next_armed
        await session.commit()
        return delivery.id if delivery else None


async def _delivery_context(
    session: AsyncSession, alert: PriceAlert
) -> tuple[str, str | None]:
    record = await _load_record(session, alert)
    if isinstance(record, FlightOfferRecord):
        data = record.data or {}
        title = str(data.get("marketing_airline") or data.get("airline") or "航班價格")
        origin, destination = data.get("origin"), data.get("destination")
        subtitle = f"{origin} → {destination}" if origin and destination else None
        return title, subtitle
    if isinstance(record, HotelOfferRecord):
        data = record.data or {}
        return str(data.get("hotel_name") or "住宿價格"), str(data.get("address") or "") or None
    return "價格通知", None


def _price_text(value: Decimal, currency: str) -> str:
    return f"{currency} {value:,.0f}"


async def deliver_notification(delivery_id: UUID) -> bool:
    settings = get_settings()
    async with SessionFactory() as session:
        delivery = await session.get(AlertNotificationDelivery, delivery_id)
        if delivery is None or delivery.status == "sent":
            return True
        alert = await session.get(PriceAlert, delivery.alert_id)
        connection = (
            await session.get(LineConnection, delivery.line_connection_id)
            if delivery.line_connection_id
            else None
        )
        if alert is None or connection is None or not connection.friend_status:
            delivery.status = "cancelled"
            delivery.last_error = "LINE connection is unavailable"
            await session.commit()
            return False
        title, subtitle = await _delivery_context(session, alert)
        target = (
            f"目標 {_price_text(alert.target_price, alert.currency)}"
            if alert.target_price is not None
            else "已刷新低價"
        )
        detail = "\n".join(
            item
            for item in (
                subtitle,
                f"目前 {_price_text(delivery.observed_price, alert.currency)}",
                target,
                f"檢查時間 {datetime.now(UTC):%Y-%m-%d %H:%M} UTC",
            )
            if item
        )
        messages = [
            {
                "type": "template",
                "altText": f"{title} 已達價格通知條件",
                "template": {
                    "type": "buttons",
                    "title": "價格到價通知",
                    "text": f"{title}\n{detail}"[:160],
                    "actions": [
                        {
                            "type": "uri",
                            "label": "查看價格通知",
                            "uri": f"{settings.next_public_site_url.rstrip('/')}/alerts",
                        }
                    ],
                },
            }
        ]
        try:
            await LineMessagingClient(settings).push_messages(
                connection.line_user_id, messages, retry_key=delivery.id
            )
        except LineApiError as exc:
            delivery.attempts += 1
            delivery.last_error = str(exc)
            if exc.retryable and delivery.attempts < settings.price_alert_delivery_max_attempts:
                delivery.status = "retry"
                delivery.next_attempt_at = datetime.now(UTC) + timedelta(
                    minutes=2 ** delivery.attempts
                )
            else:
                delivery.status = "failed"
            connection.last_delivery_error = str(exc)
            await session.commit()
            return False
        delivery.status = "sent"
        delivery.attempts += 1
        delivery.sent_at = datetime.now(UTC)
        delivery.last_error = None
        connection.last_delivery_at = delivery.sent_at
        connection.last_delivery_error = None
        await session.commit()
        return True
