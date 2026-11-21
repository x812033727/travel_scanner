#!/usr/bin/env bash
# Run on the connected production host. Inspects only; no --apply, deploy or provider call.
set -u
umask 077

c03_host_repo="${C03_HOST_REPO:-/root/travel_scanner}"
cd "$c03_host_repo" || exit 2
c03_readback_dir="$(mktemp -d /tmp/c03-remake-readback.XXXXXX)" || exit 2
c03_compose=(docker compose -f docker-compose.prod.yml)

git rev-parse HEAD > "$c03_readback_dir/host-head.txt"
"${c03_compose[@]}" exec -T api python -m app.video_budget.reconcile_cli \
  --slug story-everyday-moleskine-c03 \
  > "$c03_readback_dir/original-budget.json" 2> "$c03_readback_dir/original-budget.stderr"
c03_original_exit=$?
"${c03_compose[@]}" exec -T api python -m app.video_budget.reconcile_cli \
  --slug story-everyday-moleskine-c03-remake-20261025 \
  > "$c03_readback_dir/remake-budget.json" 2> "$c03_readback_dir/remake-budget.stderr"
c03_remake_exit=$?

"${c03_compose[@]}" exec -T video-worker node --input-type=module \
  > "$c03_readback_dir/worker-branding.json" 2> "$c03_readback_dir/worker-branding.stderr" <<'NODE'
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createHash } from "node:crypto";
import { resolveWorkBase } from "./tools/video/core/paths.mjs";
import { isPreproductionHeld } from "./tools/video/core/pending-pilot-budget.mjs";
import { readCurrentBranding } from "./tools/video/core/branding.mjs";

const slug = "story-everyday-moleskine-c03-remake-20261025";
const base = resolveWorkBase({ root: process.cwd(), env: process.env, home: os.homedir() });
const shelf = path.join(base, "_branding");
const held = isPreproductionHeld(slug);
const output = { slug, local_preproduction_hold: held, formal_v4_identity_verified: false };
let registry = null;
try {
  registry = readCurrentBranding(base);
  output.native_registry_validation = registry ? "PASS" : "MISSING_OR_DISABLED";
} catch {
  output.native_registry_validation = "INVALID";
}
if (registry) {
  output.branding_id = registry.id;
  output.branding_hash = registry.hash;
  output.assets = {};
  for (const role of ["intro", "outro"]) {
    const entry = registry[role];
    const file = entry?.file ? path.resolve(shelf, entry.file) : null;
    const inside = file && file.startsWith(shelf + path.sep);
    const exists = inside && fs.existsSync(file);
    const sha256 = exists ? createHash("sha256").update(fs.readFileSync(file)).digest("hex") : null;
    output.assets[role] = { exists: Boolean(exists), sha256, expected_sha256: entry?.sha256 ?? null, matches: Boolean(sha256 && sha256 === entry?.sha256), declared_frames: entry?.frames ?? null };
  }
  output.formal_v4_identity_verified = registry.id === "mokaair-brand-package-v4-endscreen"
    && registry.intro.frames === 150 && registry.outro.frames === 630
    && output.assets.intro.matches && output.assets.outro.matches;
} else {
  output.branding_missing_or_disabled_or_invalid = true;
}
console.log(JSON.stringify(output, null, 2));
process.exitCode = held || !output.formal_v4_identity_verified ? 3 : 0;
NODE
c03_worker_exit=$?

printf 'Private results: %s\n' "$c03_readback_dir"
printf 'Original budget exit: %s; remake budget exit: %s; worker/branding exit: %s\n' \
  "$c03_original_exit" "$c03_remake_exit" "$c03_worker_exit"
printf 'Keep detailed budget operations private; share only the needed summary and asset hashes.\n'
if [ "$c03_original_exit" -ne 0 ] || [ "$c03_remake_exit" -ne 0 ] || [ "$c03_worker_exit" -ne 0 ]; then
  exit 3
fi
