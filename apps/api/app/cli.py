import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime, timedelta
from io import TextIOWrapper
from uuid import UUID

from sqlalchemy import select

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.crawlers.airlines import AirlineFareCrawlerService
from app.crawlers.schemas import AirlineFareSearch
from app.crawlers.verification import build_verification_report
from app.db import SessionFactory
from app.hotspots.jobs import collect_once
from app.infra import get_redis
from app.models import AdminAuditLog, User
from app.places.naver import NaverPlaceService
from app.providers.registry import build_provider, provider_status
from app.search.schemas import SearchCreate
from app.trips.routing import NaverDirectionsProvider, RoutePoint
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


async def set_admin(email: str, enabled: bool) -> None:
    normalized_email = email.strip().lower()
    async with SessionFactory() as session:
        user = await session.scalar(select(User).where(User.email == normalized_email))
        if user is None:
            raise SystemExit("User was not found")
        user.is_admin = enabled
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="admin_role.updated",
                target=f"user:{user.id}",
                metadata_json={"email": normalized_email, "is_admin": enabled, "source": "cli"},
            )
        )
        await session.commit()
        state = "administrator" if enabled else "regular user"
        print(f"Updated {normalized_email} to {state}")


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
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
    status = provider_status(settings)
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
    provider = build_provider(get_redis(), settings)
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


async def verify_naver_maps() -> bool:
    settings = get_settings()
    redis = get_redis()
    service = NaverPlaceService(redis, settings)
    palace = await service.search_place("景福宮 서울")
    village = await service.search_place("北村韓屋村 서울")
    route = None
    if palace and village:
        route = await NaverDirectionsProvider(settings, None, redis).compute(
            RoutePoint(
                item_id=UUID("00000000-0000-4000-8000-000000000001"),
                name=str(palace.get("name") or "景福宮"),
                latitude=float(palace["latitude"]),
                longitude=float(palace["longitude"]),
                provider_place_id=str(palace.get("place_id") or "") or None,
                place_provider="naver_local",
            ),
            RoutePoint(
                item_id=UUID("00000000-0000-4000-8000-000000000002"),
                name=str(village.get("name") or "北村韓屋村"),
                latitude=float(village["latitude"]),
                longitude=float(village["longitude"]),
                provider_place_id=str(village.get("place_id") or "") or None,
                place_provider="naver_local",
            ),
            None,
            "FASTEST",
            "drive",
        )
    report = {
        "provider": "naver_maps",
        "configured": settings.naver_maps_configured,
        "places": {
            "gyeongbokgung": bool(palace),
            "bukchon_hanok_village": bool(village),
        },
        "drive_route": {
            "available": route is not None,
            "duration_minutes": route.duration_minutes if route else None,
            "distance_meters": route.distance_meters if route else None,
        },
        "dynamic_map": {
            "client_id_configured": bool(settings.naver_maps_client_id),
            "requires_browser_origin_check": True,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(settings.naver_maps_configured and palace and village and route)


def main() -> None:
    if isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Mokaair development utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("add-usage-package")
    command.add_argument("--email", required=True)
    command.add_argument(
        "--package",
        choices=[code for code in PACKAGE_DEFAULTS if code != "TRIAL_3"],
        required=True,
    )
    command.add_argument("--reference", required=True)
    admin = subparsers.add_parser("set-admin")
    admin.add_argument("--email", required=True)
    admin.add_argument(
        "--revoke",
        action="store_true",
        help="Remove database administrator access instead of granting it",
    )
    verify = subparsers.add_parser("verify-airline-crawlers")
    verify.add_argument("--origin", default="TPE")
    verify.add_argument("--destination", default="NRT")
    verify.add_argument("--strict", action="store_true")
    live = subparsers.add_parser("verify-live-provider")
    live.add_argument("--origin", default="TPE")
    live.add_argument("--destination", default="NRT")
    live.add_argument("--strict", action="store_true")
    naver = subparsers.add_parser("verify-naver-maps")
    naver.add_argument("--strict", action="store_true")
    subparsers.add_parser("collect-hotspots")
    args = parser.parse_args()
    if args.command == "add-usage-package":
        asyncio.run(add_usage_package(args.email, args.package, args.reference))
    elif args.command == "set-admin":
        asyncio.run(set_admin(args.email, not args.revoke))
    elif args.command == "verify-airline-crawlers":
        passed = asyncio.run(verify_airline_crawlers(args.origin, args.destination))
        if args.strict and not passed:
            raise SystemExit(1)
    elif args.command == "verify-live-provider":
        passed = asyncio.run(verify_live_provider(args.origin, args.destination))
        if args.strict and not passed:
            raise SystemExit(1)
    elif args.command == "verify-naver-maps":
        passed = asyncio.run(verify_naver_maps())
        if args.strict and not passed:
            raise SystemExit(1)
    elif args.command == "collect-hotspots":
        print(asyncio.run(collect_once()))


if __name__ == "__main__":
    main()
