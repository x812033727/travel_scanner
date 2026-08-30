from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from ortools.sat.python import cp_model
from pydantic import BaseModel

from app.pricing.engine import TotalCost, TotalCostEngine
from app.providers.schemas import ActivityOffer, FlightOffer, HotelOffer, TransportOffer
from app.search.schemas import SearchCreate

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
        if query.preferences.hotel_min_rating:
            hotels = [item for item in hotels if item.rating >= query.preferences.hotel_min_rating]
        flights = sorted(flights, key=lambda x: x.total_price)[:6] or [None]  # type: ignore[list-item]
        hotels = sorted(hotels, key=lambda x: x.total_price)[:6] or [None]  # type: ignore[list-item]
        activities = sorted(activities, key=lambda x: x.price)[:4] or [None]  # type: ignore[list-item]
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
            if time_saved > 0:
                pros.append(f"比最便宜方案少 {time_saved} 分鐘飛行時間")
            if price > cheapest_price:
                cons.append(f"比最便宜方案多 NT${int(price - cheapest_price):,}")
            if duplicate:
                cons.append("目前符合條件的候選較少，與其他方案使用相同組合")
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
                )
            )
        return [results[1], results[0], results[2]]
