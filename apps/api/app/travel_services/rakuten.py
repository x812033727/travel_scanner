"""Rakuten's Japan and Global property IDs belong to different namespaces."""

import re
from typing import Literal
from urllib.parse import urlsplit

RAKUTEN_JAPAN_HOST = "travel.rakuten.co.jp"
RAKUTEN_GLOBAL_HOST = "travel.rakuten.com"
RakutenHotelIdentity = tuple[Literal["japan", "global"], str]


def rakuten_hotel_identity(value: str) -> RakutenHotelIdentity | None:
    """Identify observed property formats without converting IDs between markets.

    Japan accepts only the untracked primary property page. Its catalog also
    includes overseas hotels; the market does not determine the hotel's country.
    Global extraction is informational and does not narrow existing Global links.
    """
    from app.travel_services.schemas import safe_url

    parsed = urlsplit(safe_url(value))
    if parsed.hostname == RAKUTEN_JAPAN_HOST:
        match = re.fullmatch(r"/HOTEL/([1-9][0-9]*)/\1\.html", parsed.path)
        if match and not parsed.query:
            return "japan", match[1]
    elif parsed.hostname == RAKUTEN_GLOBAL_HOST:
        match = re.fullmatch(
            r"/[^/]+/[^/]+/hotel_info_item/(?:[^/]+/)+([1-9][0-9]*)/?", parsed.path
        )
        if match:
            return "global", match[1]
    return None
