---
id: 2026-10-20-tutorial-flow-and-hooks-rules-learned
title: Tutorial flow and hooks: rules learned from two reference videos
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-20T17:25:00Z
created_at: 2026-10-20T17:21:40Z
completed_at:
branch: claude/ai-video-production-520ea2
depends_on: []
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - docs/videos/reference-study-20261021
---

# Tutorial flow and hooks: rules learned from two reference videos

## Why

The owner (2026-10-21) set two popular tutorials as the target for the channel's AI videos:
Gary Chen's Codex beginner guide (`xFPiU5sit7g`, 479,000 views) and 俗說 AI's Skill explainer
(`s0jRepBGI6s`, 58,000 views in six days on a 3,570-subscriber channel). Beyond copying their look,
the owner asked how their content flows and hooks, with the same teaching value, so that viewers
cannot tell the video was machine-made, and asked for the answer as a skill or rules.

A blind reader scoring both transcripts against the channel's 13-question storytelling panel found
the panel would reject both (10 and 8 of 12 required questions answered no): the panel was written
for history and event stories, and a tutorial moves by other means (a voiced viewer objection, a
promise sentence, the running example's progress at every chapter opening, a narrator who is
present with numbers and admitted uncertainty).

## Definition of done

- [x] The study with both videos' beat-by-beat structure and the blind reader's measurements is in
      `docs/videos/reference-study-20261021/README.md` (transcripts stay out of the public repo).
- [x] The rules are a skill reference (`references/teaching-flow.md`), a SKILL.md rule (13), and a
      pointer in `script-writing.md`; the planner and writer prompts read them for a tutorial.
- [x] The worker carries them (`register.mjs` `TEACHING_FLOW_RULES`, in the slides planner, writer
      and listener after `TEACHING_RULES`).
- [x] The narrative panel has a tutorial wording (`TUTORIAL_PANEL_QUESTIONS`, same ids and required
      flags, chosen by `category: "tutorial"`), a voiced objection counts as an open loop, a chapter
      opener that carries the example's state or the viewer's question is not a label, and lint lets
      a tutorial's one promise sentence through while still warning on sections and ordinals.
- [x] Tests for each of those in the three test files; `node --test tools/video` and
      `npm run test:tools` green.
- [ ] The first video written under the rules passes the tutorial panel and the owner's review.

## Steps

- [x] Fetch both transcripts (Codex: yt-dlp subtitles; Skill: no subtitles, local faster-whisper).
- [x] Blind panel on both by an independent agent.
- [x] Write the study, the reference, the worker rules, the panel variant, the lint exemption, tests.
- [ ] Produce the first tutorial under the rules (separate ticket per video).

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/core/lint.test.mjs tools/video/automation/prompts.test.mjs
npm run test:tools
```

## Notes

- Reading a reference video: YouTube's innertube and transcript panel refuse a signed-out browser
  (400 / LOGIN_REQUIRED); `python -m yt_dlp --skip-download --write-subs --sub-langs zh-TW` gets
  uploader captions; a video with none needs its audio and a local `faster-whisper` (small, int8,
  about 4 minutes for 7 minutes of audio; decode with ffmpeg to 16 kHz PCM first because PyAV's
  `metadata_errors` argument breaks on the installed PyAV).
- What the panel still rightly catches in the two hits: a detour that sells another video, a body
  sentence that retells the opening, the same list read three times, an empty label opener, a
  triple ask at the close.
- Not done, for other tickets: a per-slide key-sentence bar like 俗說 AI's; title and thumbnail
  patterns of the two hits (「還有人不會嗎？」「非技術人員也能上手」) in `publish.md`.
