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

### 2026-10-26 additional unchanged-source EN evidence

The same issue was confirmed in the third episode's genuine EN retakes; this is
new evidence for this existing **open, unclaimed** ticket, not another ticket or
an implementation. No command was rerun to reproduce it.

- The preserved `formal-dub-en-retake1-dry-run.log` says
  `en: 100 requests, 0 to synthesize; about 0 billable characters now (6513 for the track)`.
- Actual `formal-dub-en-retake1.log` then reports six one-line retakes and
  `6 requests synthesized (372 billable characters), 94 reused`.
  The unchanged-source result records changed raw IDs
  `zfgp,z9dp,84hx,5waf,8ywa,cgit`, with all other 99 raw clips unchanged.
- Actual `formal-dub-en-retake2.log` reports
  `2 requests synthesized (114 billable characters), 98 reused`; changed IDs
  `8ywa,cgit`, with the other 103 raw clips unchanged. No second zero-work dry-run
  receipt is claimed: only the first dry log above is preserved.
- These are native planned/synthesized request and character reports, not an
  independent provider wire-count or billing statement. TTS character estimates
  do not describe ASR token usage or resolve an uncertain transcription charge.

All files are retained under the external `work/ai-tech-next` proof directory:

| proof | SHA256 |
|---|---|
| formal-dub-en-retake1-dry-run.log | 48a80d7c22582705ffb97c7ad10292e5bec0ea24bace4c7469915d719e89a66d |
| formal-dub-en-retake1.log | 2601497d3c63cce28bb16dd2c01f9299b5b6ee696aaaaa8879468eccd4fb7028 |
| formal-dub-en-retake2.log | ba954d87a8a549d41ea007d22e731b1033f523c1ddb144e41638fe78e444f38c |
| formal-en-retake1-synth-fit-meter.result.json | 45dde074bda4588671271f87cd74b5ce66df420b948c5fd825b711fcbc0980ac |
| formal-en-retake2-synth-fit-meter.result.json | 0a765a85957d2aab753e2d3ee5b9356022741be77045ee2cc889c9658ac5187b |

The inspected native `tools/video/dubs/cli.mjs` SHA256 is
`32fa90b9ae4ca8979584319647cd2f89a29d6d0827abed3137cd18e77545b807`.
At 480 it returns `dryRun(...)` before `dubLocale(...)`. `dryRun` at 421-440
sees only cache keys/WAV existence and receives no redo/force options. Actual
`dubLocale` at 217-233 loads `values.redo`, makes flagged lines pending even when
their cache is current, and estimates per-line retakes. The outer monthly
`needed` at 493 is also cache-only. This confirms the existing scope and DoD;
the future regression should include both six-ID/372-character and
two-ID/114-character cached-redo shapes, without making paid requests.

Offline duplicate checking found this same ticket in all five local worktrees
and six local branch task trees. No live remote/PR query was made under the
no-network instruction. Existing scope remains exactly the dub CLI and its
native tests. Owner/status/claim and all existing implementation checkboxes are
unchanged; no provider call, journal edit, tool patch, stage or commit occurred.
