---
id: 2026-10-28-correct-japanese-seasonal-intel-image-descriptions
title: Correct Japanese seasonal intel source claims and image descriptions
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
  - apps/web/public/guides/japan-winter-illumination-2026/diagram-1.svg
---

# Correct Japanese seasonal intel source claims and image descriptions

## Why

Fresh read-only source inspection and actual original-image viewing found three
Traditional Chinese image descriptions that do not match their photographs in
two already-public Japanese seasonal travel articles. Further primary-source
checking confirms that the illumination article's September 13 assertion that
the two Osaka 2026 events were unannounced conflicts with a May 26 official city
announcement. It also affects the prose, table and timeline diagram. Translating
these strings would carry errors into four more languages. Correct the sources
through the existing source-correction process before localizing these articles.

## Definition of done

- [ ] The three confirmed descriptions accurately identify their actual original photographs, with an independent source/image review.
- [ ] Confirmed announcement/date errors are corrected consistently across the illumination body, table, captions and SVG timeline, without turning prior-year times into confirmed 2026 times.
- [ ] Remaining seasonal source claims have a complete dated audit; original false statements are distinguished from information announced after the original check date.
- [ ] All unrelated source values, metadata, credits, licences and image bytes remain unchanged.
- [ ] A source-correction receipt binds current published versions/hashes and the exact before/after pointers; production application follows its own guarded approval/backup/replay process.
- [ ] Subsequent localization uses the corrected published source and a fresh baseline rather than the old source hashes.

## Steps

- [ ] Recheck article visibility, full current source documents and the image bytes against the retained October 28 findings; stop on drift.
- [ ] Independently review the three exact alt corrections and confirmed event-claim corrections, then apply the approved source candidate.
- [ ] Correct the Osaka diagram's announcement legend and date bars, render it again and independently inspect the actual final image.
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
- The original photograph files do not need to change. The illumination SVG
  timeline does need a separately reviewed source correction. Suggestions remain
  candidates until independent review; no source, production row or original
  image was changed during this inspection.
- Both articles also have an existing repository-only description difference.
  Reconcile this explicitly rather than discarding or silently publishing it.
- Independently read primary announcement:
  https://www.city.osaka.lg.jp/hodoshiryo/keizaisenryaku/0000678946.html
  (page and release field show May 26, 2026, 14:00). It announces Midosuji
  November 3 to December 31 and the main Renaissance program December 11 to
  December 25, with some contents extending November 3 to December 31. These
  dates precede the article's stated September 13 check; this is an original
  announcement-status error. Do not claim the separately inaccessible city page
  or linked 404 PDF was successfully checked.
- Confirmed illumination pointers: `/blocks/0/text`, `/blocks/7/text`,
  `/blocks/13/rows/5/1`, `/blocks/13/rows/6/1`, `/blocks/13/caption`,
  `/blocks/14/caption`, `/blocks/14/description`, `/blocks/15/text`.
  The last paragraph's claim that only Midosuji remains after December 25 needs
  qualification for the separately announced partial Renaissance contents.
- Timeline `diagram-1.svg`: 0-based title/desc/text sequence indices 1, 3, 26,
  29 contain the affected descriptions/status. XML preorder elements 50 and 55
  are the Osaka date bars. Recheck their status styling and the Renaissance
  main-period start; the confirmed start is December 11, while the old diagram
  projects December 14. Main dates and partial-content dates must remain distinct.
- `/blocks/13/rows/6/2` needs fresh official detail before writing 2026 times;
  do not promote its prior-year projection. The New Year article's blanket claim
  about December-only event announcements also needs a dated official audit.
- Complete claim-level fact/price/date audit is a continuing read-only step;
  this ticket does not assert that every other claim has passed. Partial reads,
  HTTP 200 challenge pages and JS-only shells are not successful source evidence.
