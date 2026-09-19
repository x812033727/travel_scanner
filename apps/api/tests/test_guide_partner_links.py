"""Partner links: non-travel affiliate programs placed in an article, and how a click is counted.

Reuses the guides fixtures (SQLite plus the optional PostgreSQL leg), so every rule is proven
through the endpoints the editor and the reader actually use.
"""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import func, select, update

from app.affiliates import content_links
from app.affiliates.content_links import (
    AFFILIATE_QUERY_KEYS,
    CONTENT_PARTNERS,
    HOST_SCOPED_KEYS,
    affiliate_marker,
    host_matches,
    link_key,
)
from app.affiliates.sub_id import SUB_ID_RE
from app.guides import router as guides_router
from app.guides.admin_service import _ordinary_urls
from app.guides.content_pack import default_directory, load_packs
from app.guides.models import GuideArticle, GuideArticleLocale
from app.guides.publication import today
from app.models import AffiliateClick
from app.problems import AppError
from app.travel_services.registry import BRANDS
from app.travel_services.schemas import untracked_url
from tests import test_guides as guides

# The guides fixtures, registered here under their own names (see test_guides_content_pack).
database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
publish = guides.publish
set_hidden = guides.set_hidden

HOSTINGER = "https://www.hostinger.com/tw/vps-hosting?aff_id=12345"
BOOK = (
    "https://www.books.com.tw/exep/assp.php/mokaair/products/0010999999"
    "?utm_source=mokaair&utm_medium=ap-books"
)


@pytest.fixture(autouse=True)
def limiter(monkeypatch) -> AsyncMock:
    mock = AsyncMock()
    monkeypatch.setattr(guides_router, "enforce_named_rate_limit", mock)
    return mock


def partner_block(url: str = HOSTINGER, partner: str = "hostinger", **extra: str) -> dict:
    return {"type": "partner_link", "partner": partner, "url": url, "label": "看方案", **extra}


def article_document(*blocks: dict) -> dict:
    base = document(title="用 Claude Code 把網站部署到 VPS", description="從本機到上線的步驟")
    return {**base, "blocks": [*base["blocks"], *blocks]}


async def post_article(api, *blocks: dict, slug="claude-code-vps", kind="life", **extra):
    return await api.post(
        "/admin/guides",
        json={
            "slug": slug,
            "kind": kind,
            "destination_id": None,
            "topics": ["ai"] if kind == "life" else ["transport"],
            "document": article_document(*blocks),
            "locale": "zh-TW",
            **extra,
        },
    )


async def published_article(api, *blocks: dict, **extra) -> dict:
    created = await post_article(api, *blocks, **extra)
    assert created.status_code == 201, created.text
    body = created.json()
    published = await publish(api, body["id"], "zh-TW", body["locales"][0]["version"])
    assert published.status_code == 200, published.text
    return published.json()


async def click_count(database) -> int:
    async with database() as session:
        return int(await session.scalar(select(func.count()).select_from(AffiliateClick)) or 0)


# --- what the reader gets -------------------------------------------------------------


async def test_a_partner_link_reaches_the_reader_with_a_key_and_the_partner_name(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        await published_article(
            api,
            partner_block(note="本站就架在這個方案上"),
            {"type": "paragraph", "text": "年繳方案才有佣金，月繳沒有。"},
            # The same link placed twice is one link: one entry, one key, one click count.
            partner_block(label="再看一次方案"),
            partner_block(BOOK, "books_com_tw", label="延伸閱讀"),
        )
        body = (await api.get("/guides/life/claude-code-vps", params={"locale": "zh-TW"})).json()
    assert body["partner_links"] == [
        {
            "key": link_key(HOSTINGER),
            "partner": "hostinger",
            "display_name": "Hostinger",
            "url": HOSTINGER,
        },
        {"key": link_key(BOOK), "partner": "books_com_tw", "display_name": "博客來", "url": BOOK},
    ]
    stored = [block for block in body["document"]["blocks"] if block["type"] == "partner_link"]
    assert stored[0] == partner_block(note="本站就架在這個方案上")
    assert stored[1]["note"] == ""


async def test_a_travel_article_may_carry_a_partner_link_too(database, actor) -> None:
    """The registry holds no travel brand, so allowing every kind opens no way around the
    catalog's own approval of travel offers."""
    async with client(make_app(database, actor)) as api:
        await published_article(api, partner_block(BOOK, "books_com_tw"), kind="howto")
        body = (await api.get("/guides/howto/claude-code-vps", params={"locale": "zh-TW"})).json()
    assert [link["partner"] for link in body["partner_links"]] == ["books_com_tw"]


# --- what an editor may write ---------------------------------------------------------


@pytest.mark.parametrize(
    ("block", "code"),
    [
        (partner_block(partner="notion"), "partner_link_unknown"),
        (partner_block(BOOK), "partner_link_host"),
        (partner_block("https://evilhostinger.com/tw?aff_id=1"), "partner_link_host"),
        (partner_block("https://hostinger.com.example.net/tw"), "partner_link_host"),
        (
            partner_block("https://www.hostinger.com/tw?REFERRALCODE=ABCDEF12"),
            "partner_link_forbidden",
        ),
    ],
    ids=["unknown-partner", "other-partners-host", "lookalike", "suffix-trick", "referral"],
)
async def test_a_partner_link_is_checked_against_the_registry(
    database, actor, block, code
) -> None:
    async with client(make_app(database, actor)) as api:
        response = await post_article(api, block)
    assert response.status_code == 422, response.text
    assert response.json()["code"] == code
    if code == "partner_link_forbidden":
        assert "REFERRALCODE" in response.json()["detail"]


@pytest.mark.parametrize(
    "block",
    [
        partner_block("http://www.hostinger.com/tw"),
        partner_block(partner="Hostinger"),
        partner_block(label=""),
        partner_block("javascript:alert(1)"),
    ],
    ids=["plain-http", "code-casing", "blank-label", "script-url"],
)
async def test_a_malformed_partner_link_never_reaches_the_registry(database, actor, block) -> None:
    async with client(make_app(database, actor)) as api:
        response = await post_article(api, block)
    assert response.status_code == 422
    assert not response.json()["code"].startswith("partner_link_")


async def test_more_than_three_partner_links_are_refused(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        response = await post_article(api, *[partner_block(label=f"方案 {n}") for n in range(4)])
    assert response.status_code == 422
    assert response.json()["code"] == "guide_partner_link_limit"


async def test_a_removed_partner_degrades_to_no_link_rather_than_an_error(
    database, actor, monkeypatch
) -> None:
    async with client(make_app(database, actor)) as api:
        published = await published_article(api, partner_block())
        monkeypatch.setattr(content_links, "PARTNERS_BY_CODE", {})

        public = await api.get("/guides/life/claude-code-vps", params={"locale": "zh-TW"})
        assert public.status_code == 200
        assert public.json()["partner_links"] == []
        # The stored block is untouched; only the reader's page stops drawing it.
        assert public.json()["document"]["blocks"][-1]["partner"] == "hostinger"

        detail = await api.get(f"/admin/guides/{published['id']}", params={"locale": "zh-TW"})
        assert detail.status_code == 200

        clicked = await api.post(
            f"/guides/life/claude-code-vps/partner-links/{link_key(HOSTINGER)}/click"
        )
        assert clicked.status_code == 404
        assert clicked.json()["code"] == "affiliate_link_not_found"

        again = await publish(api, published["id"], "zh-TW", published["locales"][0]["version"])
        assert again.status_code == 422
        assert again.json()["code"] == "partner_link_unknown"
    assert await click_count(database) == 0


# --- counting a click -----------------------------------------------------------------


@pytest.mark.parametrize(("kind", "placement"), [("life", "life"), ("howto", "guide")])
async def test_a_click_writes_one_anonymous_row_and_never_redirects(
    database, actor, limiter, kind, placement
) -> None:
    async with client(make_app(database, actor)) as api:
        await published_article(api, partner_block(), kind=kind)
        response = await api.post(
            f"/guides/{kind}/claude-code-vps/partner-links/{link_key(HOSTINGER)}/click",
            params={"locale": "zh-TW"},
        )
    assert response.status_code == 204
    assert "location" not in response.headers
    assert response.headers["cache-control"] == "no-store"
    assert limiter.await_args is not None
    assert limiter.await_args.args[0] == "guide-partner-click"
    async with database() as session:
        rows = list(await session.scalars(select(AffiliateClick)))
    assert len(rows) == 1
    row = rows[0]
    assert (row.partner, row.brand, row.module, row.placement) == (
        "hostinger", "hostinger", "hosting", placement,
    )
    assert row.sub_id == f"cnt_hosting_zh-TW_{placement}"
    assert SUB_ID_RE.fullmatch(row.sub_id)
    assert row.destination_summary == "claude-code-vps"
    assert row.article_slug == "claude-code-vps"
    assert row.target_host == "www.hostinger.com"
    assert row.status == "clicked"
    assert row.user_id is None and row.trip_id is None and row.search_id is None
    assert row.destination_id is None and row.offer_id is None


async def test_clicks_the_reader_could_not_have_made_write_nothing(database, actor) -> None:
    key = link_key(HOSTINGER)
    async with client(make_app(database, actor)) as api:
        draft = await post_article(api, partner_block(), slug="still-a-draft")
        assert draft.status_code == 201
        assert (
            await api.post(f"/guides/life/still-a-draft/partner-links/{key}/click")
        ).status_code == 404

        published = await published_article(api, partner_block())
        path = f"/guides/life/claude-code-vps/partner-links/{key}/click"
        for response in (
            await api.post(path, params={"locale": "ja"}),
            await api.post(path.replace("/life/", "/howto/")),
            await api.post(path.replace(key, link_key(BOOK))),
        ):
            assert response.status_code == 404, response.text
        assert (await api.post(path.replace(key, "not-a-key"))).status_code == 422

        hidden = await set_hidden(api, published["id"], published["version"])
        assert hidden.status_code == 200, hidden.text
        assert (await api.post(path)).status_code == 404
    assert await click_count(database) == 0


async def test_an_expired_notice_draws_and_counts_no_partner_link(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published_article(
            api, partner_block(), valid_until=(today() + timedelta(days=1)).isoformat()
        )
        async with database() as session:
            await session.execute(
                update(GuideArticle).values(valid_until=today() - timedelta(days=1))
            )
            await session.commit()
        body = (await api.get("/guides/life/claude-code-vps", params={"locale": "zh-TW"})).json()
        assert body["expired"] is True
        assert body["partner_links"] == []
        clicked = await api.post(
            f"/guides/life/claude-code-vps/partner-links/{link_key(HOSTINGER)}/click"
        )
        assert clicked.status_code == 404
    assert await click_count(database) == 0


async def test_a_rate_limited_click_writes_nothing(database, actor, limiter) -> None:
    limiter.side_effect = AppError(429, "rate_limit_exceeded", "請求過於頻繁，請稍後再試")
    async with client(make_app(database, actor)) as api:
        await published_article(api, partner_block())
        response = await api.post(
            f"/guides/life/claude-code-vps/partner-links/{link_key(HOSTINGER)}/click"
        )
    assert response.status_code == 429
    assert await click_count(database) == 0


# --- keeping affiliate URLs out of ordinary links -------------------------------------

TRACKED = "https://www.booking.com/hotel/jp/example.html?aid=304142"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda doc: doc["blocks"].append({"type": "link", "text": "訂房", "url": TRACKED}),
        lambda doc: doc["sources"].append({"title": "short", "url": "https://bit.ly/3abcdef"}),
        lambda doc: doc.update(
            hero={
                "src": "/guides/claude-code-vps/hero.jpg",
                "alt": "終端機畫面",
                "width": 1600,
                "height": 900,
                "credit": {
                    "author": "Someone",
                    "license": "CC BY 4.0",
                    "source_url": "https://tp.st/abc123",
                },
            }
        ),
        lambda doc: doc["blocks"].append(
            {
                "type": "image",
                "src": "/guides/claude-code-vps/step-1.webp",
                "alt": "步驟一",
                "width": 1200,
                "height": 800,
                "credit": {
                    "author": "Someone",
                    "license": "CC BY 4.0",
                    "source_url": "https://example.org/photo?aff_id=9",
                },
            }
        ),
    ],
    ids=["link-block", "source", "hero-credit", "image-credit"],
)
async def test_an_ordinary_url_may_not_carry_affiliate_tracking(database, actor, mutate) -> None:
    tracked = article_document()
    mutate(tracked)
    async with client(make_app(database, actor)) as api:
        created = await post_article(api)
        assert created.status_code == 201
        body = created.json()

        refused = await api.post(
            "/admin/guides",
            json={"slug": "tracked", "kind": "life", "topics": [], "document": tracked},
        )
        assert refused.status_code == 422
        assert refused.json()["code"] == "content_link_affiliate"

        draft = await api.put(
            f"/admin/guides/{body['id']}/zh-TW/draft",
            json={"expected_version": body["locales"][0]["version"], "document": tracked},
        )
        assert draft.status_code == 422
        assert draft.json()["code"] == "content_link_affiliate"

        # A draft stored before the rule existed can still be opened, but not published.
        async with database() as session:
            await session.execute(update(GuideArticleLocale).values(draft_json=tracked))
            await session.commit()
        opened = await api.get(f"/admin/guides/{body['id']}", params={"locale": "zh-TW"})
        assert opened.status_code == 200
        published = await publish(api, body["id"], "zh-TW", body["locales"][0]["version"])
        assert published.status_code == 422
        assert published.json()["code"] == "content_link_affiliate"


@pytest.mark.parametrize(
    "url",
    [
        "https://www.ftc.gov.tw/internet/main/doc/docDetail.aspx?uid=165&docid=13021",
        "https://news.example.com/story?aid=1234&cid=5",
        "https://www.jreast.co.jp/tw/?utm_source=newsletter",
        "https://www.hostinger.com/tutorials/vps-hosting",
        "https://www.books.com.tw/products/0010999999",
        "https://docs.claude.com/en/docs/claude-code/overview",
        "mailto:support@mokaair.com",
    ],
)
def test_an_ordinary_link_is_left_alone(url: str) -> None:
    assert affiliate_marker(url) is None


@pytest.mark.parametrize(
    ("url", "marker"),
    [
        ("https://www.klook.com/activity/1-x/?aid=134379", "aid"),
        ("https://www.agoda.com/zh-tw/hotel.html?cid=1844104", "cid"),
        ("https://www.amazon.co.jp/dp/B000000000?tag=mokaair-22", "tag"),
        ("https://www.trip.com/hotels/?Allianceid=1&SID=2", "allianceid"),
        ("https://www.hostinger.com/tw?REFERRALCODE=ABCDEF12", "referralcode"),
        ("https://www.books.com.tw/exep/assp.php/mokaair/products/0010999999", "/exep/assp.php/"),
        ("https://anything.example/page?aff_id=1", "aff_id"),
        ("https://n8n.partnerlinks.io/abc", "partnerlinks.io"),
        ("https://reurl.cc/abc", "reurl.cc"),
    ],
)
def test_an_affiliate_or_short_link_is_recognised(url: str, marker: str) -> None:
    assert affiliate_marker(url) == marker


@pytest.mark.parametrize(
    "key",
    [
        "marker", "trs", "aid", "cid", "aff", "affiliate_id", "aff_id",
        "sub_id", "tag", "sid", "clickid", "irclickid", "utm_source",
    ],
)
def test_what_the_travel_catalog_refuses_an_article_refuses_too(key: str) -> None:
    """The keys ``untracked_url`` refuses on an offer target, spelled out: on a travel brand's
    own host an article link carrying any of them is just as much a tracked link."""
    url = f"https://www.klook.com/activity/1-x/?{key}=1"
    with pytest.raises(ValueError):
        untracked_url(url)
    assert affiliate_marker(url) is not None
    assert key in AFFILIATE_QUERY_KEYS | HOST_SCOPED_KEYS


def test_no_shipped_content_pack_carries_a_tracked_ordinary_link() -> None:
    packs = load_packs(default_directory())
    assert packs, "the shipped packs moved; this test is no longer looking at them"
    offenders = [
        f"{pack.slug}/{locale}: {url}"
        for pack in packs
        for locale, pack_document in pack.locales.items()
        for url in _ordinary_urls(pack_document)
        if affiliate_marker(url) is not None
    ]
    assert offenders == []


def test_no_content_partner_is_a_travel_brand_or_shares_a_host() -> None:
    travel_hosts = [host for brand in BRANDS.values() for host in brand.hosts]
    seen: list[str] = []
    for partner in CONTENT_PARTNERS:
        assert partner.code not in BRANDS
        assert SUB_ID_RE.fullmatch(f"cnt_{partner.category}_zh-TW_life")
        for host in partner.hosts:
            assert not any(host_matches(host, t) or host_matches(t, host) for t in travel_hosts)
            assert not any(host_matches(host, s) or host_matches(s, host) for s in seen)
        seen.extend(partner.hosts)


async def test_the_partner_list_is_for_admins_and_not_mistaken_for_an_article(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        response = await api.get("/admin/guides/partners")
    assert response.status_code == 200, response.text
    partners = {item["code"]: item for item in response.json()["partners"]}
    assert partners["hostinger"] == {
        "code": "hostinger",
        "display_name": "Hostinger",
        "category": "hosting",
        "hosts": ["hostinger.com"],
    }
    assert "books_com_tw" in partners
    async with client(make_app(database)) as anonymous:
        assert (await anonymous.get("/admin/guides/partners")).status_code in {401, 403}
