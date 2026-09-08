from typing import Literal

from pydantic import BaseModel

AffiliateModule = Literal["flight", "hotel", "activities", "transport", "connectivity"]


class AffiliatePartnerStatus(BaseModel):
    code: str
    display_name: str
    enabled: bool
    configured: bool
    available: bool
    modules: list[AffiliateModule]
    capabilities: list[str]


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
