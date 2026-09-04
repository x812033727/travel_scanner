from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from ortools.sat.python import cp_model
from pydantic import BaseModel, Field

from app.optimization.hotel_filters import filter_hotels_with_relaxation
from app.pricing.engine import TotalCost, TotalCostEngine
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, TransportOffer
from app.search.schemas import SearchCreate
from app.trips.itinerary import ItineraryDay, ItineraryFood, ItineraryHotspot, build_itinerary

WEIGHTS = {
    "balanced": {"price": 0.35, "time": 0.20, "convenience": 0.20, "quality": 0.15, "risk": 0.10},
    "comfortable": {
        "price": 0.15,
        "time": 0.25,
        "convenience": 0.25,
        "quality": 0.25,
        "risk": 0.10,
    },
}

INTEREST_LABELS = {
    "food": "美食",
    "shopping": "購物",
    "culture": "文化",
    "nature": "自然",
    "family": "親子",
    "nightlife": "夜生活",
    "spa": "溫泉／SPA",
    "beach": "海灘／跳島",
    "deep_travel": "深度旅遊",
}

INTEREST_KEYWORDS = {
    "food": ("food", "market", "restaurant", "dining", "cooking", "美食", "市場", "料理"),
    "shopping": ("shopping", "mall", "outlet", "shop", "購物", "商場", "選物"),
    "culture": ("culture", "museum", "temple", "palace", "heritage", "文化", "博物館", "寺"),
    "nature": ("nature", "park", "garden", "mountain", "hiking", "自然", "公園", "山", "步道"),
    "family": ("family", "kids", "aquarium", "zoo", "親子", "兒童", "水族館", "動物園"),
    "nightlife": ("nightlife", "night", "bar", "pub", "夜生活", "夜景", "酒吧", "夜市"),
    "spa": ("spa", "massage", "onsen", "hot spring", "溫泉", "按摩", "水療", "汗蒸"),
    "beach": ("beach", "island", "snorkel", "diving", "coast", "海灘", "海島", "跳島", "海岸"),
}


def activity_interest_score(activity: ActivityOffer, interests: list[str]) -> int:
    """Score a provider activity without claiming a category the provider did not supply."""
    if not interests:
        return 0
    category = activity.category.casefold()
    text = " ".join(
        value for value in (activity.title, activity.description or "", activity.category) if value
    ).casefold()
    return max(
        (
            (100 if category == interest.casefold() else 0)
            + sum(
                1 for keyword in INTEREST_KEYWORDS.get(interest, ()) if keyword.casefold() in text
            )
            for interest in interests
        ),
        default=0,
    )


@dataclass(frozen=True)
class Candidate:
    flight: FlightOffer | None = None
    hotel: HotelOffer | None = None
    activity: ActivityOffer | None = None
    transport: TransportOffer | None = None
    cost: TotalCost | None = None
    score: float = 0

    @property
    def key(self) -> str:
        return ":".join(
            str(item.id)
            for item in (self.flight, self.hotel, self.activity, self.transport)
            if item
        )


class OptimizationScore(BaseModel):
    total: float
    price: float
    time: float
    convenience: float
    quality: float
    risk: float
    solver: str


class TripPlanResult(BaseModel):
    id: UUID
    mode: str
    title: str
    duplicate: bool = False
    total_cost: TotalCost
    flight: FlightOffer | None
    hotel: HotelOffer | None
    activity: ActivityOffer | None
    transport: TransportOffer | None
    score: OptimizationScore
    pros: list[str]
    cons: list[str]
    compared_with_cheapest: dict[str, Any]
    itinerary: list[ItineraryDay] = Field(default_factory=list)


def pareto(candidates: list[Candidate]) -> list[Candidate]:
    result: list[Candidate] = []
    for candidate in candidates:
        if candidate.cost is None:
            continue
        price = candidate.cost.total_cost
        duration = candidate.flight.duration_minutes if candidate.flight else 0
        dominated = any(
            other.cost
            and other.cost.total_cost <= price
            and (other.flight.duration_minutes if other.flight else 0) <= duration
            and (
                other.cost.total_cost < price
                or (other.flight.duration_minutes if other.flight else 0) < duration
            )
            for other in candidates
        )
        if not dominated:
            result.append(candidate)
    return result or candidates


class TripOptimizer:
    def __init__(self) -> None:
        self.cost_engine = TotalCostEngine()
        self.relaxed_hotel_preferences: list[str] = []

    def _filter_hotels(self, query: SearchCreate, hotels: list[HotelOffer]) -> list[HotelOffer]:
        result = filter_hotels_with_relaxation(
            query.preferences, query.travelers.adults + query.travelers.children, hotels
        )
        self.relaxed_hotel_preferences = [constraint.label for constraint in result.relaxed]
        return result.matches

    def _candidates(
        self,
        query: SearchCreate,
        flights: list[FlightOffer],
        hotels: list[HotelOffer],
        activities: list[ActivityOffer],
        transports: list[TransportOffer],
    ) -> list[Candidate]:
        if query.preferences.avoid_red_eye:
            flights = [item for item in flights if 6 <= item.departure_time.hour < 23]
        hotels = self._filter_hotels(query, hotels)
        if query.preferences.interests:
            interest_matches = [
                item
                for item in activities
                if activity_interest_score(item, query.preferences.interests) > 0
            ]
            if interest_matches:
                activities = interest_matches
        flights = sorted(flights, key=lambda x: x.total_price)[:6] or [None]  # type: ignore[list-item]
        hotels = sorted(hotels, key=lambda x: x.total_price)[:6] or [None]  # type: ignore[list-item]
        activities = sorted(
            activities,
            key=lambda x: (-activity_interest_score(x, query.preferences.interests), x.price),
        )[:4] or [None]  # type: ignore[list-item]
        transports = sorted(transports, key=lambda x: x.price)[:4] or [None]  # type: ignore[list-item]
        beam = [Candidate(flight=item) for item in flights]

        def score_and_cap(expanded: list[Candidate]) -> list[Candidate]:
            for index, candidate in enumerate(expanded):
                cost = self.cost_engine.calculate(
                    candidate.flight,
                    candidate.hotel,
                    candidate.activity,
                    candidate.transport,
                    query.travelers.adults + query.travelers.children,
                )
                expanded[index] = replace(candidate, cost=cost)
            return sorted(
                expanded, key=lambda x: x.cost.total_cost if x.cost else Decimal("Infinity")
            )[:40]

        beam = score_and_cap(
            [replace(candidate, hotel=offer) for candidate in beam for offer in hotels]
        )
        beam = score_and_cap(
            [replace(candidate, activity=offer) for candidate in beam for offer in activities]
        )
        beam = score_and_cap(
            [replace(candidate, transport=offer) for candidate in beam for offer in transports]
        )
        budget = query.preferences.budget_twd
        feasible = [
            item
            for item in beam
            if item.cost and (budget is None or item.cost.total_cost <= budget)
        ]
        return pareto(feasible or beam)

    def _metrics(self, candidate: Candidate, candidates: list[Candidate]) -> dict[str, float]:
        prices = [float(item.cost.total_cost) for item in candidates if item.cost]
        durations = [
            float(item.flight.duration_minutes if item.flight else 0) for item in candidates
        ]

        def inverse(value: float, values: list[float]) -> float:
            low, high = min(values), max(values)
            return 100 if high == low else 100 * (high - value) / (high - low)

        flight, hotel, transport = candidate.flight, candidate.hotel, candidate.transport
        convenience = (
            (transport.convenience_score if transport else 65)
            + (100 - min(100, (hotel.station_walk_minutes if hotel else 15) * 6))
        ) / 2
        quality = (hotel.rating / 5 * 100) if hotel else 60
        risk = (
            50
            + (20 if flight and flight.refundable else 0)
            + (15 if hotel and hotel.refundable else 0)
            + (15 if flight and flight.changeable else 0)
        )
        return {
            "price": inverse(float(candidate.cost.total_cost if candidate.cost else 0), prices),
            "time": inverse(float(flight.duration_minutes if flight else 0), durations),
            "convenience": convenience,
            "quality": quality,
            "risk": min(100, risk),
        }

    def _select(
        self, candidates: list[Candidate], profile: str
    ) -> tuple[Candidate, dict[str, float], str]:
        scored: list[tuple[Candidate, dict[str, float], int]] = []
        for candidate in candidates:
            metrics = self._metrics(candidate, candidates)
            score = int(
                sum(metrics[key] * weight for key, weight in WEIGHTS[profile].items()) * 1000
            )
            scored.append((candidate, metrics, score))
        model = cp_model.CpModel()
        choices = [model.new_bool_var(f"candidate_{index}") for index in range(len(scored))]
        model.add_exactly_one(choices)
        model.maximize(sum(choices[index] * row[2] for index, row in enumerate(scored)))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 0.5
        status = solver.solve(model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            index = next(index for index, choice in enumerate(choices) if solver.value(choice))
            return scored[index][0], scored[index][1], "or-tools-cp-sat"
        best = max(scored, key=lambda row: row[2])
        return best[0], best[1], "beam-fallback"

    def optimize(
        self,
        query: SearchCreate,
        flights: list[FlightOffer],
        hotels: list[HotelOffer],
        activities: list[ActivityOffer],
        transports: list[TransportOffer],
        hotspots: list[ItineraryHotspot] | None = None,
        foods: list[ItineraryFood] | None = None,
    ) -> list[TripPlanResult]:
        candidates = self._candidates(query, flights, hotels, activities, transports)
        if not candidates:
            return []
        cheapest = min(
            candidates, key=lambda item: item.cost.total_cost if item.cost else Decimal("Infinity")
        )
        selections: list[tuple[str, Candidate, dict[str, float], str]] = [
            ("cheapest", cheapest, self._metrics(cheapest, candidates), "minimum-total-cost")
        ]
        for profile in ("balanced", "comfortable"):
            candidate, metrics, solver = self._select(candidates, profile)
            selections.append((profile, candidate, metrics, solver))
        cheapest_price = cheapest.cost.total_cost if cheapest.cost else Decimal(0)
        titles = {"cheapest": "最便宜", "balanced": "整體最佳", "comfortable": "更舒適"}
        results: list[TripPlanResult] = []
        seen: set[str] = set()
        for mode, candidate, metrics, solver in selections:
            duplicate = candidate.key in seen
            seen.add(candidate.key)
            total = sum(
                metrics[key] * (WEIGHTS.get(mode, WEIGHTS["balanced"]).get(key, 0.2))
                for key in metrics
            )
            price = candidate.cost.total_cost if candidate.cost else Decimal(0)
            time_saved = (cheapest.flight.duration_minutes if cheapest.flight else 0) - (
                candidate.flight.duration_minutes if candidate.flight else 0
            )
            pros = []
            cons = []
            if candidate.flight and 6 <= candidate.flight.departure_time.hour < 23:
                pros.append("航班不是紅眼時段")
            if candidate.hotel and candidate.hotel.station_walk_minutes <= 6:
                pros.append(f"飯店步行約 {candidate.hotel.station_walk_minutes} 分鐘到車站")
            if candidate.hotel and candidate.hotel.breakfast_included:
                pros.append("住宿方案包含早餐")
            if candidate.hotel and candidate.hotel.refundable:
                pros.append("住宿方案可退款")
            if candidate.activity:
                matched_interests = [
                    interest
                    for interest in query.preferences.interests
                    if activity_interest_score(candidate.activity, [interest]) > 0
                ]
                if matched_interests:
                    labels = "、".join(
                        INTEREST_LABELS.get(interest, interest) for interest in matched_interests
                    )
                    pros.append(f"活動符合{labels}偏好")
            if time_saved > 0:
                pros.append(f"比最便宜方案少 {time_saved} 分鐘飛行時間")
            if query.preferences.budget_twd is not None:
                budget = Decimal(query.preferences.budget_twd)
                if price <= budget:
                    pros.append(f"符合總預算，尚餘 NT${int(budget - price):,}")
                else:
                    cons.append(f"超出總預算 NT${int(price - budget):,}")
            if price > cheapest_price:
                cons.append(f"比最便宜方案多 NT${int(price - cheapest_price):,}")
            if duplicate:
                cons.append("目前符合條件的候選較少，與其他方案使用相同組合")
            if self.relaxed_hotel_preferences:
                cons.append("住宿候選不足，已放寬：" + "、".join(self.relaxed_hotel_preferences))
            if candidate.hotel is None:
                cons.append("沒有住宿符合所有必要條件，請調整住宿篩選")
            results.append(
                TripPlanResult(
                    id=uuid5(NAMESPACE_URL, f"{candidate.key}:{mode}"),
                    mode=mode,
                    title=titles[mode],
                    duplicate=duplicate,
                    total_cost=candidate.cost,
                    flight=candidate.flight,
                    hotel=candidate.hotel,
                    activity=candidate.activity,
                    transport=candidate.transport,
                    score=OptimizationScore(
                        total=round(total, 2),
                        solver=solver,
                        **{key: round(value, 2) for key, value in metrics.items()},
                    ),
                    pros=pros or ["總成本符合目前條件"],
                    cons=cons or ["價格與時間差異不明顯"],
                    compared_with_cheapest={
                        "price_difference": price - cheapest_price,
                        "flight_minutes_saved": time_saved,
                    },
                    itinerary=build_itinerary(
                        query,
                        candidate.flight,
                        candidate.hotel,
                        candidate.activity,
                        candidate.transport,
                        hotspots,
                        foods,
                    ),
                )
            )
        return [results[1], results[0], results[2]]
