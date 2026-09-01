"""Add stable destination identity to hotspots.

Revision ID: 0019_hotspot_destination_id
Revises: 0018_hotspot_multilingual_guides
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0019_hotspot_destination_id"
down_revision: str | None = "0018_hotspot_multilingual_guides"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


LEGACY_IDS = {
    "NRT": "tokyo",
    "KIX": "osaka-kyoto",
    "FUK": "fukuoka",
    "CTS": "sapporo",
    "OKA": "okinawa",
    "NGO": "nagoya",
    "ICN": "seoul",
    "PUS": "busan",
    "CJU": "jeju",
    "BKK": "bangkok",
    "CNX": "chiang-mai",
    "HKT": "phuket",
    "KBV": "krabi",
    "TPE": "taipei",
    "SIN": "singapore",
    "HKG": "hong-kong",
    "HAN": "hanoi",
    "SGN": "ho-chi-minh-city",
    "DAD": "da-nang",
}


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {str(column["name"]) for column in inspector.get_columns("travel_hotspots")}
    if "destination_id" not in columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("destination_id", sa.String(64), nullable=True),
        )
        table = sa.table(
            "travel_hotspots",
            sa.column("city_code", sa.String()),
            sa.column("destination_id", sa.String()),
        )
        for city_code, destination_id in LEGACY_IDS.items():
            op.execute(
                table.update()
                .where(table.c.city_code == city_code)
                .values(destination_id=destination_id)
            )
        op.execute(
            table.update()
            .where(table.c.destination_id.is_(None))
            .values(destination_id=sa.func.lower(table.c.city_code))
        )
        op.alter_column("travel_hotspots", "destination_id", nullable=False)
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("travel_hotspots")}
    if "ix_travel_hotspots_destination_id" not in indexes:
        op.create_index(
            "ix_travel_hotspots_destination_id",
            "travel_hotspots",
            ["destination_id"],
        )


def downgrade() -> None:
    op.drop_index("ix_travel_hotspots_destination_id", table_name="travel_hotspots")
    op.drop_column("travel_hotspots", "destination_id")
