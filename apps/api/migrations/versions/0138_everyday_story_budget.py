"""Seed seven held C-series budget accounts without resetting earlier exposure.

Revision ID: 0138_story_everyday_budget
Revises: 0137_video_manga_tier

The previous application image recognizes this exact revision, seven USD 25 accounts,
and four full-ceiling historical holds. Its paid admission guard still refuses every
``story-everyday-*`` request. A small provenance table records which rows this migration
actually inserted, so a database downgrade cannot erase a pre-existing matching row.
"""

import re
from collections.abc import Sequence
from decimal import Decimal
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "0138_story_everyday_budget"
down_revision: str | None = "0137_video_manga_tier"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACCOUNT = "video_pilot_budgets"
OPERATIONS = "video_pilot_budget_operations"
OWNERSHIP = "video_pilot_budget_0138_owned"
LIMIT = Decimal("25.000000")
HISTORICAL_ID = "pre-ledger-history"
HISTORICAL = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)
NEW_PILOTS = (
    "story-everyday-dr-martens-c07",
    "story-everyday-oxo-c10",
    "story-everyday-frixion-c15",
)
PILOTS = HISTORICAL + NEW_PILOTS
# Freeze the reviewed 0133 account set. Importing current application constants into a
# migration would make a later replay change when those constants change.
PRIOR_LIMITS = {
    "story-rolling-suitcase": LIMIT,
    "story-conveyor-belt-sushi": LIMIT,
    "story-rolling-suitcase-v2": LIMIT,
    "story-conveyor-belt-sushi-v2": Decimal("5.000000"),
    "story-five-lego-legoland": Decimal("5.000000"),
    "story-five-costco-hot-dog": Decimal("5.000000"),
    "story-five-adidas-puma-brothers": Decimal("5.000000"),
    "story-five-ajinomoto-chip-film": Decimal("5.000000"),
    "story-five-pringles-vat-case": Decimal("5.000000"),
}


def _account() -> sa.TableClause:
    return sa.table(
        ACCOUNT,
        sa.column("slug", sa.String(80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )


def _operation() -> sa.TableClause:
    return sa.table(
        OPERATIONS,
        sa.column("id", sa.Uuid()),
        sa.column("slug", sa.String(80)),
        sa.column("operation_id", sa.String(160)),
        sa.column("category", sa.String(40)),
        sa.column("provider", sa.String(40)),
        sa.column("model", sa.String(128)),
        sa.column("max_usd", sa.Numeric(12, 6)),
        sa.column("actual_usd", sa.Numeric(12, 6)),
        sa.column("status", sa.String(12)),
        sa.column("attempts", sa.Integer()),
        sa.column("receipt_ref", sa.String(255)),
        sa.column("release_reason", sa.String(255)),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )


def _ownership() -> sa.TableClause:
    return sa.table(
        OWNERSHIP,
        sa.column("slug", sa.String(80)),
        sa.column("account_created", sa.Boolean()),
        sa.column("account_created_at", sa.DateTime(timezone=True)),
        sa.column("hold_created", sa.Boolean()),
        sa.column("hold_id", sa.Uuid()),
    )


def _online() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("0138 requires online account and provenance verification")


def _lock_budget_tables(bind: sa.Connection) -> None:
    # One short transaction prevents a concurrent writer from changing a checked row
    # between preflight, the seed, and the provenance record.
    bind.execute(sa.text(f"LOCK TABLE {ACCOUNT}, {OPERATIONS} IN SHARE ROW EXCLUSIVE MODE"))


def _account_row(bind: sa.Connection, account: sa.TableClause, slug: str) -> sa.RowMapping | None:
    return bind.execute(sa.select(account).where(account.c.slug == slug)).mappings().one_or_none()


def _hold_row(bind: sa.Connection, operation: sa.TableClause, slug: str) -> sa.RowMapping | None:
    return (
        bind.execute(
            sa.select(operation).where(
                operation.c.slug == slug,
                operation.c.operation_id == HISTORICAL_ID,
            )
        )
        .mappings()
        .one_or_none()
    )


def _verify_account(row: sa.RowMapping | None, slug: str) -> None:
    if row is None or row["limit_usd"] != LIMIT or row["created_at"] is None:
        raise RuntimeError(f"0138 account {slug} is missing or conflicts with USD 25")


def _verify_hold(row: sa.RowMapping | None, slug: str) -> None:
    if row is None or (
        row["category"],
        row["provider"],
        row["model"],
        row["max_usd"],
        row["attempts"],
    ) != ("historical", "unattributed", "unattributed", LIMIT, 1):
        raise RuntimeError(f"0138 historical hold {slug} is missing or conflicts")
    status = row["status"]
    if status == "uncertain":
        valid = (
            row["actual_usd"] is None
            and row["receipt_ref"] is None
            and row["release_reason"] is None
        )
    elif status == "settled":
        valid = row["actual_usd"] is not None and bool(row["receipt_ref"])
    elif status == "released":
        reason = row["release_reason"]
        valid = (
            row["actual_usd"] is None
            and isinstance(reason, str)
            and bool(
                re.fullmatch(
                    r"operator-no-charge evidence=[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}; \S.*",
                    reason,
                )
            )
        )
    else:
        valid = False
    if not valid:
        raise RuntimeError(f"0138 historical hold {slug} has an invalid outcome")


def _prior_accounts_match(bind: sa.Connection, account: sa.TableClause) -> None:
    rows = bind.execute(sa.select(account.c.slug, account.c.limit_usd)).all()
    prior = {slug: limit for slug, limit in rows if slug not in PILOTS}
    if len(rows) != len(prior) + sum(slug in PILOTS for slug, _ in rows):
        raise RuntimeError("0138 account inventory contains duplicate slugs")
    if prior != PRIOR_LIMITS:
        raise RuntimeError("0138 prior account inventory or limits do not match 0133")


def upgrade() -> None:
    _online()
    bind = op.get_bind()
    _lock_budget_tables(bind)
    account, operation, ownership = _account(), _operation(), _ownership()
    _prior_accounts_match(bind, account)

    already_owned = sa.inspect(bind).has_table(OWNERSHIP)
    if not already_owned:
        op.create_table(
            OWNERSHIP,
            sa.Column("slug", sa.String(80), primary_key=True),
            sa.Column("account_created", sa.Boolean(), nullable=False),
            sa.Column("account_created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("hold_created", sa.Boolean(), nullable=False),
            sa.Column("hold_id", sa.Uuid(), nullable=True),
        )
    owners = {row["slug"]: row for row in bind.execute(sa.select(ownership)).mappings()}
    if already_owned and set(owners) != set(PILOTS):
        raise RuntimeError("0138 ownership inventory is incomplete or conflicts")

    for slug in PILOTS:
        prior = owners.get(slug)
        account_row = _account_row(bind, account, slug)
        account_created = account_row is None
        if account_created:
            if prior is not None:
                raise RuntimeError(f"0138 owned account {slug} disappeared")
            bind.execute(
                sa.insert(account).values(slug=slug, limit_usd=LIMIT, created_at=sa.func.now())
            )
            account_row = _account_row(bind, account, slug)
        _verify_account(account_row, slug)
        assert account_row is not None

        hold_created = False
        hold_row = None
        if slug in HISTORICAL:
            hold_row = _hold_row(bind, operation, slug)
            hold_created = hold_row is None
            if hold_created:
                if prior is not None:
                    raise RuntimeError(f"0138 owned historical hold {slug} disappeared")
                bind.execute(
                    sa.insert(operation).values(
                        id=uuid4(),
                        slug=slug,
                        operation_id=HISTORICAL_ID,
                        category="historical",
                        provider="unattributed",
                        model="unattributed",
                        max_usd=LIMIT,
                        actual_usd=None,
                        status="uncertain",
                        attempts=1,
                        receipt_ref=None,
                        release_reason=None,
                        created_at=sa.func.now(),
                        updated_at=sa.func.now(),
                    )
                )
                hold_row = _hold_row(bind, operation, slug)
            _verify_hold(hold_row, slug)
            assert hold_row is not None

        if prior is None:
            bind.execute(
                sa.insert(ownership).values(
                    slug=slug,
                    account_created=account_created,
                    account_created_at=account_row["created_at"],
                    hold_created=hold_created,
                    hold_id=hold_row["id"] if hold_row is not None else None,
                )
            )
        elif (
            prior["account_created_at"] != account_row["created_at"]
            or (slug in HISTORICAL and (hold_row is None or prior["hold_id"] != hold_row["id"]))
            or (slug in NEW_PILOTS and prior["hold_id"] is not None)
            or bool(prior["hold_created"])
            and slug in NEW_PILOTS
        ):
            raise RuntimeError(f"0138 ownership for {slug} no longer matches the ledger")


def downgrade() -> None:
    _online()
    bind = op.get_bind()
    _lock_budget_tables(bind)
    if not sa.inspect(bind).has_table(OWNERSHIP):
        raise RuntimeError("0138 ownership record is missing; refusing destructive downgrade")
    account, operation, ownership = _account(), _operation(), _ownership()
    owners = {row["slug"]: row for row in bind.execute(sa.select(ownership)).mappings()}
    if set(owners) != set(PILOTS):
        raise RuntimeError("0138 ownership inventory is incomplete or conflicts")

    # Complete preflight before the first DELETE. A reconciled historical charge or a
    # later operation must survive, so it makes this downgrade unsafe.
    for slug in PILOTS:
        owner = owners[slug]
        account_row = _account_row(bind, account, slug)
        _verify_account(account_row, slug)
        assert account_row is not None
        if owner["account_created_at"] != account_row["created_at"]:
            raise RuntimeError(f"0138 account {slug} was replaced")
        hold_row = _hold_row(bind, operation, slug) if slug in HISTORICAL else None
        if slug in HISTORICAL:
            _verify_hold(hold_row, slug)
            assert hold_row is not None
            if owner["hold_id"] != hold_row["id"]:
                raise RuntimeError(f"0138 historical hold {slug} was replaced")
            if owner["hold_created"] and hold_row["status"] != "uncertain":
                raise RuntimeError(f"0138 historical hold {slug} was reconciled; preserve it")
        elif owner["hold_created"] or owner["hold_id"] is not None:
            raise RuntimeError(f"0138 ownership for {slug} conflicts")
        # A hold on a pre-existing account is just as important as a newly
        # created account: removing it while another operation remains would
        # erase the reserve for unreconciled historical exposure.
        if owner["account_created"] or owner["hold_created"]:
            rows = (
                bind.execute(sa.select(operation.c.id).where(operation.c.slug == slug))
                .scalars()
                .all()
            )
            removable = (
                {hold_row["id"]} if hold_row is not None and owner["hold_created"] else set()
            )
            if set(rows) != removable:
                raise RuntimeError(f"0138 account {slug} has later operations; preserve it")

    for slug in HISTORICAL:
        owner = owners[slug]
        if owner["hold_created"]:
            result = bind.execute(
                sa.delete(operation).where(
                    operation.c.slug == slug,
                    operation.c.id == owner["hold_id"],
                )
            )
            if result.rowcount != 1:
                raise RuntimeError(f"0138 historical hold {slug} changed during downgrade")
    for slug in PILOTS:
        if owners[slug]["account_created"]:
            result = bind.execute(sa.delete(account).where(account.c.slug == slug))
            if result.rowcount != 1:
                raise RuntimeError(f"0138 account {slug} changed during downgrade")
    op.drop_table(OWNERSHIP)
