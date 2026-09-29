---
id: 2026-09-28-en-video-04-always-on-agent
title: Produce EN video 04: how an AI agent actually works, always-on agents explained
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
  - docs/videos/always-on-agent-explained
---

# Produce EN video 04: how an AI agent actually works, always-on agents explained

## Why

Second of the three English videos the owner chose on 2026-09-28 (season plan `docs/ai-video-en-season-01/README.md`, brief `briefs/02-always-on-agent-explained.md`): what an AI agent actually does between the request and the result, told through one real recorded run, with the makers' own computer-use numbers for where agents still fail. DevDay (2026-09-29) had not happened on writing day, so the script uses the brief's fallback hook and labels OpenAI's always-on assistant as a report.

## Definition of done

- [x] `docs/videos/always-on-agent-explained/` has `brief.md` (eight sections, `套用立場：3、4、5`), `video.json` (`narration_locale: en`), `claims.md`, `demo-log.md`; lint 0 errors.
- [x] `verify-1.md` (66 rows, 4 fact changes) and `verify-2.md` (50 rows, 0 changes) written by two independent agents; listener review applied (20 lines); lint 0 errors, 1 warning (hook about 42 s by the estimator, about 32 s at the voice's pace); slides render with no layout problem.
- [ ] On or after 2026-09-29: the `always-on` scene (line xc6d and its fourth bullet) updated with what DevDay actually announced, before TTS.
- [ ] Outline, audio, final and publish gates approved; owner uploads private; `scoreboard.csv` rows filled at 48 h, 7 d, 28 d.

## Steps

- [x] Real run recorded 2026-09-28 (Claude Code 2.1.283, tools WebFetch and Write): three fetches, one HTTP 403, one file, two-sentence report; `demo-log.md`.
- [x] Script written (53 lines, about 8.4 min estimated) with the run as chapter 3; verified twice; listener review done.
- [ ] After DevDay: re-check the always-on chapter; then tts → check-audio → render → assemble → captions → qa → package, on the owner's machine or the host worker (needs the video-tool token).

## How to verify

```bash
node tools/video/cli.mjs lint --slug always-on-agent-explained
node tools/video/cli.mjs status --slug always-on-agent-explained --workdir <VIDEO_WORKDIR>
```

## Notes

- GPT-6 Astra's OSWorld 2.0 figure is not spoken or shown: openai.com's launch page answers HTTP 403 to the editorial user agent and the official system card (deploymentsafety.openai.com) does not carry it. The stats card shows Anthropic's 81.8% partial only.
- This video assumes video 1 (`openai-agents-broke-in`) is public first: two lines refer to last week's headlines and the closing points forward to video 3.

- 2026-09-28（站主決定）：影片是繁中影片（繁中旁白與投影片），英文字幕之外，另做英文、日文、韓文三條配音音軌（`dub --locale en,ja,ko`，`docs/videos/DUBS.md`）；站主在 Studio「語言」頁上傳。前提：頻道已開通進階功能，且關掉「允許自動配音」。
- 2026-09-28 (claude-opus-5-5): zh-TW narration recorded (6:28) and checked (2 flags left, both transcriber errors per Whisper; `say` fixes for 動作四 → 第四個動作 and 上週上新聞 → 上個禮拜); re-paced to 27 scenes, longest state under 15 s; caption reviews applied in en, ja, ko, zh-CN (15, 23, 21, 16 fixes). Not done yet, on purpose: hx5y, xc6d and the always-on slide's fourth bullet wait for DevDay (2026-09-29) in zh-TW and all four translations, then re-record only those lines; dubs wait for the Gemini month to reset (8,106 characters left on 2026-09-28; dubs cost about 11,000 with `--line-by-line`).
- 2026-09-28 17:30 UTC: the site's Gemini limit went from 300,000 to 5,000,000 characters a month around 15:00 UTC, so the dubs no longer wait for 2026-10-01; they can follow the DevDay update directly. The lexicon terms added for videos 5 and 6 mark this timeline stale (`tasks/open/2026-09-28-speechhash-hashes-the-whole-lexicon-so.md`), but `tts --dry-run` shows 0 lines to re-record. Watch zdw7's 403 in the ja and ko dubs: on video 5 both voices read 4050 as 450, dropping the inner zero.
