---
id: 2026-10-04-news-publication-recovery
title: Deploy the news diagram fix and reassess held publication drafts
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-04T05:35:03Z
completed_at:
branch:
depends_on:
  - 2026-10-04-news-publish-retired-diagram
scope:
  - docs/news-automation-recovery-2026-10-04.md
---

# Deploy the news diagram fix and reassess held publication drafts

## Why

News sources and workers are healthy, but a retired diagram requirement stopped
the five-locale publication path. The code fix belongs to the dependency above.
Production activation and the already held drafts still need an owner decision.

## Definition of done

- [ ] The owner authorizes merging and deploying the exact validated news fix.
- [ ] Deployment preflight/hold/lock checks pass, the target SHA is live and news
      services use its image.
- [ ] An eligible new candidate passes the real asset/policy boundary and its
      actual public article is verified; ordinary review holds are preserved.
- [ ] The owner chooses a small recovery pilot for existing drafts, including
      whether to spend model calls, before any retry or publication.
- [ ] A recovery record lists outcomes and remaining holds without assuming
      deployment automatically publishes old candidates.

## Steps

- [ ] Read the dependency's PR checks and obtain exact merge/deploy authorization.
- [ ] Use the deploy skill's live preflight and one-shot background deployment.
- [ ] Verify SHA, services, public site and a real eligible publication.
- [ ] Review the 39 held drafts and propose a bounded recovery pilot.
- [ ] Save deployment/recovery evidence in the scoped document.

## How to verify

Use `.agents/skills/deploy/SKILL.md` and `host-verify.sh` for deployment. Read-only
counts of `news_candidates` and recent `news_pipeline_runs` prove stage outcomes;
verify a `published` candidate's article and locales on the public site.

## Notes

- Read-only production snapshot at 2026-10-04 05:27-05:36 UTC, live d038b035e:
  three idle news workers, empty queued/started/scheduled registries, 22 enabled
  sources scanning successfully; enabled/automatic and all category flags on.
- Last candidate publication: 2026-09-30 20:31:15 UTC (2026-10-01 04:31 Taipei).
- 38 `needs_redraft/news_hard_checks_failed` candidates have five stored locale
  documents but no guide article. All 38 include `news_diagram`; nine also have
  punctuation errors. Do not discard those stored translations by blindly calling
  retry: `_queue_new_draft` restarts authoring and incurs new model calls.
- One saved `manual_review/news_hard_checks_failed` candidate is
  `72a833be-5dfe-4eee-becf-a8a080aa930d`, article
  `3e0ca86f-ea38-4f93-9bb5-bf96d71527b9`. It also has punctuation errors;
  removing the diagram requirement alone does not make it publishable.
- Scheduler recovers `discovered` and stale in-flight jobs, not `needs_redraft`
  or `manual_review`. Deployment will not automatically recover these 39.
- Hard-check failure precedes the final-editor hold and Jev's final-call checks.
  A diagram-only lint is not proof that either final gate passed. Standard
  reverify preserves text but an unconfirmed candidate waits for the publish
  button; it does not automatically replay the final editor/Jev stages. Choose
  a supported recovery path and retain every required review decision.
- Preserve separate review decisions for 162 `news_zh_draft_ready`, 133
  `news_duplicate_uncertain`, and other evidence/locale/Jev holds.
- No production writes, restarts, retries or publication were made during diagnosis.
- 2026-10-06 pilot of three held drafts through `backfill_cli --resume-saved-bundles --limit 3
  --apply` (live e12925cc4): 3 of 3 published in five locales, only a `jev-final` run each, no
  model drafting. Details and slugs are in
  `tasks/done/2026-10-04-resume-held-news-drafts-from-their.md`. Left for the owner: whether to
  resume the remaining held drafts the same way (the dry run without `--limit` lists them and
  which locales today's checks still refuse).
