---
id: 2026-10-20-prepare-starbucks-2008-store-reversal-brand
title: Prepare Starbucks 2008 store reversal brand-story X16
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T21:23:47Z
completed_at:
branch: codex/brand-story-starbucks-x16
depends_on: []
scope:
  - docs/videos/story-everyday-starbucks-x16
---

# Prepare Starbucks 2008 store reversal brand-story X16

## Why

The new 20-video brand-story series needs an X16 Starbucks episode about the July 1, 2008 U.S. direct-store closure announcement. The frequently repeated numbers mix announcement targets, actual closures, net store counts, two separate closure cohorts, and later sales changes. A reviewable preproduction package must preserve those denominators before paid media work.

## Definition of done

- [x] An X16 six-chapter long-film script and two independent Shorts exist with linked source originals, exact line references, paid loops, illustrated storyboard, and 9:16 per-beat crop/safe-area plan.
- [x] The script states the 600-includes-100 and 70%-of-selected-group limits; 205+383=588 is separate from the January 2009 ~200 cohort; U.S. comp, 53rd-week, and consolidated operating-income scopes are explicit.
- [x] Offline generators, lint, Shorts schema/source checks, docs tests, task check, source hashes and a US$25 whole-episode quote are recorded. No paid media or YouTube artifact is claimed.
- [ ] A different agent performs a fresh line-by-line SEC audit against the frozen JSON SHA; two fresh independent readers blind-review the same narration and Shorts. Revisions require new SHA-linked reviews.
- [ ] After those reviews, the owner may authorize actual priced media work; real TTS, CC, MP4, 9:16 phone QA, branding manifest and platform URLs remain separate delivery gates.

## Steps

- [x] Read AGENTS.md, brand-story and curio production rules, recent X15 as a **format** guide, and the source scout.
- [x] Re-download five SEC originals and record byte lengths, SHA-256 and denominator boundaries in `source-matrix.md`.
- [x] Draft and compile `docs/videos/story-everyday-starbucks-x16/` with 20-series X16 metadata, script, Shorts and source/visual handoffs.
- [x] Check lint, Shorts, docs-videos tests and task board; freeze current JSON hashes; commit initial package only.
- [ ] Hand independent same-hash source audit and two narrative blind reads to other agents; keep receipts in the episode folder.

## How to verify

```bash
node docs/videos/story-everyday-starbucks-x16/compose-video.mjs
node docs/videos/story-everyday-starbucks-x16/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-starbucks-x16
npm run test:docs-videos
npm run check:tasks
sha256sum docs/videos/story-everyday-starbucks-x16/{video,shorts}.json
```

`shorts.json` is a two-object array for `from-episode`; for `shorts/cli.mjs validate`, write each object to a temporary JSON file and use `--source-base docs/videos/story-everyday-starbucks-x16`.

## Notes

2026-10-20 author handoff: Five issuer SEC originals all returned HTTP 200 and match the raw-byte SHA values in `source-matrix.md`; S3's first HTTP response was 106 bytes shorter but a second GET matched the original exact 1,563,888-byte file. Script is 157 lines, 159-character hook, 2,456-character substantive body, 10 loop links, 92 planned image-01 illustrations and 11 stats cards. Shorts have 8 beats each and 179/177 characters, and every beat has a 9:16 planned crop with safe-area instructions. Official 5-second intro follows the condensed opening, official 21-second v4 outro follows the last three narration lines. Everything remains **offline preproduction**.

Frozen author candidate: `video.json` SHA-256 `9f59ef1533c74c0347e40d5534bb390aa00310ab4b5274e9f6172e68bf3c58fc`; `shorts.json` SHA-256 `1491b408cd15131425167b18093d1411af8ae8d979ee6082f923658bdfdc8498`. Author source matrices are not independent PASS receipts. S1–S5 are all <3 MiB; `source-matrix.md` explains individual claims and exclusions. No paid provider call, MP4, upload, publish approval, or true YouTube watch URL exists.
