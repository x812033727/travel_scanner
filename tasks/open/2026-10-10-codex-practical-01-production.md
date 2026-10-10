---
id: 2026-10-10-codex-practical-01-production
title: Produce Codex practical lesson 01 App and CLI with verified baseline evidence
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-practical-pilot
claimed_at: 2026-10-10T17:16:39Z
created_at: 2026-10-10T17:16:37Z
completed_at:
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - docs/videos/codex-practical-01-app
  - docs/videos/codex-practical-01-cli
---

# 第 01 課：接手專案先建立基準：知道哪裡能跑、哪裡還沒做（App／CLI）

## Why

使用者要求18課36支可獨立跟做的實作系列。本票負責本課兩入口的真實操作、獨立查核與成片，沿用已核對教材與既有 slides/tutorial 產線。

## Definition of done

- [ ] 建立只含本集起始五檔的工作副本，跑出並解讀教材基準 2 通過／1 失敗。
- [ ] 分辨起始版刻意未完成的篩選、作者參考版 3 通過與模型實作成果三種狀態。
- [ ] 用本機 HTTP 預覽驗證已存在的新增、完成與儲存，寫出第 03 集要接手的範圍。
- [ ] App、CLI 各完成一段主流程、一次實際失敗修復與一題獨立變式；只拿本課教材也能完成。
- [ ] 兩版分別保留版本、輸入、執行結果、來源hash；App 有真實原生操作畫面。
- [ ] 未撰稿者重做並查核；旁白、CC、成片 QA 与來源hash各有收據。
- [ ] 教材測試、媒體品管、站主學習回饋、上傳與公開狀態分開記錄。

## Steps

- [ ] 先讀 `docs/videos/codex-practical-series/lessons/01.md`、兩份 episodes brief、教材README/驗收及 STATUS。
- [ ] 為 App／CLI 各建立新的 start 副本，錄製完整輸入與結果，不借另一入口的成果。
- [ ] 完成課內變式：在兩份全新副本分別執行 start 與 reference 的同一測試，說明為什麼只有起始版紅燈，再寫一段給第03集的窄範圍交接。
- [ ] 根據真實結果撰寫各自video.json/claims/script，由另一代理寫verify-1。
- [ ] lint → outline核准讀回 → TTS額度dry-run → TTS/旁白檢查 → render/assemble/captions → QA/package；未知付費呼叫不直接重送。
- [ ] 記錄站主跟做與改版；首批01→03/05通過後，才製作其餘課。

## How to verify

使用本課 acceptance 與固定資料逐項核對；`node tools/video/cli.mjs lint --slug codex-practical-01-app` 及CLI版本（App缺素材時不能以空稿宣稱通過）。媒體工作父目錄 `C:/Users/x8120/mokaair-work/codex-practical-series/media`；每關hash與review-pull讀回核對。

## Notes

2026-10-11：CLI 真實唯讀 exec、基準测试、來源 hash 和瀏覽器收據已保存；CLI 稿件查核中。App 原生素材 pending_capture。
目前文字階段 native computer API 不可用，原生 App 素材是實際接續條件。不要以CLI終端、公開頁或練習網站截圖替代。媒體不進Git；不新增後台API。上傳、公開、合併與部署另需使用者授權與獨立收據。
