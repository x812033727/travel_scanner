"""Seed the USD 25 accounts of six story remakes the owner approved on 2026-10-26.

Revision ID: 0141_story_remake_budgets
Revises: 0140_c11_ucc_remake_budget

Each remake is a new film with no pre-ledger history. An account alone admits no paid
request; the application's activated-slug list decides.
"""

import re
from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0141_story_remake_budgets"
down_revision: str | None = "0140_c11_ucc_remake_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SLUGS = (
    "story-everyday-camelbak-c14-remake-20261025",
    "story-everyday-moleskine-c03-remake-20261025",
    "story-everyday-bubble-wrap-c04-remake-20261025",
    "story-everyday-play-doh-c06-remake-20261025",
    "story-everyday-kincho-c05-remake-20261025",
    "story-everyday-kikkoman-c08-remake-20261025",
)
OWNERSHIP = "video_pilot_budget_0141_owned"
C20_SLUG = "story-everyday-zippo-c20-short-v8"
C11_SLUG = "story-everyday-ucc-c11-remake-20261025"
PRIOR_OWNERS = {
    "video_pilot_budget_0139_owned": C20_SLUG,
    "video_pilot_budget_0140_owned": C11_SLUG,
}
PRIOR_LIMITS = {
    "story-rolling-suitcase": Decimal("25"),
    "story-conveyor-belt-sushi": Decimal("25"),
    "story-rolling-suitcase-v2": Decimal("25"),
    "story-conveyor-belt-sushi-v2": Decimal("5"),
    "story-five-lego-legoland": Decimal("5"),
    "story-five-costco-hot-dog": Decimal("5"),
    "story-five-adidas-puma-brothers": Decimal("5"),
    "story-five-ajinomoto-chip-film": Decimal("5"),
    "story-five-pringles-vat-case": Decimal("5"),
    "story-everyday-moleskine-c03": Decimal("25"),
    "story-everyday-bubble-wrap-c04": Decimal("25"),
    "story-everyday-kincho-c05": Decimal("25"),
    "story-everyday-play-doh-c06": Decimal("25"),
    "story-everyday-dr-martens-c07": Decimal("25"),
    "story-everyday-oxo-c10": Decimal("25"),
    "story-everyday-frixion-c15": Decimal("25"),
    C20_SLUG: Decimal("25"),
    C11_SLUG: Decimal("25"),
}
HISTORICAL = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("0141 requires online remake account verification")
    bind = op.get_bind()
    bind.execute(sa.text(
        "LOCK TABLE video_pilot_budgets, video_pilot_budget_operations, "
        "video_pilot_budget_0139_owned, video_pilot_budget_0140_owned "
        "IN SHARE ROW EXCLUSIVE MODE"
    ))
    accounts = bind.execute(sa.text(
        "SELECT slug, limit_usd, created_at FROM video_pilot_budgets"
    )).mappings().all()
    if len(accounts) != len(PRIOR_LIMITS) or {
        row["slug"]: Decimal(row["limit_usd"]) for row in accounts
    } != PRIOR_LIMITS:
        raise RuntimeError("0141 prior account inventory is not reviewed 0140")
    accounts_by_slug = {row["slug"]: row for row in accounts}
    holds = bind.execute(sa.text(
        "SELECT slug, category, provider, model, max_usd, actual_usd, "
        "status, attempts, receipt_ref, release_reason "
        "FROM video_pilot_budget_operations "
        "WHERE operation_id = 'pre-ledger-history'"
    )).mappings().all()
    if len(holds) != len(HISTORICAL) or {row["slug"] for row in holds} != set(HISTORICAL):
        raise RuntimeError("0141 historical C-series holds are missing")
    for row in holds:
        if (row["category"], row["provider"], row["model"], row["max_usd"],
                row["attempts"]) != (
                    "historical", "unattributed", "unattributed", Decimal("25"), 1
                ):
            raise RuntimeError("0141 historical C-series hold identity changed")
        actual = row["actual_usd"]
        status = row["status"]
        receipt = row["receipt_ref"]
        release_reason = row["release_reason"]
        if status == "uncertain":
            valid = actual is None and receipt is None and release_reason is None
        elif status == "settled":
            valid = actual is not None and bool(receipt)
        elif status == "released":
            valid = (actual is None and isinstance(release_reason, str)
                     and bool(re.fullmatch(
                         r"operator-no-charge evidence=[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}; \S.*",
                         release_reason,
                     )))
        else:
            valid = False
        if not valid:
            raise RuntimeError("0141 historical C-series hold outcome is invalid")
    for table, slug in PRIOR_OWNERS.items():
        owners = bind.execute(sa.text(
            f"SELECT slug, account_created, account_created_at FROM {table}"
        )).mappings().all()
        if (len(owners) != 1 or owners[0]["slug"] != slug
                or owners[0]["account_created"] is not True
                or owners[0]["account_created_at"] != accounts_by_slug[slug]["created_at"]):
            raise RuntimeError(f"0141 prior ownership {table} changed")
        prior_pk = sa.inspect(bind).get_pk_constraint(table)
        if (prior_pk.get("name") != f"{table}_pkey"
                or prior_pk.get("constrained_columns") != ["slug"]):
            raise RuntimeError(f"0141 prior ownership {table} primary key changed")
    if sa.inspect(bind).has_table(OWNERSHIP):
        raise RuntimeError("0141 ownership table already exists")
    op.create_table(
        OWNERSHIP,
        sa.Column("slug", sa.String(80), primary_key=True),
        sa.Column("account_created", sa.Boolean(), nullable=False),
        sa.Column("account_created_at", sa.DateTime(timezone=True), nullable=False),
    )
    for slug in SLUGS:
        row = bind.execute(sa.text(
            "INSERT INTO video_pilot_budgets(slug, limit_usd, created_at) "
            "VALUES (:slug, 25.000000, now()) RETURNING created_at"
        ), {"slug": slug}).one()
        bind.execute(sa.text(
            "INSERT INTO video_pilot_budget_0141_owned "
            "(slug, account_created, account_created_at) "
            "VALUES (:slug, true, :created_at)"
        ), {"slug": slug, "created_at": row[0]})


def downgrade() -> None:
    raise RuntimeError("Story remake ledger evidence cannot be erased automatically")
