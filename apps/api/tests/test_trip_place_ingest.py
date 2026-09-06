"""Reading a paste into the waiting list, without deciding anything about it."""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

import httpx
import pytest

from app.models import TravelHotspot
from app.trips.ingest import candidate_from, parse_line, serialize_candidate, split_lines


def hotspot() -> TravelHotspot:
    return TravelHotspot(
        id=uuid4(),
        slug="sensoji",
        name="淺草寺",
        city_code="NRT",
        destination_id="tokyo",
        city_name="東京",
        country_code="JP",
        country_name="日本",
        category="culture",
        search_text="淺草寺",
        latitude=Decimal("35.714800"),
        longitude=Decimal("139.796700"),
        google_place_id="ChIJ8T1GpMGOGGARDYGSgpooDWw",
        metadata_json={"local_name": "浅草寺"},
        depth_score=Decimal("7.50"),
        source_urls=[],
    )


def test_a_paste_is_one_place_per_line_without_repeats() -> None:
    assert split_lines(" 淺草寺 \n\nhttps://maps.app.goo.gl/abc\n淺草寺 \n") == [
        "淺草寺",
        "https://maps.app.goo.gl/abc",
    ]


@pytest.mark.asyncio
async def test_a_short_link_is_expanded_and_its_place_id_kept() -> None:
    seen: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        if "maps.app.goo.gl" in str(request.url):
            return httpx.Response(
                302,
                headers={
                    "location": (
                        "https://www.google.com/maps/place/"
                        "?q=place_id:ChIJ8T1GpMGOGGARDYGSgpooDWw"
                    ),
                },
            )
        return httpx.Response(200)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=False)
    parsed = await parse_line("https://maps.app.goo.gl/abc", client=client)
    await client.aclose()

    assert parsed.place_id == "ChIJ8T1GpMGOGGARDYGSgpooDWw"
    assert parsed.source == "maps_url"
    assert seen[0] == "https://maps.app.goo.gl/abc"


@pytest.mark.asyncio
async def test_a_typed_name_stays_a_name_rather_than_failing() -> None:
    parsed = await parse_line("金峰魯肉飯")
    assert parsed.place_id is None
    assert parsed.query == "金峰魯肉飯"
    assert parsed.source == "text"


@pytest.mark.asyncio
async def test_a_link_to_somewhere_that_is_not_google_is_refused() -> None:
    from app.problems import AppError

    with pytest.raises(AppError):
        await parse_line("https://example.com/maps/place/somewhere")


@pytest.mark.asyncio
async def test_a_match_in_the_catalogue_brings_its_record_with_it() -> None:
    trip_id = uuid4()
    parsed = await parse_line("ChIJ8T1GpMGOGGARDYGSgpooDWw")
    place = hotspot()

    candidate = candidate_from(
        trip_id,
        parsed,
        place,
        {"zh-TW": "淺草寺", "en": "Sensoji", "ja": "浅草寺", "ko": "센소지", "zh-CN": "浅草寺"},
    )

    assert candidate.trip_plan_id == trip_id
    assert candidate.hotspot_id == place.id
    assert candidate.title == "淺草寺"
    assert candidate.location_name == "東京"
    assert candidate.latitude == Decimal("35.714800")
    assert candidate.names_json["title"]["en"] == "Sensoji"
    assert candidate.data["matched"] == "hotspot"
    assert candidate.data["depth_score"] == 7.5


@pytest.mark.asyncio
async def test_a_place_we_do_not_have_is_still_kept_as_what_the_traveller_typed() -> None:
    parsed = await parse_line("金峰魯肉飯")
    candidate = candidate_from(uuid4(), parsed, None)

    assert candidate.hotspot_id is None
    assert candidate.title == "金峰魯肉飯"
    assert candidate.names_json == {}
    assert candidate.data["matched"] == "none"
    assert serialize_candidate(candidate)["title"] == "金峰魯肉飯"
