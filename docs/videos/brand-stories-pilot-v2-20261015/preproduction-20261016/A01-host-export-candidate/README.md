# A01 read-only export binding candidate — HOLD

This directory contains an **offline inspector**, a read-only SQL projection, and synthetic tests. `inspect-export.mjs` never opens SSH, the database, an API or a media provider; it reads only caller-supplied local files and emits a JSON report on stdout. It has no install, retry, STOP-change, media-generation or payment path. Even a successful local binding reports `production_status: HOLD`, `installation_allowed: false` and `paid_work_allowed: false`. The production capture procedure and this candidate still need independent review before use.

## Exact input contract

1. `--snapshot` is an absolute **local** directory with these paths, preserving bytes and relative names:
   - `docs/videos/lexicon.json` and `docs/videos/story-rolling-suitcase-v2/{video.json,series.json,claims.md,script.md}`; `verify-1.md` when present.
   - `story-rolling-suitcase-v2/auto.json`, `review/narrative.json`, and each of `story/chapters/{hook,origin,idea,engine,turn,now}.json`; `story/reviews/script-review.json` when present.
   - The complete `story-rolling-suitcase-v2/story/recheck-audit/<event>/` directory for each event, with `index.json`, the JSON journals named by it, and its bound review/author files. The actual host format is **one directory per event**, unlike the round-11 offline fixture's single `round9-tip.json`.
   - Only `story-rolling-suitcase-v2/manual-revisions/<revision>/installation-receipt.json` files, not the backups beneath those revision directories.
   - No media bytes, environment files, token files or settings dumps.
2. `--pins` is a separate local JSON file: `{ "id": "capture-id", "links": 80, "install_receipt_sha256": "…", "tip_index_sha256": "…", "source_composite_sha256": "…", "archive_index_manifest_sha256": "…", "state_sha256": "…" }`. The state hash must be recorded independently at capture time. All hashes must be independently recorded from the intended immutable capture, not generated from a copy after an inspection failure. The reused inspector currently requires **exactly 80 links**. If production has gained an event, this candidate rejects it; do not delete an event or repin history merely to make it pass. The default historical pins in the reused inspector are not live proof.
3. `--state` is a **separately acquired sanitized read-only** JSON snapshot. Its exact top-level keys are `schema_version` (1), `slug` (`story-rolling-suitcase-v2`), `observed_at` (UTC ISO string), `release`, `archive`, `filesystem`, and `db`. The `archive` fields must equal the recomputed source composite, 80-index manifest and tip index SHA. `release` has `{git_sha,worker_sha256,panel_rules_sha256}`. `observed_at` is checked for UTC syntax only: the offline program cannot authenticate host origin, freshness or the absence of a change after capture.

`filesystem` has `{global_stop,scoped_stop,lease,unresolved_journals,run_receipts,media_assets}`. Each STOP/lease record is `{present:boolean,sha256:<64-hex-or-null>}`; `sha256` is null only when absent. Each receipt or media asset is `{path:<safe relative path>,sha256:<64 hex>,bytes:<nonnegative integer>}`. Hash media **on the host** if needed; do not copy media bytes into the snapshot. An empty inventory is only a supplied value, **never proof that enumeration was complete**. A reviewer must verify the exact A01 workdir/manifests and any omissions before relying on it. A `LEASE` file's absence or presence is recorded, never changed by this tool.

`db` has `{series,episode,project,budget,stage_jobs,media_jobs}`. `series` and `episode` are the exact fields projected by `readback.sql` from `video_drama_series` and `video_drama_episodes`; `project` is from `video_projects`. The inspector pins the authored `series.json` SHA-256 `b2cdb40d…` and requires its exact A01 plan: `brand-stories-curio-pilot-v2`, 10 minutes, `hands_off=true`, `image_model=image-01`, `look.preset=cute-mystery`, `style_preset=custom`, `visual_tier=stills`, `compilation=false`, `episodes_per_day=1`, `planned_episodes=2`, plus the exact authored title, premise and note. These are the importer's 12 `COMPARED` fields; the SQL columns and types are defined on `VideoDramaSeries`. It also requires imported series `status=active`, episode 1 `status=started`, project `stage=blocked`. Any drift remains a HOLD. `stage_jobs` is the A01 subset of `video_stage_jobs`, keyed by `request_json->>'slug'`; `media_jobs` is the A01 subset of `video_media_jobs`. `budget` is the unmodified JSON from `python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2` in inspect mode. It includes **every** operation and its linked media jobs; do not call it with `--operation-id`, which would hide other rows. The inspector checks exact US$25 limit, aggregate arithmetic, operation IDs/statuses, duplicates, and **bidirectional equality of every SQL media job ID/status and its budget operation**. Any A01 image, clip or music job with a null `pilot_budget_operation_id` is rejected. SQL and budget CLI reads are separate transactions and therefore do not constitute an atomic live snapshot.

## Read-only host collection recipe for independent review

The currently deployed compose file is `/root/travel_scanner/docker-compose.prod.yml`. Run these from `/root/travel_scanner` only after confirming the actual `video-worker` mount paths and that A01 is quiescent. The following archive command writes **only to stdout**. The caller must use a binary-safe local capture; do not paste the tar stream into chat. It explicitly names source files and the audit JSON directory, not the whole video workdir:

```bash
docker compose -f docker-compose.prod.yml --profile video exec -T video-worker bash -euo pipefail -c '
slug=story-rolling-suitcase-v2
work=/var/lib/mokaair/video-work
audit="$work/$slug/story/recheck-audit"
test -d "$audit"
test -z "$(find "$audit" -type l -print -quit)"
test -z "$(find "$audit" -type f ! -name "*.json" -print -quit)"
receipts=()
while IFS= read -r -d "" name; do receipts+=("$name"); done < <(
  find "$work/$slug/manual-revisions" -mindepth 2 -maxdepth 2 -type f \
    -name installation-receipt.json -printf "$slug/manual-revisions/%P\0"
)
test "${#receipts[@]}" -gt 0
docs=("docs/videos/lexicon.json" "docs/videos/$slug/video.json" "docs/videos/$slug/series.json"
  "docs/videos/$slug/claims.md" "docs/videos/$slug/script.md")
test ! -f "/opt/mokaair/docs/videos/$slug/verify-1.md" || docs+=("docs/videos/$slug/verify-1.md")
workfiles=("$slug/auto.json" "$slug/review/narrative.json" "$slug/story/recheck-audit")
for chapter in hook origin idea engine turn now; do workfiles+=("$slug/story/chapters/$chapter.json"); done
test ! -f "$work/$slug/story/reviews/script-review.json" || workfiles+=("$slug/story/reviews/script-review.json")
tar -cf - -C /opt/mokaair "${docs[@]}" -C "$work" "${workfiles[@]}" "${receipts[@]}"
'
```

Collect the database projection with **SELECT only**, in a read-only transaction, using the exact checked-in `readback.sql` as stdin; collect budget separately with the existing read-only CLI. Keep those JSON outputs locally and assemble only the documented fields into `--state`. Capture `git rev-parse HEAD` from the host checkout. Capture the worker file hash with `sha256sum /opt/mokaair/tools/video/automation/story.mjs` in the worker container; capture panel rule text hash with Node's SHA-256 of exported `PANEL_INSTRUCTIONS` from `/opt/mokaair/tools/video/core/narrative.mjs`. Inspect global `VIDEO_WORKDIR/STOP`, A01 `STOP` and `LEASE` using `test -e` and `sha256sum` only; inspect unresolved run journals and media inventory without reading media into the exported archive. From this **local Windows worktree**, stream the local SQL through PuTTY stdin (the file is not on the host):

```powershell
$sqlPath = 'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-export-candidate/readback.sql'
Get-Content -LiteralPath $sqlPath -Raw -Encoding utf8 | & 'C:\Program Files\PuTTY\plink.exe' -batch -load '<saved-session>' -l root 'cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T postgres psql -X -q -t -A -U travel -d travel_scanner -v ON_ERROR_STOP=1 -f -'
& 'C:\Program Files\PuTTY\plink.exe' -batch -load '<saved-session>' -l root 'cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2'
```

Replace `<saved-session>` with the approved local PuTTY session name. Check each process exit code before using its output. `readback.sql` is sent through stdin and is not deployed by this work. The `psql` output is one JSON object between transaction markers; reject null `series`, `episode` or `project`. The second command must have no reconciliation action. The collection remains incomplete until a reviewer verifies exact audit pins, host origin, STOP/lease/journal/asset enumeration, budget output, and a second readback without drift. **No production install or paid call is authorized by this recipe.**

The release and three control-file observations can be collected with these read-only commands. The `PANEL_INSTRUCTIONS` hash is the actual exported rule text, whereas `worker_sha256` is only the `story.mjs` file hash; neither replaces the deployed Git SHA or a full worker provenance check.

```bash
git -C /root/travel_scanner rev-parse HEAD
docker compose -f docker-compose.prod.yml --profile video exec -T video-worker \
  sha256sum /opt/mokaair/tools/video/automation/story.mjs
docker compose -f docker-compose.prod.yml --profile video exec -T video-worker \
  node --input-type=module -e 'import {createHash} from "node:crypto"; import {PANEL_INSTRUCTIONS} from "/opt/mokaair/tools/video/core/narrative.mjs"; console.log(createHash("sha256").update(PANEL_INSTRUCTIONS).digest("hex"))'
docker compose -f docker-compose.prod.yml --profile video exec -T video-worker bash -eu -c '
work=/var/lib/mokaair/video-work
for name in STOP story-rolling-suitcase-v2/STOP story-rolling-suitcase-v2/LEASE; do
  if [ -e "$work/$name" ]; then sha256sum "$work/$name"; else printf "ABSENT %s\n" "$name"; fi
done'
```

## Local evaluation

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-export-candidate/inspect-export.mjs --snapshot C:\path\to\a01-snapshot --pins C:\path\to\pins.json --state C:\path\to\state.json
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-export-candidate/inspect-export.test.mjs
```

Exit 0 means **local bytes and supplied readback agree**, not that production is safe or current. Any missing file, inconsistent audit link, tamper, source drift, duplicate operation or state mismatch returns nonzero. The report includes only hashes, status counts and error codes; it does not print source text, model output, account tokens, vendor IDs or media. A separate reviewer still has to check the real narrative, source facts, run receipts, provider billing, live jobs and permissions before the owner-authorized A01 workflow can move.
