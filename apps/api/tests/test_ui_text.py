"""Administrator overrides of the web UI copy: validation, caching, audit and routes.

The table itself is stood in for by ``FakeSession`` plus the four ``_``-prefixed lookup
functions in the service, so these tests exercise everything around the database —
the placeholder rules, the Redis cache and its invalidation, the audit rows and the
snapshot — without PostgreSQL. ``test_ui_text_integration.py`` drives the real table.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict, cast
from uuid import uuid4

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError as PydanticValidationError
from redis.exceptions import RedisError

import app.admin.service as admin_service
import app.ui_text.router as ui_text_router
import app.ui_text.service as ui_text_service
from app.auth.service import current_user
from app.db import get_session
from app.i18n import ERROR_DETAILS
from app.main import app
from app.models import AdminAuditLog, UiTextOverride, User
from app.problems import AppError
from app.ui_text.icu import parse_icu
from app.ui_text.schemas import (
    UI_TEXT_LOCKED_NAMESPACES,
    UI_TEXT_NAMESPACES,
    PublicUiText,
    UiTextBatchWrite,
    UiTextSnapshot,
    UiTextWrite,
)
from app.ui_text.service import (
    CACHE_KEY,
    batch_ui_text,
    braces_balanced,
    content_version,
    icu_parameters,
    invalidate_ui_text_cache,
    normalize_value,
    public_ui_text,
    require_namespace,
    reset_ui_text,
    ui_text_snapshot,
    upsert_ui_text,
)

ERROR_CODES = (
    "ui_text_namespace_unknown",
    "ui_text_namespace_locked",
    "ui_text_value_empty",
    "ui_text_value_control_chars",
    "ui_text_braces_unbalanced",
    "ui_text_parameters_mismatch",
    "ui_text_override_not_found",
    "ui_text_batch_duplicate_key",
    "ui_text_default_required",
)


class FakeSession:
    """The rows of ``ui_text_overrides`` for one test, plus what the service added."""

    def __init__(self, rows: list[UiTextOverride] | None = None) -> None:
        self.rows: list[UiTextOverride] = []
        for row in rows or []:
            self.add(row)
        self.audit: list[AdminAuditLog] = []
        self.commits = 0
        self.public_queries = 0

    def add(self, value: object) -> None:
        now = datetime.now(UTC)
        if isinstance(value, UiTextOverride):
            # The ORM stamps these at flush time; the fake does it on add.
            value.id = value.id or uuid4()
            value.created_at = value.created_at or now
            value.updated_at = now
            if value not in self.rows:
                self.rows.append(value)
        elif isinstance(value, AdminAuditLog):
            value.id = value.id or uuid4()
            value.created_at = now
            self.audit.append(value)

    async def delete(self, value: object) -> None:
        assert isinstance(value, UiTextOverride)
        self.rows.remove(value)

    async def commit(self) -> None:
        self.commits += 1


def override(namespace: str, key: str, locale: str, value: str) -> UiTextOverride:
    return UiTextOverride(
        namespace=namespace, key=key, locale=locale, value=value, default_snapshot=value
    )


@pytest.fixture
def fake_table(monkeypatch: pytest.MonkeyPatch) -> None:
    async def find(session: Any, locale: str, namespace: str, key: str) -> UiTextOverride | None:
        return next(
            (
                row
                for row in session.rows
                if row.locale == locale and row.namespace == namespace and row.key == key
            ),
            None,
        )

    async def listed(session: Any, locale: str) -> list[tuple[UiTextOverride, str | None]]:
        rows = sorted(
            (row for row in session.rows if row.locale == locale),
            key=lambda row: (row.namespace, row.key),
        )
        return [(row, "admin@example.com") for row in rows]

    async def public_rows(session: Any, locale: str) -> list[tuple[str, str, str]]:
        session.public_queries += 1
        return [(row.namespace, row.key, row.value) for row in session.rows if row.locale == locale]

    async def recent_audit(session: Any) -> list[AdminAuditLog]:
        return list(reversed(session.audit))[:20]

    monkeypatch.setattr(ui_text_service, "_find_override", find)
    monkeypatch.setattr(ui_text_service, "_list_overrides", listed)
    monkeypatch.setattr(ui_text_service, "_public_rows", public_rows)
    monkeypatch.setattr(ui_text_service, "_recent_audit", recent_audit)


@pytest.fixture
def actor() -> User:
    return User(id=uuid4(), email="admin@example.com", password_hash="x", is_admin=True)


@pytest.fixture
def session_override() -> Iterator[None]:
    async def provide_session() -> AsyncIterator[object]:
        yield object()

    app.dependency_overrides[get_session] = provide_session
    yield
    app.dependency_overrides.clear()


def error_code(exc_info: pytest.ExceptionInfo[AppError]) -> str:
    return exc_info.value.code


# --- pure rules -------------------------------------------------------------------------


class IcuCase(TypedDict):
    id: str
    default: str
    override: str
    problem: str | None


ICU_CASES = cast(
    list[IcuCase],
    json.loads(
        (Path(__file__).resolve().parents[3] / "docs/ui-text-icu-cases.json").read_text(
            encoding="utf-8"
        )
    ),
)


@pytest.mark.parametrize("case", ICU_CASES, ids=lambda case: case["id"])
def test_override_icu_contract_matches_shared_formatjs_cases(case: IcuCase) -> None:
    if case["problem"] is None:
        assert (
            normalize_value(case["override"], case["default"], key=case["id"]) == case["override"]
        )
        return
    with pytest.raises(AppError) as error:
        normalize_value(case["override"], case["default"], key=case["id"])
    assert (
        error.value.code
        == {
            "braces": "ui_text_braces_unbalanced",
            "parameters": "ui_text_parameters_mismatch",
        }[case["problem"]]
    )
    assert case["id"] in error.value.detail


def test_branch_usage_cannot_hide_behind_same_global_runtime_and_literal_names() -> None:
    default = "Help: '{name}'. {mode, select, short {{name}} other {{name}}}"
    changed = "Help: '{name}'. {mode, select, short {'{name}'} other {{name}}}"
    assert parse_icu(default).literal_parameters == parse_icu(changed).literal_parameters
    with pytest.raises(AppError) as error:
        normalize_value(changed, default, key="branch-local-name")
    assert error.value.code == "ui_text_parameters_mismatch"


def test_nested_select_keeps_bounded_structured_signatures() -> None:
    default = "Hello {name}"
    changed = "Welcome {name}"
    hidden = "Welcome '{name}'"
    for _ in range(30):
        default = "{mode, select, other {" + default + "}}"
        changed = "{mode, select, other {" + changed + "}}"
        hidden = "{mode, select, other {" + hidden + "}}"
    assert normalize_value(changed, default, key="nested") == changed
    with pytest.raises(AppError) as error:
        normalize_value(hidden, default, key="nested")
    assert error.value.code == "ui_text_parameters_mismatch"


@pytest.mark.parametrize(
    "style",
    ["::#", "::+", "::r", "::.00/+", "::/foo", "::unit", "::integer-width/00", "::E"],
)
def test_rejects_formatjs_skeleton_parser_errors(style: str) -> None:
    with pytest.raises(AppError) as error:
        normalize_value("{value, number, " + style + "}", "{value, number}", key="format")
    assert error.value.code == "ui_text_braces_unbalanced"
    assert "第 " in error.value.detail


def test_named_style_closing_brace_matches_formatjs_argument_boundary() -> None:
    # FormatJS consumes foo{x as the style, leaving {y} as an actual argument.
    default = "{value, number, foo{x} {y}}"
    assert normalize_value("{value, number} {y}", default, key="style")
    with pytest.raises(AppError) as error:
        normalize_value("{value, number, foo{x} text}", default, key="style")
    assert error.value.code == "ui_text_parameters_mismatch"


def test_current_catalog_defaults_are_valid_icu() -> None:
    def messages(value: object) -> Iterator[str]:
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for child in value.values():
                yield from messages(child)

    catalog_root = Path(__file__).resolve().parents[3] / "apps/web/messages"
    catalogs = list(catalog_root.glob("*/*.json"))
    assert catalogs
    for catalog in catalogs:
        for message in messages(json.loads(catalog.read_text(encoding="utf-8"))):
            parse_icu(message)


def test_icu_parameters_extract_what_the_catalog_checker_extracts() -> None:
    assert icu_parameters("{count, plural, one {# day} other {# days}}") == {"count"}
    assert icu_parameters("Hello {name}, {name}!") == {"name"}
    assert icu_parameters("{名字} and {# thing}") == set()
    assert icu_parameters("'{destination}' is quoted") == {"destination"}
    assert icu_parameters("no placeholders") == set()


def test_braces_must_open_before_they_close_and_end_balanced() -> None:
    assert braces_balanced("{count, plural, one {# day} other {# days}}")
    assert braces_balanced("plain")
    assert not braces_balanced("{count, plural, one {# day}")
    assert not braces_balanced("}{")


def test_normalize_value_keeps_meaningful_whitespace_and_line_feeds() -> None:
    assert normalize_value(", ", ", ", key="sep") == ", "
    assert normalize_value(" · Return {times}", " · Return {times}", key="k") == " · Return {times}"
    assert normalize_value("a\r\nb\rc", "abc", key="k") == "a\nb\nc"
    assert normalize_value("{count} of {count}", "{count}", key="k") == "{count} of {count}"


@pytest.mark.parametrize(
    ("value", "default", "code"),
    [
        ("   ", "Home", "ui_text_value_empty"),
        ("", "Home", "ui_text_value_empty"),
        ("bad\x00byte", "Home", "ui_text_value_control_chars"),
        ("line\u2028separator", "Home", "ui_text_value_control_chars"),
        ("{count, plural, one {# day}", "{count}", "ui_text_braces_unbalanced"),
        ("Hi", None, "ui_text_default_required"),
        ("Hi there", "Hi {name}", "ui_text_parameters_mismatch"),
        ("Hi {name} {extra}", "Hi {name}", "ui_text_parameters_mismatch"),
    ],
)
def test_normalize_value_rejects_what_would_break_the_page(
    value: str, default: str | None, code: str
) -> None:
    with pytest.raises(AppError) as exc_info:
        normalize_value(value, default, key="navigation.home")
    assert error_code(exc_info) == code
    assert "navigation.home" in exc_info.value.detail


def test_parameter_mismatch_names_both_directions() -> None:
    with pytest.raises(AppError) as exc_info:
        normalize_value("Hi {who}", "Hi {name}", key="k")
    assert "name" in exc_info.value.detail
    assert "who" in exc_info.value.detail


def test_parameter_mismatch_explains_roles_branches_and_offsets() -> None:
    with pytest.raises(AppError) as error:
        normalize_value(
            "{count, plural, offset:2 one {'{name}'} other {#}}",
            "{count, plural, offset:1 one {{name} #} other {#}}",
            key="guests",
        )
    detail = error.value.detail
    for expected in ("guests", "count", "plural", "offset:1", "offset:2", "one:", "other:"):
        assert expected in detail
    assert "{name} (argument)" in detail
    assert "#" in detail
    assert "勿用單引號包住參數" in detail
    assert "frozenset" not in detail
    assert "(6," not in detail


def test_namespace_allowlist_excludes_legacy_and_unknown_groups() -> None:
    assert len(UI_TEXT_NAMESPACES) == 24
    require_namespace("travelServices")
    require_namespace("community")
    assert "legacy" not in UI_TEXT_NAMESPACES
    assert UI_TEXT_LOCKED_NAMESPACES == ("legacy",)
    require_namespace("navigation")
    require_namespace("catalogReview")
    with pytest.raises(AppError) as locked:
        require_namespace("legacy")
    assert error_code(locked) == "ui_text_namespace_locked"
    with pytest.raises(AppError) as unknown:
        require_namespace("nope")
    assert error_code(unknown) == "ui_text_namespace_unknown"


def test_every_error_code_has_a_sentence_in_the_translated_locales() -> None:
    for locale in ("en", "ja", "ko", "zh-CN"):
        for code in ERROR_CODES:
            assert ERROR_DETAILS[locale][code].strip(), f"{locale}/{code}"


def test_content_version_changes_on_add_update_and_delete() -> None:
    empty = content_version({})
    one = content_version({"navigation.home": "Start"})
    changed = content_version({"navigation.home": "Begin"})
    assert len(empty) == 16
    assert len({empty, one, changed}) == 3
    assert content_version({"b": "2", "a": "1"}) == content_version({"a": "1", "b": "2"})


def test_audit_actions_show_up_in_the_settings_activity_list() -> None:
    source = Path(admin_service.__file__).read_text(encoding="utf-8")
    assert '"ui_text_updated"' in source
    assert '"ui_text_reset"' in source


# --- public read and cache ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_public_ui_text_is_anonymous_and_not_cached_by_http(
    monkeypatch: pytest.MonkeyPatch, session_override: None
) -> None:
    async def payload(_session: object, _redis: object, locale: str) -> PublicUiText:
        return PublicUiText(locale=locale, version="abc", entries={"navigation.home": "Start"})

    monkeypatch.setattr(ui_text_router, "public_ui_text", payload)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/runtime/ui-text", params={"locale": "ja"})
        invalid = await client.get("/api/v1/runtime/ui-text", params={"locale": "xx"})

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == {
        "locale": "ja",
        "version": "abc",
        "entries": {"navigation.home": "Start"},
    }
    assert invalid.status_code == 422


@pytest.mark.asyncio
async def test_public_ui_text_is_served_from_redis_until_invalidated(fake_table: None) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    session = FakeSession([override("navigation", "home", "ja", "スタート")])

    first = await public_ui_text(session, redis, "ja")  # type: ignore[arg-type]
    second = await public_ui_text(session, redis, "ja")  # type: ignore[arg-type]

    assert first.entries == {"navigation.home": "スタート"}
    assert first == second
    assert session.public_queries == 1
    assert await redis.ttl(CACHE_KEY.format(locale="ja")) > 0

    session.rows.append(override("navigation", "trips", "ja", "旅程"))
    stale = await public_ui_text(session, redis, "ja")  # type: ignore[arg-type]
    assert stale.entries == first.entries

    await invalidate_ui_text_cache(redis)
    fresh = await public_ui_text(session, redis, "ja")  # type: ignore[arg-type]
    assert fresh.entries == {"navigation.home": "スタート", "navigation.trips": "旅程"}
    assert fresh.version != first.version
    assert session.public_queries == 2


@pytest.mark.asyncio
async def test_public_ui_text_survives_a_redis_outage(fake_table: None) -> None:
    class BrokenRedis:
        async def get(self, _key: str) -> str:
            raise RedisError("down")

        async def set(self, *_args: object, **_kwargs: object) -> None:
            raise RedisError("down")

        async def delete(self, *_keys: str) -> None:
            raise RedisError("down")

    session = FakeSession([override("common", "save", "en", "Save")])
    payload = await public_ui_text(session, BrokenRedis(), "en")  # type: ignore[arg-type]
    assert payload.entries == {"common.save": "Save"}
    await invalidate_ui_text_cache(BrokenRedis())  # type: ignore[arg-type]


# --- writes ------------------------------------------------------------------------------


async def warm_cache(redis: fakeredis.aioredis.FakeRedis) -> None:
    for locale in ("en", "ja", "ko", "zh-TW", "zh-CN"):
        await redis.set(CACHE_KEY.format(locale=locale), "{}")


@pytest.mark.asyncio
async def test_upsert_stores_the_override_audits_it_and_clears_every_locale(
    fake_table: None, actor: User
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await warm_cache(redis)
    session = FakeSession()

    snapshot = await upsert_ui_text(
        session,  # type: ignore[arg-type]
        redis,
        actor,
        "ja",
        "navigation",
        "home",
        UiTextWrite(value="スタート", default_value="Home"),
    )

    assert session.commits == 1
    row = session.rows[0]
    assert (row.namespace, row.key, row.locale) == ("navigation", "home", "ja")
    assert row.value == "スタート"
    assert row.default_snapshot == "Home"
    assert row.updated_by_user_id == actor.id
    for locale in ("en", "ja"):
        assert await redis.exists(CACHE_KEY.format(locale=locale)) == 0

    audit = session.audit[0]
    assert audit.action == "ui_text_updated"
    assert audit.target == "ui-text:ja:navigation"
    assert audit.metadata_json == {
        "changes": [{"key": "home", "before": None, "after": "スタート"}],
        "count": 1,
    }

    assert snapshot.locale == "ja"
    assert snapshot.namespace == "navigation"
    assert snapshot.namespace_counts == {"navigation": 1}
    assert snapshot.locked_namespaces == ["legacy"]
    assert [entry.key for entry in snapshot.entries] == ["home"]
    assert snapshot.entries[0].updated_by_email == "admin@example.com"
    assert snapshot.audit[0].action == "ui_text_updated"

    again = await upsert_ui_text(
        session,  # type: ignore[arg-type]
        redis,
        actor,
        "ja",
        "navigation",
        "home",
        UiTextWrite(value="ホーム", default_value="Home"),
    )
    assert len(session.rows) == 1
    assert session.rows[0].value == "ホーム"
    assert again.version != snapshot.version
    assert session.audit[1].metadata_json["changes"] == [
        {"key": "home", "before": "スタート", "after": "ホーム"}
    ]


@pytest.mark.asyncio
async def test_upsert_rejects_bad_input_before_touching_rows(fake_table: None, actor: User) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    session = FakeSession()
    for namespace, payload, code in [
        ("legacy", UiTextWrite(value="x", default_value="x"), "ui_text_namespace_locked"),
        ("nope", UiTextWrite(value="x", default_value="x"), "ui_text_namespace_unknown"),
        (
            "usage",
            UiTextWrite(value="消耗", default_value="消耗 {uses} 次"),
            "ui_text_parameters_mismatch",
        ),
    ]:
        with pytest.raises(AppError) as exc_info:
            await upsert_ui_text(session, redis, actor, "zh-TW", namespace, "charge", payload)  # type: ignore[arg-type]
        assert error_code(exc_info) == code
    assert session.rows == []
    assert session.commits == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("batch", [False, True], ids=["single-write", "batch-write"])
async def test_quoted_parameter_rejection_preserves_rows_audit_and_cache(
    fake_table: None, actor: User, batch: bool
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    session = FakeSession([override("common", "greeting", "en", "Hello {name}")])
    before = await public_ui_text(session, redis, "en")  # type: ignore[arg-type]
    cached_before = await redis.get(CACHE_KEY.format(locale="en"))
    with pytest.raises(AppError) as error:
        if batch:
            await batch_ui_text(
                session,  # type: ignore[arg-type]
                redis,
                actor,
                UiTextBatchWrite(
                    locale="en",
                    namespace="common",
                    entries=[
                        {"key": "greeting", "value": "Hi {name}", "default_value": "Hi {name}"},
                        {"key": "later", "value": "Hi '{name}'", "default_value": "Hi {name}"},
                    ],
                ),
            )
        else:
            await upsert_ui_text(
                session,  # type: ignore[arg-type]
                redis,
                actor,
                "en",
                "common",
                "greeting",
                UiTextWrite(value="Hi '{name}'", default_value="Hi {name}"),
            )
    assert error.value.code == "ui_text_parameters_mismatch"
    assert [(row.key, row.value) for row in session.rows] == [("greeting", "Hello {name}")]
    assert session.rows[0].default_snapshot == "Hello {name}"
    assert session.commits == 0
    assert session.audit == []
    assert await redis.get(CACHE_KEY.format(locale="en")) == cached_before
    assert await public_ui_text(session, redis, "en") == before  # type: ignore[arg-type]
    assert session.public_queries == 1


@pytest.mark.asyncio
async def test_reset_removes_the_override_and_reports_a_missing_one(
    fake_table: None, actor: User
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await warm_cache(redis)
    session = FakeSession([override("common", "save", "en", "Store")])

    snapshot = await reset_ui_text(session, redis, actor, "en", "common", "save")  # type: ignore[arg-type]

    assert session.rows == []
    assert snapshot.entries == []
    assert snapshot.namespace_counts == {}
    assert session.audit[0].action == "ui_text_reset"
    assert session.audit[0].metadata_json == {"key": "save", "before": "Store"}
    assert await redis.exists(CACHE_KEY.format(locale="en")) == 0

    with pytest.raises(AppError) as exc_info:
        await reset_ui_text(session, redis, actor, "en", "common", "save")  # type: ignore[arg-type]
    assert exc_info.value.status == 404
    assert error_code(exc_info) == "ui_text_override_not_found"


@pytest.mark.asyncio
async def test_batch_updates_creates_and_restores_in_one_commit(
    fake_table: None, actor: User
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await warm_cache(redis)
    session = FakeSession(
        [
            override("common", "save", "en", "Store"),
            override("common", "cancel", "en", "Abort"),
            override("common", "keep", "en", "Keep"),
        ]
    )
    payload = UiTextBatchWrite(
        locale="en",
        namespace="common",
        entries=[
            {"key": "save", "value": "Save now", "default_value": "Save"},
            {"key": "cancel", "value": None},
            {"key": "greeting", "value": "Hi {name}", "default_value": "Hello {name}"},
            {"key": "keep", "value": "Keep", "default_value": "Keep"},
            {"key": "absent", "value": None},
        ],
    )

    snapshot = await batch_ui_text(session, redis, actor, payload)  # type: ignore[arg-type]

    assert session.commits == 1
    assert {(row.key, row.value) for row in session.rows} == {
        ("save", "Save now"),
        ("greeting", "Hi {name}"),
        ("keep", "Keep"),
    }
    assert [entry.key for entry in snapshot.entries] == ["greeting", "keep", "save"]
    assert len(session.audit) == 1
    assert session.audit[0].metadata_json == {
        "changes": [
            {"key": "save", "before": "Store", "after": "Save now"},
            {"key": "cancel", "before": "Abort", "after": None},
            {"key": "greeting", "before": None, "after": "Hi {name}"},
        ],
        "count": 3,
    }
    assert await redis.exists(CACHE_KEY.format(locale="zh-CN")) == 0


@pytest.mark.asyncio
async def test_batch_is_all_or_nothing(fake_table: None, actor: User) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    session = FakeSession([override("common", "save", "en", "Store")])

    duplicate = UiTextBatchWrite(
        locale="en",
        namespace="common",
        entries=[
            {"key": "save", "value": "One", "default_value": "Save"},
            {"key": "save", "value": "Two", "default_value": "Save"},
        ],
    )
    with pytest.raises(AppError) as dup:
        await batch_ui_text(session, redis, actor, duplicate)  # type: ignore[arg-type]
    assert error_code(dup) == "ui_text_batch_duplicate_key"

    missing_default = UiTextBatchWrite(
        locale="en",
        namespace="common",
        entries=[
            {"key": "save", "value": "Fine", "default_value": "Save"},
            {"key": "later", "value": "No default"},
        ],
    )
    with pytest.raises(AppError) as required:
        await batch_ui_text(session, redis, actor, missing_default)  # type: ignore[arg-type]
    assert error_code(required) == "ui_text_default_required"

    assert session.rows[0].value == "Store"
    assert session.commits == 0

    with pytest.raises(PydanticValidationError):
        UiTextBatchWrite(
            locale="en",
            namespace="common",
            entries=[
                {"key": f"k{index}", "value": "x", "default_value": "x"} for index in range(101)
            ],
        )
    with pytest.raises(PydanticValidationError):
        UiTextBatchWrite(
            locale="en", namespace="common", entries=[{"key": "bad key!", "value": "x"}]
        )


# --- routes ------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admin_routes_require_an_administrator(session_override: None) -> None:
    member = User(id=uuid4(), email="member@example.com", password_hash="x", is_admin=False)
    app.dependency_overrides[current_user] = lambda: member
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            listed = await client.get("/api/v1/admin/ui-text", params={"locale": "en"})
            written = await client.put(
                "/api/v1/admin/ui-text/en/common/save",
                json={"value": "Store", "default_value": "Save"},
            )
    finally:
        app.dependency_overrides.clear()
    assert listed.status_code == 403
    assert written.status_code == 403
    assert listed.json()["code"] == "admin_required"


@pytest.mark.asyncio
async def test_admin_routes_validate_paths_before_reaching_the_service(
    monkeypatch: pytest.MonkeyPatch, session_override: None, actor: User
) -> None:
    calls: list[tuple[str, str, str]] = []

    async def upsert(
        _session: object,
        _redis: object,
        _actor: object,
        locale: str,
        namespace: str,
        key: str,
        _payload: object,
    ) -> UiTextSnapshot:
        calls.append((locale, namespace, key))
        return UiTextSnapshot(
            locale=locale,
            namespace=namespace,
            version="v",
            namespaces=list(UI_TEXT_NAMESPACES),
            locked_namespaces=["legacy"],
            namespace_counts={},
            entries=[],
            audit=[],
        )

    monkeypatch.setattr(ui_text_router, "upsert_ui_text", upsert)
    app.dependency_overrides[current_user] = lambda: actor
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            ok = await client.put(
                "/api/v1/admin/ui-text/zh-TW/search/catalog.cities.osaka-kyoto",
                json={"value": "大阪・京都", "default_value": "Osaka / Kyoto"},
            )
            bad_locale = await client.put(
                "/api/v1/admin/ui-text/xx/search/home",
                json={"value": "x", "default_value": "x"},
            )
            bad_key = await client.put(
                "/api/v1/admin/ui-text/en/search/has space",
                json={"value": "x", "default_value": "x"},
            )
    finally:
        app.dependency_overrides.clear()
    assert ok.status_code == 200
    assert calls == [("zh-TW", "search", "catalog.cities.osaka-kyoto")]
    assert bad_locale.status_code == 422
    assert bad_key.status_code == 422


@pytest.mark.asyncio
async def test_snapshot_filters_by_namespace_but_counts_every_namespace(fake_table: None) -> None:
    session = FakeSession(
        [
            override("common", "save", "en", "Store"),
            override("navigation", "home", "en", "Start"),
            override("navigation", "trips", "en", "Journeys"),
            override("navigation", "home", "ja", "スタート"),
        ]
    )
    everything = await ui_text_snapshot(session, "en", None)  # type: ignore[arg-type]
    navigation = await ui_text_snapshot(session, "en", "navigation")  # type: ignore[arg-type]

    assert [entry.key for entry in everything.entries] == ["save", "home", "trips"]
    assert everything.namespace_counts == {"common": 1, "navigation": 2}
    assert [entry.key for entry in navigation.entries] == ["home", "trips"]
    assert navigation.namespace_counts == everything.namespace_counts
    assert navigation.version == everything.version
    assert navigation.namespaces == list(UI_TEXT_NAMESPACES)

    with pytest.raises(AppError) as exc_info:
        await ui_text_snapshot(session, "en", "legacy")  # type: ignore[arg-type]
    assert error_code(exc_info) == "ui_text_namespace_locked"
