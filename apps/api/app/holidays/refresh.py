"""Re-read the two government calendars and say what changed.

Governments amend calendars they have already published — the 114年 Taiwanese file was
reissued with three working days turned into holidays — so this is a diff you run again,
not an import you run once. It never writes the ``names`` a human wrote; when a new key
appears it says so and leaves the translation to a person.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import httpx

from app.holidays.service import DATA_DIR, LOCALES

TW_CATALOG_URL = "https://data.gov.tw/api/v2/rest/dataset/14718"
# The CSV itself sits behind an opaque GUID that changes with every reissue, so the
# download URL is always read from the catalogue rather than written down here.
JP_CALENDAR_URL = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
TW_ENCODINGS = ("utf-8-sig", "utf-8", "cp950")
TIMEOUT_SECONDS = 60.0

TW_KINDS = {"補假": "substitute", "補行上班": "makeup_workday"}
TW_KEYS = {
    "開國紀念日": "tw_founding_day",
    "小年夜": "tw_lunar_new_year_eve_eve",
    "農曆除夕": "tw_lunar_new_year_eve",
    "春節": "tw_lunar_new_year",
    "補假": "tw_substitute",
    "補行上班": "tw_makeup_workday",
    "和平紀念日": "tw_peace_memorial_day",
    "兒童節": "tw_childrens_day",
    "清明節": "tw_tomb_sweeping_day",
    "勞動節": "tw_labour_day",
    "端午節": "tw_dragon_boat_festival",
    "中秋節": "tw_mid_autumn_festival",
    "孔子誕辰紀念日/教師節": "tw_teachers_day",
    "國慶日": "tw_national_day",
    "臺灣光復暨金門古寧頭大捷紀念日": "tw_retrocession_day",
    "行憲紀念日": "tw_constitution_day",
}
JP_KEYS = {
    "元日": "jp_new_years_day",
    "成人の日": "jp_coming_of_age_day",
    "建国記念の日": "jp_national_foundation_day",
    "天皇誕生日": "jp_emperors_birthday",
    "春分の日": "jp_vernal_equinox_day",
    "昭和の日": "jp_showa_day",
    "憲法記念日": "jp_constitution_memorial_day",
    "みどりの日": "jp_greenery_day",
    "こどもの日": "jp_childrens_day",
    "海の日": "jp_marine_day",
    "山の日": "jp_mountain_day",
    "敬老の日": "jp_respect_for_the_aged_day",
    "秋分の日": "jp_autumnal_equinox_day",
    "スポーツの日": "jp_sports_day",
    "文化の日": "jp_culture_day",
    "勤労感謝の日": "jp_labour_thanksgiving_day",
}


class HolidaySourceError(RuntimeError):
    """The upstream file could not be read; the vendored data is left alone."""


@dataclass
class Diff:
    country: str
    year: int
    added: list[dict[str, str]] = field(default_factory=list)
    removed: list[dict[str, str]] = field(default_factory=list)
    changed: list[dict[str, str]] = field(default_factory=list)
    untranslated: list[str] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not (self.added or self.removed or self.changed or self.untranslated)

    def as_dict(self) -> dict[str, Any]:
        return {
            "country": self.country,
            "year": self.year,
            "added": self.added,
            "removed": self.removed,
            "changed": self.changed,
            "untranslated": self.untranslated,
            "unchanged": self.empty,
        }


def _decode(raw: bytes) -> str:
    """The encoding is sniffed, never inferred from the year: one 114年 file is cp950."""
    for encoding in TW_ENCODINGS:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise HolidaySourceError("the Taiwanese calendar decoded as none of " + ", ".join(TW_ENCODINGS))


def _get(client: httpx.Client, url: str) -> httpx.Response:
    try:
        response = client.get(url, timeout=TIMEOUT_SECONDS, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as exc:  # includes the DGPA certificate chain failure
        raise HolidaySourceError(f"{url} could not be read: {exc}") from exc
    return response


def tw_download_url(client: httpx.Client, year: int) -> str:
    """The CSV for one year, found in the catalogue by its Republic-of-China title.

    The fields are ``resourceDescription`` / ``resourceDownloadUrl`` under
    ``result.distribution`` — not the ``resources[]`` shape most catalogues use. When a
    year has been reissued the later entry wins, which is how an amended calendar arrives.
    """
    catalog = _get(client, TW_CATALOG_URL).json()
    title = f"{year - 1911}年中華民國政府行政機關辦公日曆表"
    matches = [
        entry
        for entry in catalog.get("result", {}).get("distribution", [])
        if str(entry.get("resourceDescription", "")).startswith(title)
        and "Google行事曆專用" not in str(entry.get("resourceDescription", ""))
    ]
    if not matches:
        raise HolidaySourceError(f"the catalogue has no {title}")
    return str(matches[-1]["resourceDownloadUrl"])


def tw_rows(client: httpx.Client, year: int) -> list[dict[str, Any]]:
    """Every day the Taiwanese calendar names, as vendored rows without ``names``."""
    return tw_rows_from_bytes(_get(client, tw_download_url(client, year)).content)


def tw_rows_from_bytes(raw: bytes) -> list[dict[str, Any]]:
    """The same parse from a file on disk, for the days the CSV cannot be downloaded."""
    text = _decode(raw)
    rows: list[dict[str, Any]] = []
    for row in csv.DictReader(io.StringIO(text)):
        note = (row.get("備註") or "").strip()
        if not note:
            continue  # a plain weekend: no name, nothing to show a reader
        raw_date = (row.get("西元日期") or "").strip()
        day = date(int(raw_date[:4]), int(raw_date[4:6]), int(raw_date[6:8]))
        off = (row.get("是否放假") or "").strip() == "2"
        rows.append({
            "date": day.isoformat(),
            "key": TW_KEYS.get(note, note),
            "kind": TW_KINDS.get(note, "public_holiday"),
            "is_working_day": not off,
            "source": "dgpa_gov_tw",
        })
    return rows


def jp_rows(client: httpx.Client, year: int) -> list[dict[str, Any]]:
    """The Cabinet Office calendar for one year, with its two kinds of ``休日`` told apart.

    A ``休日`` between two holidays is a 国民の休日; otherwise it is the 振替休日 of the most
    recent Sunday holiday, and it is named after that holiday.
    """
    return jp_rows_from_bytes(_get(client, JP_CALENDAR_URL).content, year)


def jp_rows_from_bytes(raw: bytes, year: int) -> list[dict[str, Any]]:
    """The same parse from a file on disk. The file is Shift_JIS with CRLF line endings."""
    text = raw.decode("shift_jis")
    parsed: dict[str, str] = {}
    for line in csv.reader(io.StringIO(text)):
        if len(line) != 2 or "/" not in line[0]:
            continue
        parts = [int(part) for part in line[0].split("/")]
        parsed[date(parts[0], parts[1], parts[2]).isoformat()] = line[1].strip()
    rows: list[dict[str, Any]] = []
    for day_text, name in sorted(parsed.items()):
        if not day_text.startswith(str(year)):
            continue
        day = date.fromisoformat(day_text)
        if name != "休日":
            key, kind = JP_KEYS.get(name, name), "public_holiday"
        elif (
            (day - timedelta(days=1)).isoformat() in parsed
            and (day + timedelta(days=1)).isoformat() in parsed
        ):
            key, kind = "jp_citizens_holiday", "bridge_holiday"
        else:
            back = day
            while back.isoformat() in parsed and back.weekday() != 6:
                back -= timedelta(days=1)
            base = JP_KEYS.get(parsed.get(back.isoformat(), ""), "jp_unknown")
            key, kind = f"{base}_substitute", "substitute"
        rows.append({
            "date": day_text,
            "key": key,
            "kind": kind,
            "is_working_day": False,
            "source": "cao_go_jp",
        })
    return rows


def _vendored(country: str, year: int) -> list[dict[str, Any]]:
    path = DATA_DIR / f"{country}_{year}.json"
    if not path.exists():
        return []
    loaded: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def compare(country: str, year: int, fetched: list[dict[str, Any]]) -> Diff:
    """What the upstream file says minus what is in the repository."""
    diff = Diff(country=country, year=year)
    stored = {row["date"]: row for row in _vendored(country, year)}
    fresh = {row["date"]: row for row in fetched}
    translated = {row["key"] for row in stored.values()}
    diff.untranslated = sorted({row["key"] for row in fetched if row["key"] not in translated})
    for day in sorted(set(fresh) - set(stored)):
        diff.added.append({"date": day, "key": fresh[day]["key"], "kind": fresh[day]["kind"]})
    for day in sorted(set(stored) - set(fresh)):
        diff.removed.append({"date": day, "key": stored[day]["key"], "kind": stored[day]["kind"]})
    for day in sorted(set(stored) & set(fresh)):
        for field_name in ("key", "kind", "is_working_day"):
            if stored[day][field_name] != fresh[day][field_name]:
                diff.changed.append({
                    "date": day,
                    "field": field_name,
                    "stored": str(stored[day][field_name]),
                    "upstream": str(fresh[day][field_name]),
                })
    return diff


def apply(country: str, year: int, fetched: list[dict[str, Any]]) -> int:
    """Write the fetched dates back, carrying every human-written name across.

    A row whose key is new has no translation to carry, so it is written with the names of
    the key it replaced on that date when there is one, and otherwise refused: an empty
    name would reach a calendar cell as a blank tooltip.
    """
    stored = {row["date"]: row for row in _vendored(country, year)}
    by_key = {row["key"]: row["names"] for row in stored.values()}
    written: list[dict[str, Any]] = []
    for row in fetched:
        names = by_key.get(row["key"]) or (stored.get(row["date"], {}) or {}).get("names")
        if not names or any(not names.get(locale) for locale in LOCALES):
            raise HolidaySourceError(
                f"{country} {row['date']} ({row['key']}) has no translation yet; "
                "add its names to the data file before applying"
            )
        merged = dict(row)
        merged["names"] = names
        note = (stored.get(row["date"], {}) or {}).get("note")
        if note:
            merged["note"] = note
        written.append(merged)
    path = DATA_DIR / f"{country}_{year}.json"
    path.write_text(json.dumps(written, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(written)


def refresh(
    country: str,
    year: int,
    *,
    write: bool = False,
    file: Path | None = None,
) -> dict[str, Any]:
    """Read one country-year, report the diff, and only write when asked to.

    ``file`` parses a copy downloaded by hand. Python cannot fetch the Taiwanese CSV at
    all — its intermediate certificate is missing a Subject Key Identifier, which curl
    tolerates and OpenSSL does not, on this machine and inside the production image alike
    — so that path is the supported one for Taiwan rather than a fallback.
    """
    code = country.lower()
    if code == "kr":
        raise HolidaySourceError(
            "Korea has no machine-readable source in scope: its rows are written by hand "
            "from 관공서의 공휴일에 관한 규정. See docs/public-holidays.md."
        )
    if file is not None:
        raw = file.read_bytes()
        fetched = tw_rows_from_bytes(raw) if code == "tw" else jp_rows_from_bytes(raw, year)
        if code == "tw" and any(not row["date"].startswith(str(year)) for row in fetched):
            raise HolidaySourceError(f"{file} is not the calendar for {year}")
    else:
        agent = {"User-Agent": "mokaair-holidays/1.0 (+https://mokaair.com)"}
        with httpx.Client(headers=agent) as client:
            fetched = tw_rows(client, year) if code == "tw" else jp_rows(client, year)
    diff = compare(code, year, fetched)
    summary = diff.as_dict()
    summary["fetched"] = len(fetched)
    if write and not diff.empty:
        summary["written"] = apply(code, year, fetched)
    return summary
