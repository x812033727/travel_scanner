# News held-cohort recovery, 2026-10-10

The owner asked to inspect the review/redraft queues, then explicitly asked to
process them. The inspected cohort is the 208 candidate IDs in
`<home>/.codex/news-review/20261010-6f71/snapshot.json`, captured at 08:36 Taipei.
New arrivals are outside this recovery cohort. The immutable snapshot SHA-256 is
`8545e0f27902e0765a8a73eb21eaabf24cc5241adddf9a7217e38c2fe8aab84f5`.

## Starting state

| Queue | Count | Holds |
| --- | ---: | --- |
| Manual review | 115 | 76 evidence changes, 17 final review, 12 verification, 5 locale review, 4 hard checks, 1 uncertain duplicate |
| Needs redraft | 90 | 75 locale review, 15 verification |
| Failed | 3 | 2 subscription timeouts, 1 slug conflict |

All 90 redrafts have a manual judge outcome; 42 reached the two-rewrite cap.
Seventy-four of the 75 current locale holds concern investment disclaimers.
Eighty-six redrafts retain partial documents. All 114 existing articles are
unpublished and retain five locales. The old 520-ID cohort has 139 unresolved
items (88 review, 51 redraft); the remaining 69 current holds are newer.

## Recovery gates

- Match exact cohort ID, state, hold, retry, timestamps, evidence/source hashes,
  article identity, document hashes, history, and unpublished locale versions.
- Inspect pipeline runs and actual RQ registries before any enqueue. Unknown
  provider, commit or queue outcomes are preserved and reconciled, not retried.
- Preserve saved author text, evidence and judge history. Never reset a rewrite
  cap or fabricate an approval/verification assessment.
- Refresh changed sources through the existing service. Correct factual or
  translation defects using supported sources, then use the normal independent
  verification, locale, hard-check and final-review gates.
- Fix the disclaimer correction cycle before releasing dependent paid stages.
- Submit a small pilot, observe persisted outcomes and public locales, then
  continue the cohort in bounded batches.

## Durable evidence and stage state

External workspace: `<home>/.codex/news-review/20261010-6f71/`.

- `snapshot.json`, `readback.json`, `inspection-items.json`,
  `inspection-summary.json`: original read-only inspection.
- `processing-baseline.raw.json`: fresh full candidate, draft, source, assessment
  and run data for planning actual corrections.
- `collision-check.txt`: no active news-code scope or open PR; the previous
  operations branch remains attached to its own worktree and is not modified.
- `uv-sync.log`: current worktree API dependency preparation.

The code-repair task is `2026-10-10-news-disclaimer-correction-loop` on
`codex/news-recovery-20261010`. The operational task is
`2026-10-10-news-held-cohort-recovery`. This new operation does not take over or
close the older task owned by `codex-news-backlog-review`.

## Completion ledger

- [x] Capture and seal the original 208-ID cohort and current full documents.
- [x] Check shared ownership and claim the isolated repair/operation tasks.
- [x] Reproduce and fix the disclaimer correction cycle; 267 relevant tests,
      full API Ruff and mypy app/tests passed. Independent code review passed.
- [ ] Obtain a verified production repair with deployment guards intact.
- [ ] Complete a guarded source-refresh pilot and read its actual outcomes.
- [ ] Resolve the remaining source, editorial, redraft and technical holds.
- [ ] Reconcile all 208 IDs into verified final outcomes or explicit remaining
      blockers with follow-up tickets; verify public locales for publications.

No production mutation has been performed by this recovery operation yet.

The original four uncertain video-stage jobs are terminal records with completed
timestamps, not live provider calls. They remain untouched. The deployment lock
is held by PID 2701735, a shared READ lease for the renewed-finals video flow.
No lease is removed or process stopped by this news operation; deployment must
wait for its proper release. The source-refresh pilot is independent of that
flow and does not rebuild or restart containers.

Two duplicate decisions are being reviewed: OSS Scanner is already covered by
the published Anthropic Cyber Mission article; the Foresight slug conflict is
the same event as another retained, unpublished five-locale draft. Do not describe
the latter as a published article or discard its existing draft.
