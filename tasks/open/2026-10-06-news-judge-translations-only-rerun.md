---
id: 2026-10-06-news-judge-translations-only-rerun
title: News judge reruns only the translations when a locale review fails
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-06T07:42:29Z
completed_at:
branch:
depends_on:
  - 2026-10-06-news-review-judge
scope:
  - apps/api/app/news_automation/judge.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_judge.py
  - apps/api/tests/test_news_pipeline.py
---

# News judge reruns only the translations when a locale review fails

## Why

When a locale review fails before an article exists, the story rests in `needs_redraft` with
`news_locale_review_failed`. The review judge (`2026-10-06-news-review-judge`) answers that
stop with a whole rewrite: a new zh-TW draft, the fact check, Jev, then stage two again. The
zh-TW draft had already passed the fact check; only a translation was at fault.

A translations-only rerun was designed and left out on purpose. It saves the draft, the
verification and one judgement (three or four calls) but stage two itself, 13 to 22 model
calls and up to six Jev calls, is repeated either way because passed translations are not
stored (`apps/api/app/news_automation/pipeline.py`, the translation loop in `_second_stage`).
And it has real hazards the review found:

- The rerun has to set the marker that authorises publication, from the redraft list, so the
  redraft judgement would also be a publication judgement on the zh-TW draft.
- Its entry into stage two must sit after the duplicate check (a `needs_redraft` row is not a
  known title, so another outlet's version may have been published meanwhile), where an
  uncertain or failed Jev answer overwrites the marker of an approved draft.
- The zh-TW final edit runs first in stage two and its hold is only looked at after the
  translations; a locale stop returns before that, so the judge could approve a rerun over a
  zh-TW text the final editor had just refused.
- Rows older than 2026-09-25 have no slug on their draft run, and rows older than 2026-09-30
  have no stored text for the failed locale.
- Notes for the translator would cover only the newest failed locale.

Worth doing only if the production numbers say so: how many `news_locale_review_failed` stops
the judge rewrites, and how many of those rewrites then fail the fact check they had passed.

## Definition of done

- [ ] The numbers above are read from production and written here, and the owner has decided
      whether the saving is worth the added path.
- [ ] If yes: a locale stop whose zh-TW draft is still verified can be rerun from that draft,
      every hazard above has a test, and a story that keeps failing in translation still
      stops at the rewrite limit.

## Steps

- [ ] Count, per week since the judge was switched on: judge `revise` rows whose `hold` is
      `news_locale_review_failed`, and the outcome of the rerun that followed each.
- [ ] Show the owner the count and the calls a translations-only rerun would have saved.
- [ ] If the owner wants it, design from the notes above and from the plan file's review
      findings recorded in the parent task.

## How to verify

Read-only on the host, with the owner's agreement: `news_assessments` rows with
`assessment_type = 'judge'` and `verdict = 'revise'`, joined to the candidate's later status.

## Notes

- Filed 2026-10-06 while implementing the parent task; nothing was measured yet because the
  judge had not run in production.
- If a rewrite fails because the judge and the writer cannot see the refused text, the cheaper
  fix is to keep that text for them (in a place the admin preview and
  `service.verified_zh_draft` never read), not this rerun.
