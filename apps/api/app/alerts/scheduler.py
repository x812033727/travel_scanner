import asyncio
from datetime import UTC, datetime, timedelta

from redis import Redis
from rq import Queue
from sqlalchemy import select

from app.config import get_settings
from app.db import SessionFactory
from app.models import AlertNotificationDelivery, PriceAlert


async def enqueue_due() -> dict[str, int]:
    settings = get_settings()
    now = datetime.now(UTC)
    queued_alerts: list[str] = []
    queued_deliveries: list[str] = []
    async with SessionFactory() as session:
        alerts = list(
            (
                await session.scalars(
                    select(PriceAlert)
                    .where(
                        PriceAlert.active.is_(True),
                        PriceAlert.monitoring_mode == "automatic",
                        PriceAlert.next_check_at.is_not(None),
                        PriceAlert.next_check_at <= now,
                    )
                    .order_by(PriceAlert.next_check_at)
                    .limit(100)
                    .with_for_update(skip_locked=True)
                )
            ).all()
        )
        for alert in alerts:
            alert.monitoring_status = "queued"
            alert.next_check_at = now + timedelta(minutes=15)
            queued_alerts.append(str(alert.id))
        deliveries = list(
            (
                await session.scalars(
                    select(AlertNotificationDelivery)
                    .where(
                        AlertNotificationDelivery.status.in_(("pending", "retry")),
                        AlertNotificationDelivery.next_attempt_at <= now,
                    )
                    .order_by(AlertNotificationDelivery.next_attempt_at)
                    .limit(100)
                    .with_for_update(skip_locked=True)
                )
            ).all()
        )
        for delivery in deliveries:
            delivery.next_attempt_at = now + timedelta(minutes=15)
            queued_deliveries.append(str(delivery.id))
        await session.commit()
    connection = Redis.from_url(settings.redis_url)
    queue = Queue("alerts", connection=connection)
    for alert_id in queued_alerts:
        queue.enqueue(
            "app.alerts.jobs.refresh_price_alert",
            alert_id,
            job_id=f"price-alert:{alert_id}:{int(now.timestamp())}",
            job_timeout=300,
        )
    for delivery_id in queued_deliveries:
        queue.enqueue(
            "app.alerts.jobs.deliver_line_notification",
            delivery_id,
            job_id=f"line-delivery:{delivery_id}:{int(now.timestamp())}",
            job_timeout=60,
        )
    connection.close()
    return {"alerts": len(queued_alerts), "deliveries": len(queued_deliveries)}


async def run() -> None:
    settings = get_settings()
    while True:
        await enqueue_due()
        await asyncio.sleep(settings.price_alert_scheduler_poll_seconds)


if __name__ == "__main__":
    asyncio.run(run())
