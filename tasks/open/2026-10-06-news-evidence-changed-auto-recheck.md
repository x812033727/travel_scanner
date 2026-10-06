---
id: 2026-10-06-news-evidence-changed-auto-recheck
title: A news story held for changed evidence is re-checked without the owner
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-06T07:42:31Z
completed_at:
branch:
depends_on:
  - 2026-10-06-news-review-judge
scope:
  - apps/api/app/news_automation/judge.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/tests/test_news_judge.py
  - apps/api/tests/test_news_review_actions.py
---

# A news story held for changed evidence is re-checked without the owner

## Why

The review judge (`2026-10-06-news-review-judge`) answers the holds that are judgements. Three
holds in the review queue need work instead, and the owner chose on 2026-10-06 to keep them
for now:

- `news_evidence_changed`: the source pages changed after the article was checked. The owner
  presses "用最新來源重新查核", which fetches the pages again and re-runs the fact check, the
  locale reviews and Jev's last call on the saved article (`service.refresh_candidate_evidence`).
  Newsroom pages (The Verge, TechCrunch, CoinDesk) change often, so a judged publication can
  end here too.
- `news_locale_review_failed` or `news_verification_failed` on a story a person confirmed: the
  owner presses "重新翻譯並發布".
- `news_hard_checks_failed` with a saved article: someone has to edit the article.

The first two are the same button every time, pressed without reading anything. They could run
once without a person; the third cannot.

## Definition of done

- [ ] The owner has decided whether an evidence-changed hold (and a confirmed story stopped in
      translation) is retried once without them, and that decision is written here.
- [ ] If yes: each such hold is retried at most once per story, the retry obeys the same
      switches as the judge, a second stop rests with the owner, and each retry leaves an
      audit row.

## Steps

- [ ] Count these three holds per week on the host and show the owner.
- [ ] Ask the owner; the retry of an evidence-changed hold costs a fact check, four locale
      reviews and up to five Jev calls.
- [ ] If agreed, call the existing service functions with a system actor from the judge job's
      trigger, with a per-candidate once-only guard read from the audit log or a run row.

## How to verify

`cd apps/api && uv run pytest tests/test_news_judge.py tests/test_news_review_actions.py -q`,
then on the host after a deploy the owner agrees to: no `news_evidence_changed` row older than
an hour without a retry on record.

## Notes

- Filed 2026-10-06 while implementing the parent task. `refresh_candidate_evidence` and
  `approve_candidate` both take an actor and write `human_reason`; a system retry must not
  write the human fields (the parent task gave `_queue_new_draft` and `_queue_reverify` an
  optional reason for the same purpose).
