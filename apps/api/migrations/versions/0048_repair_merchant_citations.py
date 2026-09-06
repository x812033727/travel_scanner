"""Repair the five first-party merchant citations that no longer open.

Revision ID: 0048_repair_merchant_citations
Revises: 0047_ai_vendor_settings

``MERCHANT_DIRECT_SOURCE_SEEDS`` is copied onto ``food_merchant_sources`` when a merchant
is seeded, and the seeder finds an existing source by its URL, so correcting the constant
alone leaves every existing row citing the dead address and adds a second row for the new
one. Five of the 63 citations could not be opened on 2026-09-06:

* ``hanlin-tea.com.tw`` resets every connection;
* ``taicheongbakery.com.hk`` serves a certificate that does not cover its own hostname;
* ``krua-apsorn.com`` answers 500 at every path;
* the Krabi citation was a 2019 PDF, not a page about the restaurant;
* the Singapore citation was a PDF that never named Hill Street Fried Kway Teow.

Four are rewritten to the tourism board's page about that merchant, each fetched and read
before this was written; the fifth is deleted, because a merchant with no first-party
source is honest and one with a dead link is not. None of the replacements is the shop's
own site, so a merchant whose official website was copied from the dead URL loses it. The
rewrite matches the exact old string, so a row an administrator has since edited by hand
is untouched.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0048_repair_merchant_citations"
down_revision: str | None = "0047_ai_vendor_settings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (url, source_type, source_scope, source_title, claims)
Citation = tuple[str, str, str, str, list[str]]

REPLACEMENTS: tuple[tuple[Citation, Citation], ...] = (
    (
        (
            "https://www.hanlin-tea.com.tw/",
            "merchant_official",
            "merchant_website",
            "Hanlin Tea Room official website",
            ["display_name", "official_website"],
        ),
        (
            "https://www.twtainan.net/zh-tw/shop/consume/2236/",
            "official_tourism",
            "merchant_listing",
            "Tainan City tourism listing for Hanlin Tea Room (赤崁店)",
            ["display_name", "address"],
        ),
    ),
    (
        (
            "https://www.taicheongbakery.com.hk/en/brands/tai_cheong/index.html",
            "merchant_official",
            "merchant_website",
            "Tai Cheong Bakery official website",
            ["display_name", "official_website"],
        ),
        (
            "https://www.discoverhongkong.com/eng/place-to-go/travel.guide-tai-cheong-bakery.html",
            "official_tourism",
            "merchant_listing",
            "Hong Kong Tourism Board listing for Tai Cheong Bakery",
            ["display_name", "address"],
        ),
    ),
    (
        (
            "https://www.krua-apsorn.com/",
            "merchant_official",
            "merchant_website",
            "Krua Apsorn official website",
            ["display_name", "address", "official_website"],
        ),
        (
            "https://www.tourismthailand.org/Restaurant/krua-apsorn",
            "official_tourism",
            "merchant_listing",
            "Tourism Authority of Thailand listing for Krua Apsorn",
            ["display_name", "address"],
        ),
    ),
    (
        (
            "https://www.thailandtravel.or.jp/common/pdf/Krabi_trang2019.pdf",
            "official_tourism",
            "merchant_listing",
            "Tourism Authority of Thailand Krabi restaurant guide",
            ["display_name", "address"],
        ),
        (
            "https://www.tourismthailand.org/Restaurant/ruean-mai",
            "official_tourism",
            "merchant_listing",
            "Tourism Authority of Thailand listing for Ruean Mai",
            ["display_name", "address"],
        ),
    ),
)

REMOVALS: tuple[str, ...] = (
    "https://www.visitsingapore.com/content/dam/desktop/global/deals/hk/Singapore_Food_Guide_PDF.pdf",
)


def _rewrite(pairs: Sequence[tuple[Citation, Citation]]) -> None:
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    for old, new in pairs:
        if "food_merchant_sources" in tables:
            bind.execute(
                sa.text(
                    """
                    UPDATE food_merchant_sources
                       SET source_url = :new_url,
                           source_type = :new_type,
                           source_scope = :new_scope,
                           source_title = :new_title,
                           claims_json = CAST(:new_claims AS json),
                           last_verified_at = now()
                     WHERE source_url = :old_url
                    """
                ),
                {
                    "new_url": new[0],
                    "new_type": new[1],
                    "new_scope": new[2],
                    "new_title": new[3],
                    "new_claims": json.dumps(new[4]),
                    "old_url": old[0],
                },
            )
        if "food_merchants" in tables and new[2] != "merchant_website":
            bind.execute(
                sa.text(
                    """
                    UPDATE food_merchants
                       SET official_website_url = NULL,
                           official_website_verified_at = NULL
                     WHERE official_website_url = :old_url
                    """
                ),
                {"old_url": old[0]},
            )


def upgrade() -> None:
    _rewrite(REPLACEMENTS)
    bind = op.get_bind()
    if "food_merchant_sources" in set(sa.inspect(bind).get_table_names()):
        for url in REMOVALS:
            bind.execute(
                sa.text("DELETE FROM food_merchant_sources WHERE source_url = :url"),
                {"url": url},
            )


def downgrade() -> None:
    # The dead URLs come back as citations; the deleted Singapore row and the cleared
    # official-website fields are not restored, the next seed run rebuilds the former.
    _rewrite([(new, old) for old, new in REPLACEMENTS])
