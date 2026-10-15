---
id: 2026-10-15-curio-m09-research-outline
title: Curio M09 research and outline
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:34:56Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-m09
---

# Curio M09 research and outline

## Why

站主要求繼續製作五集奇聞檔案局；本票負責 M09 安提基特拉機械的更新研究與雙大綱，清楚區分殘存零件、推知功能及現代重建。

## Definition of done

- [x] 保存本次研究 research.md、可追溯 claims.md 與兩案 brief.md。
- [x] 獨立查核員覆核來源及敘事，修正確有依據的問題。
- [x] 協調者完成站主選綱交接；不涵蓋完整稿、付費生成或上架。

## Steps

- [x] 讀系列與故事規則，參考 H01-v2 前 30 景。
- [x] 唯讀承接 M09 題庫，重開主要論文、2021 更正及研究機構頁。
- [x] 補查 2024 月曆環孔數研究的作者機構摘要，避免稱前盤已完全破解。
- [x] 寫 A 推薦／B 替代、10 分鐘節拍與至少三個開場 loops 預案。
- [x] 獨立覆核。

## How to verify

核對來源 ID、claim 與大綱每個轉折；兩案預算各 600 秒。確認 30 只指殘存齒輪、69 只指 2021 模型。協調者統一執行 `git diff --check` 與 `npm run check:tasks`。

## Notes

- 查核日期 2026-10-16（Asia/Taipei）；票號沿用任務工具的 UTC 2026-10-15 日期。
- 唯讀題庫來源提交 `949bb91fc85d41a53633d056062b27d87651e9d5`，不改共享題庫。
- Nature 與 PMC 一般頁部分請求回驗證殼；2021 本文與更正實際從 Europe PMC 全文 XML 讀取。2006 使用 PubMed 摘要，2008 使用可讀的 Nature 摘要，沒有聲稱讀完付費全文。
- 2024 孔數是研究模型與孔洞問題，不能替換齒輪數。本案不岔入統計細節，也不把 2021 模型叫最新定論。
- 1902 發現者、潛水深度與掃描機重量不進稿；沒有足夠本次證據就不硬加戲。
- 2026-10-16 01:01（Asia/Taipei），協調者完成手動大綱送審並讀回 `pending`；review ID：`264fb9fa-e606-4b4e-93e3-ef7c07b7878d`，對應 brief SHA-256：`B9BE6725FEA76B516A03E2498ABCEACE0A158EA3FDC40A5C88ED5EA9E850DEE7`。送審版 brief 未再修改。
- 交接完成，釋出本票認領；仍待站主選 A／B 大綱，以及本批 US$30.00 估算停手上限授權（尚未核准）。正式生產尚未開始，沒有付費請求或 worker 啟動；本票未標 done，整集尚未完成，由協調者統一 commit／PR。
- 2026-10-16 獨立覆核意見已修：2021 明標電腦重建，不暗示實體複製品已驗證；1901 開場為後見描述，不畫潛水員當場識別齒輪；盤面以同一次操作帶用途，避免三個定義連念。研究／大綱版已凍結，不代表正式稿或完整敘事 QA 已通過。
