import hashlib

from app.providers.schemas import FlightOffer, FlightSegment


def itinerary_key_from_segments(segments: list[FlightSegment], cabin_class: str) -> str:
    """Group the same flown itinerary without collapsing cabin/fare families."""
    parts = [cabin_class.lower()]
    for segment in segments:
        parts.append(
            "|".join(
                (
                    segment.flight_number.replace(" ", "").upper(),
                    segment.origin.upper(),
                    segment.destination.upper(),
                    segment.departure_time.isoformat(timespec="minutes"),
                    segment.arrival_time.isoformat(timespec="minutes"),
                    str(segment.leg_index),
                )
            )
        )
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:32]


def ensure_itinerary_key(offer: FlightOffer) -> FlightOffer:
    if offer.itinerary_key:
        return offer
    return offer.model_copy(
        update={"itinerary_key": itinerary_key_from_segments(offer.segments, offer.cabin_class)}
    )
