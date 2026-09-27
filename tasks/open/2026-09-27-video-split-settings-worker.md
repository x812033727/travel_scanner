---
id: 2026-09-27-video-split-settings-worker
title: Video split settings worker: a drama reads its own voice, standing instructions, rounds and language defaults
status: review
priority: P1
area: tools
owner: claude-fable-5-1-video-split
claimed_at: 2026-09-27T07:07:56Z
created_at: 2026-09-27T06:16:01Z
completed_at:
branch: claude/video-review-manga-workflow-fp1rpz
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

- [x] `state.format === "drama"` 時：`instructionsFor` 的 standing 用 `drama_stage_instructions[stage]`；`settle()` 寫進 `video.json` 的旁白 `voice` 用 `drama_voice ?? voice`；`verify()` 用 `drama_max_verify_rounds`；`narration()` 用 `drama_max_retake_rounds`；`dramaPayload`／`planPayload` 的題材用 `drama_topic_scope`（現在送的是 `topic_scope`）。語言預設由改寫後的 `2026-09-26-video-dubs-worker` 處理。
- [x] `client.mjs` 讀 `ToolSettingsView` 的新欄位；舊站沒有時退回教學的值（工人可能比站先部署）。
- [x] `automation.test.mjs`：漫劇用自己的聲音、指示與輪數；教學的流程與送出的 payload 不變。
- [x] `docs/videos/AUTOMATION.md` 的設定表改成 DRAMA-FLOW.md §一的三欄。

## Steps

- [x] `flow.mjs` 與 `client.mjs`。
- [x] 測試與 `AUTOMATION.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- `settle()` 目前把設定的 `voice` 寫給每支影片；漫劇的角色聲音在 `characters[].voice`，不受影響。
- 2026-09-27（claude-fable-5-1-video-split）做完，在分支 `claude/video-review-manga-workflow-fp1rpz`：
  - `flow.mjs` 新增 `settingsFor(settings, format)`：回 `voice`、`instructions`、`verifyRounds`、`retakeRounds`、`topicScope`；漫劇讀 `drama.drama_*`，`drama_voice` 為 null 或站還沒有那個欄位就用教學的（跟遷移複製的語意一致）。`stage()`（常設指示）、`settle()`（旁白 voice）、`scriptPayload`（給撰稿的 voice）、`verify()`、`narration()`、`planPayload`（題材範圍，`draftDrama` 與 `replan` 帶 format）都改讀它。
  - `client.mjs` 沒有要改：設定是整個 JSON 回來的，新欄位在 `drama` 物件裡；退回舊值的邏輯在 `settingsFor`。
  - 沒改 `captions()`：語言仍照 `caption_locales`（兩種格式），等語言票（改寫後的 `2026-09-26-video-dubs-worker`）換成每支影片的選擇；`drama_caption_locales` 只是語言面板的預先勾選。
  - 測試：`settingsFor` 的四種情況（分開、null 跟教學、舊站、沒有 drama 物件）、`settle()` 漫劇用自己的旁白聲音而教學不受影響、`stage()` 漫劇與教學各接自己的常設指示；`node --test tools/video/automation/automation.test.mjs` 與 `npm run test:tools` 全過。
  - `AUTOMATION.md` 的設定表改成教學／漫劇／共用三欄，並註明語言面板落地前 CC 仍照 `caption_locales`。
