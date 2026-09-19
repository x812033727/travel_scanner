from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import UUID, uuid4

import pytest
from sqlalchemy.sql import operators

from app.hotspots import guide_scan
from app.hotspots.guide_scan import DEFAULT_REASON, SOURCE, run, scan_guides
from app.models import AdminAuditLog, HotspotGuide, TravelHotspot


def _hotspot(name: str, *, city: str, country: str, code: str, destination: str) -> TravelHotspot:
    return TravelHotspot(
        id=uuid4(),
        slug=name,
        name=name,
        city_code=code,
        destination_id=destination,
        city_name=city,
        country_code=code,
        country_name=country,
        category="culture",
        search_text=name,
    )


def _guide(
    hotspot: TravelHotspot,
    title: str,
    *,
    summary: str | None = None,
    locale: str = "zh-TW",
    content_type: str = "article",
    status: str = "approved",
) -> HotspotGuide:
    return HotspotGuide(
        id=uuid4(),
        hotspot_id=hotspot.id,
        content_type=content_type,
        provider="brave" if content_type == "article" else "youtube",
        locale=locale,
        title=title,
        creator_name="someone",
        canonical_url=f"https://example.test/{uuid4().hex}",
        summary=summary,
        review_status=status,
    )


def _ids_filter(statement: Any) -> set[UUID] | None:
    for criterion in statement._where_criteria:
        left = getattr(criterion, "left", None)
        if getattr(left, "key", None) == "id" and criterion.operator is operators.in_op:
            return set(criterion.right.value)
    return None


class FakeSession:
    """Rows, the localization lookup, and a record of what was added and committed."""

    def __init__(
        self,
        rows: list[tuple[HotspotGuide, TravelHotspot]],
        localizations: dict[tuple[UUID, str], Any] | None = None,
    ) -> None:
        self.rows = rows
        self.localizations = localizations or {}
        self.added: list[object] = []
        self.commits = 0
        self.localization_lookups = 0

    async def execute(self, statement: Any) -> SimpleNamespace:
        wanted = _ids_filter(statement)
        rows = [row for row in self.rows if wanted is None or row[0].id in wanted]
        return SimpleNamespace(all=lambda: rows)

    async def scalar(self, statement: Any) -> Any:
        self.localization_lookups += 1
        wanted: list[Any] = []
        for criterion in statement._where_criteria:
            wanted.append(criterion.right.value)
        return self.localizations.get((wanted[0], wanted[1]))

    def add(self, item: object) -> None:
        self.added.append(item)

    async def commit(self) -> None:
        self.commits += 1


def _fixture() -> tuple[FakeSession, dict[str, HotspotGuide], TravelHotspot, TravelHotspot]:
    ngoc_son = _hotspot("玉山祠", city="河內", country="越南", code="VN", destination="hanoi")
    maruyama = _hotspot("圓山公園", city="札幌", country="日本", code="JP", destination="sapporo")
    guides = {
        "yushan": _guide(
            ngoc_son,
            "玉山山脈 > 交通部觀光署",
            summary="位於南臺灣的中央山脈西側，臺灣南投縣水里鄉",
        ),
        "temple": _guide(ngoc_son, "玉山祠｜還劍湖上的文昌帝君廟"),
        "alias": _guide(ngoc_son, "台灣人也推薦的 Ngoc Son Temple"),
        "taipei": _guide(
            maruyama, "圓山自然景觀公園｜花博文化遺跡，台北散步景點", content_type="video"
        ),
        "sapporo": _guide(maruyama, "札幌円山公園の桜と円山動物園", locale="ja"),
        "old": _guide(maruyama, "台北圓山飯店一日遊", status="rejected"),
    }
    rows = [
        (guide, ngoc_son if guide.hotspot_id == ngoc_son.id else maruyama)
        for guide in guides.values()
    ]
    session = FakeSession(
        rows,
        localizations={
            (ngoc_son.id, "zh-TW"): SimpleNamespace(
                name="玉山祠", aliases=["Ngoc Son Temple"], search_terms=["玉山祠 河內"]
            )
        },
    )
    return session, guides, ngoc_son, maruyama


@pytest.mark.asyncio
async def test_the_scan_flags_rows_about_another_country_and_nothing_else() -> None:
    session, guides, _ngoc_son, _maruyama = _fixture()
    # The fake returns every row; the statement itself is what narrows production reads.
    report = await scan_guides(session)
    flagged = {finding.guide_id: finding for finding in report.findings}
    assert set(flagged) == {guides["yushan"].id, guides["taipei"].id, guides["old"].id}
    yushan = flagged[guides["yushan"].id]
    assert (yushan.elsewhere, yushan.city, yushan.country, yushan.content_type) == (
        "台灣",
        "河內",
        "越南",
        "article",
    )
    assert yushan.reason == "地點不符：內容講的是台灣，這個景點在河內（越南）"
    assert flagged[guides["taipei"].id].elsewhere == "台北"
    # The localized alias makes the third row this attraction, as in the review itself,
    # and the localization is read once per attraction and locale, not once per row.
    assert guides["alias"].id not in flagged
    assert session.localization_lookups == 3  # (玉山祠, zh-TW), (圓山公園, zh-TW), (圓山公園, ja)
    assert (report.scanned, report.skipped, report.applied) == (6, 0, False)


@pytest.mark.asyncio
async def test_a_skip_list_keeps_a_known_false_positive() -> None:
    session, guides, _ngoc_son, _maruyama = _fixture()
    report = await scan_guides(session, skip=[guides["yushan"].id])
    assert guides["yushan"].id not in {finding.guide_id for finding in report.findings}
    assert report.skipped == 1


def test_the_statement_reads_only_the_requested_rows() -> None:
    statement = guide_scan.guides_statement(statuses=("approved",), locales=("zh-TW", "ja"))
    where = str(statement.whereclause)
    assert "hotspot_guides.review_status IN" in where
    assert "hotspot_guides.locale IN" in where
    assert "JOIN travel_hotspots" in str(statement)
    # Named rows are looked up whatever their status, so an already rejected id is reported.
    named = guide_scan.guides_statement(statuses=None, ids=[uuid4()])
    assert "review_status" not in str(named.whereclause)
    assert "hotspot_guides.id IN" in str(named.whereclause)


@pytest.mark.asyncio
async def test_a_dry_run_lists_named_rows_too_and_writes_nothing() -> None:
    session, guides, _ngoc_son, _maruyama = _fixture()
    missing = uuid4()
    report = await run(
        session,
        reject=[guides["temple"].id, guides["old"].id, guides["yushan"].id, missing],
    )
    # A named row the rule already flagged is not listed twice; a rejected one and an
    # unknown id are reported instead of silently dropped.
    assert [entry[0] for entry in report.named] == [guides["temple"].id]
    assert report.already_rejected == [guides["old"].id]
    assert report.missing == [missing]
    assert (report.applied, report.rejected, session.commits, session.added) == (False, 0, 0, [])
    assert guides["yushan"].review_status == "approved"


@pytest.mark.asyncio
async def test_applying_rejects_findings_and_named_rows_with_one_audit_entry() -> None:
    session, guides, _ngoc_son, _maruyama = _fixture()
    actor = uuid4()
    report = await run(session, reject=[guides["temple"].id], actor_id=actor)
    assert (report.applied, report.rejected) == (True, 4)  # 3 findings + 1 named row
    for key in ("yushan", "taipei", "temple"):
        guide = guides[key]
        assert guide.review_status == "rejected", key
        assert guide.reviewed_by_user_id == actor
        assert guide.reviewed_at is not None
    assert guides["yushan"].review_reason == "地點不符：內容講的是台灣，這個景點在河內（越南）"
    assert guides["temple"].review_reason == DEFAULT_REASON
    assert guides["alias"].review_status == "approved"
    assert session.commits == 1
    (entry,) = session.added
    assert isinstance(entry, AdminAuditLog)
    assert (entry.action, entry.target, entry.actor_user_id) == (
        "hotspot_guides_reviewed",
        "hotspot-guides:4",
        actor,
    )
    assert entry.metadata_json["action"] == "reject"
    assert entry.metadata_json["source"] == SOURCE
    assert set(entry.metadata_json["ids"]) == {
        str(guides[key].id) for key in ("yushan", "taipei", "old", "temple")
    }


@pytest.mark.asyncio
async def test_applying_with_nothing_to_reject_writes_nothing() -> None:
    ngoc_son = _hotspot("玉山祠", city="河內", country="越南", code="VN", destination="hanoi")
    session = FakeSession([(_guide(ngoc_son, "玉山祠｜還劍湖上的文昌帝君廟"), ngoc_son)])
    report = await run(session, actor_id=uuid4())
    assert (report.applied, report.rejected, session.commits, session.added) == (True, 0, 0, [])
