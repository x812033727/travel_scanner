---
id: 2026-09-27-news-translations-can-lag-behind-a
title: News translations can lag behind a zh-TW changed by the final edit
status: done
priority: P2
area: api
owner: codex-gpt6-news-source
claimed_at: 2026-09-30T03:40:00Z
created_at: 2026-09-27T09:42:29Z
completed_at: 2026-09-30T03:50:04Z
branch: codex/news-final-source
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
---

# News translations can lag behind a zh-TW changed by the final edit

## Why

In the 2026-09-27 review of held drafts, all four translations of
`ai-news-google-project-suncatcher-20260924` differed from the saved zh-TW in the same way.
They had a three-item summary where zh-TW has four; the missing item is the energy case,
"up to eight times the solar power". They also carried a longer callout with an unsupported
"not yet independently verified" line, and ja, ko and zh-CN framed a table as "Google's three
major challenges". The reviewer concluded that they were translated from an earlier zh-TW
draft. Other drafts showed smaller one-sided differences, for example a zh-TW sentence
missing from en.

The second stage translates first, then runs `final-edit-<locale>` on each locale
separately (#763). If the final edit changes zh-TW, nothing carries that change into the
other four locales. Their locale reviews compare them with the zh-TW they were translated
from, not with the zh-TW that is saved.

## Definition of done

- [x] After a final edit changes zh-TW, the saved translations are made from, or reviewed
      against, the final zh-TW.
- [x] A test in which the final edit changes a zh-TW fact shows that the saved en carries the
      change, or that the candidate stops for review.

## Steps

- [ ] Confirm the mechanism on `ai-news-google-project-suncatcher-20260924`: its pipeline runs
      and the zh-TW revision history.
- [x] Choose the fix: final-edit zh-TW before translating, re-translate the changed parts, or
      run the locale review against the final zh-TW.
- [x] Test.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- The reviewer's report is summarised in the ticket
  `2026-09-27-news-evidence-excerpts-stop-at-8`. Both come from the same review.
- 2026-09-30 audit at main 64f132e1: no competing scope across 20 open PRs,
  53 live remote heads, 177 accessible worktrees or active claims. Expanded the
  scope only to the existing pipeline regression-test file.
- Confirmed the mechanism in current code: translation and locale review precede
  final editing; `_final_edit` also retains the initial zh-TW as the source for
  later locales. Refreshing that reference alone would still leave a stale
  translation when a target-locale edit fails its hard checks and falls back.
- Finalize zh-TW before generating any translations, then run the existing
  locale reviews and four target-locale final edits against that accepted source.
  Preserve source-edit holds and both source/locale mechanical-check fallbacks.
  Normal processing still makes five final-editor calls. Editor-supplied bundles
  keep their existing path and are not rewritten.
- Persist an accepted source revision together with its verification assessment
  before translating. A provider failure can then be retried using the saved
  verified source instead of an older preview paired with a newer hash. Final
  editor assessments also record the source document fingerprint.
- The historical production runs and revisions of the named Suncatcher draft
  have not been re-read; that investigative step remains unchecked. The supplied
  incident report guided a local reproduction, not a claim about live history.
  No production access, model spending, source refresh or article publication
  was performed. Existing held articles still need their own editorial review.
- Six new regression cases derive each translation from the actual source fact:
  a 4-to-8 change propagates to all saved locales, including an English final
  edit that fails twice and falls back. The other cases cover accepted/rejected
  zh-TW mechanical-check retries, a source manual hold, and a translation-service
  failure after source acceptance followed by owner requeue and completion.
- Local validation: all 52 pipeline tests and 86 related news tests passed;
  full API Ruff, mypy app (444 files) and mypy tests (333 files) passed. All model
  calls were mocked. Independent implementation review found no blocker.
- Final collision refresh found 21 open PRs with no overlap. Main advanced to
  72069973 with Shorts review changes; neither that commit nor the updated Shorts
  branch changes this scope. Rebase and post-rebase checks are recorded below.
- Rebased onto 72069973: standalone pipeline suite still passes all 52 tests;
  full API Ruff and mypy app (444 files) / tests (335 files) pass. Task validation
  passes for 1,187 files; only pre-existing stale-claim/overlap warnings remain.
