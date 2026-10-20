---
id: 2026-10-20-prepare-krispy-kreme-mcdonalds-brand-x18
title: Prepare Krispy Kreme McDonald’s brand-story X18
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T22:40:36Z
completed_at:
branch: codex/brand-story-krispy-kreme-x18
depends_on: []
scope:
  - docs/videos/story-everyday-krispy-kreme-x18
---

# Prepare Krispy Kreme McDonald’s brand-story X18

## Why

The new twenty-film brand-story series needs a reviewable X18 about the Krispy Kreme and McDonald’s daily-delivery partnership. The 160-store trial was described as exceeding demand expectations, yet the rollout was paused around 2,400 McDonald’s restaurants and jointly ended. It is easy to mistake the 2026 nationwide plan for completed rollout, treat one party’s satisfaction as both parties’ profit, or attribute broad company financial changes solely to this partnership. The offline package must preserve the event chronology and accounting denominators before any paid production.

## Definition of done

- [x] X18 has six linked zh-TW chapters, a 30–60-second condensed opening, three unrevealed future moments, >=2,450 substantive body characters, >=8 paid loops, and exactly three closing sentences.
- [x] Two independent 25–55-second paper Shorts have 8 portrait beats each, bound to 16 distinct main-film shots, with source maps and crop/safe-area plans.
- [x] Eight SEC originals have HTTP, raw bytes, SHA-256, <3 MiB and first-40k readability recorded; source limits distinguish plan/actual, 6/29/7/2 cutoffs, point-of-access denominators, GAAP and adjusted metrics.
- [x] Offline JSON compilation, lint 0/0, Shorts validations, docs-video tests, task check, diff check and US$25 whole-episode quote are recorded. No paid media, MP4, upload or source-review PASS is claimed.
- [ ] A different agent independently audits all lines, cards, Shorts and publishing text against fresh originals at the frozen SHA; two fresh readers blind-review the same exact narration. Any revisions invalidate those reviews.
- [ ] After independent review, real TTS and actual media may proceed within one US$25 limit; actual body >=8:00, official animations, CC, Shorts phone QA and true platform links remain separate gates.

## Steps

- [x] Read AGENTS.md, brand-story / youtube-video skills, X16/X17 format guides and network policy; create independent sparse worktree from latest origin/main.
- [x] Author re-downloaded eight issuer SEC HTML exhibits and built `source-matrix.md` with precise dates, counts, denominator boundaries and prohibited inferences.
- [x] Draft six-chapter treatment, brief, narration, author line-source matrix and shot/card JSON with official 5-second intro and 21-second v4 outro handoff.
- [x] Draft two independent Shorts, source matrix, 9:16 per-beat plan and source-anchored JSON; add production quote, publishing handoff and README.
- [x] Run offline checks and freeze main/Shorts SHA in README and this task, commit initial package locally only.
- [x] Obtain independent source and narrative review of v1 and v2 frozen versions; archive the exact-SHA PASS/HOLD receipts and author response.
- [x] Revise shared v2 narrative blockers in v3, rebuild, and freeze the author package at new main/Shorts SHA.
- [ ] Obtain a new independent SEC audit and two first-blind reviews on the exact v3 SHA; any subsequent edit requires a new freeze.

## How to verify

```bash
node docs/videos/story-everyday-krispy-kreme-x18/compose-video.mjs
node docs/videos/story-everyday-krispy-kreme-x18/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-krispy-kreme-x18
node --input-type=module -e 'import {readFileSync} from "node:fs"; import {episodeShortsProblems} from "./tools/video/shorts/episode.mjs"; const d="docs/videos/story-everyday-krispy-kreme-x18/"; const p=episodeShortsProblems(JSON.parse(readFileSync(d+"shorts.json")),JSON.parse(readFileSync(d+"video.json"))); if(p.length){console.error(p);process.exit(1)} console.log("episode Shorts PASS")'
npm run test:docs-videos
npm run check:tasks
git diff --check
sha256sum docs/videos/story-everyday-krispy-kreme-x18/{video,shorts}.json
```

`shorts.json` contains two objects; the individual `shorts/cli.mjs validate` command requires a temporary JSON holding one object plus `--source-base docs/videos/story-everyday-krispy-kreme-x18`. The commands above do not create media or prove spoken duration.

## Notes

2026-10-20 author handoff: Eight SEC originals all returned HTTP 200 and match the source matrix raw bytes/SHA. The middle-event originals matter: 2024 Q3 reported October Chicago rollout, 2024 Q4 confirmed over 1,900 McDonald’s locations as of Dec 29, and 2025 Q1 confirmed over 2,400 as of Mar 30 plus reassessed schedule / expectation of no Q2 additions. This avoids stretching two press releases with financial tables.

Candidate main contains 133 lines, 203-character opening, 2,747-character substantive body, 14 linked loops, 114 image-01 stills and 11 postproduction stats cards. Shorts are 198/214 characters. Actual TTS, image generation, finished film, platform URLs and independent review do not exist. Frozen author candidate `video.json` SHA-256 `d7fb2a16e4e7671d2fed585438f3a365fe4a450ef8267cb02a3bc62a6d07384e`; `shorts.json` SHA-256 `62c4c30c03082a0c0bcf631b0e56282bb44033483671ab499eb97febf1e6e7a2`. Any later revision needs new freeze and review.

Author checks on this candidate: lint 0 errors/0 warnings; each Short CLI validate PASS; `episodeShortsProblems` PASS; `npm run test:docs-videos` 236/236 PASS; `npm run check:tasks` exit 0 (pre-existing stale-claim/scope warnings). `git diff --check` and commit id are recorded in git history. These do not constitute independent source or story PASS.

v1 independent [SEC audit](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/script-source-audit-v1-independent.md) passed, but two fresh [A](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/blind-a-v1-independent.md) / [B](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/blind-b-v1-independent.md) narrative ballots shared mandatory Q4/Q7/Q8/Q10/Q13 NO. v2 author trimmed the financial tail, placed an anonymous physical tray action first, withheld Chicago until chapter three, returned the tray at the cost answer, and fixed Short 2's native map/keyframe source. Frozen v2 `video.json` SHA-256 `714dd069258b64b2fdb0da473ec9a4ed4d1162d2000a515bbae3f944d7c1b50b`, `shorts.json` `760e2eef6dc0f7a15adc42d1740ea49de6c06553f97c55a8bf6d943b446815f6`; lint 0/0, episode Shorts check empty, two Shorts validate, docs-video tests 236/236.

v2 independent [SEC audit](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/script-source-audit-v2-independent.md) re-fetched all S1–S8 raw originals with matching byte counts and SHA and passed factual scope. Two truly fresh readers [A](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/blind-a-v2-independent.md) and [B](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/blind-b-v2-independent.md) both answered mandatory Q8 and Q13 NO: route/delivery cost restatements and a company-wide finance tail after the partnership's answer. B additionally marked Q3 NO because chapter six rewinds from the July 2 termination back to the June 29 cutoff. Thus v2 narrative remains **HOLD**. v3 should keep the date distinction, but advance from June accounting into July termination without rewalking the same cutoff; let the daily tray have new states rather than repeating the daily-delivery premise; reduce the Q3/FY total-company result to a brief bounded coda or supporting material. Real TTS, official animations, paid media and platform links remain unverified.

v3 author package: [response](../../docs/videos/story-everyday-krispy-kreme-x18/reviews/author-response-v3.md) addresses v2 Q3/Q8/Q13 by keeping 6/23 **announcement** → 6/29 Q2 cutoff → 7/2 **effective** exit → 9/28 Q3 point-of-access map in order. The central S5 answer remains the company-attributed unit-demand/cost mismatch; the Q3/FY company-wide profit tail is outside spoken narration. S2's wider-delivery carrier tender and early partnership start-up costs add sourced movement, with scope and other U.S. cost factors marked. Last scene closes the illustrative McDonald’s delivery route. Short 2 now ends on the date/POA denominator answer, without a second profitability question. Frozen candidate `video.json` SHA-256 `ba5500bc756135bd2a0d5093fd0a0d209b8c7b3bdcd3b087c0d205e76b852b43`; `shorts.json` SHA-256 `ecb5cc1422695b11ebd62efae8a6369ec89c9cf481a4b18f71490b8367e23141`. Opening 185 chars, body 2,482 written chars (lint 2,423 spoken units, barely over 8:00 at 300/min), 13 loops, 118 lines, 106 stills, six native stats, Short lengths 198/188 written chars. Author checks: lint 0 errors/0 warnings; both individual Short schema/source validations PASS; `episodeShortsProblems=[]`; `npm run test:docs-videos` 236/236 PASS; `npm run check:tasks` exit 0 with unrelated pre-existing stale-claim/scope warnings; `git diff --check` clean. Exact v3 still requires another agent’s line/card/Shorts/source audit and two new independent first-blind story reviews. True TTS duration may fall short despite the paper estimate; do not buy media before the review gates and budget recheck.
