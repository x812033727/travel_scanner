"""Flight anchors filled from a provider offer.

The hand-typed path (`apply_flight_anchor_details` in the trips router)
deliberately drops the offer id and the price snapshot: a typed flight is not
the flight that was quoted. This is the other branch. Here the anchor *is* the
offer, so it keeps the id that alerts and pricing look up, the quote it was
created from, and the airport-local times the provider reported.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from app.models import TripPlanItem
from app.providers.schemas import FlightOffer
from app.trips.itinerary import offer_flight_info
from app.trips.pricing import offer_price_snapshot

FlightRole = Literal["outbound_flight", "return_flight"]

# A flight the member chose is theirs, however they chose it: typed by hand, or picked
# out of a search and brought back with `from-offer`. Re-pricing rebuilds the plan
# around these; it never replaces one.
MEMBER_CHOSEN_SOURCES = frozenset({"manual", "offer"})


def member_chose_flight(item: TripPlanItem) -> bool:
    """Whether this anchor holds a flight the member picked, not one the plan produced."""
    return str(item.data.get("flight_selection_source") or "") in MEMBER_CHOSEN_SOURCES


def offer_has_leg(offer: FlightOffer, role: FlightRole) -> bool:
    """Whether the offer covers this anchor: a one-way offer has no return leg.

    The test is `return_departure_time`, not the presence of a leg-1 segment,
    because that is the field the anchor is built from. A multi-city offer has
    leg-1 segments and no return time (`amadeus.py` fills it for round trips
    only), and accepting one writes an anchor with no times at all.
    """
    if role == "outbound_flight":
        return True
    return offer.return_departure_time is not None


def offer_leg_date(offer: FlightOffer, role: FlightRole) -> date | None:
    """The airport-local departure day of the leg this anchor would hold."""
    info = offer_flight_info(offer, returning=role == "return_flight")
    local = info.get("departure_local")
    return date.fromisoformat(str(local)[:10]) if local else None


def apply_flight_offer(item: TripPlanItem, role: FlightRole, offer: FlightOffer) -> None:
    returning = role == "return_flight"
    info = offer_flight_info(offer, returning=returning)
    item.item_type = "flight"
    item.locked = True
    item.fixed_time = True
    item.is_skipped = False
    item.offer_id = offer.id
    item.start_time = offer.return_departure_time if returning else offer.departure_time
    item.end_time = offer.return_arrival_time if returning else offer.arrival_time
    item.duration_minutes = None
    item.latitude = None
    item.longitude = None
    item.provider_place_id = None
    item.location_source = None
    item.is_estimated = False
    item.title = f"{info['airline']} {info['flight_number']}"
    item.location_name = f"{info['origin']} → {info['destination']}"
    item.data = {
        **{key: value for key, value in item.data.items() if key != "price_snapshot"},
        "source_mode": offer.source_mode,
        "is_bookable": offer.is_bookable,
        "timeline_section": "flight_anchor",
        "flight_leg": "return" if returning else "outbound",
        "flight_selection_source": "offer",
        "flight_info": info,
        "price_snapshot": offer_price_snapshot(offer.model_dump(mode="json")),
    }
