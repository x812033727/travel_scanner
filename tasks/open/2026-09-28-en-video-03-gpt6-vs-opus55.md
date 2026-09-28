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
- [x] Recorded 2026-09-28, the day the prices were read: zh-TW narration (Sulafat) → `check-audio` (3 flags left, all transcriber errors confirmed by Whisper) → the owner approved the audio on /admin/videos and chose to carry the approval over the re-pacing (clips unchanged, only scene gaps) → re-paced to 27 scenes (longest state 11.5 s) → `render` → `assemble` → caption reviews applied in 4 locales → dubs en/ja/ko fit and checked → `captions` → `qa` 10/11 → `review-push --gate final` (pending the owner).
- [x] `package` (4/4) → publish gate (auto-approved) → dubs gate sent (waiting for the owner).

## How to verify

```bash
node tools/video/cli.mjs lint --slug gpt6-vs-opus55-worth-paying
node tools/video/cli.mjs status --slug gpt6-vs-opus55-worth-paying --workdir <VIDEO_WORKDIR>
```

## Notes

- openai.com/api/pricing/ and the Astra launch page answer HTTP 403 to the editorial user agent; platform.openai.com/docs/pricing does not, and its table rows are embedded as JSON (["gpt-6-astra"],[10],[1],[12.5],[50]).
- Google's page lists no Pro model of the 3.8 generation on 2026-09-28; Gemini is represented by 3.8 Flash and the narration says so.
- Gemini 3.8 Flash's price doubles on 2027-01-01 per the page; the video must be re-checked before any re-upload after that date.

- 2026-09-28（站主決定）：影片是繁中影片（繁中旁白與投影片），英文字幕之外，另做英文、日文、韓文三條配音音軌（`dub --locale en,ja,ko`，`docs/videos/DUBS.md`）；站主在 Studio「語言」頁上傳。前提：頻道已開通進階功能，且關掉「允許自動配音」。
- 2026-09-28 (claude-opus-5-5), what the production taught:
  - The site's Gemini transcriber in `check-audio` pulls text toward what it knows (Gemini 3.8 → 1.5, 2026 → 2023, Grok 4.7 → 視覺, even memorised old prices). A local Whisper (faster-whisper medium/large-v3) settles each flag for free; filed as `2026-09-28-check-audio-gemini-transcriber-rewrites-unfamiliar`.
  - `check-audio` transcription is billed against the same Gemini month: about 2,000 characters a dub track. Check once, then Whisper.
  - Scene-whole dub requests mis-split without falling back: clips shifted by one line (heard as lines "spoken" at 0.4–0.6x the track's rate). Dub with `--line-by-line` (added the same day).
  - Slides were re-paced so no state stays over 15 s (QA `pace`); line ids and texts did not change, so narration and translations stayed valid.
  - QA: `policy` fails until the channel stance is filled in on the site.
- 2026-09-28 09:47 UTC: final approved by the owner on /admin/videos (and recorded from the chat, same hash); `package` 4/4; publish gate auto-approved (「可以上架」); dubs gate sent with en, ja, ko and waiting for the owner to upload the tracks in Studio's Languages page and approve it. Left for the owner: upload private per `upload/UPLOAD.md`, paste the YouTube URL and publish time on the card, then fill `scoreboard.csv` at 48 h, 7 d and 28 d.
