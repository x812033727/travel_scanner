---
id: 2026-09-20-hanoi-old-quarter-vietnam-tourism-source
title: Repair dead Vietnam Tourism source link in Hanoi Old Quarter guide
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-20T13:27:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
  - tasks/open/2026-09-20-hanoi-old-quarter-vietnam-tourism-source.md
---

# Repair dead Vietnam Tourism source link in Hanoi Old Quarter guide

## Why

The published zh-TW Hanoi Old Quarter article cites a Vietnam Tourism destination URL that returned HTTP 404 in the 2026-09-20 source audit. A separate original-source correction PR #599 deliberately changes only an awkward sentence; the dead citation remains unresolved. The destination source needs a verified working official replacement or a documented removal without losing support for the article's claims.

## Definition of done

- [ ] Recheck the exact cited URL, find an authoritative live replacement supporting the same Hanoi/Hoan Kiem claim, or remove/replace the unsupported citation with a documented rationale.
- [ ] Change only the affected source citation title/URL and directly related text if required, preserving all other source dates, prose, credits and locale status.
- [ ] Validate the ArticlePack and run a guarded version-aware update so no concurrently edited published article is overwritten. Rebind pending Hanoi locales if the published source hash changes.

## Steps

- [ ] Claim only after the active Hanoi localization task releases or narrows its pack scope; do not force through the overlap.
- [ ] Verify source authority and claim coverage before editing, then compare source versions/hashes and prepare a minimal diff.
- [ ] Record the live status, release, and downstream four-locale rebind evidence.

## How to verify

Verify the replacement URL directly from the official publisher, parse the pack as `ArticlePack`, inspect the exact JSON pointer diff and run relevant guides content tests plus `npm run check:tasks`. After controlled release, inspect the live source URL and published version/hash.

## Notes

- Exact stale source: `apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json`, `/locales/zh-TW/sources/1/url`, `https://vietnam.travel/places-to-go/northern-vietnam/ha-noi` (observed HTTP 404 on 2026-09-20). Current title: `越南官方旅遊：河內目的地與還劍湖`; `checked_on` is `2026-09-14` and must not be silently presented as a fresh check.
- At the 2026-09-20 read-only snapshot, the article was v1, published zh-TW v6, normalized document SHA-256 `7414980741ec969be8132a476130d6fb725ac6e079594b4b993823235b84d3d0`. PR #599 changes only `/locales/zh-TW/blocks/11/text` and is not yet a live source update; re-snapshot after it releases.
- The existing first source `https://vietnam.travel/node/915` is official and describes Old Quarter walking. It is already cited and should not be duplicated as a replacement without confirming the missing source's Hoan Kiem coverage.
- The active Hanoi localization task `2026-09-20-article-localization-batch-006` currently claims this pack, so this task is intentionally open/unclaimed. Coordinate the release of that scope before changing product content. No URL or production change was made when filing this task.
