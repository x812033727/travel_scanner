---
id: 2026-10-03-drama-design-documents-say-what-the
title: Drama design documents say what the code does: shot length norms, the still-move reader, pan direction, exit codes
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T11:20:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/DRAMA.md
  - docs/videos/BINGE.md
  - .agents/skills/youtube-video/references/drama-craft.md
  - .agents/skills/youtube-video/references/visual-quality.md
  - .agents/skills/youtube-video/references/animation-production.md
---

# Drama design documents say what the code does: shot length norms, the still-move reader, pan direction, exit codes

## Why

While the `animation-camera` and `animation-production` skills were written (2026-10-03),
five readers mapped the drama documents against the code and found sentences the code has
left behind. The skills state the code's truth and point at the documents, so the documents
should stop contradicting them:

1. `docs/videos/DRAMA.md` §設計 still says 「每鏡 3–8 秒、每分鐘 5–8 張關鍵影格、八成硬切」
   and prices a 3-minute episode as 30 shots × 6 s; the measured craft spec
   (`drama-craft.md`) targets a 2.5–3.5 s median, which is 50–70 shots for 3 minutes.
2. `docs/videos/BINGE.md` §畫面等級 says `motionMove` 「先看 camera 再看 motion」; since
   2026-10-03 it reads `camera` only, and `locked` holds the still (PSNR-checked).
3. `docs/videos/DRAMA.md` §資料模型 says `duration_s = clamp(ceil(frames/30), 4, 10)`;
   under a `veo-3.1*` model `clips.mjs` buys a fixed 8 s.
4. `drama-craft.md` §二 and §五 and `visual-quality.md` §2 (the hand-insert paragraph) and
   `animation-production.md` (the Lite contract) could point at the two new skills where
   they now hold the fuller rule (axis and eyelines, the three readers' keyword tables,
   the routes and their prices).
5. `docs/videos/DRAMA.md` §供應商 lists 14 reference images for Gemini 3 Pro Image; the
   server caps a request at `MAX_REFERENCES = 4` (`apps/api/app/video_media/schemas.py`).

The `drama.md` sentences in the skill (pan direction, PSNR on `locked`, exit code 3 for an
unapproved gate) were already fixed in the skills task; these are the files outside its scope.

## Definition of done

- [ ] Each sentence above says what the code does, with the file and constant beside it, or
      is removed; `docs/videos/DRAMA.md` keeps its history lines dated.
- [ ] The two bound skill copies of `youtube-video/SKILL.md` are not touched (duration
      receipt); `docs/videos/DRAMA.md` is not bound.

## Steps

- [ ] Fix the five places; run `node --test tools/skills.test.mjs`.

## How to verify

```bash
node --test tools/skills.test.mjs
grep -n "每鏡 3–8 秒\|先看 camera 再看 motion\|clamp(ceil(frames/30), 4, 10)\|14 張參考圖" docs/videos/DRAMA.md docs/videos/BINGE.md
```

## Notes

- Filed by the `animation-camera-and-animation-production-skills` task; the readers' maps
  that found these are summarised in that task's pull request.
