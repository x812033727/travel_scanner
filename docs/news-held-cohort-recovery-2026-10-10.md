# News held-cohort recovery, 2026-10-10

The owner asked to inspect the review/redraft queues, then explicitly asked to
process them. The inspected cohort is the 208 candidate IDs in
`<home>/.codex/news-review/20261010-6f71/snapshot.json`, captured at 08:36 Taipei.
New arrivals are outside this recovery cohort. The immutable snapshot SHA-256 is
`8545e0f27902e0765a8a73eb21eaabf24cc5241addf9a7217e38c2fe8aab84f5`.

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
- Fix the disclaimer correction cycle and system-navigation factual-verification
  payload before releasing dependent model stages.
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
- [x] Reproduce and fix the factual verifier treating system topic navigation
      as an unsupported claim. Fifteen cases fail before the repair; the 282
      affected-suite tests pass afterward, with independent review and all
      API Ruff/mypy checks passing (470 app files, 381 test files).
- [ ] Obtain a verified production repair with deployment guards intact.
- [x] Complete a guarded source-refresh pilot and read its actual outcomes.
- [ ] Resolve the remaining source, editorial, redraft and technical holds.
- [ ] Reconcile all 208 IDs into verified final outcomes or explicit remaining
      blockers with follow-up tickets; verify public locales for publications.

## Verified production actions

The source pilot used exactly three original IDs. Clef-omni candidate
`45c60793-4f8e-492c-8534-c96a5ce46842` published its five locales at 09:23 Taipei.
Actual public API and HTML checks confirm matching published versions, titles,
H1s, canonical URLs and bodies. Anthropic biolab candidate `0f71c3b3` remains
held for a system-navigation false positive; Google calls candidate `6e27eb54`
remains held for source attribution. Neither hold is called completed.

The two duplicate decisions were applied through the real rejection service
and independently read back, with original drafts, sources and histories kept:

- OSS Scanner `ad6ae991-b9f2-4eac-aea0-4dd5a0a8187c`: rejection audit
  `73d2e3b1-4a4a-44b5-a42c-4ea429a72a8f`; the published Cyber Mission article
  remains unchanged.
- Foresight `7d8fa6d8-54fd-49c3-ac2b-6630e22b3e2f`: rejection audit
  `36758e55-de63-4dc4-bf47-87e90435fd1d`; its retained main article is an
  unpublished five-language draft.

Thirty-two independently reviewed editorial corrections were saved through
the real guide service: the first 21 drafts/59 locale commits, the Google calls
draft/five locale commits, and ten further drafts/42 locale commits. Each batch
has independent SQL readback proving exact corrected documents, preserved
candidate holds/retries/cache, source/history rows, untouched locales and null
publication pointers. All 106 actual save audits also match the reviewed
before/after documents and version increments. These drafts are saved and
still await normal review. Corrections address unsupported forecasts, source
attribution, dates, model names, scope and translation fidelity; unchanged
saved languages were preserved.

The two known subscription-CLI timeouts retain genuine matching draft verification
and judge approval. Each was enqueued once at 09:39 Taipei to resume the existing
worker route, after full immutable baseline archival and actual-runtime checks:
Surface `38ca14e5` audit `116a429d-0bcd-4b90-ab01-e6b925ba4200`; NVIDIA
`c407d08b` audit `6c9e283c-e678-474a-a4d8-e7849c3a3ffb`. Both completed saved
five-language drafts and their normal subsequent review stages, then entered
`manual_review/news_evidence_changed`. Neither is published. The original
timeout intents must not be replayed; source follow-up uses a new guarded run.
Enqueue receipts do not establish publication or vendor settlement.
Unknown outcomes are never replayed.

The 10:10 Taipei readback of the original 208 IDs contains 1 published,
2 rejected, 115 manual review and 90 redraft; no failed candidates remain.
The 205 nonterminal IDs have mutually exclusive next routes:

| Next route | Count | Current evidence and dependency |
| --- | ---: | --- |
| Source refresh | 75 | Original remaining73 plus the two completed timeout resumes; new sealed runs, production dry3/dry2 pass, corrected runtime required |
| Owner redraft recovery | 90 | Exact original IDs; production dry3 pass, corrected runtime required, old judge history/42 rewrite caps/86 partial drafts retained |
| Saved corrections awaiting normal re-verification | 32 | Actual 106 saves and independent SQL/audit readback; corrected runtime and fresh guards required |
| Unchanged drafts awaiting normal re-verification | 5 | Anthropic biolab, Muse, Citrix, Emerald and FDA; corrected runtime and fresh guards required |
| Source extension/completion | 3 | GitHub/SB1000, Orchard and Microsoft physical AI; audited source workflow required |

The final per-ID ledger is `original208-recovery-ledger.json` under
`<home>/.codex/news-review/20261010-6f71/`.
`cohort-readback-final.json` is the actual production snapshot; the sealed
completion ledger joins it to the immutable original cohort, save receipts,
public checks, remaining plans and follow-up tickets. A saved correction is
not a completed review or publication.

The source operators preserve the original pilot receipts. New runs exclude
the three already executed pilots; a finished dispatch is never re-enqueued
when its RQ result expires. Actual refresh commits are followed by fresh,
locked full-row comparison before one dispatch. Independent operator tests
cover real save/refresh services, lost acknowledgements, stale ORM reads,
unknown intents and preservation of candidate/source/history/locale state.

The source extension/completion follow-up is
`2026-10-10-add-audited-source-extension-for-held`. Later official signing
evidence and Orchard's versioned author paper cannot be inserted through
raw evidence writes or fabricated evidence-change holds. Microsoft physical
AI's unchanged draft needs the complete excerpt of its existing source.

Durable phase intents/audits are stored in the verified named volume at
`/var/lib/mokaair/video-reviews/ops-news-review-20261010-6f71/`, with host copies
and local logs. No fake approval marker, cap reset or settings change was used.

The original four uncertain video-stage jobs are terminal records with completed
timestamps, not live provider calls. They remain untouched. The deployment lock
is held by PID 2701735, a shared READ lease for the renewed-finals video flow.
No lease is removed or process stopped by this news operation; deployment must
wait for its proper release. The source-refresh pilot is independent of that
flow and does not rebuild or restart containers.

Both code repairs are in draft PR #1411. All 22 repository CI checks passed
on code commit `5f152be3e36ce873cd561a911baf60828bde160a`; the final records-only
commit receives its own required checks. Merge and deployment require the owner
gate; the existing shared video deployment lease must be released by its owner.
The production runtime remains `35f99a16d7e4bcd5807845cdeded929894bf21ac`.
Local tests and CI do not establish a deployed repair.
