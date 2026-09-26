---
id: 2026-09-26-video-series-episodes
title: Video series T3: episodes made in order from the chapter outline, the script gate, the recap and the reused character sheets
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:36:29Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-series-core-script-gate
  - 2026-09-26-video-series-planning
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - docs/videos/AUTOMATION.md
---

# Video series T3: episodes made in order from the chapter outline, the script gate, the recap and the reused character sheets

## Why

集數要依核准的篇章細綱一集接一集地做：企劃書由細綱生成、劇本經站主核准、角色設定圖沿用作品的、做完寫前情、上架後自動開下一集。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [ ] `draftEpisode(request)`：企劃書由細綱生成（`## 故事前提`＝作品前提＋本集一句話、`## 角色` 逐字來自設定集、`## 站主觀點` 來自頻道立場或作品備註、`## 幕`＝beats、`## 大綱` 單一選項），本機直接核准 outline；`report` 帶 `series_slug`、`episode_number`。
- [ ] `scriptPayload` 帶作品脈絡（設定集、本集 beats、前 3 集前情全文、所有集的一句話、謎團狀態）；查核用作品變體（張力與連貫性、雷同檢查）並輸出 `beat_coverage`、`continuity_problems`。
- [ ] `advance()` 在 listener 之後 `scriptGate`：送審／等／退回 → 撰稿 FIX 模式；`video assembled` 後 `recap` 寫回；上架確認後 `POST episodes/{n}/done`。
- [ ] 設定圖沿用：作品存檔 `_series/<series>/characters/`，`look` 先查存檔、只為新角色生成，核准後複製進存檔（接 hands-off-drama-look 的自動選）。
- [ ] `automation.test.mjs` 端到端：第 1 集到劇本關卡、退回、核准、look 生成；上架後自動開第 2 集且 look 沿用不生成。

## Steps

- [ ] draftEpisode 與 payload。
- [ ] scriptGate、recap、done。
- [ ] look 沿用。
- [ ] 測試與 `AUTOMATION.md`。

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs tools/video/media/look-keyframes.test.mjs && npm run test:tools
```
