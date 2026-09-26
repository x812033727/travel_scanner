---
id: 2026-09-26-video-series-planning
title: Video series T2: the setting book, the series outline and the chapter outlines, planned by the worker with the tension rules
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:36:26Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-series-api
  - 2026-09-26-video-series-web-routes
scope:
  - tools/video/automation/series.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/series.test.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/SERIES.md
---

# Video series T2: the setting book, the series outline and the chapter outlines, planned by the worker with the tension rules

## Why

站主點名「規劃劇情跟劇本」是重點：設定集要有衝突引擎與長線謎團，總綱要有全季張力地圖，篇章細綱每集要有鉤子、衝突、轉折、懸念、伏筆與張力曲線。這張票把三種作品層文件的生成、送審、退回重寫做進工人，提示詞照 `SERIES.md` 的規格逐條寫。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [ ] `automation/series.mjs`：`seriesStep()` 問 `series/next`，`setting`／`outline`／`chapter` 各跑一次企劃模型（`stage("planner", "series-<slug>", payload, 32_000, "drama", variant)`），答案是 `{body_md, body_json}`，`POST docs`；退回帶 `owner_note` 與上一版重寫，超過 `series_doc_rewrites` 停在待審。
- [ ] 提示詞：`references/prompts/series-setting.md`、`series-outline.md`、`series-chapter.md`，與 `prompts.mjs` 的作品變體（含「不得使用既有作品的人物、名詞、情節」、雙男主留白、開放結局與保留謎團）；`references/series.md` 說明做法；`SKILL.md` 路線表；`.claude` 副本位元組相同。
- [ ] `series.test.mjs`：假站端到端（三份文件、退回一次、重寫上限）；文件 JSON 的必要欄位檢查（每集的 hook／conflict／turn／cliffhanger／setups／payoffs／tension／characters）。

## Steps

- [ ] series.mjs 與 client 的作品呼叫。
- [ ] 提示詞與 skill 文件。
- [ ] 測試。

## How to verify

```bash
node --test tools/video/automation/series.test.mjs && npm run test:tools
```
