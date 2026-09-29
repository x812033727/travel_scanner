---
id: 2026-09-29-video-storytelling-prompts
title: Storytelling register and illustration prompts for planner, writer and listener, plus restyle
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:52:47Z
created_at: 2026-09-29T09:14:24Z
completed_at: 2026-09-29T10:08:47Z
branch: claude/sharp-brown-dh2x95
depends_on:
  - 2026-09-29-video-illustrated-slides-worker
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/register.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/cli.mjs
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/ILLUSTRATED.md
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/formats.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/listener-register.md
---

# Storytelling register and illustration prompts for planner, writer and listener, plus restyle

## Why

站主要說書式旁白（反常識開場、「你以為…其實…」、章末懸念、具體場景與比喻）與每 5–8 秒一張插圖；現在的 `prompts.mjs` `COMMON`（32–37 行）把頻道說成 dark slides，版型指南沒有 shot，聽眾審稿不管節奏。現有影片要能不重寫就改口吻（`restyle`）。

## Definition of done

- [x] `register.mjs`：`REGISTER_RULES`（一份文字給 planner／writer／listener 與後台常設指示）與 `STORY_VOICE_STYLE`。
- [x] `prompts.mjs`：`COMMON` 改插圖＋卡片＋說書；`TEMPLATE_GUIDE` 加 `shot`（英文提示詞 ≤1000 字、camera 詞彙、still、transition）；節奏規則 5–8 秒、share ≥ 0.5、構圖置中；writer 回 `look`、`shorts`；planner 大綱是故事節拍；listener 加節奏審稿；`VARIANT_INSTRUCTIONS` 加 `listener:register`。
- [x] `cli.mjs` `restyle --slug`：listener register 一輪→`saveAndLint`→`verified=false`，不動 `brief.md`，line id 不變。
- [x] skill references：`script-writing.md` 說書式一節、`writer-video.md`、`planner.md`、`listener-register.md`（新）、`formats.md`。
- [x] `instructionsFor('writer','drama')` 與 explainer 變體 golden 不變。

## Steps

- [x] `register.mjs`＋測試。
- [x] `prompts.mjs`＋`prompts.test.mjs`。
- [x] `restyle` 指令（`flow.mjs` 的部分在 worker 票之後）。
- [x] skill references。

## How to verify

```bash
npm run test:tools
node tools/video/automation/cli.mjs restyle --slug <slug> --dry-run
```

## Notes

`voice.style` 是設定值不是提示詞：站主已在第 0 期貼到後台；它在 `speechHash` 裡，改了全部重錄。

做完學到的：

- 漫劇的聽稿提示原本是 `${INSTRUCTIONS.listener}` 再加講者規則，直接把說書規則接在投影片的聽稿提示後面會連帶進漫劇；拆成 `LISTENER_BASE`（兩種格式共用的耳朵編輯）之後投影片加 `REGISTER_RULES`，漫劇加講者，`DRAMA_INSTRUCTIONS` 的四個 key 不變。
- `restyle` 的答案逐句過 `rewrite.mjs` 的守門：中文數字（「三秒」→「五秒」）不在守門範圍，守門只認阿拉伯數字、拉丁字詞與字典詞；所以 `restyle` 之後 `verified=false` 讓查核再跑一輪，不是多餘的。
- `settle()` 多了一條：純投影片（沒有 `shot`）若撰稿仍回 `look`，直接刪掉，不然 lint 會以「look 沒有 shot」擋下來讓撰稿多修一輪。
- scope 加了 `flow.mjs`、`automation.test.mjs`、`tools/video/cli.mjs`（指令表與說明）、兩份 `SKILL.md`（列出新提示檔）與 `ILLUSTRATED.md`（`restyle` 的說明與階段表）；worker 票已結案，沒有重疊。
