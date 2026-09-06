import argparse
import asyncio
import getpass
import json
import sys
from datetime import UTC, datetime, timedelta
from io import TextIOWrapper
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import func, select

from app import hotspots as hotspots_package
from app.admin.service import load_runtime_settings
from app.auth.schemas import RegisterRequest
from app.auth.service import hash_password
from app.config import get_settings
from app.crawlers.airlines import AirlineFareCrawlerService
from app.crawlers.schemas import AirlineFareSearch
from app.crawlers.verification import build_verification_report
from app.db import SessionFactory
from app.foods.coordinate_fill_cli import fill_food_merchant_coordinates
from app.foods.place_matching_cli import match_food_merchant_places
from app.foods.service import seed_food_catalog
from app.foods.trend_import import DEFAULT_FILE as TREND_MERCHANTS_FILE
from app.foods.trend_import import backfill_english_names, import_trend_merchants
from app.holidays.refresh import HolidaySourceError
from app.holidays.refresh import refresh as refresh_holidays
from app.hotspots.candidate_cli import import_candidates
from app.hotspots.candidate_generation import generate_candidates
from app.hotspots.cities import CITY_BY_CODE
from app.hotspots.guide_review import review_pending_guides
from app.hotspots.jobs import collect_once
from app.hotspots.place_matching import (
    MatchReport,
    approve_pending_candidate,
    match_missing_places,
    missing_place_targets,
)
from app.hotspots.simplified_names import (
    BOOTSTRAP_DIR,
    ConversionReport,
    acceptable,
    apply_conversions,
    convert_names,
    seed_rows,
    stored_label_count,
    write_rows,
)
from app.hotspots.wikidata_labels import BOOTSTRAP_FILES, fill_bootstrap_files
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
from app.trips.name_backfill import backfill_trip_item_names
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
            counts[key] = int(await session.scalar(select(func.count()).select_from(model)) or 0)
        counts["merchants_with_area"] = int(
            await session.scalar(
                select(func.count())
                .select_from(FoodMerchant)
                .where(FoodMerchant.area_id.is_not(None))
            )
            or 0
        )
    return counts


async def backfill_trip_items(dry_run: bool) -> dict[str, int]:
    async with SessionFactory() as session:
        return await backfill_trip_item_names(session, dry_run=dry_run)


def fill_hotspot_labels(files: list[str], dry_run: bool, overwrite_original: bool) -> None:
    """Write Wikidata labels into the bootstrap files and print a per-file summary."""

    report = fill_bootstrap_files(
        Path(hotspots_package.__file__).parent,
        files=files,
        dry_run=dry_run,
        overwrite_original=overwrite_original,
        country_for_city=lambda code: CITY_BY_CODE[code].country_code,
    )
    for filename, counts in report.files.items():
        print(f"{filename:32} {counts['changed']:4} of {counts['rows']:4} rows changed")
    for line in report.changed_rows:
        print(f"  {line}")
    if report.missing_qids:
        print(f"no Wikidata entity for: {', '.join(report.missing_qids)}")
    if dry_run:
        print(f"dry run: {report.total_changed} rows would change")
    else:
        print(f"{report.total_changed} rows updated; review the diff before committing")


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


async def review_guide_backlog(
    *,
    provider: str | None,
    locales: list[str],
    limit: int | None,
    min_relevance: int,
    min_quality: int,
    max_calls: int,
    batch_size: int,
    max_output_tokens: int | None,
    apply: bool,
    verbose: bool,
) -> dict[str, Any]:
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        if max_output_tokens:
            # Gemini's thinking tokens count against the same ceiling, and a truncated
            # reply costs the whole batch, so a long run may need more than the admin
            # value tuned for interactive searches.
            settings = settings.model_copy(
                update={"hotspot_guide_ai_max_output_tokens": max_output_tokens}
            )
        report = await review_pending_guides(
            session,
            settings,
            provider_name=cast(Any, provider),
            locales=locales or None,
            limit=limit,
            min_relevance=min_relevance,
            min_quality=min_quality,
            max_calls=max_calls,
            batch_size=batch_size,
            apply=apply,
        )
    shown = report.decisions if verbose else report.decisions[:40]
    for item in shown:
        scores = (
            f"r={item.relevance_score:>3} q={item.quality_score:>3}"
            if item.relevance_score is not None
            else "no score  "
        )
        print(
            f"  {item.decision:<9} {item.locale:<5} {item.content_type:<7} {scores} "
            f"{item.hotspot_name} — {item.title[:60]}"
        )
    if not verbose and len(report.decisions) > len(shown):
        print(f"  ... {len(report.decisions) - len(shown)} more (use --verbose)")
    return {
        "applied": report.applied,
        "provider": report.provider,
        "model": report.model,
        "counts": report.counts(),
        "ai_calls": report.calls,
        "input_tokens": report.input_tokens,
        "output_tokens": report.output_tokens,
        "errors": report.errors,
    }


def _read_text(path: Path) -> str:
    """Read a file from an async command; the CLI is single-user and blocking here is fine."""
    return path.read_text(encoding="utf-8")


async def fill_simplified_names(
    *,
    provider: str | None,
    apply: bool,
    max_output_tokens: int | None,
    mapping_file: Path | None,
    source: str = "seeds",
) -> dict[str, Any]:
    """Convert, or apply a mapping produced by an earlier run.

    The API key lives in the admin database, so the conversion runs where that
    database is; the bootstrap files it edits are checked into the repository. So
    the two halves are separable: emit the mapping on the server, apply it here.
    """
    if source == "areas":
        # The area catalog is Python, not JSON, so this half only ever emits a mapping;
        # the table it feeds is written by hand into areas.py and reviewed in the diff.
        from app.hotspots.areas import HOTSPOT_AREAS

        loaded = []
        before = 0
        names = sorted({area.names["zh-TW"] for areas in HOTSPOT_AREAS.values() for area in areas})
    else:
        paths = [BOOTSTRAP_DIR / name for name in BOOTSTRAP_FILES]
        loaded = seed_rows(paths)
        before = sum(stored_label_count(rows) for _path, rows in loaded)
        names = [str(row["name"]) for _path, rows in loaded for row in rows if row.get("name")]
    if mapping_file:
        raw = cast(dict[str, Any], json.loads(_read_text(mapping_file)))
        pairs = cast(dict[str, str], raw.get("conversions", raw))
        report = ConversionReport(
            converted={
                key: value
                for key, value in pairs.items()
                # Re-check every pair here: the mapping is a file that travelled.
                if acceptable(key, value)
            }
        )
        report.rejected = [(k, v) for k, v in pairs.items() if not acceptable(k, v)]
    else:
        async with SessionFactory() as session:
            settings = await load_runtime_settings(session)
        if max_output_tokens:
            settings = settings.model_copy(
                update={"hotspot_guide_ai_max_output_tokens": max_output_tokens}
            )
        report = await convert_names(names, settings, provider_name=cast(Any, provider))
    written = 0
    # Writing a run that converted nothing would strip every existing label, which is
    # how a failed vendor call once looked identical to a successful no-op.
    refused = apply and (source == "areas" or bool(report.errors) or not report.converted)
    if apply and not refused:
        for path, rows in loaded:
            written += apply_conversions(rows, report.converted)
            write_rows(path, rows)
    # The conversions that share the fewest characters with their input are the ones
    # a rename would hide in, so they are the ones worth reading.
    riskiest = sorted(
        report.converted.items(),
        key=lambda pair: len(set(pair[0]) & set(pair[1])) / max(len(set(pair[0])), 1),
    )[:12]
    for traditional, simplified in riskiest:
        print(f"  check  {traditional} -> {simplified}")
    for traditional, simplified in report.rejected[:12]:
        print(f"  reject {traditional} -> {simplified}")
    if refused:
        print(
            "refusing to write: "
            + (f"{len(report.errors)} batch error(s)" if report.errors else "no conversions")
            + f"; {before} existing zh-CN label(s) left untouched"
        )
    return {
        "applied": apply and not refused,
        "refused": refused,
        "conversions": report.converted if not apply else {},
        "labels_before": before,
        "converted": len(report.converted),
        "unchanged": len(report.unchanged),
        "rejected": len(report.rejected),
        "missing": len(report.missing),
        "written": written,
        "ai_calls": report.calls,
        "errors": report.errors,
    }


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

    coordinates = subparsers.add_parser(
        "fill-food-merchant-coordinates",
        help=(
            "Read each merchant's own cited pages and store the coordinate they publish. "
            "Uses only merchant_website and merchant_listing sources; a city food guide "
            "says nothing about where one restaurant stands."
        ),
    )
    coordinates.add_argument(
        "--destination", action="append", default=[], help="Limit to a destination (repeatable)"
    )
    coordinates.add_argument("--limit", type=int, help="Stop after this many merchants")
    coordinates.add_argument(
        "--apply", action="store_true", help="Write the coordinates instead of only reporting them"
    )
    subparsers.add_parser(
        "seed-foods",
        help="Upsert the food catalog, merchants, areas and categories, then print the counts",
    )
    trend = subparsers.add_parser(
        "import-trend-merchants",
        help=(
            "Import a JSON batch of 潮流街區 merchants as pending, inactive rows; "
            "reports only unless --apply. Re-running skips what already exists."
        ),
    )
    trend.add_argument(
        "--file",
        default=str(TREND_MERCHANTS_FILE),
        help="JSON list of merchants (default: the batch committed in app/foods/data)",
    )
    trend.add_argument("--limit", type=int, help="Stop after this many merchants")
    trend.add_argument(
        "--apply", action="store_true", help="Write the rows instead of only reporting them"
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
    labels = subparsers.add_parser(
        "fill-hotspot-labels",
        help=(
            "Backfill original-script names and per-locale labels in the hotspot bootstrap "
            "files from Wikidata (network access required); review the diff afterwards"
        ),
    )
    labels.add_argument(
        "--file",
        action="append",
        default=[],
        choices=list(BOOTSTRAP_FILES),
        help="Limit to one bootstrap file; repeatable (default: all)",
    )
    labels.add_argument(
        "--overwrite-original",
        action="store_true",
        help="Replace reviewed local_name values with the Wikidata label as well",
    )
    labels.add_argument(
        "--dry-run", action="store_true", help="Report what would change without writing"
    )
    holidays = subparsers.add_parser(
        "refresh-holidays",
        help=(
            "Re-read a government calendar and report how it differs from the vendored "
            "JSON; writes nothing without --apply and never overwrites a written name"
        ),
    )
    holidays.add_argument("--country", choices=["tw", "jp"], required=True)
    holidays.add_argument("--year", type=int, required=True)
    holidays.add_argument(
        "--file",
        help=(
            "Parse a copy downloaded by hand instead of fetching; required for tw, whose "
            "certificate chain OpenSSL refuses (see docs/public-holidays.md)"
        ),
    )
    holidays.add_argument(
        "--apply", action="store_true", help="Write the fetched dates back into the data file"
    )
    backfill = subparsers.add_parser(
        "backfill-trip-item-names",
        help=(
            "Give trip items saved before migration 0039 their five-locale labels from the "
            "catalog; rows the traveller renamed are left alone"
        ),
    )
    backfill.add_argument(
        "--dry-run", action="store_true", help="Count what would change without writing"
    )
    guide_review = subparsers.add_parser(
        "review-pending-guides",
        help=(
            "Score the pending guide backlog with the configured AI vendor and record "
            "approve/reject on each row. One AI call covers 20 candidates; nothing is "
            "written without --apply."
        ),
    )
    guide_review.add_argument(
        "--provider", help="AI vendor to use (default: the configured guide-search vendor)"
    )
    guide_review.add_argument(
        "--locale", action="append", default=[], help="Only this locale (repeatable)"
    )
    guide_review.add_argument("--limit", type=int, help="Stop after this many pending rows")
    guide_review.add_argument("--min-relevance", type=int, default=60)
    guide_review.add_argument("--min-quality", type=int, default=40)
    guide_review.add_argument(
        "--max-calls", type=int, default=200, help="Hard ceiling on billable AI calls"
    )
    guide_review.add_argument(
        "--batch-size", type=int, default=20, help="Candidates per AI call (default 20)"
    )
    guide_review.add_argument(
        "--max-output-tokens",
        type=int,
        help="Override the guide-search output ceiling for this run",
    )
    guide_review.add_argument(
        "--apply", action="store_true", help="Write the decisions instead of only reporting them"
    )
    guide_review.add_argument(
        "--verbose", action="store_true", help="Print every decision, not just the first 40"
    )
    english_names = subparsers.add_parser(
        "backfill-merchant-english-names",
        help=(
            "Give merchants already imported the English label their data file now carries; "
            "dry run unless --apply"
        ),
    )
    english_names.add_argument(
        "--apply", action="store_true", help="Write the changes (default: report only)"
    )
    simplified = subparsers.add_parser(
        "fill-simplified-names",
        help=(
            "Derive every seed's zh-CN label from its Traditional name with the configured "
            "AI vendor, dropping any reply that is not a character-for-character conversion"
        ),
    )
    simplified.add_argument("--provider", help="AI vendor (default: the configured one)")
    simplified.add_argument(
        "--source",
        choices=("seeds", "areas"),
        default="seeds",
        help="What to convert: the hotspot seed files, or the area catalog (emit only)",
    )
    simplified.add_argument("--max-output-tokens", type=int)
    simplified.add_argument(
        "--from-mapping",
        help="Apply a conversions mapping emitted by an earlier run instead of calling the AI",
    )
    simplified.add_argument(
        "--apply", action="store_true", help="Write the bootstrap files instead of reporting"
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
        report = asyncio.run(import_candidates(Path(args.file), apply=args.apply, limit=args.limit))
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
        report = asyncio.run(match_food_merchant_places(args.destination, args.limit, args.apply))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "fill-food-merchant-coordinates":
        report = asyncio.run(
            fill_food_merchant_coordinates(args.destination, args.limit, args.apply)
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "import-trend-merchants":
        report = asyncio.run(
            import_trend_merchants(Path(args.file), apply=args.apply, limit=args.limit)
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
    elif args.command == "backfill-trip-item-names":
        print(json.dumps(asyncio.run(backfill_trip_items(args.dry_run)), ensure_ascii=False))
    elif args.command == "review-pending-guides":
        summary = asyncio.run(
            review_guide_backlog(
                provider=args.provider,
                locales=args.locale,
                limit=args.limit,
                min_relevance=args.min_relevance,
                min_quality=args.min_quality,
                max_calls=args.max_calls,
                batch_size=args.batch_size,
                max_output_tokens=args.max_output_tokens,
                apply=args.apply,
                verbose=args.verbose,
            )
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    elif args.command == "backfill-merchant-english-names":
        english_summary = asyncio.run(backfill_english_names(apply=args.apply))
        print(json.dumps(english_summary, ensure_ascii=False, indent=2))
    elif args.command == "fill-simplified-names":
        simplified_summary = asyncio.run(
            fill_simplified_names(
                provider=args.provider,
                apply=args.apply,
                max_output_tokens=args.max_output_tokens,
                mapping_file=Path(args.from_mapping) if args.from_mapping else None,
                source=args.source,
            )
        )
        print(json.dumps(simplified_summary, ensure_ascii=False, indent=2))
        if simplified_summary.get("refused"):
            raise SystemExit(1)
    elif args.command == "refresh-holidays":
        try:
            holiday_summary = refresh_holidays(
                args.country,
                args.year,
                write=args.apply,
                file=Path(args.file) if args.file else None,
            )
        except HolidaySourceError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
            raise SystemExit(1) from exc
        print(json.dumps(holiday_summary, ensure_ascii=False, indent=2))
    elif args.command == "fill-hotspot-labels":
        fill_hotspot_labels(
            args.file or list(BOOTSTRAP_FILES), args.dry_run, args.overwrite_original
        )


if __name__ == "__main__":
    main()
