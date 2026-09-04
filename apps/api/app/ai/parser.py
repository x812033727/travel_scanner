import re
from datetime import UTC, date, datetime
from typing import Protocol

from pydantic import BaseModel, Field

from app.destinations.catalog import (
    DESTINATIONS,
    destination_for_code,
    infer_destination_region,
    match_destination,
)


class ParseTripRequest(BaseModel):
    text: str = Field(min_length=3, max_length=2000)


# The interest vocabulary is shared with the LLM parser in app.ai.trip_parser,
# which offers these codes to the model and drops anything outside the list.
INTEREST_KEYWORDS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("美食", "吃"), "food"),
    (("購物", "逛街"), "shopping"),
    (("文化", "博物館"), "culture"),
    (("自然", "登山"), "nature"),
    (("親子", "家庭", "樂園"), "family"),
    (("夜生活", "酒吧", "夜店"), "nightlife"),
    (("按摩", "溫泉", "水療", "SPA", "spa"), "spa"),
    (("海灘", "沙灘", "跳島"), "beach"),
    (("深度旅遊", "在地", "小眾", "巷弄", "冷門", "近郊"), "deep_travel"),
)
INTEREST_CODES: tuple[str, ...] = tuple(code for _, code in INTEREST_KEYWORDS)


class ParsedTravelers(BaseModel):
    adults: int = 1
    children: int = 0
    children_ages: list[int] = Field(default_factory=list)
    rooms: int = 1


class ParsedTripRequest(BaseModel):
    origin: str | None = None
    destination: str | None = None
    destination_region: str | None = None
    departure_month: str | None = None
    departure_date: str | None = None
    return_date: str | None = None
    travelers: ParsedTravelers = Field(default_factory=ParsedTravelers)
    trip_length_days: int | None = None
    budget_twd: int | None = None
    interests: list[str] = Field(default_factory=list)
    avoid_red_eye: bool = False
    hotel_min_rating: int | None = None
    hotel_max_nightly_twd: int | None = None
    breakfast_required: bool = False
    refundable_required: bool = False
    max_station_walk_minutes: int | None = None
    preferred_area: str | None = None
    pace: str = "balanced"
    confidence: float
    missing_fields: list[str]
    parser: str = "mock-rules-v1"


class AITripParser(Protocol):
    async def parse(self, text: str) -> ParsedTripRequest: ...


class MockAITripParser:
    async def parse(self, text: str) -> ParsedTripRequest:
        upper = text.upper()
        iata_codes = re.findall(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", upper)
        origin = "TPE" if any(word in text for word in ("台北", "臺北", "桃園")) else None
        if origin is None and iata_codes:
            origin = iata_codes[0]
        destination_profile = match_destination(text)
        if destination_profile and destination_profile.code == origin:
            explicit_country = next(
                (
                    profile
                    for profile in DESTINATIONS
                    if profile.country_label in text
                    or profile.country.casefold() in text.casefold()
                ),
                None,
            )
            if explicit_country and explicit_country.country != destination_profile.country:
                destination_profile = explicit_country
        if len(iata_codes) > 1:
            destination = iata_codes[1]
            destination_profile = destination_for_code(destination)
        else:
            destination = destination_profile.code if destination_profile else None
        region = (
            destination_profile.country if destination_profile else infer_destination_region(text)
        )
        people_match = re.search(r"(\d+)\s*(?:個)?人", text)
        chinese_people = {"一個人": 1, "兩個人": 2, "兩人": 2, "三個人": 3, "三人": 3, "四個人": 4}
        adults = (
            int(people_match.group(1))
            if people_match
            else next((value for word, value in chinese_people.items() if word in text), 1)
        )
        days_match = re.search(r"(\d+)\s*天", text)
        budget_match = re.search(r"(?:預算)?\s*(\d+(?:\.\d+)?)\s*萬", text)
        raw_twd_match = re.search(r"預算\s*(\d{4,})", text)
        budget = (
            int(float(budget_match.group(1)) * 10_000)
            if budget_match
            else (int(raw_twd_match.group(1)) if raw_twd_match else None)
        )
        month_match = re.search(r"(1[0-2]|[1-9])\s*月", text)
        iso_dates = re.findall(r"20\d{2}-\d{2}-\d{2}", text)
        departure_month = None
        if month_match:
            month = int(month_match.group(1))
            today = datetime.now(UTC).date()
            year = today.year if month >= today.month else today.year + 1
            departure_month = date(year, month, 1).isoformat()
        elif iso_dates:
            departure_month = iso_dates[0][:7] + "-01"
        interests = [
            code for words, code in INTEREST_KEYWORDS if any(word in text for word in words)
        ]
        rating_match = re.search(r"(?:至少|最低)?\s*([1-5])\s*星", text)
        chinese_rating = next(
            (value for label, value in {"三星": 3, "四星": 4, "五星": 5}.items() if label in text),
            None,
        )
        rooms_match = re.search(r"(\d+)\s*間房", text)
        children_match = re.search(r"(\d+)\s*(?:位|個)?(?:小孩|兒童|孩子)", text)
        child_ages_match = re.search(r"(?:小孩|兒童|孩子)(?:年齡)?\s*([0-9、,，\s]+)\s*歲", text)
        child_ages = (
            [int(value) for value in re.findall(r"\d+", child_ages_match.group(1))]
            if child_ages_match
            else []
        )
        nightly_match = re.search(r"(?:飯店|住宿)?\s*每晚(?:預算|最多|上限)?\s*(\d{3,})", text)
        walk_match = re.search(r"(?:車站)?步行(?:不超過|最多|上限)?\s*(\d+)\s*分", text)
        preferred_area_match = re.search(r"(?:想住|住在|住宿區域)\s*([^，,。]{2,20})", text)
        pace = "balanced"
        if any(word in text for word in ("悠閒", "放鬆", "慢遊", "慢旅行")):
            pace = "relaxed"
        elif any(word in text for word in ("緊湊", "充實", "多排", "跑景點")):
            pace = "packed"
        missing = []
        if origin is None:
            missing.append("origin")
        if destination is None and region is None:
            missing.append("destination")
        if departure_month is None:
            missing.append("departure_date")
        # A regex parse is never certain either, so it stays under the same
        # 0.95 ceiling the LLM parser uses; the two are compared on one field.
        confidence = max(0.45, min(0.9, 1 - len(missing) * 0.15))
        return ParsedTripRequest(
            origin=origin,
            destination=destination,
            destination_region=region,
            departure_month=departure_month,
            departure_date=iso_dates[0] if iso_dates else None,
            return_date=iso_dates[1] if len(iso_dates) > 1 else None,
            travelers=ParsedTravelers(
                adults=adults,
                children=len(child_ages) or (int(children_match.group(1)) if children_match else 0),
                children_ages=child_ages,
                rooms=int(rooms_match.group(1)) if rooms_match else 1,
            ),
            trip_length_days=int(days_match.group(1)) if days_match else None,
            budget_twd=budget,
            interests=interests,
            avoid_red_eye=any(word in text for word in ("不要紅眼", "避免紅眼", "非紅眼")),
            hotel_min_rating=int(rating_match.group(1)) if rating_match else chinese_rating,
            hotel_max_nightly_twd=int(nightly_match.group(1)) if nightly_match else None,
            breakfast_required=any(word in text for word in ("含早餐", "要早餐", "包含早餐")),
            refundable_required=any(word in text for word in ("可退款", "免費取消", "可取消")),
            max_station_walk_minutes=int(walk_match.group(1)) if walk_match else None,
            preferred_area=preferred_area_match.group(1).strip() if preferred_area_match else None,
            pace=pace,
            confidence=confidence,
            missing_fields=missing,
        )
