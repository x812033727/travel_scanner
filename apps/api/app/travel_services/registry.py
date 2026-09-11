from dataclasses import dataclass
from urllib.parse import urlsplit

from app.affiliates.schemas import AffiliateModule
from app.travel_services.rakuten import RAKUTEN_JAPAN_HOST, rakuten_hotel_identity
from app.travel_services.schemas import safe_url


@dataclass(frozen=True)
class Brand:
    name: str
    hosts: tuple[str, ...]
    kinds: tuple[str, ...]
    api_supported: bool = True
    modules: tuple[AffiliateModule, ...] = ()

    @property
    def supported_modules(self) -> tuple[AffiliateModule, ...]:
        if self.modules:
            return self.modules
        mapping: dict[str, AffiliateModule] = {
            "hotel": "hotel",
            "transfer": "transport",
            "tour": "activities",
            "esim": "connectivity",
        }
        return tuple(dict.fromkeys(mapping[kind] for kind in self.kinds))


BRANDS = {
    "klook": Brand("Klook", ("klook.com",), ("hotel", "transfer", "tour", "esim")),
    "kkday": Brand("KKday", ("kkday.com",), ("hotel", "transfer", "tour")),
    "airalo": Brand("Airalo", ("airalo.com",), ("esim",)),
    "saily": Brand("Saily", ("saily.com",), ("esim",)),
    "yesim": Brand("Yesim", ("yesim.app",), ("esim",)),
    "gigsky": Brand("GigSky", ("gigsky.com",), ("esim",)),
    "kiwitaxi": Brand("Kiwitaxi", ("kiwitaxi.com",), ("transfer",)),
    "welcome_pickups": Brand("Welcome Pickups", ("welcomepickups.com",), ("transfer",)),
    "gettransfer": Brand("GetTransfer.com", ("gettransfer.com",), ("transfer",)),
    "intui": Brand("intui.travel", ("intui.travel",), ("transfer",)),
    "tiqets": Brand("Tiqets", ("tiqets.com",), ("tour",)),
    "wegotrip": Brand("WeGoTrip", ("wegotrip.com",), ("tour",)),
    "booking": Brand("Booking.com", ("booking.com",), ("hotel",)),
    "trip_com": Brand("Trip.com", ("trip.com",), ("hotel", "tour", "transfer")),
    "agoda": Brand("Agoda", ("agoda.com",), ("hotel",)),
    "expedia": Brand("Expedia", ("expedia.com", "expedia.co.uk"), ("hotel",), False),
    "viator": Brand("Viator", ("viator.com",), ("tour", "transfer")),
    "getyourguide": Brand("GetYourGuide", ("getyourguide.com",), ("tour", "transfer")),
    "rakuten": Brand("Rakuten Travel", ("travel.rakuten.com",), ("hotel",)),
    # Travelpayouts excludes Kiwi.com from Partner Links API conversion. A reviewed
    # static link remains supported; API eligibility is separate from enrollment.
    "kiwi": Brand("Kiwi.com", ("kiwi.com",), (), False, modules=("flight",)),
}


def brand_target(code: str, value: str) -> str:
    value = safe_url(value)
    host = urlsplit(value).hostname or ""
    if code not in BRANDS or not any(
        host == h or host.endswith("." + h) for h in BRANDS[code].hosts
    ):
        raise ValueError("Target does not belong to the selected brand")
    return value


def direct_hotel_target(code: str, value: str) -> str:
    """Permit Japan's exact Rakuten hotel pages only for ordinary direct links.

    BRANDS and brand_target remain the affiliate channel's allowlist: a verified
    Japan property does not establish Travelpayouts/API support for that market.
    """
    value = safe_url(value)
    if code == "rakuten" and urlsplit(value).hostname == RAKUTEN_JAPAN_HOST:
        identity = rakuten_hotel_identity(value)
        if identity is None or identity[0] != "japan":
            raise ValueError("An exact untracked Rakuten Japan hotel page is required")
        return value
    return brand_target(code, value)


def affiliate_target(value: str) -> str:
    value = safe_url(value)
    host = urlsplit(value).hostname or ""
    if not any(
        host == h or host.endswith("." + h) for h in ("tp.st", "tp.media", "travelpayouts.com")
    ):
        raise ValueError("Verified Travelpayouts redirect required")
    return value


def affiliate_click_target(code: str, value: str) -> str:
    """Accept a Travelpayouts redirect or its final allowlisted brand URL."""
    try:
        return affiliate_target(value)
    except ValueError:
        return brand_target(code, value)
