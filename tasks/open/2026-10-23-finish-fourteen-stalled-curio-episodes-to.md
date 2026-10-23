---
id: 2026-10-23-finish-fourteen-stalled-curio-episodes-to
title: Finish fourteen stalled Curio episodes to ready-to-upload with eight languages and dubs
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-curio-finish
claimed_at: 2026-10-23T18:17:11Z
created_at: 2026-10-23T18:16:48Z
completed_at:
branch: claude/suspicious-antonelli-878480
depends_on: []
scope:
  - docs/videos/history-curiosity/finish-20261024
  - docs/videos/curio-s10/video.json
  - docs/videos/curio-s12/video.json
  - docs/videos/curio-s13/video.json
  - docs/videos/curio-s15/video.json
  - docs/videos/curio-s16/video.json
  - docs/videos/curio-s17/video.json
  - docs/videos/curio-s19/video.json
  - docs/videos/curio-s20/video.json
  - docs/videos/curio-s21/video.json
  - docs/videos/curio-s24/video.json
  - docs/videos/curio-s25/video.json
  - docs/videos/curio-s27/video.json
  - docs/videos/curio-s29/video.json
  - docs/videos/curio-s31/video.json
  - docs/videos/curio-s10/i18n
  - docs/videos/curio-s12/i18n
  - docs/videos/curio-s13/i18n
  - docs/videos/curio-s15/i18n
  - docs/videos/curio-s16/i18n
  - docs/videos/curio-s17/i18n
  - docs/videos/curio-s19/i18n
  - docs/videos/curio-s20/i18n
  - docs/videos/curio-s21/i18n
  - docs/videos/curio-s24/i18n
  - docs/videos/curio-s25/i18n
  - docs/videos/curio-s27/i18n
  - docs/videos/curio-s29/i18n
  - docs/videos/curio-s31/i18n
---

# Finish fourteen stalled Curio episodes to ready-to-upload with eight languages and dubs

## Why

The owner (2026-10-24): finish the 奇聞檔案局 episodes filed under 觀念解說 that are not ready to upload, use the
recommended choices without asking, complete everything before upload, and make the dubs by default.

On /admin/videos (read 2026-10-24 with the video tool token) these fourteen have an approved audio and storyboard
(S24, S29: audio; S29 storyboard too) but no final cut, no upload package and no languages: S10 S12 S13 S15 S16 S17
S19 S20 S21 S24 S25 S27 S29 S31. They were made in Claude cloud containers (tasks `2026-10-19-curio-s-axis-*`,
`2026-10-20-curio-s-axis-*`) that are gone; the site keeps the review payloads and some media files, not the
per-line narration, timeline and keyframes that render, captions and dub need. Their scripts are on main.

Not in this ticket: S07, S32, S33, S37 and S40 (Codex's: scripts only on `codex/curio-s34-endurance-20261019`,
S40's eight languages wait on Codex's workdir, task `2026-10-21-curio-s02-s03-s04-s05-s23`); S06, S26, S38
(a re-assembly with channel intro and outro is in another session).

## Definition of done

- [ ] Each of the fourteen has an approved final cut with the channel intro after the condensation and the
  v4 end-screen outro, an upload package, and a languages review with en ja ko es pt id vi th: title and
  description, captions and dub track (or a skip with its reason).

## Steps (per episode, one at a time: the site rate-limits keyframes per token)

- [ ] Local workdir from the script on main: tts (site channel voice) → check-audio → review-push audio.
- [ ] keyframes --takes 3 (the site dedupes an identical request per slug, so prompts left as they were cost
  nothing when the old job's file is still stored) → music → review-push storyboard.
- [ ] render → clips → assemble → captions → qa → review-push final.
- [ ] package → review-push publish; i18n-sheet / translate / i18n-merge; dub all eight line by line;
  check-audio per locale; review-push languages.

## Notes

- Quota: Gemini's daily speech quota (tts and dubs share it) resets 07:00 UTC; one episode's eight dubs take
  over an hour.
