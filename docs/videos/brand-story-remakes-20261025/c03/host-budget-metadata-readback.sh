#!/usr/bin/env bash
# Run only through an already established production-host connection.
# No deploy/build/restart, provider request, reconciliation or DB data mutation.
set -u
umask 077

c03_probe_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || exit 4
c03_probe_python="$c03_probe_dir/host-budget-metadata-readback.py"
c03_expected_probe_sha256="d7c791cf6c34d2a9e043403e297cf1dfeadc15e0a7dfa93005bedbd7be3632ee"
if ! command -v python3 >/dev/null 2>&1 || ! command -v docker >/dev/null 2>&1; then
  printf '{"result":"UNKNOWN","production_authorized":false,"reason_code":"host_prerequisite_unavailable"}\n'
  exit 4
fi
c03_actual_probe_sha256="$(python3 - "$c03_probe_python" 2>/dev/null <<'PY'
import hashlib, pathlib, sys
try:
    print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
except BaseException:
    raise SystemExit(4)
PY
)" || exit 4
if [ "$c03_actual_probe_sha256" != "$c03_expected_probe_sha256" ]; then
  printf '{"result":"UNKNOWN","production_authorized":false,"reason_code":"probe_source_hash_mismatch"}\n'
  exit 4
fi
cd /root/travel_scanner 2>/dev/null || exit 4
c03_readback_dir="$(mktemp -d /tmp/c03-budget-metadata.XXXXXX)" || exit 4
c03_compose=(docker compose -f docker-compose.prod.yml)
c03_host_sha="$(git rev-parse HEAD 2>/dev/null)" || c03_host_sha="UNKNOWN"
if [[ ! "$c03_host_sha" =~ ^[0-9a-f]{40}$ ]]; then c03_host_sha="UNKNOWN"; fi

# Only four explicitly named, non-secret container metadata fields are inspected.
for c03_service in api video-worker; do
  c03_container="$("${c03_compose[@]}" ps -q "$c03_service" 2>/dev/null)" || c03_container=""
  c03_container_data=""
  if [[ "$c03_container" =~ ^[0-9a-f]{12,64}$ ]]; then
    c03_container_data="$(docker inspect --format '{{.Id}} {{.Image}} {{.Config.Image}} {{.State.Running}}' "$c03_container" 2>/dev/null)" || c03_container_data=""
  fi
  python3 - "$c03_service" "$c03_container_data" > "$c03_readback_dir/$c03_service-container.json" <<'PY'
import json, re, sys
service, raw = sys.argv[1:]
parts = raw.split()
result = {"service": service, "status": "UNKNOWN"}
if (len(parts) == 4 and re.fullmatch(r"[0-9a-f]{64}", parts[0])
        and re.fullmatch(r"sha256:[0-9a-f]{64}", parts[1])
        and re.fullmatch(r"travel-scanner-(?:api|video-worker):[A-Za-z0-9_.-]{1,100}", parts[2])
        and parts[3] in {"true", "false"}):
    result.update(status="OBSERVED", container_id=parts[0], image_id=parts[1],
                  image_reference=parts[2], running=parts[3] == "true")
print(json.dumps(result, sort_keys=True))
PY
done

# The script travels on stdin; it is not installed/copied into the running image.
# Stderr is discarded so a driver/connection error cannot leak a DSN or traceback.
"${c03_compose[@]}" exec -T api python - < "$c03_probe_python" \
  > "$c03_readback_dir/api-budget-metadata.json" 2>/dev/null
c03_api_exit=$?

"${c03_compose[@]}" exec -T video-worker node --input-type=module \
  > "$c03_readback_dir/worker-budget-registry.json" 2>/dev/null <<'NODE'
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";
const slugs = ["story-everyday-moleskine-c03", "story-everyday-moleskine-c03-remake-20261025"];
const expected = "58273eb487f49bf94ca917a541e8df570a403056f744fdb8437e430f955eae93";
const output = { status: "UNKNOWN", production_authorized: false };
try {
  const source = path.resolve("tools/video/core/pending-pilot-budget.mjs");
  output.guard_sha256 = createHash("sha256").update(fs.readFileSync(source)).digest("hex");
  output.reviewed_guard_matches = output.guard_sha256 === expected;
  output.node_version = /^v[0-9.]+$/.test(process.version) ? process.version : "UNKNOWN";
  if (!output.reviewed_guard_matches) {
    output.reason_code = "worker_guard_changed_requires_review";
    process.exitCode = 4;
  } else {
    const guard = await import(pathToFileURL(source).href);
    output.slugs = slugs.map(slug => ({
      slug, preproduction_held: Boolean(guard.isPreproductionHeld(slug)),
      activated_exact_slug: guard.ACTIVATED_STORY_SLUGS.includes(slug),
    }));
    output.status = "READ_ONLY_METADATA_OBTAINED";
    process.exitCode = output.slugs.some(row => row.preproduction_held) ? 3 : 0;
  }
} catch {
  output.reason_code = "worker_registry_unavailable";
  process.exitCode = 4;
}
console.log(JSON.stringify(output));
NODE
c03_worker_exit=$?

# Project every component onto an explicit output allowlist before retaining or
# printing the summary. Unknown fields/revision strings are never passed through.
python3 - "$c03_readback_dir" "$c03_host_sha" "$c03_api_exit" "$c03_worker_exit" \
  "$c03_actual_probe_sha256" 2>/dev/null <<'PY'
import json, pathlib, re, sys
directory = pathlib.Path(sys.argv[1])
slugs = ("story-everyday-moleskine-c03", "story-everyday-moleskine-c03-remake-20261025")
revisions = {"0132_video_pilot_budget", "0133_story_followon_budget", "0137_video_manga_tier",
             "0138_story_everyday_budget", "0139_c20_zippo_pilot_budget", "0140_c08_kikkoman_pilot_budget"}
baseline = {
    "models": "8eaad7c3c125ee206d2896f4fa31e8e05e4e4af6d7b038801566b2646485d98e",
    "service": "1b3043b58f2811e8a2176bb210c34cb7b0ef26928c79f7c7bf51fcb4aaf4cecf",
    "db": "5fa7d7036175ab6a891408982d2eac27b8dfcebefc5791c2e04db15f82584997",
    "schema": "9deef8ae92447bde10916d7383c62a939d7153587ae5458715b9a15df313f9a2",
}
allowed_reasons = {
    "account_missing", "metadata_not_read", "schema_not_compatible",
    "invalid_or_incomplete_ledger_aggregate", "probe_does_not_authorize_provider_dispatch",
    "api_preproduction_held_or_unknown", "exact_slug_not_registered_at_usd25",
    "db_cap_does_not_match_reviewed_exact_slug_usd25", "ledger_overrun",
    "deployed_budget_semantics_not_bound_to_reviewed_source",
    "old_preledger_history_missing_or_not_exact_full_usd25",
    "old_preledger_full_usd25_still_uncertain", "unsupported_database_backend",
    "read_only_transaction_not_verified", "probe_unavailable_or_interrupted",
    "worker_guard_changed_requires_review", "worker_registry_unavailable",
    "component_metadata_unavailable", "component_reason_unrecognized",
}
def mapping(value): return value if isinstance(value, dict) else {}
def array(value): return value if isinstance(value, list) else []
def flag(value): return value if type(value) is bool else None
def count(value): return value if type(value) is int and 0 <= value <= 1000000000 else None
def number(value): return value if isinstance(value, str) and re.fullmatch(r"-?[0-9]{1,20}\.[0-9]{6}", value) else None
def digest(value): return value if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) else None
def choice(value, allowed): return value if isinstance(value, str) and value in allowed else None
def reason(value): return choice(value, allowed_reasons) or "component_reason_unrecognized"
def read(name):
    try:
        return mapping(json.loads((directory / name).read_text()))
    except BaseException:
        return {"result": "UNKNOWN", "reason_code": "component_metadata_unavailable"}
def account(raw, slug):
    raw = mapping(raw)
    reg = mapping(raw.get("registry"))
    output = {"slug": slug, "account_exists": flag(raw.get("account_exists")),
              "metadata_status": choice(raw.get("metadata_status"), {"UNKNOWN", "NOT_READY", "READ_ONLY_METADATA_OBTAINED"}) or "UNKNOWN",
              "paid_dispatch_readiness": "NOT_READY", "available_is_payment_authority": False,
              "registry": {"registered_cap_usd": number(reg.get("registered_cap_usd")),
                           "activated_exact_slug": flag(reg.get("activated_exact_slug")),
                           "preproduction_held": flag(reg.get("preproduction_held"))},
              "reason_codes": sorted({reason(item) for item in array(raw.get("reason_codes"))})}
    for key in ("cap_usd", "settled_usd", "settled_including_closed_history_usd", "reserved_usd", "reserved_only_usd",
                "uncertain_usd", "historical_closed_usd", "old_preledger_uncertain_usd", "available_usd",
                "observed_ledger_remaining_usd", "admissible_available_usd"):
        output[key] = number(raw.get(key))
    for key in ("uncertain_operations", "old_preledger_uncertain_operations", "operation_count", "overrun_operations"):
        output[key] = count(raw.get(key))
    output["old_preledger_verification"] = choice(raw.get("old_preledger_verification"), {
        "NOT_APPLICABLE", "EXACT_FULL_USD25_CLOSURE", "FULL_USD25_UNCERTAIN_HOLD", "MISSING_OR_ANOMALOUS"})
    output["available_calculation"] = choice(raw.get("available_calculation"), {
        "stored_cap_minus_settled_excluding_exact_full_usd25_owner_closed_history_minus_reserved_including_uncertain",
        "conservative_stored_cap_minus_all_settled_minus_reserved_including_uncertain"})
    return output
def safe_api(raw):
    tx, sc = mapping(raw.get("transaction")), mapping(raw.get("schema"))
    observed = array(sc.get("current_revisions"))[:16]
    known = [r for r in observed if isinstance(r, str) and r in revisions]
    unknown = min(16, (count(sc.get("unknown_revision_count")) or 0) + len(observed) - len(known))
    expected = choice(sc.get("expected_revision"), revisions)
    hashes = {key: digest(mapping(raw.get("source_sha256")).get(key)) for key in baseline}
    accounts = array(raw.get("accounts"))
    by_slug = {row.get("slug"): row for row in accounts if isinstance(row, dict) and row.get("slug") in slugs}
    result = {"probe": "c03-fixed-slug-budget-metadata-v2", "result": "NOT_READY",
              "production_authorized": False, "source_sha256": hashes,
              "baseline_commit": "8c338dfc264dedaf200e4e50da816631285c207a",
              "reviewed_budget_semantics_match": raw.get("reviewed_budget_semantics_match") is True and hashes == baseline,
              "transaction": {"read_only": choice(tx.get("read_only"), {"on", "off"}),
                              "isolation": choice(tx.get("isolation"), {"repeatable read", "read committed", "serializable"}),
                              "verified": tx.get("verified") is True and tx.get("read_only") == "on" and tx.get("isolation") == "repeatable read"},
              "schema": {"current_revisions": known, "unknown_revision_count": unknown,
                         "expected_revision": expected, "required_columns_match": flag(sc.get("required_columns_match")),
                         "compatible": sc.get("compatible") is True and len(known) == 1 and unknown == 0 and expected is not None},
              "accounts": [account(by_slug.get(s), s) for s in slugs]}
    if isinstance(raw.get("python_version"), str) and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", raw["python_version"]):
        result["python_version"] = raw["python_version"]
    if "reason_code" in raw: result["reason_code"] = reason(raw["reason_code"])
    return result
def safe_worker(raw):
    rows = array(raw.get("slugs"))
    by_slug = {row.get("slug"): row for row in rows if isinstance(row, dict) and row.get("slug") in slugs}
    output = {"status": choice(raw.get("status"), {"UNKNOWN", "READ_ONLY_METADATA_OBTAINED"}) or "UNKNOWN",
              "production_authorized": False, "guard_sha256": digest(raw.get("guard_sha256")),
              "reviewed_guard_matches": raw.get("reviewed_guard_matches") is True and raw.get("guard_sha256") == "58273eb487f49bf94ca917a541e8df570a403056f744fdb8437e430f955eae93",
              "slugs": [{"slug": s, "preproduction_held": flag(mapping(by_slug.get(s)).get("preproduction_held")),
                         "activated_exact_slug": flag(mapping(by_slug.get(s)).get("activated_exact_slug"))} for s in slugs]}
    if isinstance(raw.get("node_version"), str) and re.fullmatch(r"v[0-9.]+", raw["node_version"]): output["node_version"] = raw["node_version"]
    if "reason_code" in raw: output["reason_code"] = reason(raw["reason_code"])
    return output
def safe_container(raw, service):
    output = {"service": service, "status": "UNKNOWN"}
    if (raw.get("status") == "OBSERVED" and digest(raw.get("container_id"))
            and isinstance(raw.get("image_id"), str) and re.fullmatch(r"sha256:[0-9a-f]{64}", raw["image_id"])
            and isinstance(raw.get("image_reference"), str) and re.fullmatch(r"travel-scanner-(?:api|video-worker):[A-Za-z0-9_.-]{1,100}", raw["image_reference"])
            and type(raw.get("running")) is bool):
        output.update({key: raw[key] for key in ("container_id", "image_id", "image_reference", "running")}, status="OBSERVED")
    return output
api = safe_api(read("api-budget-metadata.json"))
worker = safe_worker(read("worker-budget-registry.json"))
containers = [safe_container(read(service + "-container.json"), service) for service in ("api", "video-worker")]
api_complete = (api["transaction"]["verified"] is True and api["schema"]["compatible"] is True
            and api["schema"]["required_columns_match"] is True and api["reviewed_budget_semantics_match"] is True
            and all(a["account_exists"] is True and a["metadata_status"] == "READ_ONLY_METADATA_OBTAINED"
                    and all(a[k] is not None for k in ("cap_usd", "settled_usd", "reserved_usd", "uncertain_usd", "available_usd", "uncertain_operations")) for a in api["accounts"]))
api["metadata_complete"] = api_complete
api["result"] = "NOT_READY" if api_complete else "UNKNOWN"
complete = (sys.argv[3] == "3" and sys.argv[4] in {"0", "3"} and api_complete
            and worker["status"] == "READ_ONLY_METADATA_OBTAINED" and worker["reviewed_guard_matches"] is True
            and all(row["preproduction_held"] is not None and row["activated_exact_slug"] is not None for row in worker["slugs"])
            and all(c.get("status") == "OBSERVED" and c.get("running") is True for c in containers))
summary = {"probe": "c03-fixed-slug-host-readback-v2", "result": "NOT_READY" if complete else "UNKNOWN",
           "metadata_complete": complete,
           "production_authorized": False, "host_git_sha": sys.argv[2],
           "python_probe_sha256": sys.argv[5], "component_exit_codes": {
               "api": int(sys.argv[3]), "worker": int(sys.argv[4])},
           "containers": containers, "api": api, "worker": worker,
           "private_results_directory": str(directory)}
for name, data in (("api-budget-metadata.json", api), ("worker-budget-registry.json", worker),
                   ("api-container.json", containers[0]), ("video-worker-container.json", containers[1])):
    (directory / name).write_text(json.dumps(data, sort_keys=True) + "\n")
with (directory / "safe-summary.json").open("x") as handle:
    json.dump(summary, handle, sort_keys=True, indent=2)
print(json.dumps(summary, sort_keys=True))
raise SystemExit(3 if complete else 4)
PY
exit $?
