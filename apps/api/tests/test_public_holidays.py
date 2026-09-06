"""The vendored calendars, the parsers that refresh them, and the public endpoint.

The dates asserted here are the product's contract with the reader: a wrong one puts a
red dot on a working Tuesday, or leaves Chuseok unmarked in the most expensive week of
the Korean year. They are checked against the government files verbatim.
"""

from __future__ import annotations

import json

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.holidays import refresh as refresh_module
from app.holidays.service import (
    ATTRIBUTION,
    LOCALES,
    calendars,
    holidays_between,
    is_working_day,
)
from app.main import app

# A slice of the real 114年 file, which is the one DGPA reissued in cp950 and the only
# published year that carries a make-up working Saturday.
TW_CSV_2025 = "\n".join([
    "西元日期,星期,是否放假,備註",
    "20250101,三,2,開國紀念日",
    "20250125,六,2,",
    "20250208,六,0,補行上班",
    "20250228,五,2,和平紀念日",
    "20251006,一,2,補假",
    "20251225,四,2,行憲紀念日",
])
TW_CATALOG = {
    "result": {
        "distribution": [
            {
                "resourceDescription": "114年中華民國政府行政機關辦公日曆表",
                "resourceFormat": "CSV",
                "resourceDownloadUrl": "https://www.dgpa.gov.tw/FileConversion?filename=old.csv",
            },
            {
                "resourceDescription": "114年中華民國政府行政機關辦公日曆表_Google行事曆專用",
                "resourceFormat": "CSV",
                "resourceDownloadUrl": "https://www.dgpa.gov.tw/FileConversion?filename=cal.csv",
            },
            {
                "resourceDescription": "114年中華民國政府行政機關辦公日曆表(1141020更新)",
                "resourceFormat": "CSV",
                "resourceDownloadUrl": "https://www.dgpa.gov.tw/FileConversion?filename=new.csv",
            },
        ]
    }
}
# 内閣府's own file: Shift_JIS, CRLF, unpadded dates, and two rows named only 休日.
JP_CSV = "\r\n".join([
    "国民の祝日・休日月日,国民の祝日・休日名称",
    "2026/5/3,憲法記念日",
    "2026/5/4,みどりの日",
    "2026/5/5,こどもの日",
    "2026/5/6,休日",
    "2026/9/21,敬老の日",
    "2026/9/22,休日",
    "2026/9/23,秋分の日",
]) + "\r\n"


def _client(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_the_taiwanese_parser_reads_cp950_and_keeps_a_make_up_saturday_a_working_day() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "data.gov.tw":
            return httpx.Response(200, json=TW_CATALOG)
        assert request.url.params["filename"] == "new.csv", "the reissued file wins"
        return httpx.Response(200, content=TW_CSV_2025.encode("cp950"))

    with _client(handler) as client:
        rows = refresh_module.tw_rows(client, 2025)

    by_date = {row["date"]: row for row in rows}
    assert set(by_date) == {"2025-01-01", "2025-02-08", "2025-02-28", "2025-10-06", "2025-12-25"}
    assert "2025-01-25" not in by_date, "a plain weekend has no name and no row"
    make_up = by_date["2025-02-08"]
    assert (make_up["kind"], make_up["is_working_day"]) == ("makeup_workday", True)
    assert by_date["2025-10-06"]["kind"] == "substitute"
    assert by_date["2025-12-25"]["key"] == "tw_constitution_day"


def test_the_japanese_parser_tells_a_substitute_from_a_citizens_holiday() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "www8.cao.go.jp", "www.cao.go.jp/syukujitsu.csv is a 404 page"
        return httpx.Response(200, content=JP_CSV.encode("shift_jis"))

    with _client(handler) as client:
        rows = refresh_module.jp_rows(client, 2026)

    by_date = {row["date"]: row for row in rows}
    assert by_date["2026-05-06"]["kind"] == "substitute"
    assert by_date["2026-05-06"]["key"] == "jp_constitution_memorial_day_substitute"
    assert by_date["2026-09-22"]["kind"] == "bridge_holiday"
    assert by_date["2026-09-22"]["key"] == "jp_citizens_holiday"


def test_a_refresh_of_a_year_already_in_the_repository_reports_no_difference() -> None:
    """What the parsers produce is what is vendored, minus the hand-written names."""
    for country, year in (("tw", 2026), ("tw", 2027), ("jp", 2026), ("jp", 2027)):
        stored = json.loads((refresh_module.DATA_DIR / f"{country}_{year}.json").read_text("utf-8"))
        fetched = [
            {key: row[key] for key in ("date", "key", "kind", "is_working_day", "source")}
            for row in stored
        ]
        diff = refresh_module.compare(country, year, fetched)
        assert diff.empty, diff.as_dict()


def test_every_vendored_row_is_named_in_all_five_locales() -> None:
    for country, rows in calendars().items():
        assert rows, f"{country} has no calendar"
        for row in rows:
            for locale in LOCALES:
                assert row.name(locale).strip(), f"{country} {row.date} has no {locale} name"


def test_taiwan_2026_matches_the_office_calendar_word_for_word() -> None:
    rows = holidays_between("TW", "2026-01-01", "2026-12-31")
    assert len(rows) == 22
    assert sum(1 for row in rows if row.kind == "substitute") == 6
    named = {row.date: row.name("zh-TW") for row in rows}
    assert named["2026-02-15"] == "小年夜"
    assert named["2026-02-16"] == "農曆除夕"
    assert named["2026-09-28"] == "孔子誕辰紀念日/教師節"
    assert named["2026-10-25"] == "臺灣光復暨金門古寧頭大捷紀念日"
    assert named["2026-12-25"] == "行憲紀念日"
    assert not any(row.is_working_day for row in rows), "2026 has no make-up Saturday"


def test_the_lunar_new_year_break_is_nine_days_long() -> None:
    """The union of weekends and holidays, minus make-up days — not a sum of counts."""
    days = [f"2026-02-{day:02d}" for day in range(12, 26)]
    off = [day for day in days if not is_working_day("TW", day)]
    assert off == [f"2026-02-{day:02d}" for day in range(14, 23)]


def test_japan_2026_keeps_the_two_days_general_apis_drop() -> None:
    rows = holidays_between("JP", "2026-01-01", "2026-12-31")
    assert len(rows) == 18
    kinds = {row.date: row.kind for row in rows}
    assert kinds["2026-05-06"] == "substitute", "Golden Week is five days, not four"
    assert kinds["2026-09-22"] == "bridge_holiday", "Silver Week exists in 2026"


def test_korea_2026_has_no_invented_chuseok_substitute() -> None:
    rows = holidays_between("KR", "2026-01-01", "2026-12-31")
    assert len(rows) == 22
    dates = {row.date for row in rows}
    assert {"2026-09-24", "2026-09-25", "2026-09-26"} <= dates
    assert "2026-09-28" not in dates, "제3조제2항 substitutes a Sunday overlap, not a Saturday"
    assert "2026-06-08" not in dates, "현충일 is not in the 제3조제1항 list either"
    assert "2026-06-03" in dates, "the local election day is a public holiday"


def test_a_make_up_working_saturday_would_stay_a_working_day() -> None:
    """2026 and 2027 have none, so the guarantee is checked on the kind, not on a date."""
    assert is_working_day("TW", "2026-02-14") is False, "a plain Saturday is not a working day"
    assert is_working_day("TW", "2026-02-25") is True
    assert refresh_module.TW_KINDS["補行上班"] == "makeup_workday"


@pytest.mark.asyncio
async def test_the_endpoint_answers_without_a_session_and_in_the_readers_language() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        golden_week = await client.get(
            "/api/v1/holidays",
            params={"country": "JP", "from": "2026-05-01", "to": "2026-05-10", "locale": "zh-TW"},
        )
        assert golden_week.status_code == 200, golden_week.text
        body = golden_week.json()
        assert [row["date"] for row in body["holidays"]] == [
            "2026-05-03",
            "2026-05-04",
            "2026-05-05",
            "2026-05-06",
        ]
        assert body["holidays"][0]["name"] == "憲法紀念日"
        assert body["country_name"] == "日本"
        assert body["attribution"] == ATTRIBUTION["JP"]
        assert body["coverage_end"] == "2027-12-31"
        assert golden_week.headers["cache-control"].startswith("public")

        korean = await client.get(
            "/api/v1/holidays",
            params={"country": "kr", "from": "2026-09-20", "to": "2026-09-30", "locale": "ko"},
        )
        assert [row["date"] for row in korean.json()["holidays"]] == [
            "2026-09-24",
            "2026-09-25",
            "2026-09-26",
        ]
        assert korean.json()["holidays"][1]["name"] == "추석"

        english = await client.get(
            "/api/v1/holidays",
            params={"country": "TW", "from": "2026-02-14", "to": "2026-02-23", "locale": "en"},
        )
        names = [row["name"] for row in english.json()["holidays"]]
        assert names[0] == "Lunar New Year's Eve Eve"
        assert all(name.isascii() for name in names)


@pytest.mark.asyncio
async def test_the_endpoint_refuses_a_country_it_has_no_calendar_for() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        unknown = await client.get(
            "/api/v1/holidays", params={"country": "TH", "from": "2026-01-01", "to": "2026-12-31"}
        )
        assert unknown.status_code == 404
        assert unknown.json()["code"] == "holiday_country_unknown"

        backwards = await client.get(
            "/api/v1/holidays", params={"country": "TW", "from": "2026-05-01", "to": "2026-04-01"}
        )
        assert backwards.status_code == 422
        assert backwards.json()["code"] == "holiday_range_invalid"
