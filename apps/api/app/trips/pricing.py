"""Price snapshots on saved trips.

A provider offer expires within hours, but the trip built from it lives for weeks.
These helpers keep the part of a quote a traveller still needs after the offer is
gone (amount, currency, provider, when it was seen) apart from estimates, so the
trip page can say "已報價" and "估算" as two different numbers.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, cast

from app.models import TripPlan, TripPlanItem
from app.trips.schedule import FLIGHT_SYSTEM_ROLES, primary_lodging


def offer_price_snapshot(offer: dict[str, Any] | None) -> dict[str, Any] | None:
    """Reduce a normalized offer dump to the fields a trip keeps once the offer expires."""
    if not isinstance(offer, dict) or offer.get("total_price") is None:
        return None
    snapshot: dict[str, Any] = {
        "total_price": str(offer["total_price"]),
        "currency": str(offer.get("currency") or "TWD"),
        "provider": offer.get("provider"),
        "source_mode": offer.get("source_mode"),
        "retrieved_at": offer.get("retrieved_at"),
        "expires_at": offer.get("expires_at"),
    }
    if offer.get("nightly_price") is not None:
        snapshot["nightly_price"] = str(offer["nightly_price"])
    if offer.get("nights") is not None:
        snapshot["nights"] = int(offer["nights"])
    return snapshot


def lodging_from_offer(offer: dict[str, Any], *, selection_source: str) -> dict[str, Any] | None:
    """Build the `primary_lodging` record for a hotel offer dump, snapshot included.

    Same shape the stay-area picker writes, so every consumer (system hotel cards,
    reoptimisation, pricing) reads one structure regardless of where the hotel came from.
    """
    name = offer.get("hotel_name")
    if not isinstance(name, str) or not name.strip():
        return None
    offer_id = offer.get("id")
    return {
        "name": name,
        "location_name": offer.get("address") or name,
        "provider_place_id": None,
        "latitude": offer.get("latitude"),
        "longitude": offer.get("longitude"),
        "location_source": "provider",
        "offer_id": str(offer_id) if offer_id else None,
        "provider": offer.get("provider"),
        "hotel_id": offer.get("hotel_id"),
        "selection_source": selection_source,
        "selected_at": datetime.now(UTC).isoformat(),
        "price_snapshot": offer_price_snapshot(offer),
    }


def _amount(value: Any) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def trip_pricing(trip: TripPlan, rows: list[TripPlanItem]) -> dict[str, Any]:
    """Sum what was actually quoted for this trip, keeping estimates separate.

    Flight anchors carry the snapshot of the offer they were created from; the
    primary lodging carries its own. A round-trip offer appears on both flight
    anchors with the same `offer_id`, so it is counted once. Amounts in another
    currency than the trip's are listed but never silently converted.
    """
    currency = trip.currency or "TWD"
    entries: list[dict[str, Any]] = []
    for row in rows:
        if row.system_role not in FLIGHT_SYSTEM_ROLES:
            continue
        snapshot = row.data.get("price_snapshot")
        if not isinstance(snapshot, dict):
            continue
        entries.append(
            {
                "kind": "flight",
                "role": row.system_role,
                "item_id": str(row.id),
                "title": row.title,
                "offer_id": str(row.offer_id) if row.offer_id else None,
                **snapshot,
            }
        )
    lodging = primary_lodging(trip, rows)
    lodging_snapshot = lodging.get("price_snapshot") if lodging else None
    if lodging and isinstance(lodging_snapshot, dict):
        entries.append(
            {
                "kind": "hotel",
                "role": "primary_lodging",
                "item_id": None,
                "title": lodging.get("name"),
                "offer_id": lodging.get("offer_id"),
                **lodging_snapshot,
            }
        )
    quoted_total = Decimal(0)
    unsummed: list[str] = []
    seen_offers: set[str] = set()
    for entry in entries:
        offer_id = cast(str | None, entry.get("offer_id"))
        amount = _amount(entry.get("total_price"))
        counted = amount is not None and (offer_id is None or offer_id not in seen_offers)
        if offer_id is not None:
            seen_offers.add(offer_id)
        entry_currency = str(entry.get("currency") or currency)
        if counted and entry_currency != currency:
            counted = False
            if entry_currency not in unsummed:
                unsummed.append(entry_currency)
        entry["counted"] = counted
        if counted and amount is not None:
            quoted_total += amount
    total_cost = trip.data.get("total_cost")
    estimated = (
        _amount(total_cost.get("estimated_cost")) if isinstance(total_cost, dict) else None
    )
    return {
        "currency": currency,
        "quoted_total": str(quoted_total),
        "estimated_total": str(estimated) if estimated is not None else None,
        "items": entries,
        "unsummed_currencies": unsummed,
    }
