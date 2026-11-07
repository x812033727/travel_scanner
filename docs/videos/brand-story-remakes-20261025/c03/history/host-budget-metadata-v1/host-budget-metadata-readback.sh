#!/usr/bin/env bash
# Run only through an already established production-host connection.
# No deploy/build/restart, provider request, reconciliation or DB data mutation.
set -u
umask 077

c03_probe_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || exit 4
c03_probe_python="$c03_probe_dir/host-budget-metadata-readback.py"
c03_expected_probe_sha256="3d6156d543596c28058ad3191322ca5868d513d3c0dbd88bda1c192716db49d9"
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

# All retained JSON contains only allowlisted metadata. No raw stderr is retained.
python3 - "$c03_readback_dir" "$c03_host_sha" "$c03_api_exit" "$c03_worker_exit" \
  "$c03_actual_probe_sha256" <<'PY'
import json, pathlib, sys
directory = pathlib.Path(sys.argv[1])
def read(name):
    try:
        data = json.loads((directory / name).read_text())
        return data if isinstance(data, dict) else {"result": "UNKNOWN"}
    except BaseException:
        return {"result": "UNKNOWN", "reason_code": "component_metadata_unavailable"}
api, worker = read("api-budget-metadata.json"), read("worker-budget-registry.json")
containers = [read("api-container.json"), read("video-worker-container.json")]
complete = (sys.argv[3] == "3" and sys.argv[4] in {"0", "3"}
            and api.get("transaction", {}).get("verified") is True
            and api.get("schema", {}).get("compatible") is True
            and worker.get("status") == "READ_ONLY_METADATA_OBTAINED"
            and all(c.get("status") == "OBSERVED" and c.get("running") is True for c in containers))
summary = {"probe": "c03-fixed-slug-host-readback-v1", "result": "NOT_READY" if complete else "UNKNOWN",
           "production_authorized": False, "host_git_sha": sys.argv[2],
           "python_probe_sha256": sys.argv[5], "component_exit_codes": {
               "api": int(sys.argv[3]), "worker": int(sys.argv[4])},
           "containers": containers, "api": api, "worker": worker,
           "private_results_directory": str(directory)}
with (directory / "safe-summary.json").open("x") as handle:
    json.dump(summary, handle, sort_keys=True, indent=2)
print(json.dumps(summary, sort_keys=True))
raise SystemExit(3 if complete else 4)
PY
exit $?
