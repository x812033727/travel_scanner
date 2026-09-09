"""Prepare a source-credit-only edit; never replay research records over live hotels.

Pure helper for the reviewed operator workflow. It does not read/write a database or
approve a product. Callers must check the saved status/version and use normal admin review.
"""

from app.travel_services.schemas import ProductInput

IDENTITY_FACTS = (
    "google_place_id",
    "naver_map_url",
    "latitude",
    "longitude",
    "coordinate_source_url",
    "map_verified",
)


def prepare_credit_update(current: ProductInput, researched: ProductInput) -> ProductInput:
    if current.kind != "hotel" or researched.kind != "hotel":
        raise ValueError("Hotel identity required")
    if any(
        getattr(current, key) != getattr(researched, key)
        for key in ("source_key", "kind", "destination_id", "source_url")
    ):
        raise ValueError("Hotel identity changed; re-review required")
    if any(getattr(current.facts, key) != getattr(researched.facts, key) for key in IDENTITY_FACTS):
        raise ValueError("Location identity changed; re-review required")
    if not current.facts.map_verified:
        raise ValueError("Source credits do not approve an unreviewed map")
    if "hotel_links" in current.facts.model_fields_set:
        raise ValueError("Use saved facts, not projected legacy hotel_links")
    credits = researched.facts.source_credits
    if len(credits) != 1 or credits[0].url != current.facts.coordinate_source_url:
        raise ValueError("Exact coordinate-source attribution required")
    data = current.model_dump(mode="json")
    data["facts"].pop("hotel_links", None)
    existing = current.facts.source_credits
    matches = [c for c in existing if c.url == credits[0].url]
    if matches and (len(matches) != 1 or matches[0] != credits[0]):
        raise ValueError("Existing attribution differs; do not overwrite it")
    if not matches:
        data["facts"]["source_credits"].append(credits[0].model_dump(mode="json"))
    return ProductInput.model_validate(data)
