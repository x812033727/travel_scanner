---
id: 2026-10-20-prepare-x10-ebay-paypal-brand-story
title: Prepare X10 eBay PayPal brand-story episode
status: in-progress
priority: P2
area: docs
owner: codex-x10
claimed_at: 2026-10-20T19:12:55Z
created_at: 2026-10-20T18:04:54Z
completed_at:
branch: codex/brand-story-ebay-paypal-x10
depends_on: []
scope:
  - docs/videos/story-everyday-ebay-paypal-x10
---

# Prepare X10 eBay PayPal brand-story episode

## Why

The brand-story series needs another recognizable, nonduplicate episode after X01–X09. eBay's decision to spin off PayPal and later intermediate Marketplace payments is a documented reversal with an accessible SEC primary-source trail. The episode needs an original Taiwan-Mandarin script and shot package before any paid media work.

## Definition of done

- [ ] A six-body-chapter, source-bound X10 package includes 30–60 s condensed opening, at least 8 minutes of substantive spoken body by final TTS, three-line native ending, fixed 5 s/21 s branding handoff, two Shorts, and clickable-link checklist.
- [ ] Final main/Shorts SHA has an independent line-level source audit and two independent script-only narrative blind reviews; free lint has zero errors/warnings.
- [x] Draft PR opened with clear preproduction status; no paid generation or finished-video claim.

## Steps

- [x] Check 100-topic plan, X01–X09 drafts and retained reference-channel topic notes for duplicates; select eBay/PayPal angle.
- [x] Read accessible SEC source documents and write source notes plus claim matrix.
- [x] Draft six-body-chapter treatment, 105-line script and shot JSON, two Shorts, quote and publishing handoff.
- [x] Freeze main/Shorts SHA and obtain independent SEC source audit, including exact shot-and-line Shorts checks.
- [x] Obtain two independent script-only blind reads of the first SHA and resolve their shared findings in a revised candidate.
- [x] Re-audit v3 SHA against sources and obtain two new blind reads; revise their shared `no_recap` finding, main-question payoff and visual spoilers.
- [x] Re-audit v4 SHA against sources and obtain one new script-only blind read; both identified specific failures, preserved as historical receipts.
- [x] Re-audit v5 SHA against sources and obtain two independent script-only blind reads; source and blind A passed, blind B identified `scene_first` and `no_recap` failures.
- [x] Re-audit v6 SHA against sources and obtain two independent script-only blind reads; source passed, both blinds identified `no_recap` failures.
- [ ] Re-audit final v7 SHA against sources and obtain two independent script-only blind passes.
- [x] Open draft PR #1627 with clear preproduction status and historical review receipts.
- [x] Run v4 lint, docs-video tests, task check, claim/Shorts parity, then push the revised package to the draft PR.
- [x] Run v5 lint, docs-video tests, task check, claim/Shorts parity, then push the revised package to the draft PR.
- [x] Run v6 lint, docs-video tests, task check, claim/Shorts parity, then push the revised package to the draft PR.
- [x] Run v7 lint, docs-video tests, task check, claim/Shorts parity, then push the revised package to the draft PR.

## How to verify

From repo root:

```bash
node docs/videos/story-everyday-ebay-paypal-x10/compose-video.mjs
node docs/videos/story-everyday-ebay-paypal-x10/compose-shorts.mjs
node tools/video/cli.mjs lint --file docs/videos/story-everyday-ebay-paypal-x10/video.json --json
npm run test:docs-videos
npm run check:tasks
```

Compare generated SHA-256 against all review receipts, check Shorts phrases and shot IDs, and read `brief.md`/`publishing-handoff.md` to confirm no media or Studio URLs are claimed.

## Notes

SEC archive and `data.sec.gov` pages are accessible; `ebayinc.com` and live YouTube were blocked in this cloud, so no factual claim relies on them. Relevant accessible documents and scope limits are recorded in `source-notes.md`. C10 OXO belongs to a separate twenty-episode plan; the existing X01–X09 angles do not include eBay/PayPal. The user authorized choosing recommended decisions and opening PRs, but this task intentionally makes no paid calls. Paired video-tool token works in this environment; official selected 5 s/21 s branding assets and clickable Studio URLs are still pending media handoff. Draft script estimate is ~9:03 substantive body, to be measured after TTS.

The independent SEC source receipt `reviews/source-review-v2-root.md` passed the earlier SHA `7cf5f20c…` main / `9c82557f…` Shorts. Two blind receipts on that SHA both failed shared `no_toc`, `chapters_link` and `no_recap` gates, so the narration, loops and Shorts were revised. Those historical receipts cannot pass the new SHA; independent delta source review and a new two-reader blind pass remain open. Draft PR #1627 is a review surface, not a finished episode.

The v3 source delta receipt `reviews/source-review-v3-delta-root.md` passed main SHA `39edff49…` / Shorts `ae05695…`; its two new blind receipts both failed `no_recap`, and reader B also found the main why-question incompletely answered. v4 removed repeated claims but the independent source receipt `reviews/source-review-v4-independent.md` failed Short 2's FY2022 report attribution, while `reviews/blind-a-v4.md` failed opening spoiler and the central reason payoff. v5 removes the spoiler, places eBay's product rationale and its comparison limit in the 2020 body, names FY2022 explicitly, and rebuilds Short 2 as a standalone question-to-answer cut. All older receipts are historical only; v5 needs new exact-SHA checks before any media.

v5 `video.json` SHA-256 `f3d24233b82f41379b5126a06fcec8f9ec7759a17b403b2fa5a58a27b80f9bb4` and `shorts.json` SHA-256 `b7a3d36dc11ec780b65089b2fca1167893e06ba771ed912e578ae94a30a49d6e` received an independent [source PASS](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/source-review-v5-independent.md) and [blind A PASS](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/blind-a-v5-independent.md), but [blind B FAIL](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/blind-b-v5-independent.md) on `scene_first` and `no_recap`. These receipts are historical and do not pass v6.

v6 candidate: `video.json` SHA-256 `ff55b13fe19506d4f79586567fe47887f77dcb1b5b8d3aa9736d46416083179b`; `shorts.json` SHA-256 `d599da0a337d4740f9526d863fb6546a1f12f5df9ad33087bd46dd839b3d3c00`. The 2018 opening is explicitly an imagined buyer/seller checkout, not a documented individual sale; the 2015 chapter opener calls back to the opening agreement, while Short 1 uses a different self-contained line. Local lint returned 0 errors/0 warnings, both Shorts passed generator validation, 13/13 phrases match the selected main illustration shot, and the 105-line source matrix matches every line. The estimated spoken body is 546.3 seconds, not a TTS measurement. `npm run test:docs-videos` passed 236/236; `npm run check:tasks` exited 0 with unrelated existing queue warnings. Final independent source and narrative passes remain open.

v6 received an independent [source PASS](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/source-review-v6-independent.md). Both [blind A](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/blind-a-v6-independent.md) and [blind B](../../docs/videos/story-everyday-ebay-paypal-x10/reviews/blind-b-v6-independent.md) failed only `no_recap`: A flagged adjacent repetition of 2020 agreement expiry, B flagged the final answer repeating the buyer/seller product claim and partner-comparison caveat. Their source SHA is historical, not v7 approval.

v7 candidate: `video.json` SHA-256 `d0e77292c9b3547c8a34c19a034d1d400b18a157af8ecd846136019c6c398d6d`; `shorts.json` SHA-256 `15fa00305f4ad52d79b05fd9bbf4e0743923330a23f37792d1963c5ed9216a22`. `x100602` now advances to more markets without repeating the preceding expiry; `x100614` keeps the per-user measurement limit in the body, while `x100717` introduces the untested continued-PayPal comparison as the new closing limit. The opening visual shows a generic payment click and parcel beside a separate seller. Local lint returned 0 errors/0 warnings, with estimated hook 51.0 seconds and body 542.9 seconds; Shorts shot-line pairs 13/13 and source matrix 105/105. `npm run test:docs-videos` passed 236/236 and `npm run check:tasks` exited 0 with unrelated queue warnings. Source audit, blind reviews, and actual TTS durations remain open.
