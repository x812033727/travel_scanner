"""Daily feed refresh and link maintenance. Discovery never publishes new content."""

import asyncio
import re
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit
from xml.etree import ElementTree

import httpx
from sqlalchemy import select

from app.admin.service import load_runtime_settings
from app.catalog_review.evidence import public_request_target
from app.db import SessionFactory, engine
from app.models import TravelServiceImport, TravelServiceOffer, TravelServiceProduct
from app.travel_services.imports import upsert_product
from app.travel_services.network import verify_link
from app.travel_services.schemas import Facts, ProductInput
from app.travel_services.service import catalog_config

# Documented official feed; no configurable arbitrary fetch URL or extra credential.
AIRALO_FEED = "https://www.airalo.com/products.xml"
FEED_LIMIT = 15_000_000


def parse_airalo(body: bytes, now: datetime) -> list[ProductInput]:
    if len(body) > FEED_LIMIT or b"<!DOCTYPE" in body.upper() or b"<!ENTITY" in body.upper():
        raise ValueError("Unsafe feed")
    root = ElementTree.fromstring(body)
    result = []
    countries = {
        "japan-esim": ("JP", "tokyo"),
        "south-korea-esim": ("KR", "seoul"),
        "taiwan-esim": ("TW", "taipei"),
    }
    for item in root.iter("item"):
        values = {child.tag.split("}")[-1]: (child.text or "").strip() for child in item}
        url, title = values.get("link", ""), values.get("title", "")
        parts = urlsplit(url)
        country = countries.get(parts.path.strip("/").split("/")[0])
        if (
            not country
            or parts.hostname not in ("airalo.com", "www.airalo.com")
            or not title
            or not values.get("id")
        ):
            continue
        amount = re.fullmatch(
            r"(\d+(?:\.\d+)?) ([A-Z]{3})", values.get("sale_price") or values.get("price", "")
        )
        duration = re.search(r"\b(\d+)\s*(?:days|day)\b", title, re.I)
        data = re.search(r"\b(\d+(?:\.\d+)?)\s*GB\b", title, re.I)
        # Extract only explicit feed fields; never infer restrictions, coverage or availability.
        facts = Facts(
            country_codes=[country[0]],
            validity_days=int(duration[1]) if duration else None,
            data_gb=float(data[1]) if data else None,
            reference_price=float(amount[1]) if amount else None,
            currency=amount[2] if amount else None,
            price_checked_at=now if amount else None,
        )
        result.append(
            ProductInput(
                source_key=f"airalo:{values['id']}",
                kind="esim",
                destination_id=country[1],
                title=title,
                source_url=url,
                facts=facts,
            )
        )
        if len(result) >= 500:
            break
    return result


async def fetch_airalo() -> bytes:
    async with asyncio.timeout(60), httpx.AsyncClient(timeout=15, trust_env=False) as client:
        pinned = await public_request_target(AIRALO_FEED)
        if pinned is None:
            raise ValueError("Unsafe feed address")
        target, host = pinned
        async with client.stream(
            "GET",
            target,
            headers={"Host": host, "Connection": "close"},
            extensions={"sni_hostname": host},
            follow_redirects=False,
        ) as response:
            response.raise_for_status()
            chunks: list[bytes] = []
            size = 0
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > FEED_LIMIT:
                    raise ValueError("Feed too large")
                chunks.append(chunk)
            return b"".join(chunks)


async def refresh() -> dict[str, Any]:
    async with SessionFactory() as session:
        config, _ = await catalog_config(session)
        settings = await load_runtime_settings(session)
        if not config.airalo_feed_enabled:
            return {"status": "disabled"}
        from app.models import TravelServiceBrand
        from app.travel_services.service import ready_brand

        brand = await session.scalar(
            select(TravelServiceBrand).where(
                TravelServiceBrand.code == "airalo",
                TravelServiceBrand.project_id == (settings.travelpayouts_project_id or ""),
            )
        )
        if not brand or not ready_brand(brand, settings, datetime.now(UTC)):
            return {"status": "not_configured"}
        brand_id = brand.id
        await session.commit()
        run = TravelServiceImport(source="airalo", status="running", rows_json=[], result_json={})
        session.add(run)
        await session.commit()
        run_id = run.id
        try:
            products = parse_airalo(await fetch_airalo(), datetime.now(UTC))
            if not products:
                raise ValueError("No supported products")
            updated = 0
            for payload in products:
                existing = await session.scalar(
                    select(TravelServiceProduct)
                    .where(TravelServiceProduct.source_key == payload.source_key)
                    .with_for_update()
                )
                if (
                    existing
                    and existing.title == payload.title
                    and existing.source_url == payload.source_url
                    and existing.destination_id == payload.destination_id
                    and all(
                        existing.facts.get(key) == getattr(payload.facts, key)
                        for key in ("country_codes", "validity_days", "data_gb", "unlimited")
                    )
                ):
                    # Price refresh cannot erase reviewed restrictions or publish drafts.
                    existing.facts = {
                        **existing.facts,
                        **payload.facts.model_dump(
                            mode="json", include={"reference_price", "currency", "price_checked_at"}
                        ),
                    }
                    existing.version += 1
                    product = existing
                else:
                    product, _ = await upsert_product(session, payload)
                offer = await session.scalar(
                    select(TravelServiceOffer).where(
                        TravelServiceOffer.brand_id == brand_id,
                        TravelServiceOffer.target_url == payload.source_url,
                    )
                )
                if offer is None:
                    session.add(
                        TravelServiceOffer(
                            product_id=product.id,
                            brand_id=brand_id,
                            target_url=payload.source_url,
                            scope="product",
                            status="pending",
                        )
                    )
                updated += 1
            run.status = "completed"
            run.result_json = {"processed": updated}
        except (httpx.HTTPError, ValueError, TimeoutError, ElementTree.ParseError):
            await session.rollback()
            failed_run = await session.get(TravelServiceImport, run_id)
            assert failed_run is not None
            run = failed_run
            run.status = "failed"
            run.result_json = {"error": "service_feed_unavailable"}
        await session.commit()
        return {"status": run.status, **run.result_json}


async def maintain_links() -> dict[str, int]:
    from app.models import TravelServiceBrand

    async with SessionFactory() as session:
        pairs = (
            await session.execute(
                select(TravelServiceOffer, TravelServiceBrand)
                .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
                .where(TravelServiceOffer.status == "approved")
                .order_by(TravelServiceOffer.updated_at)
                .limit(40)
            )
        ).all()
        candidates = [
            (offer.id, offer.version, offer.target_url, brand.code) for offer, brand in pairs
        ]
        await session.commit()
        disabled = 0
        for identifier, version, target, code in candidates:
            try:
                valid = await verify_link(target, code, target)
            except (httpx.HTTPError, ValueError, TimeoutError):
                continue
            offer = await session.scalar(
                select(TravelServiceOffer)
                .where(TravelServiceOffer.id == identifier)
                .with_for_update()
            )
            if offer is None or offer.version != version:
                continue
            if not valid:
                offer.status = "disabled"
                offer.version += 1
                disabled += 1
            offer.updated_at = datetime.now(UTC)
            await session.commit()
        return {"checked": len(candidates), "disabled": disabled}


def run_daily() -> dict[str, Any]:
    async def work() -> dict[str, Any]:
        try:
            return {"feed": await refresh(), "links": await maintain_links()}
        finally:
            await engine.dispose()

    return asyncio.run(work())
