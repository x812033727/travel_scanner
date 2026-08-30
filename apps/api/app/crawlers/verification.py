from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.crawlers.airlines import ADAPTERS
from app.crawlers.schemas import AirlineCode, AirlineFareSearch, AirlineFareSearchResponse


class VerificationOutcome(StrEnum):
    PASSED = "passed"
    EXPECTED_DISABLED = "expected_disabled"
    FAILED = "failed"


class SourceVerification(BaseModel):
    airline_code: AirlineCode
    airline_name: str
    required: bool
    outcome: VerificationOutcome
    quote_count: int
    detail: str


class AirlineCrawlerVerificationReport(BaseModel):
    passed: bool
    verified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    origin: str
    destination: str
    total_quotes: int
    sources: list[SourceVerification]


def build_verification_report(
    query: AirlineFareSearch, response: AirlineFareSearchResponse
) -> AirlineCrawlerVerificationReport:
    sources: list[SourceVerification] = []
    reported_codes: set[AirlineCode] = set()
    for source in response.sources:
        reported_codes.add(source.airline_code)
        required = ADAPTERS[source.airline_code].enabled
        if not required and source.state == "disabled":
            outcome = VerificationOutcome.EXPECTED_DISABLED
        elif source.state == "success" and source.quote_count > 0:
            outcome = VerificationOutcome.PASSED
        else:
            outcome = VerificationOutcome.FAILED
        sources.append(
            SourceVerification(
                airline_code=source.airline_code,
                airline_name=source.airline_name,
                required=required,
                outcome=outcome,
                quote_count=source.quote_count,
                detail=source.detail,
            )
        )
    for code in query.airlines:
        adapter = ADAPTERS[code]
        if adapter.enabled and code not in reported_codes:
            sources.append(
                SourceVerification(
                    airline_code=code,
                    airline_name=adapter.name,
                    required=True,
                    outcome=VerificationOutcome.FAILED,
                    quote_count=0,
                    detail="驗證結果缺少此必要來源",
                )
            )
    passed = all(
        source.outcome != VerificationOutcome.FAILED for source in sources if source.required
    )
    return AirlineCrawlerVerificationReport(
        passed=passed,
        origin=query.origin,
        destination=query.destination,
        total_quotes=len(response.quotes),
        sources=sources,
    )
