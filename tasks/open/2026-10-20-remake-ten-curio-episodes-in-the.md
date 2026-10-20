---
id: 2026-10-20-remake-ten-curio-episodes-in-the
title: Remake ten Curio episodes in the cloud and make all eight languages (S01 S09 S18 S11 S14 S06 S07 S08 S38 S39)
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-curio-remake-langs
claimed_at: 2026-10-20T15:21:04Z
created_at: 2026-10-20T15:21:00Z
completed_at:
branch: claude/hopeful-dirac-6vwu7n
depends_on: []
scope:
  - docs/videos/history-curiosity/remake-20261020
  - docs/videos/curio-s01/video.json
  - docs/videos/curio-s01/i18n
  - docs/videos/curio-s09/video.json
  - docs/videos/curio-s09/i18n
  - docs/videos/curio-s18/video.json
  - docs/videos/curio-s18/i18n
  - docs/videos/curio-s11/video.json
  - docs/videos/curio-s11/i18n
  - docs/videos/curio-s14/video.json
  - docs/videos/curio-s14/i18n
---

# Remake ten Curio episodes in the cloud and make all eight languages (S01 S09 S18 S11 S14 S06 S07 S08 S38 S39)

## Why

The owner (2026-10-20) asked for these ten 奇聞檔案局 episodes to be finished, with all eight languages
(en, ja, ko, es, pt, id, vi, th; title and description, CC and dub). On the site S01, S09 and S18 have an approved
final and all eight languages ticked, but every part has sat at "working" since 2026-10-19 17:30: the cloud
container that made them (session_011THWxsqrx66wg1ayBDAj5z) is unreachable, and the site keeps only a preview,
the narration MP3 and a contact sheet, not the per-line audio, timeline and keyframes that `dub`, `captions` and
`package` need. S11 and S14 stopped at audio and storyboard approval in that same container. S06, S07, S08, S38
and S39 stopped at audio approval in Codex's environment (PR #1598). The owner chose to remake all ten here
rather than wait for the original workdirs (option 2), and approved an imagery and music cap of US$36.

## Definition of done

- [ ] Each of the ten has a new narration, illustrations, music, final cut and upload package, each gate approved by the owner on /admin/videos.
- [ ] Each of the ten has the eight languages (metadata, captions, dub) in a languages batch, or a skip with its reason.
- [ ] Spend stays under US$36 for images and music; the actual figure per episode is written here.

## Steps

- [ ] tts → check-audio → review-push audio, for all ten.
- [ ] keyframes --takes 3 per episode → review-push storyboard.
- [ ] music → render → clips → assemble → captions → qa → review-push final.
- [ ] package; languages (the owner ticks the panel for the seven not yet ticked).

## How to verify

`node tools/video/cli.mjs status --slug curio-sNN` for each, and the video's page on /admin/videos.

## Notes

- Scripts: S01, S09, S18, S11, S14 from main; S06, S07, S08, S38, S39 from Codex's branch
  `codex/curio-s34-endurance-20261019` (the versions whose audio the site approved), copied into a scratch
  worktree of main. Codex was asked (through the owner) to stop these five so the two do not both push reviews.
- Quote at 3 takes: S01 3.44, S09 3.24, S18 3.00, S11 3.08, S14 3.44, S06 3.24, S07 3.48, S08 3.52, S38 4.50,
  S39 3.48 = US$34.42; music about US$1-1.5. Codex's three-image S07 pilot failed 0/3 with the same prompts.
- 2026-10-20 progress (claude-opus-5-5-curio-remake-langs, cloud container, workdir /root/mokaair-work/videos):
  - Narration re-recorded for all ten (site Gemini, free tier). check-audio + up to three targeted redo rounds;
    what is left flagged is transcriber homophones on names (今川/京川, 牛一/扭一, 樊城/返城). S14 mu323 cannot be
    transcribed (Gemini PROHIBITED_CONTENT); S38 check still running. Audio pushed for S01 S06 S07 S08 S09 S11 S14 S18 S39.
  - Keyframes: one episode at a time. The video tool token is limited to 240 image submits, 900 polls and 360 judge
    calls an hour (apps/api/app/video_media/admin_api.py); four episodes at once got HTTP 429 within minutes.
    S01 85 shots US$1.62 (5 prompts rewritten), S09 80 US$1.76 (5), S18 74 US$1.59 (8), S11 76 US$1.28 (1 left).
    Failures were empty scenes, hands and objects; "one person doing one thing" passed on the first rerun every time.
  - Music: S01, S09, S18. Storyboards pushed: S01, S09, S18. clips stop until the owner approves the storyboard.
  - Translations: nine subagents filled i18n-sheet worksheets for en ja ko es pt id vi th; merged with i18n-merge.
    i18n-merge rejects Han characters in Latin/Thai descriptions (S09 我自刊我書, S14 the leaflet quote): reworded.
    S06 S07 S08 S39 translations follow Codex's scripts (branch codex/curio-s34-endurance-20261019), so they are kept
    under docs/videos/history-curiosity/remake-20261020/<slug>/i18n until those scripts reach main.
  - Container Chromium is older than Playwright 1.64 wants: symlink /opt/pw-browsers headless_shell into a
    PLAYWRIGHT_BROWSERS_PATH as chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell.

