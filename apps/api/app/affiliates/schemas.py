from typing import Literal

from pydantic import BaseModel

AffiliateModule = Literal["flight", "hotel", "activities", "transport", "connectivity"]
AffiliateChannel = Literal["travelpayouts", "klook_direct"]
# Where a member-initiated (tokened) clickout was rendered. Typing only: these paths never
# accept a placement from the request, so this is deliberately not the request-validated
# BookingPlacement vocabulary that the public destination-offer routes use. The click
# report's placement dimension is the union of both.
AffiliatePlacement = Literal["search", "trip", "stay"]


class AffiliatePartnerStatus(BaseModel):
    code: str
    display_name: str
    enabled: bool
    configured: bool
    available: bool
    modules: list[AffiliateModule]
    capabilities: list[str]
    # The modules a front-end button can actually render for today's settings, which is
    # narrower than `modules` (see partner_supports_module). Klook with only an AID is
    # `configured` for reviewed catalog offers yet supports none of the legacy modules.
    supported_modules: list[AffiliateModule] = []


class AffiliateOption(BaseModel):
    partner: str
    display_name: str
    module: AffiliateModule
    cta: str
    clickout_url: str


class AffiliateOptionsResponse(BaseModel):
    module: AffiliateModule
    disclosure: str
    options: list[AffiliateOption]


class DestinationAffiliateOption(BaseModel):
    id: str
    brand: str
    display_name: str
    destination_id: str
    module: AffiliateModule
    cta: str
    clickout_url: str


class DestinationAffiliateOptionsResponse(BaseModel):
    destination_id: str
    module: AffiliateModule
    disclosure: str
    options: list[DestinationAffiliateOption]
