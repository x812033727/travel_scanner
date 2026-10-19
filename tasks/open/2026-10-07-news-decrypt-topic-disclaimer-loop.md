---
id: 2026-10-07-news-decrypt-topic-disclaimer-loop
title: Classify mixed-topic Decrypt stories before crypto policy and hand off held candidates
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-07T04:34:10Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
---

# Classify mixed-topic Decrypt stories before crypto policy and hand off held candidates

## Why

這張票從 4e16 未追蹤原稿恢復到共享隊列，保留原 ID 與建立日期，狀態 open、無 owner。原觀察為 2026-10-07 04:30 UTC，正式站 SHA `2024304170c6b43ecb4259e6b4fb0ce8a60d9893`；不是目前正式站候選狀態。

原兩個 Decrypt AI 故事繼承 fixed `crypto` feed 的類別，pipeline 因該類別在初稿及 correction 後加入 crypto notice，獨立 checker 两轮因此要求修改：

- `777cd153-b8dd-4c82-8a7f-22fb6a34375e`：Google Launches Nano Banana 2.1，`https://decrypt.co/380257/google-launches-nano-banana-2-1`。
- `ae1fa4ac-bc77-4185-b1b0-17f75d559cd7`：TikTok metadata dataset on Hugging Face，`https://decrypt.co/380229/someone-scraped-5-billion-tiktok-videos-posted-data-hugging-face`。

本輪 frozen main `657d34790d1446d4f4b2784b4cf5261a22f2c5f6` 的 Decrypt config 仍是 crypto；scanner 只對 mixed source 用 `classify_vertical`，pipeline 在 verification 前與第一次 corrected_document 後仍依 candidate.vertical 用 `with_crypto_disclaimer`。分類 scope 確實未完成；此讀碼沒有更新正式站、候選、retry 或來源設定。

## Done when

- [ ] 以實際 source/body 證據確定 Decrypt 混合主題的窄分類決策，在首次套 category/topic/crypto policy 前，AI、tech 與 genuine crypto 代表案例取得正確分類。
- [ ] 用來源 config／scanner 的最小修正與有意義回歸完成 code scope；不回退已完成的 crypto warning policy 修復。
- [ ] Genuine crypto 保留既有 finance/non-investment-advice notice 與全部發佈防護，不提升 Decrypt 的 first-party／single-source 資格。
- [ ] 原兩個 held candidate 的歷史證據已與共享 `2026-10-10-add-audited-held-news-category-correction` 和既有新聞操作票連結；各自需要 fresh state/hash/ownership 後才能提出有界恢復。交接本身不等於恢復、重新審稿或發佈已完成。

## Steps

- [x] 保存 4e16 原票完整 bytes，以及原 assessment_details／summary 快照與 SHA-256；原檔保留在 Git 外。
- [x] 逐票去重：#1371 的 translated notice 辨認、#1411 的 genuine-warning delete/reappend 修復已完成，不能重開；本票只保留 mixed-source classification 缺口。
- [ ] Claim 前重新核對 branches/worktrees/open PR 和 sources/scanner scope；已有 source config 票重疊時先窄分工，不用 force 接管。
- [ ] 對 pinned source/body 建立 AI、tech、genuine crypto fixtures，確認 fixed feed 繼承與 mixed classification；只改最小必需範圍。
- [ ] 在 existing held-category 票 Notes 交叉連結這兩個歷史 ID／證據；保持其原 Gemini/Manus IDs 及授權 cohort，額外候選須獨立 fresh readback／操作批准。
- [ ] 原新聞 owner 取得恢復責任與外部證據位置；沒有 fresh 狀態驗證之前不 queue/retry/rewrite、重設 cap、核准或發佈。

## Verification

Focused scanner/source config tests 應涵蓋 AI／tech 不被 fixed crypto 繼承、genuine crypto 正確保留、既有 mixed／fixed source 慣例不回退。按 dev-and-ci 跑受影響 API checks。分類重現及程式驗證不需要 provider call；舊 checker 的「其他主張相符」不是獨立 editorial PASS。

既有 held-category ticket 的有界修正維持 genuine actor audit、expected old category/state/time/evidence hash、fresh row lock、無 active DB/RQ work、保留 hold/cache/claims/原文歷史與 lifetime rewrite counts，以及零 queue/publication。來源全域 SourcePatch 与已存在candidate修正是兩件事。

## Notes

- 原稿保存：`<home>/.codex/scratch/codex-closeout-20261011/decrypt-original-task.md`；原兩候選狀態和 410 pending-review／99 needs-redraft／4 failed 都是 2026-10-07 觀察，不宣稱 current。
- 原來源：`<home>/.codex/news-audits/20261007-4e16/assessment_details.json`，190,746 bytes，SHA-256 `937d13558a922a4ea94397f7e5df429103c1ee41fd54c612ba6a4755d4edbca4`。
- 原摘要：同目錄 `summary.json`，13,198 bytes，SHA-256 `431d81d1b764658135a7af55e89dcbd580860c0086d4450118a56a2fab4557ac`。
- 精確副本與 readback hash 已保存到 `<home>/.codex/scratch/codex-closeout-20261011/decrypt-source/`；完整 preservation manifest 在 `receipt-review-verification.json`。不把 raw snapshots、actor/DB 資料或 private paths 放進 Git。
- 已完成：`2026-10-07-recognize-translated-news-disclaimer-notices-and`（#1371）與 `2026-10-10-news-disclaimer-correction-loop`（#1411）；兩者保留真正 crypto warning，不修正 Decrypt 固定分類。
- 尚未完成：`2026-10-10-add-audited-held-news-category-correction`，scope 為 schemas/service/router/tests，原 Gemini/Manus IDs 仍保留；本票與之互鏈而不重開同 API 實作。
- 覆核範圍內未做 implementation、production write、provider、retry、candidate approval 或 publication。
