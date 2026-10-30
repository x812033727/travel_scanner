---
id: 2026-10-29-release-localized-retrieval-ai-concepts
title: Release localized retrieval AI concepts
status: done
priority: P2
area: docs
owner: codex-release-ai-retrieval-sixteen-20261029
claimed_at: 2026-10-29T12:55:20Z
created_at: 2026-10-29T12:25:43Z
completed_at: 2026-10-30T08:27:44Z
branch: codex/release-ai-retrieval-sixteen-20261029
depends_on:
  - 2026-10-29-localize-four-retrieval-ai-concepts
scope:
  - docs/article-localization/releases/2026-10-29-retrieval-ai-concepts
---

# Release localized retrieval AI concepts

## Why

Before this release, four published retrieval-concept articles lacked public English, Japanese,
Korean and Simplified Chinese documents. Their sixteen reviewed translations and
forty-eight localized assets are being delivered by the dependent content task.
Publish this exact cohort after its content PR is approved and merged, using a
fresh release plan and explicit action-time authorization.

## Definition of done

- [x] Verify the merged content commit, green CI, fresh source hashes and exact deployment range.
- [x] Obtain approval for a concrete dry-run, full backup/restore, deployment and publication plan.
- [x] Complete the authorized release with unchanged native tooling and retained actual receipts.
- [x] Verify twenty five-language public pages, sixty total assets and desktop/mobile screenshots.
- [x] Record publication versions/hashes and a fresh whole-site public-language census.

## Steps

- [x] Claim this release task only when the dependent content task is done and its PR merged.
- [x] Read current deploy and article-localization skills; verify live runtime, holds, locks and source/target state.
- [x] Disclose all pending commits and migrations; prepare the exact image and same-image isolated rehearsal.
- [x] Run a fresh production read-only candidate dry-run for exactly sixteen new documents and zero source/hub changes.
- [x] Ask the owner to authorize the complete concrete release plan; previous PR1920 approval does not authorize this release.
- [x] After approval, take a full database backup and prove an actual isolated restore before any production writes.
- [x] Deploy only as authorized, repeat the same-image rehearsal and fresh dry-run, then publish the exact reviewed bundle with a new journal.
- [x] Verify database readback, links, idempotent dry-run and every public page/asset; inspect desktop/mobile screenshots independently.
- [x] Complete final host verification, clear only proven cohort-owned holds, and preserve every backup and failure receipt.
- [x] Refresh the global public-only locale inventory and prepare independently reviewed evidence in this task's scoped release directory for the records PR.

## How to verify

- Exact cohort: ai-term-embedding, ai-term-semantic-search, ai-term-reranking,
  ai-term-retrieval-augmented-generation; targets en, ja, ko and zh-CN only.
- Candidate source baseline: all four zh-TW documents were public/draft version 8,
  article version 2, with no target rows at the actual read-only snapshot.
  Recheck before release; this historical snapshot is not fresh release approval.
- Use unchanged native publisher, pinned reviewed bundle, same-image rehearsal,
  actual backup/restore receipts, exact runtime/image identity and public QA.
- Expected acceptance: four source pages plus sixteen translations, twelve
  original assets plus forty-eight new assets, and forty desktop/mobile cases.
  Confirm the final screenshot count in the concrete release plan.

## Notes

- The owner explicitly approved merging #1922 and preparing its release plan.
  The exact approved head f9c9c6fafb2c5f88d05c3ddaf8d9f3f96dbc6eb2 passed
  all 22 CI checks and independent review. It was squash-merged at
  2026-10-29T12:52:47Z as f3895e9df12cf68698285a51bc4af8b8fedc718c;
  the reviewed and merged Git trees are identical. This task was then claimed.
  At that merge-only checkpoint backup, hold acquisition, deployment and
  publication were not authorized; a complete plan was prepared separately.
- Candidate manifest SHA-256:
  1be206c2bbdd0fbdebf45a9a3c1dcdb378304c498e93ca2a00ce31336dbabe5b.
  Baseline SHA-256:
  bdc10b0cf4788f2a27b516a53900d8780624a3a40e297954ccb26f8f31219d2f.
  Private jobs, reviews, bundle, native install journals and snapshots remain in
  the owner's durable evidence directory and ignored local mirrors.
- The earlier sixteen-document cohort has already been published and verified;
  do not redeploy it or recreate its cleared hold. The latest actual global
  census remains 2,250 public articles, 1,482 complete in five languages, 768
  incomplete and 3,072 missing public locale documents; 120 draft-only rows were
  excluded. Do not reduce these counts for the current unpublished sixteen.
- Fresh native host preflight at 2026-10-29T12:57:32Z observed deployed checkout
  2464ad1c9c0ee0e2a9f0b9e3bb435ffa706be4cc, a clean tree, no hold and a free
  deploy lock. The exact-four READ ONLY snapshot completed at 12:58:55Z:
  all sources remain zh-TW draft/public v8, article v2, and all sixteen target
  rows are absent; API container/image identity stayed unchanged. Verify the
  database migration revision and API/web identities before classifying the
  actual deployment range. Subsequent full observation at 13:29 UTC verified
  schema 0143_video_daily_briefs already applied, stable API/web/Postgres/Git
  identities, healthy endpoints and the same four sources/absent target rows.
- Remote main advanced during preparation. Candidate c1 correctly refused at
  its remote-target gate before entering the database or native publisher;
  its failure and untouched staged payload were retained. The new fixed target
  is d0857cc450db89c064eb7da8b20fd00d1783afb0. From deployed 2464ad1c9 this
  includes #1922 and #1921, exactly two commits and 67 paths. The additional
  application change skips queued daily-brief dates already represented by a
  VideoProject and writes an audit row, allowing subsequent dates to proceed
  under the existing enabled automation. Its test, eight caption JSON files,
  two docs and one task record are also in the range. No new migration,
  dependency or ops changes are present. All 64 reviewed content/media files
  remain byte-identical to #1922; normalized source documents remain unchanged.
- Candidate c2 actually exited 0 at 2026-10-29T13:35:43Z; full evidence download
  exited 0 at 13:37:54Z. It planned exactly 16 start_translation, 16 publish,
  zero hubs and zero source corrections. Eight completed SELECT statements,
  zero rejected statements, unchanged native/selected nine-key state and
  runtime, and an empty-write candidate journal were independently verified.
  This SQLAlchemy no-DML guard is not PostgreSQL-enforced READ ONLY; native
  transaction/locking semantics remain intact. The journal is candidate-only.
  Actual receipt SHA-256:
  438de78a769a0788333fa56d4fa2078d102f6621252a3c4ccc42a000266f41c7.
  Independent actual readback SHA-256:
  7c814769bea7cee84aeaf41b5e3efd0b1787be6859836bcd10997abd2ce77614.
- The new target's 22 validation checks and two update checks all succeeded;
  announce was conditionally skipped. Raw CI evidence SHA-256:
  726aa9f3977db91ff1d323d2545f10046812eb0624d19582e82ce11bf2c0b717.
  CORE/binder, content/QA and census code reviews passed. Actual local prepare
  exited 0 and bound the real candidate, actor and CI while keeping execution
  disabled and approval null. Independent ready-binding review SHA-256:
  67ba780c83b332b2f61eaf143263619c44dfa0b7104241856f7896b7dc023f7f.
  Final proposal passed 232 independent checks, with all 30 indexed evidence
  files and 48 nested package-index entries verified. Plan SHA-256:
  9bf64b94d8a234a3c60a571b904f328be7472910cddf838f268762d622f3a5cd.
  Final review SHA-256:
  3f3820869b24853474a651c841f8d84a6a97c15cd1821bca4c294a1552c86711.
  The owner was asked to approve the full fixed-target release, including
  #1921's daily-brief behavior. No production backup, restore, hold, deployment
  or publication had been executed at that preparation checkpoint.
- On client date 2026-10-30 the owner directly replied "繼續" to the reviewed
  full release proposal. This continuation authorizes the disclosed fixed
  scope, including #1921; its literal wording and context were retained, with
  no invented option selection. Local authorization binding actually exited 0
  and preserves all seventeen reviewed code files. Approval evidence SHA-256:
  dd32556a513e5ca4d12bc39d9c8f0b81d14ff6ac3356f5dd89db1439e715639e.
  Fresh host preflight at 23:45 UTC retained base 2464ad1c9, target d0857cc4,
  a clean tree, no hold/free lock and the unchanged uncertain/queued counts.
  Full source/runtime and settings probes exited 0; independent final binding
  and transport audits precede the first host mutation.
- Keep the all-article five-language task open until fresh production evidence
  establishes completion. Store only sanitized release receipts in Git.
- At 23:52 UTC the initial private upload succeeded, but installation refused
  before creating the release stage because main had advanced to bf8881941
  (#1923). Its eight daily-video caption/description JSON changes are excluded
  from this release. A separately reviewed actual readback confirms the formal
  stage is absent, the original runtime/range remains, and no hold, backup,
  deployment or publication started. Failure and uploads are preserved.
  Preparation now keeps the already authorized d0857cc4 target fixed, with a
  new reviewed ancestry guard and explicit fixed-target native merge. The
  original approval, cohort and action scope remain unchanged; no new approval
  or additional deployed commit is claimed.
- On 2026-10-30 the fixed-target CORE installed successfully and the real
  full backup and isolated restore ran. The 578,703,137-byte dump and native
  restore both exited 0; restored and production before/after snapshots agree.
  The overall backup phase stopped at its final version guard because main
  advanced again and that newer commit object was not locally available.
  Its original worker exit 1 and stopped state, full dump, isolated database
  and owned hold are preserved. Deployment/publication have not started.
  A separately reviewed validation continuation is being prepared to verify
  the completed restore and fresh state without relabeling the failed worker
  or repeating the backup. The approved target remains d0857cc4.
- The separate validation continuation completed at 2026-10-30 00:31:28 UTC
  with its own real exit 0 and accepted receipt. All 107 original evidence
  files remain unchanged, including the failed worker. The 220-file export
  and actual backup/restore proof passed 1,087 independent checks; acceptance
  review SHA-256:
  d08e47bf674f7efc305c5e63266c8aef95cf84af76331507a9f2a5ef2c0dda3b.
  The actual fixed-target deployment was started successfully at 00:41:25 UTC
  after independently reviewing its generated binding. It is still running;
  no deployment completion or publication is claimed at this checkpoint.
- Deployment subsequently completed with real native/worker exits 0 at
  2026-10-30 00:46 UTC and independent acceptance. The same-image isolated
  rehearsal completed at 01:06 UTC: exactly 16 drafts, 16 publications and
  zero hubs, 32 revisions and 32 audit rows; all 168 table fingerprints were
  unchanged by the full replay. The fresh live dry-run completed at 01:08 UTC
  with a new empty journal and the same exact plan. Preparation acceptance
  SHA-256: c211ac9e73424bd307f0fed502519e4dc2e80c212a6b2411c5f7b3af85d9db90.
  Fresh source checks cover the four native article/locale snapshots and
  complete zh-TW rows; the backup's broader nine-category snapshot remains
  historical evidence, not a newly recaptured post-deployment snapshot.
- The real publication group completed at 01:20:44 UTC with exit 0, accepted
  true and no error: drafts, article publication, zero-hub phase, live replay
  and scoped links all completed. Its worker receipt SHA-256 is
  84a5ff189f73efb96584dba0b28e7be9e3afa74b4b7629b74e35b856322a2598.
  The complete 2,219-file export was downloaded and verified; independent
  publication acceptance and public visual QA are still pending at this
  checkpoint. The cohort-owned hold remains; final host verification, fresh
  census and the records PR have not yet been completed. Do not call the
  release or global language-completion task done from publication alone.
- Actual public capture completed at 2026-10-30T01:33:28Z with native exit 0:
  twenty exact public documents, sixty assets, forty original desktop/mobile
  captures and 195 real HTTP 200 responses. Two independent reviewers actually
  inspected all forty originals; their static-image limitations are preserved.
  All 52 expected references to unpublished translations render as authored
  plain text with no matching anchor. Actual QA assembly exited 0 and its
  independent acceptance is 3cda8ba950d1ff62fa609b696d465f32dce0b9fbd8298c5955559c4acc11d7db;
  public acceptance is 830f4dac47a4673c72ff34eea770003a3b14457793539a001ccd59fe32369937.
  Finalization, owned-hold removal, unlocked 11/0, fresh census and the records
  PR remain pending at this checkpoint.
- Finalization actually stopped at 2026-10-30T01:49:42Z with worker exit 1
  and accepted false. The owned hold was cleared, but the unmodified host
  verifier printed 9 PASS / 2 FAIL. Its shell exit 0 is not acceptance.
  The genuine failures are 28 API QueuePool timeouts and four non-exempt
  video auto exits in the native 30-line window. Original failed receipts
  are preserved; independent failure evidence audit SHA-256:
  bfe3eea047054a0779c4d1670b2da9ad826b8e8338e057b51719b7aabcd85c7d.
  Public QA acceptance above remains valid; full release acceptance, fresh
  census and the records PR remain incomplete.
- A bounded read-only log diagnostic completed at 2026-10-30T02:02:59Z.
  Before/after witnesses confirmed unchanged deployed runtime, no hold and
  available existing locks. All 28 pool timeouts occurred from 01:47:45 to
  01:48:41 UTC, with no further matching error through the 02:02:55 cutoff.
  Speech routes have a confirmed pre-existing risk of holding a database
  transaction across external provider calls; incident causation is unproved.
  The video check loses cap context across known interleaving and a short
  log window. Diagnostic integrity/runtime review SHA-256:
  7bd4b6e7472c4e035e9b5f0456bc86d68823b743dff315b1dbd5c3e3d095f6a5.
  Corrective proposals and tests are being prepared privately because the
  relevant API and verifier files have existing task/PR owners. No held
  source file, quota, host setting or runtime has been modified for these
  proposals. Original finalization will not be rerun or relabeled.
- The private corrective proposals subsequently passed independent review:
  175 focused API tests (one existing PostgreSQL case skipped), 18 native
  verifier tests, and 35 additional positive/negative native verifier fixtures.
  Combined proposal-review SHA-256:
  86ca3bae40c86fce00df1efc272d74732fbd4b5e71c8ea9dd712d51fef6d505e.
  Follow-up task `2026-10-30-retrieval-host-acceptance-repairs` is recorded
  in an isolated worktree and currently claims only its own metadata.
  Implementation awaits a narrow owner-approved overlap exception because
  the shared source files remain held by other tasks/PRs. These local results
  do not change the failed production acceptance or authorize a new deployment.
- At 2026-10-30 03:55 UTC, the owner-approved four-file overlap exception had
  been implemented in isolated repair PR #1929 at
  `97144bcd2cb196ee24a54410853b198a411c2f0b`. All four source/test files match
  the independently reviewed patches. Local API 175/1 skipped and native
  verifier 18/0 skipped passed; all 22 CI checks then passed. CI explicitly
  ran the previously skipped PostgreSQL cancellation case and all 16 new
  session regressions. The full Linux tools suite passed 2811/3 skipped and
  video documentation tests passed 239/0 skipped. Both incomplete local full
  tools executions were deliberately interrupted; neither is a local full
  suite pass. The PR remains draft with no-auto-merge, awaiting its separate
  owner merge decision. No deployment or production write occurred, and this
  broader release task remains blocked pending a newly approved repair
  release and successful host acceptance. Original failure receipts, census
  and remaining publication-record work are unchanged.

- 2026-10-30 04:26 UTC: owner separately approved merging #1929 and preparing
  the production repair plan. Reviewed head `97144bcd2` was squash merged as
  `5c105c01b448c9997e70beac2abd787bf46c4222`; trees are identical. Fresh read-only
  host preflight/probe passed: live remains `d0857cc45`, no hold, schema 0143,
  and all 20 published locale versions unchanged. The pending target contains
  five commits / 15 paths, including video docs, with no migration. A new exact
  target, backup/isolated restore, same-image probe and reacceptance plan is in
  preparation at `repair-release-preparation-01`. Main CI/plan cross-review are
  still pending. No production write/deploy is authorized by this merge answer;
  original 9/2 failure and broader BLOCKED status remain unchanged.

- 2026-10-30T04:51:47.824835+00:00: merged repair target `5c105c01` passed all22 main CI. Final
  production repair plan and prepared components passed independent review and
  were sealed in `repair-release-preparation-01`; plan SHA `1617dad8a0be0b8bbd6c41b00d01a4bf5e24681ea074b8da68558c63bd41961e`,
  package SHA `2696a5964bf6f9a63fbc3bc40b2836cedf0a2889ab65486cdb3e5383dfa483f3`. Fresh readonly64-file preservation
  passed; actual fixed-target readonly survey refused with trueexit2 because the
  target Git object is absent, without fetch/native fallback. The new owner
  decision covers exact-object preparation, full backup/isolated restore, fixed
  deployment, same-image probe and20/60/40 reacceptance, final11/0 and census.
  It has not yet authorized execution. Original9/2 failure remains immutable;
  no production mutation, deployment, fresh census or new record PR has occurred.


### 2026-10-30 completed repair and publication records

The separately owner-approved repair deployed exact target
`5c105c01b448c9997e70beac2abd787bf46c4222` after a new full database backup
and actual isolated restore. The unchanged-image isolated session rehearsal
passed all ten fake-provider cases; the original failed startup attempt remains
retained separately. Fresh readback preserved all twenty documents, source v8
and target v2, sixty assets and existing video references. New public QA and
independent visual review passed twenty pages, sixty assets and forty captures.

The actual stability window lasted 300.609304 seconds across eleven samples,
with full uncapped logs and source continuity. Fresh gap checks, guarded own-hold
clear and the final native verifier completed: eleven PASS, zero FAIL, native
exit zero. The finalization child exited zero and its monitor recorded COMPLETE
at 08:05:31 UTC. No article was republished by this repair; backups, isolated
resources and historical failure records are retained. Original 9/2 remains a
failed historical attempt, not a relabeled success.

Final actual receipt: `373cfc4523a5667a38e3d2469279d8a663cfd6610dc876267ce116037db84cfa`.
Independent final review: `8810338614a4fd2265822c4468f018219b2db3574017379982bd60f1148646a1`.
The two sanitized release records are in
`docs/article-localization/releases/2026-10-29-retrieval-ai-concepts/`.
Their independent records review is
`c3bb7da9b07c43535d6a6879c38bed76bb8ad96b403135d8900a18d4176078c9`.

Fresh read-only census: 2,286 public articles, 1,522 with all five public
languages, 764 incomplete, and 3,056 missing documents; 128 drafts excluded.
This metadata census does not establish translation/source freshness.
The overall language-completion task remains open. This records-only PR
requires its own merge approval and needs no deployment.
