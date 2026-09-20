---
id: 2026-09-20-article-localization-batch-006-three-guides
title: Localize KL and two Singapore guides into five languages (Batch 006 split)
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-20T13:26:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/kuala-lumpur-airport-transfer-plan.json
  - apps/api/app/guides/content/singapore-hawker-first-visit.json
  - apps/api/app/guides/content/singapore-gardens-indoor-outdoor.json
  - apps/web/public/guides/kuala-lumpur-airport-transfer-plan
  - apps/web/public/guides/singapore-hawker-first-visit
  - apps/web/public/guides/singapore-gardens-indoor-outdoor
  - tasks/open/2026-09-20-article-localization-batch-006-three-guides.md
---

# Localize KL and two Singapore guides into five languages (Batch 006 split)

## Why

Three published zh-TW Mokaair guides from the initial Batch 006 inventory still lack en, ja, ko and zh-CN. This task separates Kuala Lumpur and the two Singapore articles from the Hanoi guide, which needs a published source correction before its four drafts can be rebound. Preserve the currently published prose, credits, category, order and visibility.

## Definition of done

- [ ] The three exact packs have complete en, ja, ko and zh-CN documents, with full body, table, caption, alt, source title and text-bearing SVG coverage.
- [ ] Each locale is rebound to the latest published zh-TW version and content hash, with independent editorial and visual approval.
- [ ] Controlled same-site links resolve to the corresponding published locale, and no draft destination becomes a public link.
- [ ] A guarded, rerunnable installation and publication plan limits changes to the twelve missing locales and necessary image references; published outcomes and browser QA are recorded separately.

## Steps

- [x] Capture the initial read-only public/source versions and prepare twelve external, unpublished locale jobs.
- [x] Repair issues from the first independent review in external drafts; preserve the earlier attempt and hash trail.
- [ ] Obtain independent review of the latest external handoff and controlled locale-prefixed link rewriting.
- [ ] Re-snapshot source/version/visibility and compare hashes before import and publication; preserve concurrent editorial edits.
- [ ] Record per-locale schema, content, SVG, link, desktop/mobile and public-versus-draft validation.

## How to verify

Validate each materialized `GuideDocument`, every translated scalar, numeric and eligibility condition, image credits, SVG text, 1600×900 and 390px renders, then run the article import dry-run and affected API/web checks. Run `npm run check:tasks`. For release, verify live five-locale body, image, canonical, hreflang and links, and confirm unpublished material stays private.

## Notes

- Scope is exactly these three pack paths, three asset directories and this task file. Original four-guide task `2026-09-20-article-localization-batch-006` remains owned by `codex-batch006-author` but now claims Hanoi only. This new task is intentionally open and unclaimed for a separate owner.
- Initial public read-only snapshot: `C:/Users/x8120/.codex/article-localization-batch-006/production-baseline-final.json`, SHA-256 `51cad13d52c9a0d275d37943f258975ace1c89ee96b56810c4f083d689b9c322`, 2026-09-20T11:36:16Z. All three active articles had only published zh-TW, no expiry, and matching repository source at that time. Recheck immediately before release.
- `kuala-lumpur-airport-transfer-plan`: article v1, published zh-TW v4, document SHA `45b44f725bd6c1c49fe4e9df48294a904f873d98ef977557652a7da105e79538`.
- `singapore-hawker-first-visit`: article v1, published zh-TW v6, document SHA `ec29aa68e3dab66147b0964e27589889e7e1813b86a18024886eb52c33866a20`.
- `singapore-gardens-indoor-outdoor`: article v1, published zh-TW v6, document SHA `639194c34c9bec35ace1abc56b05f98b3f9eac63fa3589c6c0b8b5dca7d676f0`.
- Hero images are credited Mokaair AI-generated illustrations, explicitly not photographs. Source SVGs carry © Mokaair; preserve attribution and license metadata.
- First independent review: `C:/Users/x8120/.codex/article-localization-batch-006/independent-review.md`, SHA-256 `636e6fe2a49f026d31a8052a922a93d69fb7609c4f1268fe8830d90c9e94380c`. It requested KL English SVG legibility and Japanese last-train wording, Singapore Gardens English apostrophe rendering, and exact zh-CN filename case. Latest unsigned rework: `C:/Users/x8120/.codex/article-localization-batch-006/rework-round3/review-handoff.json`, SHA-256 `e45e34c6e5e372451ddf53050f2cf431fc1ff32160bd54aa5b3d3fa1638df6ff`. Independent re-review and current live source pinning are pending.
- Release hold: KL `/document/blocks/21/url` and Hawker `/document/blocks/23/url` are fixed zh-TW same-site links in the source-derived documents. Intended five-language routes were checked with HTTP 200 and matching `lang`/canonical in `C:/Users/x8120/.codex/article-localization-batch-006/link-route-verification.json`, SHA-256 `84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`. A separate narrow link tool must handle locale-prefixed rewriting and rebind jobs before approval or publication.
