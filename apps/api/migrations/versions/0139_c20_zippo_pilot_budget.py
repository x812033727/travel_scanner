"""Seed only the held C20 short-v8 pilot account.

Revision ID: 0139_c20_zippo_pilot_budget
Revises: 0138_story_everyday_budget

The paid admission guard continues to refuse all everyday-story slugs.
"""

import re
from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0139_c20_zippo_pilot_budget"
down_revision: str | None = "0138_story_everyday_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SLUG = "story-everyday-zippo-c20-short-v8"
OWNERSHIP = "video_pilot_budget_0139_owned"
PRIOR_OWNERSHIP = "video_pilot_budget_0138_owned"
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
}
HISTORICAL = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)
OWNED_SLUGS = HISTORICAL + (
    "story-everyday-dr-martens-c07",
    "story-everyday-oxo-c10",
    "story-everyday-frixion-c15",
)


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("0139 requires online C20 account verification")
    bind = op.get_bind()
    bind.execute(sa.text(
        "LOCK TABLE video_pilot_budgets, video_pilot_budget_operations "
        "IN SHARE ROW EXCLUSIVE MODE"
    ))
    accounts = bind.execute(sa.text(
        "SELECT slug, limit_usd, created_at FROM video_pilot_budgets"
    )).mappings().all()
    if len(accounts) != len(PRIOR_LIMITS) or {
        row["slug"]: Decimal(row["limit_usd"]) for row in accounts
    } != PRIOR_LIMITS:
        raise RuntimeError("0139 prior account inventory is not reviewed 0138")
    accounts_by_slug = {row["slug"]: row for row in accounts}
    holds = bind.execute(sa.text(
        "SELECT id, slug, category, provider, model, max_usd, actual_usd, "
        "status, attempts, receipt_ref, release_reason "
        "FROM video_pilot_budget_operations "
        "WHERE operation_id = 'pre-ledger-history'"
    )).mappings().all()
    if len(holds) != len(HISTORICAL) or {row["slug"] for row in holds} != set(HISTORICAL):
        raise RuntimeError("0139 historical C-series holds are missing")
    for row in holds:
        if (row["category"], row["provider"], row["model"], row["max_usd"],
                row["attempts"]) != (
                    "historical", "unattributed", "unattributed", Decimal("25"), 1
                ):
            raise RuntimeError("0139 historical C-series hold identity changed")
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
            raise RuntimeError("0139 historical C-series hold outcome is invalid")
    holds_by_slug = {row["slug"]: row for row in holds}
    if not sa.inspect(bind).has_table(PRIOR_OWNERSHIP):
        raise RuntimeError("0139 prior ownership table is missing")
    bind.execute(sa.text(
        "LOCK TABLE video_pilot_budget_0138_owned IN SHARE ROW EXCLUSIVE MODE"
    ))
    owners = bind.execute(sa.text(
        "SELECT slug, account_created, account_created_at, hold_created, hold_id "
        "FROM video_pilot_budget_0138_owned"
    )).mappings().all()
    if len(owners) != len(OWNED_SLUGS) or {
        row["slug"] for row in owners
    } != set(OWNED_SLUGS):
        raise RuntimeError("0139 prior ownership inventory is invalid")
    for row in owners:
        slug = row["slug"]
        if (row["account_created"] not in (True, False)
                or row["account_created_at"] != accounts_by_slug[slug]["created_at"]):
            raise RuntimeError("0139 prior account ownership changed")
        if slug in HISTORICAL:
            if (row["hold_created"] not in (True, False)
                    or row["hold_id"] != holds_by_slug[slug]["id"]):
                raise RuntimeError("0139 prior historical hold ownership changed")
        elif row["hold_created"] is not False or row["hold_id"] is not None:
            raise RuntimeError("0139 prior new-pilot ownership changed")
    if sa.inspect(bind).has_table(OWNERSHIP):
        raise RuntimeError("0139 ownership table already exists")
    if bind.execute(sa.text(
        "SELECT 1 FROM video_pilot_budgets WHERE slug = :slug"
    ), {"slug": SLUG}).first() is not None:
        raise RuntimeError("0139 C20 account predates reviewed migration")
    op.create_table(
        OWNERSHIP,
        sa.Column("slug", sa.String(80), primary_key=True),
        sa.Column("account_created", sa.Boolean(), nullable=False),
        sa.Column("account_created_at", sa.DateTime(timezone=True), nullable=False),
    )
    row = bind.execute(sa.text(
        "INSERT INTO video_pilot_budgets(slug, limit_usd, created_at) "
        "VALUES (:slug, 25.000000, now()) RETURNING created_at"
    ), {"slug": SLUG}).one()
    bind.execute(sa.text(
        "INSERT INTO video_pilot_budget_0139_owned "
        "(slug, account_created, account_created_at) "
        "VALUES (:slug, true, :created_at)"
    ), {"slug": SLUG, "created_at": row[0]})


def downgrade() -> None:
    raise RuntimeError("C20 ledger evidence cannot be erased automatically")
