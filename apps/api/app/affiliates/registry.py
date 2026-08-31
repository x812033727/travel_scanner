from dataclasses import dataclass

from app.affiliates.schemas import AffiliateModule
from app.config import Settings


@dataclass(frozen=True)
class AffiliatePartner:
    code: str
    display_name: str
    modules: tuple[AffiliateModule, ...]
    enabled_field: str
    template_field: str
    allowed_hosts_field: str
    priority: int
    capabilities: tuple[str, ...] = ("link",)


AFFILIATE_PARTNERS: tuple[AffiliatePartner, ...] = (
    AffiliatePartner(
        "skyscanner",
        "Skyscanner",
        ("flight",),
        "skyscanner_affiliate_enabled",
        "skyscanner_affiliate_url_template",
        "skyscanner_affiliate_allowed_hosts",
        10,
    ),
    AffiliatePartner(
        "trip_com",
        "Trip.com",
        ("flight", "hotel", "activities", "transport"),
        "trip_com_enabled",
        "trip_com_affiliate_url_template",
        "trip_com_allowed_hosts",
        30,
    ),
    AffiliatePartner(
        "booking",
        "Booking.com",
        ("hotel",),
        "booking_enabled",
        "booking_affiliate_url_template",
        "booking_allowed_hosts",
        10,
    ),
    AffiliatePartner(
        "agoda",
        "Agoda",
        ("hotel",),
        "agoda_enabled",
        "agoda_affiliate_url_template",
        "agoda_allowed_hosts",
        20,
    ),
    AffiliatePartner(
        "kkday",
        "KKday",
        ("activities", "transport"),
        "kkday_enabled",
        "kkday_affiliate_url_template",
        "kkday_allowed_hosts",
        10,
    ),
    AffiliatePartner(
        "klook",
        "Klook",
        ("activities", "transport"),
        "klook_enabled",
        "klook_affiliate_url_template",
        "klook_allowed_hosts",
        20,
    ),
    AffiliatePartner(
        "airalo",
        "Airalo",
        ("connectivity",),
        "airalo_enabled",
        "airalo_affiliate_url_template",
        "airalo_allowed_hosts",
        10,
    ),
    AffiliatePartner(
        "travelpayouts",
        "Travelpayouts",
        ("flight", "hotel", "activities", "transport"),
        "travelpayouts_enabled",
        "travelpayouts_static_url_template",
        "travelpayouts_allowed_hosts",
        90,
        ("link", "link_api"),
    ),
)

PARTNERS_BY_CODE = {partner.code: partner for partner in AFFILIATE_PARTNERS}


def partner_enabled(partner: AffiliatePartner, settings: Settings) -> bool:
    return bool(getattr(settings, partner.enabled_field))


def partner_configured(partner: AffiliatePartner, settings: Settings) -> bool:
    if not str(getattr(settings, partner.allowed_hosts_field) or "").strip():
        return False
    template = getattr(settings, partner.template_field)
    if template:
        if partner.code == "booking":
            return bool(settings.booking_affiliate_id)
        if partner.code == "agoda":
            return bool(settings.agoda_cid)
        if partner.code == "kkday":
            return bool(settings.kkday_cid)
        return True
    if partner.code == "travelpayouts":
        return bool(
            settings.travelpayouts_api_token
            and settings.travelpayouts_marker
            and settings.travelpayouts_project_id
            and any(
                (
                    settings.travelpayouts_flight_target_url,
                    settings.travelpayouts_hotel_target_url,
                    settings.travelpayouts_activities_target_url,
                    settings.travelpayouts_transport_target_url,
                )
            )
        )
    return False


def partners_for_module(module: AffiliateModule) -> list[AffiliatePartner]:
    return sorted(
        (partner for partner in AFFILIATE_PARTNERS if module in partner.modules),
        key=lambda partner: partner.priority,
    )
