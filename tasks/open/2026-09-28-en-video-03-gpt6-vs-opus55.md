---
id: 2026-09-28-en-video-03-gpt6-vs-opus55
title: Produce EN video 03: GPT-6 Astra vs Claude Opus 5.5 vs Gemini, which is worth paying for
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:48:21Z
created_at: 2026-09-28T02:47:48Z
completed_at:
branch: claude/ai-video-planning-l43qas
depends_on:
  - 2026-09-28-video-english-narration-locale
scope:
  - docs/videos/gpt6-vs-opus55-worth-paying
---

# Produce EN video 03: GPT-6 Astra vs Claude Opus 5.5 vs Gemini, which is worth paying for

## Why

Third of the three English videos the owner chose on 2026-09-28 (season plan `docs/ai-video-en-season-01/README.md`, brief `briefs/03-gpt6-vs-opus55-worth-paying.md`): the same three monthly jobs priced on GPT-6 Astra, GPT-6 Sol, Claude Opus 5.5, Grok 4.7 and Gemini 3.8 Flash from the vendors' own pages, then the three-question test. Prices expire: the title carries the month and every line is re-checked on recording day.

## Definition of done

- [x] `docs/videos/gpt6-vs-opus55-worth-paying/` has `brief.md` (eight sections, `套用立場：1、2、6`), `video.json` (`narration_locale: en`), `claims.md` with every calculation spelled out; lint 0 errors.
- [x] `verify-1.md` (55 claims; 8 changes: cache writes replace the input price, so job 2 became Astra $348, Sol $70, Opus 5.5 $130) and `verify-2.md` (23 rows, 0 changes) by two independent agents; the $12.50 column is confirmed as the cache-write price.
- [x] Listener review applied (14 lines); lint 0 errors, 1 warning (hook about 37 s by the estimator); slides render with no layout problem.
- [ ] Gates approved; owner uploads private; `scoreboard.csv` rows filled.

## Steps

- [x] Prices read 2026-09-28: platform.openai.com/docs/pricing and the GPT-6 Astra model page (200 with the editorial user agent), anthropic.com, docs.x.ai, ai.google.dev.
- [x] Script written (50 lines, about 8.1 min estimated); verified twice; listener review done.
- [ ] Re-open every price on recording day; then the pipeline steps on the owner's machine or the host worker.

## How to verify

```bash
node tools/video/cli.mjs lint --slug gpt6-vs-opus55-worth-paying
node tools/video/cli.mjs status --slug gpt6-vs-opus55-worth-paying --workdir <VIDEO_WORKDIR>
```

## Notes

- openai.com/api/pricing/ and the Astra launch page answer HTTP 403 to the editorial user agent; platform.openai.com/docs/pricing does not, and its table rows are embedded as JSON (["gpt-6-astra"],[10],[1],[12.5],[50]).
- Google's page lists no Pro model of the 3.8 generation on 2026-09-28; Gemini is represented by 3.8 Flash and the narration says so.
- Gemini 3.8 Flash's price doubles on 2027-01-01 per the page; the video must be re-checked before any re-upload after that date.
