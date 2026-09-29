---
id: 2026-09-29-video-illustrated-slides-worker
title: Illustrated slides: the worker runs pictures, storyboard and music for a slides video
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:48:32Z
created_at: 2026-09-29T09:14:24Z
completed_at: 2026-09-29T09:52:25Z
branch: claude/sharp-brown-dh2x95
depends_on:
  - 2026-09-29-video-illustrated-slides-assemble
  - 2026-09-29-video-slides-media-api
  - 2026-09-28-video-explainer-settle-keeps-cast
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Illustrated slides: the worker runs pictures, storyboard and music for a slides video

## Why

`tools/video/automation/flow.mjs` 的 `advance()` 已依步驟 id 派 `keyframes drawn`／`storyboard approved`／`music generated`，但 `settle()` 不給投影片預設 look、`fixPrompts` 寫死 `"drama"`、`listen()` 沒把 variant 傳下去、`saveShorts` 只給 explainer。

## Definition of done

- [x] 投影片草稿有 shot 而沒 `look` → `settle()` 給 `{ preset: SLIDES_PRESET }`；`settings.music_track`／`sfx_set` 帶進 `music`／`sfx`；`music_enabled === false` 的刪除對所有格式生效。
- [x] `fixPrompts` 傳 `state.format`；`listen()` 傳 variant；`write()` 對 `illustrated` 也存 `shorts.json`。
- [x] 插圖投影片在測試裡從 `narration approved` 走到 `final`；keyframes exit 1 送回投影片撰稿修提示詞、兩輪後 block。
- [x] 漫劇走查測試不變。

## Steps

- [x] `settle()`、`fixPrompts`、`listen()`、`write()`。
- [x] `automation.test.mjs`。

## How to verify

```bash
npm run test:tools
node tools/video/automation/cli.mjs auto --once   # 對開了 slides_media_enabled 的站
```

## Notes

`2026-09-28-video-explainer-settle-keeps-cast` 也改 `settle()`：先做完或一併做，避免兩次改寫。

- 2026-09-29：做完。`settle()`：投影片草稿有 shot 時給 `look { preset: SLIDES_PRESET }`（寫手的欄位優先），沒有 `music`／`sfx` 時從設定的 `slides_music_track`／`slides_sfx_set` 帶入（伺服器欄位在 `2026-09-29-video-slides-media-api`，沒有就不帶）；`drama.music_enabled === false` 對所有格式刪 `music`；單集解說片一律沒有角色。`fixPrompts` 傳 `state.format`；`listen()` 對非漫劇傳 variant（漫劇照舊，系列測試的假站依 variant 回答）；`write()` 對 `illustrated` 也存 `shorts.json`。`advance()` 本來就依步驟 id 派 keyframes／storyboard／music。`--force` 認領的理由：API 票只補伺服器端的開關與模型，工具端有 `stages.mjs` 的退回值，不必等。
- 走查測試：planner → outline → writer（存 2 支 Shorts）→ verifier → listener → tts → 旁白 → keyframes → storyboard（站自動核准）→ render → music（授權檔）→ assemble → captions → 等 final。
