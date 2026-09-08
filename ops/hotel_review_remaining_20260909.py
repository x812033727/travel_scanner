"""Guarded remaining hotel review of the exact 2026-09-09 pending snapshot.

No paid APIs, affiliate clicks, booking, configuration changes or blanket approvals.
snapshot/check are read-only. dry-run never calls a write route. apply requires an
explicit, newly evidenced pending subset manifest and --apply. Every mutation uses the normal admin
service, with its commit deferred until a refreshed hash receipt is also ready.
"""

import argparse
import asyncio
import copy
import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

from app.auth.service import is_admin_user
from app.db import SessionFactory, engine
from app.models import (
    AdminAuditLog,
    CatalogReviewRun,
    HotelBookingOption,
    TravelServiceConfig,
    TravelServiceProduct,
    User,
)
from app.problems import AppError
from app.travel_services import admin
from app.travel_services.network import check_hotel_link
from app.travel_services.schemas import (
    CITIES,
    HotelLink,
    HotelOptionEdit,
    HotelOptionReview,
    ProductInput,
    ReviewInput,
    safe_url,
)
from app.travel_services.service import require_product_review
from sqlalchemy import inspect, select, text

ROOT = UUID("5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a")
TAG = "hotel-review-remaining-20260909"
BASELINE_HASH = "c938d83913645ac6a7651eca0e705621b33b40bb235905392c54917492bdb03d"
BASELINE_CAPTURED_AT = "2026-09-08 21:18:03.737914+00:00"
ACTION = "hotel_catalog_evidence_review"
# Only these three independently reviewed, non-OTA CC0 P625 claims are in scope.
# No other new coordinates, OSM way centers, Google/Naver or OTA upstream values.
FACT_FIELDS = {
    "google_place_id",
    "map_verified",
    "latitude",
    "longitude",
    "coordinate_source_url",
    "source_credits",
}
COORDINATE_LICENSE_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
ORIGINAL_CREDITS_HASH = "dc36975672b8ae91f358be643c75313fb5cf367f0af626abf87c19a3524ea963"
# Existing independent hold: announced 2027-05-09 closure, while this workflow has
# no operating-date guard. A fresh platform identity does not resolve that hold.
OPERATING_DATE_HOLDS = {"ed85936a-f890-4a82-80b5-dfdfa63c971a"}
COORDINATE_ROWS = {
    "a124dc1e-7f75-44ff-b12d-080da031b3b9": {
        "source_key": "editorial:kyoto:granvia-kyoto",
        "qid": "Q11337862",
        "revision": 2438233506,
        "claim_id": "Q11337862$EA2347C0-11BE-480F-BCEE-FF40DBFD38C0",
        "latitude": 34.985861,
        "longitude": 135.760222,
        "row_hash": "3ea44e9b008f2fa3da93ec4a8dfcfed0695b08a35904a35e4754b28114a3d030",
    },
    "758907f4-4870-421e-bf6c-6243cdcc30c4": {
        "source_key": "editorial:kyoto:miyako-kyoto-hachijo",
        "qid": "Q11501050",
        "revision": 2448125393,
        "claim_id": "Q11501050$8D1DC5F3-9C1D-4CFB-97B1-0C1823A16F38",
        "latitude": 34.983778,
        "longitude": 135.755917,
        "row_hash": "76072f2a225edaf3492cdfa036b187231e9e9a71c271b068c31e983a33d4529f",
    },
    "50f2d47d-24fe-4b07-85a2-3e1c7671e452": {
        "source_key": "editorial:kyoto:westin-miyako-kyoto",
        "qid": "Q11288502",
        "revision": 2434981201,
        "claim_id": "Q11288502$5AB1D2CD-AE18-4CED-892C-97B7269B056A",
        "latitude": 35.00886111,
        "longitude": 135.78794444,
        "row_hash": "39eaef5356258ef4f6e615f3ea5653424193ecdb24b0d1eaca5d7ac8320b515e",
    },
}
GUARD_CODES = {
    "service_identity_required",
    "service_source_required",
    "service_destination_mismatch",
    "service_area_required",
    "service_link_unavailable",
    "service_offer_mismatch",
}
ENTRY_FIELDS = {
    "kind",
    "id",
    "version",
    "before_hash",
    "decision",
    "reason",
    "source_urls",
    "method",
    "checked_at",
    "browser_verified",
    "new_evidence",
    "identity_note",
    "facts_patch",
    "option_patch",
    "evidence",
}
MODELS = {"product": TravelServiceProduct, "option": HotelBookingOption}


def record(row):
    return {a.key: getattr(row, a.key) for a in inspect(type(row)).column_attrs}


def digest(value):
    # Keep this identical to the original snapshot/check command.
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def normalized(value):
    return json.loads(json.dumps(value, default=str))


def emit(value):
    print(json.dumps(value, ensure_ascii=False, default=str), flush=True)


def save_new(path, value):
    # Evidence outputs must never overwrite a baseline or an earlier receipt.
    with Path(path).open("x", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=2, default=str)
        output.write("\n")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evidence_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("A timezone-aware evidence timestamp is required")
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("A timezone-aware evidence timestamp is required")
    return stamp


def fresh(value):
    stamp = evidence_timestamp(value)
    now = datetime.now(UTC)
    if stamp.tzinfo is None or not now - timedelta(days=1) <= stamp <= now + timedelta(minutes=5):
        raise ValueError("Evidence must be timezone-aware and no older than one day")
    return stamp


def require_fresh_entry(entry):
    fresh(entry["checked_at"])
    if entry["kind"] == "product" and entry["decision"] == "approve":
        for item in entry["evidence"].values():
            fresh(item["checked_at"])


def target(entry):
    return f"{TAG}:{entry['kind']}:{entry['id']}"


def indexed(data):
    result = {}
    for kind, collection in (("product", "products"), ("option", "options")):
        for row in data[collection]:
            key = (kind, str(row["id"]))
            if key in result:
                raise ValueError("Duplicate baseline identity")
            result[key] = row
    return result


def baseline_data(path):
    data = read_json(path)
    if digest(data) != BASELINE_HASH:
        raise ValueError("Not the pinned follow-up before.json semantic snapshot")
    rows = indexed(data)
    if len(data["products"]) != 60 or len(data["options"]) != 360:
        raise ValueError("Original hotel scope changed")
    pending = {key: row for key, row in rows.items() if row["status"] == "pending"}
    if sum(k[0] == "product" for k in pending) != 20 or len(pending) != 125:
        raise ValueError("Expected exactly 20 pending products and 105 pending options")
    if data["captured_at"] != BASELINE_CAPTURED_AT:
        raise ValueError("Unexpected follow-up snapshot capture time")
    return data, rows, pending


def template(data, pending):
    # A drafting aid only: remove every row without new evidence before applying.
    checks = {str(c["id"]): c for c in data.get("checks", [])}
    decisions = []
    for (kind, identifier), row in sorted(pending.items()):
        urls = (
            [row.get("source_url")]
            if kind == "product"
            else [row.get("url"), row.get("evidence_url")]
        )
        decisions.append(
            {
                "kind": kind,
                "id": identifier,
                "version": row["version"],
                "before_hash": digest(row),
                "new_evidence": "TEMPLATE: include only newly evidenced pending rows",
                "decision": "hold",
                "reason": "TEMPLATE: replace with the actual per-item review result",
                "source_urls": list(dict.fromkeys(u for u in urls if u)),
                "method": (
                    "missing_exact_identity"
                    if checks.get(identifier, {}).get("health") == "missing_exact_identity"
                    else "primary_web"
                ),
                "checked_at": None,
                "browser_verified": False,
            }
        )
    return {"schema_version": 1, "tag": TAG, "baseline_hash": digest(data), "decisions": decisions}


def validate_manifest(manifest, pending):
    if set(manifest) != {"schema_version", "tag", "baseline_hash", "decisions"}:
        raise ValueError("Unexpected manifest fields")
    if (
        manifest["schema_version"] != 1
        or manifest["tag"] != TAG
        or manifest["baseline_hash"] != BASELINE_HASH
    ):
        raise ValueError("Manifest tag/version/baseline mismatch")
    entries = manifest["decisions"]
    if not isinstance(entries, list) or not 1 <= len(entries) <= len(pending):
        raise ValueError("A nonempty subset of initially pending rows is required")
    seen = set()
    required = ENTRY_FIELDS - {"facts_patch", "option_patch", "evidence", "identity_note"}
    for entry in entries:
        if not required <= set(entry) or set(entry) - ENTRY_FIELDS:
            raise ValueError("Missing or unexpected decision fields")
        key = (entry["kind"], entry["id"])
        if key not in pending or key in seen or str(UUID(entry["id"])) != entry["id"]:
            raise ValueError("Unexpected, approved, or duplicate decision identity")
        seen.add(key)
        row = pending[key]
        if (
            type(entry["version"]) is not int
            or entry["version"] != row["version"]
            or entry["before_hash"] != digest(row)
        ):
            raise ValueError("Manifest full-row hash or version does not match baseline")
        if entry["decision"] not in {"approve", "hold"}:
            raise ValueError("Only approve or hold is authorized")
        if (
            not isinstance(entry["reason"], str)
            or not 12 <= len(entry["reason"]) <= 2000
            or "TEMPLATE:" in entry["reason"]
        ):
            raise ValueError("An actual, sufficiently specific review reason is required")
        if entry["method"] not in {"iab", "primary_web", "missing_exact_identity"}:
            raise ValueError("Unknown review method")
        # Old receipt content remains valid input for verification/replay. Age is
        # enforced only after absence of a receipt and immediately before a new write.
        if evidence_timestamp(entry["checked_at"]) <= evidence_timestamp(BASELINE_CAPTURED_AT):
            raise ValueError("Follow-up review must postdate the pinned baseline")
        if (
            not isinstance(entry["new_evidence"], str)
            or not 12 <= len(entry["new_evidence"].strip()) <= 1000
            or "TEMPLATE:" in entry["new_evidence"]
        ):
            raise ValueError("Describe the actual new evidence; do not re-audit unchanged holds")
        if type(entry["browser_verified"]) is not bool:
            raise ValueError("browser_verified must be an explicit boolean")
        if entry["browser_verified"] and entry["method"] != "iab":
            raise ValueError("Only actual built-in-browser evidence may use an override")
        urls = entry["source_urls"]
        if not isinstance(urls, list) or not 1 <= len(urls) <= 12 or len(set(urls)) != len(urls):
            raise ValueError("New evidence requires a bounded nonempty list of distinct URLs")
        for url in urls:
            safe_url(url)
        if entry["method"] == "missing_exact_identity":
            raise ValueError("Missing identity alone is not new evidence for this follow-up")
        if entry["decision"] == "hold":
            if "option_patch" in entry or any(
                entry.get(k) for k in ("facts_patch", "evidence", "identity_note")
            ):
                raise ValueError("A hold may only add an audit receipt, not modify a row")
            continue
        if not urls or entry["method"] == "missing_exact_identity":
            raise ValueError("An approval requires actual source evidence")
        if entry["kind"] == "option":
            if str(row["product_id"]) in OPERATING_DATE_HOLDS:
                raise ValueError("An unresolved operating-date hold cannot be overridden")
            if entry.get("facts_patch") or entry.get("evidence"):
                raise ValueError("Option review cannot edit product/URL/identity fields")
            if "option_patch" in entry:
                option_edit_payload(row, entry)
            elif (
                not row["url"]
                or not row["evidence_url"]
                or row["discovery_status"] != "found"
                or row["url"] not in urls
            ):
                raise ValueError("Exact existing found option URL evidence is required")
            note = entry.get("identity_note", "")
            if not isinstance(note, str) or not 12 <= len(note.strip()) <= 1000:
                raise ValueError("A specific <=1000 character option identity note is required")
            HotelOptionReview(
                version=entry["version"],
                status="approved",
                browser_verified=entry["browser_verified"],
                identity_note=note,
            )
        else:
            if entry.get("identity_note") or "option_patch" in entry:
                raise ValueError("Product cannot carry option edits or an option identity note")
            facts = entry.get("facts_patch", {})
            if not isinstance(facts, dict) or set(facts) - FACT_FIELDS:
                raise ValueError("This batch only permits the three exact CC0/map patches")
            product_payload(row, entry)
    # Deliberately do not audit unchanged holds absent from this explicit subset.


def option_edit_payload(row, entry):
    """Fill a pinned existing empty slot, never create/replace an identity or enable quotes."""
    patch = entry.get("option_patch")
    if (
        entry.get("kind") != "option"
        or entry.get("decision") != "approve"
        or entry.get("method") != "iab"
        or entry.get("browser_verified") is not True
        or row["status"] != "pending"
        or row["version"] < 1
        or row["discovery_status"] not in {"unconfirmed", "not_found"}
        or any(row.get(k) is not None for k in ("url", "property_id", "evidence_url"))
    ):
        raise ValueError("Only a pending empty identity slot with new IAB evidence may be filled")
    if not isinstance(patch, dict) or set(patch) != {"url", "evidence_url"}:
        raise ValueError("A null-slot patch must contain exactly url and evidence_url")
    if any(
        not isinstance(u, str) or not u.strip() or u not in entry["source_urls"]
        for u in patch.values()
    ):
        raise ValueError("Both new exact URLs must be present in the reviewed source list")
    note = entry.get("identity_note", "")
    if not isinstance(note, str) or not 12 <= len(note.strip()) <= 1000:
        raise ValueError("A specific identity note is required for the new slot")
    payload = HotelOptionEdit(
        version=row["version"],
        provider=row["provider"],
        url=patch["url"],
        property_id=None,
        evidence_url=patch["evidence_url"],
        identity_note=note,
        discovery_status="found",
    )
    if payload.url != patch["url"] or payload.evidence_url != patch["evidence_url"]:
        raise ValueError("Use the exact canonical URLs validated by the normal schema")
    return payload


def product_payload(row, entry):
    if set(entry.get("facts_patch", {})) - FACT_FIELDS:
        raise ValueError("This batch cannot alter unapproved coordinate/source/area fields")
    if entry.get("method") != "iab" or entry.get("browser_verified") is not True:
        raise ValueError("Product approval requires actual built-in-browser identity")
    data = {
        key: copy.deepcopy(row[key])
        for key in (
            "source_key",
            "kind",
            "destination_id",
            "title",
            "names_json",
            "source_url",
            "facts",
        )
    }
    # An explicit empty legacy hotel_links list DISABLES independent booking options.
    data["facts"].pop("hotel_links", None)
    data["facts"].update(copy.deepcopy(entry.get("facts_patch", {})))
    payload = ProductInput.model_validate(data)
    if "hotel_links" in payload.facts.model_fields_set:
        raise ValueError("Legacy option replacement must never be requested")
    evidence = entry.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"map", "coordinates"}:
        raise ValueError("Product approval needs map and durable-coordinate evidence")
    map_info, coords = evidence["map"], evidence["coordinates"]
    if not isinstance(map_info, dict) or set(map_info) != {
        "url",
        "identity_verified",
        "method",
        "checked_at",
        "place_id",
    }:
        raise ValueError("Exact map evidence fields required")
    if (
        not isinstance(map_info, dict)
        or not isinstance(coords, dict)
        or map_info.get("identity_verified") is not True
        or map_info.get("method") != "iab"
        or coords.get("non_google") is not True
    ):
        raise ValueError("Explicit IAB identity and non-Google durable coordinates required")
    for item in (map_info, coords):
        safe_url(item["url"])
        evidence_timestamp(item["checked_at"])
        if item["url"] not in entry["source_urls"]:
            raise ValueError("Evidence URLs must also be listed in source_urls")
    validate_coordinate_evidence(row, payload, coords)
    if CITIES[payload.destination_id][0] == "KR":

        def naver_id(url):
            match = re.fullmatch(
                r"https://map\.naver\.com/(?:p|v5)/entry/place/(\d+)/?(?:\?.*)?", url or ""
            )
            return match.group(1) if match else None

        if not naver_id(payload.facts.naver_map_url) or naver_id(map_info["url"]) != naver_id(
            payload.facts.naver_map_url
        ):
            raise ValueError("The independently viewed exact Naver identity must match")
    elif (
        not payload.facts.google_place_id
        or map_info.get("place_id") != payload.facts.google_place_id
    ):
        raise ValueError("Observed Google Place ID must be explicitly bound to map evidence")
    require_product_review(payload)
    source = payload.facts.coordinate_source_url
    if urlsplit(source).hostname != urlsplit(payload.source_url).hostname:
        if not any(c.url == source and c.license_url for c in payload.facts.source_credits):
            raise ValueError("Independent coordinate source attribution/license is missing")
    return payload


def coordinate_source(allowed):
    return (
        f"https://www.wikidata.org/wiki/Special:EntityData/{allowed['qid']}.json"
        f"?revision={allowed['revision']}"
    )


def coordinate_credit(allowed):
    return {
        "title": f"Wikidata {allowed['qid']} P625 representative hotel point",
        "publisher": "Wikidata contributors",
        "url": coordinate_source(allowed),
        "license_name": "CC0-1.0",
        "license_url": COORDINATE_LICENSE_URL,
        "changes": (
            f"Selected P625 claim {allowed['claim_id']}, revision {allowed['revision']}; "
            "P143 imported from Japanese Wikipedia (Q177837). Alternative P248 "
            "Skyscanner (Q1319169) claims excluded. Representative hotel point, "
            "not a surveyed entrance; original municipal name/address credit retained."
        ),
    }


def coordinate_patch(row):
    """Canonical permitted coordinate fields; caller adds IAB Google identity."""
    allowed = COORDINATE_ROWS.get(str(row["id"]))
    if allowed is None or digest(row) != allowed["row_hash"]:
        raise ValueError("Only the three exact pending Kyoto baseline rows are allowed")
    return {
        "latitude": allowed["latitude"],
        "longitude": allowed["longitude"],
        "coordinate_source_url": coordinate_source(allowed),
        "source_credits": copy.deepcopy(row["facts"]["source_credits"])
        + [coordinate_credit(allowed)],
    }


def coordinate_evidence(row, checked_at):
    allowed = COORDINATE_ROWS.get(str(row["id"]))
    if allowed is None:
        raise ValueError("Coordinate identity is not allowlisted")
    return {
        "url": coordinate_source(allowed),
        "license_url": COORDINATE_LICENSE_URL,
        "non_google": True,
        "checked_at": checked_at,
        "qid": allowed["qid"],
        "claim_id": allowed["claim_id"],
        "revision": allowed["revision"],
        "reference": "P143:Q177837",
    }


def validate_coordinate_evidence(row, payload, evidence):
    allowed = COORDINATE_ROWS.get(str(row["id"]))
    if allowed is None:
        raise ValueError("Only three pinned Kyoto CC0 coordinate claims may be approved")
    expected = coordinate_evidence(row, evidence.get("checked_at"))
    if evidence != expected or type(evidence.get("revision")) is not int:
        raise ValueError("Coordinate claim/revision/source/license is not allowlisted")
    patch = coordinate_patch(row)
    facts = payload.facts.model_dump(mode="json")
    if (
        payload.kind != "hotel"
        or payload.source_key != allowed["source_key"]
        or payload.destination_id != "kyoto"
        or digest(row["facts"].get("source_credits")) != ORIGINAL_CREDITS_HASH
        or any(facts[k] != v for k, v in patch.items())
    ):
        raise ValueError("Coordinate identity/value/source/license/attribution is not allowlisted")


async def actor_for(session, *, require_fresh=False):
    # ROOT is solely evidence of the real authenticated admin, not hotel membership.
    root = await session.get(CatalogReviewRun, ROOT)
    if root is None or root.mode != "review_pending":
        raise RuntimeError("Authenticated root review is missing")
    if require_fresh:
        fresh(str(root.created_at))
    actor = await session.get(User, root.actor_user_id, populate_existing=True)
    audit = await session.scalar(
        select(AdminAuditLog.id).where(
            AdminAuditLog.actor_user_id == root.actor_user_id,
            AdminAuditLog.action == "catalog_review_requested",
            AdminAuditLog.target == f"catalog-review:{ROOT}",
        )
    )
    if actor is None or not actor.is_active or not is_admin_user(actor) or audit is None:
        raise RuntimeError("Current administrator/authenticated request evidence is invalid")
    return actor


async def inventory(session, lock=False):
    def query(model, order):
        statement = select(model).order_by(order).execution_options(populate_existing=True)
        return statement.with_for_update() if lock else statement

    # Lock parents before options, consistent with normal independent option edits.
    products = list(
        (
            await session.scalars(
                query(TravelServiceProduct, TravelServiceProduct.id).where(
                    TravelServiceProduct.kind == "hotel"
                )
            )
        ).all()
    )
    options = list(
        (
            await session.scalars(
                query(HotelBookingOption, HotelBookingOption.id).where(
                    HotelBookingOption.product_id.in_([p.id for p in products])
                )
            )
        ).all()
    )
    configs = list(
        (await session.scalars(query(TravelServiceConfig, TravelServiceConfig.id))).all()
    )
    data = normalized(
        {
            "products": [record(p) for p in products],
            "options": [record(o) for o in options],
            "configs": [record(c) for c in configs],
        }
    )
    objects = {("product", str(p.id)): p for p in products}
    objects.update({("option", str(o.id)): o for o in options})
    return data, objects


async def receipts_for(session, manifest, actor_id):
    entries = {target(e): e for e in manifest["decisions"]}
    rows = list(
        (
            await session.scalars(
                select(AdminAuditLog).where(
                    AdminAuditLog.action == ACTION, AdminAuditLog.target.like(f"{TAG}:%")
                )
            )
        ).all()
    )
    result = {}
    for receipt in rows:
        meta = receipt.metadata_json
        entry = entries.get(receipt.target)
        if (
            entry is None
            or receipt.target in result
            or receipt.actor_user_id != actor_id
            or meta.get("baseline_hash") != BASELINE_HASH
            or meta.get("entry_hash") != digest(entry)
            or meta.get("before_hash") != entry["before_hash"]
            or meta.get("before_version") != entry["version"]
            or meta.get("root_run_id") != str(ROOT)
            or meta.get("outcome") not in {"approved", "hold"}
            or not re.fullmatch(r"[0-9a-f]{64}", meta.get("after_hash", ""))
        ):
            raise RuntimeError("Receipt conflict, duplicate, actor mismatch, or edited decision")
        if meta["outcome"] == "hold" and (
            meta["after_hash"] != meta["before_hash"]
            or meta.get("after_version") != meta["before_version"]
        ):
            raise RuntimeError("A hold receipt must attest an unchanged row")
        if meta["outcome"] == "approved" and (
            entry["decision"] != "approve"
            or type(meta.get("after_version")) is not int
            or meta["after_version"] <= meta["before_version"]
        ):
            raise RuntimeError("An approval receipt must attest a versioned approval")
        result[receipt.target] = receipt
    return result


def verify_state(data, baseline, baseline_rows, manifest, receipts, ignore=None):
    current = indexed(data)
    if set(current) != set(baseline_rows):
        raise RuntimeError("Hotel catalog membership changed")
    if digest(sorted(data["configs"], key=lambda c: c["id"])) != digest(
        sorted(baseline["configs"], key=lambda c: c["id"])
    ):
        raise RuntimeError("Configuration changed; stop and inspect")
    expected = {key: digest(row) for key, row in baseline_rows.items()}
    for entry in manifest["decisions"]:
        receipt = receipts.get(target(entry))
        if receipt:
            expected[(entry["kind"], entry["id"])] = receipt.metadata_json["after_hash"]
    for key, row in current.items():
        if key != ignore and digest(row) != expected[key]:
            raise RuntimeError(f"Full-row snapshot changed: {key[0]}:{key[1]}")
    return current


def duplicate_map(payload, products):
    facts = payload.facts
    candidate_naver = re.search(r"/entry/place/(\d+)", facts.naver_map_url or "")
    for row in products:
        if row["source_key"] == payload.source_key:
            continue
        other = row["facts"]
        other_naver = re.search(r"/entry/place/(\d+)", other.get("naver_map_url") or "")
        if (facts.google_place_id and facts.google_place_id == other.get("google_place_id")) or (
            candidate_naver and other_naver and candidate_naver[1] == other_naver[1]
        ):
            raise RuntimeError(f"Duplicate map identity with hotel {row['id']}")


class DeferredCommit:
    """Pass-through session whose normal route commits only flush our transaction."""

    def __init__(self, session):
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session, name)

    async def commit(self):
        await self.session.flush()


def allowed_result(before, after, entry):
    if entry["kind"] == "option":
        changed = {
            "identity_note",
            "status",
            "version",
            "verified_at",
            "checked_at",
            "health_status",
            "updated_at",
        }
        patch = entry.get("option_patch")
        if patch:
            option_edit_payload(before, entry)
            changed |= {"url", "evidence_url", "discovery_status"}
            if (
                any(after.get(k) != v for k, v in patch.items())
                or after["property_id"] is not None
                or after["discovery_status"] != "found"
            ):
                raise RuntimeError("New slot did not preserve exact reviewed URLs and quote guard")
        if after["version"] != before["version"] + (2 if patch else 1):
            raise RuntimeError("Unexpected independent option version increment")
        if (
            after["identity_note"] != entry["identity_note"]
            or (after["health_status"] != "healthy" and not entry["browser_verified"])
            or after["health_status"] in {"unsafe", "unavailable"}
        ):
            raise RuntimeError("Option approval did not preserve identity/health guards")
    else:
        changed = {"facts", "status", "version", "verified_at", "updated_at"}
        old_facts, new_facts = copy.deepcopy(before["facts"]), copy.deepcopy(after["facts"])
        for field, expected in entry.get("facts_patch", {}).items():
            if new_facts.get(field) != expected:
                raise RuntimeError("Normal route did not persist the exact authorized fact")
            old_facts.pop(field, None)
            new_facts.pop(field, None)
        if old_facts != new_facts:
            raise RuntimeError("Product edit changed non-authorized facts")
    if {k: v for k, v in before.items() if k not in changed} != {
        k: v for k, v in after.items() if k not in changed
    }:
        raise RuntimeError("Normal route changed fields outside the authorized scope")
    if after["status"] != "approved" or after["version"] <= before["version"]:
        raise RuntimeError("Normal review did not produce a versioned approval")


async def lock_entry(session, entry):
    lock_key = int.from_bytes(
        hashlib.sha256(target(entry).encode()).digest()[:8], "big", signed=True
    )
    await session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_key})


async def add_receipt(session, actor, entry, before, after, outcome, guard_code=None):
    receipt = AdminAuditLog(
        actor_user_id=actor.id,
        action=ACTION,
        target=target(entry),
        metadata_json={
            "tag": TAG,
            "root_run_id": str(ROOT),
            "baseline_hash": BASELINE_HASH,
            "entry_hash": digest(entry),
            "kind": entry["kind"],
            "target_id": entry["id"],
            "requested_decision": entry["decision"],
            "outcome": outcome,
            "reason": entry["reason"],
            "new_evidence": entry["new_evidence"],
            "source_urls": entry["source_urls"],
            "method": entry["method"],
            "evidence_checked_at": entry["checked_at"],
            "browser_verified": entry["browser_verified"] if outcome == "approved" else False,
            "evidence": entry.get("evidence"),
            "option_patch": entry.get("option_patch"),
            "before_hash": digest(before),
            "after_hash": digest(after),
            "before_version": before["version"],
            "after_version": after["version"],
            "guard_code": guard_code,
        },
    )
    session.add(receipt)
    await session.flush()
    return receipt


async def process_entry(entry, baseline, baseline_rows, manifest, apply, fallback_code=None):
    async with SessionFactory() as session:
        await lock_entry(session, entry)
        actor = await actor_for(session)
        data, objects = await inventory(session, lock=True)
        receipts = await receipts_for(session, manifest, actor.id)
        current = verify_state(data, baseline, baseline_rows, manifest, receipts)
        key = (entry["kind"], entry["id"])
        before, row = current[key], objects[key]
        previous = receipts.get(target(entry))
        if previous:
            emit(
                {
                    "target": target(entry),
                    "outcome": "replayed",
                    "receipt_id": previous.id,
                    "after_hash": digest(before),
                }
            )
            return
        if apply:
            # Receipt replay above performs no write and does not renew evidence.
            # New approvals AND new hold receipts still need fresh authorization.
            actor = await actor_for(session, require_fresh=True)
            require_fresh_entry(entry)
        if before["status"] != "pending":
            raise RuntimeError("An already-reviewed row may not be modified")
        payload = None
        edit_payload = None
        if entry["decision"] == "approve" and not fallback_code:
            if entry["kind"] == "product":
                payload = product_payload(before, entry)
                duplicate_map(payload, data["products"])
            else:
                if "option_patch" in entry:
                    edit_payload = option_edit_payload(before, entry)
                payload = HotelOptionReview(
                    version=entry["version"],
                    status="approved",
                    browser_verified=entry["browser_verified"],
                    identity_note=entry["identity_note"],
                )
        if not apply:
            emit(
                {
                    "target": target(entry),
                    "decision": entry["decision"],
                    "before_hash": digest(before),
                    "mode": "dry-run",
                }
            )
            return
        outcome = "hold"
        if payload is not None:
            deferred = DeferredCommit(session)
            if entry["kind"] == "product":
                if entry.get("facts_patch"):
                    await admin.edit_product(
                        product_id=row.id,
                        payload=payload,
                        version=row.version,
                        user=actor,
                        session=deferred,
                    )
                await admin.review_product(
                    product_id=row.id,
                    payload=ReviewInput(version=row.version, status="approved"),
                    user=actor,
                    session=deferred,
                )
            else:
                if edit_payload is not None:
                    edited = await admin.edit_hotel_option(
                        product_id=row.product_id,
                        payload=edit_payload,
                        user=actor,
                        session=deferred,
                    )
                    if str(edited["id"]) != str(row.id):
                        raise RuntimeError(
                            "Normal edit attempted to create or replace the pinned slot"
                        )
                    await session.flush()
                    await session.refresh(row)
                    if (
                        row.version != before["version"] + 1
                        or str(row.product_id) != before["product_id"]
                        or row.provider != before["provider"]
                    ):
                        raise RuntimeError("Normal edit changed slot ownership/version")
                    payload = payload.model_copy(update={"version": row.version})
                await admin.review_hotel_option(
                    product_id=row.product_id,
                    option_id=row.id,
                    payload=payload,
                    user=actor,
                    session=deferred,
                )
            await session.flush()
            await session.refresh(row)
            outcome = "approved"
        after = normalized(record(row))
        if outcome == "approved":
            allowed_result(before, after, entry)
        elif before != after:
            raise RuntimeError("Hold must not mutate the target")
        post, _ = await inventory(session)
        verify_state(post, baseline, baseline_rows, manifest, receipts, ignore=key)
        if digest(indexed(post)[key]) != digest(after):
            raise RuntimeError("Post-refresh target hash changed")
        receipt = await add_receipt(session, actor, entry, before, after, outcome, fallback_code)
        receipt_id = receipt.id
        await session.commit()
        emit(
            {
                "target": target(entry),
                "outcome": outcome,
                "receipt_id": receipt_id,
                "after_hash": digest(after),
                "guard_code": fallback_code,
            }
        )


async def review_all(args, baseline, baseline_rows, pending):
    manifest = read_json(args.manifest)
    validate_manifest(manifest, pending)
    if args.mode == "verify":
        async with SessionFactory() as session:
            actor = await actor_for(session)
            data, _ = await inventory(session)
            receipts = await receipts_for(session, manifest, actor.id)
            verify_state(data, baseline, baseline_rows, manifest, receipts)
            expected = len(manifest["decisions"])
            if len(receipts) != expected:
                raise RuntimeError(f"Only {len(receipts)}/{expected} terminal review receipts")
            emit(
                {
                    "verified": expected,
                    "untouched_rows": 420 - expected,
                    "catalog_rows": 420,
                    "configs_unchanged": True,
                    "approved": sum(
                        r.metadata_json["outcome"] == "approved" for r in receipts.values()
                    ),
                    "hold": sum(r.metadata_json["outcome"] == "hold" for r in receipts.values()),
                }
            )
        return
    # Stable order also makes all product reviews precede their independent options.
    for entry in sorted(manifest["decisions"], key=lambda e: (e["kind"] == "option", e["id"])):
        try:
            await process_entry(entry, baseline, baseline_rows, manifest, args.mode == "apply")
        except AppError as exc:
            # Version conflicts, unknown errors and programming bugs MUST stop, not become holds.
            if (
                args.mode != "apply"
                or entry["decision"] != "approve"
                or exc.code not in GUARD_CODES
            ):
                raise
            # Failed normal review session has rolled back on context exit. Re-lock/re-check
            # the unchanged full baseline in a fresh transaction before recording a hold.
            await process_entry(entry, baseline, baseline_rows, manifest, True, exc.code)


async def snapshot():
    async with SessionFactory() as session:
        data, _ = await inventory(session)
        data["captured_at"] = datetime.now(UTC)
        return data


async def capture(args):
    data = await snapshot()
    if len(data["products"]) != 60 or len(data["options"]) != 360:
        raise RuntimeError("Catalog changed: manually re-scope before continuing")
    if args.mode == "check":
        semaphore = asyncio.Semaphore(3)

        async def check(option):
            if option["status"] != "pending":
                return None
            result = {
                "id": option["id"],
                "product_id": option["product_id"],
                "provider": option["provider"],
                "version": option["version"],
                "before_hash": digest(option),
                "checked_at": datetime.now(UTC),
            }
            if option["discovery_status"] != "found" or not option["url"]:
                result["health"] = "missing_exact_identity"
            else:
                async with semaphore:
                    try:
                        result["health"] = await check_hotel_link(
                            HotelLink(
                                provider=option["provider"],
                                url=option["url"],
                                evidence_url=option["evidence_url"],
                            )
                        )
                    except Exception as exc:
                        # Read-only diagnostics retain unknown failures, never approve them.
                        result["health"] = "unconfirmed"
                        result["error_type"] = type(exc).__name__
            emit(result)
            return result

        data["checks"] = [
            r for r in await asyncio.gather(*(check(o) for o in data["options"])) if r is not None
        ]
    save_new(args.output, data)
    emit(
        {
            "output": args.output,
            "products": len(data["products"]),
            "options": len(data["options"]),
            "hash": digest(data),
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        default="snapshot",
        choices=["snapshot", "check", "dry-run", "apply", "verify"],
    )
    parser.add_argument("--output")
    parser.add_argument("--baseline")
    parser.add_argument("--manifest")
    parser.add_argument("--emit-template", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.mode == "apply" and not args.apply:
        parser.error("Writing requires both apply mode and --apply")
    if args.apply and args.mode != "apply":
        parser.error("--apply is only valid in apply mode")
    if args.emit_template or args.mode in {"dry-run", "apply", "verify"}:
        if not args.baseline:
            parser.error("--baseline before.json is required")
        baseline, baseline_rows, pending = baseline_data(args.baseline)
        if args.emit_template:
            if args.apply or not args.output:
                parser.error("--emit-template requires --output and forbids --apply")
            save_new(args.output, template(baseline, pending))
            emit(
                {"template": args.output, "decisions": len(pending), "baseline_hash": BASELINE_HASH}
            )
            return
        if not args.manifest:
            parser.error("--manifest is required")
    elif not args.output:
        parser.error("Read-only snapshot/check requires a new --output file")

    async def execute():
        try:
            if args.mode in {"snapshot", "check"}:
                await capture(args)
            else:
                await review_all(args, baseline, baseline_rows, pending)
        finally:
            await engine.dispose()

    asyncio.run(execute())


if __name__ == "__main__":
    main()
