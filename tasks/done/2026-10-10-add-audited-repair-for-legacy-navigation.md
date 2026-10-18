---
id: 2026-10-10-add-audited-repair-for-legacy-navigation
title: Add audited repair for legacy navigation evidence in held news
status: done
priority: P2
area: api
owner: codex-news-recovery-6f71
claimed_at: 2026-10-11T10:23:39Z
created_at: 2026-10-10T06:40:38Z
completed_at: 2026-10-11T10:54:18Z
branch: codex/news-recovery-followup-20261011
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_automation.py
---

# Add audited repair for legacy navigation evidence in held news

## Why

Existing held candidates can retain topic/navigation URLs as evidence even
after the new review-document filter excludes those system blocks. Native
source refresh still fetches every retained URL and rolls back on an unreadable
one. Candidate `9ffcd1c1-236a-4bab-8813-f3026e251476` returned native 409 for
`https://www.coindesk.com/policy` and `https://www.coindesk.com/newsletters`.
Its original refresh intent remains preserved; the failed request must not be
blindly retried or converted into successful evidence by deleting database rows.

## Definition of done

- [x] Provide a dry-run-first, actor-audited service/CLI path for one exact held,
  unpublished candidate with a complete fresh candidate/evidence/guide/history
  CAS and no active DB/RQ work.
- [x] Require independently reviewable proof that each proposed legacy URL is
  system navigation rather than an authored source or claim. Preserve the full
  before/after evidence and affected document provenance; never silently drop
  an unreadable source, relax its qualification, or manufacture a source hash.
- [x] Preserve all old assessments, pipeline runs, revisions, actor audits and
  judge caps. Any content change must go through the genuine guide-save path.
- [x] Keep correction separate from fresh verification/enqueue/publication, with
  new auditable intent and unknown-outcome reconciliation. Do not replay the
  existing `refresh_in_flight` intent or infer publication from dispatch.

## Steps

- [x] Claim this task and inspect the exact evidence role and saved guide sources
  before deciding the narrow native correction contract.
- [x] Add focused tests for CAS drift, active ownership, navigation versus
  authored links, rollback, complete history preservation and uncertain intent.

## How to verify

Run the relevant API lint/type checks and focused news automation tests. In a
future authorized production batch, retain a full read-only before/after proof
and genuine native audit before starting a separate normal review. A current
409 rollback is a blocked outcome, not an installed correction.

## Notes

Root evidence directory is `<home>\.codex\news-review\20261010-6f71`.
`source73-20-step-0602-invoke.one-batch/stdout.raw` contains the native 409;
`source73-20-reconcile-0605.capture` retains full SQL/RQ and durable checkpoints.
The batch's first candidate `9044428a-2288-4f15-bd0a-56d3c108da61` was already
dispatched and is separately proved in `source73-20-completed1-0606.proof.json`;
the third `45ff6fc5-58df-4c8c-bee1-f2e4ad07aa5b` was not reached. Never resend
the three-item batch to work around its second candidate's failure.

2026-10-10 Source8 adds two concrete known native409 cases. Candidate
`2cba0531-7fe5-4739-a2d3-360c13f440b2` failed at 10:12Z on existing
TechCrunch category/artificial-intelligence, tag/ai and tag/mark-zuckerberg
navigation URLs. The complete rollback is independently bound in
`source10-actual0757-after-refresh-mixed-independent-semantics-v8.json`
SHA256 `6e9b936e5474bc8ba5ab5ff7787bde1297eb302afba93fdb19ce03cee7fb74ca`.
Candidate `5fcf6a8f-ba95-4dba-b9ed-ff1fec96829a` failed the next Source8
native refresh at 10:29Z on `https://www.coindesk.com/business`.
Raw intent/output files `source10-plan-0765-native-refresh.*` are preserved;
its full rollback/checkpoint qualification is pending at this note's time.

The deployed navigation exclusion for verification does not itself repair
the legacy evidence rows used by native `refresh_candidate_evidence`.
The repair must distinguish genuine article evidence from navigation,
preserve source/history/cap provenance, and produce its own audited result.
Neither known failure authorizes another fetch of the failed candidate.
Source8's frozen driver can observe a separately proved known409 checkpoint
as a no-op while explicitly handling untouched siblings; this is a different
contract from the older uncertain Source73 intent above.

2026-10-11 02:42 Taipei adds an independently verified publication-time case.
Meta candidate `2ba410eb-ea90-4de6-bc74-b1db01f195d3` completed native retry6,
verification and all five locale reviews, including one normal worker draft
bundle save (versions2->3). Final publication was downgraded to
manual/news_evidence_changed with the exact refusal
`source_content_changed:https://www.theverge.com/tech`. Its retained evidence
also includes `https://www.theverge.com/authors/verge-staff`. Actual before/
after Evidence rows remain identical because the failed publication refetch
rolled back. Do not infer which content bytes changed: the failed HTTP body/
hash is absent from the captured receipts. This case needs the same explicit
navigation-versus-authored-source contract, not another old reverify retry.

Genuine readbacks are `four-meta-source7-phase2-post-0954.capture/sql.json`
and `rq.json`, with Source and original phase2 checkpoint captures. Independent
held diagnosis `four-meta-0954-actual-held-independent-diagnosis-v2.json`
SHA256 `5bf88b16c82985858aeef6f4c90c784d98d34ad968e6cbb09d2b11f23905a8e7`
binds original Save6/full19 archives, exact new job6 and judge6 finished states,
native worker revision/audit joins, full old history and zero operator saves.
Unmodified dedicated Pure5 correctly refuses the post-scan Source row drift;
that refusal is preserved rather than turned into an invented production proof.


2026-10-11 18:55 Taipei implementation and validation:
Claim owner codex-news-recovery-6f71, branch codex/news-recovery-followup-20261011.
The owner explicitly allowed only test_news_automation.py to overlap the
still-owned video task2026-10-10-let-the-owner-re-request-a; its holder and
task were preserved. The --force claim used only this authorized exception.
Fresh pre-PR branch/remote/PR surveys show no competing open PR on service.py
or test_news_automation.py; origin/main still has PR1439 as their last news
implementation. The broad video claim was not released or edited.

Service/CLI details and exact schema keys are in repair_held_navigation and
run_navigation_repair. Use --repair-held-navigation MANIFEST --candidate-id
CID --bundle-sha256 RAW_SHA --review-file REVIEW --review-sha256 RAW_SHA for
dry-run; apply additionally requires --apply --actor-email. Review binds full
Evidence/all5documents/claim ledger, stored excerpt, dated current200 body,
resolved URL, body canonical hash and independently checked raw source receipt.
All inputs/old native rows remain preserved. Fresh verification and publication
use separate original routes after an actual committed repair/readback.

Ruff passes these three paths; mypy app+tests passes859files; final navigation
tests36pass/3Postgres skip. The relevant news automation/pipeline/judge suite
passed524 with6Postgres skips before final regression additions. Independent
source review72f04c0baa55f0bb9ee036dfb9f1306a2f94e53ec52f53900f8a74949fd3233e;
format-only final test peer5818d2bede11a35c9cab14c41ebdd47dfc41d5edd7c9b5c9d7218c7eefe9320e.
Full AST matches; unrelated old test formatting was restored. PostgreSQL
NOWAIT coverage exists but must run in CI/integration; no production repair
has been executed by this implementation. Ledger-cited URLs deliberately
remain blocked and are separately tracked by2026-10-11-add-audited-correction-for-obsolete-held.
