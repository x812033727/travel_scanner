---
id: 2026-09-29-prevent-lost-long-running-language-stages
title: Prevent lost long-running language stages and duplicate model retries
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-29T11:52:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/flow.mjs
  - apps/web/app/api/video/automation/run/route.ts
---

# Prevent lost long-running language stages and duplicate model retries

## Why

An imported long video's 94-line English translation completed successfully on
the configured Claude subscription in 302,552 ms, but the web forwarding route
aborts after 295,000 ms. The caller loses the answer even though the backend
records a successful model run, then a retry can repeat the expensive work.
The general language flow still translates and reviews a whole worksheet at once.

## Definition of done

- [ ] Long selected-language work survives model runs longer than the web request
  timeout, or is divided into bounded resumable units that fit the transport.
- [ ] An uncertain POST result does not blindly repeat the same model operation.
- [ ] Translation identity, independent review, subtitle timing, owner choices and
  quota safeguards remain intact across resume.
- [ ] A missing or malformed caption-review worksheet cannot silently reuse the
  translator's unreviewed output as a completed review.

## Steps

- [x] Check current claims before touching the shared automation flow.
- [ ] Choose durable request/result identity or bounded translation chunks; avoid
  relying only on a larger timeout while public nginx still has a shorter limit.
- [ ] Add focused timeout/resume tests and verify a complete persisted review.

## How to verify

Simulate a model completing after the caller's deadline and verify that resume
does not cause a duplicate unidentifiable model run. Check cumulative language
reviews and the existing automation/client regression tests.

## Notes

- 2026-09-30: claimed on `codex/durable-language-stages` after auditing 25 open
  PRs, remote/local branches and 175 other accessible worktrees. Original scope
  has no active editing or PR collision. `claim --force` bypassed broad stale
  overlapping claims whose changes already merged in #978, #999, #904/#962;
  no other task or worktree was modified.
- Existing `video_ai_runs` records usage, not request identity or response text.
  Subscription execution can exceed the public relay deadline. A durable
  submit/poll solution needs additional backend scope; check its collisions
  before extending this ticket. A backend/host crash after dispatch must remain
  uncertain rather than automatically launch another paid operation.
- Backend scope was blocked at that audit: open PR #1026 owned
  `video_automation/admin_api.py` and `schemas.py`; the OneDrive
  `codex/mobile-planner-app-ui` worktree has active edits in `app/main.py`, which
  an independent job router would need for registration. #1039 also owns
  `app/models.py` and proposes migration 0116. Released this ticket before code
  edits; do not work around these owners with side-effect router registration.
- Before resuming, refresh this evidence: #1026 and #1039 have since merged into
  main. The independent router still requires collision clearance for the active
  OneDrive `app/main.py` edits; no backend code was changed here.
- Recommended next implementation: durable UUID receipt + canonical input hash,
  atomic queued-to-running claim, independent execution session, submit/poll
  transport, and result/usage in one transaction. Re-fetch completed answers
  before quota checks. A true API/host crash after dispatch must remain uncertain
  without automatic retry; the host agent has no recoverable run identifier.

- Production evidence: `ai-real-world-01-image-trust`, translator,
  `claude_code/claude-opus-5-5`, status `ok`, duration `302552`, created at
  `2026-09-29T11:47:37.770926Z` in `video_ai_runs`.
- `apps/web/app/api/video/automation/run/route.ts` uses 295,000 ms;
  subscription execution allows 900 seconds plus queue time. The API-only stage
  timeout comment does not bound subscription execution.
- The isolated six-video continuation has its own explicit internal transport
  and single-attempt POST correction under `docs/videos/imported-long-languages`.
  That does not fix the shared worker. This follow-up is unclaimed to avoid the
  active dubs/storytelling work on the shared flow.
- Independent audit also found the shared `translateLocale` fallback merges the
  translator worksheet when the reviewer omits `worksheet.lines`; the isolated
  runner requires the review output before merge. Cover this in the shared fix.
