"""Repair the two official food source URLs that no longer point at a food page.

Revision ID: 0039_repair_dead_food_sources
Revises: 0038_trip_metadata

``OFFICIAL_FOOD_SOURCES`` is read when a row is created and then stored on it, so
correcting the constant leaves every existing row citing the old address. Two of them had
rotted:

* the JP page answers ``404`` outright, and it is the first source of all ten Japanese
  dishes;
* the TW address still answers ``200`` but now renders "New Taipei City", so twenty dishes
  and four destinations cite a page that says nothing about food.

Both replacements were fetched and checked before this was written. The update is a
targeted rewrite of those two exact strings, so a source an administrator has since edited
by hand is untouched.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0039_repair_dead_food_sources"
down_revision: str | None = "0038_trip_metadata"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REPLACEMENTS = (
    (
        "https://www.japan.travel/en/uk/inspiration/food-and-drink/",
        "https://www.japan.travel/en/things-to-do/eat-and-drink/",
    ),
    (
        "https://eng.taiwan.net.tw/m1.aspx?sNo=0002091",
        "https://eng.taiwan.net.tw/m1.aspx?sNo=0002026",
    ),
)


def _rewrite(pairs: Sequence[tuple[str, str]]) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    for old, new in pairs:
        if "food_merchant_sources" in tables:
            bind.execute(
                sa.text(
                    "UPDATE food_merchant_sources SET source_url = :new WHERE source_url = :old"
                ),
                {"new": new, "old": old},
            )
        if "travel_foods" in tables:
            # source_urls is a JSON array of strings; rebuild it element by element so a
            # row that cites the address twice, or alongside others, still comes out right.
            bind.execute(
                sa.text(
                    """
                    UPDATE travel_foods
                       SET source_urls = (
                           SELECT json_agg(CASE WHEN value = :old THEN :new ELSE value END
                                           ORDER BY ordinality)
                             FROM json_array_elements_text(source_urls::json)
                                  WITH ORDINALITY AS elements(value, ordinality)
                       )
                     WHERE source_urls::text LIKE :pattern
                    """
                ),
                {"new": new, "old": old, "pattern": f"%{old}%"},
            )


def upgrade() -> None:
    _rewrite(REPLACEMENTS)


def downgrade() -> None:
    _rewrite([(new, old) for old, new in REPLACEMENTS])
