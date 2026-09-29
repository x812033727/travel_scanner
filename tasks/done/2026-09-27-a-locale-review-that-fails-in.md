---
id: 2026-09-27-a-locale-review-that-fails-in
title: A locale review that fails in round two reports on its own discarded correction
status: done
priority: P2
area: api
owner: codex-news-locale-review
claimed_at: 2026-09-29T12:17:34Z
created_at: 2026-09-27T14:14:26Z
completed_at: 2026-09-29T12:26:22Z
branch: codex/news-locale-review-evidence
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
---

# A locale review that fails in round two reports on its own discarded correction

## Why

The locale review runs two rounds per locale (pipeline.py:864-936):

1. Round 1 reviews the saved translation. If the reviewer returns `revise` with a
   `corrected_document`, that correction replaces the translation, and nothing is stored.
2. Round 2 reviews the correction. If round 2 does not pass, the pipeline stores a `manual`
   assessment with round 2's issues, and the candidate is held with `news_locale_review_failed`.
   The correction is not saved.

So the editor's queue shows issues found in text that no longer exists. The issues round 1 found
in the saved draft, the text the editor actually has to fix, are lost.

This happened on 2026-09-27, when 11 held drafts were fixed by the issues on `/admin/news`:

- `ai-news-gemini-3-8-tts-20260923`, ja: the stored issues are four typos, such as 脆本 for 脚本,
  仲組み for 仕組み and 金銘 for 金銭. None of them is in the saved ja draft. The round-1 reviewer's
  own correction introduced them, round 2 flagged them, and the correction was thrown away.
- `ai-news-anthropic-claude-enzyme-system-art-20260923`, en: the stored issue is a "(translated
  from Chinese)" note in the Feng Zhang quote. The saved en draft has no such note.
- In the other drafts, the stored issues overlapped the saved text only where the correction
  had left a passage unchanged.

The editor cannot tell which issues are real, and a fix made from them cannot pass.

## Definition of done

- [x] When a locale is held, the issues the editor sees describe the saved draft of that
      locale. Store round 1's issues on the saved text, or say clearly which issues belong to
      the discarded correction.
- [x] A test in which round 1 revises and round 2 fails shows the round-1 issues on the held
      candidate.

## Steps

- [x] Bind the terminal `manual` assessment to round 1's original issues, reviewer model
      and document hash. Keep round 2's verdict, issues, model and reviewed correction
      hash in `details.discarded_correction`; do not expose them as original-draft issues.
- [x] Show the round-1 issues in the review queue (`/admin/news`) when round 2 fails.
- [x] Test in tests/test_news_pipeline.py.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- A related cause of these held drafts is
  `2026-09-27-news-translations-can-lag-behind-a`. The final edit rewrites each locale
  separately after the locale reviews pass. On a later re-check, the locale review then
  compares drifted translations with zh-TW.
  - On 2026-09-27, checkers found 2 to 19 further departures from zh-TW in each held zh-CN
    draft, beyond the stored issues.
  - The drafts were aligned with zh-TW block by block before the next re-check.
- Round 1's correction model also introduces errors of its own, such as the ja look-alike
  kanji above. That is worth watching once round 1's issues are visible.

### 2026-09-29 local repair (codex-news-locale-review)

- Started from main `9daa475f`; baseline `tests/test_news_pipeline.py`: 40 passed.
- Fresh collision check covered all files of 17 open PRs, 47 remote heads,
  384 local branches and 217 other worktrees. No active scoped work was found.
  The unattached local `codex/pr917-dedup-order` branch retains unrelated test
  work; it is preserved and is not part of this repair.
- The admin table displays assessment reasons but does not label arbitrary
  `details.reviewed` values. The terminal manual assessment now uses
  the original review's issues, model and document hash, with the discarded
  correction's review retained in diagnostic details. Successful corrections
  continue through the existing publication gates.
- On a hold, retain the original reviewed locale in the candidate preview only.
  Existing guide drafts, versions, revisions, other locales and published data
  must remain unchanged. This also makes a newly translated held locale readable.
- Scope is local code and offline tests. No production access or content release.
- Six new regression cases failed on the old source, then all 46 pipeline tests
  passed after the repair. Coverage includes new and existing articles, second-round
  manual/revise outcomes, direct manual review, empty original issues, persisted
  candidate-detail previews and unchanged guide drafts/revisions/publication.
- An additional 76 news policy, admin, review-action and backfill tests passed.
  Full API Ruff and `mypy app` (444 source files) passed. The scoped test-file mypy
  check passed on Windows, and full `mypy tests --platform linux` passed (331 files).
  Native Windows full-test mypy still has the pre-existing UnixStreamServer typing
  limitation handled separately in draft PR #975; no unrelated fix is included here.
- Two independent offline provider-error/subscription-pause checks passed against
  both the previous and repaired source, preserving failure/retry behavior.
- The pre-PR collision refresh again found no active overlap. Main remained
  `9daa475f`; all files of 17 open PRs were checked. Existing historical assessment
  rows are not rewritten; the correction applies to subsequent review runs.
- Independent source/test review found no material issue. `check:tasks` passed
  for 1,155 tickets; the Windows leftover open copy was removed only after checking
  the finished record and identical task body. Merge, deployment and live acceptance
  remain separate from this completed local implementation.
