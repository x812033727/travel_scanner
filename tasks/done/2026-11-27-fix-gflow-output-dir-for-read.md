---
id: 2026-11-27-fix-gflow-output-dir-for-read
title: Fix gflow output dir for read-only gateway CWD, uploaded still aspectOk, and mediaId recovery in flow_reconcile
status: done
priority: P1
area: tools
owner: antigravity
claimed_at: 2026-11-27T04:20:13Z
created_at: 2026-11-27T04:19:59Z
completed_at: 2026-11-27T04:22:08Z
branch: antigravity/flow-mcp-output-dir-and-reconcile
depends_on: []
scope:
  - tools/video/flow-mcp
  - ops/flow-gateway
---

# Fix gflow output dir for read-only gateway CWD, uploaded still aspectOk, and mediaId recovery in flow_reconcile

## Why

Live pilot testing of G790 (`B38`) on the `mokaair-flow-gateway` host service revealed three bugs when running remotely under non-root `flowbot`:
1. `gflow-cli 0.107.0` writes downloaded videos to `_clip_dir(None)` (`Path("tmp")` relative to `WorkingDirectory`) before moving them to `--out-file`. Because `/opt/mokaair-flow-gateway/travel_scanner` is owned by `root:root`, `gflow` failed with `storing clip <media_id> failed (ConfigurationError)` even though Google Flow generated and billed the clip.
2. `flow_approve_stills` auto-discovered uploaded stills and verified their dimensions, but omitted `record.aspectOk = true`, causing `flow_plan_clips` to reject them at the Stills-First gate.
3. `flow_reconcile` only scanned `charged === "maybe"` ledger entries and could not recover an already-billed `mediaId` (`charged === "yes"`, `nextAction === "reconcile"`) via `gflow data download` for free.

## Definition of done

- [x] `GflowCliDriver.buildEnv()` sets `GFLOW_CLI_OUTPUT_DIR` to `<runtimeHome>/tmp` (unless overridden) and creates it best-effort; `ops/flow-gateway/mokaair-flow-gateway.service` and `install.sh` also configure `/home/flowbot/.mokaair-flow/tmp`.
- [x] `flowApproveStills` sets `record.aspectOk = true` after `verifyStillDimensions` passes, so uploaded stills unlock `flow_plan_clips` immediately.
- [x] `flow_reconcile` accepts optional `recoverMediaIds: [{ shotId, mediaId }]` to download already-billed clips for free, normalize to `1080p30 bt709 tv -an`, and register them in `flow-clips/manifest.json`.

## Steps

- [x] Set `GFLOW_CLI_OUTPUT_DIR` in `tools/video/flow-mcp/drivers/gflow-cli-driver.mjs`, `ops/flow-gateway/mokaair-flow-gateway.service`, and `ops/flow-gateway/install.sh`.
- [x] Set `record.aspectOk = true` in `flowApproveStills` and add `recoverMediaIds` to `flowReconcile` (`orchestrator.mjs` + `server.mjs`).
- [x] Add regression tests in `tools/video/flow-mcp/gateway-and-bridge.test.mjs` and `driver-and-postprocess.test.mjs`.

## How to verify

```bash
node --test tools/video/flow-mcp/*.test.mjs tools/video/flow-music-mcp/*.test.mjs
bash -n ops/flow-gateway/install.sh && npm run check:tasks
```

## Notes

- Verified against `gflow-cli==0.107.0` (`storage.py:188`, `_video_network.py:382`, `gflow data download --help`).
- After deploy on `hostinger2`, recover G790 `B38` (`64490971-5528-44a8-a061-2c2c676e848a`) for 0 credits using `flow_reconcile({ slug: "sothatswhy-g790-dehumidifier-winter", series: "sothatswhy", profile: "x812033727", recoverMediaIds: [{ shotId: "B38", mediaId: "64490971-5528-44a8-a061-2c2c676e848a" }] })`.
