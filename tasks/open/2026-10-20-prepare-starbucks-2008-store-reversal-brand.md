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
- [x] The script states the 600-includes-100 and 70%-of-selected-group limits; 205+383=588 is separate from the January 2009 ~200 cohort; U.S. comp, 53rd-week, and net-store scopes are explicit.
- [x] Offline generators, lint, Shorts schema/source checks, docs tests, task check, source hashes and a US$25 whole-episode quote are recorded. No paid media or YouTube artifact is claimed.
- [ ] A different agent performs a fresh line-by-line SEC audit against the frozen JSON SHA; two fresh independent readers blind-review the same narration and Shorts. Revisions require new SHA-linked reviews.
- [ ] After those reviews, the owner may authorize actual priced media work; real TTS, CC, MP4, 9:16 phone QA, branding manifest and platform URLs remain separate delivery gates.

## Steps

- [x] Read AGENTS.md, brand-story and curio production rules, recent X15 as a **format** guide, and the source scout.
- [x] Re-download five SEC originals and record byte lengths, SHA-256 and denominator boundaries in `source-matrix.md`.
- [x] Draft and compile `docs/videos/story-everyday-starbucks-x16/` with 20-series X16 metadata, script, Shorts and source/visual handoffs.
- [x] Check lint, Shorts, docs-videos tests and task board; freeze current JSON hashes; commit initial package only.
- [x] Archive v1's independent SEC HOLD and two frozen narrative blind reports; revise the source claims, structure, and portrait matches in v2.
- [x] Obtain a fresh independent same-hash SEC audit and two fresh narrative blind reads for v2; archive source PASS and both narrative HOLD receipts.
- [x] Rewrite the narrative as v3 around the supported selection criteria and actual July-cohort progress; remove the late operating-profit catalog and the Short 2 profit-to-same-store proof mismatch.
- [x] Obtain a fresh independent same-hash SEC audit and two fresh narrative blind reads for v3; archive their source HOLD and narrative HOLD receipts.
- [x] Rewrite v4 around an anonymous selection card; remove the shared Q8/Q13 narrative failures and correct all six v3 SEC HOLD findings. Freeze JSON hashes, lint, Shorts and docs checks; no media provider call.
- [ ] Obtain a fresh independent same-hash SEC audit and two fresh first-blind story reads for v4. Actual spoken-body duration remains unverified until TTS.

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

2026-10-20 v1 author handoff: Five issuer SEC originals all returned HTTP 200 and match the raw-byte SHA values in `source-matrix.md`; S3's first HTTP response was 106 bytes shorter but a second GET matched the original exact 1,563,888-byte file. Script had 157 lines, 159-character hook, 2,456-character substantive body, 10 loop links, 92 planned image-01 illustrations and 11 stats cards. Shorts had 8 beats each and 179/177 characters, and every beat had a 9:16 planned crop with safe-area instructions. Official 5-second intro follows the condensed opening, official 21-second v4 outro follows the last three narration lines. Everything remains **offline preproduction**.

Frozen v1 author candidate: `video.json` SHA-256 `9f59ef1533c74c0347e40d5534bb390aa00310ab4b5274e9f6172e68bf3c58fc`; `shorts.json` SHA-256 `1491b408cd15131425167b18093d1411af8ae8d979ee6082f923658bdfdc8498`. Independent v1 SEC audit was HOLD; blind A passed 6/12 and blind B 3/12 narrative checks. Receipts and the [v2 author remediation map](../../docs/videos/story-everyday-starbucks-x16/reviews/v2-remediation.md) are archived; none is a v2 PASS.

Frozen v2 author candidate: `video.json` SHA-256 `792a1007cd083bf035ff8127b889a91d40c018c5b923d34f820735848762b430`; `shorts.json` SHA-256 `11e9ea6515d500e0202e2b58506e606dca0211dc1c3ff264e758935e039b4066`. Independent SEC audit PASS, but blind A and B rejected the documentary-led, accounting-heavy narrative. Source and blind receipts are in `reviews/`.

Frozen v3 author candidate: `video.json` SHA-256 `3374c911b1a023b3906c8ff318b5ec37c1bbfdeb1915b20135e761a6cc151721`; `shorts.json` SHA-256 `2c3b4beb163618e9140c8bb97693efa669301f8ec2777ca380f0aafe9db28428`. Independent SEC re-fetch matched all five originals but source audit HOLD identified six wording/scope defects (age treated as a criterion, asset write-offs as equipment original cost, net additions as gross opening pace, a September filing error, January strategy phrased as completed, and an unbounded no-counterfactual assertion). Blind A passed 9/12 required narrative questions, B 8/12; shared Q8/Q13 failures. Their exact-SHA reviews are in `reviews/`.

Frozen v4 author candidate: `video.json` SHA-256 `504b042e45967dcd2e5f316841f8c36417b40ec3f55be07a1c0ebbdf8d0adfa5`; `shorts.json` SHA-256 `c694f6c2ac1a5fa809dc374e8c7e36966d898a1cd9351b29638588d2f8d6e113`. It has 144 lines, a 148-character opening, 1,965-character substantive body, 27 linked loops, 80 planned illustrations and 10 number cards; Shorts have 157/166 characters. Lint 0 errors/warnings, both Shorts schema/source checks pass; docs tests and task check have been run. The 8:00 spoken body is **not established** without real TTS; voice instructions target 230–250 characters/minute and require measurement/rewrite if short. V4 still needs independent source and two fresh narrative reads on these hashes. No paid provider call, MP4, upload, publish approval, or true YouTube watch URL exists.
