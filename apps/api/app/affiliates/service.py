from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

import httpx
from redis.asyncio import Redis

from app.affiliates.registry import AffiliatePartner
from app.affiliates.schemas import AffiliateModule
from app.config import Settings


@dataclass(frozen=True)
class AffiliateContext:
    module: AffiliateModule
    destination: str
    departure_date: str | None
    return_date: str | None
    sub_id: str
    area: str | None = None
    hotel_name: str | None = None


def allowed_hosts(settings: Settings, partner: AffiliatePartner) -> set[str]:
    raw = str(getattr(settings, partner.allowed_hosts_field) or "")
    return {host.strip().lower().rstrip(".") for host in raw.split(",") if host.strip()}


def validate_target_url(target: str, hosts: set[str]) -> str:
    parsed = urlparse(target)
    host = (parsed.hostname or "").lower().rstrip(".")
    allowed = any(host == item or host.endswith(f".{item}") for item in hosts)
    if parsed.scheme != "https" or not host or not allowed or parsed.username or parsed.password:
        raise ValueError("Affiliate target URL is not an allowed HTTPS destination")
    return target


def _render(template: str, context: AffiliateContext) -> str:
    # {query} is the free-text search a partner landing page accepts: the hotel when
    # one is known, otherwise the destination narrowed by the stay area.
    query = " ".join(
        part for part in (context.hotel_name, context.destination, context.area) if part
    )
    values = {
        "destination": context.destination,
        "departure_date": context.departure_date or "",
        "return_date": context.return_date or "",
        "sub_id": context.sub_id,
        "module": context.module,
        "area": context.area or "",
        "hotel_name": context.hotel_name or "",
        "query": query,
    }
    rendered = template
    for name, value in values.items():
        rendered = rendered.replace(f"{{{name}}}", quote(str(value), safe=""))
    return rendered


def _with_query(target: str, key: str, value: str | None) -> str:
    if not value:
        return target
    parsed = urlparse(target)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault(key, value)
    return urlunparse(parsed._replace(query=urlencode(query)))


def _travelpayouts_target(settings: Settings, module: AffiliateModule) -> str | None:
    field = {
        "flight": "travelpayouts_flight_target_url",
        "hotel": "travelpayouts_hotel_target_url",
        "activities": "travelpayouts_activities_target_url",
        "transport": "travelpayouts_transport_target_url",
        "connectivity": "travelpayouts_activities_target_url",
    }[module]
    return cast(str | None, getattr(settings, field))


class TravelpayoutsLinkClient:
    def __init__(
        self,
        redis: Redis,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.redis = redis
        self.settings = settings
        self.client = client

    async def create(self, target: str, sub_id: str) -> str:
        assert self.settings.travelpayouts_api_token
        assert self.settings.travelpayouts_marker
        assert self.settings.travelpayouts_project_id
        digest = hashlib.sha256(
            f"{target}|{sub_id}|{self.settings.travelpayouts_marker}".encode()
        ).hexdigest()
        cache_key = f"affiliate:travelpayouts:link:{digest}"
        cached = await self.redis.get(cache_key)
        if cached:
            return str(cached)
        try:
            payload = {
                "trs": int(self.settings.travelpayouts_project_id),
                "marker": int(self.settings.travelpayouts_marker),
                "shorten": True,
                "links": [{"url": target, "sub_id": sub_id}],
            }
            if self.client is not None:
                response = await self.client.post(
                    f"{self.settings.travelpayouts_api_base_url.rstrip('/')}/links/v1/create",
                    json=payload,
                    headers={"X-Access-Token": self.settings.travelpayouts_api_token},
                )
            else:
                async with httpx.AsyncClient(
                    timeout=self.settings.provider_timeout_seconds
                ) as client:
                    response = await client.post(
                        f"{self.settings.travelpayouts_api_base_url.rstrip('/')}/links/v1/create",
                        json=payload,
                        headers={"X-Access-Token": self.settings.travelpayouts_api_token},
                    )
            response.raise_for_status()
            body = cast(dict[str, Any], response.json())
            links = cast(dict[str, Any], body.get("result", {})).get("links", [])
            partner_url = (
                links[0].get("partner_url") if links and isinstance(links[0], dict) else None
            )
            if not isinstance(partner_url, str):
                raise ConnectionError("Travelpayouts did not return a partner URL")
        except (httpx.HTTPError, ValueError, TypeError, OverflowError) as exc:
            raise ConnectionError("Travelpayouts partner link is unavailable") from exc
        await self.redis.set(
            cache_key,
            partner_url,
            ex=self.settings.affiliate_link_cache_ttl_seconds,
        )
        return partner_url


async def resolve_partner_target(
    partner: AffiliatePartner,
    context: AffiliateContext,
    settings: Settings,
    redis: Redis,
    travelpayouts_client: TravelpayoutsLinkClient | None = None,
) -> str:
    hosts = allowed_hosts(settings, partner)
    template = cast(str | None, getattr(settings, partner.template_field))
    if partner.code == "travelpayouts":
        direct = _travelpayouts_target(settings, context.module)
        if (
            direct
            and settings.travelpayouts_api_token
            and settings.travelpayouts_marker
            and settings.travelpayouts_project_id
        ):
            client = travelpayouts_client or TravelpayoutsLinkClient(redis, settings)
            try:
                return validate_target_url(
                    await client.create(_render(direct, context), context.sub_id), hosts
                )
            except (ConnectionError, ValueError):
                if not template:
                    raise
        if not template:
            raise ConnectionError("Travelpayouts has no safe fallback link")
        return validate_target_url(_render(template, context), hosts)
    if not template:
        raise ConnectionError(f"{partner.display_name} affiliate link is not configured")
    target = _render(template, context)
    if partner.code == "kkday":
        target = _with_query(target, "cid", settings.kkday_cid)
    elif partner.code == "agoda":
        target = _with_query(target, "cid", settings.agoda_cid)
    elif partner.code == "booking":
        target = _with_query(target, "aid", settings.booking_affiliate_id)
    return validate_target_url(target, hosts)


def token_payload(
    *,
    target: str,
    user_id: str,
    partner: str,
    module: AffiliateModule,
    sub_id: str,
    destination: str,
    search_id: str | None,
    trip_id: str | None,
) -> str:
    return json.dumps(
        {
            "target": target,
            "user_id": user_id,
            "partner": partner,
            "module": module,
            "sub_id": sub_id,
            "destination": destination[:128],
            "search_id": search_id,
            "trip_id": trip_id,
        },
        ensure_ascii=False,
    )
