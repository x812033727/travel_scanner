---
id: 2026-09-27-video-split-settings-worker
title: Video split settings worker: a drama reads its own voice, standing instructions, rounds and language defaults
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-27T06:16:01Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-split-settings-api
scope:
  - tools/video/automation
  - docs/videos/AUTOMATION.md
---

# Video split settings worker: a drama reads its own voice, standing instructions, rounds and language defaults

## Why

主機工人對漫劇也讀教學的 `voice`、`stage_instructions`、`max_verify_rounds`、`max_retake_rounds`、`caption_locales`（`tools/video/automation/flow.mjs`）。設定分開之後（`docs/videos/DRAMA-FLOW.md` §一），漫劇要讀自己的一份；教學一個位元組都不變。

## Definition of done

- [ ] `state.format === "drama"` 時：`instructionsFor` 的 standing 用 `drama_stage_instructions[stage]`；`settle()` 寫進 `video.json` 的旁白 `voice` 用 `drama_voice ?? voice`；`verify()` 用 `drama_max_verify_rounds`；`narration()` 用 `drama_max_retake_rounds`；`dramaPayload`／`planPayload` 的題材用 `drama_topic_scope`（現在送的是 `topic_scope`）。語言預設由改寫後的 `2026-09-26-video-dubs-worker` 處理。
- [ ] `client.mjs` 讀 `ToolSettingsView` 的新欄位；舊站沒有時退回教學的值（工人可能比站先部署）。
- [ ] `automation.test.mjs`：漫劇用自己的聲音、指示與輪數；教學的流程與送出的 payload 不變。
- [ ] `docs/videos/AUTOMATION.md` 的設定表改成 DRAMA-FLOW.md §一的三欄。

## Steps

- [ ] `flow.mjs` 與 `client.mjs`。
- [ ] 測試與 `AUTOMATION.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- `settle()` 目前把設定的 `voice` 寫給每支影片；漫劇的角色聲音在 `characters[].voice`，不受影響。
