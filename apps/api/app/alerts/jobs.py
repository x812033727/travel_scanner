import asyncio
from uuid import UUID

from app.alerts.monitor import deliver_notification, refresh_alert


def refresh_price_alert(alert_id: UUID) -> dict[str, str]:
    delivery_id = asyncio.run(refresh_alert(UUID(str(alert_id))))
    return {
        "alert_id": str(alert_id),
        "status": "refreshed",
        "notification": "pending" if delivery_id else "not-triggered",
    }


def deliver_line_notification(delivery_id: UUID) -> dict[str, str]:
    sent = asyncio.run(deliver_notification(UUID(str(delivery_id))))
    return {"delivery_id": str(delivery_id), "status": "sent" if sent else "pending"}
