---
id: 2026-10-15-curio-h12-research-outline
title: Curio H12 research and outline
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:34:42Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h12
---

# Curio H12 research and outline

## Why

站主要求繼續製作五集奇聞檔案局；本票負責 H12 弗蘭南燈塔的本次來源查核與可選大綱，避免把後世文學場景當作當年現場。

## Definition of done

- [x] 保存本次重開來源的 research.md、逐項 claims.md 與可供選擇的 A/B brief.md。
- [x] 另一位查核員覆核事實與大綱，修正有依據的問題。
- [x] 協調者完成站主選綱交接；本票不涵蓋正式劇本、付費製作或上架。

## Steps

- [x] 閱讀 curio-episode、youtube-video、故事主線／開場／十三題及 H01-v2 前 30 景。
- [x] 唯讀承接題庫 H12，重開 NLB 當年文件、Gibson 原詩及 NRS 2026 展覽公告。
- [x] 寫兩個約 10 分鐘大綱、各至少三個開場鉤子與回收預案。
- [x] 獨立覆核。

## How to verify

檢查三份文件的來源 ID 與 claims 對應，兩案時間各 600 秒；人工確認詩中餐桌沒有被當成最初現場。協調者統一執行 `git diff --check` 與 `npm run check:tasks`，避免平行改動時重複驗證。

## Notes

- 本次查核日期為 2026-10-16（Asia/Taipei）；任務工具以 UTC 產生 2026-10-15 的票號，未改票 ID。
- 題庫來源提交 `949bb91fc85d41a53633d056062b27d87651e9d5`；沒有修改共享題庫。
- 1929 神祕日誌的傳播鏈本次未重讀原刊，不放進推薦案的具體斷言。已重讀的 1912 詩只證明文學文本存在，不主張詩是所有傳說的唯一源頭。
- 110 英尺是器材箱位置，不是量得的浪高；海浪說標為 Muirhead 的最可能解釋。
- 2026-10-16 01:01（Asia/Taipei），協調者完成手動大綱送審並讀回 `pending`；review ID：`d5fae6fa-4eb7-412e-973b-5713ea63e14b`，對應 brief SHA-256：`FF4AF2F817BD382943EA3EEF63AAD97962DB04C8B0D8FEBAC1373C81952E80EB`。送審版 brief 未再修改。
- 交接完成，釋出本票認領；仍待站主選 A／B 大綱，以及本批 US$30.00 估算停手上限授權（尚未核准）。正式生產尚未開始，沒有付費請求或 worker 啟動；本票未標 done，整集尚未完成，由協調者統一 commit／PR。
- 2026-10-16 獨立覆核由另一集作者完成，協調者轉交意見；已明確分開 ARCHTOR 15 日午夜過船通報與岸上 Return Book，避免混成同一觀察。研究／大綱版已凍結供站主選擇，不代表正式稿十三題已通過。
