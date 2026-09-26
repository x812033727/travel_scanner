---
id: 2026-09-26-video-stage-instructions-tools
title: Video stage instructions: the worker appends the owner's standing instructions and reports the format
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T15:27:38Z
created_at: 2026-09-26T15:26:32Z
completed_at: 2026-09-26T15:41:03Z
branch: claude/video-stage-instructions
depends_on:
  - 2026-09-26-video-stage-instructions-api
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/AUTOMATION.md
---

# Video stage instructions: the worker appends the owner's standing instructions and reports the format

## Why

同 `2026-09-26-video-stage-instructions-api`：站主在設定分頁寫的常設指示要真的進到模型的提示詞，而且伺服器要知道這次跑的是哪種格式，才能把送出的提示詞歸在對的標題下給站主看。

## Definition of done

- [x] `instructionsFor(stage, format, standing)`：常設指示（去頭尾空白後非空）接在該階段提示詞最後，標題「## The owner's standing instructions」並說明它優先於前面的規則；空字串不加。
- [x] `Automation.stage()` 從 `settings.stage_instructions[stage]` 取字串；`client.run` 的 body 多 `format`。
- [x] `docs/videos/AUTOMATION.md` 設定表多一列。

## Steps

- [x] prompts.mjs、flow.mjs、client.mjs、AUTOMATION.md。
- [x] automation.test.mjs：單元（空白不加、漫劇版也接）與假站端到端（planner 的 run 帶 format 與常設指示）。

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs
```

## Notes

2026-09-26（claude-fable-5-1-video-drama）：分支 `claude/video-stage-instructions`。工人與 API 同一次部署換新，舊 API 會因 `format` 是未知欄位回 422（StrictModel），所以不能只部署工人。
