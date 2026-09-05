import argparse
import asyncio
import getpass
import json
import sys
from datetime import UTC, datetime, timedelta
from io import TextIOWrapper
from pathlib import Path
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import func, select

from app.admin.service import load_runtime_settings
from app.auth.schemas import RegisterRequest
from app.auth.service import hash_password
from app.config import get_settings
from app.crawlers.airlines import AirlineFareCrawlerService
from app.crawlers.schemas import AirlineFareSearch
from app.crawlers.verification import build_verification_report
from app.db import SessionFactory
from app.foods.place_matching_cli import match_food_merchant_places
from app.foods.service import seed_food_catalog
from app.hotspots.candidate_cli import import_candidates
from app.hotspots.candidate_generation import generate_candidates
from app.hotspots.jobs import collect_once
from app.hotspots.place_matching import (
    MatchReport,
    approve_pending_candidate,
    match_missing_places,
    missing_place_targets,
)
from app.infra import get_redis
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    TravelHotspot,
    User,
)
from app.places.naver import NaverPlaceService
from app.providers.registry import build_provider, provider_status
from app.search.schemas import SearchCreate
from app.trips.routing import NaverDirectionsProvider, RoutePoint
from app.usage.service import PACKAGE_DEFAULTS, create_usage_account, grant_package


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


def _read_password(from_stdin: bool) -> str:
    if from_stdin:
        return sys.stdin.readline().rstrip("\r\n")
    first = getpass.getpass("Administrator password: ")
    second = getpass.getpass("Confirm password: ")
    if first != second:
        raise SystemExit("Passwords do not match")
    return first


async def create_admin(email: str, password: str) -> None:
    """Create an administrator without going through public self-registration."""
    try:
        payload = RegisterRequest(email=email, password=password)
    except ValidationError as exc:
        raise SystemExit(f"Invalid administrator account: {exc.errors()[0]['msg']}") from exc
    normalized_email = str(payload.email).lower()
    async with SessionFactory() as session:
        existing = await session.scalar(select(User).where(User.email == normalized_email))
        if existing is not None:
            raise SystemExit("User already exists; use set-admin to grant administrator access")
        user = User(
            email=normalized_email,
            password_hash=hash_password(payload.password),
            preferred_locale=payload.preferred_locale,
            is_admin=True,
        )
        session.add(user)
        await session.flush()
        await create_usage_account(session, user)
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="admin_role.updated",
                target=f"user:{user.id}",
                metadata_json={
                    "email": normalized_email,
                    "is_admin": True,
                    "source": "cli-create-admin",
                },
            )
        )
        await session.commit()
        print(f"Created administrator {normalized_email}")


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


async def seed_foods() -> dict[str, int]:
    """Seed dishes, merchants and the browsing taxonomy without running hotspot collection."""

    async with SessionFactory() as session:
        foods = await seed_food_catalog(session)
        await session.commit()
        counts = {"foods": foods}
        for key, model in (
            ("areas", FoodArea),
            ("categories", FoodCategory),
            ("merchants", FoodMerchant),
            ("merchant_category_links", FoodMerchantCategory),
        ):
            counts[key] = int(
                await session.scalar(select(func.count()).select_from(model)) or 0
            )
        counts["merchants_with_area"] = int(
            await session.scalar(
                select(func.count()).select_from(FoodMerchant).where(FoodMerchant.area_id.is_not(None))
            )
            or 0
        )
    return counts


def _format_match(report: MatchReport) -> str:
    line = f"{report.outcome:16} {report.slug:44} {report.name}"
    if report.candidate:
        details = ", ".join(
            f"{key}={value}" for key, value in report.candidate.items() if value is not None
        )
        line += f"\n{'':17}candidate: {details}"
    return line


async def match_hotspot_places(
    destination_ids: list[str],
    slug_prefix: str | None,
    limit: int | None,
    dry_run: bool,
    approve: list[str],
) -> None:
    """Fill Google Place IDs for public hotspots that have none, or approve candidates."""

    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        if not settings.google_maps_api_key or not settings.hotspot_place_enrichment_enabled:
            raise SystemExit("Google Maps 尚未設定，或地點補齊已停用")
        redis = get_redis()
        if approve:
            for slug in approve:
                hotspot = await session.scalar(
                    select(TravelHotspot).where(TravelHotspot.slug == slug.strip().casefold())
                )
                if hotspot is None:
                    print(f"{'not_found':16} {slug}")
                    continue
                print(
                    _format_match(
                        await approve_pending_candidate(session, redis, settings, hotspot)
                    )
                )
            return
        targets = await missing_place_targets(
            session,
            destination_ids=tuple(destination_ids),
            slug_prefix=slug_prefix,
            limit=limit,
        )
        print(f"{len(targets)} public hotspots without a Google Place ID")
        if dry_run:
            for hotspot in targets:
                print(f"  {hotspot.slug:44} {hotspot.name}")
            return
        reports = await match_missing_places(session, redis, settings, targets)
        for report in reports:
            print(_format_match(report))
        summary = {
            outcome: sum(1 for report in reports if report.outcome == outcome)
            for outcome in sorted({report.outcome for report in reports})
        }
        print(f"summary: {summary} google_calls={sum(report.calls for report in reports)}")


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
    create = subparsers.add_parser("create-admin")
    create.add_argument("--email", required=True)
    create.add_argument(
        "--password-stdin",
        action="store_true",
        help="Read the password from the first line of standard input instead of prompting",
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
    candidates = subparsers.add_parser(
        "import-hotspot-candidates",
        help="Cross-check a JSON list of place names and report or write what survives",
    )
    candidates.add_argument("--file", required=True, help="JSON file with city_code and candidates")
    candidates.add_argument("--limit", type=int, help="Stop after this many candidates")
    candidates.add_argument(
        "--apply", action="store_true", help="Write the rows instead of only reporting them"
    )
    generator = subparsers.add_parser(
        "generate-hotspot-candidates",
        help=(
            "Ask Gemini for a city's attraction names and write the candidate JSON. "
            "Generation is one API call; the later import costs one billable Google "
            "lookup per name, so start around 40-50 and top up with --avoid."
        ),
    )
    generator.add_argument("--city", required=True, help="City code, e.g. TNN")
    generator.add_argument("--count", type=int, help="How many names to ask for")
    generator.add_argument("--out", help="Output path (default candidates/<CODE>.json)")
    generator.add_argument("--model", help="Override the configured Gemini model")
    generator.add_argument(
        "--avoid",
        action="append",
        default=[],
        help="Existing candidate JSON whose names must not be repeated (repeatable)",
    )
    generator.add_argument(
        "--dry-run", action="store_true", help="Print the document without writing it"
    )
    generator.add_argument("--force", action="store_true", help="Overwrite an existing file")
    merchants = subparsers.add_parser(
        "match-food-merchant-places",
        help=(
            "Attach Google Place IDs to seeded food merchants. Writes only the Place ID: "
            "publication still needs a durable non-Google coordinate and a human check "
            "that the ID is the right branch. Korea is skipped, having no API identity."
        ),
    )
    merchants.add_argument(
        "--destination", action="append", default=[], help="Limit to a destination (repeatable)"
    )
    merchants.add_argument("--limit", type=int, help="Stop after this many merchants")
    merchants.add_argument(
        "--apply", action="store_true", help="Write the Place IDs instead of only reporting them"
    )
    subparsers.add_parser(
        "seed-foods",
        help="Upsert the food catalog, merchants, areas and categories, then print the counts",
    )
    places = subparsers.add_parser(
        "match-hotspot-places",
        help="Fill Google Place IDs for public hotspots that have none (uses the live key)",
    )
    places.add_argument(
        "--destination",
        action="append",
        default=[],
        metavar="DESTINATION_ID",
        help="Limit to a destination id such as tokyo; repeatable",
    )
    places.add_argument("--slug-prefix", help="Limit to hotspot slugs starting with this text")
    places.add_argument("--limit", type=int, help="Stop after this many hotspots")
    places.add_argument(
        "--dry-run", action="store_true", help="List the targets without calling Google"
    )
    places.add_argument(
        "--approve",
        action="append",
        default=[],
        metavar="SLUG",
        help="Promote the stored pending candidate of this hotspot slug; repeatable",
    )
    args = parser.parse_args()
    if args.command == "add-usage-package":
        asyncio.run(add_usage_package(args.email, args.package, args.reference))
    elif args.command == "set-admin":
        asyncio.run(set_admin(args.email, not args.revoke))
    elif args.command == "create-admin":
        asyncio.run(create_admin(args.email, _read_password(args.password_stdin)))
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
    elif args.command == "import-hotspot-candidates":
        report = asyncio.run(
            import_candidates(Path(args.file), apply=args.apply, limit=args.limit)
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "generate-hotspot-candidates":
        report = asyncio.run(
            generate_candidates(
                city_code=args.city,
                count=args.count,
                out=Path(args.out) if args.out else None,
                model=args.model,
                dry_run=args.dry_run,
                force=args.force,
                avoid_files=[Path(item) for item in args.avoid],
            )
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "match-food-merchant-places":
        report = asyncio.run(
            match_food_merchant_places(args.destination, args.limit, args.apply)
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "collect-hotspots":
        print(asyncio.run(collect_once()))
    elif args.command == "seed-foods":
        print(json.dumps(asyncio.run(seed_foods()), ensure_ascii=False))
    elif args.command == "match-hotspot-places":
        asyncio.run(
            match_hotspot_places(
                args.destination, args.slug_prefix, args.limit, args.dry_run, args.approve
            )
        )


if __name__ == "__main__":
    main()
