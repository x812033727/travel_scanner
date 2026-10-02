---
id: 2026-10-02-run-the-two-wedding-episodes-with
title: Run the two wedding episodes with isolated media settings and bounded cost
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-02T15:37:15Z
completed_at:
branch: codex/drama-competition-wedding-20261002
depends_on:
  - 2026-10-02-drama-competition-wedding-final
scope:
  - ops/video/scoped_drama.py
  - apps/api/tests/test_scoped_drama.py
---

# Run the two wedding episodes with isolated media settings and bounded cost

## Why

The owner requested the first two Chinese wedding-reckoning episodes after final
optimization. Global drama is disabled and the selected clip model is not Lite.
Turning on that global setting can start unrelated works. A narrow administrative
runner should produce only the authorized episode slugs using isolated settings,
while retaining job accounting, idempotency, review evidence and budget limits.

## Definition of done

- [x] Dry-run validates exact episode slugs, manifest hashes, review evidence and
  Lite 1080p / 8-second settings without requesting media or changing the database.
- [x] Execute requires an authorized administrator and explicit reviewed inputs;
  only the two episodes may run and global settings/workers remain untouched.
- [x] A conservative cumulative cost guard includes pending jobs and non-media
  reserves, stops at USD 100 for the pilot and USD 350 for this two-episode batch,
  and does not treat unknown or failed vendor operations as free/retryable.
- [x] Resume preserves the original job, operation and paid attempt; unrelated
  slugs, changed inputs, missing approvals and uncertain states fail closed.
- [x] Focused offline tests pass; any untested live behavior is stated explicitly.

## Steps

- [x] Inspect existing service, tool permissions and concurrent PR #1132.
- [x] Implement the isolated runner and meaningful safety/cost/resume tests.
- [x] Independently review the change and prepare the draft manifest/runbook; no approved manifest yet.
- [x] Run a live read-only preflight after host access is available.
- [ ] Run the first-shot test only after current document/script/look/storyboard approvals.

## How to verify

Run focused API pytest for test_scoped_drama.py and lint the new Python files.
Verify a dry-run makes no provider or database writes. Live execution must retain
the before/after global-setting snapshot, exact input hashes, media job IDs, billing
estimates and later actual invoices. Offline tests do not approve actual footage.

## Notes

The existing MediaContext separates effective settings from runtime credentials;
jobs snapshot their provider/model/request. Existing HTTP endpoints do not offer
isolated settings. This tool is a new administrative path, not a paired-token
privilege escalation or a claim that the global service is enabled.

SSH_PRIVATE_KEY readiness is confirmed without reading or printing its value.
The selected workspace has no TCP destination grants or known SSH endpoint;
the owner has been asked for host/port while Chinese editorial/TTS work proceeds.
No SSH operation, deployment, global-setting write or animated generation has run.

Local implementation complete: 42 tests passed, new-file Ruff/mypy passed,
independent review found no remaining P1/P2. The checks above describe verified
local behavior, not live deployment. PostgreSQL advisory locks, provider region
and actual footage remain untested. Draft manifest is intentionally non-executable
until actual current approvals are available; full scripts are now pending review.
The live-preflight step remains unfinished, so this ticket stays open.

2026-10-03 Windows takeover (supersedes the historical host-access blocker):
SSH is available using the existing private local connection. Live read-only DB
preflight found global drama OFF, music ON, usable administrator capabilities and
a configured Gemini key. The source series remains `setting`; latest setting,
outline and chapter 1 are v3/review, and both submitted scripts remain pending.
No look/storyboard reviews or production media jobs exist. Five runtime API
dependency files match the pinned PR bytes. No deployment, settings write,
document approval, provider request or lock validation was performed.
See `docs/videos/series-plans/competition-20261002/episodes/vps-handoff-preflight-20261003.md`.

The original 42 runner tests and 19 audio-builder tests passed again locally.
The series-image-model race between reservation and the service's final model
selection was reproduced with a fake provider, then fixed inside ScopedSession:
the service's final series-model SELECT refuses an unreviewed override before
the vendor call, retains the reservation and never retries it. Tests also cover
the permitted pinned Pro model. Final validation: 44 runner tests, Ruff and mypy
passed (all exit 0), with independent diff review. First-shot and provider/output acceptance remain
unfinished; retain this ticket in open rather than declaring production complete.
