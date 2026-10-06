---
id: 2026-10-06-news-jev-publish-confidence-fell-below
title: News Jev publish confidence fell below the act threshold after the criteria keys changed
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-06T00:01:34Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_jev_publish_question.py
  - docs/news-automation.md
---

# News Jev publish confidence fell below the act threshold after the criteria keys changed

## Why

Automatic news stopped publishing again. The pipeline itself runs: every hour drafts and both
verification passes succeed, the settings are `mode=automatic` with all three
`auto_publish_*` switches on. But since 2026-10-05 12:00 UTC every candidate that reaches Jev's
first Traditional Chinese question comes back `tier: hold` and lands in `manual_review`. The last
automatic publication was 2026-10-05 11:58 UTC. The owner noticed it as "其他的也都不會動".

Read-only production numbers (`news_assessments`, `assessment_type='jev'`, `locale='zh-TW'`,
model `jev-1.13.0`, prompt version `news-v1`, read 2026-10-05 23:45 UTC):

| UTC day | answers | mean noul | min | max |
| --- | ---: | ---: | ---: | ---: |
| 09-25 … 10-03 (nine days) | 2–117 a day | 0.52–0.58 | 0.25–0.43 | 0.64–0.78 |
| 10-04 | 2 | 0.38 | 0.25 | 0.50 |
| 10-05 | 17 | 0.37 | 0.24 | 0.56 |

- Jev's noul has never reached 0.9. Production's `jev_act_confidence` acts at about 0.5: the
  final-stage answers of 0.54 and 0.56 at 10-05 11:57–11:58 were `act` and published. So a mean
  near 0.55 published about half the drafts, and a mean of 0.37 publishes none.
- After 10-05 11:58 all nine first-stage answers were 0.25–0.47.

Most likely cause: PR #1218 (`cf16eb785`, deployed with `8e8598cf0` at 2026-10-05 02:09 UTC)
changed the noul `criteria` keys from `yes`/`no` to the `true`/`false` TypeSafe documents. If the
old keys were ignored, the publish question in `apps/api/app/news_automation/ai.py` is now answered
with `false: "Any condition fails or is uncertain."` in force for the first time, which is a much
stricter question. Its ticket (`tasks/done/2026-10-03-jev-noul-criteria-keys-yes-no.md`) left
the post-deploy step unticked: "re-check a few known lines and news candidates after deploy and
note any shift here". This ticket is that step, for news.

Ruled out:

- #1274's punctuation normalization (`news_automation/typography.py`, deployed 10-05 12:07 UTC):
  the answers were already low from 07:17 to 11:40 that morning.
- Truncation: `JevClient` raises when a request is over its token caps; it never truncates.

Not proven yet: two days of low answers also coincide with fewer candidates (a weekend) and with
drafts that the verifier narrowed more often (`revise` is common). The comparison below separates
the criteria from the content.

The same criteria change also reached `video_automation/judge.py` (outline pick) and
`video_speech/checking.py` (per-line narration check, flagged below 0.5). Two narrations checked
on 10-05 23:44 and 23:54 UTC each had 3 lines flagged and rewritten once before passing. That may
be normal; it is noted here, not judged.

## Definition of done

- [ ] A recorded comparison shows how much of the drop is the criteria: the same saved
      documents asked with the old `yes`/`no` wording and with the current `true`/`false`
      wording, with the noul of each, written in Notes.
- [ ] The owner has chosen one way forward from the measured numbers (wording of the publish
      question, its criteria, the act threshold, or none), and that choice is recorded here.
- [ ] After the chosen change is live, at least one candidate is published automatically again,
      or the owner's decision to keep holding is recorded.

## Steps

- [ ] Pick about ten saved candidates: some published on 09-29/09-30 (answers 0.5+) and some held
      on 10-05. Use their saved zh-TW documents and `evidence_hash`.
- [ ] Ask Jev the publish question for each document twice, once with criteria sent as
      `yes`/`no` and once as `true`/`false`. The comparison has to send the old keys in raw JSON,
      because `NoulCriteria` now refuses them. Count the calls against `jev_daily_call_budget`
      and get the owner's agreement before making them (about 20 calls).
- [ ] If the criteria explain the drop, propose wording that keeps the stricter meaning where
      it matters (accuracy, sourcing, no investment advice) without turning "uncertain" into "no"
      for every article, and pin it with a test in `apps/api/tests/test_news_jev_publish_question.py`.
- [ ] Update `docs/news-automation.md` with what the act threshold means against Jev's real
      noul range (never above 0.78 so far).

## How to verify

```sql
-- psql inside the postgres container; daily zh-TW publish answers
select to_char(date_trunc('day', created_at),'MM-DD') d, count(*),
  round(avg(confidence)::numeric,2) avg, round(max(confidence)::numeric,2) mx
from news_assessments where assessment_type='jev' and locale='zh-TW'
  and created_at > now() - interval '14 days' group by 1 order by 1;
```

After a change: the daily mean returns to the band the owner chose, and `news_candidates` gains a
`published` row whose audit event is `news_candidate_auto_published`.

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_news_jev_publish_question.py tests/test_news_pipeline.py
```

## Notes

- Found on 2026-10-06 by a Claude Code session diagnosing "影片製作一直卡住、其他的也都不會動".
  That diagnosis made no setting change and no Jev call.
- Production's act threshold is a database setting (`news_automation_settings.jev_act_confidence`),
  not code; changing it is the owner's call on `/admin/news` settings, not a deploy.
- The criteria keys must stay `true`/`false` (the documented contract). The question is whether
  the publish question's wording, now actually read, says what the owner wants.
