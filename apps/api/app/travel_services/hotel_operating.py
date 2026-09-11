"""Authoritative accommodation-night restrictions for the reviewed hotel catalogue.

The intervals describe nights, not exact check-in hours. Partial/daytime closures
must be reviewed as conservative unavailable-night ranges with explanatory reasons.
"""

from datetime import UTC, date, datetime
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from app.models import TravelServiceProduct
from app.problems import AppError
from app.travel_services.schemas import CITIES, HotelOperatingRules


def hotel_today(product: TravelServiceProduct, now: datetime | None = None) -> date:
    country = CITIES.get(product.destination_id, (None,))[0]
    zone = {"JP": "Asia/Tokyo", "KR": "Asia/Seoul", "TW": "Asia/Taipei"}.get(country or "")
    if zone is None:
        raise AppError(409, "hotel_operating_rules_invalid", "飯店營運日期無法確認")
    return (now or datetime.now(UTC)).astimezone(ZoneInfo(zone)).date()


def operating_rules(product: TravelServiceProduct) -> HotelOperatingRules | None:
    if product.kind != "hotel":
        return None
    facts = product.facts
    # SQLAlchemy's default has not run on a newly constructed test/import instance.
    if facts is None:
        return None
    try:
        if not isinstance(facts, dict):
            raise ValueError("Invalid stored facts")
        raw = facts.get("hotel_operating_rules")
        return HotelOperatingRules.model_validate(raw) if raw is not None else None
    except (ValidationError, ValueError, TypeError) as exc:
        raise AppError(
            409, "hotel_operating_rules_invalid", "飯店營運日期資料待確認，暫時無法預訂"
        ) from exc


def hotel_publicly_available(
    product: TravelServiceProduct, now: datetime | None = None
) -> bool:
    """Hide malformed policies and hotels for which no future stay can finish."""
    try:
        rules = operating_rules(product)
        return rules is None or rules.last_checkout_date is None or (
            hotel_today(product, now) < rules.last_checkout_date
        )
    except AppError:
        return False


def require_hotel_stay(
    product: TravelServiceProduct,
    check_in: date | None = None,
    check_out: date | None = None,
    *,
    now: datetime | None = None,
) -> None:
    """Validate before exposing/resolving any booking target or changing a trip."""
    rules = operating_rules(product)
    if rules is None:
        return
    if rules.last_checkout_date and hotel_today(product, now) >= rules.last_checkout_date:
        raise AppError(409, "hotel_operating_unavailable", "這間飯店已超過最後可退房日期")
    if check_in is None or check_out is None:
        raise AppError(
            422, "hotel_operating_dates_required", "這間飯店有營運限制，請先選擇入住與退房日期"
        )
    if check_out <= check_in:
        raise AppError(422, "hotel_booking_context_invalid", "退房日期必須晚於入住日期")
    if rules.last_checkout_date and check_out > rules.last_checkout_date:
        raise AppError(409, "hotel_operating_unavailable", "住宿日期超過飯店最後可退房日期")
    if any(
        check_in < unavailable.end_date and unavailable.start_date < check_out
        for unavailable in rules.unavailable_stays
    ):
        raise AppError(409, "hotel_operating_unavailable", "住宿日期與飯店暫停住宿期間重疊")


def hotel_stay_available(
    product: TravelServiceProduct,
    check_in: date | None,
    check_out: date | None,
    *,
    now: datetime | None = None,
) -> bool:
    try:
        require_hotel_stay(product, check_in, check_out, now=now)
        return True
    except AppError:
        return False


def require_hotel_booking_target(product: TravelServiceProduct, target: str | None) -> None:
    """Saved URL parameters cannot override a restricted hotel's validated stay.

    The query may identify a room, property or stay, so stripping parameters is
    unsafe. Require a separately reviewed query-free target instead. Typed Stay22
    parameters are built later from the already validated request, not saved URLs.
    """
    if operating_rules(product) is None:
        return
    try:
        if target and not urlsplit(target).query:
            return
    except ValueError:
        pass
    raise AppError(
        409, "hotel_operating_rules_invalid", "受限飯店的訂房網址含未核對條件，請重新確認連結"
    )
