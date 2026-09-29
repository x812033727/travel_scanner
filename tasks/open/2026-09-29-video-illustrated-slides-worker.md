---
id: 2026-09-29-video-illustrated-slides-worker
title: Illustrated slides: the worker runs pictures, storyboard and music for a slides video
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:24Z
completed_at:
branch:
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

- [ ] 投影片草稿有 shot 而沒 `look` → `settle()` 給 `{ preset: SLIDES_PRESET }`；`settings.music_track`／`sfx_set` 帶進 `music`／`sfx`；`music_enabled === false` 的刪除對所有格式生效。
- [ ] `fixPrompts` 傳 `state.format`；`listen()` 傳 variant；`write()` 對 `illustrated` 也存 `shorts.json`。
- [ ] 插圖投影片在測試裡從 `narration approved` 走到 `final`；keyframes exit 1 送回投影片撰稿修提示詞、兩輪後 block。
- [ ] 漫劇走查測試不變。

## Steps

- [ ] `settle()`、`fixPrompts`、`listen()`、`write()`。
- [ ] `automation.test.mjs`。

## How to verify

```bash
npm run test:tools
node tools/video/automation/cli.mjs auto --once   # 對開了 slides_media_enabled 的站
```

## Notes

`2026-09-28-video-explainer-settle-keeps-cast` 也改 `settle()`：先做完或一併做，避免兩次改寫。
