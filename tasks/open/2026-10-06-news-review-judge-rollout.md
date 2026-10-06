---
id: 2026-10-06-news-review-judge-rollout
title: Switch the news review judge on and release the backlog in batches
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-06T13:11:02Z
completed_at:
branch:
depends_on:
  - 2026-10-06-news-review-judge
scope:
  - docs/news-automation.md
  - .agents/skills/prod-host-ops/references/news-ops.md
---

# Switch the news review judge on and release the backlog in batches

## Why

`2026-10-06-news-review-judge` adds an AI judge that answers the news review queue and the
redraft list in the owner's place. It ships switched off, and nothing about it has run in
production: every judge reply in its tests is a stand-in, and the migration, the row lock and
the new queries have only met PostgreSQL in CI. The owner decided on 2026-10-06 that the whole
existing backlog goes to the judge too; on 2026-10-04 that was 162 drafts waiting for
confirmation and 133 uncertain duplicates, plus the redraft list. Releasing that at once,
before anyone has read a single verdict, would let a model that judges badly publish or reject
hundreds of stories.

Every step below changes production, so each one waits for the owner's go-ahead. This file is
the plan, not the authorisation.

## Definition of done

- [ ] The judge is on in production with the model the owner picked, and new holds are
      answered without the owner.
- [ ] The owner has read the verdicts of a first small batch from each list and said whether
      they are sound.
- [ ] The backlog the owner wanted judged has been released, or the owner has chosen a cut-off
      date for it, and the counts are written here.
- [ ] What the judge did in its first days is recorded here: how many of each verdict, how
      many hand-backs and why, and any verdict the owner took back.

## Steps

- [ ] Deploy the merge (migration 0125). Afterwards the switch is off and the pipeline behaves
      as before: check that candidates still move and nothing has a `judge` assessment.
- [ ] The owner picks the judge's vendor and model at AI settings (各功能模型 › 新聞) and
      ticks 「待審查與需重寫交給 AI 判斷」 at `/admin/news?tab=settings`. Claude runs on the
      host's subscription accounts, like the final editor. A model different from the writer's
      is the better judge of the writer's work.
- [ ] Watch the first new holds get answered: `news_assessments` rows with
      `assessment_type = 'judge'`, the audit action `news_candidate_judged`, and judge runs
      (`judge-*` stages) that finish.
- [ ] List the backlog without changing anything, once per list, and show the owner the counts
      by hold, by vertical and by exclusion reason:
      `backfill_cli --since <date> --judge-holds` and `--judge-redrafts`.
- [ ] With the owner's go-ahead release five of each (`--limit 5 --apply`). Read every verdict
      and its reasons with the owner before the next batch.
- [ ] Ask the owner how far back to go. Stories from weeks ago can be published as they are;
      whether they should is the open question in
      `2026-10-02-decide-on-news-candidates-from-old`.
- [ ] Release the rest in batches the pipeline can absorb. An approved draft costs a whole
      second stage (about twenty model calls), and the concurrency settings and the
      subscription accounts bound how many run at once.
- [ ] Write the numbers into Notes and correct `docs/news-automation.md` and the host-ops
      reference wherever production behaved differently from what they say.

## How to verify

Read-only on the host, with the owner's agreement:

- verdicts per day and kind: `news_assessments` where `assessment_type = 'judge'`, grouped by
  `verdict` and `details_json ->> 'stage'`;
- stories the judge published: audit rows `news_candidate_judge_published`;
- stories it handed back: candidates with `judge_decision = 'manual'`, with the first reason
  of their newest judge row;
- nothing judged while a switch is off: no judge row newer than the moment the owner unticks
  the switch.

The CLI lines and what a listing prints are in
`.agents/skills/prod-host-ops/references/news-ops.md`.

## Notes

- Filed 2026-10-06 with the implementation. Nothing here has been run.
- A listing is safe at any time; `--apply` refuses to run without `--limit` and queues judge
  jobs only.
- Do not use the flagless `backfill_cli` to move redraft-list rows the judge has not answered:
  it redrafts them blind in the actor's name, without the judge's directions or its limit.
