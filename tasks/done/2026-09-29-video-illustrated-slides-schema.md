---
id: 2026-09-29-video-illustrated-slides-schema
title: Illustrated slides: schema, cadence lint, status and review order
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:17:02Z
created_at: 2026-09-29T09:14:21Z
completed_at: 2026-09-29T09:26:02Z
branch: claude/sharp-brown-dh2x95
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/cadence.mjs
  - tools/video/core/cadence.test.mjs
  - tools/video/core/fixtures/illustrated
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - tools/video/qa/pace.mjs
---

# Illustrated slides: schema, cadence lint, status and review order

## Why

站主 2026-09-29 說目前的全自動投影片影片太死板，要像黑貓研究院（每 4–6 秒換一張插圖加運鏡、配樂、說書旁白）或 Gary Chen 那樣生動。設計與分期在 `docs/videos/ILLUSTRATED.md`（第 4 期寫）與本次計畫。第一步是讓 `format: "slides"` 的 `video.json` 可以帶 `look`、`visual: "still"` 的 `shot` 場景、`music`、`sfx`，讓 lint 估計「每 ≤8 秒換畫面、至少一半時間是插圖」，讓 `status` 與審核順序知道插圖投影片多了 `keyframes drawn`、`storyboard approved`、`music generated` 三步。漫劇與原來如此事務所的驗證、步驟、雜湊都不能變。

## Definition of done

- [x] `tools/video/core/fixtures/illustrated/video.json`（投影片＋look＋still shot＋music＋sfx）lint 零錯誤；drama 與 explainer fixture 的 lint 輸出 byte-for-byte 不變。
- [x] 非漫劇的 shot 只准 `visual: "still"`，不得有 `characters`／`fit`／`start_frame`／`end_frame`，且必須有 `look`；`characters`／`series` 仍只准漫劇。
- [x] `core/cadence.mjs`：`MAX_PICTURE_SECONDS 8`、`TARGET_AVERAGE_SECONDS 6`、`MIN_ILLUSTRATION_SHARE 0.5`、`HOOK_SECONDS 20`，`cadenceProblems(doc, timeline)` 純函式，不 import `qa/`（`slideStates` 搬進 core，`qa/pace.mjs` re-export）。
- [x] lint：刪掉「投影片不配樂」警告；插圖投影片在估計時間軸上跑 `shotProblems` 與 `cadenceProblems`，**先全部是警告**；版型相似度只比卡片；開場鉤子 20 秒。
- [x] `picturesHash(doc)`＝shot 的 [id, prompt, camera]；投影片的關鍵影格 manifest 綁 `look_hash + pictures_hash`，不綁 `visual_hash`。
- [x] `state.mjs`：`SLIDES_STEPS` 依 `illustrated(doc)`／`doc.music` 多三步；`pipelineStatus` 對 `hasPictures` 讀分鏡關卡、keyframes／music manifest；`assembledMedia` 比對 `look_hash`、`pictures_hash`、`mix_hash`、`sfx_hash`；純投影片仍是 12 步。
- [x] `review/sync.mjs` `nextGate` 投影片順序 outline → audio → (storyboard) → final；`render/cli.mjs` 在 `hasPictures` 時讀 keyframes manifest。

## Steps

- [x] `core/drama.mjs`：`illustrated`、`hasPictures`、`picturesHash`、`tech-story` 預設、`SLIDES_PRESET`、放寬 `validateDrama`。
- [x] `core/schema.mjs`：`TOP_KEYS` 加 `sfx`、`validateSfx`、錯誤訊息。
- [x] `core/cadence.mjs`＋測試；`qa/pace.mjs` 改 re-export。
- [x] `core/lint.mjs`、`core/state.mjs`、`review/sync.mjs`、`render/cli.mjs` 與各測試。
- [x] fixture `core/fixtures/illustrated/`（video.json、brief.md）。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs lint --file tools/video/core/fixtures/illustrated/video.json
node tools/video/cli.mjs lint --file tools/video/core/fixtures/drama/video.json     # 輸出不變
node tools/video/cli.mjs lint --file tools/video/core/fixtures/explainer/video.json # 輸出不變
```

## Notes

- 為什麼不搬去漫劇路線：會失去投影片的 dubs 狀態（`state.mjs:383`）、pace QA、教學撰稿與查核提示詞、大綱關卡，還會繼承劇本關卡與一律揭露。
- 節奏規則先當警告：`saveAndLint` 只對錯誤重試（`flow.mjs:1196-1211`）；前五支證明撰稿能達標後再升成錯誤。

- 2026-09-29：做完。`slideStates` 搬進 `core/cadence.mjs`（`qa/pace.mjs` re-export），節奏規則全部是 lint 警告、常數在 `cadence.mjs`；投影片的 keyframes manifest 綁 `look_hash + pictures_hash`（`picturesHash`＝shot 的 id、prompt、camera），`checks.json` 多 `pictures_hash`（`keyframesHash`）、`mix_hash`、`sfx_hash`。新預設 `tech-story`（`SLIDES_PRESET`）。`sfx` 欄位 `{ set, gain_db? }` 與 `sfxHash` 也在這裡定義，合成端在 `2026-09-29-video-illustrated-slides-assemble`。
- 漫劇的 `mix` 雜湊照舊（沒有 music 也算），投影片只在有 music 時算，否則 story 的 status 測試會把「沒配樂」當成過期。
