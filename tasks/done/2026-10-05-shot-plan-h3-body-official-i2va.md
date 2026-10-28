---
id: 2026-10-05-shot-plan-h3-body-official-i2va
title: shot_plan.mjs H3 body follows the official I2VA structure
status: done
priority: P3
area: tools
owner: claude-fable-5.1
claimed_at: 2026-10-28T06:49:39Z
created_at: 2026-10-05T16:41:00Z
completed_at: 2026-10-28T06:58:11Z
branch:
depends_on:
  - 2026-10-05-delivery-promise-and-continuity-locks
scope:
  - .agents/skills/animation-preproduction/scripts/shot_plan.mjs
  - tools/animation-preproduction.test.mjs
  - .agents/skills/animation-preproduction/references/route-decisions.md
---

# shot_plan.mjs H3 body follows the official I2VA structure

## Why

`2026-10-05-animation-skill-references-prompt-facts` compared `H3_FIRST_LINE` and the H3 web
body that `shot_plan.mjs --route hailuo --hailuo-model h3` writes against MiniMax's official
prompt guides (the Hugging Face `VIDEO_PROMPT_WRITING_GUIDE_base_en.md`, model card updated
2026-08-13, and the official `MiniMax-AI/MiniMax-H3` skill `h3-prompt-writing`, both read
2026-10-05). The first line and the three fields match verbatim; the body inside `[Shot 1]`
does not. The findings are in `.agents/skills/animation-camera/references/model-misreads.md`
section six. They were out of that ticket's scope (docs only), so they are filed here for the
owner of the script.

## Definition of done

- [x] `[Shot 1]` opens with an official style word (mapped from the look preset: `anime-2d` →
      `2D-animated`, `cinematic-3d` → `3D CG`, `ink-wash` → `watercolor` or the nearest, …) and an
      anchor sentence that cites `<Picture 1>` and keeps the first frame's composition, identities,
      costumes and props; the motion follows it. Today `WEB_KEEP` sits at the end and never names
      `<Picture 1>`.
- [x] Camera sentences use only the official speed words: `at slow speed` / `at fast speed`;
      a move that is neither slow nor fast carries no speed (`at a steady speed` is not in the
      official table, and "medium amplitude and normal speed are usually omitted").
- [x] A shot planned with an end frame writes the FL2VA alignment line (`How the reference
      pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second
      mark …; Picture 2 (from Shot 1) aligns with the S.SS-second mark …`, two decimals, the
      bought seconds) instead of the I2VA line.
- [x] The three fields are separated by a blank line, as every official example is (or the
      pilot shows it makes no difference, written down).
- [x] `route-decisions.md` section six shows the new body; `tools/animation-preproduction.test.mjs`
      pins the first line, the style word, the anchor sentence and the speed words.

## Steps

- [x] Read `model-misreads.md` section six and the official base guide once more; the pilot
      ticket `2026-10-04-paid-verification-hailuo-kling-web` decides the two unverified lines
      (`N/A` sound fields, the `no on-screen text` negation).
- [x] Change `webPrompt` and `webMove` in `shot_plan.mjs`, update the test and the reference.

## How to verify

```bash
node --test tools/animation-preproduction.test.mjs tools/skills.test.mjs
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs --route hailuo --hailuo-model h3 <episode>
```

## Notes

- Depends on `2026-10-05-delivery-promise-and-continuity-locks`, which holds `shot_plan.mjs`
  in its scope; take this one after it lands.
- Keep `sha256` of the body as the lock's identity: changing the body re-locks every H3 shot,
  so do it before a batch, not between its phases.

### 2026-10-28: findings from `2026-10-28-h3-motion-quality-smooth-clips` for whoever takes this

The H3 motion manual (`.agents/skills/minimax-h3-colab/references/motion-quality.md`, sources with
read dates) adds to the list above, all out of that ticket's scope and belonging to `webPrompt`:

- `locked` must stay a real hold: `The camera holds a static shot` (H3 drifts by default; fuser.studio
  2026-10-28). `H3_SENTENCE.locked` already says still; keep it, never rewrite it into a push.
- Speed words only from the official pair (`at slow speed` / `at fast speed`), amplitude only
  `small` / `large`; drop `at a steady speed`.
- One camera move per clip; never join two with `then` (three `then`s produced two cuts in fuser's
  test) and never `[Shot 2]`.
- The anchor sentence should name the people (`Xu Yan shown in <Picture 1> keeps the same face,
  hair, costume and props as the first frame; the set layout stays as it is.`) rather than the generic
  `WEB_KEEP`; `gen-dh.mjs` in `docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/` now
  writes that form and is a worked example.
- Plan seconds: `shot_plan.mjs` should not let an H3 shot be bought at 4 s (107 frames, under the
  124–362 trained range); 5 s is the floor, 6 s for on-screen speech or two beats.

### 2026-10-28：做了什麼（claude-fable-5.1）

- `webMove`：`locked` → `The camera holds a static shot`；速度詞只剩 `with small amplitude at slow speed`／`with large amplitude at fast speed`（fast／quick／whip／snap），不慢不快不寫；回傳多一個 `fast`。
- `webPrompt`（H3）：`[Shot 1] <風格詞>. <錨句> <motion>. <運鏡句>. <look.motion>. One continuous shot.`；`h3StyleWord(look)` 由預設集名或 custom 的 style 字對官方表，對不到記 note；`h3Anchor(cast)` 點名 `<Picture 1>` 裡的人（拉丁名字才寫）；有 `end_frame` 且知道秒數（`webPrompt` 新的 `seconds` 選項，`planEpisode` 傳 `buy_s`）時第一行換成 `h3AlignLine(seconds)`；`WEB_KEEP` 只剩 Hailuo 2.3 與 Kling 用。三欄之間仍單一換行：2026-10-28 Colab 小樣三支這樣送都成，先不改。
- 秒數：`HAILUO_MODELS.h3.seconds` 下限 `H3_MIN_SECONDS` 5；`on_screen_speech`（旁白不算）或 `two_beats`（then／after that／分號）時下限 `H3_TALK_SECONDS` 6，兩個旗標寫在 plan 的每鏡上；`twoBeats` 匯出，motion 有兩拍時正文記 note。
- 修仙第 1 集實測：42 支從 169 秒變 238 秒（28 支 6 秒、14 支 5 秒）。
- 沒做：風格詞對不到的 look 只記 note 不擋；`overall_soundscape` 仍 `N/A`（產線丟音軌）。
