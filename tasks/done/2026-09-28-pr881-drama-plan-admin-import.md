---
id: 2026-09-28-pr881-drama-plan-admin-import
title: Import authored drama and video plans for admin review
status: done
priority: P1
area: ops
owner: codex-drama-plan-import
claimed_at: 2026-09-28T13:07:16Z
created_at: 2026-09-28T11:01:58Z
completed_at: 2026-09-28T13:12:16Z
branch: codex/import-reviewed-drama-plans
depends_on: []
scope:
  - ops/video/import_drama_plans.py
  - ops/video/import_outline_reviews.mjs
  - apps/api/tests/test_video_drama_plan_import.py
  - tools/video/review/import-outline-reviews.test.mjs
  - docs/videos/series-plans/binge-five-20260928/IMPORT.md
---

# Import authored drama and video plans for admin review

## Why

The owner cannot see the works from PRs #881 and #894 on the website and asked
for the same audit of the video review queue. Merged source packages do not
create database works or submit review previews. Keep this handoff distinct
from producing, approving, scheduling or publishing the videos.

## Definition of done

- [x] Inspect the merged packages and the live video/drama pages.
- [x] Import the ten drama works and sixty documents as review-only records,
  atomically, without generating media or silently approving any document.
- [x] Reconcile the conventional video scripts against exact live project slugs
  and source articles; submit all ten original plans as pending outlines with
  outstanding verification and topic overlap called out for the owner.
- [x] Record incomplete media delivery and rendered-page acceptance in a separate
  follow-up task without describing them as completed by this plan import.

## Steps

- [x] Confirm PR #881 merged as e36db07bbb1a511046def7c42cd6978f3888cc52
  and #894 as 7ea55748dd2520675ff685cb3bd6855b7942f0ee.
- [x] Run both drama-pack validators: ten works pass, sixty documents total.
- [x] Check the live drama page: it says there are no works and AI drama is off.
- [x] Inventory the additional merged video packages #867, #868, #871, #880, #891.
- [x] Finish exact-slug matching for the six #891 scripts: none exist in the
  production project table. Existing same-topic automated projects use different
  slugs; source/content overlap still needs an editorial decision before production.
- [x] Implement a dry-run-first, idempotent importer with source provenance,
  collision refusal, audit logs, and one transaction for each complete batch.
- [x] Test worker selection after import: review documents must produce no job,
  even if the global drama switch is later enabled.
- [x] Expand or split implementation scope before modifying any additional paths;
  existing author tasks are owned by other agents and must not be taken over.

## How to verify

`node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews`
and `node docs/videos/series-plans/claude-binge-five-20260928/validate.mjs` passed.
Use the exact source slugs and authenticated `/zh-TW/admin/videos` and
`/zh-TW/admin/videos?tab=drama` for eventual acceptance. The importer must prove
dry run writes nothing, changed existing works are not overwritten, replay does
not duplicate records, and the worker cannot take an imported review-only work.

## Notes

## Audit evidence, 2026-09-28

| Package | Delivered source material | Website finding / next step |
| --- | --- | --- |
| #881 | Five Codex dramas, forty episodes and six core documents each | Live drama page has no works; import is missing. |
| #894 | Five Claude dramas, forty episodes and six core documents each | Same missing import. |
| #867 | `ai-agent-vs-chatbot`, `ai-citation-check` | Neither original title is in the live video list. Both local `final.mp4` files exist under `C:/Users/x8120/mokaair-work/videos/`; full QA and review push remain separate gates. |
| #868 | `ai-coding-tools-same-task`, `ai-bug-fix-pr-review` | Neither title is in the live list. PR reports historical rendered cuts, but `final.mp4` was not found at the corresponding standard local paths in this audit; recover the actual artifacts before submission. |
| #880 | `docs/ai-video-season-01`: six long cuts and twelve Shorts review cuts | Source and historical media receipts were merged; no matching production projects. The packaging worktree `ai-video-season-pr` contains zero MP4s from its manifest. Find/check the original production exports, then integrate review submission. |
| #871 | Three Shorts pilots and fifteen detailed campaign briefs | All three local final files exist and SHA-256 matches the delivery receipt. No Shorts tab appears on the live admin page; Shorts backend/web/push work is in open PRs #898, #901 and #906. Do not label all fifteen briefs as finished videos. |
| #891 | Six English-market tutorial scripts | None of the six authored slugs exist in production. The site has other agent, price and Vids projects with different slugs. Independent verification, pending claims, and topic-overlap review remain before proceeding. |

The live conventional video list displayed nineteen cards, including two dropped
videos. A clicked English agent card resolves to `always-on-agent-explained`, not
`ai-agent-vs-chatbot` or `ai-agents-explained-what-they-cost`. This prevents treating
that card as proof either authored package was submitted. Pending counts changed
during browser observation. A later database snapshot under `BEGIN READ ONLY`
at **2026-09-28T11:12:36.769184Z** confirmed nineteen projects, zero drama series,
and zero pending reviews. None of the ten checked source video slugs from
#867/#868/#891 exist. Related but distinct existing projects include
`always-on-agent-explained`, `claude-opus-5-5-three-numbers`,
`google-vids-omni-free-quota`, and `gpt6-vs-opus55-worth-paying`.

The live drama page explicitly showed "還沒有作品" and "漫劇目前是關閉的".
No settings were changed. Existing service `create_series` commits a runnable
`setting` row; `hands_off=false` controls approval, not initial planning. The
normal patch route refuses pause while in setting/outline. Do not implement a
create-then-pause loop or use pre-approved document imports just to make cards
appear. All documents can instead be created as `review` in the same transaction
as the work; prove this against `next_job_for` before any live application.

Initial SSH inventory did not execute because the saved PuTTY session had no
username. Supplying the documented root user enabled the read-only SQL snapshot;
the transaction ended with ROLLBACK. Browser UI reads also succeeded, although
later inspections were intermittently interrupted by browser timeouts; direct
navigation to the JSON endpoint was blocked. No credential, database or
production state was modified.
At the initial audit the importer was not implemented. No review was approved,
no media was generated, and no YouTube upload/publication occurred in that audit.

## Implementation after the owner's website-visibility follow-up

- Added `ops/video/import_drama_plans.py`: prepare-only portable bundle, read-only
  PostgreSQL dry run, active admin and exact bundle hash for apply, batch-wide
  collision checks, source/audit binding, and one caller-owned transaction.
- Prepared both actual source batches (10 works, 60 docs), SHA-256
  `722f4ad0991608aa1455e2fb1fdb5de0723f936e5960af1f3a15e0ada0f0b1a1`.
  Local artifact: `%TEMP%/drama-review-import-20260928.json` (not committed).
- `apps/api/tests/test_video_drama_plan_import.py`: 15 passed. Tests cover actual
  package import, no jobs with drama enabled, dry-run/no autoflush, replay,
  modified/approved work collisions, rollback and invalid/tampered packages.
  Independent code review found no material issue. Ruff passed.
  Both targeted mypy checks subsequently passed (importer and test file).
  The source-body assertion follow-up passed separately (1 test). CI was not run.
- Added a separate conventional-outline import helper within this task's scope;
  the existing API accepts a human-pending outline without a Jev pick. Registering
  a project does not create worker state or cause production by itself. Check the
  server work directory for pre-existing target `auto.json` files before applying.
- Further video findings: #867's two local MP4 speech hashes no longer match the
  current scripts/dictionary. Do not present those files as current approved cuts.
  All four #867/#868 projects still have `outline_approved=false`. The status text
  `outline approved` names the next gate, not an approval already granted.
- #891's six scripts may be shown for review with verification/topic-overlap
  limitations clearly stated; showing a plan does not approve production.
- Correction to initial Shorts handoff: #901 only adds BFF routes, not the admin
  Shorts tab. That tab was still open at the initial audit and subsequently merged
  in #912; deployment and pilot submission still need separate verification.
- Before the owner's import approval, production apply and browser verification
  were pending. The authorized import receipt below records the later result.
- Conventional outline bundle prepared and validated for all ten source videos:
  `C:/Users/x8120/AppData/Local/Temp/mokaair-outline-recovery-f8Ofsn/bundle.json`,
  SHA-256 `60deef472e42fdb99090ce21cfac3f37478ec1d1149d958a394e4b5460665604`.
  Real source validation and mocked first apply, replay, final-item collision,
  interrupted report recovery, bad hash/pick refusal, and one-second pacing pass.
  Node syntax and diff checks pass. No credentials were read in preparation.
- The owner authorized production insertion of exactly these ten drama works and
  ten conventional outline reviews. Pending documents are not finished videos or
  permission to generate/publish.

## Authorized production import, 2026-09-28

The owner replied **好** to the concrete request to import both batches, keep
everything pending, and verify it. This authorized the production import.

- Production repository revision at preflight:
  `045afc1eb9ebf371cc54ef9b2dd10be82e7a7b01`.
- The ten conventional target slugs had no server worker `auto.json`. Before
  applying, production had zero series and zero pending video reviews.
- Transferred the tested drama helper and reviewed bundle to a temporary host
  directory and the API container. The production read-only dry run validated
  all ten works and returned exactly the reviewed bundle hash.
- Applied the drama bundle as the configured active administrator: ten creates,
  six review documents each. No application deploy or feature setting changed.
- Applied the conventional bundle through the existing paired tool API. All ten
  results returned `pending`; the recovery receipt is next to the local bundle.
- Read-only SQL verification at **2026-09-28T11:48:29.792642Z** found:
  - 10 target series, 60 readable `review` documents, exactly setting/outline/four
    chapters for each work; all series remain `setting`, hands-off false.
  - Zero target drama episodes, queued requests, or media projects.
  - 10 target conventional projects, each with exactly one pending outline review;
    all contain the original brief and 2–3 options, no automatic pick.
  - Zero review attachments, approvals, retry requests or YouTube publication fields.
- Browser control failed to initialize three times (IAB and Chrome); no rendered
  browser acceptance is claimed. Opening the drama URL in Codex returned `queued`.
  Database and submission API verification passed. A future browser check should
  read the cards/documents only, without approval or generation.

View the imported material at:

- `https://mokaair.com/zh-TW/admin/videos?tab=drama`
- `https://mokaair.com/zh-TW/admin/videos?tab=reviews`

The #871/#880 media recovery and Shorts delivery verification remain open as described above.
This import made authored plans available for review; it did not produce final videos.

## PR handoff

The importer implementation and verified production import are complete. Remaining
browser acceptance and media reconciliation are tracked in
`tasks/open/2026-09-28-verify-imported-review-pages-and-reconcile.md`.
The conventional helper detects existing collisions but its separate report and
submit requests cannot exclude a concurrent writer; the runbook requires exclusive
operation on the target slugs. It is not an unattended synchronization service.

Revalidated after updating to main `ebde813d`: all 15 Python import tests passed;
the 9 durable Node recovery tests passed; focused ruff passed. The Node tests are
included in the existing `npm run test:tools` / video tooling CI glob.
