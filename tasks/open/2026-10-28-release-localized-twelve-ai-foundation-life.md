---
id: 2026-10-28-release-localized-twelve-ai-foundation-life
title: Release localized twelve AI foundation life guides
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-ai-foundations-release
claimed_at: 2026-10-28T11:01:31Z
created_at: 2026-10-28T07:58:43Z
completed_at:
branch: codex/release-ai-foundations-20261028
depends_on:
  - 2026-10-28-localize-twelve-ai-foundation-life-guides
scope:
  - docs/article-localization/releases/2026-10-28-ai-foundations
---

# Release localized twelve AI foundation life guides

## Why

The dependent content task adds en, ja, ko and zh-CN documents and translated
artwork for twelve already-public Traditional Chinese life articles. Repository
installation does not create or publish production locale rows. This separate
task owns the guarded release and its public acceptance evidence.

## Definition of done

- [ ] The exact merged content revision has green checks and is present in the deployed revision.
- [ ] A fresh production snapshot, publish holds, source versions and a pinned native bundle authorize exactly 48 missing target locale rows.
- [ ] The owner approves the concrete deployment/publication scope; a fresh database backup is verified before any production write.
- [ ] All four native publisher phases and their replay pass, with no pending journal operation and no change to the twelve zh-TW sources.
- [ ] All sixty public pages pass document/image/canonical/hreflang/link checks and actual desktop/mobile visual acceptance.
- [ ] Only sanitized release evidence is committed under the declared release directory.

## Steps

- [x] Confirm the dependent content PR is merged and its exact-head checks passed.
- [x] Inspect the full pending deployment range, migrations, active hold/lock state and production publish holds before proposing deployment.
- [x] Bind a fresh repeatable-read snapshot, source versions and current absence of target rows to the reviewed native bundle; stop on drift.
- [x] Run a candidate-only native dry-run against production state and present the exact create/publish counts for owner approval.
- [ ] Repeat native dry-run after verifying the actual deployed runtime; never reuse the candidate journal for publication.
- [ ] Take and verify a fresh pg_dump backup, then deploy the approved content revision under the release driver's hold ownership.
- [ ] Execute drafts, publish-articles and publish-hubs using the same bundle, baseline, manifest SHA and durable state directory; rebuild/check links.
- [ ] Reconcile database rows and journal, replay without writes, verify all public pages/images and inspect desktop/mobile screenshots.
- [ ] Write README.md and evidence.json, close this task in the evidence PR, and remove only the release driver's own hold after successful final verification.

## How to verify

Follow the article-localization and deploy skills, the native publisher's guards
and `ops/release/README.md`. Use `report_progress.py` with the actual journal and
hash-bound browser evidence; files existing locally or green CI cannot establish
publication. Retain source snapshots, backup receipts, logs and screenshots in a
persistent directory outside Git. Inspect release-safety CI with real PostgreSQL.

## Notes

- PR #1911 merged as `2668668feda6aa158dff048e4655dbde5c21fd7b` after all
  22 checks passed on the exact approved head. The merge tree equals that head.
- Initial release preparation on 2026-10-28 found live revision `4c4bf7fde`;
  the range at that time was PR #1912 (two task documents) and PR #1911 (this cohort).
  No application code, dependency, migration, Compose or Dockerfile changes are
  in that range. Deployment hold absent, deployment lock free, no active paid
  video stage job observed. These are preparation observations, not action-time
  authorization or a substitute for fresh preflight.
- The 11:02 UTC repeatable-read selected snapshot passed native validate_initial:
  twelve public, active, unexpired source articles, exactly twelve zh-TW rows,
  and all 48 target rows absent. Snapshot SHA-256:
  `dac9b79e31b3335902c42a02ff8d2105dd89969fc506b2793aa299d21dc2f8dc`.
  The immutable authoring baseline and reviewed manifest remain unchanged.
- Independent local verification passed 48 review/admission records, all 156
  merged pack/locale-asset files and all 36 original asset files. The native
  plan derived from the new snapshot is 48 drafts, 48 article publications,
  and zero hub publications. This is not yet a production runtime dry-run.
- A scheduled pip-audit on the merged main revision failed independently of
  content CI. Existing issue #1646 tracks the dependency findings; the deployed
  revision and this release target use identical dependency files. Retain and
  disclose the actual audit result before a deployment decision; do not label
  it a transient test failure or claim all main checks are green.
- The owner then chose: "先修補安全稽核，再備份、部署與發布（建議）".
  Complete the six-package security repair before backup, deployment and this
  48-document release. Track the repair in
  `2026-10-28-resolve-existing-python-dependency-security-audit`; verify actual
  installed patched versions as part of this release's runtime acceptance.
- Candidate native preflight completed against the actual API runtime with an
  unmodified publisher: 48 drafts, 48 article publications, zero hubs. Eight
  executed application SQL statements were SELECT-only, with no DML. Selected
  source-row state and runtime fingerprints were identical before and after.
  Independent remote evidence review passed; no backup, deployment or publication
  was performed. The candidate journal must not be used for production writes.
- Two preparation failures were preserved before any database operation: a
  missing host Git object (resolved by fetch without checkout change), and a
  cap-drop container rejecting chown. A separately reviewed new attempt set
  ownership in its exact host payload, used archive copy into a fresh API stage,
  and verified all copied permissions/hashes as the API user. No container
  capability or publisher guard was changed.
- Exact cohort: ai-term-artificial-intelligence, ai-term-machine-learning,
  ai-term-deep-learning, ai-term-neural-network, ai-term-generative-ai,
  ai-term-transformer, ai-term-attention-mechanism, ai-term-pretraining,
  ai-term-inference, ai-term-model-parameters, ai-term-overfitting,
  ai-term-supervised-fine-tuning.
- Target locales: en, ja, ko, zh-CN. No hub or source correction is authorized by
  this release task. The inference citation redirect has a separate maintenance
  task and is not silently changed here.
- The source authoring baseline SHA is
  `3a496f7b1bc9225b64c3d7e7ac439c314ad816c80285a112722e6c5ff19687c8`;
  release must obtain and reconcile a fresh snapshot rather than treating this
  authoring snapshot as current production state.
- The owner's earlier eight-document release and PR #1906 receipt merge are
  separate completed cohorts. They do not publish these 48 new documents.
- Security repair PR #1887 is now merged as
  `911443f2d0fb102dbe501d265849746af185a787`. Its exact reviewed head had 22 green
  CI checks, a successful enforcing Linux audit and unchanged API test counts
  (8327 passed, 25 skipped). The merged tree equals the checked head; a second
  enforcing audit on merged main also passed (run 40683551386).
- The current approved deployment range adds only the six-package dependency
  repair and its task record to the earlier content/task range: 166 paths total,
  including 12 packs, 144 translated assets, two dependency files and eight task
  files. There are no migrations, application-code, Compose or Dockerfile changes.
- Fresh native host preflight at 11:50:31 UTC remained clear: clean `4c4bf7fde`,
  no deployment hold/active lock/flagged release/running paid video work, 181 GB
  free. A new immutable backup/deploy package is bound to the merged security
  target and the owner's explicit backup/deploy/publish answer. Its final package
  review is pending; no backup, deployment or publication is claimed here.
- The four extra API shard warnings match the existing aiosqlite teardown family.
  Follow-up task `2026-10-28-close-sqlite-test-engines-before-event` preserves that
  test-quality work separately; no warning suppression is part of this release.
