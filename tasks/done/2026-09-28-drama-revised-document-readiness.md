---
id: 2026-09-28-drama-revised-document-readiness
title: Invalidate drama episode readiness when governing document versions change
status: done
priority: P1
area: api
owner: codex-ten-drama
claimed_at: 2026-09-28T15:03:48Z
created_at: 2026-09-28T14:26:39Z
completed_at: 2026-10-05T00:24:30Z
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_series_binge.py
---

# Invalidate drama episode readiness when governing document versions change

## Why

After normal approval of setting, outline and chapter 1, its ten episode rows
are ready. Saving a consistent replacement chapter as review does not invalidate
those rows. next_job_for stops looking at documents but then dispatches episode 1;
context selection uses the older approved chapter. If the replacement is rejected
and consumes the rewrite budget, the same fall-through starts the old version.

The owner sees the latest chapter awaiting review or rejected, yet production can
start the same chapter from an older version. docs/videos/SERIES.md:46,93 says
exhausted document rewrites stop for review. Keeping an earlier approved document
for history is legitimate, but there is no explicit active-production-version
choice tied to the ready rows and the latest review state.

This was reproduced offline with the real Wedding documents and actual service
functions from both this checkout and deployed revision 045afc1e. It is separate
from the manual Markdown/JSON mismatch: this reproduction supplies consistent
body_md and body_json. No production state was changed or shown to have suffered
this sequence already.

## Definition of done

- [x] Define the production-version contract for material replacement documents.
  Pending/rejected governing revisions must not silently fall back to starting
  newly queued episodes from old approved content. If continuing a pinned version
  is supported, make that explicit and reviewable to the owner.
- [x] Enforce the invariant in scheduling and episode start, including the
  exhausted-rewrite and force-next paths. A different future chapter awaiting
  review must not unnecessarily block an unaffected approved chapter.
- [x] Reconcile affected not-yet-started episode rows and dependent chapter
  approvals after upstream revisions. Preserve completed/running work and history;
  do not destructively rebuild a series as a shortcut.
- [x] Cover the six-preloaded-document scenario and actual revised payloads in
  service/API tests, including repeat calls and races between edit and start.

## Steps

- [x] Inspect edit_doc :1371, next_job_for :545-546 and :563-584, and
  approved_doc :295-302 in apps/api/app/video_automation/series.py.
- [x] Also address upstream dependency drift: after chapter 1 approval makes rows
  ready, approving outline v2 leaves chapter v1 approved and existing ready-row
  titles/loglines unchanged (_apply_approval only updates planned rows :1269).
  The offline probe changed E1's title in both Markdown and JSON; the approved
  outline showed the new title but the ready episode kept 這次不簽 and could start.
- [x] Coordinate with active series API owners before implementation. Related
  audit tickets cover initial approval order and Markdown/JSON synchronization;
  this ticket concerns version dependency after normal initial approval.

## How to verify

Use the real Wedding documents.json and series-request.json in a memory or test
database session. The audit called actual decide_doc, edit_doc, submit_doc,
_apply_approval, next_job_for and approved_doc, replacing only database plumbing
and response constructors. Settings: series_doc_rewrites=2, max_in_flight=1,
monthly episodes=40, auto_continue=true, chapter_ahead=2, started_this_month=0.

1. Seed the six documents as v1 review; normally approve setting, outline,
   chapter 1. Confirm ten ready episodes.
2. Change E1 hook in chapter 1's JSON and corresponding Markdown; edit_doc with
   approve=false. Confirm v2 review, ten ready, next job episode 1, worker uses v1.
3. Reject v2. Confirm next job is a chapter rewrite. submit_doc a consistent v3,
   reject it, exhausting the two-rewrite budget. Confirm next job is episode 1.
4. In a fresh normally approved session, approve outline v2 with a changed E1
   title in both representations. Confirm ready E1 still has its old title and
   chapter v1 stays approved; next job is still episode 1.

Observed identically for working-tree and 045afc1e:

```text
chapter v2 review -> 10 ready -> episode 1, chapter context v1
chapter v2 rejected -> rewrite chapter 1
chapter v3 rejected, budget exhausted -> episode 1
outline v2 approved -> ready row old title, chapter v1 approved -> episode 1
```

Exact local audit probe (outside the repository; accepts an optional revision):

```powershell
& 'C:\Users\x8120\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\python.exe' -X utf8 'C:\Users\x8120\AppData\Local\Temp\mokaair-drama-version-audit-20260928-31ce.py' . 045afc1e
```

Use database-backed tests for the fix; the audit reproduction does not establish
HTTP concurrency behavior or browser acceptance.

## Notes

- Negative control passed: rejecting a preloaded chapter before setting/outline
  approval does not dispatch a blank-parent chapter rewrite. It waits, then
  rewrites only after both approved parents exist. Do not report that as a bug.
- Third ten-drama audit, 2026-09-28. No code fix, approval, generation, deployment
  or publication occurred.

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
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-ten-drama (since 2026-09-28T15:03:48Z) was stale; the work landed in #978 and every box was already ticked, so the ticket is closed.
