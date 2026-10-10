---
id: 2026-10-10-codex-practical-06-production
title: Produce Codex practical lesson 06 paired App and CLI videos
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-10T17:21:16Z
completed_at:
branch: codex/codex-practical-series-20261011
depends_on:
  - 2026-10-10-codex-practical-curriculum
  - 2026-10-10-codex-practical-01-production
  - 2026-10-10-codex-practical-03-production
  - 2026-10-10-codex-practical-05-production
scope:
  - docs/videos/codex-practical-06-app
  - docs/videos/codex-practical-06-cli
---

# 第 06 課：讓測試替你抓回歸：先紅、修好、再確認沒壞別的（App／CLI）

## Why

使用者要求18課36支可獨立跟做的實作系列。本票負責本課兩入口的真實操作、獨立查核與成片，沿用已核對教材與既有 slides/tutorial 產線。

## Definition of done

- [ ] 把『All 篩選不得改變原順序』寫成失敗的測試。
- [ ] 用修改前紅燈、修復後綠燈證明測試能捕捉這個缺陷。
- [ ] 區分資料函式、儲存與瀏覽器操作的驗證邊界。
- [ ] App、CLI 各完成一段主流程、一次實際失敗修復與一題獨立變式；只拿本課教材也能完成。
- [ ] 兩版分別保留版本、輸入、執行結果、來源hash；App 有真實原生操作畫面。
- [ ] 未撰稿者重做並查核；旁白、CC、成片 QA 与來源hash各有收據。
- [ ] 教材測試、媒體品管、站主學習回饋、上傳與公開狀態分開記錄。

## Steps

- [ ] 先讀 `docs/videos/codex-practical-series/lessons/06.md`、兩份 episodes brief、教材README/驗收及 STATUS。
- [ ] 為 App／CLI 各建立新的 start 副本，錄製完整輸入與結果，不借另一入口的成果。
- [ ] 完成課內變式：新增『active 篩選不得改變未顯示任務』測試，混合完成狀態與同名任務，測試結果及原輸入。
- [ ] 根據真實結果撰寫各自video.json/claims/script，由另一代理寫verify-1。
- [ ] lint → outline核准讀回 → TTS額度dry-run → TTS/旁白檢查 → render/assemble/captions → QA/package；未知付費呼叫不直接重送。
- [ ] 記錄站主跟做與改版；首批01→03/05通過後，才製作其餘課。

## How to verify

使用本課 acceptance 與固定資料逐項核對；`node tools/video/cli.mjs lint --slug codex-practical-06-app` 及CLI版本（App缺素材時不能以空稿宣稱通過）。媒體工作父目錄 `C:/Users/x8120/mokaair-work/codex-practical-series/media`；每關hash與review-pull讀回核對。

## Notes

2026-10-11：教材與教案已建立；當課 App/CLI 原生操作、獨立重做與媒體尚未完成。不得把作者參考程式當模型成果。
目前文字階段 native computer API 不可用，原生 App 素材是實際接續條件。不要以CLI終端、公開頁或練習網站截圖替代。媒體不進Git；不新增後台API。上傳、公開、合併與部署另需使用者授權與獨立收據。
