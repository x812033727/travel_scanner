"""The admin theme endpoints, driven directly with a fake session.

The rule these tests exist for is the one a reader cannot see from the endpoint
signature: replacing a hotspot's themes must leave a seeded link behind as a
tombstone rather than deleting it, or the next collect run brings back the theme
an administrator just removed.
"""

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from uuid import UUID, uuid4

import pytest

from app.hotspots.admin_router import (
    HotspotThemeAssignment,
    HotspotThemesPutPayload,
    ThemeUpdatePayload,
    ThemeWritePayload,
    assign_hotspot_themes,
    create_hotspot_theme,
    update_hotspot_theme,
)
from app.models import AdminAuditLog, HotspotTheme, HotspotThemeLink, TravelHotspot
from app.problems import AppError

NAMES = {"zh-TW": "賞櫻", "zh-CN": "赏樱", "en": "Cherry Blossoms", "ja": "桜", "ko": "벚꽃"}
USER = SimpleNamespace(id=uuid4())
STAMP = datetime(2026, 9, 7, tzinfo=UTC)


def theme(slug: str, kind: str = "season", months: list[int] | None = None) -> HotspotTheme:
    row = HotspotTheme(
        slug=slug,
        kind=kind,
        names_json=dict(NAMES),
        months_json=months if months is not None else ([3, 4] if kind == "season" else []),
        display_order=1,
        is_active=True,
        source="seed",
    )
    row.id = uuid4()
    return row


def link(hotspot_id: UUID, theme_id: UUID, source: str, is_active: bool = True) -> HotspotThemeLink:
    row = HotspotThemeLink(
        hotspot_id=hotspot_id,
        theme_id=theme_id,
        months_json=None,
        source=source,
        note=None,
        is_active=is_active,
    )
    row.id = uuid4()
    return row


class FakeSession:
    """Answers the handful of queries the theme endpoints make.

    ``scalar`` serves the theme lookup by slug, ``scalars`` the existing links, and
    ``execute`` the ordered link+theme rows.
    """

    def __init__(
        self,
        *,
        hotspot: TravelHotspot | None = None,
        themes: list[HotspotTheme] | None = None,
        links: list[HotspotThemeLink] | None = None,
    ) -> None:
        self.hotspot = hotspot
        self.themes = themes or []
        self.links = links or []
        self.added: list[Any] = []
        self.deleted: list[Any] = []
        self.commits = 0

    async def get(self, model: type, key: UUID) -> Any:
        if model is TravelHotspot:
            return self.hotspot if self.hotspot and self.hotspot.id == key else None
        return next((item for item in self.themes if item.id == key), None)

    async def scalar(self, statement: Any) -> Any:
        text = str(statement)
        if "hotspot_themes" in text:
            wanted = statement.compile().params
            slug = next((value for key, value in wanted.items() if key.startswith("slug")), None)
            return next(
                (item for item in self.themes if item.slug == slug and item.is_active), None
            )
        return None

    async def scalars(self, statement: Any) -> Any:
        return SimpleNamespace(all=lambda: list(self.links))

    async def execute(self, statement: Any) -> Any:
        rows = [
            (item, next(t for t in self.themes if t.id == item.theme_id)) for item in self.links
        ]
        return SimpleNamespace(all=lambda: rows)

    def add(self, item: Any) -> None:
        self.added.append(item)

    async def delete(self, item: Any) -> None:
        self.deleted.append(item)
        self.links = [row for row in self.links if row is not item]

    async def flush(self) -> None:
        # The database stamps Timestamped defaults on INSERT; the endpoint reads them
        # back straight after, and SessionFactory keeps them loaded (expire_on_commit
        # is False), so the fake has to do the same or it tests a state that cannot occur.
        for item in self.added:
            if getattr(item, "created_at", None) is None:
                item.created_at = STAMP
                item.updated_at = STAMP

    async def commit(self) -> None:
        self.commits += 1


def audit(session: FakeSession) -> AdminAuditLog:
    return next(item for item in session.added if isinstance(item, AdminAuditLog))


def new_links(session: FakeSession) -> list[HotspotThemeLink]:
    return [item for item in session.added if isinstance(item, HotspotThemeLink)]


def test_theme_payload_rejects_a_partial_name_map() -> None:
    with pytest.raises(ValueError, match="site locales"):
        ThemeWritePayload(slug="sakura", kind="season", names={"en": "Cherry"}, months=[3])


def test_theme_payload_rejects_months_on_a_shop_type() -> None:
    with pytest.raises(ValueError, match="does not carry months"):
        ThemeWritePayload(slug="drugstore", kind="shop", names=dict(NAMES), months=[3])


def test_theme_payload_requires_months_on_a_season() -> None:
    with pytest.raises(ValueError, match="needs at least one month"):
        ThemeWritePayload(slug="sakura", kind="season", names=dict(NAMES), months=[])


def test_theme_payload_rejects_an_impossible_month() -> None:
    with pytest.raises(ValueError, match="between 1 and 12"):
        ThemeWritePayload(slug="sakura", kind="season", names=dict(NAMES), months=[13])


def test_assignment_payload_rejects_a_repeated_theme() -> None:
    with pytest.raises(ValueError, match="only be listed once"):
        HotspotThemesPutPayload(
            themes=[HotspotThemeAssignment(slug="sakura"), HotspotThemeAssignment(slug="sakura")]
        )


@pytest.mark.asyncio
async def test_creating_a_theme_writes_an_audit_row() -> None:
    session = FakeSession(themes=[])
    payload = ThemeWritePayload(
        slug="hanabi", kind="season", names=dict(NAMES), months=[7, 8], display_order=4
    )

    result = await create_hotspot_theme(payload, USER, session)  # type: ignore[arg-type]

    assert result["slug"] == "hanabi"
    assert result["months"] == [7, 8]
    assert result["source"] == "admin"
    created = next(item for item in session.added if isinstance(item, HotspotTheme))
    assert created.source == "admin"
    assert audit(session).action == "hotspot_theme_created"
    assert session.commits == 1


@pytest.mark.asyncio
async def test_creating_a_theme_twice_is_a_conflict() -> None:
    session = FakeSession(themes=[theme("sakura")])
    payload = ThemeWritePayload(slug="sakura", kind="season", names=dict(NAMES), months=[3, 4])

    with pytest.raises(AppError) as refused:
        await create_hotspot_theme(payload, USER, session)  # type: ignore[arg-type]

    assert refused.value.status == 409
    assert refused.value.code == "hotspot_theme_slug_exists"
    assert session.commits == 0


@pytest.mark.asyncio
async def test_updating_a_shop_theme_with_months_is_refused() -> None:
    drugstore = theme("drugstore", kind="shop")
    session = FakeSession(themes=[drugstore])

    with pytest.raises(AppError) as refused:
        await update_hotspot_theme(
            drugstore.id,
            ThemeUpdatePayload(months=[3]),
            USER,
            session,  # type: ignore[arg-type]
        )

    assert refused.value.status == 422
    assert refused.value.code == "theme_months_not_applicable"
    assert session.commits == 0


@pytest.mark.asyncio
async def test_updating_a_missing_theme_is_not_found() -> None:
    session = FakeSession(themes=[])

    with pytest.raises(AppError) as missing:
        await update_hotspot_theme(
            uuid4(),
            ThemeUpdatePayload(is_active=False),
            USER,
            session,  # type: ignore[arg-type]
        )

    assert missing.value.status == 404
    assert missing.value.code == "hotspot_theme_not_found"


@pytest.mark.asyncio
async def test_assigning_an_unknown_theme_is_refused_before_anything_is_written() -> None:
    hotspot = TravelHotspot(slug="sensoji", category="culture")
    hotspot.id = uuid4()
    session = FakeSession(hotspot=hotspot, themes=[theme("sakura")])

    with pytest.raises(AppError) as refused:
        await assign_hotspot_themes(
            hotspot.id,
            HotspotThemesPutPayload(themes=[HotspotThemeAssignment(slug="bogus")]),
            USER,  # type: ignore[arg-type]
            session,  # type: ignore[arg-type]
            "zh-TW",
        )

    assert refused.value.status == 422
    assert refused.value.code == "unsupported_theme"
    assert session.added == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_assigning_replaces_seed_links_with_tombstones_and_deletes_the_rest() -> None:
    """A seeded link the administrator drops must stay as a tombstone; an ai link
    is simply deleted, because nothing re-creates it."""
    hotspot = TravelHotspot(slug="sensoji", category="culture")
    hotspot.id = uuid4()
    sakura, maple, lights = theme("sakura"), theme("autumn-leaves"), theme("illumination")
    seeded = link(hotspot.id, sakura.id, "seed")
    guessed = link(hotspot.id, maple.id, "ai")
    session = FakeSession(hotspot=hotspot, themes=[sakura, maple, lights], links=[seeded, guessed])

    result = await assign_hotspot_themes(
        hotspot.id,
        HotspotThemesPutPayload(
            themes=[HotspotThemeAssignment(slug="illumination", months=[12], note="丸之內")],
            reason="季節校正",
        ),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
        "zh-TW",
    )

    # The seed link survives, deactivated and re-owned so the sync leaves it alone.
    assert (seeded.is_active, seeded.source) == (False, "admin")
    assert guessed in session.deleted
    added = new_links(session)
    assert len(added) == 1
    assert added[0].theme_id == lights.id
    assert added[0].months_json == [12]
    assert added[0].note == "丸之內"
    assert added[0].source == "admin"
    assert (result["tombstoned"], result["removed"]) == (1, 1)
    entry = audit(session)
    assert entry.action == "hotspot_themes_assigned"
    assert entry.metadata_json["slugs"] == ["illumination"]
    assert entry.metadata_json["reason"] == "季節校正"
    assert session.commits == 1


@pytest.mark.asyncio
async def test_reassigning_an_existing_link_takes_it_over_rather_than_duplicating() -> None:
    hotspot = TravelHotspot(slug="sensoji", category="culture")
    hotspot.id = uuid4()
    sakura = theme("sakura")
    seeded = link(hotspot.id, sakura.id, "seed")
    session = FakeSession(hotspot=hotspot, themes=[sakura], links=[seeded])

    await assign_hotspot_themes(
        hotspot.id,
        HotspotThemesPutPayload(themes=[HotspotThemeAssignment(slug="sakura", months=[5])]),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
        "zh-TW",
    )

    assert new_links(session) == []
    assert seeded.months_json == [5]
    assert seeded.source == "admin"
    assert seeded.is_active is True
    assert session.deleted == []


@pytest.mark.asyncio
async def test_clearing_every_theme_keeps_the_seed_tombstone() -> None:
    hotspot = TravelHotspot(slug="sensoji", category="culture")
    hotspot.id = uuid4()
    sakura = theme("sakura")
    seeded = link(hotspot.id, sakura.id, "seed")
    session = FakeSession(hotspot=hotspot, themes=[sakura], links=[seeded])

    result = await assign_hotspot_themes(
        hotspot.id,
        HotspotThemesPutPayload(themes=[]),
        USER,  # type: ignore[arg-type]
        session,  # type: ignore[arg-type]
        "zh-TW",
    )

    assert seeded.is_active is False
    assert session.deleted == []
    assert result["tombstoned"] == 1


@pytest.mark.asyncio
async def test_assigning_to_a_missing_hotspot_is_not_found() -> None:
    session = FakeSession(hotspot=None, themes=[theme("sakura")])

    with pytest.raises(AppError) as missing:
        await assign_hotspot_themes(
            uuid4(),
            HotspotThemesPutPayload(themes=[HotspotThemeAssignment(slug="sakura")]),
            USER,  # type: ignore[arg-type]
            session,  # type: ignore[arg-type]
            "zh-TW",
        )

    assert missing.value.status == 404
    assert missing.value.code == "hotspot_not_found"


@pytest.mark.asyncio
async def test_months_on_a_shop_theme_are_refused_when_assigning() -> None:
    hotspot = TravelHotspot(slug="akihabara", category="shopping")
    hotspot.id = uuid4()
    session = FakeSession(hotspot=hotspot, themes=[theme("drugstore", kind="shop")])

    with pytest.raises(AppError) as refused:
        await assign_hotspot_themes(
            hotspot.id,
            HotspotThemesPutPayload(themes=[HotspotThemeAssignment(slug="drugstore", months=[3])]),
            USER,  # type: ignore[arg-type]
            session,  # type: ignore[arg-type]
            "zh-TW",
        )

    assert refused.value.status == 422
    assert refused.value.code == "theme_months_not_applicable"
