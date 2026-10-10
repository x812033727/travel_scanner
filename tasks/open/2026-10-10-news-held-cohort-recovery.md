---
id: 2026-10-10-news-held-cohort-recovery
title: Resolve the 208 held news candidates inspected on October 10
status: in-progress
priority: P1
area: ops
owner: codex-news-recovery-6f71
claimed_at: 2026-10-10T00:53:32Z
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
- [ ] Published articles have actual public locale verification, independently
      of queue/worker success.
- [ ] All writes have exact guards, durable intent/audit receipts and readback;
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
- Two duplicate rejections have real audit/assessment readback. Twenty-one
  reviewed drafts (59 locale commits) were saved in bounded3 batches, with
  independent SQL preservation readback; these remain unpublished and held.
- Timeout2: actual old runtime and genuine verified/judge-approved draft checks
  passed. Each received one enqueue after full durable archival; outcomes are
  pending, with no replay of unknown jobs and no claim of publication.
- A second completed code task, 2026-10-10-exclude-system-topic-navigation-from-news,
  repairs the pilot's navigation false positive. Both repairs are in draft PR1411;
  merge/deploy and the other owner's shared video lease remain separate gates.
