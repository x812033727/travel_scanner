---
id: 2026-10-07-count-targeted-dub-retakes-in-dry
title: Count targeted dub retakes in dry-run and budget checks
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T06:15:44Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Count targeted dub retakes in dry-run and budget checks

## Why

The dub dry-run and outer monthly budget calculation only inspect existing cache
keys and WAV existence. They ignore the explicit `--redo` IDs, although dubLocale
correctly marks those lines pending and synthesizes them again. During the LLM
Korean QA operation, all 138 existing clips were current but 22 flagged retakes
required 22 line bodies and 666 Gemini billable characters. Dry-run and the outer
monthly-needed calculation treated those cached retakes as zero new work.

## Definition of done

- [ ] A cached targeted retake reports the actual pending requests and estimated
  billable characters before synthesis, including partial-scene/line-by-line work.
- [ ] The monthly preflight refuses targeted retakes exceeding the remaining
  limit, using the same planning rules as actual synthesis.
- [ ] A focused offline regression proves both counts without provider requests.

## Steps

- [ ] Check current shared-tool ownership before claiming this scope.
- [ ] Align dry-run/monthly planning with the native redo/force/line-by-line rules.

## How to verify

Run the native dub tests with a fully current clip cache, selected redo IDs and
stubbed budget/client responses. Verify nonzero retake counts, exact line-body
billable totals and budget refusal before a synth call. Cover a partial scene,
line-by-line retakes, ordinary cache reuse and force behavior.

## Notes

The actual synthesis planner is `dubLocale` in tools/video/dubs/cli.mjs; it reads
redo IDs, computes current/retakes and estimates each line body. The dryRun helper
and outer `needed` calculation use separate cache-only logic. This is a deferred
native-tool fix; the active language operation reconstructed the exact 22 bodies
offline and stayed within the existing configured budget. It changes no settings
and does not clear or resend uncertain paid requests.
