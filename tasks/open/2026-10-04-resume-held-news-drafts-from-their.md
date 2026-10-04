---
id: 2026-10-04-resume-held-news-drafts-from-their
title: Resume held news drafts from their five stored locales, without drafting again
status: review
priority: P1
area: api
owner: claude-opus-5-5-news-resume
claimed_at: 2026-10-04T14:12:27Z
created_at: 2026-10-04T14:12:11Z
completed_at:
branch: claude/news-resume-saved-bundles
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_resume_saved_bundle.py
  - .agents/skills/prod-host-ops/references/news-ops.md
---

# Resume held news drafts from their five stored locales, without drafting again

## Why

From 2026-10-01 until #1201 was deployed (2026-10-04 06:29 UTC), every automatic news
article failed the hard checks for a process figure the pipeline no longer drew. Before
#1136 such an article was kept only on the candidate: 38 production candidates sit in
`needs_redraft / news_hard_checks_failed` with five translated, reviewed and final-edited
locales in `draft_bundle_json` and no guide article. Nothing could finish them:

- 重新查核 (`reverify_candidate`) refuses `needs_redraft`.
- 重新執行 and the default `backfill_cli` pool draft the story again, which discards the
  stored translations and spends about 25 model calls per story.

On 2026-10-04 the owner chose to add a recovery path and pilot it on three stories first.

## Definition of done

- [x] A stored bundle can be sent back to the pipeline so that it resumes at the hard checks.
  It gets a fresh duplicate check, the final editor's recorded verdicts, Jev's last call and
  publication, and it is never drafted or translated again.
- [x] Every outcome a normal second stage has is kept: a check that still fails saves an
  editable article, and the final-edit hold, the Jev hold, duplicates and changed evidence
  all still apply.
- [x] The marker survives a crash, a stalled worker, a paused subscription and a spent Jev
  budget. A rerun never redrafts.
- [x] The dry run lists which stored locales today's checks still refuse, and puts the clean
  bundles first, so a pilot picks the ones that can actually go out.
- [ ] Merged, deployed, and a three-story pilot run on production with the owner's approval.
  The outcomes are recorded in `2026-10-04-news-publication-recovery`.

## Steps

- [x] `pipeline.RESUME_MARKER`, `KEPT_MARKERS`, `_resume_saved_bundle`,
  `_recorded_final_holds`; the tail of `_second_stage` became `_finish_bundle` so both paths
  share it.
- [x] `backfill_cli --resume-saved-bundles` (pool, still-failing report, `resume()` with a
  `news_candidate_resumed` audit row).
- [x] Tests in `apps/api/tests/test_news_resume_saved_bundle.py`, which recreate the pre-#1136
  state from a real pipeline run.
- [x] Host procedure in `.agents/skills/prod-host-ops/references/news-ops.md`.
- [ ] PR, CI, deploy (skill `deploy`), dry run on the host, `--limit 3 --apply` after the
  owner's go-ahead.

## How to verify

```bash
cd apps/api
uv run pytest tests/test_news_resume_saved_bundle.py tests/test_news_pipeline.py tests/test_news_backfill_cli.py -q
uv run ruff check . && uv run mypy app && uv run mypy tests
```

On the host, after deploying: run the dry run in `news-ops.md`, then `--limit 3 --apply`.
Watch the three candidates in `/admin/news`, or with read-only selects on `news_candidates`
and `news_pipeline_runs`. A resumed candidate's runs after the resume are `jev-final` only,
with no `draft`, `translation-*` or `final-edit-*`.

## Notes

- With the resume branch disabled, 4 of the 5 new tests fail; with `KEPT_MARKERS` replaced by
  `REVERIFY_MARKERS`, the same 4 fail. The duplicate test passes either way, because the
  duplicate check runs before the branch.
- A locale with no final-edit record, or whose record describes different text, counts as
  held. The article is saved and waits for a person; it never goes out on its own.
- Production snapshot, 2026-10-04 14:05 UTC: the 38 were created on 10-01 (19) and 10-02 (19).
  The task `2026-10-04-news-publication-recovery` says about ten of them also have
  punctuation problems. Those will land in `news_hard_checks_failed` with a saved article
  that can be edited.
- `apps/api/tests` is listed in the stale `2026-10-03-illustrated-slides-round-2-a-family`
  (a video task, claimed on 10-03). This task adds one new test file there, so it was claimed
  with `--force`.
