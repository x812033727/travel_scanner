---
id: 2026-10-06-news-review-judge
title: News review and redraft queues are decided by an AI judge model the owner picks
status: done
priority: P1
area: api
owner: claude-opus-5-5-news-judge
claimed_at: 2026-10-06T07:35:08Z
created_at: 2026-10-06T07:34:20Z
completed_at: 2026-10-06T13:39:03Z
branch: claude/ai-hourly-news-review-97e9d8
depends_on: []
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/judge.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/models.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/app/news_automation/worker.py
  - apps/api/app/news_automation/duplicates.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/app/news_automation/settings_cli.py
  - apps/api/app/i18n.py
  - apps/api/migrations/versions/0125_news_review_judge.py
  - apps/api/tests/test_news_judge.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_automation_settings_models.py
  - apps/api/tests/test_news_review_actions.py
  - apps/api/tests/test_news_settings_cli.py
  - apps/api/tests/test_news_admin.py
  - apps/api/tests/test_news_backfill_cli.py
  - apps/api/tests/test_migration_0125_news_review_judge.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/components/admin-news-model-settings.tsx
  - apps/web/components/admin-ai-model-overview.tsx
  - apps/web/components/admin-ai-model-overview.test.tsx
  - apps/web/lib/admin-news.ts
  - apps/web/lib/admin-news-messages
  - apps/web/e2e/admin-operations.spec.ts
  - docs/news-automation.md
  - .agents/skills/prod-host-ops/references/news-ops.md
---

# News review and redraft queues are decided by an AI judge model the owner picks

## Why

The hourly news pipeline stops a story in two places that wait for the owner. `manual_review`
(the admin's "待審查" list, label "待你判斷") holds drafts Jev did not act on, stories with one
non-first-party source, uncertain duplicates and articles the final editor or Jev's last call
held. `needs_redraft` ("需重寫") holds drafts that failed the fact check, the claim-source or
date checks, or a locale review before an article existed. In the seven days to 2026-10-04
about 180 stories reached a human gate (84 uncertain duplicates, 83 zh-TW drafts, 17 last-call
holds) and the owner cannot press a button for each, so nothing moves.

The owner asked on 2026-10-06 for an AI model to make these decisions, with a setting that
picks which model. Decisions taken that day:

1. A story entering the review queue is decided by the judge model from what the detail page
   shows. Three answers: publish, reject, or hand back to the owner with reasons.
2. The whole existing backlog is judged too, released in batches by a CLI after a small trial.
3. Holds in the review queue that need work rather than a judgement stay with the owner:
   `news_hard_checks_failed` with a saved article, `news_evidence_changed`, and locale or
   verification failures kept there because a person confirmed. The code keeps one more
   kind there that the plan did not name: a story that already has its article and that the
   fact check, a locale review or the date check stopped when the article was checked
   again. Nobody need have confirmed it; the owner fixes the article and presses 重新查核.
4. The judge may publish a story with one non-first-party, non-trusted source. This repeals the
   2026-09-25 rule that a person must press for those; the judge is told the site count and the
   first-party and trusted-alone flags.
5. The needs-redraft list is handled by the same judge: it decides how to rewrite, and the
   story goes through the pipeline's checks again.

Defaults chosen with the plan (the owner approved it): one switch and one model for both
lists; the judge may reject from the redraft list; at most two judge-directed rewrites per
story; a rewritten story follows the normal path (automatic gates when Jev and the evidence
allow, otherwise the review queue and the judge); a failed locale review is a whole rewrite;
`failed` rows and the 2026-10-01/02 rows that already hold five stored locales are left alone;
the judge acts only where automatic mode and that vertical's auto-publish are on.

Rejected on review, so nobody proposes them again:

- A per-minute sweep over the queue. Two failing rows block the rest for an hour under an
  hourly job id, a job crossing the hour is paid twice, and re-ticking a vertical after a
  major-error report would publish weeks-old holds at once. A trigger from the job that
  produced the hold, plus a CLI for the backlog, replaced it.
- `judge_decision == "publish"` as the key into stage two. A flag has to be cleared at every
  requeue and a missed site publishes edited text on an old verdict. A kept marker in
  `error_code` is overwritten by every outcome.
- A translations-only rerun for a failed locale review. It saves three or four calls and needs
  the publication marker to be set from the redraft list, an entry after the duplicate check,
  and guards for rows older than 2026-09-25 that have no stored slug.
- Keeping the failed draft text for the rewrite. No backlog row has it, and the claim ledger
  plus the checkers' issues are enough to steer a fresh draft.

## Definition of done

- [x] With the switch off (the shipped default) the pipeline, the admin page and every existing
      test behave as before.
- [x] With the switch on, a story that lands in a judged hold gets exactly one judge verdict,
      recorded as an assessment with the model and reasons, and the verdict is carried out:
      publish, reject, close as duplicate, continue, rewrite with directions, or hand back.
- [x] A person's action during the model call wins: the verdict is dropped.
- [x] The judge never publishes when automatic mode or that vertical's auto-publish is off,
      checked again at publication.
- [x] No story is rewritten on the judge's directions more than twice, and directions never
      reach a draft they were not written for.
- [x] The owner can pick the judge's vendor and model beside the writer, verifier and final
      editor, switch the judge on in the news settings, see its reasons on a story, and take
      back a story the judge closed.
- [x] A news-page settings save does not change the stored judge model or switch.

## Steps

- [x] Writer instructions name the evidence role and the event-date rule (own commit).
- [x] Migration 0125, models, settings schemas, `update_settings`, settings CLI.
- [x] Reply schemas and model calls in `ai.py`; revision notes on the writer payload.
- [x] `judge.py`: `wanted`, `judge_candidate`, apply rules, failure handling, reopen action.
- [x] `pipeline.py`: two kept markers, judged stage-two entry, steered draft, claim clears the
      judge columns.
- [x] `jobs.py` trigger and judge job, worker-start recovery of cut-off judge runs.
- [x] `backfill_cli.py`: `--judge-holds`, `--judge-redrafts`, default pool skips judged rows.
- [x] Web: fourth model picker, switch, verdict lines, badges, reopen button, copy in five
      locales, fixtures.
- [x] Docs and the host-ops reference.
- [x] Adversarial review of the diff before the pull request.

## How to verify

From the repository root. The two directory changes are in subshells, so each line starts
from the root again:

```bash
(cd apps/api && uv run alembic heads && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest)
npm run lint:web && npm run typecheck:web && npm run test:web
CI=1 npm run check:i18n && npm run test:tools && npm run check:tasks
(cd apps/web && npx playwright test e2e/admin-operations.spec.ts)
```

After a deploy the owner agrees to: the switch is off and nothing changes. The owner picks the
model at AI settings and ticks the switch at `/admin/news?tab=settings`. On the host, run both
backlog flags without `--apply` and show the counts; with the owner's go-ahead release five of
each and read the verdicts in `news_assessments` (`assessment_type = 'judge'`) before the rest.

## Notes

- Claimed with `--force`. The overlap is `pipeline.py` and `test_news_pipeline.py` in
  `2026-10-04-resume-held-news-drafts-from-their` and
  `2026-10-05-news-auto-publish-reads-its-switches`, both in review. Their work is on main
  (#1212 a266a5bba, #1247 1ff45131f) and draft PR #1334 closes them.
- Draft PR #1326 also edits `admin-news-workspace.tsx`, its test and `docs/news-automation.md`;
  whichever lands second resolves the overlap.
- The design was reviewed twice against the code before any line was written: one planning
  agent, then a nine-agent workflow (two mappers, three designs, a merge, three reviewers).
  The plan the owner approved is the result.
- The adversarial review of the diff moved the code away from that plan in five places.
  The judge job's RQ limit is 30 minutes, not 15: one question on a subscription account
  may take two rounds of up to eight minutes, before a publication's evidence re-fetch.
  A second job for a hold that is being judged steps aside instead of asking again.
  Expired evidence excerpts keep a story from the judge in the review queue as well as in
  the redraft list. A confirmed story the final editor held is not put to the judge, whose
  only possible answer there was a hand-back. An uncertain duplicate check records that it
  interrupted a rewrite, so the directions survive a rewrite that was paused or cut off
  before that hold.
- The judge's row in the AI model overview takes its name from the news page's own copy
  (`judgeFeature` in `apps/web/lib/admin-news-messages`), not from
  `apps/web/messages/*/admin.json`. Those five files are bound by the long-video duration
  receipt (`tools/video/long-form/review.mjs`), and one added key there turned
  `review.test.mjs` red; a key in the news catalog needs no receipt increment and cannot
  collide with one.
- Checked on this machine before the pull request: API lint, both type checks, one migration
  head and the whole API suite in four shards; web lint, type check and the whole unit suite;
  `check:i18n`, `check:tasks`, the skills test and the duration receipt test. Not checked
  here, because this machine has no PostgreSQL or Redis: the migration on a real database,
  the row lock and the timestamp comparisons of the new queries (every test is SQLite and
  fakeredis), and the Playwright admin spec. CI runs those.
- `npm run test:tools` has four reds on this Windows machine that the change does not touch
  and Linux CI does not have: ffmpeg filter paths in `tools/reference-analysis.test.mjs` and
  `tools/video/shorts/from-drama.test.mjs`, a backslash path in
  `tools/video/media/media.test.mjs`, and the known `tools/video/tts/check.test.mjs` case.
- Left for later, both cosmetic: when the owner's own publish button meets changed evidence
  on a story the judge had handed back at another hold, the row keeps its 「AI 交回」 badge
  without a verdict block (the summary would need `judge_hold`); and Jev's last-call records
  carry no text fingerprint, so after a re-check without an edit the judge is not shown a
  Jev objection that still applies.
- What only production can show is whether the model judges well: every judge reply in the
  tests is a stand-in. The rollout task releases five stories of each list first for that
  reason.
