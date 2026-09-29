---
id: 2026-09-28-verify-imported-review-pages-and-reconcile
title: Verify imported review pages and reconcile remaining video previews
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T13:09:23Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928/IMPORT.md
---

# Verify imported review pages and reconcile remaining video previews

## Why

Ten drama works (sixty documents) and ten conventional video outlines were
imported with owner approval on 2026-09-28. Production SQL and submission API
checks passed, but browser control timed out before rendered-page acceptance.
Separate media packages from #871 and #880 are still not delivered by that
plan-only import. Preserve this work after closing the importer implementation.

## Definition of done

- [ ] Read all ten imported drama cards and their six documents in the browser;
  verify the ten conventional cards show the original brief and pending outline.
- [ ] Reconcile #867/#868/#880 source cuts and review previews with their author
  tasks, recording verified hashes, missing artifacts and actual submission state.
- [ ] Confirm the deployed Shorts tab and push route, then coordinate #871's
  three verified pilot files through the existing Shorts owner-review task.
- [ ] Update the import receipt with evidence without silently approving or
  publishing any work or taking over another agent's active task.

## Steps

- [ ] Use `/zh-TW/admin/videos?tab=drama&series=<slug>` and
  `/zh-TW/admin/videos?tab=reviews&video=<slug>`; expand full-text panels only.
- [ ] Recover #868's two finals and #880's six long/twelve short exports from
  their original production directories. The #880 packaging worktree has receipts
  but no MP4s; #867's found cuts have stale speech hashes against current scripts.
- [ ] Check the current deployed revision: the Shorts tab subsequently merged in
  #912 (initially absent); BFF #901 alone was not the complete tab.
- [ ] Keep media submission/generation approval separate from reviewing existing
  plans. The previous owner approval covered only the ten dramas and ten outlines.

## How to verify

The production snapshot at `2026-09-28T11:48:29.792642Z` contained exactly 10 target
drama series, 60 review docs, 10 target conventional projects, and one pending
outline each. Drama episode/request/media-project counts and review attachments
were zero. Confirm rendered content, not just HTTP success or an empty list.
See `docs/videos/series-plans/binge-five-20260928/IMPORT.md` for bundle hashes.

## Notes

The completed implementation is recorded in
`tasks/done/2026-09-28-pr881-drama-plan-admin-import.md`.
Coordinate with the existing #867/#868 author tasks, the AI season-one final
review task, and Shorts owner-review task; do not re-claim their scopes blindly.
The conventional outline helper uses separate GET/PUT/POST requests and requires
exclusive operation on its ten target slugs. A future unattended/general importer
needs conditional server writes; client preflight is not an atomic concurrency
guard. Expand scope and track that implementation before changing shared APIs.
