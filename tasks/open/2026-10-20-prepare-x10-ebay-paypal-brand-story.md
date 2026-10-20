---
id: 2026-10-20-prepare-x10-ebay-paypal-brand-story
title: Prepare X10 eBay PayPal brand-story episode
status: in-progress
priority: P2
area: docs
owner: codex-x10
claimed_at: 2026-10-20T18:04:58Z
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
- [ ] Draft PR opened with clear preproduction status; no paid generation or finished-video claim.

## Steps

- [x] Check 100-topic plan, X01–X09 drafts and retained reference-channel topic notes for duplicates; select eBay/PayPal angle.
- [x] Read accessible SEC source documents and write source notes plus claim matrix.
- [x] Draft six-body-chapter treatment, 105-line script and shot JSON, two Shorts, quote and publishing handoff.
- [x] Freeze main/Shorts SHA and obtain independent SEC source audit, including exact shot-and-line Shorts checks.
- [ ] Obtain two independent script-only blind reads; resolve supported findings and rebind any changed SHA.
- [ ] Run repository checks, commit, push and open draft PR.

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

SEC archive and `data.sec.gov` pages are accessible; `ebayinc.com` and live YouTube were blocked in this cloud, so no factual claim relies on them. Relevant accessible documents and scope limits are recorded in `source-notes.md`. C10 OXO belongs to a separate twenty-episode plan; the existing X01–X09 angles do not include eBay/PayPal. The user authorized choosing recommended decisions and opening PRs, but this task intentionally makes no paid calls. Paired video-tool token works in this environment; official selected 5 s/21 s branding assets and clickable Studio URLs are still pending media handoff. Draft script estimate is ~8:58 substantive body, to be measured after TTS.

The independent SEC source receipt `reviews/source-review-v2-root.md` passes exact SHA `7cf5f20c…` main / `9c82557f…` Shorts. The two narrative blind reads remain pending; the draft PR is a review surface, not a finished episode.
