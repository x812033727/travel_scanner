---
id: 2026-11-01-sothatswhy-candidate-pool
title: So Thats Why: build the staged large candidate pool from the reviewed plan
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T05:56:09Z
completed_at:
branch:
depends_on:
  - 2026-11-01-sothatswhy-episode-depth
scope:
  - tools/video/so-thats-why/pool
  - docs/videos/so-thats-why/pool
---

# So Thats Why: build the staged large candidate pool from the reviewed plan

## Why

站主要素材池可累積十萬筆以上，再依內容厚度組成影片。規劃已在 `docs/videos/so-thats-why/refresh-20261101/POOL-STRATEGY.md`；目前只有 313 筆來源紀錄，沒有大型索引或批次擴庫。不得用同義標題或無來源答案灌成十萬列，也不能讓候選資料繞過逐集企劃和查核。

## Definition of done

- [ ] 以現有 313 筆與原 ID／查核／退題理由建立可續跑的本機索引，不修改歷史包或正式資料庫。
- [ ] 原始提問、去重問題、前提通過候選、來源足夠素材、影片企劃／已審劇本分開計數。
- [ ] 每條主張連到精確來源、條件、日期與查核狀態；模型提案與未讀連結不能自動升格。
- [ ] 去重保留原 ID／別名／回復路徑；已剔除與已製作內容可查，換標題不能復活。
- [ ] 小批候選驗證去重和前提篩選後再到約 1,000／10,000／100,000 以上，逐批報實際數量、缺陷與成本，不把目標寫成完成量。
- [ ] 主題群有相接理由；輸出到新版單集企劃入口，不能每題自動套固定長度生成影片。

## Steps

- [ ] 開始前重新查工作樹、同 scope 任務與 PR；閱讀 CURRENT、POOL-STRATEGY、SPEC 及本機 selector。
- [ ] 設計並試匯入索引、候選／來源／主張／關係／修訂資料；建立 idempotent 批次日誌與 dry-run。
- [ ] 抽查來源類型、重複合併、前提淘汰與入選，各自保存樣本和錯誤；進片主張仍逐條查核。
- [ ] 先交小批有效結果與實際運行成本；擴量前依當期使用者授權範圍處理付費與外部寫入。

## How to verify

以可重現的匯入／去重／續跑／回復與來源變更案例驗證；精確指令於實作時補。既有 `node tools/video/so-thats-why/cli.mjs check` 和定向測試必須繼續通過，來源 ID 與歷史狀態不可丟失。抽查報告只代表抽樣，不宣稱整批事實全對。

## Notes

- 此票僅記錄待做，沒有 claim、背景工作、外部爬取或費用發生。
- 《十萬個為什麼》是提問方向，沒有指定版本，也不授權複製整本問答。
- 先本機小批驗證，按使用需求再決定是否服務化；不要先開正式 DB migration。
- 已完成的 30 支候選只是編輯規劃，不是 30 支完成腳本或核准影片。
