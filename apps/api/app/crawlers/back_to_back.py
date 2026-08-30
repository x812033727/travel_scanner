import asyncio
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from itertools import product

import httpx
from redis.asyncio import Redis

from app.config import Settings
from app.crawlers.airlines import (
    ADAPTERS,
    AirlineFareCrawlerService,
    CrawlerError,
    CrawlerPolicyError,
    FetchResult,
    PublicFareAdapter,
)
from app.crawlers.fx import FxRateProvider
from app.crawlers.schemas import (
    AirlineCrawlerSource,
    AirlineFareSearch,
    BackToBackComparison,
    BackToBackFareSearch,
    BackToBackFareSearchResponse,
    BackToBackPricingCapability,
    BackToBackStrategy,
    ComparisonMode,
    ComparisonVerdict,
    FareCandidateSet,
    FareStrategyTotal,
    FareTicketComponent,
    FareTicketRole,
    FxRateSnapshot,
    PublicFareQuote,
    SourceState,
    SupplementalFareComponent,
    SupplementalFareInput,
    SupplementalFareRole,
    SupplementalFareSegment,
)

TWD_QUANTUM = Decimal("1")
PERCENT_QUANTUM = Decimal("0.1")

FARE_ROLE_LABELS = {
    FareTicketRole.CONVENTIONAL_FIRST: "第一趟一般票",
    FareTicketRole.CONVENTIONAL_SECOND: "第二趟一般票",
    FareTicketRole.WRAPPER: "台灣始發包覆票",
    FareTicketRole.REVERSE: "外站始發倒買票",
}


@dataclass(frozen=True)
class AirlineCandidateResult:
    candidates: dict[FareTicketRole, list[PublicFareQuote]]
    source: AirlineCrawlerSource
    warnings: list[str]


@dataclass(frozen=True)
class PriceOption:
    estimated_twd: Decimal
    airline_code: str | None
    currency: str
    amount: Decimal
    identity: str
    ticket: FareTicketComponent | None = None
    supplemental: SupplementalFareComponent | None = None


def build_fare_queries(query: BackToBackFareSearch) -> dict[FareTicketRole, AirlineFareSearch]:
    common = {
        "flex_days": query.flex_days,
        "cabin_class": query.cabin_class,
        "airlines": query.airlines,
        "limit_per_airline": query.limit_per_airline,
    }
    queries = {
        FareTicketRole.CONVENTIONAL_FIRST: AirlineFareSearch(
            origin=query.origin,
            destination=query.first_destination,
            departure_date=query.first_trip.departure_date,
            return_date=query.first_trip.return_date,
            **common,
        ),
        FareTicketRole.CONVENTIONAL_SECOND: AirlineFareSearch(
            origin=query.origin,
            destination=query.second_destination,
            departure_date=query.second_trip.departure_date,
            return_date=query.second_trip.return_date,
            **common,
        ),
    }
    if query.first_destination == query.second_destination:
        if query.strategy == BackToBackStrategy.NESTED_ROUND_TRIPS:
            queries[FareTicketRole.WRAPPER] = AirlineFareSearch(
                origin=query.origin,
                destination=query.first_destination,
                departure_date=query.first_trip.departure_date,
                return_date=query.second_trip.return_date,
                **common,
            )
        queries[FareTicketRole.REVERSE] = AirlineFareSearch(
            origin=query.first_destination,
            destination=query.origin,
            departure_date=query.first_trip.return_date,
            return_date=query.second_trip.departure_date,
            **common,
        )
    return queries


def _empty_candidates() -> dict[FareTicketRole, list[PublicFareQuote]]:
    return {role: [] for role in FareTicketRole}


class BackToBackFareService:
    def __init__(
        self,
        settings: Settings,
        redis: Redis,
        *,
        crawler: AirlineFareCrawlerService | None = None,
        fx_provider: FxRateProvider | None = None,
    ) -> None:
        self.settings = settings
        self.crawler = crawler or AirlineFareCrawlerService(settings, redis)
        self.fx_provider = fx_provider or FxRateProvider(settings, redis)

    async def _paced_fetch(self, client: httpx.AsyncClient, url: str) -> FetchResult:
        for attempt in range(2):
            try:
                return await self.crawler.fetcher.fetch(client, url)
            except CrawlerError as exc:
                if exc.code != "source_throttled" or attempt > 0:
                    raise
                await asyncio.sleep(self.settings.airline_crawler_min_interval_seconds + 0.05)
        raise AssertionError("unreachable")

    async def _search_airline(
        self,
        client: httpx.AsyncClient,
        adapter: PublicFareAdapter,
        queries: dict[FareTicketRole, AirlineFareSearch],
    ) -> AirlineCandidateResult:
        candidates = _empty_candidates()
        if not adapter.enabled:
            return AirlineCandidateResult(
                candidates=candidates,
                source=AirlineCrawlerSource(
                    airline_code=adapter.code,
                    airline_name=adapter.name,
                    host=adapter.host,
                    state=SourceState.DISABLED,
                    policy="runtime_robots_check_fail_closed",
                    detail=adapter.disabled_reason,
                ),
                warnings=[f"{adapter.name}：{adapter.disabled_reason}"],
            )

        full_back_to_back = FareTicketRole.REVERSE in queries
        page_specs: list[tuple[str, str, tuple[FareTicketRole, ...]]]
        try:
            if full_back_to_back:
                page_specs = [
                    (
                        "台灣始發",
                        adapter.fare_url(queries[FareTicketRole.CONVENTIONAL_FIRST]),
                        tuple(
                            role
                            for role in (
                                FareTicketRole.CONVENTIONAL_FIRST,
                                FareTicketRole.CONVENTIONAL_SECOND,
                                FareTicketRole.WRAPPER,
                            )
                            if role in queries
                        ),
                    ),
                    (
                        "外站始發",
                        adapter.fare_url(queries[FareTicketRole.REVERSE]),
                        (FareTicketRole.REVERSE,),
                    ),
                ]
            else:
                page_specs = [
                    (
                        "第一次旅行台灣始發",
                        adapter.fare_url(queries[FareTicketRole.CONVENTIONAL_FIRST]),
                        (FareTicketRole.CONVENTIONAL_FIRST,),
                    ),
                    (
                        "第二次旅行台灣始發",
                        adapter.fare_url(queries[FareTicketRole.CONVENTIONAL_SECOND]),
                        (FareTicketRole.CONVENTIONAL_SECOND,),
                    ),
                ]
        except CrawlerError as exc:
            return AirlineCandidateResult(
                candidates=candidates,
                source=AirlineCrawlerSource(
                    airline_code=adapter.code,
                    airline_name=adapter.name,
                    host=adapter.host,
                    state=SourceState.FAILED,
                    policy="allowlisted_routes_only",
                    detail=exc.detail,
                ),
                warnings=[f"{adapter.name}：{exc.detail}"],
            )
        warnings: list[str] = []
        cache_hits: list[bool] = []
        successful_pages = 0
        policy_failure = False

        for page_label, source_url, roles in page_specs:
            try:
                fetched = await self._paced_fetch(client, source_url)
                cache_hits.append(fetched.cache_hit)
                successful_pages += 1
                for role in roles:
                    candidates[role] = adapter.parse(
                        fetched.content,
                        source_url,
                        queries[role],
                    )
                    if not candidates[role]:
                        unfiltered_query = queries[role].model_copy(
                            update={
                                "departure_date": None,
                                "return_date": None,
                                "limit_per_airline": 30,
                            }
                        )
                        available = adapter.parse(
                            fetched.content,
                            source_url,
                            unfiltered_query,
                        )
                        nearest_detail = ""
                        requested = queries[role]
                        if available and requested.departure_date:
                            target_departure = requested.departure_date
                            target_return = requested.return_date
                            nearest = min(
                                available,
                                key=lambda quote: (
                                    abs((quote.departure_date - target_departure).days)
                                    + (
                                        abs((quote.return_date - target_return).days)
                                        if quote.return_date and target_return
                                        else 0
                                    ),
                                    quote.total_price,
                                    quote.departure_date,
                                ),
                            )
                            nearest_detail = (
                                f"；公開頁最接近的是 {nearest.departure_date.isoformat()}"
                                f"–{
                                    (
                                        nearest.return_date.isoformat()
                                        if nearest.return_date
                                        else '單程'
                                    )
                                }"
                            )
                        warnings.append(
                            f"{adapter.name}：{FARE_ROLE_LABELS[role]}在指定日期前後 "
                            f"{queries[role].flex_days} 天內沒有公開快取票價{nearest_detail}"
                        )
            except CrawlerPolicyError as exc:
                policy_failure = True
                warnings.append(f"{adapter.name} {page_label}：{exc.detail}")
            except CrawlerError as exc:
                warnings.append(f"{adapter.name} {page_label}：{exc.detail}")

        quote_count = sum(len(quotes) for quotes in candidates.values())
        if successful_pages == len(page_specs):
            state = SourceState.SUCCESS
            detail = (
                "讀取台灣始發與外站始發公開近期票價成功"
                if full_back_to_back
                else "讀取兩次旅行的台灣始發公開近期票價成功"
            )
        elif successful_pages:
            state = SourceState.BLOCKED if policy_failure else SourceState.FAILED
            detail = "只取得部分方向的公開近期票價"
        else:
            state = SourceState.BLOCKED if policy_failure else SourceState.FAILED
            detail = (
                "台灣始發與外站始發公開票價皆無法取得"
                if full_back_to_back
                else "兩次旅行的台灣始發公開票價皆無法取得"
            )
        return AirlineCandidateResult(
            candidates=candidates,
            source=AirlineCrawlerSource(
                airline_code=adapter.code,
                airline_name=adapter.name,
                host=adapter.host,
                state=state,
                policy="robots_allowed" if successful_pages == 2 else "fail_closed_partial",
                detail=detail,
                quote_count=quote_count,
                cache_hit=bool(cache_hits) and all(cache_hits),
            ),
            warnings=warnings,
        )

    @staticmethod
    def _timeline_is_valid(
        first: PublicFareQuote,
        second: PublicFareQuote,
        *,
        back_to_back: bool,
    ) -> bool:
        if first.return_date is None or second.return_date is None:
            return False
        if back_to_back:
            dates = (
                first.departure_date,
                second.departure_date,
                second.return_date,
                first.return_date,
            )
        else:
            dates = (
                first.departure_date,
                first.return_date,
                second.departure_date,
                second.return_date,
            )
        return all(left < right for left, right in zip(dates, dates[1:], strict=False))

    @staticmethod
    def _ticket_component(
        role: FareTicketRole,
        quote: PublicFareQuote,
        rates: dict[str, FxRateSnapshot],
    ) -> FareTicketComponent:
        rate = rates.get(quote.currency)
        estimated = None
        if rate is not None:
            estimated = (quote.total_price * rate.rate).quantize(
                TWD_QUANTUM, rounding=ROUND_HALF_UP
            )
        return FareTicketComponent(
            role=role,
            quote=quote,
            estimated_twd=estimated,
            fx_rate=rate,
        )

    @classmethod
    def _best_strategy(
        cls,
        first_role: FareTicketRole,
        second_role: FareTicketRole,
        candidates: dict[FareTicketRole, list[PublicFareQuote]],
        rates: dict[str, FxRateSnapshot],
        *,
        same_airline: bool,
        back_to_back: bool,
    ) -> FareStrategyTotal | None:
        choices: list[tuple[Decimal, str, str, FareTicketComponent, FareTicketComponent]] = []
        for first, second in product(candidates[first_role], candidates[second_role]):
            if same_airline and first.airline_code != second.airline_code:
                continue
            if not cls._timeline_is_valid(first, second, back_to_back=back_to_back):
                continue
            first_ticket = cls._ticket_component(first_role, first, rates)
            second_ticket = cls._ticket_component(second_role, second, rates)
            if first_ticket.estimated_twd is None or second_ticket.estimated_twd is None:
                continue
            total = first_ticket.estimated_twd + second_ticket.estimated_twd
            choices.append(
                (
                    total,
                    first.airline_code.value,
                    second.airline_code.value,
                    first_ticket,
                    second_ticket,
                )
            )
        if not choices:
            return None
        total, _, _, first_ticket, second_ticket = min(
            choices,
            key=lambda item: (
                item[0],
                item[1],
                item[2],
                str(item[3].quote.id),
                str(item[4].quote.id),
            ),
        )
        original_totals: dict[str, Decimal] = {}
        for ticket in (first_ticket, second_ticket):
            currency = ticket.quote.currency
            original_totals[currency] = original_totals.get(currency, Decimal("0")) + (
                ticket.quote.total_price
            )
        return FareStrategyTotal(
            tickets=[first_ticket, second_ticket],
            original_currency_totals=original_totals,
            estimated_twd=total,
        )

    @classmethod
    def _supplemental_component(
        cls,
        role: SupplementalFareRole,
        fare: SupplementalFareInput,
        *,
        origin: str,
        destination: str,
        departure_date: date,
        rates: dict[str, FxRateSnapshot],
        segments: list[SupplementalFareSegment] | None = None,
    ) -> SupplementalFareComponent:
        rate = rates.get(fare.currency)
        estimated = None
        if rate is not None:
            estimated = (fare.amount * rate.rate).quantize(TWD_QUANTUM, rounding=ROUND_HALF_UP)
        return SupplementalFareComponent(
            role=role,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            amount=fare.amount,
            currency=fare.currency,
            airline_code=fare.airline_code,
            segments=segments
            or [
                SupplementalFareSegment(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                )
            ],
            estimated_twd=estimated,
            fx_rate=rate,
        )

    @classmethod
    def _manual_conventional_component(
        cls,
        query: BackToBackFareSearch,
        *,
        first_trip: bool,
        rates: dict[str, FxRateSnapshot],
    ) -> SupplementalFareComponent | None:
        fare = query.conventional_first_fare if first_trip else query.conventional_second_fare
        if fare is None:
            return None
        trip = query.first_trip if first_trip else query.second_trip
        destination = query.first_destination if first_trip else query.second_destination
        role = (
            SupplementalFareRole.CONVENTIONAL_FIRST_MANUAL
            if first_trip
            else SupplementalFareRole.CONVENTIONAL_SECOND_MANUAL
        )
        return cls._supplemental_component(
            role,
            fare,
            origin=query.origin,
            destination=destination,
            departure_date=trip.departure_date,
            rates=rates,
            segments=[
                SupplementalFareSegment(
                    origin=query.origin,
                    destination=destination,
                    departure_date=trip.departure_date,
                ),
                SupplementalFareSegment(
                    origin=destination,
                    destination=query.origin,
                    departure_date=trip.return_date,
                ),
            ],
        )

    @staticmethod
    def _ticket_option(ticket: FareTicketComponent) -> PriceOption | None:
        if ticket.estimated_twd is None:
            return None
        return PriceOption(
            estimated_twd=ticket.estimated_twd,
            airline_code=ticket.quote.airline_code.value,
            currency=ticket.quote.currency,
            amount=ticket.quote.total_price,
            identity=str(ticket.quote.id),
            ticket=ticket,
        )

    @staticmethod
    def _supplemental_option(component: SupplementalFareComponent) -> PriceOption | None:
        if component.estimated_twd is None:
            return None
        return PriceOption(
            estimated_twd=component.estimated_twd,
            airline_code=(component.airline_code.value if component.airline_code else None),
            currency=component.currency,
            amount=component.amount,
            identity=f"manual:{component.role.value}:{component.airline_code or 'other'}",
            supplemental=component,
        )

    @classmethod
    def _best_conventional_with_manual(
        cls,
        query: BackToBackFareSearch,
        candidates: dict[FareTicketRole, list[PublicFareQuote]],
        rates: dict[str, FxRateSnapshot],
        *,
        same_airline: bool,
    ) -> FareStrategyTotal | None:
        option_groups: list[list[PriceOption]] = []
        for role, first_trip in (
            (FareTicketRole.CONVENTIONAL_FIRST, True),
            (FareTicketRole.CONVENTIONAL_SECOND, False),
        ):
            options = [
                option
                for quote in candidates[role]
                if (option := cls._ticket_option(cls._ticket_component(role, quote, rates)))
                is not None
            ]
            manual = cls._manual_conventional_component(
                query,
                first_trip=first_trip,
                rates=rates,
            )
            if manual is not None:
                manual_option = cls._supplemental_option(manual)
                if manual_option is not None:
                    options.append(manual_option)
            option_groups.append(options)

        choices: list[tuple[Decimal, str, str, PriceOption, PriceOption]] = []
        for first, second in product(*option_groups):
            if same_airline and (
                first.airline_code is None
                or second.airline_code is None
                or first.airline_code != second.airline_code
            ):
                continue
            choices.append(
                (
                    first.estimated_twd + second.estimated_twd,
                    first.airline_code or "ZZ",
                    second.airline_code or "ZZ",
                    first,
                    second,
                )
            )
        if not choices:
            return None
        total, _, _, first, second = min(
            choices,
            key=lambda item: (item[0], item[1], item[2], item[3].identity, item[4].identity),
        )
        original_totals: dict[str, Decimal] = {}
        tickets: list[FareTicketComponent] = []
        supplemental: list[SupplementalFareComponent] = []
        for option in (first, second):
            original_totals[option.currency] = (
                original_totals.get(option.currency, Decimal(0)) + option.amount
            )
            if option.ticket is not None:
                tickets.append(option.ticket)
            if option.supplemental is not None:
                supplemental.append(option.supplemental)
        return FareStrategyTotal(
            tickets=tickets,
            supplemental_fares=supplemental,
            original_currency_totals=original_totals,
            estimated_twd=total,
        )

    @classmethod
    def _best_reverse_two_segment(
        cls,
        query: BackToBackFareSearch,
        candidates: dict[FareTicketRole, list[PublicFareQuote]],
        rates: dict[str, FxRateSnapshot],
        *,
        same_airline: bool,
    ) -> FareStrategyTotal | None:
        head = query.head_one_way_fare
        tail = query.tail_one_way_fare
        if head is None or tail is None:
            return None
        head_ticket = cls._supplemental_component(
            SupplementalFareRole.HEAD_ONE_WAY,
            head,
            origin=query.origin,
            destination=query.first_destination,
            departure_date=query.first_trip.departure_date,
            rates=rates,
        )
        tail_ticket = cls._supplemental_component(
            SupplementalFareRole.TAIL_ONE_WAY,
            tail,
            origin=query.second_destination,
            destination=query.origin,
            departure_date=query.second_trip.return_date,
            rates=rates,
        )
        middle_options: list[PriceOption] = []
        for reverse in candidates[FareTicketRole.REVERSE]:
            if reverse.return_date is None or reverse.departure_date >= reverse.return_date:
                continue
            reverse_ticket = cls._ticket_component(FareTicketRole.REVERSE, reverse, rates)
            option = cls._ticket_option(reverse_ticket)
            if option is not None:
                middle_options.append(option)

        if query.middle_two_segment_fare is not None:
            middle_component = cls._supplemental_component(
                SupplementalFareRole.MIDDLE_TWO_SEGMENT,
                query.middle_two_segment_fare,
                origin=query.first_destination,
                destination=query.second_destination,
                departure_date=query.first_trip.return_date,
                rates=rates,
                segments=[
                    SupplementalFareSegment(
                        origin=query.first_destination,
                        destination=query.origin,
                        departure_date=query.first_trip.return_date,
                    ),
                    SupplementalFareSegment(
                        origin=query.origin,
                        destination=query.second_destination,
                        departure_date=query.second_trip.departure_date,
                    ),
                ],
            )
            middle_option = cls._supplemental_option(middle_component)
            if middle_option is not None:
                middle_options.append(middle_option)

        choices: list[
            tuple[
                Decimal,
                str,
                PriceOption,
            ]
        ] = []
        for middle_option in middle_options:
            if same_airline and (
                head.airline_code is None
                or tail.airline_code is None
                or middle_option.airline_code is None
                or head.airline_code.value != middle_option.airline_code
                or tail.airline_code.value != middle_option.airline_code
            ):
                continue
            estimated_parts = (
                middle_option.estimated_twd,
                head_ticket.estimated_twd,
                tail_ticket.estimated_twd,
            )
            if any(value is None for value in estimated_parts):
                continue
            total = sum((value for value in estimated_parts if value is not None), Decimal(0))
            choices.append(
                (
                    total,
                    middle_option.airline_code or "ZZ",
                    middle_option,
                )
            )
        if not choices:
            return None
        total, _, best_middle = min(
            choices,
            key=lambda item: (item[0], item[1], item[2].identity),
        )
        original_totals: dict[str, Decimal] = {}
        for currency, amount in (
            (best_middle.currency, best_middle.amount),
            (head_ticket.currency, head_ticket.amount),
            (tail_ticket.currency, tail_ticket.amount),
        ):
            original_totals[currency] = original_totals.get(currency, Decimal(0)) + amount
        return FareStrategyTotal(
            tickets=[best_middle.ticket] if best_middle.ticket is not None else [],
            supplemental_fares=[
                head_ticket,
                *(
                    [best_middle.supplemental]
                    if best_middle.supplemental is not None
                    else []
                ),
                tail_ticket,
            ],
            original_currency_totals=original_totals,
            estimated_twd=total,
        )

    @staticmethod
    def _comparison(
        mode: ComparisonMode,
        conventional: FareStrategyTotal | None,
        back_to_back: FareStrategyTotal | None,
        *,
        unavailable_detail: str | None = None,
        alternative_label: str = "倒買法",
    ) -> BackToBackComparison:
        label = "混搭航空公司" if mode == ComparisonMode.MIXED_AIRLINES else "同航空公司"
        if (
            conventional is None
            or back_to_back is None
            or conventional.estimated_twd is None
            or back_to_back.estimated_twd is None
        ):
            return BackToBackComparison(
                mode=mode,
                conventional=conventional,
                back_to_back=back_to_back,
                verdict=ComparisonVerdict.COMPARISON_UNAVAILABLE,
                detail=unavailable_detail or f"{label}缺少完整票價或換算匯率，暫時無法比較。",
            )

        savings = conventional.estimated_twd - back_to_back.estimated_twd
        percent = None
        if conventional.estimated_twd > 0:
            percent = (savings / conventional.estimated_twd * Decimal("100")).quantize(
                PERCENT_QUANTUM, rounding=ROUND_HALF_UP
            )
        if savings > 0:
            verdict = ComparisonVerdict.BACK_TO_BACK_CHEAPER
            detail = f"{label}的{alternative_label}估算較省。"
        elif savings < 0:
            verdict = ComparisonVerdict.CONVENTIONAL_CHEAPER
            detail = f"{label}的一般買法估算較省。"
        else:
            verdict = ComparisonVerdict.SAME_PRICE
            detail = f"{label}兩種買法的估算總價相同。"
        return BackToBackComparison(
            mode=mode,
            conventional=conventional,
            back_to_back=back_to_back,
            savings_twd=savings,
            savings_percent=percent,
            verdict=verdict,
            detail=detail,
        )

    async def search(self, query: BackToBackFareSearch) -> BackToBackFareSearchResponse:
        queries = build_fare_queries(query)
        same_destination = query.first_destination == query.second_destination
        comparison_supported = (
            same_destination or query.strategy == BackToBackStrategy.REVERSE_TWO_SEGMENT
        )
        timeout = httpx.Timeout(self.settings.airline_crawler_timeout_seconds)
        headers = {
            "User-Agent": self.settings.airline_crawler_user_agent,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        }
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            results = await asyncio.gather(
                *(self._search_airline(client, ADAPTERS[code], queries) for code in query.airlines)
            )

        candidates = _empty_candidates()
        warnings: list[str] = []
        for candidate_result in results:
            warnings.extend(candidate_result.warnings)
            for role, quotes in candidate_result.candidates.items():
                candidates[role].extend(quotes)
        for quotes in candidates.values():
            quotes.sort(
                key=lambda quote: (
                    quote.airline_code.value,
                    quote.currency,
                    quote.total_price,
                    quote.departure_date,
                    quote.return_date or date.max,
                    str(quote.id),
                )
            )

        currencies = {quote.currency for quotes in candidates.values() for quote in quotes}
        for manual_fare in (
            query.head_one_way_fare,
            query.middle_two_segment_fare,
            query.tail_one_way_fare,
            query.conventional_first_fare,
            query.conventional_second_fare,
        ):
            if manual_fare is not None:
                currencies.add(manual_fare.currency)
        sorted_currencies = sorted(currencies)
        rate_results = await asyncio.gather(
            *(self.fx_provider.rate_to_twd(currency) for currency in sorted_currencies),
            return_exceptions=True,
        )
        rates: dict[str, FxRateSnapshot] = {}
        for currency, rate_result in zip(sorted_currencies, rate_results, strict=True):
            if isinstance(rate_result, FxRateSnapshot):
                rates[currency] = rate_result
                if rate_result.is_stale:
                    warnings.append(f"{currency} 使用七日內的舊匯率估算 TWD。")
            else:
                warnings.append(f"{currency}：目前無法取得 TWD 估算匯率。")

        comparisons: list[BackToBackComparison] = []
        for mode in (ComparisonMode.MIXED_AIRLINES, ComparisonMode.SAME_AIRLINE):
            same_airline = mode == ComparisonMode.SAME_AIRLINE
            label = "混搭航空公司" if mode == ComparisonMode.MIXED_AIRLINES else "同航空公司"
            conventional = self._best_conventional_with_manual(
                query,
                candidates,
                rates,
                same_airline=same_airline,
            )
            if comparison_supported:
                missing_roles = [
                    FARE_ROLE_LABELS[role]
                    for role, manual_fare in (
                        (
                            FareTicketRole.CONVENTIONAL_FIRST,
                            query.conventional_first_fare,
                        ),
                        (
                            FareTicketRole.CONVENTIONAL_SECOND,
                            query.conventional_second_fare,
                        ),
                    )
                    if not candidates[role] and manual_fare is None
                ]
                if query.strategy == BackToBackStrategy.REVERSE_TWO_SEGMENT:
                    back_to_back = self._best_reverse_two_segment(
                        query,
                        candidates,
                        rates,
                        same_airline=same_airline,
                    )
                    if (
                        not candidates[FareTicketRole.REVERSE]
                        and query.middle_two_segment_fare is None
                    ):
                        missing_roles.append("中段反向兩航段票價")
                    if query.head_one_way_fare is None:
                        missing_roles.append("第一趟去程單程票價")
                    if query.tail_one_way_fare is None:
                        missing_roles.append("第二趟回程單程票價")
                    if (
                        same_airline
                        and any(
                            fare is not None and fare.airline_code is None
                            for fare in (
                                query.head_one_way_fare,
                                query.middle_two_segment_fare,
                                query.tail_one_way_fare,
                                query.conventional_first_fare,
                                query.conventional_second_fare,
                            )
                        )
                    ):
                        missing_roles.append("手動輸入票價的航空公司")
                    alternative_label = "外站兩段票"
                else:
                    back_to_back = self._best_strategy(
                        FareTicketRole.WRAPPER,
                        FareTicketRole.REVERSE,
                        candidates,
                        rates,
                        same_airline=same_airline,
                        back_to_back=True,
                    )
                    missing_roles.extend(
                        FARE_ROLE_LABELS[role]
                        for role in (
                            FareTicketRole.WRAPPER,
                            FareTicketRole.REVERSE,
                        )
                        if not candidates[role]
                    )
                    alternative_label = "包覆倒買"
                if missing_roles:
                    unavailable_detail = (
                        f"{label}缺少{'、'.join(missing_roles)}的公開快取票價，"
                        "因此無法組成完整比較；這不是 0% 節省。"
                    )
                else:
                    unavailable_detail = (
                        f"{label}雖有候選票價，但日期順序、航空公司或匯率無法組成相容的完整方案。"
                    )
                comparisons.append(
                    self._comparison(
                        mode,
                        conventional,
                        back_to_back,
                        unavailable_detail=unavailable_detail,
                        alternative_label=alternative_label,
                    )
                )
            else:
                comparisons.append(
                    BackToBackComparison(
                        mode=mode,
                        conventional=conventional,
                        verdict=ComparisonVerdict.COMPARISON_UNAVAILABLE,
                        detail=(
                            f"{label}已計算兩張一般來回票；兩次目的地不同時，"
                            "倒買法需要兩張開口票。現有公開票價頁沒有開口票價格，"
                            "因此不估算倒買總價。"
                        ),
                    )
                )

        if not comparison_supported:
            warnings.insert(
                0,
                "兩次目的地不同：完整倒買比較需要開口票票價來源；目前只顯示可驗證的一般買法基準。",
            )

        return BackToBackFareSearchResponse(
            query=query,
            pricing_capability=(
                BackToBackPricingCapability.FULL_BACK_TO_BACK
                if comparison_supported
                else BackToBackPricingCapability.OPEN_JAW_PROVIDER_REQUIRED
            ),
            comparisons=comparisons,
            candidates=[
                FareCandidateSet(role=role, quotes=candidates[role]) for role in FareTicketRole
            ],
            fx_rates=[rates[currency] for currency in sorted(rates)],
            sources=[candidate_result.source for candidate_result in results],
            warnings=list(dict.fromkeys(warnings)),
        )
