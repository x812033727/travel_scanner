"""Reading the vendored calendars: in memory, ISO strings, no timezone arithmetic."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
COUNTRIES = ("TW", "JP", "KR")
LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")
DEFAULT_LOCALE = "zh-TW"
KINDS = ("public_holiday", "substitute", "bridge_holiday", "makeup_workday")

COUNTRY_NAMES: dict[str, dict[str, str]] = {
    "TW": {"zh-TW": "臺灣", "zh-CN": "台湾", "en": "Taiwan", "ja": "台湾", "ko": "대만"},
    "JP": {"zh-TW": "日本", "zh-CN": "日本", "en": "Japan", "ja": "日本", "ko": "일본"},
    "KR": {"zh-TW": "韓國", "zh-CN": "韩国", "en": "South Korea", "ja": "韓国", "ko": "대한민국"},
}

# The licence terms are in docs/public-holidays.md; these are the strings they oblige us
# to show. Taiwan's is the strict one: without it the open-data licence is treated as
# never having been granted, so it travels with the data rather than living in a template.
ATTRIBUTION: dict[str, str] = {
    "TW": (
        "本資料使用行政院人事行政總處「中華民國政府行政機關辦公日曆表」"
        "（115年版、116年版），依政府資料開放授權條款第1版"
        "（https://data.gov.tw/license）提供，本網站另行標註假日類別。"
    ),
    "JP": (
        "出典：内閣府ウェブサイト"
        "（https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv）、"
        "公共データ利用規約（第1.0版）"
        "（https://www.digital.go.jp/resources/open_data/public_data_license_v1.0）。"
        "振替休日と国民の休日の区別は当サイトによる加工です。"
    ),
    "KR": (
        "「관공서의 공휴일에 관한 규정」(대통령령)과 관련 법률의 조문을 근거로 "
        "본 사이트가 직접 작성했습니다."
    ),
}


@dataclass(frozen=True)
class Holiday:
    """One dated row of a national calendar, with its name already in five languages."""

    country: str
    date: str
    key: str
    kind: str
    is_working_day: bool
    names: dict[str, str]
    source: str
    note: str | None = None

    def name(self, locale: str) -> str:
        return self.names.get(locale) or self.names[DEFAULT_LOCALE]


def _row(country: str, payload: dict[str, object]) -> Holiday:
    names = payload["names"]
    assert isinstance(names, dict)
    missing = [locale for locale in LOCALES if not names.get(locale)]
    if missing:
        raise ValueError(f"{country} {payload['date']} is missing {', '.join(missing)}")
    kind = str(payload["kind"])
    if kind not in KINDS:
        raise ValueError(f"{country} {payload['date']} has an unknown kind {kind!r}")
    note = payload.get("note")
    return Holiday(
        country=country,
        date=str(payload["date"]),
        key=str(payload["key"]),
        kind=kind,
        is_working_day=bool(payload["is_working_day"]),
        names={locale: str(names[locale]) for locale in LOCALES},
        source=str(payload["source"]),
        note=str(note) if note else None,
    )


@lru_cache(maxsize=1)
def calendars() -> dict[str, tuple[Holiday, ...]]:
    """Every vendored row, by country, sorted by date. Read once per process."""
    loaded: dict[str, list[Holiday]] = {country: [] for country in COUNTRIES}
    for path in sorted(DATA_DIR.glob("*_*.json")):
        country = path.stem.split("_")[0].upper()
        if country not in loaded:
            raise ValueError(f"{path.name} is not one of {COUNTRIES}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        loaded[country].extend(_row(country, item) for item in payload)
    for country, rows in loaded.items():
        dates = [row.date for row in rows]
        if len(dates) != len(set(dates)):
            raise ValueError(f"{country} has two rows for the same day")
    return {
        country: tuple(sorted(rows, key=lambda row: row.date))
        for country, rows in loaded.items()
    }


def coverage(country: str) -> tuple[str, str] | None:
    """The first and last day the vendored data can answer for, or None when empty."""
    rows = calendars().get(country.upper(), ())
    if not rows:
        return None
    return f"{rows[0].date[:4]}-01-01", f"{rows[-1].date[:4]}-12-31"


def holidays_between(country: str, start: str, end: str) -> list[Holiday]:
    """Rows from ``start`` to ``end`` inclusive, both ISO ``YYYY-MM-DD`` strings."""
    rows = calendars().get(country.upper(), ())
    return [row for row in rows if start <= row.date <= end]


def is_working_day(country: str, day: str) -> bool:
    """Whether offices open. A make-up Saturday counts as work; a plain weekend does not.

    Long weekends are the union of {weekend, holidays} minus {make-up work days}; adding
    holiday counts to weekend counts double-counts every holiday that already falls on one.
    """
    for row in calendars().get(country.upper(), ()):
        if row.date == day:
            return row.is_working_day
    return date.fromisoformat(day).weekday() < 5
