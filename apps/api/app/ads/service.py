"""Whether an article page may carry a Google AdSense unit, and with which identifiers."""

from __future__ import annotations

import re
from typing import Any

from app.config import Settings

# Both shapes are Google's: a publisher id is `ca-pub-` plus 16 digits, an ad unit slot
# is 10 digits. Validating here means the page never renders an `<ins>` that can only
# fail, and a typo in the back office shows up as "off" rather than as a blank box.
PUBLISHER_ID_PATTERN = re.compile(r"ca-pub-\d{16}")
SLOT_ID_PATTERN = re.compile(r"\d{10}")

DISABLED: dict[str, Any] = {
    "enabled": False, "publisher_id": None, "slot_id": None, "cmp_enabled": False,
}


def adsense_config(settings: Settings, *, tracking_allowed: bool) -> dict[str, Any]:
    """The public configuration for one request.

    `tracking_allowed` is false when the browser sent DNT or GPC. The site's standing
    rule is that such a browser loads no third-party script at all, so the answer is the
    same as if advertising were switched off entirely: no identifiers leave the server.
    """
    publisher_id = (settings.adsense_publisher_id or "").strip()
    slot_id = (settings.adsense_slot_id or "").strip()
    enabled = bool(
        tracking_allowed
        and settings.adsense_enabled
        and PUBLISHER_ID_PATTERN.fullmatch(publisher_id)
        and SLOT_ID_PATTERN.fullmatch(slot_id)
    )
    if not enabled:
        return dict(DISABLED)
    # Only meaningful alongside an enabled configuration: it tells the page whether a
    # certified consent message decides personalisation, or whether the loader must force
    # non-personalised ads because there is nothing there to ask the reader.
    return {
        "enabled": True,
        "publisher_id": publisher_id,
        "slot_id": slot_id,
        "cmp_enabled": bool(settings.adsense_cmp_enabled),
    }
