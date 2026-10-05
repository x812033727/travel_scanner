---
id: 2026-09-28-drama-listener-stale-check
title: Invalidate stale drama checks after listener narrative edits
status: done
priority: P2
area: tools
owner: codex-ten-drama
claimed_at: 2026-09-28T14:39:32Z
created_at: 2026-09-28T14:28:35Z
completed_at: 2026-10-05T00:24:13Z
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/core/script-check.mjs
  - tools/video/core/screenplay.mjs
  - tools/video/core/screenplay.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Invalidate stale drama checks after listener narrative edits

## Why

The episode verifier writes review/script-check.json before the listener edits
video.json. listen() saves the edited script and sets listener_done, but leaves
verified=true and the old check intact. The subsequent script submission sends
the current screenplay/hash alongside the previous coverage, continuity report
and retention timings, without binding the report to its checked narrative.

The current ten plans use hands_off=false, so this does not by itself prove they
would bypass owner approval. It can present stale evidence to their reviewer.
Hands-off scripts also consume the same stale verdict for automatic gating.
No completed episode from these ten was used or alleged defective; this is a
deterministic reproduction of the shared worker path with a local fixture.

## Definition of done

- [x] A changed narrative cannot reuse a verifier report for an older narrative.
  Bind the report to the checked narrative/version and enforce the binding both
  when deciding locally and when building a review submission.
- [x] After listener narrative edits, refresh required semantic/continuity checks
  and measure retention on the exact script being submitted. Recomputing timings
  alone does not validate changed content or moved/deleted story beats.
- [x] Avoid a perpetual verifier-listener loop. A no-op listener and prompt-only
  media changes should preserve applicable evidence; meaningful narrative changes
  should receive a finite, explicit recheck.
- [x] Cover changed hook duration, moved/removed payoff lines, changed ending,
  no-op listener and prompt-only updates in focused worker/review tests.

## Steps

- [x] Trace flow.mjs:1011-1014: verify then listen then scriptGate.
  verify writes the check at :1343, listen saves edits at :1361-1366 without
  clearing verified or invalidating that check.
- [x] Inspect flow.mjs:891-892 (hands-off scriptVerdict) and
  review/sync.mjs:371-394 (current script plus unchecked prior report). A current
  payload narrative_hash alone does not prove the report checked that narrative.
- [x] Consider the missing series context in listen's payload (:1361): it has
  video, brief and house style, but no setting_md, chapter_md, beats or recaps.
  Keeping facts/reveals unchanged is a prompt instruction, not enforced by lint.
  Resolve this as part of the evidence contract instead of assuming the model
  can never alter protected content.

## How to verify

Offline reproduction calls actual Automation.listen and saveAndLint, with only
the model answer replaced by a deterministic listener candidate. It uses the
repository drama fixture, a compilation episode with the outro removed, valid
series.json identifiers/cast, and an isolated temp root/work directory. The first
shot contains one line. Seed a prior check using actual retentionNumbers and
valid coverage; then make the listener lengthen that hook from 1 s to 8.4 s.

The new candidate passes actual lint (including the shot duration limit), but
the current retention rule's 8-second limit fails if recomputed. Observed:

```json
{"verified":true,"listener_done":true,"narrative_changed":true,"report_unchanged":true,"old_hook_seconds":1,"current_hook_seconds":8.4,"stale_report_passes":true,"current_report_passes":false}
```

The only requested model stage was listener; the recorded payload had no
setting_md. No vendor, API, browser, TTS or media generation was called.

Exact local probe (outside the repository; argument is repository root):

```powershell
node 'C:\Users\x8120\AppData\Local\Temp\mokaair-drama-listener-audit-20260928.mjs' .
```

For implementation, run tools/video/automation/series.test.mjs and
tools/video/review/sync.test.mjs with focused regressions proving a stale report
cannot be submitted as current. Test manual and hands-off review paths separately.

## Notes

- The first probe setup hit a Windows Node native abort in the fixture helper's
  fs.cpSync. The temp-only probe was changed to ordinary readFileSync/writeFileSync
  copies; the completed reproduction exits 0. Do not report that fixture setup
  failure as an established production worker failure.
- Third ten-drama audit, 2026-09-28. This records the issue only; no code fix,
  production document edit, approval or deployment was performed.

## Implementation coordination

- Owner explicitly authorized isolated-branch backend fixes on 2026-09-28 despite
  overlapping claims; no other branch or task claim is changed.

## Repair implementation, 2026-09-28

- Implemented in isolated branch `codex/ten-drama-audit-fixes` under the claimed
  ten-drama content / preloaded-approval / listener tasks. The owner explicitly
  approved parallel backend repairs despite other task claims; no other branch
  or owner claim was changed.
- Report: `docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260928.md`.
- Local source/documents and code are revised; historical production/import
  receipts are unchanged. No deployment, production update, approval, generation
  or publication has been performed by this repair.

### Verification and handoff

- Content: both ten-work validators pass; 34 generator/continuity tests pass;
  independent revised-source receipts and all 60 current document hashes checked.
- API: 80 focused tests pass, including SQLite transaction coverage; 5 PostgreSQL
  integration tests remain skipped locally. Ruff and touched-file mypy pass.
- Worker/tool suite: 578 pass, 1 existing Windows/Bash environment skip.
- The branch is ready for code review; it has not been merged or deployed. The
  independent production/browser follow-up remains with its existing owner.

## Review follow-up, 2026-09-29

Three defects of the binding itself, found in review and fixed on this branch
(reviewer: claude-fable-5-1); each has a test in `series.test.mjs` that fails on
the code before the fix.

- verify() hashed the checker's raw answer and compared it with the saved file,
  which settle() had already rewritten. speechHash reads the voice object and
  the cast's order, the two things settle() owns, so an answer with the voice's
  keys or the cast in another order was refused as "the lint repair changed the
  checked script", and two such rounds blocked the episode. The candidate is now
  settled the way saveAndLint settles it before it is compared
  (`Automation.settled`, `Automation.checkedIsSaved`).
- An answer without a voice made speechHash throw a TypeError. step() only
  catches AutomationError, the state was not yet saved, and the same video was
  checked again (a paid call) every round ahead of every other video. Settling
  restores the voice; a candidate too broken to settle or hash counts as
  repaired by lint instead of throwing.
- A report written before this change has no hashes, so every series episode
  under way at the deploy was checked again at whatever stage it had reached,
  and the checker may rewrite video.json under an approved screenplay and paid
  media. Such a report (`scriptCheckUnbound`) is now made again only while the
  script gate is still ahead; past the gate the episode goes on as it was. The
  gate itself still refuses it (scriptGate), so nothing unbound reaches the
  owner as current evidence. A missing report is still checked again.
- Not changed: script.md carries a `speech` line, so the same screenplay has
  other bytes than before. An approval already given stays valid because
  script.md is only rewritten at the gate; a screenplay waiting for the owner at
  the deploy is sent again and leaves its first card behind.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-ten-drama (since 2026-09-28T14:39:32Z) was stale; the work landed in #978 and every box was already ticked, so the ticket is closed.
