---
id: 2026-10-09-video-stage-receipt-site-identity
title: Preserve stage receipt identity across public and internal video worker transport
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-09T10:33:33Z
completed_at:
branch: codex/stalled-videos-completion-20261008
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/client.test.mjs
  - ops/video/worker.sh
  - tasks/open/2026-10-09-video-stage-receipt-site-identity.md
---

# Preserve stage receipt identity across public and internal video worker transport

## Why

On 2026-10-09, two completed, approved long-video packages remained visibly blocked after the owner pressed retry and pasted YouTube IDs. The native retry refused retained stage journals before dispatch with `stage journal has changed identities or source bytes`. The production source and all package bytes remained current; this finding does not establish an outstanding provider response or authorize another paid call.

The configured worker loop sets `MOKAAIR_SITE` to `VIDEO_INTERNAL_SITE` (`http://web:3000`) for each `auto` invocation. A normal `docker compose exec` CLI uses the stored public site (`https://mokaair.com`). `automationClient` passes the effective transport `site` into `runReceiptStore`; its `read()` requires exact `record.site === site`. Thus a journal created through the public transport passes the real native validator with public-site context, while the same untouched bytes fail when the normal loop supplies its internal transport. Owner retries traverse all journals before selecting candidates, so even completed retained entries can produce a misleading `uncertain:writer` block.

Read-only reproduction at production HEAD `57139d78d1ea5a3f79500f92ce957db9b9870759`, worker `441f7eca8caeca54c510f7754fe1cd98e335564145dcb27c075d3016e6a9e293`, 2026-10-09T10:21:57Z:

- CF `cloudflare-workers-per-worker-permissions-ai-agent` and SEC `sec-ai-trading-bot-whatsapp-scam`: real current native `retryCandidates` with the public context returns `[]`; identical journal bytes with the normal internal context throw the exact identity error.
- No new `VideoStageJob` or `VideoAiRun` since 10:11:45Z; active stage/media counts are zero. No provider call, journal reset, credential/site setting change or production code change was made during the reproduction.
- Native `run-receipts.mjs` SHA-256 `c81ebc524090ddc12c23510055b7d27cf29fe736aed332136a3ea169869ddd31`, client `456363a81de1e851c304d1adcba445026ed3b9b6f240906addd7da6ca9c96306`, actual `/usr/local/bin/video-worker` `2250fe48289048b2771ac5209396b52651ab3d5b950dee5e7400a3d816c445f5`.

## Definition of done

- [ ] The same configured production site can use its public/internal transports without rejecting unchanged retained stage receipts solely because the transport origin changed.
- [ ] Existing source hashes, request UUIDs, raw results, journal bytes, adoption proofs and uncertain holds remain protected; no successful or unknown paid operation is reissued or given a new namespace implicitly.
- [ ] A genuinely different site, source/request identity, raw receipt, or owner context still fails closed.
- [ ] The retry path reports actual uncertainty separately from a transport/identity mismatch; no retry clears or archives entries before every required identity check passes.
- [ ] Fake-transport tests reproduce public CLI → native internal worker and the reverse, preserving zero new POSTs for completed/unknown original keys.

## Steps

- [x] Record the current exact read-only reproduction and preserve evidence; production source/journals remain untouched.
- [ ] Decide the narrow stable logical-site versus transport binding using existing credential/SDK contracts, then inspect compatibility for existing public and internal journals.
- [ ] Implement only the reviewed binding and migration/compatibility behavior necessary for original identities; do not weaken raw source/result validation.
- [ ] Add meaningful regressions for valid completed, pending/uncertain, changed-site, altered-request/result and owner-retry cases.

## How to verify

Use fake transports only. Run `node --test tools/video/automation/run-receipts.test.mjs tools/video/automation/client.test.mjs`, then repository tool/task checks appropriate to the implementation. No provider or production retry is required to prove the mismatch.

The retained outside-repository evidence is `C:/Users/x8120/mokaair-work/stalled-video-audit-20261008/overnight-20261009/dubs-selected/actual-current-new-retry-native-validator-site-readonly-v2.jsonl`; `actual-new-auto-block-retry-journals-readonly.jsonl` lists every unchanged journal SHA and exclusively retained new auto snapshots. The source-only follow-up does not authorize production mutation, credential values, owner choices, YouTube actions, replay, deployment or paid work.

## Notes

This is distinct from the existing imported-language runner speech-journal fixture task and lost planner/Jev outcomes task. On 10:17Z the owner independently filled CF/SEC YouTube IDs; the old unpublished-package reconciliation correctly refused its `uploaded=true` guard and was not executed. Neither READY nor an owner-entered ID alone proves owner listening or public YouTube publication.
