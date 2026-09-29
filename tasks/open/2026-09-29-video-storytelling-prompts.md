---
id: 2026-09-29-video-storytelling-prompts
title: Storytelling register and illustration prompts for planner, writer and listener, plus restyle
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:24Z
completed_at:
branch:
depends_on:
  - 2026-09-29-video-illustrated-slides-worker
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/register.test.mjs
  - tools/video/automation/cli.mjs
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

- [ ] `register.mjs`：`REGISTER_RULES`（一份文字給 planner／writer／listener 與後台常設指示）與 `STORY_VOICE_STYLE`。
- [ ] `prompts.mjs`：`COMMON` 改插圖＋卡片＋說書；`TEMPLATE_GUIDE` 加 `shot`（英文提示詞 ≤1000 字、camera 詞彙、still、transition）；節奏規則 5–8 秒、share ≥ 0.5、構圖置中；writer 回 `look`、`shorts`；planner 大綱是故事節拍；listener 加節奏審稿；`VARIANT_INSTRUCTIONS` 加 `listener:register`。
- [ ] `cli.mjs` `restyle --slug`：listener register 一輪→`saveAndLint`→`verified=false`，不動 `brief.md`，line id 不變。
- [ ] skill references：`script-writing.md` 說書式一節、`writer-video.md`、`planner.md`、`listener-register.md`（新）、`formats.md`。
- [ ] `instructionsFor('writer','drama')` 與 explainer 變體 golden 不變。

## Steps

- [ ] `register.mjs`＋測試。
- [ ] `prompts.mjs`＋`prompts.test.mjs`。
- [ ] `restyle` 指令（`flow.mjs` 的部分在 worker 票之後）。
- [ ] skill references。

## How to verify

```bash
npm run test:tools
node tools/video/automation/cli.mjs restyle --slug <slug> --dry-run
```

## Notes

`voice.style` 是設定值不是提示詞：站主已在第 0 期貼到後台；它在 `speechHash` 裡，改了全部重錄。
