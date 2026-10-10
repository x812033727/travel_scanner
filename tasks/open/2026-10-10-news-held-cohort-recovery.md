---
id: 2026-10-10-news-held-cohort-recovery
title: Resolve the 208 held news candidates inspected on October 10
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-10T00:53:31Z
completed_at:
branch: codex/news-recovery-20261010
depends_on: []
scope:
  - docs/news-held-cohort-recovery-2026-10-10.md
---

# Resolve the 208 held news candidates inspected on October 10

## Why

The owner asked to process the 208 candidate IDs inspected on 2026-10-10:
115 review holds, 90 redrafts and three failures. Most cannot be resubmitted
to the judge as-is. Preserve existing documents and evidence, repair technical
or editorial defects, and use the normal independent review/publication gates.
New arrivals are outside this operation.

## Definition of done

- [ ] All 208 IDs have a persisted final decision/publication or a documented
      unresolved blocker with its own follow-up and preserved artifacts.
- [x] Published articles have actual public locale verification, independently
      of queue/worker success.
- [x] All writes have exact guards, durable intent/audit receipts and readback;
      model/commit/queue uncertainty and previous judge caps remain preserved.

## Steps

- [x] Capture full current candidate, source, draft, assessment and run data.
- [x] Check ownership, create an isolated branch and claim this narrow operation.
- [ ] Repair the disclaimer correction loop and verify production readiness.
- [x] Run a three-item source-refresh pilot and inspect its decisions.
- [ ] Continue the remaining source cohort after repairing the pilot defects.
- [ ] Correct saved editorial drafts and redrafts; resolve duplicate and failures.
- [ ] Reconcile all 208 outcomes and verify published locales.

## How to verify

Use read-only candidate/assessment/run/audit and article-locale snapshots bound
to the exact original ID cohort. Inspect actual RQ jobs before replaying any
operation. Verify public pages after persisted publication. Queue submission,
a judge approval, local tests and CI are distinct stages.

## Notes

- Durable external workspace: `<home>/.codex/news-review/20261010-6f71/`.
  The cohort snapshot digest and completion ledger are in
  `docs/news-held-cohort-recovery-2026-10-10.md`.
- The code-repair task is `2026-10-10-news-disclaimer-correction-loop`.
- Source76: guarded pilot3 executed after independent review and real dry-run.
  One five-language publication has actual public verification; two are held
  for navigation/source attribution defects. Remaining73 were not dispatched.
- The 08:55 Taipei host preflight found the deploy lock held and four uncertain
  paid-video stage records. Their actual ownership/liveness must be inspected
  before scheduling a deployment; do not clear unrelated paid-work evidence.
- The old `2026-10-07-resolve-current-news-review-and-redraft` task stays with
  its existing owner/worktree. This operation neither closes nor edits it.
- Two duplicate rejections have real audit/assessment readback. Thirty-two
  reviewed drafts (106 locale commits) were saved in bounded batches, with
  independent full SQL and actual audit before/after/version verification;
  these remain unpublished and held.
- Timeout2: actual old runtime and genuine verified/judge-approved draft checks
  passed. Each received one enqueue after full durable archival, completed
  saved five-language drafts and normal reviews, then entered actual source
  change holds. Neither is published; do not replay the old timeout plans.
- A second completed code task, 2026-10-10-exclude-system-topic-navigation-from-news,
  repairs the pilot's navigation false positive. Both repairs are in draft PR1411;
  merge/deploy and the other owner's shared video lease remain separate gates.
- Fresh 10:10 Taipei exact208 readback: 1 published, 2 rejected, 115 manual
  review and 90 redraft, no failed. Remaining routes are75 source,90 redraft,
  32 saved corrections,5 unchanged reverify and3 source extension/completion.
  All205 nonterminal candidates remain explicitly pending.
- Prepared source73/source2 new-run operators and owner90 recovery have passed
  independent reviews and real host dry pilots. Actual apply still requires
  the exact corrected deployed runtime; no additional dispatch took place.
- Source extension/completion follow-up:
  2026-10-10-add-audited-source-extension-for-held; finance contextual-lint
  follow-up: 2026-10-10-distinguish-reported-and-negated-trading-verbs.
