"""The 0132 image must start on exactly the reviewed 0133 rollback schema."""

from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from app import migration_guard as guard
from app.video_budget.models import PILOT_LIMITS_USD


def test_revision_classification_never_accepts_an_unknown_or_multiple_database_head() -> None:
    known = {"0131_prior", guard.ROLLBACK_IMAGE_HEAD}
    exact = guard.classify_revisions((guard.ROLLBACK_IMAGE_HEAD,), guard.ROLLBACK_IMAGE_HEAD, known)
    assert exact.state == "exact"
    prior = guard.classify_revisions(("0131_prior",), guard.ROLLBACK_IMAGE_HEAD, known)
    assert prior.state == "upgrade"
    assert guard.classify_revisions((), guard.ROLLBACK_IMAGE_HEAD, known).state == "upgrade"
    rollback = guard.classify_revisions(
        (guard.REVIEWED_FUTURE_REVISION,), guard.ROLLBACK_IMAGE_HEAD, known
    )
    assert rollback.state == "rollback-compatible"
    with pytest.raises(guard.MigrationGuardError, match="unknown"):
        guard.classify_revisions(("0134_unknown",), guard.ROLLBACK_IMAGE_HEAD, known)
    with pytest.raises(guard.MigrationGuardError, match="multiple"):
        guard.classify_revisions(
            (guard.ROLLBACK_IMAGE_HEAD, "0134_unknown"), guard.ROLLBACK_IMAGE_HEAD, known
        )
    with pytest.raises(guard.MigrationGuardError, match="unknown"):
        guard.classify_revisions((guard.REVIEWED_FUTURE_REVISION,), "0131_prior", known)
    assert (
        guard.classify_revisions(
            (guard.REVIEWED_ADMISSION_REVISION,), guard.REVIEWED_FUTURE_REVISION, known
        ).state
        == "rollback-compatible"
    )
    with pytest.raises(guard.MigrationGuardError, match="unknown"):
        guard.classify_revisions(
            (guard.REVIEWED_ADMISSION_REVISION,), guard.ROLLBACK_IMAGE_HEAD, known
        )


class _Rows:
    def __init__(self, values: Sequence[object]) -> None:
        self.values = values

    def all(self) -> Sequence[object]:
        return self.values

    def scalars(self) -> "_Rows":
        return self


_ConstraintRow = tuple[str, str, str | bytes, bool, str | bytes, bool, str]
_CONSTRAINTS: list[_ConstraintRow] = [
    (
        "video_pilot_budgets",
        "video_pilot_budgets_pkey",
        "p",
        True,
        " ",
        False,
        "PRIMARY KEY (slug)",
    ),
    (
        "video_pilot_budgets",
        "ck_video_pilot_budget_limit",
        "c",
        True,
        " ",
        False,
        "CHECK ((limit_usd = ANY (ARRAY[5.000000, 25.000000])))",
    ),
    (
        "video_pilot_budget_operations",
        "video_pilot_budget_operations_pkey",
        "p",
        True,
        " ",
        False,
        "PRIMARY KEY (id)",
    ),
    (
        "video_pilot_budget_operations",
        "uq_video_pilot_budget_operation",
        "u",
        True,
        " ",
        False,
        "UNIQUE (slug, operation_id)",
    ),
    (
        "video_pilot_budget_operations",
        "video_pilot_budget_operations_slug_fkey",
        "f",
        True,
        "r",
        True,
        "FOREIGN KEY (slug) REFERENCES video_pilot_budgets(slug) ON DELETE RESTRICT",
    ),
    (
        "video_pilot_budget_operations",
        "ck_video_pilot_budget_operation_status",
        "c",
        True,
        " ",
        False,
        "CHECK (((status)::text = ANY ((ARRAY['reserved'::character varying, "
        "'uncertain'::character varying, 'settled'::character varying, "
        "'released'::character varying])::text[])))",
    ),
    (
        "video_pilot_budget_operations",
        "ck_video_pilot_budget_operation_max",
        "c",
        True,
        " ",
        False,
        "CHECK ((max_usd > (0)::numeric))",
    ),
    (
        "video_pilot_budget_operations",
        "ck_video_pilot_budget_operation_actual",
        "c",
        True,
        " ",
        False,
        "CHECK (((actual_usd IS NULL) OR (actual_usd >= (0)::numeric)))",
    ),
]


class _Connection:
    def __init__(
        self,
        accounts: dict[str, Decimal],
        constraints: Sequence[_ConstraintRow] | None = None,
        index: str = "CREATE INDEX ix_video_pilot_budget_operations_slug "
        "ON public.video_pilot_budget_operations USING btree (slug)",
        admission_column: Sequence[object] = ((True, True, True, True, True),),
        admission_tokens: Sequence[object] = ((None,),),
    ) -> None:
        self.results = [
            _Rows([(slug, limit, "created") for slug, limit in accounts.items()]),
            _Rows([]),
            _Rows(_CONSTRAINTS if constraints is None else constraints),
            _Rows([("ix_video_pilot_budget_operations_slug", index)]),
            _Rows(admission_column),
            _Rows(admission_tokens),
        ]

    async def execute(self, _statement: object) -> _Rows:
        return self.results.pop(0)


async def _verify_fake(connection: _Connection) -> None:
    await guard._verify_reviewed_0133(cast(AsyncConnection, connection))


async def _verify_0134_fake(connection: _Connection) -> None:
    await guard._verify_reviewed_0134(cast(AsyncConnection, connection))


@pytest.mark.asyncio
async def test_future_schema_readback_requires_nine_exact_accounts_and_schema() -> None:
    await _verify_fake(_Connection(dict(PILOT_LIMITS_USD)))
    asyncpg_rows = [
        (*row[:2], str(row[2]).encode("ascii"), row[3], str(row[4]).encode("ascii"), *row[5:])
        for row in _CONSTRAINTS
    ]
    await _verify_fake(_Connection(dict(PILOT_LIMITS_USD), asyncpg_rows))
    missing = dict(PILOT_LIMITS_USD)
    missing.pop("story-five-lego-legoland")
    with pytest.raises(guard.MigrationGuardError, match="accounts or limits"):
        await _verify_fake(_Connection(missing))
    wrong = dict(PILOT_LIMITS_USD)
    wrong["story-conveyor-belt-sushi-v2"] = Decimal(25)
    with pytest.raises(guard.MigrationGuardError, match="accounts or limits"):
        await _verify_fake(_Connection(wrong))
    extra = dict(PILOT_LIMITS_USD)
    extra["unreviewed-account"] = Decimal(5)
    with pytest.raises(guard.MigrationGuardError, match="accounts or limits"):
        await _verify_fake(_Connection(extra))
    no_check = [row for row in _CONSTRAINTS if row[1] != "ck_video_pilot_budget_limit"]
    with pytest.raises(guard.MigrationGuardError, match="constraint"):
        await _verify_fake(_Connection(dict(PILOT_LIMITS_USD), no_check))
    weakened = {
        "uq_video_pilot_budget_operation": "UNIQUE (id)",
        "ck_video_pilot_budget_operation_status": "CHECK (true)",
        "ck_video_pilot_budget_operation_max": "CHECK (max_usd >= 0)",
        "ck_video_pilot_budget_operation_actual": "CHECK (true)",
        "ck_video_pilot_budget_limit": "CHECK (limit_usd IN (5, 25, 1000))",
        "video_pilot_budget_operations_slug_fkey": (
            "FOREIGN KEY (operation_id) REFERENCES video_pilot_budgets(slug) ON DELETE RESTRICT"
        ),
    }
    for constraint_name, definition in weakened.items():
        mutated = [
            (*row[:6], definition) if row[1] == constraint_name else row for row in _CONSTRAINTS
        ]
        with pytest.raises(guard.MigrationGuardError, match="changed"):
            await _verify_fake(_Connection(dict(PILOT_LIMITS_USD), mutated))
    bad_fk = [(*row[:4], "a", False, row[6]) if row[2] == "f" else row for row in _CONSTRAINTS]
    with pytest.raises(guard.MigrationGuardError, match="foreign key"):
        await _verify_fake(_Connection(dict(PILOT_LIMITS_USD), bad_fk))
    with pytest.raises(guard.MigrationGuardError, match="index"):
        await _verify_fake(
            _Connection(dict(PILOT_LIMITS_USD), index="CREATE INDEX ... (operation_id)")
        )


@pytest.mark.asyncio
async def test_0134_rollback_requires_nullable_uuid_column_and_unheld_a01_token() -> None:
    await _verify_0134_fake(_Connection(dict(PILOT_LIMITS_USD)))
    for bad_column in (
        [],
        [(False, True, True, True, True)],
        [(True, False, True, True, True)],
        [(True, True, False, True, True)],
        [(True, True, True, False, True)],
        [(True, True, True, True, False)],
    ):
        with pytest.raises(guard.MigrationGuardError, match="column"):
            await _verify_0134_fake(
                _Connection(dict(PILOT_LIMITS_USD), admission_column=bad_column)
            )
    for bad_token in ([], [("held-token",)], [(None,), (None,)]):
        with pytest.raises(guard.MigrationGuardError, match="token"):
            await _verify_0134_fake(_Connection(dict(PILOT_LIMITS_USD), admission_tokens=bad_token))


def test_migrate_runs_alembic_for_known_revisions_but_skips_only_reviewed_rollback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(guard, "_alembic_config", lambda: "test-config")
    monkeypatch.setattr(
        "app.migration_guard.command.upgrade", lambda _config, revision: calls.append(revision)
    )

    async def rollback() -> guard.MigrationState:
        return guard.MigrationState(
            guard.REVIEWED_FUTURE_REVISION, guard.ROLLBACK_IMAGE_HEAD, "rollback-compatible"
        )

    monkeypatch.setattr(guard, "read_state", rollback)
    assert guard.main([]) == 0
    assert guard.main(["--status"]) == 0
    assert calls == []
    assert "state=rollback-compatible" in capsys.readouterr().out

    async def exact() -> guard.MigrationState:
        return guard.MigrationState(guard.ROLLBACK_IMAGE_HEAD, guard.ROLLBACK_IMAGE_HEAD, "exact")

    monkeypatch.setattr(guard, "read_state", exact)
    assert guard.main(["--status"]) == 0
    assert calls == [], "the verifier must remain read-only"
    assert guard.main([]) == 0
    assert calls == ["head"], "the normal path still delegates to Alembic"


def test_migrate_fails_closed_when_database_cannot_be_read_or_is_behind(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    async def unreadable() -> guard.MigrationState:
        raise OSError("private connection detail")

    monkeypatch.setattr(guard, "read_state", unreadable)
    assert guard.main([]) == 1
    assert guard.main(["--status"]) == 1
    assert "private connection detail" not in capsys.readouterr().err

    async def behind() -> guard.MigrationState:
        return guard.MigrationState("0131_prior", guard.ROLLBACK_IMAGE_HEAD, "upgrade")

    monkeypatch.setattr(guard, "read_state", behind)
    assert guard.main(["--status"]) == 1


def test_compose_and_host_verifier_use_the_same_guard_entry_point() -> None:
    root = Path(__file__).resolve().parents[3]
    compose = (root / "docker-compose.prod.yml").read_text(encoding="utf-8")
    verify = (root / ".agents/skills/deploy/scripts/host-verify.sh").read_text(encoding="utf-8")
    assert 'command: ["python", "-m", "app.migration_guard"]' in compose
    assert "python -m app.migration_guard --status" in verify
    assert "state=${schema_state:-missing}" in verify
