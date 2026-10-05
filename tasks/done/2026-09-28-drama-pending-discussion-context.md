---
id: 2026-09-28-drama-pending-discussion-context
title: Provide prerequisite context when discussing preloaded drama documents
status: done
priority: P2
area: api
owner: codex-ten-drama
claimed_at: 2026-09-28T15:03:46Z
created_at: 2026-09-28T14:17:08Z
completed_at: 2026-10-05T00:24:24Z
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/messages.py
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_drama_messages.py
  - tools/video/automation/discuss.mjs
---

# Provide prerequisite context when discussing preloaded drama documents

## Why

The ten imported works each have a setting, outline and four chapter documents
already awaiting review. An owner may discuss/rewrite a pending chapter now,
but the discussion context uses context_view, which includes only approved
parents. While all six documents are still in review, the model gets the chapter
and short series premise without the existing full setting, total outline or
mystery definitions. That can undermine a continuity correction during review.

This is distinct from the production approval-order bug tracked in
2026-09-28-drama-preloaded-document-approval-order. Production should consume
approved inputs; editorial discussion needs an explicit policy for references
that are still awaiting approval.

## Definition of done

- [x] A discussion/rewrite of a preloaded outline or chapter receives sufficient
  prerequisite context, or is blocked with an actionable explanation before a
  model call. Do not require approval of known-bad source just to discuss it.
- [x] If pending parent documents are included, mark their review state/version
  clearly and retain the distinction from approved production inputs.
- [x] Handle an older approved parent plus a newer pending revision explicitly;
  do not silently mix versions or change normal episode production selection.
- [x] Add focused API/worker tests for all-review imported state, approved
  parents, revised parents and missing parents.

## Steps

- [x] Trace messages.py:208-213 (pending target can be discussed) and :277
  (context_view), series.py:1540-1556 (approved parents only), and
  tools/video/automation/discuss.mjs:65-67 (passes only supplied parents).
- [x] Coordinate with existing drama-room API/UI owners before implementation.
  Claiming the original approval-order ticket was refused during this audit due
  to active overlapping video tasks; no force claim or implementation followed.

## How to verify

Offline execution of actual context_view/approved_doc/setting_kind/chapter-range
functions against each of the ten real documents.json bundles, with six review
documents and no episodes, yielded the same result for all ten:

```text
all_review_series_checked=10
stored_docs_each=6
discussion_parent_setting=None
discussion_parent_outline=None
mysteries_each=0
```

The probe used in-memory session rows and output constructors; it exercised the
actual selection logic, not an HTTP/database integration or a paid model run.
For the fix, assert the real messages endpoint and discussion payload carry the
chosen parent versions/status labels; retain the approved-only production tests.

## Notes

- Found in the second ten-drama audit on 2026-09-28. All six pending documents
  exist, so this is not the ordinary empty-work planning sequence.
- This task files the finding only. No discussion message, model call, approval,
  production write or deployment was performed.

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
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-ten-drama (since 2026-09-28T15:03:46Z) was stale; the work landed in #978 and every box was already ticked, so the ticket is closed.
