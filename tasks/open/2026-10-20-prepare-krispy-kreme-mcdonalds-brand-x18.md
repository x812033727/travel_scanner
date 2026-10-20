---
id: 2026-10-20-prepare-krispy-kreme-mcdonalds-brand-x18
title: Prepare Krispy Kreme McDonald’s brand-story X18
status: in-progress
priority: P2
area: docs
owner: x18-brand-author
claimed_at: 2026-10-20T22:40:38Z
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
- [ ] Obtain independent source and narrative review on this frozen version; fix any HOLD findings, rebuild and review new SHA.

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
