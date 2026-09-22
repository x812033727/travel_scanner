---
id: 2026-09-20-localize-four-tokyo-first-trip-guides
title: Localize four Tokyo first-trip guides and diagrams
status: review
priority: P1
area: docs
owner: codex-batch007-resume
claimed_at: 2026-09-22T07:16:19Z
created_at: 2026-09-20T12:47:01Z
completed_at:
branch: codex/article-localization-batch007-resume
depends_on: []
scope:
  - apps/api/app/guides/content/narita-haneda-to-tokyo.json
  - apps/api/app/guides/content/tokyo-transit-passes.json
  - apps/api/app/guides/content/tokyo-disney-guide.json
  - apps/api/app/guides/content/tokyo-where-to-stay.json
  - apps/web/public/guides/narita-haneda-to-tokyo
  - apps/web/public/guides/tokyo-transit-passes
  - apps/web/public/guides/tokyo-disney-guide
  - apps/web/public/guides/tokyo-where-to-stay
---

# Localize four Tokyo first-trip guides and diagrams

## Why

The four public Tokyo planning guides have only `zh-TW` published. Their main-tree
packs also contain only `zh-TW`, and each article embeds an editable text SVG. Complete
`en`, `ja`, `ko` and `zh-CN` bodies and diagrams from the current published source,
then hand off for independent review before any import or publication.

## Definition of done

- [x] Four full documents in each of the four missing languages, including title,
  description, every body block, tables, links, captions, alt text and source titles.
- [x] Four-language SVG variants for each diagram, rendered and checked for overflow.
- [x] Source versions and hashes pinned; no existing `zh-TW` prose was replaced. Original
  Narita artwork has reviewed geometry/style corrections with all 25 strings preserved;
  Transit has reviewed layout corrections and one explicit IC-card label correction below.
- [x] Independent editorial and asset review completed before a separate release task uses
  the packs.
- [ ] Final Git-bound canonical wrapper, repository-description preservation receipt and
  all required CI checks pass before the authorized production release.
- [ ] Publish only the 16 missing locales, preserve the four existing zh-TW rows and verify
  all five languages on desktop/mobile, including the two deployed original SVG corrections.

## Steps

- [x] Check active task scopes and claim exact article/asset paths.
- [x] Capture live published source in a read-only repeatable-read transaction.
- [x] Reconcile published documents against main packs and translate all content in provisional drafts.
- [x] Localize SVG text; render and inspect the four language versions provisionally.
- [x] Produce provisional handoff for an independent reviewer.

## How to verify

Run source-hash comparison, pack lint and SVG rendering checks on the external draft.
After independent review, run the guarded import dry-run and normal API/web checks
in the release branch. No import, PR or publication is authorized by this task alone.

## Notes

- Main tree: `5648b84043a09e9db7f773d7a080260d39f9d453`.
- Live source snapshot: `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-live-source.json`,
  captured 2026-09-20T12:44:58Z; SHA-256
  `cadd602ab7da7865dc60295fe8af9cab0861741fec35734b13d3de575fd5ab69`.
- All four articles were `published`, active, `article_version=2`, `zh-TW`
  `published_version=6`, with no expiry and no other published locale.
- Published source differs from the main packs in description and image metadata.
  Use the live published document as translation source; preserve current attribution.
- Source rechecked by another production read-only transaction before revision:
  all four article/source versions and published document hashes were unchanged.
  Recheck capture: `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-live-source-refresh.json`.
- Updated provisional 16-document handoff:
  `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-provisional\review-handoff.json`,
  SHA-256 `787c615ea9e6ccec5b61d1ea8518bd1ad25f676e4ddeeb6d5523b7037c1f2661`.
  It includes 60 translated summary items, 16 separately translated image descriptions,
  complete source/version bindings, corrected document/SVG hashes, and 1600×900 plus
  390px previews for every language.
- The original model attempts, second-pass numeric repairs, two narrow manual
  corrections and SVG pre-layout originals are preserved outside the repo.
  Corrected drafts now have zero strict field, numeric/URL/code token, schema,
  SVG canvas and text-text overlap errors. The original 219 field and 23 canvas
  errors remain visible in provenance rather than being erased.
- This handoff is **not ready for import**: the shared pipeline has not formally
  materialized `summary.items` or `image.description`, and independent editorial
  and visual review remains. At 390px the whole 1600px diagram is scaled down;
  small lettering needs explicit mobile-readability review.
- Formal materialization awaits shared-pipeline support for `summary.items` and
  `image.description`, followed by independent text/image review.
- No active task scope overlapped the eight explicit pack and asset paths when claimed.

## Published-source correction checkpoint (2026-09-20)

- Source-only PR [#603](https://github.com/x812033727/travel_scanner/pull/603)
  is open for review; the full five-language task is still unfinished.
- The independent review at
  `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-provisional\independent-review-HOLD.md`
  identified seven zh-TW source issues; its SHA-256 is
  `912f4038b3d0bc98ac0aeb6257813d0d730fe79ceadc4b953bbbe26d26aae48f`.
- A narrow source-correction PR changes only the existing Narita, Disney and transit
  zh-TW packs and the transit zh-TW decision-tree SVG. Tokyo stay is unchanged.
  The new facts are sourced to Tokyo Metro, JR Group, JR East and Tokyo Disney
  official pages checked on 2026-09-20; existing source links and check dates
  remain intact. The Narita pack already has the schema maximum of 20 source
  entries; the JR East eligibility page is cited in the PR review description
  rather than replacing or deleting an existing source.
- The 16 provisional translation documents and language SVGs remain outside the
  repository and **on hold**. Re-read the published source after any eventual
  source release, rebind versions/hashes, fix their locale text and images,
  rerender at desktop and mobile widths, then obtain an independent re-review
  before importing or publishing them.
- A 1600×900 render of the existing zh-TW transit decision tree also shows
  pre-existing IC-card banner text extending beyond its rounded box. The price
  card corrected in this PR fits; the broader diagram layout needs separate
  visual cleanup during Batch007 image review.

## 給這張票的擁有者（claude-opus-5 留，2026-09-22）

`apps/web/public/guides/narita-haneda-to-tokyo/diagram-1.svg` **有三個文字元素被畫到畫布外**，
`viewBox` 是 `0 0 1600 900`，超出就會被裁掉，所以那些字在任何螢幕上都看不到：

| 右緣 | 內容 |
|---|---|
| 1696 | `N'EX 最快 53 分 · TYO-NRT 巴士 最快 65 分` |
| 1631 | `浜松町 Hamamatsucho` |
| 1630 | `單軌電車 最快 13 分 · 轉 JR 山手線` |

被裁掉的是班次與車程，讀者真正要的資訊。用瀏覽器實測（`getBBox()`）確認，不是估算。

我本來要一起修，但這個檔在你的 scope 裡，所以沒有動。
同類缺陷的完整清單與修法在票 `2026-09-22-diagram-text-clipped-offcanvas`；
我已經用同樣手法修好 `incheon-airport-to-seoul` 與 `tokyo-5-day-itinerary`：
**在分隔號處拆成兩行**，或把標籤改成 `text-anchor="end"` 並把 `x` 釘在 1580，
兩種都不用縮字級（15px 是下限，縮下去手機上又讀不到）。

驗證方式：在瀏覽器開那個 SVG，跑
`[...document.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x+b.width>1600.5})`
，要是空陣列。

### 2026-09-22 resumed after source release

Normal claim as `codex-batch007-resume` succeeded without --force after closing
our completed batch009 and handing back the stale AIO edit task as a task-only
blocked publication follow-up. All original provisional drafts remain on hold.
Fresh read-only source receipt at 2026-09-22T06:35:52Z confirms all seven prior
source findings are fixed live; Narita/Disney/transit are published zh-TW v8 and
stay is v6. Source-readiness receipt SHA256
`be24da5c0685cb96c55921b983674bbf24d5062df95b522bffd9bcd905d4f433`
under `C:/Users/x8120/.codex/article-localization-release/batch007-resumption-20260922`.
Remaining: 100 source-driven translated leaf updates, 32 same-locale site-link
rewrites, four transit price cards, and all 16 diagram visual repairs/reviews.
Stay's sole unpublished repository /description edit must be preserved through
the reviewed preservation path; no prior HOLD is promoted to PASS by this note.

### 2026-09-22 initial reviewed integration

- Integrated the 16 complete `en`, `ja`, `ko` and `zh-CN` documents into the four
  existing packs. Each frozen document differs only at its independently reviewed
  diagram `height` pointer; all other prose, numbers, URLs, credits, source dates and
  document structure remain byte/model-bound to the reviewed draft.
- Preserved every existing repository `zh-TW` GuideDocument and article metadata,
  including the repository-only Tokyo stay description. No live source was copied
  over that repository edit.
- Added the 16 independently reviewed localized SVGs. At this checkpoint the existing
  original asset changed was
  `apps/web/public/guides/narita-haneda-to-tokyo/diagram-1.svg`: nine reviewed
  geometry/style substitutions connect N'EX through Shinagawa, separate the Tokyo
  and Shinjuku Airport Limousine branches, and move inherited off-canvas labels back
  into the 1600x900 viewBox. Its title, description, all 25 decoded visible strings,
  dimensions and source document remain unchanged.
- Text review receipts:
  `revised-text/root-narita-disney-text-delta-review.json` SHA-256
  `043ab361ab2940127c5ebeeb57a682a3416fbaac7697dde445879635e86e1aca` and
  `revised-text/independent-review-transit-stay-pass.json` SHA-256
  `4e00cbaf21890667a20a300578979c146e40379ca25f80efec8ace052472e640`.
- Initial asset/render receipt (Transit superseded by the final review below):
  `revised-assets/independent-final-review/receipt.json` SHA-256
  `54003aa4aaaaaf49a5e08e5da878aefc4ca1465370383a6f16af0640903c2357`.
  It binds 17 SVGs, 68 independently viewed PNG renders and all 16 height pointers.
- Structural integration audit:
  `integration/integration-audit.json` SHA-256
  `3ed336cbbcea3fb9500b98efaaf9cdf7316035cd251545c639bdad8c2530dd1e`.

Still incomplete for the separate release sequence:

- [ ] Independent review of the committed Git bytes and preservation freeze.
- [ ] Pull request CI and merge.
- [ ] Import/publish and production desktop/mobile browser QA.

### 2026-09-22 final Transit review and scoped validation

The original Transit SVG had inherited 13/14px labels and an overflowing IC-card
banner. Its reviewed layout now fits all text inside the original 1600x900 canvas
at a minimum 15px. One visible label in all five languages changed from the
generic `180–330` subway-fare range to the source paragraph's advice to tap the IC
card for each ride. Tokyo Metro's official regular-ticket page distinguishes
paper fares from IC fares, so that range was inappropriate in the IC-card branch;
the published prose never contained the range. The diagram correction neither
changes the zh-TW GuideDocument nor rewrites its source-check dates.

Root review also restored two source graph edges in each of the four translated
diagrams: the starting banner to question 1, and the skip-JR-Pass result to
question 2. All ten decision branches, the Tokyo-day return cue, all other text
and existing geometry were checked. Earlier candidates and HOLD evidence remain
outside Git. The final review binds all five assets and twenty desktop/mobile
pan renders, and independently reruns the numeric guard over all eighteen final
diagrams without exceptions.

Evidence under `C:/Users/x8120/.codex/article-localization-release/batch007-resumption-20260922/`:

- `revised-assets/transit-final-v4/root-independent-review-pass.json`, SHA-256
  `908332306b40007b3c0ac94a53df47a36979258d26d6884f8229cfe5f06f3d43`.
- `integration/root-final-transit-integration.json`, SHA-256
  `085a65300e695eee8a704c2ef30d2e3493decb0655e3089b73c24e4f15f5bf65`.
- `live-source-full-20260922T090401Z.json`, SHA-256
  `fd5b140d099030ce3f17479e7ae72683b90aacab939b4aac670115a678896a54`.
  All four published source versions and document hashes remain unchanged, with
  draft, latest revision and published document identical for each zh-TW locale.

Scoped lint passes using the independently reviewed diagram-dimension change in
PR #658 (`6d7a932482f62ce607a82b86d183436a40012948`). Only the four complete English
translations' advisory length warnings remain. The four repository zh-TW documents
and article metadata are unchanged. Tokyo stay's sole live/repository difference
remains `/description` and needs the final Git-bound preservation review.

The final release must deploy and separately hash-check the original Narita and
Transit SVGs; they are referenced by the unchanged zh-TW documents and are not
selected locale-import operations. Complete canonical release and public browser
acceptance remain outstanding.
