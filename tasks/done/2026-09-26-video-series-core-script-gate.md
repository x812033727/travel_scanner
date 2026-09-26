---
id: 2026-09-26-video-series-core-script-gate
title: Video series T1: the series field, the screenplay file and the script gate in the tool's core
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T19:54:31Z
created_at: 2026-09-26T17:36:24Z
completed_at: 2026-09-26T19:56:16Z
branch: claude/video-series-core
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/state.mjs
  - tools/video/core/approvals.mjs
  - tools/video/core/screenplay.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/pages.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/cli.mjs
  - docs/videos/DESIGN.md
---

# Video series T1: the series field, the screenplay file and the script gate in the tool's core

## Why

每一集的劇本要在花錢做圖與片段之前給站主看，而且作品的集數要在工具端知道自己屬於哪一部作品、第幾集，好讓角色逐字沿用、設定圖沿用。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [x] `video.json` 頂層可選 `series: { slug, episode, chapter }`（schema 與 `validateDrama`）；lint：作品集數的 `characters` 必須是作品人物表的子集且 `appearance`／`voice`／`sheet_prompt` 逐字相同，角色依 id 排序。
- [x] `core/screenplay.mjs`：`screenplay(doc)` 產生 `docs/videos/<slug>/script.md`（場景、【角色】台詞、情緒、每鏡提示詞、章節）與 `narrativeHash(doc)`（只算場景順序與每句 id／文字／說話者／情緒）；`cli.mjs` 加 `script` 指令。
- [x] `DRAMA_STEPS` 在 `fact-checked` 後加 `script approved`（綁敘事雜湊，不綁提示詞）；`GATES.script`；`REVIEW_GATES`、`STEP_LABELS`、`nextGate`（drama：outline → script → look → audio → storyboard → final）、`scriptSubmission`（payload：scenes、beats、coverage、continuity_problems、minutes）；`review/pages.mjs` 的劇本頁。
- [x] 投影片與單集漫劇的既有測試與煙霧測試仍綠；`core/drama.test.mjs`、`sync.test.mjs` 更新。

## Steps

- [x] schema／drama／lint。
- [x] screenplay 與雜湊。
- [x] 步驟、關卡、送審、頁面。

## How to verify

```bash
npm run test:tools && node tools/video/assemble/smoke.mjs --fixture drama --channel msedge
```

2026-09-27（claude-fable-5-1-video-drama）：PR #821（與 T2、T3 同一支）。`script approved` 只在 `video.json` 有 `series` 時進步驟清單，單集漫劇的流程不變；`script.md` 由 `review-push --gate script` 每次重寫（同敘事＝同 bytes，核准不失效）。`series.json` 不在只警告。
