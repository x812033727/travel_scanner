"""``GET /holidays``: a public, cacheable read of the vendored calendars."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel

from app.holidays.service import (
    ATTRIBUTION,
    COUNTRIES,
    COUNTRY_NAMES,
    Holiday,
    coverage,
    holidays_between,
)
from app.i18n import Locale, current_locale
from app.problems import AppError

router = APIRouter(prefix="/holidays", tags=["holidays"])

CurrentLocale = Annotated[Locale, Depends(current_locale)]
# A year of calendar is 365 days; a request wider than three years is a mistake, not a plan.
MAX_RANGE_DAYS = 1_100
# The data changes once a year and ships in the image, so a day of caching is honest.
CACHE_CONTROL = "public, max-age=86400, stale-while-revalidate=604800"


class HolidayRow(BaseModel):
    date: str
    key: str
    kind: Literal["public_holiday", "substitute", "bridge_holiday", "makeup_workday"]
    is_working_day: bool
    name: str
    country: str
    country_name: str
    source: str


class HolidayList(BaseModel):
    country: str
    country_name: str
    locale: str
    coverage_start: str | None
    coverage_end: str | None
    attribution: str
    holidays: list[HolidayRow]


def _serialize(row: Holiday, locale: str) -> HolidayRow:
    return HolidayRow(
        date=row.date,
        key=row.key,
        kind=row.kind,
        is_working_day=row.is_working_day,
        name=row.name(locale),
        country=row.country,
        country_name=COUNTRY_NAMES[row.country][locale],
        source=row.source,
    )


@router.get("", response_model=HolidayList)
async def list_holidays(
    response: Response,
    request_locale: CurrentLocale,
    country: Annotated[str, Query(min_length=2, max_length=2)],
    from_: Annotated[str, Query(alias="from", pattern=r"^\d{4}-\d{2}-\d{2}$")],
    to: Annotated[str, Query(pattern=r"^\d{4}-\d{2}-\d{2}$")],
    locale: Annotated[Locale | None, Query()] = None,
) -> HolidayList:
    """Public holidays for one country over one date range, named in the reader's language.

    Static data: no session, no database, no upstream call. A day the vendored calendar
    does not cover is simply absent, which is what ``coverage_end`` is for — the caller can
    tell "no holidays that week" apart from "we do not know that year yet".
    """
    code = country.upper()
    if code not in COUNTRIES:
        raise AppError(404, "holiday_country_unknown", f"沒有 {code} 的假日資料")
    if to < from_:
        raise AppError(422, "holiday_range_invalid", "結束日期早於開始日期")
    if (date.fromisoformat(to) - date.fromisoformat(from_)).days > MAX_RANGE_DAYS:
        raise AppError(422, "holiday_range_too_wide", "一次最多查詢三年份的假日")
    chosen = locale or request_locale
    span = coverage(code)
    response.headers["Cache-Control"] = CACHE_CONTROL
    return HolidayList(
        country=code,
        country_name=COUNTRY_NAMES[code][chosen],
        locale=chosen,
        coverage_start=span[0] if span else None,
        coverage_end=span[1] if span else None,
        attribution=ATTRIBUTION[code],
        holidays=[_serialize(row, chosen) for row in holidays_between(code, from_, to)],
    )
