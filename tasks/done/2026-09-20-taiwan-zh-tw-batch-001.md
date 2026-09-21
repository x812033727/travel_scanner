---
id: 2026-09-20-taiwan-zh-tw-batch-001
title: Taiwan zh-TW first sub-batch: Jiufen and Taipei night markets
status: done
priority: P2
area: api
owner: codex-taiwan-zh-tw
claimed_at: 2026-09-20T17:10:33Z
created_at: 2026-09-20T17:10:11Z
completed_at: 2026-09-21T14:15:56Z
branch: codex/taiwan-zh-tw-batch-001
depends_on: []
scope:
  - apps/api/app/guides/content/jiufen-shifen-yehliu-day-trip.json
  - apps/api/app/guides/content/taipei-night-markets-guide.json
  - apps/web/public/guides/jiufen-shifen-yehliu-day-trip/diagram-1-zh-tw.svg
  - apps/web/public/guides/jiufen-shifen-yehliu-day-trip/diagram-1.svg
  - apps/web/public/guides/taipei-night-markets-guide/diagram-1-zh-tw.svg
---

# Taiwan zh-TW first sub-batch: Jiufen and Taipei night markets

## Why

Two currently published Taiwan travel articles have four published locales but no
zh-TW document. Their source diagrams mix traditional Chinese and English text.
This first bounded batch adds full zh-TW documents and zh-TW-only diagrams while
retaining the existing article IDs, published locales, metadata and image credits.
It also corrects source-backed Jiufen pack facts found during review. The guarded
release uses an explicit seven-operation list for the two missing zh-TW documents
and five reviewed corrections to existing published locales.

## Definition of done

- [x] Both zh-TW GuideDocuments cover every source field and validate against the API schema.
- [x] Both text-bearing SVGs are localized, rendered and visually reviewed at desktop and 390px.
- [x] Independent editorial review verifies numbers, eligibility, source titles, links and credits.
- [x] The two missing zh-TW locales and five reviewed existing-locale corrections are published from an explicit, version-guarded seven-operation plan after dry run and release QA.

## Steps

- [x] Pin fresh read-only live article/source versions, document hashes and artwork/credit inventory.
- [x] Author and independently review Jiufen zh-TW document and both corrected SVGs.
- [x] Author and independently review Taipei night markets zh-TW document and SVG.
- [x] Prepare and approve a hash-bound review handoff; do not publish before guarded release checks.

## How to verify

Run `npm run check:tasks`, focused GuideDocument/ArticlePack validation,
translation field coverage/numeric/link audits, SVG render/overflow review,
then the repository checks and version-pinned import dry run before release.

## Notes

- Worktree `codex/taiwan-zh-tw-batch-001` began at main `f34bb245691e7f32f97d1c9373394e87650591af` after #606 released these pack paths.
- Live snapshot captured 2026-09-20T16:35:47Z: `C:\Users\x8120\.codex\article-localization-taiwan-zh-tw\live-taiwan-14.json` SHA-256 `827fa4701f09bd7232bb88231813743d2821c4d35d7d0c70d41e5e9c7d4d1ffd`. Both article versions are 2. Jiufen zh-CN published v6 document SHA `5676530b028d613b5792b5fb4b0a48ca58e0cd9c7334ed3ff0652a650e146412`; night markets zh-CN published v4 SHA `d59e523a886cb7e693268e82e19269cfa952f8204a55f5d482b88c952694e7aa`. The repository packs are not necessarily the live description revision; derive translation from the pinned live published documents and import only new zh-TW.
- **Source correction still open:** Jiufen live zh-CN `/blocks/30/text` says mainland individual/group tourism is applied for online at NIA, without stating who submits. The official NIA individual-tourism procedure says an approved Taiwan travel agency files online on the applicant's behalf (https://www.immigration.gov.tw/5385/7244/7250/7257/7266/36078/, lines 123–126, last updated 2022-05-17). The new zh-TW states this procedural role without claiming that tourism applications are currently accepted. Correct the published zh-CN source in a separate narrowly scoped task; this batch's existing-locale patches cover only the reviewed fare, eligibility, hours and night-market grammar corrections.
- `GuideDocument` image paths only allow lowercase basenames; the locale's article key stays `zh-TW`, but the two new SVG filenames are `diagram-1-zh-tw.svg`. The initial uppercase filenames were caught and corrected before schema validation/review.
- Fresh read-only production recheck at 2026-09-20T17:34:43Z in external `batch001/fresh-live-two.json` reconfirmed both article versions 2, Jiufen zh-CN published v6 SHA `5676530b028d613b5792b5fb4b0a48ca58e0cd9c7334ed3ff0652a650e146412`, night markets zh-CN published v4 SHA `d59e523a886cb7e693268e82e19269cfa952f8204a55f5d482b88c952694e7aa`, and zh-TW absent. The external snapshot SHA is `6bf0c1c2e81c3dbfd2be1ab2caac012465f24bde2f52dc9e9c94d8a80bc13035`.
- Authoring audit covers all Jiufen 107 source text fields plus the NIA and 2026 Shifen announcement titles (109 target fields), and all night markets 148/148 source/target fields, with no copied long prose and all 33/36 source block types and positions preserved. The existing `en`, `ja`, `ko`, `zh-CN` Jiufen documents only change at the reviewed Yehliu eligibility fields, 1815/1062 endpoint fares, the 2026 Shifen hours fields, and their source records; the existing night-market zh-CN document has one grammar correction matching the new zh-TW wording. The guarded release patches only those explicit existing-locale fields. Article metadata and photo credits are unchanged. Numeric audit differences are accounted for by the explicit fare and 2026 Shifen date/last-entry corrections, eligibility details, diagram alt/description, and translated source titles.
- Official recheck on 2026-09-21: Yehliu's ticket page limits the NT$60 concession to students with Taiwan formal-enrollment ID or ISIC, children 6–11, and visitors 65+ of any nationality; New Taipei City Tourism Bureau's 2026 announcement sets Shifen Waterfall's extended hours to May 1–September 30, 09:00–18:00, last entry 17:30. The Highway Bureau fare tables list Taipei Main Station East Gate 3 to Yehliu on route 1815 as NT$99 (NT$104 is the next stop, Guoshengpu), and MRT Zhongxiao Fuxing to Jiufen Old Street on route 1062 as NT$94 (NT$105 is the terminal, Quanjitang). Those qualifications, dates and endpoint-specific fares now appear in all five repository locales and the new zh-TW route graphic.
- Both new 1600×900 zh-TW SVGs and the corrected shared Jiufen SVG rendered at native size and 390px. The receipt records actual desktop screenshots as 1600×900 and mobile screenshots as 390×219.375, separately from each SVG's 1600×900 natural size. Browser SVG geometry reports 35/35/42 visible text nodes, zero canvas overflow and zero text/text overlap; independent manual review of all six renders saw no clipping. At 390px the full route diagram text is small; the ImageBlock descriptions retain all route/station/time details as readable page text. Public mobile page QA remains required after publication.
- Read-only link checks: `/zh-TW/foods?city=taipei` and `/zh-TW/destinations/taipei` returned HTTP 200. The referenced `/zh-TW/guides/howto/taipei-metro-easycard-guide` returned the localized “這篇文章目前看不到” page; its `ArticleInline` must remain non-clickable until that locale is actually published.
- Focused API content pack/link tests passed (12 passed, 5 skipped); direct `ArticlePack` validation confirmed five locales with 33/36 blocks and 18/20 sources; both focused pack lint runs passed with existing warnings only; `npm run test:tools` passed (75 passed, 1 skipped); `npm run check:tasks` validated 648 files with unrelated pre-existing warnings; `git diff --check` passed. Independent re-review approved the five content/image files with no remaining blocker after the corrected shared SVG was added.
- PR #619 merged to main as `808538aeae2e92c4cd85eafc60ef5da0cfe6cf87`. Exact-main push CI run `35605788579` completed successfully with API, web, containers and full-stack-smoke jobs all green.
- The guarded release advanced production from `7adddf8582b6abd7bdbd87e53569a8de70d2d098` to `808538aeae2e92c4cd85eafc60ef5da0cfe6cf87`. The predeploy backup is a verified `pg_dump -Fc` (`6b7ec0e393b20491c9a3cfb12ce3623422cae1536fcdb29fde4f484805203c25`); the separate prepublication backup is also index-verified (`48d82ff2b112c7370d57cf50f107227519db47edd3f108d0f5748d9c3f89ba44`). Post-release readiness reports database and Redis `ok` at schema `0082_travel_food_subtopics`.
- Publication used plan `33725f6584dbb1dea872829cbcc61f9c5ee7b4cd34578314ba9b5b3c82975e9f` and resealed package manifest `a6f28700b655c63990e1aa2cdf87284fd4634090a93a27455f08c92d9e6530f9`. The guarded phase receipts show dry run `old` with zero writes, drafts `drafted` with seven writes, publish `complete` with seven writes, and verify `complete` with zero writes.
- Two fail-closed tooling defects were found during release. The first one-off mount changed the release path and was refused before the dry run; the second expired the verified actor ORM object and rolled back before the first draft commit. Both fixes were independently reviewed, regression-tested, hash-pinned and resealed. A repeated guarded dry run after the failed draft attempt proved all seven database states were still `old` before publication resumed.
- The prepublication browser stage proved both real zh-TW routes remained unavailable and absent from the public sitemap while all seven database states were exact drafts. Final browser QA passed all 20 page checks (two slugs, five locales, desktop and 390px mobile), including exact prose, fares, eligibility, Shifen hours, zh-CN queue wording, canonical, reciprocal hreflang, same-locale links, exact SVG hashes and page overflow. Sitemap traversal checked 12 XML documents and 2,361 locations. The release recorded 22 passing checks and 28 hash-bound evidence files, then cleared `/root/travel-scanner-deploy.hold` at `2026-09-21T14:14:04Z`.
