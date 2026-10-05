---
id: 2026-09-28-en-video-02-ai-real-jobs
title: Produce EN video 02: AI can now do 21% of real freelance jobs (Remote Labor Index curve)
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T04:40:55Z
completed_at:
branch: claude/ai-video-planning-l43qas
depends_on:
  - 2026-09-28-video-english-narration-locale
scope:
  - docs/videos/ai-real-jobs-chart
---

# Produce EN video 02: AI can now do 21% of real freelance jobs (Remote Labor Index curve)

## Why

Fourth season video the owner chose (outline A, 2026-09-28): the Remote Labor Index curve from 2.5% to about 21% of real paid freelance projects in eleven months, why companies still cite AI in layoffs, and a three-question test on one real O*NET job. zh-TW master with CC in zh-TW, zh-CN, ja, ko, en and dub tracks in en, ja, ko.

## Definition of done

- [x] `docs/videos/ai-real-jobs-chart/`: brief (outline A approved), zh-TW `video.json`, `claims.md`, `verify-1.md`, `verify-2.md`; translations en (verified English), ja, ko, zh-CN, each reviewed by a second model and fixed.
- [x] Narration recorded and checked; the owner approved the audio gate; 26 scenes with no state over 15 s; render and assemble clean; dubs en/ja/ko fit and checked; `qa` 10/11 (policy: channel stance blank).
- [ ] Final, publish and dubs gates approved; the owner uploads private; `scoreboard.csv` rows filled.

## Steps

- [x] Converted from the English script to zh-TW with the same line ids; the demo table split in two so all eight rows fit.
- [x] `say` for percents (百分之…) and Claude 的 Fable: the voice read % three different ways and dropped Fable after Claude.
- [x] `review-push --gate final` (pending the owner, 2026-09-28).
- [x] `package` (4/4) → publish gate (auto-approved) → dubs gate sent (waiting for the owner).

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-real-jobs-chart
node tools/video/cli.mjs status --slug ai-real-jobs-chart --workdir <VIDEO_WORKDIR>
```

## Notes

- 2026-09-28 (claude-opus-5-5), what the production taught:
  - The site's Gemini transcriber in `check-audio` pulls text toward what it knows (Gemini 3.8 → 1.5, 2026 → 2023, Grok 4.7 → 視覺, even memorised old prices). A local Whisper (faster-whisper medium/large-v3) settles each flag for free; filed as `2026-09-28-check-audio-gemini-transcriber-rewrites-unfamiliar`.
  - `check-audio` transcription is billed against the same Gemini month: about 2,000 characters a dub track. Check once, then Whisper.
  - Scene-whole dub requests mis-split without falling back: clips shifted by one line (heard as lines "spoken" at 0.4–0.6x the track's rate). Dub with `--line-by-line` (added the same day).
  - Slides were re-paced so no state stays over 15 s (QA `pace`); line ids and texts did not change, so narration and translations stayed valid.
  - O*NET content is CC BY 4.0; every caption locale's description says the tasks were shortened and translated.

- 2026-09-28（站主決定）：影片是繁中影片（繁中旁白與投影片），英文字幕之外，另做英文、日文、韓文三條配音音軌（`dub --locale en,ja,ko`，`docs/videos/DUBS.md`）；站主在 Studio「語言」頁上傳。前提：頻道已開通進階功能，且關掉「允許自動配音」。
- 2026-09-28 09:47 UTC: final approved by the owner on /admin/videos (and recorded from the chat, same hash); `package` 4/4; publish gate auto-approved (「可以上架」); dubs gate sent with en, ja, ko and waiting for the owner to upload the tracks in Studio's Languages page and approve it. Left for the owner: upload private per `upload/UPLOAD.md`, paste the YouTube URL and publish time on the card, then fill `scoreboard.csv` at 48 h, 7 d and 28 d.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus-5-5 (since 2026-09-28T04:41:07Z) was stale and is released so it stops locking its scope. Landed: #968. Still open: Final, publish and dubs gates approved; owner uploads private; scoreboard.csv rows filled.
