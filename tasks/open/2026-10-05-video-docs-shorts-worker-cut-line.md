---
id: 2026-10-05-video-docs-shorts-worker-cut-line
title: Video docs: shorts worker cut line and drama burn-in default are stale
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T14:39:34Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/README.md
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/shorts.md
---

# Video docs: shorts worker cut line and drama burn-in default are stale

## Why

Two places where the video docs say the opposite of what the code does, found while
surveying the video tooling on 2026-10-05:

- `.agents/skills/youtube-video/references/shorts.md` (table row 「長片精華」) and
  `docs/videos/AUTOMATION.md` (section 「還沒有的」) both say the worker's highlight
  line is not built yet and point at ticket `2026-09-28-video-shorts-worker-cut`. That
  ticket is in `tasks/done/`, and `tools/video/automation/shorts.mjs` declares
  `MAKES = ["lab", "cut"]` with `shorts/cut.mjs` wired in. Only the vertical drama line
  (`2026-09-28-video-shorts-worker-drama`) is still missing.
- `docs/videos/README.md` (opening paragraph and the 「字幕」 row) says drama videos
  burn the zh-TW subtitles into the picture by default. `tools/video/core/drama.mjs`
  `resolveSubtitles` defaults `burn_in` to `false`, and `docs/videos/DRAMA.md` plus
  `references/animation-production.md` say the new automated route is CC only.

Anyone starting from the skill or the README plans around capabilities that are wrong.

## Definition of done

- [ ] `shorts.md` and `AUTOMATION.md` describe the worker's `cut` line as built, with the
      drama vertical line as the only missing one.
- [ ] `docs/videos/README.md` says drama subtitles are CC by default (`burn_in: false`),
      with burn-in only for old approved files that set it explicitly.
- [ ] No other sentence in those three files contradicts `tools/video/automation/shorts.mjs`
      or `tools/video/core/drama.mjs`.

## Steps

- [ ] Fix the two sentences in `shorts.md` and the 「還沒有的」 bullet in `AUTOMATION.md`.
- [ ] Fix the opening paragraph and the 「字幕」 table row in `docs/videos/README.md`.
- [ ] Re-read `docs/videos/SHORTS.md` for the same claim and fix it if present.

## How to verify

```bash
grep -n "worker-cut" .agents/skills/youtube-video/references/shorts.md docs/videos/AUTOMATION.md
grep -n "燒" docs/videos/README.md
npm run test:tools   # keeps .agents/skills and .claude/skills in step
npm run check:tasks
```

## Notes

- Filed from a research session on outside video tooling; no code changed.
- The `.claude/skills/youtube-video/SKILL.md` copy only mirrors `SKILL.md`, so editing
  `references/shorts.md` under `.agents/skills` needs no second copy.
