---
id: 2026-09-27-video-drama-room-worker
title: Video drama room worker: the planner and the writer answer the owner's messages, every drama has a script gate, the brief comes from the approved document
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-27T06:16:02Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-drama-room-one-off-series
  - 2026-09-27-video-drama-room-messages-api
scope:
  - tools/video/automation
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - .agents/skills/youtube-video/references/prompts/discuss.md
---

# Video drama room worker: the planner and the writer answer the owner's messages, every drama has a script gate, the brief comes from the approved document

## Why

工人要接上討論串（`2026-09-27-video-drama-room-messages-api`）與「單集就是一集的作品」（`2026-09-27-video-drama-room-one-off-series`）：回站主的訊息、要改就出新版本；每支漫劇都在花錢之前有劇本關卡；`brief.md` 由核准的文件寫出，漫劇不再用選大綱的卡片。設計在 `docs/videos/DRAMA-FLOW.md` §二、§三。

## Definition of done

- [ ] `discussStep()` 排在 `seriesStep()` 之前，一輪回一則：文件用 `planner` variant `discuss`，劇本用 `writer` variant `discuss`；輸入是文件（或 `video.json`）、整條串、這則訊息、作品脈絡、頻道立場；輸出 `{ reply, revised }`。`revised` 是劇本時：寫 `video.json`（保留每句 id、只改站主要的）→ `saveAndLint` → `verified = false`、`listener_done = false`，下一輪重跑查核、聽眾審稿、再送劇本關卡；回覆先 `POST …/answer`。模型給不出可用答案就回覆說明、串停著，不自動重試。
- [ ] 提示詞：`VARIANT_INSTRUCTIONS["planner:discuss"]`、`["writer:discuss"]`（規矩照 DRAMA-FLOW.md §三：繁中 300 字內、問題只回答、要改才出版本並列出改了什麼、不動上層已核准的文件、劇本要過 lint）；同一份給代理用的 `.agents/skills/youtube-video/references/prompts/discuss.md`。
- [ ] `stepsFor`：`script approved` 對每支漫劇都在（拿掉 `|| doc.series`）；`series_script_gate` 關著時本機自動核准劇本。
- [ ] `draftEpisode` 也服務 one-off（`bible` 當 `setting`，`## 大綱` 單一選項、本機直接核准，備註「依故事聖經」）；`draftDrama` 舊路只留給遷移前已 `started` 的請求，之後刪。
- [ ] `automation.test.mjs`：one-off 從 bible 到劇本關卡；討論回問題不出版本；討論要改就出新版本；劇本討論改完重跑查核並再送審；教學的流程不變。

## Steps

- [ ] `discussStep` 與兩個 variant。
- [ ] `stepsFor`、`draftEpisode`、`draftDrama`。
- [ ] 測試與 `discuss.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- `tools/skills.test.mjs` 只鏡像 SKILL.md；references 只有 `.agents/` 一份。
- 討論的每一輪一次模型呼叫，不算 `series_doc_rewrites`（那個只管單純退回）。
