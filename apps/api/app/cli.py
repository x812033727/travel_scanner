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
from app.models import Plan, Subscription, UsageLedger, User
from app.providers.registry import build_provider, provider_status
from app.search.schemas import SearchCreate
from app.usage.service import seed_plans


async def set_plan(email: str, plan_code: str) -> None:
    async with SessionFactory() as session:
        await seed_plans(session)
        user = await session.scalar(select(User).where(User.email == email.lower()))
        plan = await session.scalar(select(Plan).where(Plan.code == plan_code.upper()))
        if user is None or plan is None:
            raise SystemExit("User or plan was not found")
        subscription = await session.scalar(
            select(Subscription).where(Subscription.user_id == user.id).with_for_update()
        )
        if subscription is None:
            raise SystemExit("Subscription was not found")
        difference = plan.monthly_credits - subscription.credit_balance
        subscription.plan_id = plan.id
        subscription.credit_balance = plan.monthly_credits
        session.add(
            UsageLedger(
                user_id=user.id,
                subscription_id=subscription.id,
                entry_type="plan_adjustment",
                amount=difference,
                balance_after=subscription.credit_balance,
                reference=f"set-plan:{plan.code}:{subscription.period_start}",
                metadata_json={"plan": plan.code, "source": "cli"},
            )
        )
        await session.commit()
        print(f"{email} is now on {plan.code} with {plan.monthly_credits} credits")


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
    command = subparsers.add_parser("set-plan")
    command.add_argument("--email", required=True)
    command.add_argument("--plan", choices=["FREE", "PRO"], required=True)
    verify = subparsers.add_parser("verify-airline-crawlers")
    verify.add_argument("--origin", default="TPE")
    verify.add_argument("--destination", default="NRT")
    verify.add_argument("--strict", action="store_true")
    live = subparsers.add_parser("verify-live-provider")
    live.add_argument("--origin", default="TPE")
    live.add_argument("--destination", default="NRT")
    live.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if args.command == "set-plan":
        asyncio.run(set_plan(args.email, args.plan))
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
