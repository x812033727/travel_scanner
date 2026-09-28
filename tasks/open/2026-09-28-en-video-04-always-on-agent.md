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
- [ ] `verify-1.md` written by an independent agent; listener review applied; lint still 0 errors.
- [ ] On or after 2026-09-29: the `always-on` scene (line xc6d and its fourth bullet) updated with what DevDay actually announced, before TTS.
- [ ] Outline, audio, final and publish gates approved; owner uploads private; `scoreboard.csv` rows filled at 48 h, 7 d, 28 d.

## Steps

- [x] Real run recorded 2026-09-28 (Claude Code 2.1.283, tools WebFetch and Write): three fetches, one HTTP 403, one file, two-sentence report; `demo-log.md`.
- [x] Script written (53 lines, about 8.6 min estimated) with the run as chapters 3; verifier round 1 dispatched.
- [ ] After DevDay: re-check the always-on chapter; then tts → check-audio → render → assemble → captions → qa → package, on the owner's machine or the host worker (needs the video-tool token).

## How to verify

```bash
node tools/video/cli.mjs lint --slug always-on-agent-explained
node tools/video/cli.mjs status --slug always-on-agent-explained --workdir <VIDEO_WORKDIR>
```

## Notes

- GPT-6 Astra's OSWorld 2.0 figure is not spoken or shown: openai.com's launch page answers HTTP 403 to the editorial user agent and the official system card (deploymentsafety.openai.com) does not carry it. The stats card shows Anthropic's 81.8% partial only.
- This video assumes video 1 (`openai-agents-broke-in`) is public first: two lines refer to last week's headlines and the closing points forward to video 3.
