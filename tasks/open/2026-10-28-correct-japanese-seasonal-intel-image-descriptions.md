---
id: 2026-10-28-correct-japanese-seasonal-intel-image-descriptions
title: Correct Japanese seasonal intel image descriptions
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-28T08:20:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-winter-illumination-2026.json
  - apps/api/app/guides/content/japan-year-end-new-year-2026-2027.json
---

# Correct Japanese seasonal intel image descriptions

## Why

Fresh read-only source inspection and actual original-image viewing found three
Traditional Chinese image descriptions that do not match their photographs in
two already-public Japanese seasonal travel articles. Translating these strings
would carry the errors into four more languages. Correct the source through the
existing source-correction process before localizing these two articles.

## Definition of done

- [ ] The three confirmed descriptions accurately identify their actual original photographs, with an independent source/image review.
- [ ] All unrelated source values, metadata, credits, licences and image bytes remain unchanged.
- [ ] A source-correction receipt binds current published versions/hashes and the exact before/after pointers; production application follows its own guarded approval/backup/replay process.
- [ ] Subsequent localization uses the corrected published source and a fresh baseline rather than the old source hashes.

## Steps

- [ ] Recheck article visibility, full current source documents and the image bytes against the retained October 28 findings; stop on drift.
- [ ] Independently review and apply the three exact alt-only corrections in the repository.
- [ ] Reconcile the existing repository-only description differences without silently discarding or publishing them.
- [ ] Build and review native source-correction evidence, run content checks and open the source-fix PR.
- [ ] Prepare a guarded production correction release with fresh dry-run/backup/owner authorization; verify public readback and then unblock the affected localization scope.

## How to verify

Use the article-localization source-correction workflow. The retained private
finding report includes complete source documents, published versions, exact
pointers/current/proposed strings, original-image hashes and actual viewing
times. Verify image pixels and all unchanged values independently; passing a
schema validator cannot establish whether an alt description matches a photo.

## Notes

- Finding report SHA256:
  `d229f7fe3f528865343b9035b5216670dcc12a892eaeb079d90666ec1445efa1`.
  Raw API/image evidence remains outside Git in the owner's persistent workspace.
- `japan-winter-illumination-2026`, published zh-TW v4, `/blocks/10/alt`:
  the source claims illuminated arches and visitors walking underneath. The
  actual photograph shows the unlit daytime Kobe light installation behind
  barriers, without those visitors. Proposed: 「神戶光雕白天的拱門裝置，尚未點燈，前方設有圍欄」.
- `japan-year-end-new-year-2026-2027`, published zh-TW v6, `/hero/alt`:
  the source claims Nakamise Street and distant Hozomon. The photograph instead
  shows a crowd at the Sensoji fortune counter. Proposed:
  「淺草寺籤所前聚集的人群，屋簷下掛著『みくじ 百円』招牌」.
- The same New Year article, `/blocks/8/alt`: the source claims a shop display
  with amounts on bags; the photograph shows pedestrians carrying lucky bags.
  Proposed: 「行人提著印有『福袋』字樣的購物袋走在人行道上」.
- These are source-image findings, not authorization to change source image
  files. The suggestions remain candidates until independent review; no source,
  production row or original photograph was changed during this inspection.
- Both articles also have an existing repository-only description difference.
  Source fact/price/date audit is a separate continuing read-only step; this
  ticket does not assert that every other source claim has passed.
