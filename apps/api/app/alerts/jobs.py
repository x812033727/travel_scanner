from uuid import UUID


def refresh_price_alert(alert_id: UUID) -> dict[str, str]:
    """Mock job entrypoint; a scheduler can enqueue this later."""
    return {"alert_id": str(alert_id), "status": "mock-refreshed", "notification": "not-sent"}
