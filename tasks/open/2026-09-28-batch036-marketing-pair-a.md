---
id: 2026-09-28-batch036-marketing-pair-a
title: Batch036 localize marketing pair A in five languages
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T09:19:38Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/marketing-plan-small-business.json
  - apps/api/app/guides/content/paid-vs-organic-marketing.json
  - apps/web/public/guides/marketing-plan-small-business
  - apps/web/public/guides/paid-vs-organic-marketing
  - docs/article-localization/batch036-marketing-pair-a-evidence.md
  - tasks/open/2026-09-28-batch036-marketing-pair-a.md
---

# Batch036 localize marketing pair A in five languages

## Why

Both public guides had only the published zh-TW v4 document at the pinned
read-only inventory. Four locale rows per article were missing. Add complete
repository drafts and translated original illustrations before guarded import.

## Definition of done

- [x] Add complete zh-CN/en/ja/ko documents for both articles, preserving 33
      source blocks, tables, source dates/URLs, and article-reference targets.
- [x] Add and render 24 localized image assets with original credits intact.
- [x] Obtain independent editorial review of meaning, figures and navigation.
- [ ] Obtain green PR checks before merge.
- [ ] Correct the inherited Google SEO page title and `hl=zh-Hant` source
      metadata through a versioned source follow-up before publication.
- [ ] Import/publish guarded locale revisions and verify live pages separately.

## Steps

- [x] Pin production and repository source versions and claim the pair scope.
- [x] Author eight target documents and 24 language assets.
- [x] Run content, asset, SVG-browser, focused tests and task checks.
- [x] Open draft PR and record its URL and CI status.

## How to verify

From `apps/api`, run `uv run python -m app.guides.pack_cli lint --kind life
--slug <slug>` for both slugs, then `uv run pytest
tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`.
From the root, run `npm run test --workspace @travel-scanner/web --
components/content-blocks.test.tsx` and `npm run check:tasks`. The scoped
evidence document pins source, document, asset and render hashes.

## Notes

The original subagent completed the marketing-plan documents and art but hit a
usage limit before finishing the second article. Codex-root released and
reclaimed this task, completed paid-vs-organic in four target languages and
made its localized hero/diagram from the original SVGs. The first SVG browser
run detected two overflowing English headings; both were reduced by 2 px and
the next run passed all 16 assets. Both packs lint with source no-summary and
advisory long-English-body warnings only. API tests: 12 passed, 5 skipped;
web tests: 65 passed. Independent read-only editorial review marked both
articles GO. The reviewer found a zh-CN `照著` typo, corrected in the pack;
the SEO source page title and Google Ads forced-language URL remain inherited
source-metadata follow-up. Public browser QA is pending.
Draft PR: https://github.com/x812033727/travel_scanner/pull/908.
CI began on the submitted branch; merge remains gated on independent editorial
review and green checks.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-root (since 2026-09-28T10:23:38Z) was stale and is released so it stops locking its scope. Landed: #908. Still open: Green PR checks before merge (done implicitly, merged); Correct inherited Google SEO title and hl=zh-Hant source metadata via versioned source follow-up; Import/publish guarded locale revisions and verify live pages.

## 2026-10-07 current marketing-plan review

Reclaimed by `codex-article-localization-4e16` on
`codex/article-missing-locales-20261007` for marketing-plan-small-business only.
The original pair scope remains recorded so paid-vs-organic-marketing stays
held for its unresolved source-metadata follow-up; that pack and its assets
must remain byte-identical in this recheck.

- [x] Compare marketing-plan zh-TW with the current retained production
      snapshot: source SHA-256
      `1f556287a76e6352278f7a53601c6cb425201f2db1be6fe75d7f4f72943f6403`
      matches, published zh-TW v4, four target rows absent, no aliases or holds.
- [x] Independently read all five documents, check the current official
      Australian/SBA supporting content, and inspect eight freshly rendered
      target SVGs plus four actual target hero JPGs.
- [x] Prepare nine mandatory marketing-plan pointer changes: eight terminal
      published-title labels and zh-CN hero alt `萤幕` to `屏幕`.
- [x] Root applies the exact corrections as a party distinct from the reviewer.
- [x] Independently recheck final hashes and issue a genuine current
      route-b-review-v1 receipt. Preserved originals remain CORRECTIONS_REQUIRED;
      corrected marketing-plan documents have current PASS review.

Private evidence directory:
the owner's persistent storage, under the current independent-review evidence.
Combined two-article `findings.json` SHA-256:
`e7f567907ebb7a4665a09d999fc5db2a54fca08617199cf9eeb61101ccd4da46`.
Larger zh-CN copy normalization and an optional matching SVG accessibility
description are separately proposed, not included in the mandatory application.
The independent reviewer did not apply article corrections. Root applied the
nine exact marketing-plan changes, then the reviewer confirmed current PASS.
Corrected pack SHA-256:
`06faef98b9310009ee7a32904f60474fd6da373c5a9305879334d9b9c2753582`.
Combined current review receipt SHA-256:
`6215361cac8abb391690d973feee8dc1b775400ab4477f8384b83fbd61e0bf72`.
Sanitized current evidence is appended to the scoped Batch036 evidence doc.
No locale has been imported or published. The paid-vs-organic source
follow-up and this pair's release work remain incomplete.

## Final cohort review, 2026-10-07

Current independent final review at 2026-10-07T05:57:52.724199+00:00 verifies this task's
exact current content, unchanged source/root metadata/assets and all same-cohort
terminal link labels. Combined 32-row route-b receipt SHA-256
`87986003cd9e266df5e569270ab3d2859f1573433d5c0f1d967c331e1969beaa`; common evidence SHA-256
`d6e10b7546c48b0cdd76c0c03517c6d8ba0a2c0a84a99462ada3e6ed74e91527`.
Use only the immutable external `reuse-t1/life-cohort-final-review-v2` receipts.
All current eight life-pack lints exited 0; no production publication is claimed.
The prospective content PR must freeze exact committed blobs separately.

Root additionally applied four prospective business-guide title labels as a distinct actor. Current marketing-plan pack SHA-256 `c871fb1cbac44c7886755a64c501a4667d01493aa51aedc42e04ba03fa1152ed`; held paid-vs-organic and its assets remain unchanged.

### Partial scope release

marketing-plan-small-business current four-language review and corrections are
complete in PR #1365 and the first 52-target release cohort. paid-vs-organic
remains held by its recorded source/citation questions and is not included.
This paired ticket remains unfinished for that held article and is released to
the shared queue; no paid-vs-organic content or image bytes were changed.
