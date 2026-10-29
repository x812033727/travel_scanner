---
id: 2026-10-28-release-localized-two-ai-concept-life
title: Release localized two AI concept life guides
status: done
priority: P1
area: docs
owner: codex-gpt6-article-locales-20261029
claimed_at: 2026-10-29T00:44:07Z
created_at: 2026-10-28T13:52:03Z
completed_at: 2026-10-29T01:31:48Z
branch: codex/article-locales-completion-20261029
depends_on:
  - 2026-10-28-localize-two-ai-concept-life-guides
scope:
  - docs/article-localization/releases/2026-10-28-ai-concepts
---

# Release localized two AI concept life guides

## Why

The dependent content task adds eight reviewed en/ja/ko/zh-CN translations for
the public foundation-model and tokenization life articles. It also corrects
tokenization's two inaccurate source alt strings and matching SVG descriptions
through an independently approved native source-correction receipt. Repository
installation and green CI do not publish these documents. This task owns the
guarded release using the deployed runtime, source correction and translation publication.

## Definition of done

- [x] The exact reviewed content commit is merged after applicable checks pass, with the full pending deploy range and migration scope inspected.
- [x] Fresh production source/draft/published/target guards match the admitted bundle; concrete owner authorization and a verified fresh full backup precede writes.
- [x] Actual deployed-image isolated rehearsal, native publisher phases, durable journal readback and idempotent replay pass for exactly the authorized locales/source correction.
- [x] All ten public documents (two articles times five locales), public assets, link resolution, sitemap/canonical/hreflang and actual desktop/mobile views pass independent acceptance.
- [x] Sanitized release evidence is recorded, only the release driver's own hold is cleared and final host verification passes.

## Steps

- [x] Verify merged content and exact final source-correction/job/artifact reviews; preserve the original source bindings and failed attempts.
- [x] Take fresh source/version/visibility/target snapshots, validate source-correction old/new hashes, and dry-run the exact native plan.
- [x] Obtain approval for the exact publication scope, verify backup restore and rehearse under the owned hold using the already deployed runtime.
- [x] Execute the native phases with one durable state directory, rebuild/check links and replay without further writes.
- [x] Complete paced public capture with settled navigation/geometry, independent visual review and native progress accounting.
- [x] Write README.md/evidence.json, close this task and clear only its own hold after final acceptance.

## How to verify

Follow the article-localization/deploy skills, source_correction.verify_review,
the native publisher's source-drift guards and ops/release/README.md. The exact
publication count must come from the final manifest and fresh runtime dry-run;
it includes the approved source correction as well as new target documents.
The native progress report is historical journal accounting, not a live query.
Retain actual database, backup/restore, browser/network and screenshot receipts
outside Git; release docs contain only sanitized hashes/counts/public paths.

## Notes

### Final outcome — 2026-10-29

Released and accepted at 2026-10-29T01:29:26.944801+00:00. The fresh full backup
contains 573,479,205 bytes and passed an actual isolated restore. Native phases
completed nine drafts and nine publications (eight translations and one source
correction), zero hubs, with exact 18-revision/18-audit history. Rehearsal and
replay preserved the expected 167 table rowsets. Foundation-model zh-TW remains
v10, tokenization zh-TW is corrected v12, and all eight new locales are v2.

Public checks passed for ten documents and 28 media files. Two independent
reviewers viewed all 20 original desktop/mobile PNGs; their static-image limits
are retained. All 113 HTTP requests returned 200, minimum spacing 1300 ms. All
28 new unavailable references are confirmed as retained plain text. Native
progress accounting completed seven stages for all eight translations, zero
errors. The existing finalizer cleared only its own hold; the standard host
verifier reported 11 PASS, 0 FAIL. Backup and restored sandbox are retained.

Sanitized evidence: `docs/article-localization/releases/2026-10-28-ai-concepts/`.
Final receipt SHA256:
`f0b47ec36428cd91315f00eaaffc4d617637fd3ad004124cb968217080253113`.
Actual QA SHA256:
`38f17a5afe6c7a177389a54a656eb01e582ed11bd02d6744ba19beddf28d9121`.
The fresh post-acceptance census still has 3,088 missing documents; the global
localization program stays open. This release did not invoke deployment or
publish any next-cohort source corrections.

### Historical approval and pre-release checkpoints

The following notes retain the states observed before completion. Their pending
or unpublished statements describe those checkpoints, not the final outcome above.

- On 2026-10-29 the owner explicitly chose: "先備份、驗證還原，再發布並驗收這批（建議）".
  This authorizes a fresh full backup, actual restore, isolated rehearsal and
  publication/acceptance of the exact eight translations plus tokenization's
  two zh-TW alternative-text changes. It does not authorize other cohorts.
  Another deployment brought the checkout and API/web runtime to the already
  reviewed `7e380b739645d942cf225c8c70ddb7290d253641`; this release uses that
  deployed runtime and does not invoke another deployment. Fresh runtime
  identities were read back at 2026-10-29T00:44:48Z, both services running with
  zero restarts. The previous candidate stage remains preserved and will not
  be reused as a production journal. Preparation now uses a separate bounded
  publication-only driver and a new actual backup/rehearsal/journal chain.
- Readiness work resumed on 2026-10-29 Asia/Taipei. PR #1914 was merged with
  explicit owner authorization at `7e380b739645d942cf225c8c70ddb7290d253641`;
  its entire tree matches the approved head and all 22 PR checks passed.
  The owner explicitly reserved deployment and publication for separate
  confirmation. The later "continue" request is being used to prepare the
  concrete release scope and read-only candidate preflight, not to invent
  that production authorization.
- Fresh host preflight at 2026-10-28T16:24:20Z found a clean deployed checkout
  `911443f2d0fb102dbe501d265849746af185a787`, no deployment hold or flagged
  staged release, a free deploy lock, no installed auto-deploy timer and no
  running paid video stage. The full pending range contains only #1913 and
  #1914: content/assets plus documentation/tasks, without migrations, runtime
  code, dependency, configuration, Dockerfile or Compose changes.
- Fresh read-only repeatable-read snapshot at 2026-10-28T16:25:06Z found both
  articles active and public, article version 2, clean zh-TW draft/published
  version 10 and all eight target locale rows absent. Source hashes still
  match the original reviewed production bindings. Do not replace those pins
  with corrected repository content or call this a completed release.
- Ownership audit found no release-scope conflict across 43 open PRs, 248
  remote heads, 527 local branches and 73 worktrees. Its private receipt SHA256
  is `298b17b60b7973f1317c313730cfa07465d2f10a8f789294e1371505093614e1`.
  The two pre-existing uncommitted future source-task notes and unrelated
  local environment directory remain preserved and outside this release.
- The merged target's same 22 core CI checks also passed. Auxiliary branch-update
  and announcement jobs are tracked separately from those 22 checks; the latter
  announcement was skipped. Independent core-CI review SHA256:
  `425cf42fab37deddc53fd39f561823af2e74afa1a82d0943dda2823352ba282c`.
- Candidate predeployment dry-run passed using the unchanged native publisher
  in the actual current API runtime with staged target Git bytes: exactly nine
  draft operations (eight `start_translation`, one tokenization zh-TW
  `save_draft`), nine publications and zero hubs. Foundation zh-TW is excluded
  from writes. This is not deployment, backup, new-image isolated rehearsal or
  publication. Its private candidate journal must never be reused for publication.
- Attempt 1 stopped before extraction or database access because a new check
  assumed OCI commit labels; both accepted runtime images actually have null
  revision labels. Its archive, stage and error remain preserved. Attempt 2
  instead pins the exact API/web identities against accepted prior deployment
  and fresh readback, and additionally verifies selected runtime pack bytes
  against the live Git commit. Four locks, no-DML SQL guard, actual publication
  holds and all before/after checks remain intact. Independent executable
  review SHA256: `64fc4e6b5fa791e6035130f4f7d152d8c41c7ee9d9ecb860b1dddf3824bcdb7a`.
- Successful candidate archive SHA256:
  `2b5cb2abc870b299b19840ee75104c6ebdcac0da6587ea9a6ab83f21e8126117`.
  Native journal SHA256:
  `901346b7be2bbd7583022ad2e6891231e337991cd67ccca5149d4b0ea34399e8`.
  Selected before/after snapshot bytes are equal at SHA256
  `f57585c55434b8df2570c4eb099c1badaa65b08c93da3890971222fac024f634`;
  actual runtime identities, API modules/packs and publication holds are unchanged.
  No production content write, backup, deployment or publication has occurred
  for this cohort. All failed and successful preflight evidence stays private.
- Independent actual-host evidence review passed: all ten command records exit
  zero, eight SELECT statements complete with zero rejections, all native done
  lists empty and pending intent null. Sealed candidate receipt SHA256:
  `a426bd099825afa373b683d37d71341202dbd51e053e4196920be9e1f0e9b7c2`.
  Independent final review SHA256:
  `8482f3010c0ff38450b154c3f6d4267c41bd3841a6a8a2bc06b438cbd8c3634c`.
  The prepared approval package and readable scope are saved privately under
  `next-wave-20261028/release8-readiness-root`. Waiting for the owner's separate
  backup/deployment/publication decision; release the task while waiting.
- Selected slugs: ai-term-foundation-model, ai-term-tokenization. Eight new
  translations are the intended scope; tokenization zh-TW also has two alt
  corrections. Its SVG desc metadata changes preserve all original visible
  pixels/text/geometry and the JPEG. Foundation-model's source stays unchanged.
- The old tokenization source is clean public v10. Native independent correction
  review SHA256:
  `9653389d926c83b7015bff4827c6084ef95f3c147fc4a177e4b22f8905dad980`.
  Corrected source canonical SHA256:
  `e7f4742aaacaba918503108e6b07cfbfd1dc24536f3a3dca6f2f7eeb7fc20364`.
- Source correction authoring baseline retains original database pins; never
  replace them with corrected content pretending it was already public. The
  editable hero SVG companion has separately bound old/new hashes and pixel
  proof; public diagram SVG and unchanged source JPEG are in the native review.
- This is separate from the completed 48-translation release recorded in
  PR #1913, and from the earlier two business-analysis articles. None of their
  backup, deployment, publication approval or finalization receipts authorize
  this new cohort. No production write for these articles is claimed here.
- Final authoring manifest SHA256:
  `26e5a4626ea069118ea232383e15c20d149ff09246ce1ce7839caf4d45eeeffe`.
  It selects four locales for foundation-model and five for tokenization:
  eight new translations plus the reviewed tokenization zh-TW correction.
  The bundle has two packs and twenty-six assets (twenty-four new localized
  assets, the corrected original diagram and the unchanged source JPEG).
- Corrected authoring baseline SHA256:
  `2a77df5832dbbd833495faeb101073e434865736051d60fc15876b80bd5835df`.
  Native local install and replay passed. Candidate predeployment dry-run now
  passes as recorded above; actual-runtime postdeployment dry-run, fresh verified
  backup, deployment, publication journal and public acceptance remain pending.
