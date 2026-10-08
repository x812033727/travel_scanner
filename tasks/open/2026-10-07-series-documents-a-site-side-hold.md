---
id: 2026-10-07-series-documents-a-site-side-hold
title: Series documents: a site-side hold and a retry for a document whose planner answer was lost
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-07T12:54:04Z
completed_at:
branch:
depends_on:
  - 2026-10-05-hold-lost-planner-and-jev-answers
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_series_document_lifecycle.py
  - apps/web/app/api/video/automation/series
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/messages
  - tools/video/automation/client.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
---

# Series documents: a site-side hold and a retry for a document whose planner answer was lost

## Why

A series document (setting book, series outline, chapter outline, story bible) is planned by the
worker's planner stage, which is synchronous: when its answer is lost on the way
(`video_ai_run_uncertain`, client.mjs `RUN_UNCERTAIN`) the model may have run and been paid for,
and the server keeps no answer to fetch again. Since 2026-10-05-hold-lost-planner-and-jev-answers
the worker records the loss in `_series/<slug>/lost-docs.json` (tools/video/automation/series.mjs
`planDocument`) and does not ask the planner again while the owner's inputs are the same. That
hold is local to the worker, and the site knows nothing of it:

- `GET automation/series/next` keeps naming the same job, oldest series first
  (apps/api/app/video_automation/series.py `next_job`). Every younger series and every one-off
  bible waits behind it, with nothing on /admin/videos saying why.
- The page has no action that releases it. Changing the series' note, premise or title
  (the admin API) or flipping 全自動 (hands_off) changes the hashed inputs and releases it, but
  changes the series; withdrawing it (`DELETE`) and filing it again is a new series row and
  releases it too, and is refused (409 `video_series_started`) once any episode has started,
  which is the usual case for a chapter outline. While it is held the series' own ready episodes
  wait too: `next_job_for` names a due chapter before them. Pausing the series lets the ones
  after it move, and does not release it. A rewrite can also be released by a line on a document
  that files a new version, which is not an obvious way to ask for "plan it again".
- The series page keeps saying the worker writes the document on its next round (`docsEmpty`
  「工人下一輪會寫設定集。」, `bibleEmpty`, `chapterRequested`), which is not true while it is held.
- The hold lives on one worker's disk: a worker moved to another host, or a lost work directory,
  pays for the planner again.

## Definition of done

- [ ] A document job whose planner answer was lost is recorded on the site with the reason and
      when, and `next_job` moves past it until the owner acts: to the same series' ready
      episodes first (a held chapter outline must not stop the chapter already planned), then to
      the next series' job.
- [ ] The series page shows the held document's reason in place of "the worker writes it next
      round", with a 重新規劃 action that clears the hold, writes an audit line, and lets the next
      round plan it exactly once.
- [ ] The worker never plans a held document again on its own, on any host, and nothing is held
      for an error that settled the request (`OUTPUT_INVALID`, the limiter's 503, a never-sent
      connection, the API's own 502).

## Steps

- [ ] API (series.py, admin_api.py): a tool route, for example
      `POST automation/series/{slug}/docs/hold` with `{ kind, chapter_number, previous_id, stage,
      variant, why }`, idempotent per job, that records a held document job; `next_job_for` skips a
      held job and goes on to the same series' ready episodes, then the next series; the summary
      (schemas.py) carries the hold for the page. A migration may be needed for where the hold
      lives (add `apps/api/migrations` to the scope after checking collisions).
- [ ] The Next.js route that forwards it, `apps/web/app/api/video/automation/series/[slug]/docs/hold/route.ts`,
      with its route test: every worker path has its own route there and none is a catch-all, so
      without it production answers the worker 404, which the client below tolerates as a site
      from before the route, and the hold silently never reaches the site.
- [ ] An owner action `POST /admin/video-automation/series/{slug}/docs/hold/clear` (重新規劃) that
      clears it with an audit line; a changed series or a new version clears it as well.
- [ ] apps/web/components/admin-video-series.tsx: the held document's reason in place of the
      next-round text, and the 重新規劃 button; the five locales (zh-TW, en, ja, ko, zh-CN) in
      apps/web/messages, `npm run check:i18n`.
- [ ] client.mjs `seriesHold(slug, hold)`, called by series.mjs `planDocument` right after the
      local record in lost-docs.json is saved; a site from before the route answers 404 and the
      local hold stands as it does today. Keep the local record: it is what holds the job while
      the site cannot be told.
- [ ] Tests: the API's next job past a held document and the clear action's audit line; the
      worker's hold sent once and a 404 tolerated (tools/video/automation/series.test.mjs, the
      `documentJobs` helper).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_series.py tests/test_video_series_document_lifecycle.py
node --test tools/video/automation/series.test.mjs
npx vitest run apps/web/app/api/video/automation/series
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- Found while doing 2026-10-05-hold-lost-planner-and-jev-answers. `lost-docs.json` is the local
  record: one entry per `documentKey` (`<kind>:<chapter>:<previous id or "first">`) with `{ kind,
  chapter, previous_version, stage, variant, inputs, at, why }`, where `inputs` hashes the series'
  facts, the rewritten version's id, version and note, and the approved setting's and outline's
  id and version (`documentInputs`); the worker's own progress (counters, status, recaps,
  episodes, mysteries) does not change it.
- No existing site call fits: `messageAnswer` answers an owner's line only, and `seriesDoc`
  files a valid document only; a series document job has no note field.
- A hands-off series' checker answer lost on the way is not held: the planner's answer is filed
  without a verdict, and the site leaves the version for the owner.
- Where the hold is kept on the site is open: a column on the series (or the document job) needs
  a migration, and then `apps/api/migrations` and its test join the scope (backend-conventions
  skill).
- series.mjs is bound by the duration receipt (docs/videos/long-form/review.json): a change there
  needs the independent re-bind.
