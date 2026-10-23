---
id: 2026-10-13-hide-stale-news-hold-instructions-after
title: Hide stale news hold instructions after final decision
status: done
priority: P3
area: web
owner: codex-stale-ui-a8cd
claimed_at: 2026-10-13T04:29:24Z
created_at: 2026-10-13T04:12:27Z
completed_at: 2026-10-13T04:48:06Z
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
---

# Hide stale news hold instructions after final decision

## Why

During the October 13 hourly news review, the published Evernorth, Clarity and
Apple/Huxe candidate detail cards still showed the old red hold label
`五語已就緒，待發布` and the English explanation "The checked five-locale
article is waiting for the publish button." The same cards simultaneously
showed `已發布`, an AI final decision of `發布`, and working public article links.
The old hold explanation can mislead an editor into trying to publish again.
This is a display inconsistency; the persisted publication state and public
pages were separately verified. Rejected candidate cards also retain their
former hard-check or locale-failure label next to `已退件`, which should be
presented as history rather than a current instruction.

## Definition of done

- [x] Published and rejected news detail cards make the final state primary and
      do not instruct the editor to publish, rewrite or retry a resolved item.
- [x] Prior hold reasons remain discoverable as historical diagnostics when
      useful, without looking like the current next action.

## Steps

- [x] Trace where the candidate detail renders the status, hold label and
      explanatory text; make the final-state branch explicit.
- [x] Add regression tests for a published candidate retaining an old
      `news_ready_to_publish` hold reason and a rejected candidate retaining a
      hard-check/locale hold reason. Preserve actionable text for real holds.

## How to verify

Run the focused `admin-news-workspace.test.tsx` test and web lint/typecheck.
Inspect a seeded published and rejected detail in the admin UI; the candidate
state, former reason and next-action copy must not contradict one another.

## Notes

- Browser evidence from the same-day production review is preserved in
  `docs/news-hourly-review-2026-10-13.md`; no public article fix is needed.
- Keep this distinct from news pipeline state changes and the cross-category
  duplicate follow-up; only admin display wording is in scope.
- Published, rejected and duplicate list rows now omit stale hold labels. The
  detail keeps their old error code and explanation behind a neutral, collapsed
  Reasons disclosure; unresolved holds keep their existing prominent guidance.
- Focused `admin-news-workspace.test.tsx`: 64 passed on 2026-10-13.
- `npm run lint:web` and `npm run typecheck:web`: passed on 2026-10-13.
