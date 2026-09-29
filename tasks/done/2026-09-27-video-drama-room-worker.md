---
id: 2026-09-27-video-drama-room-worker
title: Video drama room worker: the planner and the writer answer the owner's messages, every drama has a script gate, the brief comes from the approved document
status: done
priority: P1
area: tools
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:44Z
created_at: 2026-09-27T06:16:02Z
completed_at: 2026-09-29T02:11:47Z
branch: codex/p1-task-audit
depends_on:
  - 2026-09-27-video-drama-room-one-off-series
  - 2026-09-27-video-drama-room-messages-api
scope:
  - tools/video/automation
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/review/sync.mjs
  - .agents/skills/youtube-video/references/prompts/discuss.md
  - .agents/skills/youtube-video/references/prompts/series-bible.md
---

# Video drama room worker: the planner and the writer answer the owner's messages, every drama has a script gate, the brief comes from the approved document

## Why

工人要接上討論串（`2026-09-27-video-drama-room-messages-api`）與「單集就是一集的作品」（`2026-09-27-video-drama-room-one-off-series`）：回站主的訊息、要改就出新版本；每支漫劇都在花錢之前有劇本關卡；`brief.md` 由核准的文件寫出，漫劇不再用選大綱的卡片。設計在 `docs/videos/DRAMA-FLOW.md` §二、§三。

## Definition of done

- [x] `discussStep()` 排在 `seriesStep()` 之前，一輪回一則：文件用 `planner` variant `discuss`，劇本用 `writer` variant `discuss`；輸入是文件（或 `video.json`）、整條串、這則訊息、作品脈絡、頻道立場；輸出 `{ reply, revised }`。`revised` 是劇本時：寫 `video.json`（保留每句 id、只改站主要的）→ `saveAndLint` → `verified = false`、`listener_done = false`，下一輪重跑查核、聽眾審稿、再送劇本關卡；回覆先 `POST …/answer`。模型給不出可用答案就回覆說明、串停著，不自動重試。
- [x] 提示詞：`VARIANT_INSTRUCTIONS["planner:discuss"]`、`["writer:discuss"]`（規矩照 DRAMA-FLOW.md §三：繁中 300 字內、問題只回答、要改才出版本並列出改了什麼、不動上層已核准的文件、劇本要過 lint）；同一份給代理用的 `.agents/skills/youtube-video/references/prompts/discuss.md`。
- [x] `stepsFor`：`script approved` 對每支漫劇都在（拿掉 `|| doc.series`）；`series_script_gate` 關著時本機自動核准劇本。
- [x] `draftEpisode` 也服務 one-off（`bible` 當 `setting`，`## 大綱` 單一選項、本機直接核准，備註「依故事聖經」）；`draftDrama` 舊路只留給遷移前已 `started` 的請求，之後刪。
- [x] `automation.test.mjs`：one-off 從 bible 到劇本關卡；討論回問題不出版本；討論要改就出新版本；劇本討論改完重跑查核並再送審；教學的流程不變。

## Steps

- [x] `discussStep` 與兩個 variant。
- [x] `stepsFor`、`draftEpisode`、`draftDrama`。
- [x] 測試與 `discuss.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- 2026-09-27 做完（claude-fable-5-1-video-languages）。
  - 討論在新檔 `tools/video/automation/discuss.mjs`：`discussStep()` 在 `step()` 裡排在 `seriesStep()` 之前、但在「推進手上影片」之後——所以劇本改完那一輪先重跑查核、聽眾審稿、重送劇本關卡，下一則討論才會被回。文件的討論：`planner` variant `discuss`，回覆＋（要改時）整份新版本，先用 `documentProblem` 檢查再送 `messages/{id}/answer`；被拒的新版本不送，回覆末尾寫「（新版本沒有存下來：原因）」。劇本的討論：`writer` variant `discuss`，`revised.video` 走 `saveAndLint`，過了就 `verified = false`、`listener_done = false` 存 auto.json，lint 不過就把 video.json 放回原樣、回覆說明；answer 一律 `revised: null`（檔案工人自己寫）。模型不是 JSON 或沒有 `reply` → 用 `unusableReply` 回一則說明，串就停在那裡，不重試、不 `halt`。這台工人沒有那支影片 → 也回覆說明。
  - `client.mjs` 多 `messageNext`、`messageAnswer`。舊站沒有這條路（404）就當沒有東西。
  - 提示詞：`SERIES_INSTRUCTIONS` 多 `planner:bible`（one-off 的故事聖經：角色、三幕、單一大綱、素材、不做的事）、`planner:discuss`、`writer:discuss`；reference 在 `prompts/discuss.md` 與 `prompts/series-bible.md`。
  - 每支漫劇都有劇本關卡：`stepsFor`、`pipelineStatus`、`review/sync.mjs` 的 `nextGate` 都拿掉 `doc.series` 的條件；`series_script_gate === false` 時 `scriptGate()` 本機 `approve`（備註「「劇本先給我看」關著，依設定自動核准」）不送站上。
  - `draftEpisode` 服務 one-off：`context.setting` 就是 bible（站上這樣回），`episode.beats` 是 bible 的 `outline`；brief 標題是故事名、`一句話：`、`## 大綱` 單一選項；本機核准 outline 備註「依故事聖經」；`state.series.kind = "one-off"`。one-off 的撰稿與查核用一般漫劇提示詞（不是 `writer:episode`／`verifier:episode`，那兩份講的是長篇的 recaps 與下一集）；`recap` 不做。video.json 的 `series` 照舊只有 slug／episode／chapter。
  - `draftDrama`（舊路）還在：站上 `drama-requests/next` 現在只回遷移前沒有 `series_id` 的排隊請求，正式站上遷移後不會再有；請求流程的測試改成驗「劇本先給我看關著」的自動核准。
  - `series.mjs`：`DOC_KINDS` 加 `bible`、`documentProblem` 的 `bible` 分支（characters、acts、outline）、`documentName()`、`isOneOff()`。
- `tools/skills.test.mjs` 只鏡像 SKILL.md；references 只有 `.agents/` 一份。
- 討論的每一輪一次模型呼叫，不算 `series_doc_rewrites`（那個只管單純退回）。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：claude-fable-5-1-video-languages；原分支：未記錄。

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- tools/video/automation/discuss.mjs:200 implements discussStep; client.mjs:141 provides message-next API.
- Task Notes and #870 describe one-off bible routing, script gate and re-verification after script edits.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Close stale review task.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
