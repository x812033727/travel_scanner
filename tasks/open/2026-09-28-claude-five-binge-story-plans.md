---
id: 2026-09-28-claude-five-binge-story-plans
title: Five original 120-minute binge drama plans by Claude, to compare with Codex's five
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:08:04Z
created_at: 2026-09-28T02:07:32Z
completed_at:
branch: claude/manga-drama-planning-5qgd63
depends_on: []
scope:
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Five original 120-minute binge drama plans by Claude, to compare with Codex's five

## Why

站主要做五部約兩小時、目標破百萬點閱的漫劇，同時請 Codex 與 Claude 各規劃五部，之後比誰的點閱率高、劇情好。Codex 的五部在 `codex/five-binge-story-plans`（`docs/videos/series-plans/binge-five-20260928/`）。這張票是 Claude 版：五部原創、彼此與 Codex 那五部都不重疊的 120 分鐘合集企劃，每部有設定集、四十集總綱、四篇細綱、連貫性表與上架包裝，都以產線的 `body_md`／`body_json` 形狀交付並通過工人的 `documentProblem`／`retentionProblem`。不建立後台作品、不生成媒體、不上架。

## Definition of done

- [ ] 五部各有 `source.mjs` 與由 `build.mjs` 產生的 19 個檔案（設定集、總綱、四篇細綱的 md／json、`documents.json`、`series-request.json`、連貫性表、包裝、manifest）。
- [ ] `node validate.mjs` 對五部零錯誤（含工人的規則、跨篇懸念、第 20 集翻轉、謎團排程、包裝上限）；`node --test validate.test.mjs` 全過。
- [ ] `README.md` 說明五部各是什麼、為什麼有機會破百萬、怎麼餵進產線；`COMPARE.md` 定下與 Codex 版公平比較的規矩。
- [ ] 分支推上 `claude/manga-drama-planning-5qgd63`，站主可以並排讀兩批。

## Steps

- [x] 讀 DRAMA／SERIES／BINGE 三份設計與工人、伺服器的文件驗證規則；看 Codex 版的目錄結構（只看結構，不看劇情）。
- [x] 開票、認領；寫 `build.mjs`、`validate.mjs`、`AUTHORING.md`、`validate.test.mjs`。
- [x] 定五部的故事聖經（題材、機制、人物、謎團答案、四篇、每集一句話、結局），派五個代理各展開一部的 `source.mjs`。
- [ ] 逐部審稿（鉤子、爽點是否具體、翻轉是否成立、結局是否收乾），修正後重建、驗證。
- [ ] 寫 README 與 COMPARE，推分支。

## How to verify

```bash
node docs/videos/series-plans/claude-binge-five-20260928/build.mjs
node docs/videos/series-plans/claude-binge-five-20260928/validate.mjs --write-report
node --test docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
npm run check:tasks
```

## Notes

- 五部與題材：`reload-first-day`《開服第一天，她的天賦叫讀檔》system-game／女主；`before-the-hammer`《重生回落槌前一秒》rebirth-revenge／女主；`three-needles`《三針》urban-return／男主；`taste-of-the-throne`《她替公主試毒十年》empress-rise／女主；`ghost-at-his-side`《符師與他的鬼》custom／雙男主留白。Codex 版沒有做 system-game；兩批的前提、人物、機制全部不同。
- 共同值由 `build.mjs` 注入：120 分鐘、每集 3 分鐘、40 集、每篇 10 集、compilation、hybrid、cinematic-3d、open_ended false；`hands_off` 預設 false，避免建立作品時誤觸全自動開拍。
- 驗證接的是工人真正的函式（`tools/video/automation/series.mjs`），另外加：鉤子 ≤ 28 字、跨篇相鄰懸念不同型、第 10／20／30／40 集 reveal 或 reversal、第 18–22 集正好一次 `world_flip`、每條謎團的埋下／推進／揭曉要在細綱對得上、每個角色與場景都要登記且出場。
