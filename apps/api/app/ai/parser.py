import re
from datetime import UTC, date, datetime
from typing import Protocol

from pydantic import BaseModel, Field


class ParseTripRequest(BaseModel):
    text: str = Field(min_length=3, max_length=2000)


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
        destinations = {"東京": "NRT", "大阪": "KIX", "福岡": "FUK", "首爾": "ICN", "曼谷": "BKK"}
        destination = next((code for word, code in destinations.items() if word in text), None)
        if destination is None and len(iata_codes) > 1:
            destination = iata_codes[1]
        region = "Japan" if any(word in text for word in ("日本", "東京", "大阪", "福岡")) else None
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
            code
            for words, code in (
                (["美食", "吃"], "food"),
                (["購物", "逛街"], "shopping"),
                (["文化", "博物館"], "culture"),
                (["自然", "登山"], "nature"),
            )
            if any(word in text for word in words)
        ]
        rating_match = re.search(r"(?:至少|最低)?\s*([1-5])\s*星", text)
        chinese_rating = next(
            (value for label, value in {"三星": 3, "四星": 4, "五星": 5}.items() if label in text),
            None,
        )
        rooms_match = re.search(r"(\d+)\s*間房", text)
        missing = []
        if origin is None:
            missing.append("origin")
        if destination is None and region is None:
            missing.append("destination")
        if departure_month is None:
            missing.append("departure_date")
        confidence = max(0.45, 1 - len(missing) * 0.15)
        return ParsedTripRequest(
            origin=origin,
            destination=destination,
            destination_region=region,
            departure_month=departure_month,
            departure_date=iso_dates[0] if iso_dates else None,
            return_date=iso_dates[1] if len(iso_dates) > 1 else None,
            travelers=ParsedTravelers(
                adults=adults,
                rooms=int(rooms_match.group(1)) if rooms_match else 1,
            ),
            trip_length_days=int(days_match.group(1)) if days_match else None,
            budget_twd=budget,
            interests=interests,
            avoid_red_eye=any(word in text for word in ("不要紅眼", "避免紅眼", "非紅眼")),
            hotel_min_rating=int(rating_match.group(1)) if rating_match else chinese_rating,
            confidence=confidence,
            missing_fields=missing,
        )
