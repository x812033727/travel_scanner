"""The per-slug publish hold: content that may be imported but must not go live yet.

A hold exists because an article can reach ``main`` without the review its own pull request
asked for -- #635 did, carrying an unapproved fare correction -- and the next
``guides-import --publish`` would otherwise ship it. The hold stops publication only; the
draft still imports, so a sweep over every pack is not blocked by one held article.
"""

from __future__ import annotations

import asyncio

import pytest

from app.cli import import_guides
from app.guides import content_pack
from app.guides.content_pack import (
    ContentPackError,
    apply_import,
    default_directory,
    load_packs,
    load_publish_holds,
    plan_import,
    publish_holds_path,
)
from tests import test_guides as guides
from tests.test_guides_content_pack import write_pack

database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
publish = guides.publish

REASON = "batch010 review gate is open"


@pytest.fixture
def hold(monkeypatch):
    """Replace the shipped hold list for the duration of one test."""

    def apply(mapping: dict[str, str]) -> None:
        monkeypatch.setattr(content_pack, "load_publish_holds", lambda: dict(mapping))

    return apply


async def test_a_held_article_imports_its_draft_but_is_never_published(
    database, actor, tmp_path, hold
) -> None:
    write_pack(tmp_path, "singapore-changi")
    hold({"singapore-changi": REASON})

    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        entry = plan.articles[0]
        assert entry.publish_hold == REASON
        # Every locale is planned for import and none of them for publication.
        assert [item.action for item in entry.locales] == ["create", "create"]
        assert [item.publish for item in entry.locales] == [False, False]
        assert plan.as_dict()["articles"][0]["publish_hold"] == REASON

        report = await apply_import(session, actor, plan, publish=True)

    assert report.failed is None
    assert report.created == ["singapore-changi:zh-TW", "singapore-changi:en"]
    # The run asked to publish and refused, and says so rather than staying silent.
    assert report.published == []
    assert report.publish_held == {"singapore-changi": REASON}
    assert report.as_dict()["publish_held"] == {"singapore-changi": REASON}

    async with client(make_app(database)) as api:
        body = await api.get("/guides/howto/singapore-changi", params={"locale": "zh-TW"})
        assert body.json()["status"] != "published"


async def test_a_hold_does_not_stop_the_other_packs_in_the_same_run(
    database, actor, tmp_path, hold
) -> None:
    write_pack(tmp_path, "singapore-changi")
    write_pack(tmp_path, "narita-to-tokyo")
    hold({"singapore-changi": REASON})

    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        report = await apply_import(session, actor, plan, publish=True)

    assert report.failed is None
    assert report.publish_held == {"singapore-changi": REASON}
    assert report.published == ["narita-to-tokyo:zh-TW", "narita-to-tokyo:en"]


async def test_a_held_article_already_live_is_left_alone(database, actor, tmp_path, hold) -> None:
    """A hold applied after publication does not unpublish anything; it only stops the
    next publication. Retracting live content is an editorial decision, not an import."""
    write_pack(tmp_path, "singapore-changi")
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        await apply_import(session, actor, plan, publish=True)

    write_pack(tmp_path, "singapore-changi", locales={"zh-TW": document(title="改過的標題")})
    hold({"singapore-changi": REASON})
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        report = await apply_import(session, actor, plan, publish=True)

    assert report.updated == ["singapore-changi:zh-TW"]
    assert report.published == []
    assert report.publish_held == {"singapore-changi": REASON}
    async with client(make_app(database)) as api:
        body = (await api.get("/guides/howto/singapore-changi", params={"locale": "zh-TW"})).json()
        assert body["status"] == "published"
        # The live text is the reviewed one; the unreviewed edit sits in the draft.
        assert body["document"]["title"] != "改過的標題"


def test_naming_a_held_slug_and_asking_to_publish_is_refused(monkeypatch, tmp_path) -> None:
    """Sweeping every pack skips a held one quietly-but-reported; asking for it by name is
    not that accident, so it fails loudly before anything is read or written."""
    monkeypatch.setattr("app.cli.load_publish_holds", lambda: {"singapore-changi": REASON})
    with pytest.raises(SystemExit) as refusal:
        asyncio.run(
            import_guides(
                directory=tmp_path,
                actor_email="editor@example.com",
                slugs={"singapore-changi"},
                locales=None,
                publish=True,
                dry_run=False,
            )
        )
    message = str(refusal.value)
    assert "singapore-changi" in message
    assert REASON in message
    assert publish_holds_path().name in message


def test_naming_a_held_slug_without_publish_is_allowed(monkeypatch, tmp_path) -> None:
    """Importing a held article's draft is the point of the hold being publish-only."""
    monkeypatch.setattr("app.cli.load_publish_holds", lambda: {"singapore-changi": REASON})
    write_pack(tmp_path, "singapore-changi")
    with pytest.raises(SystemExit) as stop:
        asyncio.run(
            import_guides(
                directory=tmp_path,
                actor_email=None,
                slugs={"singapore-changi"},
                locales=None,
                publish=False,
                dry_run=False,
            )
        )
    # It got past the hold and stopped on the unrelated missing-actor rule.
    assert "actor" in str(stop.value).lower()


def test_a_malformed_hold_list_is_refused(tmp_path) -> None:
    path = tmp_path / "publish_holds.json"
    path.write_text('{"slug": ""}', encoding="utf-8")
    with pytest.raises(ContentPackError):
        load_publish_holds(path)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ContentPackError):
        load_publish_holds(path)
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ContentPackError):
        load_publish_holds(path)


def test_a_missing_hold_list_holds_nothing(tmp_path) -> None:
    assert load_publish_holds(tmp_path / "absent.json") == {}


def test_every_shipped_hold_names_a_real_pack() -> None:
    """A hold on a slug that does not exist protects nothing and reads as if it does, so a
    typo in the list must fail here rather than at the next release."""
    holds = load_publish_holds()
    slugs = {pack.slug for pack in load_packs(default_directory())}
    assert set(holds) <= slugs, f"held slugs with no pack: {sorted(set(holds) - slugs)}"
    assert all(reason.strip() for reason in holds.values())
