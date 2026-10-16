---
id: 2026-10-16-improve-mobile-readability-of-brand-story
title: Improve mobile readability of brand-story title cards
status: in-progress
priority: P1
area: tools
owner: codex-five-card-qa
claimed_at: 2026-10-16T01:19:19Z
created_at: 2026-10-16T00:17:57Z
completed_at:
branch: codex/a01-pilot-deploy-evidence-20261015
depends_on: []
scope:
  - tools/video/templates
  - docs/videos/brand-stories-five-20261014/drafts-20261016/formal-prototypes/mobile-title-qa
---

# Improve mobile readability of brand-story title cards

## Why

The four brand-story prototypes A16, A37, B14 and A21 contain 49 source-bound `title` cards. Their source labels now spell out the original internal `S#` codes, but the shared title template renders the source badge at 36px and subtitle at 46px in a 1920×1080 frame. At a 320×180 player preview these become about 6px and 7.7px. Full-size cards have no clipping, while the source and subtitle are broadly unreadable on a phone. Shortening two representative source labels cannot fix the shared typography. The baseline and hash-bound candidate evidence are in `docs/videos/brand-stories-five-20261014/drafts-20261016/formal-prototypes/readable-source-qa-20261016.md`.

## Definition of done

- [x] Source badges and subtitles on all 49 A16/A37/B14/A21 title cards are readable at 320×180 without hiding source provenance, numbers or claim scope.
- [x] All 49 cards remain unclipped at 1920×1080; the shared template's other title cards do not regress in the sampled non-brand control.
- [x] A complete before/after visual QA record and actual render hashes are saved under `mobile-title-qa`; originals, reviewed narration and source maps stay unchanged.

## Steps

- [x] Inspect `tools/video/templates/theme.css` and `templates.mjs` to choose appropriate title-card font sizing and information hierarchy; account for this template's other users.
- [x] Update the template and run the relevant existing tests within `tools/video/templates` without changing the 49 existing candidate texts or their source pins.
- [x] Re-render all 49 cards with the official local renderer at 1920×1080 and inspect each at full size and 320×180; record cards needing further design work rather than marking a mechanical render as a visual PASS.

## How to verify

Run `node --test tools/video/templates/templates.test.mjs` and `npm run test:docs-videos` for the shared template. Use the exact chapter JSONs under each `formal-prototypes/{A16,A37,B14,A21}/readable-source-candidate/chapters/`, not an unreviewed rewrite. Capture the official renderer's problems, PNG hashes and all 49 full-size/mobile inspection results in the scoped QA directory. Compare original chapter and reviewed narration hashes before and after; confirm the old evidence remains available.

## Notes

- 2026-10-16 local result: the shared `title` CSS now uses 64px source badge and subtitle, stronger subtitle contrast, 24px spacing and source word-preserving wrapping. Six full-size and six native 320×180 contact sheets were visually inspected for all 49 A16/A37/B14/A21 candidate cards; none had unreadable source/subtitle, clipping or overlap. A16 `now-072` uses two intact source lines; A16 `turn-062`, B14 `turn-075`, A21 double-line titles and the non-brand `showcase#opening` control were individually checked. Official renderer problems: 0 for all 50. The 24 candidate and 24 original chapter SHA checks matched their prior evidence exactly, so narration/source text did not change. Exact per-card/sheet evidence and limits: `docs/videos/brand-stories-five-20261014/drafts-20261016/formal-prototypes/mobile-title-qa/` (local render index SHA `ea19061985552373d9bf39ea13fb31bf2288b9f868897f53b264d76c29efbb50`). This is a static local card PASS, not film/owner/host acceptance.
- `templates.test.mjs`: 27/27; `repo-hygiene.test.mjs`: 3/3. `test:docs-videos`: 214/215, with one unrelated Windows system-Node `package-runtime.mjs` process failure `3221226505` in imported-long-languages runner; no broad rerun. No host/model/paid calls, push or PR action in this task phase.
- 2026-10-16 claim: `codex-five-card-qa` used `--force` only because its same-owner five-film task claims the parent documentation path while this narrowly scoped template/mobile-QA follow-up is being done on the shared branch at the owner's direction. No other agent's active template scope is being taken; this does not mark the broader five-film task complete or change its pilot/media gates.
- 2026-10-16: Parent/root visually inspected A16 `now-072` and B14 `turn-075` at 1920×1080 and agreed the mobile problem is in the shared 36/46px template, not just long tag copy. The existing readable-source candidate stays separate from original chapters and has not been installed in the worker. The full 49-card render index SHA-256 is `ac70757f531fc86e758429df9105ca606d5a743f4539483a8ec6a42c636072c8`; PNGs/contact sheets are outside Git under `<local-temp>/five-next/card-source-candidate-20261016-r3/`. That Temp path is evidence from this run, not a durable dependency; regenerate if absent.
- This is local template/visual QA work. It does not authorize chapter adoption, paid media, host import, deployment or release of the five films.
