from typing import Any
from uuid import UUID, uuid4

import httpx
import pytest

from app.foods.coordinate_fill import (
    CoordinateFillReport,
    GeoCandidate,
    MerchantPage,
    fill_merchant_coordinates,
    in_country,
    page_candidates,
    select_candidate,
    summarize,
)
from app.foods.coordinate_fill_cli import MAX_BYTES, build_fetcher, is_public_https_url
from app.models import FoodMerchant

JSON_LD_PAGE = """
<html><head>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Restaurant","name":"Jumbo Seafood Riverside Point",
 "address":{"@type":"PostalAddress","addressLocality":"Singapore"},
 "geo":{"@type":"GeoCoordinates","latitude":1.2884,"longitude":103.8461}}
</script>
</head><body>店家介紹</body></html>
"""

GRAPH_PAGE = """
<script type="application/ld+json">
{"@graph":[{"@type":"WebPage"},
 {"@type":"LocalBusiness","name":"Jumbo Seafood Riverside Point",
  "geo":{"latitude":"1.2884","longitude":"103.8461"}}]}
</script>
"""

# What a tourism board's "ten places to eat" page actually looks like.
MULTI_VENUE_PAGE = """
<script type="application/ld+json">
{"@type":"ItemList","itemListElement":[
 {"@type":"Restaurant","name":"Some Other Place","geo":{"latitude":1.3000,"longitude":103.8000}},
 {"@type":"Restaurant","name":"Jumbo Seafood Riverside Point",
  "geo":{"latitude":1.2884,"longitude":103.8461}},
 {"@type":"Restaurant","name":"A Third Restaurant","geo":{"latitude":1.3100,"longitude":103.9000}}]}
</script>
"""

MULTI_VENUE_NO_NAMES = """
<script type="application/ld+json">
{"@type":"ItemList","itemListElement":[
 {"@type":"Restaurant","geo":{"latitude":1.3000,"longitude":103.8000}},
 {"@type":"Restaurant","geo":{"latitude":1.3100,"longitude":103.9000}}]}
</script>
"""

META_PAGE = """
<meta itemprop="latitude" content="35.6595">
<meta itemprop="longitude" content="139.7005">
"""

POSITION_PAGE = '<meta name="geo.position" content="1.2884;103.8461">'

TWO_LATITUDES_PAGE = """
<meta itemprop="latitude" content="1.2884"><meta itemprop="longitude" content="103.8461">
<meta itemprop="latitude" content="1.3100"><meta itemprop="longitude" content="103.9000">
"""

GOOGLE_EMBED_PAGE = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!3d1.2884!4d103.8461!5e0"></iframe>
<a href="https://maps.google.com/maps?q=1.2884,103.8461">地圖</a>
"""

COMMENTED_PAGE = """
<!-- <script type="application/ld+json">
{"@type":"Restaurant","name":"Staging Copy","geo":{"latitude":9.9,"longitude":9.9}}
</script> -->
<script type="application/ld+json">
{"@type":"Restaurant","name":"Jumbo Seafood Riverside Point",
 "geo":{"latitude":1.2884,"longitude":103.8461}}
</script>
"""


def merchant(**overrides: Any) -> FoodMerchant:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "singapore-jumbo-riverside",
        "destination_id": "singapore",
        "country_code": "SG",
        "name": "Jumbo Seafood Riverside Point",
        "local_name": "珍寶海鮮",
        "review_status": "pending",
        "map_match_status": "unverified",
        "is_active": False,
        "display_order": 1,
    }
    values.update(overrides)
    return FoodMerchant(**values)


class FillSession:
    """Just enough session for the fill loop: a duplicate lookup and commit counting."""

    def __init__(self, owner: str | None = None) -> None:
        self.owner = owner
        self.commits = 0
        self.added: list[Any] = []

    async def scalar(self, _statement: object) -> str | None:
        return self.owner

    def add(self, value: Any) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.commits += 1


def pages(*bodies: str | None) -> Any:
    queue = list(bodies)
    seen: list[str] = []

    async def fetch(url: str) -> str | None:
        seen.append(url)
        if not queue:
            raise AssertionError(f"unexpected extra fetch of {url}")
        body = queue.pop(0)
        if body == "boom":
            raise TimeoutError("slow")
        return body

    fetch.seen = seen  # type: ignore[attr-defined]
    return fetch


def sources(row: FoodMerchant, *specs: tuple[str, str, str]) -> dict[UUID, list[MerchantPage]]:
    return {row.id: [MerchantPage(*spec) for spec in specs]}


def website(url: str) -> tuple[str, str, str]:
    return ("merchant_website", "merchant_official", url)


def listing(url: str) -> tuple[str, str, str]:
    return ("merchant_listing", "official_tourism", url)


NAMES = ("Jumbo Seafood Riverside Point", "珍寶海鮮")


def test_json_ld_geo_is_read_with_the_name_of_the_entity_that_owns_it() -> None:
    found = page_candidates(JSON_LD_PAGE)

    assert [(c.latitude, c.longitude, c.owner, c.method) for c in found] == [
        (1.2884, 103.8461, "Jumbo Seafood Riverside Point", "json_ld")
    ]


def test_a_graph_document_and_string_numbers_still_parse() -> None:
    candidate, reason = select_candidate(page_candidates(GRAPH_PAGE), NAMES)

    assert reason == "named"
    assert candidate is not None and candidate.key == (1.2884, 103.8461)


def test_a_multi_venue_listing_picks_the_venue_that_carries_the_merchants_name() -> None:
    candidate, reason = select_candidate(page_candidates(MULTI_VENUE_PAGE), NAMES)

    assert reason == "named"
    assert candidate is not None and candidate.key == (1.2884, 103.8461)


def test_a_multi_venue_listing_that_names_nobody_is_ambiguous_not_a_guess() -> None:
    candidate, reason = select_candidate(page_candidates(MULTI_VENUE_NO_NAMES), NAMES)

    assert candidate is None
    assert reason == "ambiguous"


def test_a_single_coordinate_is_accepted_even_when_the_name_does_not_match() -> None:
    candidate, reason = select_candidate(page_candidates(POSITION_PAGE), NAMES)

    assert reason == "only"
    assert candidate is not None and candidate.key == (1.2884, 103.8461)


def test_meta_tags_are_read_only_when_the_page_carries_exactly_one_pair() -> None:
    assert [c.key for c in page_candidates(META_PAGE)] == [(35.6595, 139.7005)]
    # Two of each could pair a latitude from one venue with a longitude from another.
    assert page_candidates(TWO_LATITUDES_PAGE) == []


def test_coordinates_inside_a_google_map_embed_are_never_read() -> None:
    # They are Google's coordinates whatever page they sit in, so storing them under
    # merchant_official provenance would launder the licensing rule.
    assert page_candidates(GOOGLE_EMBED_PAGE) == []


def test_json_ld_inside_an_html_comment_is_ignored() -> None:
    candidate, _ = select_candidate(page_candidates(COMMENTED_PAGE), NAMES)

    assert candidate is not None and candidate.key == (1.2884, 103.8461)


def test_a_page_without_structured_coordinates_yields_nothing() -> None:
    prose = "<html><body>營業時間 11:00-21:00 電話 02-2345-6789</body></html>"
    assert page_candidates(prose) == []
    assert page_candidates('<script type="application/ld+json">{ not json </script>') == []
    # Null Island is a placeholder, never a restaurant.
    assert page_candidates('<meta name="geo.position" content="0.0;0.0">') == []


def test_bare_integers_and_grouped_numbers_are_not_coordinates() -> None:
    # A CMS placeholder of content="0" must not parse, and "13,7563" is unresolvably
    # ambiguous between a decimal comma and a group separator.
    placeholder = '<meta itemprop="latitude" content="0"><meta itemprop="longitude" content="0">'
    grouped = (
        '<script type="application/ld+json">'
        '{"geo":{"latitude":"13,7563","longitude":"100,5018"}}</script>'
    )
    assert page_candidates(placeholder) == []
    assert page_candidates(grouped) == []


def test_the_country_box_rejects_a_coordinate_from_the_wrong_country() -> None:
    assert in_country("SG", 1.2884, 103.8461) is True
    assert in_country("SG", 35.6595, 139.7005) is False
    # An unlisted country cannot be checked, so it must not drop every row there.
    assert in_country("FR", 48.85, 2.35) is True


@pytest.mark.asyncio
async def test_a_dry_run_reports_without_writing() -> None:
    session = FillSession()
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, website("https://www.jumboseafood.com.sg/en/riverside-point")),
        pages(JSON_LD_PAGE),
        apply=False,
    )

    assert [r.outcome for r in reports] == ["would_fill"]
    assert reports[0].source_type == "merchant_official"
    assert row.latitude is None
    assert session.commits == 0


@pytest.mark.asyncio
async def test_applying_writes_the_coordinate_and_its_provenance_only() -> None:
    session = FillSession()
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, listing("https://www.visitsingapore.com/jumbo")),
        pages(JSON_LD_PAGE),
        apply=True,
    )

    assert [r.outcome for r in reports] == ["filled"]
    assert float(row.latitude) == pytest.approx(1.2884)  # type: ignore[arg-type]
    assert float(row.longitude) == pytest.approx(103.8461)  # type: ignore[arg-type]
    assert row.coordinate_source_type == "official_tourism"
    assert row.coordinate_source_url == "https://www.visitsingapore.com/jumbo"
    # Stamped like every other coordinate writer: it records when the coordinate was last
    # confirmed against its source, not that a human approved the merchant.
    assert row.coordinate_verified_at is not None
    # Publication still needs a human, so no review state may move here.
    assert row.map_match_status == "unverified"
    assert row.review_status == "pending"
    assert row.is_active is False
    assert session.commits == 1
    entry = session.added[0]
    assert entry.action == "food_merchant.cli_coordinates_filled"
    assert entry.target == f"food_merchant:{row.id}"
    assert entry.actor_user_id is None
    assert entry.metadata_json["coordinate_source_type"] == "official_tourism"
    assert entry.metadata_json["latitude"] == pytest.approx(1.2884)
    assert entry.metadata_json["method"] == "json_ld"


@pytest.mark.asyncio
async def test_a_coordinate_another_merchant_already_stands_on_is_reported_not_written() -> None:
    # Two merchants citing one multi-venue article is how this happens, and it means at least
    # one of the two coordinates is wrong.
    session = FillSession(owner="singapore-other-restaurant")
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, listing("https://www.visitsingapore.com/shared-article")),
        pages(JSON_LD_PAGE),
        apply=True,
    )

    assert [r.outcome for r in reports] == ["duplicate"]
    assert reports[0].owner == "singapore-other-restaurant"
    assert row.latitude is None
    assert session.commits == 0


@pytest.mark.asyncio
async def test_the_merchants_own_site_is_read_before_a_tourism_listing() -> None:
    session = FillSession()
    row = merchant()
    fetch = pages(JSON_LD_PAGE)

    await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(
            row,
            listing("https://tourism.example/listing"),
            website("https://own.example/branch"),
        ),
        fetch,
        apply=True,
    )

    assert fetch.seen == ["https://own.example/branch"]
    assert row.coordinate_source_type == "merchant_official"


@pytest.mark.asyncio
async def test_a_scope_with_no_provenance_rule_is_dropped_rather_than_crashing() -> None:
    session = FillSession()
    row = merchant()
    fetch = pages()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, ("destination_context", "official_tourism", "https://city.example/food")),
        fetch,
        apply=True,
    )

    assert [r.outcome for r in reports] == ["no_source"]
    assert fetch.seen == []


@pytest.mark.asyncio
async def test_a_coordinate_outside_the_country_is_reported_not_written() -> None:
    session = FillSession()
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, website("https://own.example/hq")),
        pages(META_PAGE),  # Tokyo coordinates on a Singapore merchant
        apply=True,
    )

    assert [r.outcome for r in reports] == ["implausible"]
    assert row.latitude is None
    assert session.commits == 0


@pytest.mark.asyncio
async def test_the_first_specific_failure_survives_a_later_empty_page() -> None:
    session = FillSession()
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, website("https://own.example/hq"), listing("https://tourism.example/x")),
        pages(META_PAGE, "<html>nothing here</html>"),
        apply=True,
    )

    assert [r.outcome for r in reports] == ["implausible"]


@pytest.mark.asyncio
async def test_a_dead_page_falls_through_to_the_next_one() -> None:
    session = FillSession()
    row = merchant()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, website("https://own.example/gone"), listing("https://tourism.example/x")),
        pages("boom", JSON_LD_PAGE),
        apply=True,
    )

    assert [r.outcome for r in reports] == ["filled"]
    assert row.coordinate_source_type == "official_tourism"


@pytest.mark.asyncio
async def test_rows_without_a_usable_page_and_with_coordinates_are_skipped() -> None:
    session = FillSession()
    without = merchant(slug="a")
    already = merchant(slug="b", latitude=1.1, longitude=103.1)
    fetch = pages()

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [without, already],
        {},
        fetch,
        apply=True,
    )

    assert [r.outcome for r in reports] == ["no_source", "already_filled"]
    assert fetch.seen == []


@pytest.mark.asyncio
async def test_one_failure_does_not_stop_the_batch_and_progress_is_reported() -> None:
    session = FillSession()
    first = merchant(slug="a")
    second = merchant(slug="b")
    lines: list[str] = []

    reports = await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [first, second],
        {
            first.id: [MerchantPage(*website("https://own.example/a"))],
            second.id: [MerchantPage(*website("https://own.example/b"))],
        },
        pages("boom", JSON_LD_PAGE),
        apply=True,
        progress=lines.append,
    )

    assert [r.outcome for r in reports] == ["fetch_failed", "filled"]
    assert second.coordinate_source_url == "https://own.example/b"
    assert any("a: fetch_failed" in line for line in lines)


@pytest.mark.asyncio
async def test_consecutive_requests_to_one_host_are_spaced_out() -> None:
    session = FillSession()
    row = merchant()
    waits: list[float] = []

    async def pause(seconds: float) -> None:
        waits.append(seconds)

    await fill_merchant_coordinates(
        session,  # type: ignore[arg-type]
        [row],
        sources(row, website("https://one.example/a"), listing("https://one.example/b")),
        pages("<html>nothing</html>", JSON_LD_PAGE),
        apply=True,
        pause=pause,
        host_delay_seconds=1.5,
    )

    assert waits == [1.5]


def test_the_summary_counts_outcomes() -> None:
    summary = summarize(
        [
            CoordinateFillReport(
                "a", "A", "filled", 1.0, 103.0, "merchant_official", "u", "json_ld", "A"
            ),
            CoordinateFillReport("b", "B", "ambiguous"),
        ]
    )

    assert summary["processed"] == 2
    assert summary["outcomes"] == {"filled": 1, "ambiguous": 1}
    assert summary["rows"][0]["coordinate_source_type"] == "merchant_official"
    assert summary["rows"][0]["matched_entity"] == "A"


def test_geo_candidate_keys_round_to_five_places() -> None:
    assert GeoCandidate(1.288401, 103.846099, None, "json_ld").key == (1.2884, 103.8461)


def resolver(mapping: dict[str, list[str]]) -> Any:
    def resolve(host: str) -> list[str]:
        if host not in mapping:
            raise OSError("NXDOMAIN")
        return mapping[host]

    return resolve


def test_only_public_https_hosts_are_fetchable() -> None:
    resolve = resolver(
        {
            "example.com": ["93.184.216.34"],
            "postgres": ["172.18.0.2"],
            "metadata.google.internal": ["169.254.169.254"],
            "split.example": ["93.184.216.34", "127.0.0.1"],
            "v6.example": ["2606:2800:220:1:248:1893:25c8:1946"],
            "ula.example": ["fd00::1"],
        }
    )

    assert is_public_https_url("https://example.com/page", resolve) is True
    assert is_public_https_url("https://v6.example/page", resolve) is True
    # http is never followed, however public the host is
    assert is_public_https_url("http://example.com/page", resolve) is False
    # the compose network, the cloud metadata endpoint and IPv6 unique-local are all refused
    assert is_public_https_url("https://postgres:5432/", resolve) is False
    assert is_public_https_url("https://metadata.google.internal/", resolve) is False
    assert is_public_https_url("https://ula.example/", resolve) is False
    # one private address among several is enough to refuse the name
    assert is_public_https_url("https://split.example/", resolve) is False
    assert is_public_https_url("https://nowhere.example/", resolve) is False
    assert is_public_https_url("https://192.168.1.10/", resolver({})) is False


@pytest.mark.asyncio
async def test_a_redirect_into_the_private_network_is_refused() -> None:
    resolve = resolver({"public.example": ["93.184.216.34"], "postgres": ["172.18.0.2"]})
    transport = httpx.MockTransport(
        lambda request: httpx.Response(302, headers={"location": "https://postgres:5432/"})
    )
    async with httpx.AsyncClient(transport=transport, follow_redirects=False) as client:
        fetch = build_fetcher(client, resolve)

        assert await fetch("https://public.example/start") is None


@pytest.mark.asyncio
async def test_a_public_redirect_is_followed_and_the_body_is_capped() -> None:
    resolve = resolver({"a.example": ["93.184.216.34"], "b.example": ["93.184.216.35"]})

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "a.example":
            return httpx.Response(301, headers={"location": "https://b.example/final"})
        return httpx.Response(
            200,
            headers={"content-type": "text/html; charset=utf-8"},
            content=("x" * (MAX_BYTES + 1000)).encode(),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        body = await build_fetcher(client, resolve)("https://a.example/start")

    assert body is not None
    assert len(body) <= MAX_BYTES


@pytest.mark.asyncio
async def test_a_redirect_loop_and_a_non_html_body_both_give_up() -> None:
    resolve = resolver({"loop.example": ["93.184.216.34"], "pdf.example": ["93.184.216.35"]})

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "loop.example":
            return httpx.Response(302, headers={"location": "https://loop.example/again"})
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        fetch = build_fetcher(client, resolve)

        assert await fetch("https://loop.example/start") is None
        assert await fetch("https://pdf.example/menu") is None
