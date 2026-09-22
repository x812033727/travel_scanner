---
id: 2026-09-21-taiwan-zh-tw-second-sub-batch
title: Taiwan zh-TW second sub-batch: Taipei metro and Taoyuan airport
status: done
priority: P2
area: api
owner: codex-taiwan-zh-tw
claimed_at: 2026-09-21T13:20:02Z
created_at: 2026-09-21T13:19:57Z
completed_at: 2026-09-21T15:12:25Z
branch: codex/taiwan-zh-tw-batch-002
depends_on: []
scope:
  - apps/api/app/guides/content/taipei-metro-easycard-guide.json
  - apps/api/app/guides/content/taoyuan-airport-to-taipei.json
  - apps/web/public/guides/taipei-metro-easycard-guide/diagram-1-zh-tw.svg
  - apps/web/public/guides/taoyuan-airport-to-taipei/diagram-1-zh-tw.svg
---

# Taiwan zh-TW second sub-batch: Taipei metro and Taoyuan airport

## Why

Two published Taiwan transport guides have complete en, ja, ko and zh-CN
publications but no zh-TW document. Their route diagrams also contain mixed
Traditional Chinese and English labels. This bounded batch adds full zh-TW
documents and zh-TW-only diagrams while preserving the current repository
metadata, existing locales, image credits and live editorial revisions.

## Definition of done

- [x] Both zh-TW GuideDocuments cover every live source field and validate against the API schema.
- [x] Both text-bearing SVGs are localized, rendered and visually reviewed at desktop and 390px.
- [x] Independent editorial review approves facts, numbers, links, source records and artwork.
- [x] Only the missing zh-TW locales are imported and published after guarded PR, CI and release checks.

## Steps

- [x] Capture a fresh read-only production snapshot for exactly the two claimed slugs.
- [x] Author the complete Taipei Metro/EasyCard zh-TW document and localized diagram.
- [x] Author the complete Taoyuan Airport transport zh-TW document and localized diagram.
- [x] Resolve independent-review findings and create a hash-bound review handoff.

## How to verify

Run focused `pack_cli lint` for both slugs, `pytest` for guide content packs and
links, `npm run test:tools`, `npm run check:tasks`, translation field/number/link
audits, and Playwright SVG render/geometry checks. Before release, repeat the
production version/hash guard and a slug-scoped import dry run.

## Notes

- Worktree `C:\Users\x8120\.codex\worktrees\taiwan-zh-tw-batch-002\travel_scanㄐ`
  and branch `codex/taiwan-zh-tw-batch-002` started from `origin/main`
  `c10ba4de869ee32573abd9e2fc20ed43edfec6fb`.
- Fresh read-only production snapshot captured at 2026-09-21T13:20:38Z in
  `C:\Users\x8120\.codex\article-localization-taiwan-zh-tw\batch002\fresh-live-two.json`,
  SHA-256 `c1d3d0826716f08eb4bcf715b378a4790f078ba017787eb2db6a8635b7a06758`.
  Both articles are active/published article version 2 with no zh-TW locale.
  Taipei Metro zh-CN is published version 6, SHA-256
  `38e3517128e73d39f93ad68087e91613af7582c5000bf2e4622fc29badf7e235`;
  Taoyuan Airport zh-CN is published version 6, SHA-256
  `9a4341448f4f6c3c6a5a8db94c14c7c0ca7d12d07eb5c91893ae6f9d777098cc`.
  Repository zh-CN differs from both live documents, so the new zh-TW prose was
  derived from the fresh live publications. Existing repository locales and all
  article metadata remain byte-for-byte equivalent in parsed form.
- Primary-source rechecks corrected the zh-TW target rather than copying two
  stale claims: Taoyuan Airport MRT accepts Visa, Mastercard, JCB and UnionPay
  contactless cards, Apple Pay, Google Pay and Samsung Pay, and provides an
  Alipay ride code; Taipei Metro food/drink violations carry the statutory
  NT$1,500–7,500 range. TWAC wording now lists the exact document/status groups
  that must submit within seven days and does not infer nationality from locale.
  Mainland China tourism wording states the Taiwan travel-agency filing role and
  requires a current acceptance/eligibility check instead of claiming the 2022
  procedure is presently open to every reader.
- The Taipei Metro document retains 37 blocks and 20 sources; Taoyuan Airport
  retains 36 blocks and 20 sources. The latter replaces two redundant source
  records with the official Taoyuan Metro contactless-card and Alipay pages to
  stay within the GuideDocument maximum of 20 sources.
- SVG render receipt SHA-256 is
  `e446ee1f9c9876037e8978a6c7dae5517c40dec5e89aa0a117c6b0055b2f99ff`.
  Both 1600x900 diagrams rendered at desktop and 390px; the four PNGs have no
  clipping or missing glyphs on manual inspection. Geometry audit SHA-256
  `e97c240500eb07a33a595937d5ce2504c5d9f78d68d45f041b2c621f041b904a`
  reports 38/32 visible text nodes and zero canvas-overflow or text-overlap issues.
  Mobile diagram text is necessarily small, so the ImageBlock descriptions carry
  the full route, fare, eligibility and rule details as readable page text.
- Both focused pack lint commands pass with pre-existing editorial warnings only;
  guide content/link tests pass (12 passed, 5 skipped); `npm run test:tools`
  passes (75 passed, 1 skipped); `npm run check:tasks` validates 655 task files
  with unrelated pre-existing warnings; `git diff --check` passes.
- Independent review resolved Taiwan terminology for contactless credit/debit
  cards, `航廈` and `尖峰時段`; it also corrected the HSR early-bird purchase
  window wording, an 1819 timetable space and the taxi fare-table wording.
  The reviewer re-read the final LF-normalized repository bytes and approved the
  two packs, two SVGs, primary-source facts, source metadata, internal links and
  desktop/mobile renders with no remaining blockers. The final pack SHA-256 values
  are `3c684f162bd5abbe128b3374338e431b3f4089013fb584de30ba3fae30b581d6`
  and `6f06c7b7fe6ea026634b7de2605e4aeb0c02ed31160e51fe58637dcd65d9db76`;
  final SVG SHA-256 values are
  `f34bde51024d684e41820c73fd93ef6e5d95fa86dc10f1d614e10bd7528f19d6`
  and `548b9d1ea5859c52e659d86808d4ef60fafb7fecd3bb764a38d685d6fd283bff`.
  The hash-bound review receipt is
  `C:\Users\x8120\.codex\article-localization-taiwan-zh-tw\batch002\independent-review.json`,
  SHA-256 `f135e81463f57a2e117322496357e83dc5a06f85ec210244ca8db65dc1159ef3`.
- Content PR #620 merged to main as
  `bb53e361bb6c1ac35a00ac0f65e49c0b304ac034`. Exact-main CI run
  `35612293976` completed successfully with API, web, containers and
  full-stack-smoke jobs all green (4/4).
- Publication used plan
  `8537f1c625fdb5647664b95a788ec7bf890bc2e608bb7ef982956ed05c23a68e`
  and manifest
  `8b7d820cbd023a5176c1d705bf2a3f9cf835178438ab597c540e37379cbe4de3`.
  The predeploy backup is a verified `pg_dump -Fc`
  (`23f99d97fcb7b9f672a0c2257b66278b58637a007c020b18fbdd43dd06b5e7ba`);
  the separate prepublication backup is also index-verified
  (`9c1fa3069d59e9b77da05bce7d5efe714dfd30ef54664255a0e5707e3fd91493`).
- Guarded phase receipts show dry run `old` for both operations with zero
  writes, drafts `drafted` for both with two writes, publish `complete` for
  both with two writes, and verify `complete` for both with zero writes. The
  draft browser proof confirmed both real zh-TW routes were unavailable and
  absent from all 2,361 public sitemap URLs before publication.
- Final browser QA passed all 20 page checks (two slugs, five locales, desktop
  and 390px mobile), including exact content and SVGs, canonical, reciprocal
  hreflang, same-locale links and layout. It recorded 22 passing checks, 28
  hash-bound evidence files and 2,363 sitemap locations. Browser receipt SHA-256
  is `38827350c52eff6a6790bb20e13e60914c5fbdd89a98d6b9da370a4a558f0127`.
- The release completed at `2026-09-21T15:08:26.317632+00:00`, then removed
  the deployment hold. Final readiness reports database and Redis `ok` at
  schema `0082_travel_food_subtopics`; all 10 containers are running with zero
  restarts.
- Two postdeploy log lines are accounted for. `destination stream closed early`
  occurred only during browser QA and remains tracked by open task
  `2026-09-12-community-smoke-econnreset-stays-unexplained-after`; the Otaru
  `HTTPStatusError` came from a completed background hotspot collection and did
  not affect this release.
