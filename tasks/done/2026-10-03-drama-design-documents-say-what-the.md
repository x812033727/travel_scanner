---
id: 2026-10-03-drama-design-documents-say-what-the
title: Drama design documents say what the code does: shot length norms, the still-move reader, pan direction, exit codes
status: done
priority: P3
area: docs
owner: claude-opus-5-5-drama-docs-truth
claimed_at: 2026-10-04T14:50:15Z
created_at: 2026-10-03T11:20:00Z
completed_at: 2026-10-04T15:15:30Z
branch: claude/drama-docs-say-what-code-does
depends_on: []
scope:
  - docs/videos/DRAMA.md
  - docs/videos/BINGE.md
  - .agents/skills/youtube-video/references/drama-craft.md
  - .agents/skills/youtube-video/references/visual-quality.md
  - .agents/skills/youtube-video/references/animation-production.md
  - .claude/skills/youtube-video/references/animation-production.md
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

- [x] Each sentence above says what the code does, with the file and constant beside it, or
      is removed; `docs/videos/DRAMA.md` keeps its history lines dated.
- [x] The two bound skill copies of `youtube-video/SKILL.md` are not touched (duration
      receipt); `docs/videos/DRAMA.md` is not bound.

## Steps

- [x] Fix the five places; run `node --test tools/skills.test.mjs`.

## How to verify

```bash
node --test tools/skills.test.mjs
grep -n "每鏡 3–8 秒\|先看 camera 再看 motion\|clamp(ceil(frames/30), 4, 10)\|14 張參考圖" docs/videos/DRAMA.md docs/videos/BINGE.md
```

## Notes

- Filed by the `animation-camera-and-animation-production-skills` task; the readers' maps
  that found these are summarised in that task's pull request.
- 2026-10-04, claude-opus-5-5-drama-docs-truth. Claimed with `--force`: the overlap was
  `2026-10-03-illustrated-slides-round-2-a-family` (status review, scope
  `.agents/skills/youtube-video/references`), whose work landed on origin/main as #1172
  (merged 2026-10-03T10:34Z); its two open steps are a receipt rebind and a post-deploy look,
  neither in these files.
- What changed, each beside its file and constant:
  1. `DRAMA.md` §品質目標: the shot norms are `drama-craft.md`'s (median 2.5–3.5 s, 90% ≤ 6 s,
     longest 8 s, dissolves ≤ 10%) with `craft.mjs` `TARGETS` and `drama.mjs`
     `MAX_SHOT_SECONDS`/`WARN_SHOT_SECONDS`/`MIN_MEDIAN_SHOT_SECONDS`; §供應商 and §成本與紀錄
     price 60 shots × 3 s through `clipSeconds` (Lite US$39, Omni 37, H3 32, Veo 3.1 193 per take
     with judge; keyframes about US$9) and point at the `animation-production` skill's 錢怎麼算.
     Arithmetic checked against `catalog.py` and the skill's table (60 × 0.65 / 0.61 / 0.53 /
     3.21; 60 × 0.144).
  2. `BINGE.md` §畫面等級: `motionMove` reads `camera` only (since #1170), the table gains the
     `locked` row and the explicit `drift` word, the check names `locked` with `IDENTITY_START`
     and `KEYFRAME_MIN_PSNR`. The pan-right row said the picture runs left; `zoompanExpr`
     slides the window right→left, so the picture runs right: corrected. A dated line in
     「實作與原計畫不同的地方」 records it.
  3. `DRAMA.md` §資料模型: `clipSeconds` (`veo-3.1*` at 1080p fixed 8 s; else
     `MIN_CLIP_SECONDS` 4 to `MAX_CLIP_SECONDS` 10 snapped up to the model's `durations`).
  4. Pointers: `drama-craft.md` §二 → `animation-camera` (space, `scene-coverage.md`,
     `camera-keywords.md`); §五 → `animation-production` (錢怎麼算, 三條路線, `cost-model.md`),
     plus `clipSeconds` instead of "the model's shortest length" and the source-cut limits
     (`MAX_SOURCE_CLIP_SECONDS` 10, profile 8 in `productionShotProblems`, and the bought
     seconds). `visual-quality.md` §2: listing a character on a hand insert appends its
     appearance (`shotPrompt`/`shotAppearancePrompt`) and an `identity_<id>` question that can
     fail the picture (`MIN_CRITERION` 4.0), pointing at `animation-camera`'s insert rule.
     `animation-production.md` Lite contract: `clipSeconds` 8 s, no references for Lite
     (`clips.mjs`), the profile's lint rows (`productionShotProblems`), the import refusal
     (`importClip`, exit 3), and pointers to both skills.
  5. `DRAMA.md` §供應商: references are capped at `MAX_REFERENCES = 4` (`schemas.py`;
     `keyframes.mjs` sends the last four); the model's 14 is unused.
- `DRAMA.md` keeps its history: the opening line gains a dated 2026-10-04 clause and each
  corrected sentence says what it used to say, without the old figures.
- `.claude/skills/youtube-video/references/animation-production.md` is the byte-identical copy
  of the edited file, added to scope so both stay equal.
- Not touched, read and left: `BINGE.md` §畫面等級's 成本 bullet (one 6 s Omni shot ≈ US$0.90 is
  what `clipSeconds` buys for a 6 s shot) and its §成本與吞吐 (that is `binge_quote`'s own
  arithmetic, `apps/api/app/video_automation/series.py`).
- Checks: `node --test tools/skills.test.mjs` 6/6; the How-to-verify grep finds nothing (exit 1);
  `node tools/video/long-form/cli.mjs check` PASS (none of these files is in `reviewed_files`).
