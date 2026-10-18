---
id: 2026-10-07-correct-japan-entry-customs-source-before
title: Correct Japan entry customs source before localization
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T14:12:08Z
created_at: 2026-10-07T08:30:15Z
completed_at: 2026-10-07T17:32:38Z
branch: codex/article-locales-wave4-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/japan-entry-2026-visit-japan-web.json
  - apps/web/public/guides/japan-entry-2026-visit-japan-web
  - docs/article-localization/japan-entry-source-review-20261007.md
---

# Correct Japan entry customs source before localization

## Why

The actual published zh-TW source contains a clickable Machine Learning article
inside the unit760 ml, overgeneralizes medicines to two months, lists all guns
and swords as absolutely prohibited, and omits the form/purity scope of the1kg
gold declaration threshold. These errors must not be reproduced in four new
languages. The10,000yen duty-free exclusion also needs category-aggregate wording.

## Definition of done

- [x] A distinct source writer proposes only the exact verified source changes;
      a genuine independent full-source review approves final document/assets.
- [x] The760 ml unit is plain text, not an article link; other inlines stay exact.
- [x] Medicines distinguish prescription/poisonous/powerful one-month and other
      medicine two-month self-use import-confirmation exemptions, plus applicable
      topical/cosmetic category limits; larger imports are not labelled impossible.
- [x] Prohibited firearms and regulated gun/sword imports are distinguished.
- [x] Gold declaration specifies bullion of at least90% purity exceeding1kg;
      duty-free10,000yen exclusion is aggregated per品目, not per individual object.
- [x] Original database identities/versions, photos, valid_until and unrelated
      source/metadata remain pinned; source correction is independently verified.
- [x] The four missing target languages resume only after genuine source approval;
      publication and public verification remain separate guarded release work.

## Steps

- [x] Claim after verifying actual worktree/remote/PR ownership and fresh source.
- [x] Preserve the original baseline and all failure/source evidence.
- [x] Propose the final exact ten document pointers and two SVG text slots.
- [x] Obtain a distinct independent full-source/candidate/primary-source review.
- [x] Verify source_correction against a fresh baseline and precisely apply/install.
- [x] Explicitly resolve existing repository-only description preservation before
      assembly; do not silently overwrite its accepted answer-first rewrite.

### 2026-10-07 final review and scope update

- Root claimed this task in the separate wave4 worktree at merged main
  `7524c25995d59f3826227e693d52f2ef5b3a19a2`, after current remote and open-PR checks.
- Final external candidate proposal SHA
  `6cbf307efcbc7d0991629cc7868ba7f2dcda49b7246a15887a3a53f74f9d4566`
  has ten exact JSON pointers and two exact source SVG text slots. Earlier claims
  that no SVG change was needed are historical and superseded by this review.
- Distinct independent source-correction review SHA
  `9ec315b0adeb31ea3d2f9ecd1ae236960cdfe54d4144b2f18d011421faa6f4e4`
  binds corrected canonical source
  `4709f8e36b080bc76a1703704db2744b28409fcc31289eebf5c3105c7ca3f3c5`.
- The asset scope now includes the exact article directory so its reviewed SVG
  correction and four native-language variants can be authored. Original photographs,
  SVG geometry, unrelated source text and all other assets must remain pinned.
- The only new checked_on date is the independently approved new official citation
  URL at sources/8. All other historical cutoff/citation dates remain unchanged.
- The previously accepted repository answer-first description is explicitly included
  in the approved ten-leaf source-correction receipt. Separate repository-preservation
  admission is unnecessary for this final candidate; other production guards stay exact.
- After exact source approval, author/review en, ja, ko and zh-CN within this pack;
  bind all image/document hashes, then use a separate guarded release ticket.
- This scope update initially admitted no target translation or publication. The
  later actual local completion is recorded below; first32 release remains separate.

## How to verify

Read the full article, original and final SVG/photos, and primary Customs pages:
https://www.customs.go.jp/tetsuzuki/c-answer/imtsukan/1806_jr.htm
https://www.customs.go.jp/tetsuzuki/c-answer/imtsukan/1809_jr.html
https://www.customs.go.jp/mizugiwa/kinshi.htm
https://www.customs.go.jp/kaigairyoko/shiharaishudan.htm
https://www.customs.go.jp/kaigairyoko/menzei.htm
Use the unchanged official source-correction verifier, pack lint, source/media
preservation checks and exact independent review bindings. No target translation
may hide a different rule from an uncorrected original.

## Notes

The read-only independent source FAIL receipt SHA is
`0f987008c2ed1311f85f3ca285c20418288e4d3aa72be388628c6467474749b6`;
complete evidence SHA is
`f427eb7ca9ab40254860f5a0848c45915a90ff7aa165f813ffcb97aaff31b18c`.
Original published source SHA:
`b61bf8edee8f8ab40529399de2f6ef2c3f2419eeb69fb6958955c6c07793743e`.
Original repository pack SHA:
`ff77ccb926b9a218d2587ade952840e31e96bb439cc1d67a1ddfc0d135a75ab9`.

The original audit's description-preservation and no-SVG-change observations were
superseded by the independently reviewed v4 candidate: ten document leaves include
the answer-first description, and two visible SVG slots plus its paired description
carry the same reviewed customs facts. The original cutoff remains2026-09-13;
photographs and SVG geometry remain exact, with diagram text at least15px. JESTA
implementation remains a dated target, with no invented launch or fee availability.

### Actual local completion

- Official source correction verification and precise source admission exited0.
  Derived baseline SHA: `b743c32e7ef650f43b3688f53bb1ac8d07bea7e005470131a6985307b1477d03`.
- Four genuine final language/image reviews bind the actual current artifacts.
  Original single CLI attempts are preserved; no provider retries were made.
  Root applied reviewer proposals and did not approve its own target edits.
- Official assembly: one article, seven assets and one source correction; manifest
  `fc048145476869d1e7ec5fffba794908d0b58065fcb84b04477a3ea046791a3c`.
- Official install and identical replay exited0; all eight journal operations,
  original photos/metadata and captured installed bytes were verified. Completion
  receipt SHA: `c83c899a2606f17aed486197dd7bc77d5a6d0d1b6d8001ce0bd6eeafcd97ca2a`.
- Separate open release ticket selects four new locales and one source correction.
  Merge, deployment, database publication and five-language public verification
  remain pending owner authorization and guarded release phases.
- Scoped pack lint passed for the one intel entry; translation checks found0 hits.
  Existing English text-length warning is retained. Checks receipt SHA:
  `94c2da0c0d4cd6de97cec4fc32e08725b856bfc35a783c806d25598d1d567756`.
  Local authoring is complete; the content PR's exact-head CI must pass before merge.
