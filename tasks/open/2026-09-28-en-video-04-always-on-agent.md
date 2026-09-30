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
- [x] On or after 2026-09-29: the `always-on` scene (line xc6d and its fourth bullet) updated with what DevDay actually announced, before TTS.
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
- 2026-09-29 19:30 UTC (claude-opus-5-5): DevDay announced **dots**, OpenAI's always-on agent (developers.openai.com/codex/dots: "an always-on agent", powered by GPT-6 Astra, "lives in the cloud and has its own computer and browser", "can keep working even when your computer is off"; rolling out gradually to Pro 100/200/500 outside the EEA, UK and Switzerland, and to Business Premium and Enterprise). The same day's developer changelog adds computer use to the Agents API, GPT-6.1 Sol and GPT-6 Astra Ultrafast. Changed: hx5y (「OpenAI 更在 DevDay 上，發表了永遠不下線的那種」), xc6d (dots, its own cloud computer, keeps working after you shut down), the fourth bullet, xc5x and the `always-on-loop` title (「不管哪一家推出」), the description's closing sentences, a new `sources` row and the tag "OpenAI dots"; en, ja, ko and zh-CN re-merged for those lines and fields; claims c5 rewritten; `dots` added to the lexicon as null. Lint 0 errors, 2 warnings (hook estimate 32 s, which recorded at 28.2 s before the change; total 7.1 min). The Agents API's computer use and GPT-6.1 Sol are not in the script. Verify round 3 (a separate verifier agent, `verify-3.md`, 37 rows): 0 fact changes; OpenAI's dated "DevDay 2026" page (developers.openai.com/codex/whats-new/devday-2026) lists "Meet your dot"; its source and bookkeeping fixes (R1–R4) and three wording options (ja xc6d, shorter ja/ko hx5y, a full-sentence zh-TW description) applied; c3 still has no official GPT-6 Astra OSWorld figure. ja rcus, wvpe and ko eyuh, dduj, txqe, wvpe shortened to fit their dub windows (the pre-dub overruns of 2026-09-28). Next: tts for the three changed lines, check-audio, render, the audio gate, then the en/ja/ko dubs.
- 2026-09-29 20:15 UTC (claude-opus-5-5): hx5y, xc6d and xc5x re-recorded (152 characters; narration 6:39); check-audio 0 flags with the Whisper second opinion (it also cleared the two 9/28 false flags); the audio gate was auto-approved. Rendered (no layout problem; the longest slide state 12.2 s; hook chapter 29.0 s); assembled (11,982 frames, -14 LUFS). Dubs: en 0 flags; ja p7nm, 5dmh, uf2w reworded and prkk put in kanji; ko hx5y, eyuh trimmed to fit, eyuh says 모델 세 개 (세 and 새 sound alike) and zf6x reworded; all three dubs 0 flags. Captions for five locales (ko cue 83 at 13.4 characters a second is a warning). qa 9 of 11: links (openai.com/index/gpt-6-astra/ answers 403 to the checker) and policy (channel stance blank) are the season-wide known items. Final gate submitted 20:11 UTC (final.mp4 141c98d543b0); after the owner approves: review-pull, package, review-push --gate publish and --gate dubs.
- 2026-09-29 20:38 UTC (claude-opus-5-5): the owner approved the final cut at 20:37; packaged (4 of 4 package checks, metadata.json ee06c0e888e3); the publish card was auto-approved; the dubs card (en, ja, ko) waits for the owner. What is left is the owner's: approve the dubs card, upload private from `upload/` following UPLOAD.md, add the three dub tracks in Studio, paste the URL on the 可以上架 card; proposed date 2026-10-13 (`schedule.csv`).
