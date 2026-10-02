---
id: 2026-09-29-prevent-lost-long-running-language-stages
title: Prevent lost long-running language stages and duplicate model retries
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-lang-stages
claimed_at: 2026-10-02T14:43:36Z
created_at: 2026-09-29T11:52:23Z
completed_at:
branch: claude/video-language-stage-timeouts
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/flow.mjs
  - apps/web/app/api/video/automation/run/route.ts
  - tools/video/automation/sheet-units.mjs
  - tools/video/automation/sheet-units.test.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/automation.test.mjs
  - apps/web/app/api/video/speech/forward.ts
  - apps/web/app/api/video/automation/run/route.test.ts
---

# Prevent lost long-running language stages and duplicate model retries

## Why

An imported long video's 94-line English translation completed successfully on
the configured Claude subscription in 302,552 ms, but the web forwarding route
aborts after 295,000 ms. The caller loses the answer even though the backend
records a successful model run, then a retry can repeat the expensive work.
The general language flow still translates and reviews a whole worksheet at once.

## Definition of done

- [x] Long selected-language work survives model runs longer than the web request
  timeout, or is divided into bounded resumable units that fit the transport.
- [x] An uncertain POST result does not blindly repeat the same model operation.
- [x] Translation identity, independent review, subtitle timing, owner choices and
  quota safeguards remain intact across resume.
- [x] A missing or malformed caption-review worksheet cannot silently reuse the
  translator's unreviewed output as a completed review.

## Steps

- [x] Check current claims before touching the shared automation flow.
- [x] Choose durable request/result identity or bounded translation chunks; avoid
  relying only on a larger timeout while public nginx still has a shorter limit.
- [x] Add focused timeout/resume tests and verify a complete persisted review.

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

- 2026-10-02 (claude-opus-5-5-lang-stages, branch
  `claude/video-language-stage-timeouts`): `claim --force` over the stale claims of
  2026-09-28-drama-listener-stale-check (#978), 2026-09-28-sothatswhy-shorts-from-episode
  (#904/#950/#962) and 2026-09-30-video-worker-moves-two-videos-at (#999), all merged.
  No open PR touched the scope. No backend change: bounded units instead of the
  durable submit/poll design above. Scope grew by the new module and its test, the
  client and automation tests, the run route's test, and `forward.ts` (an optional
  lost-answer response so the run route can tell "never sent" from "maybe ran").
- Why not a longer deadline: Node's fetch (undici) gives up waiting for response
  headers after 300 s on both hops (worker -> web, web -> API) whatever the
  AbortController says, and nginx allows 300 s for the public `/api/`. So
  `RUN_TIMEOUT_MS` stays 295 s.
- Bounded units (`tools/video/automation/sheet-units.mjs`, new, so flow.mjs only
  orchestrates): a sheet whose lines exceed 24 lines or 2,400 characters (source +
  current text, what the model must echo) is asked as a metadata unit plus runs of the
  todo lines; a sheet that fits stays one call with the same payload as before. One
  unit per worker step; translator answer, then reviewer answer, each kept in
  `<workdir>/i18n/<locale>.units.json` under a SHA-256 of the unit worksheet and
  `source_locale` (ids, sources, todo flags and dub `max_chars` included, so a changed
  line or budget is a new unit). Nothing merges until every unit has its own review;
  the merge input is the fresh sheet with reviewed texts by id (sources, ids, budgets
  from the sheet). A lines unit is shown only its scenes of the video. Kept answers
  are cleared on a successful merge or when the sheet is done; a merge refusal drops
  the units it names (all when it names none), so they are asked again.
- Reviewer: no `worksheet.lines`, or a line missing/empty, is `retryLater
  ("caption_reviewer")` with the translation kept; it is never merged unreviewed.
  Translator gaps are `retryLater("translator")` before a reviewer is paid. The
  `translator` counter still clears only on a successful merge (a merge refusal must
  reach two and block, not loop); `caption_reviewer` clears after a usable review.
- Uncertain results: the client sends `automation/run` again only when nothing ran
  (ECONNREFUSED/ENOTFOUND/EAI_AGAIN/EHOSTUNREACH/ENETUNREACH/connect timeout, the web
  route's 502 `upstream_unavailable`, 429) or the API settled it
  (`video_ai_upstream_busy|unreachable|failed`, `video_ai_output_invalid`). A dropped
  connection, a header/body timeout, an unreadable 200 body, the route's new 504
  `video_ai_run_uncertain` or any other 5xx throws `RUN_UNCERTAIN` after one request.
  `forward.ts` gained an optional `lost` answer used only by the run route (other
  routes unchanged). In flow.mjs, `move()` turns `RUN_UNCERTAIN` into a block naming
  the stage and unit and ends the run; the owner's retry on /admin/videos resumes from
  the kept units. Paths outside `move()` (drafts, series, discussions, story, Shorts,
  compilation, Jev's judge calls) are filed as
  2026-10-02-stop-repeating-lost-stage-answers-outside.
- Quota: every unit is its own `/automation/run` call, so the API's budget check and
  per-token rate limit (120 runs/hour) apply per unit; a long locale is about ten
  calls instead of two.
- Verified: `node --test tools/video/automation/*.test.mjs` (new tests fail on the old
  flow/client), the run route's vitest (2 of 5 fail on the old route), the bound-file
  check fails only for flow.mjs and automation.test.mjs (author does not rebind).
