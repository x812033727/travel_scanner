import argparse
import asyncio
import sys
from datetime import UTC, datetime, timedelta
from io import TextIOWrapper

from sqlalchemy import select

from app.config import get_settings
from app.crawlers.airlines import AirlineFareCrawlerService
from app.crawlers.schemas import AirlineFareSearch
from app.crawlers.verification import build_verification_report
from app.db import SessionFactory
from app.infra import get_redis
from app.models import User
from app.providers.registry import build_provider, provider_status
from app.search.schemas import SearchCreate
from app.usage.service import PACKAGE_DEFAULTS, grant_package


async def add_usage_package(email: str, package_code: str, reference: str) -> None:
    async with SessionFactory() as session:
        user = await session.scalar(select(User).where(User.email == email.lower()))
        if user is None:
            raise SystemExit("User was not found")
        ledger, created = await grant_package(session, user.id, package_code, reference)
        if not created:
            raise SystemExit("This external reference was already used")
        await session.commit()
        print(
            f"Added {ledger.amount} uses to {email}; "
            f"remaining balance is {ledger.balance_after} (reference {ledger.reference})"
        )


async def verify_airline_crawlers(origin: str, destination: str) -> bool:
    query = AirlineFareSearch(
        origin=origin,
        destination=destination,
        limit_per_airline=2,
    )
    response = await AirlineFareCrawlerService(get_settings(), get_redis()).search(
        query, force_refresh=True
    )
    report = build_verification_report(query, response)
    print(report.model_dump_json(indent=2))
    return report.passed


async def verify_live_provider(origin: str, destination: str) -> bool:
    status = provider_status()
    if status.status != "ready":
        print(status.model_dump_json(indent=2))
        return False
    today = datetime.now(UTC).date()
    query = SearchCreate(
        origin=origin.upper(),
        destination=destination.upper(),
        departure_date=today + timedelta(days=60),
        return_date=today + timedelta(days=65),
        travelers={"adults": 1, "rooms": 1},
        modules=["flight", "hotel", "activities", "transport"],
        preferences={"interests": ["food", "culture"]},
    )
    provider = build_provider(get_redis())
    if provider is None:
        print(status.model_dump_json(indent=2))
        return False
    flights, hotels, activities, transfers = await asyncio.gather(
        provider.search_flights(query),
        provider.search_hotels(query),
        provider.search_activities(query),
        provider.search_transport(query),
    )
    report = {
        "provider": status.provider,
        "mode": status.mode,
        "origin": origin.upper(),
        "destination": destination.upper(),
        "counts": {
            "flight": len(flights),
            "hotel": len(hotels),
            "activities": len(activities),
            "transport": len(transfers),
        },
        "all_modules_returned": all((flights, hotels, activities, transfers)),
    }
    print(report)
    return bool(report["all_modules_returned"])


def main() -> None:
    if isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Travel Scanner development utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("add-usage-package")
    command.add_argument("--email", required=True)
    command.add_argument(
        "--package",
        choices=[code for code in PACKAGE_DEFAULTS if code != "TRIAL_3"],
        required=True,
    )
    command.add_argument("--reference", required=True)
    verify = subparsers.add_parser("verify-airline-crawlers")
    verify.add_argument("--origin", default="TPE")
    verify.add_argument("--destination", default="NRT")
    verify.add_argument("--strict", action="store_true")
    live = subparsers.add_parser("verify-live-provider")
    live.add_argument("--origin", default="TPE")
    live.add_argument("--destination", default="NRT")
    live.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if args.command == "add-usage-package":
        asyncio.run(add_usage_package(args.email, args.package, args.reference))
    elif args.command == "verify-airline-crawlers":
        passed = asyncio.run(verify_airline_crawlers(args.origin, args.destination))
        if args.strict and not passed:
            raise SystemExit(1)
    elif args.command == "verify-live-provider":
        passed = asyncio.run(verify_live_provider(args.origin, args.destination))
        if args.strict and not passed:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
