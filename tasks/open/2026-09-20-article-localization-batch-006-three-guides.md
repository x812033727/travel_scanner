---
id: 2026-09-20-article-localization-batch-006-three-guides
title: Localize KL and two Singapore guides into five languages (Batch 006 split)
status: in-progress
priority: P2
area: api
owner: codex-batch006-three
claimed_at: 2026-09-20T13:34:51Z
created_at: 2026-09-20T13:26:59Z
completed_at:
branch: codex/article-localization-batch-006-three-guides
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

- [x] The three exact packs have complete en, ja, ko and zh-CN documents, with full body, table, caption, alt, source title and text-bearing SVG coverage.
- [x] Each locale is rebound to the latest published zh-TW version and content hash, with independent editorial and visual approval.
- [x] Controlled same-site links resolve to the corresponding published locale, and no draft destination becomes a public link.
- [ ] A guarded, rerunnable installation and publication plan limits changes to the twelve missing locales and necessary image references; published outcomes and browser QA are recorded separately.

## Steps

- [x] Capture the initial read-only public/source versions and prepare twelve external, unpublished locale jobs.
- [x] Repair issues from the first independent review in external drafts; preserve the earlier attempt and hash trail.
- [x] Obtain independent review of the latest external handoff and controlled locale-prefixed link rewriting.
- [ ] Re-snapshot source/version/visibility and compare hashes before import and publication; preserve concurrent editorial edits.
- [ ] Record per-locale schema, content, SVG, link, desktop/mobile and public-versus-draft validation.

## How to verify

Validate each materialized `GuideDocument`, every translated scalar, numeric and eligibility condition, image credits, SVG text, 1600×900 and 390px renders, then run the article import dry-run and affected API/web checks. Run `npm run check:tasks`. For release, verify live five-locale body, image, canonical, hreflang and links, and confirm unpublished material stays private.

## Notes

- Scope is exactly these three pack paths, three asset directories and this task file. Original four-guide task `2026-09-20-article-localization-batch-006` remains owned by `codex-batch006-author` but now claims Hanoi only. This task is claimed by `codex-batch006-three`.
- Initial public read-only snapshot: `C:/Users/x8120/.codex/article-localization-batch-006/production-baseline-final.json`, SHA-256 `51cad13d52c9a0d275d37943f258975ace1c89ee96b56810c4f083d689b9c322`, 2026-09-20T11:36:16Z. All three active articles had only published zh-TW, no expiry, and matching repository source at that time. Recheck immediately before release.
- `kuala-lumpur-airport-transfer-plan`: article v1, published zh-TW v4, document SHA `45b44f725bd6c1c49fe4e9df48294a904f873d98ef977557652a7da105e79538`.
- `singapore-hawker-first-visit`: article v1, published zh-TW v6, document SHA `ec29aa68e3dab66147b0964e27589889e7e1813b86a18024886eb52c33866a20`.
- `singapore-gardens-indoor-outdoor`: article v1, published zh-TW v6, document SHA `639194c34c9bec35ace1abc56b05f98b3f9eac63fa3589c6c0b8b5dca7d676f0`.
- Hero images are credited Mokaair AI-generated illustrations, explicitly not photographs. Source SVGs carry © Mokaair; preserve attribution and license metadata.
- First independent review: `C:/Users/x8120/.codex/article-localization-batch-006/independent-review.md`, SHA-256 `636e6fe2a49f026d31a8052a922a93d69fb7609c4f1268fe8830d90c9e94380c`. It requested KL English SVG legibility and Japanese last-train wording, Singapore Gardens English apostrophe rendering, and exact zh-CN filename case. Latest unsigned rework: `C:/Users/x8120/.codex/article-localization-batch-006/rework-round3/review-handoff.json`, SHA-256 `e45e34c6e5e372451ddf53050f2cf431fc1ff32160bd54aa5b3d3fa1638df6ff`. Independent re-review and current live source pinning are pending.
- Release hold: KL `/document/blocks/21/url` and Hawker `/document/blocks/23/url` are fixed zh-TW same-site links in the source-derived documents. Intended five-language routes were checked with HTTP 200 and matching `lang`/canonical in `C:/Users/x8120/.codex/article-localization-batch-006/link-route-verification.json`, SHA-256 `84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`. A separate narrow link tool must handle locale-prefixed rewriting and rebind jobs before approval or publication.

## 2026-09-20 rebind and assembly checkpoint

- The three-guide live read-only audit at 13:32:37Z found all three published
  zh-TW versions/content hashes unchanged, no expiry, and all twelve target
  locales absent. Its receipt is
  `C:/Users/x8120/.codex/article-localization-batch-006/batch006-three-prepublish-audit-2026-09-20.json`,
  SHA-256 `641cb3418302cc01b4974025e67826262d19a7aa6e0e7b5e4e63881ae5bd8137`.
  All five versions of the three reviewed destination routes returned 200 with
  matching HTML language and canonical.
- Reprepared twelve jobs using the merged #596 locale-link tool. All 12 new
  source fields are byte-for-byte equivalent to the reviewed round3 fields.
  Reused only the twelve pinned `translated-fields.json` files after checking
  every old artifact manifest/receipt and source/pack hash. No new model call.
  Rebinding receipt:
  `C:/Users/x8120/.codex/article-localization-batch-006/three-guide-rebind-1ba-receipt.json`,
  SHA-256 `3cb6366b39a4af47bcefb68a293172831ea0c53616d9e7474104c8a61a33dbe4`.
- All twelve new documents pass strict field/GuideDocument validation and SVG
  rendering reports no layout issues. Compared with the prior reviewed round3
  documents, the only changes are exactly eight LinkBlock URLs: one per target
  locale in KL and Singapore hawker, each changed from the zh-TW route to the
  same published route in its target language. Gardens documents are unchanged;
  all twelve rendered SVG files have exactly the same bytes as round3. Diff
  receipt `C:/Users/x8120/.codex/article-localization-batch-006/three-guide-rebind-diff.json`,
  SHA-256 `f7e6fc9a36a04f3fe72c669c8ab8d19700c052afee6209735f02986924b9b2ed`.
- Staged exactly twelve target locale documents and twelve locale-suffixed SVGs
  in this branch. Original zh-TW documents, source SVGs, hero photos/credits,
  categories and ordering are unchanged. The assembly receipt is
  `C:/Users/x8120/.codex/article-localization-batch-006/three-guide-assembled-receipt.json`,
  SHA-256 `b46bb7c370b1506dc20d7be9577c4cb044fc2de34976de180ea0f8b26f66c3f2`.
  Independent round3/rebind editorial and visual signoff is complete; no
  import or publication has occurred for these three guides.
- Independent twelve-document and artwork signoff:
  `C:/Users/x8120/.codex/article-localization-batch-006/three-guide-independent-signoff.json`,
  SHA-256 `4e4b382ac27cd2f95c931afb4f66a38cde4a3fa4442c962b13e737210c921875`.
  Reviewer checked every translated scalar, numerical/eligibility condition,
  credits, SVG text, 1600x900 and 390px renders. All twelve assembled
  GuideDocument/SVG hashes match the approved artifacts. Eight rewritten
  locale links were rechecked after deployment: 200 response, matching HTML
  language and canonical, no redirect; evidence SHA-256
  `64519680453aec9bea17e1d730065fb497f233769eb1f7e51e3ae442c025e71a`.
- Focused repository tests: twelve passed, five skipped in
  `test_guides_content_pack.py` and `test_guides_content_links.py`.
  `npm run check:tasks` and `git diff --check` passed. Publication remains
  contingent on merged PR, green CI, fresh source/version audit, guarded
  deployment, import dry run and signed-out browser verification.
