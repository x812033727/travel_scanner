---
id: 2026-10-10-add-audited-held-news-bundle-ingestion
title: Add audited ingestion for held news draft bundles
status: in-progress
priority: P2
area: api
owner: codex-news-held-bundle-ingestion
claimed_at: 2026-10-11T06:46:06Z
created_at: 2026-10-10T06:04:34Z
completed_at:
branch: codex/news-held-bundle-ingestion
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_automation.py
---

# Add audited ingestion for held news draft bundles

## Why

Held news can stop with only two cached language documents and no guide
article. An editor can correct and complete the source-bound draft bundle,
but the existing news reverify service requires an existing guide and all
five saved locales. The generic guide importer does not bind its article
to a NewsCandidate. Direct cache/database writes would lose normal audit
and provenance evidence.

In the original208 recovery, CFTC candidate
`e25bc5a4-cca4-4e61-bb77-5b1b45243561` is `needs_redraft`, retry 4,
with only zh-TW and ja cached documents, no guide and two preserved judge
rewrites. The latest Japanese failure fingerprint matches the cached
document. A concrete external five-language correction package now exists,
but has no native ingestion path and truthfully retains `no_hero` for every
language. The latest original208 census at 2026-10-11T06:31:33Z has
22 redrafts without a guide; this operation still selects exactly one CID.

## Definition of done

- [x] An explicitly selected held candidate accepts a reviewed, complete,
  source-bound draft bundle through a normal audited service/CLI operation.
- [x] The saved guide is linked to that exact candidate, with genuine native
  revision/audit identities and owner-authored provenance distinct from model runs.
- [x] Original candidate history, evidence, rewrite caps and uncertain requests
  remain intact. A pending asset or review gate remains pending.
- [x] Fresh verification, all locale reviews and final JEV use the corrected
  documents; ingestion itself never approves or publishes them.

## Steps

- [x] Reuse native guide creation/save primitives and add candidate/source-bound
  ingestion with expected status, retry, evidence and complete-history CAS.
- [x] Reject incomplete languages, invalid schema, content-policy failures, changed evidence,
  concurrent work, unrelated candidate/article bindings and reused uncertain intent.
- [x] Record missing assets as an unresolved downstream gate; saving a draft
  with no hero must never be reported as passing publication policy.
- [x] Preserve owner-authored bundle provenance without fabricating writer runs,
  model assessments, audit reasons or source-extension records.
- [x] Keep asset generation, review dispatch and publication as separate native
  stages with fresh guards and persisted readbacks.

## How to verify

Run focused API tests for partial-cache/no-guide recovery, source or candidate
drift, concurrency, native save commits and revision/audit joins, a repeated or
uncertain intent, a genuine cap-2 history and a missing hero. Assert that ingestion
does not publish or fabricate a model run and that downstream checks review the
exact newly saved document fingerprints. Use a bounded dry run before a separately
authorized production operation; inspect actual SQL/RQ history afterward.

## Notes

- External evidence root: `C:\Users\x8120\.codex\news-review\20261010-6f71\`.
- Actual `processed-held25-actual-0563.json`, SHA256
  `985b829eac27cee719cc335d52318c4c224cb9614ad37f7a725f6a0e42e304cb`,
  captured the exact 25 selected candidates at 05:49:01 UTC.
- Concrete `cftc-reviewable-five-v3/manifest.json`, SHA256
  `65a1dd10eaf4f763c5e289cc4cc8b2cee1f6e3004fa8703939280d613796d779`,
  preserves zh-TW, corrects the source-bound Japanese statute bracket, and
  supplies en, ko and zh-CN translations. The true remaining hard issue is
  `no_hero` in all five documents; this is not an approved or saved native bundle.
- Existing `reverify_candidate` permits manual/shadow/failed statuses; its
  `_queue_reverify` additionally requires an existing guide with all five
  locales. CFTC's current status and missing guide both fail those prerequisites.
- The judge cap prevents further automatic judge-redraft rounds. It is not
  itself a blanket prohibition on publishing a corrected draft that later
  passes normal verification and JEV; do not invent a cap-reset approval gate.
- At filing, no native CFTC ingestion, save, asset generation, extra retry,
  source change, approval or publication has been performed.
- Independent native workflow report
  `cftc-partial-cache-native-workflow-independent-operator-v1.json`, SHA256
  `a4ec18e4a62b40359cf7166533385ef6a6ead32999623b4d45348bb0c8c6c633`,
  confirms the current prerequisite gap and reusable native primitives.
- Independent complete five-language content review
  `cftc-reviewable-five-v3-independent-content-operator.json`, SHA256
  `e2de2380800fccd02b36a7653e02ebc98d361fe5f84227107eee8a84827bc02b`,
  passes source and translation checks while truthfully retaining five
  `no_hero` failures and no native save, new model approval or publication.

- 2026-10-11: the video dub task intentionally retains its host-validation claim
  after PR1432 merged. Its broad apps/api/tests scope includes the otherwise
  untouched test_news_automation.py. Root removed that test path before claiming
  the three non-overlapping implementation files. Committed test changes await
  the owner's explicitly requested narrow scope exception; external tests and
  current existing tests may run without editing another claimed file.

- Owner reply on 2026-10-11 explicitly authorizes only the news test-file scope
  exception while preserving the video task and its holder. The own-ticket
  claim extension uses --force only for the broad tests-directory overlap;
  exact four news files remain disjoint from merged PR1432's video changes.
  No foreign ticket is released, finished or edited.

- Native CLI workflow: `python -m app.news_automation.backfill_cli
  --capture-ingestion-state --candidate-id <CID>` captures the complete selected
  state. A SHA-pinned `--ingest-held-bundle <manifest> --candidate-id <CID>
  --bundle-sha256 <SHA> --review-file <review> --review-sha256 <SHA>` validates
  without writes. Add `--apply --actor-email <admin>` only for the separately
  guarded draft save. Capture is fresh for 900 seconds; apply rechecks all rows
  under PostgreSQL NOWAIT locks and refuses actual live RQ work.
- The manifest and draft-only review contracts are documented by the CLI
  function. Source refs and full five-document hashes must match the actual
  evidence and independent review. Missing hero assets remain unresolved.
- Before apply, the operator must create the private mode0700 directory
  `/var/lib/mokaair/video-reviews/news-held-bundle-ingestion` on the existing
  persistent volume. A stable `<CID>.intent.json` is fsynced before mutation
  and retained on every outcome. An unknown commit response requires native
  audit/revision readback; changing the operation UUID cannot bypass that intent.
- The initial frozen implementation passed 35 focused tests and 733 existing
  news tests (10 local integration skips), full API Ruff and both mypy groups.
  Independent review reproduced empty-argument backlog fall-through and two
  concurrency defects. Their original receipts remain preserved; final fixes
  and real PostgreSQL integration coverage are being verified before PR.

- Final frozen v2 passes 52 focused cases; three real PostgreSQL cases explicitly
  skip without RUN_INTEGRATION_TESTS=1. They cover candidate NOWAIT, a genuine
  guide-editor write blocked by locked locales, and committed version drift.
  Full API Ruff and mypy app471/tests388 pass again. The complete API pytest
  run is ongoing at draft-PR preparation; real PostgreSQL checks remain a
  required CI gate, not a local claim of row-lock effectiveness.
- Nonauthor code review `held-news-bundle-ingestion-frozen-v2-independent-code-review-v1.json`,
  SHA256 `e21e053af2069dcef5c7dbd2a8ad769a9f8fc182b4dc2715a8d872cd89bd9b5f`,
  passes the final exact four source hashes. Its actual local boundary tests
  `8db5fe1d64f22555ed22086c297ebe95e19fb3109f39111b08e77c120c90825a`
  refuse late worker/old ORM/false handoffs and allow genuine reverify followed
  by an ordinary owner retry. The initial race receipt555a8d94 is retained.
- Independent CLI review `held-bundle-ingestion-cli-independent-final-review-v2.json`,
  SHA256 `14ba524075c039dfe52cc6c8033ac2b52b05c1f9e59c9a1dd7ff141eaeefd9f3`,
  passes 21 Windows and 21 POSIX cases, including actual file/directory fsync.
  Commit/actor checks there are explicitly marked stubs, not production proof.
- The saved ingestion audit remains the worker fence until a linked, genuine
  actor-owned native reverify/evidence-refresh audit advances the retry count.
  A marker or retry change alone cannot start another draft. This also preserves
  ordinary subsequent owner retry behavior after the first genuine handoff.
- Implementation completion does not mean deployment, CFTC ingestion, asset
  generation, new model approval or publication. Those remain separately
  guarded operations under the open original208 recovery task. The full news
  cohort and the published Secure/Bitmine corrections remain unfinished.
