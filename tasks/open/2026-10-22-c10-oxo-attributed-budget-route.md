---
id: 2026-10-22-c10-oxo-attributed-budget-route
title: Add attributed C10 OXO whole-film budget route
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-22T17:59:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_budget
  - apps/api/migrations
  - tools/video/tts
  - tools/video/media
  - tools/video/automation
---

# Add attributed C10 OXO whole-film budget route

## Why

站主已核准 C10《OXO》本機試片整支 US$25 硬停線，綁定草稿 PR #1689 的劇本、逐鏡與報價；這不是可花餘額。2026-10-23 唯讀稽核確認當時 `main` 與草稿 PR #1684 的 `video_budget/models.py` 均沒有 `story-everyday-oxo-c10`，TTS／媒體客戶端也沒有 C10 的試片歸因路由。未識別 slug 不能取得持久的單片預留與未知結果保留；第一句 TTS 都不能安全付費。C03–C06 的舊費用另在 `2026-10-22-reconcile-c03-c06-prior-charges-and` 待歸因。

## Definition of done

- [ ] C10 有單片 US$25 帳戶；TTS／ASR、圖片、評審、配樂與文字階段每筆付費操作都先按穩定 ID 預留，未知結果保留全額，重試不重置故事總額。
- [ ] 完整測試以超額、失價、帳戶缺漏及未知結果 fail closed；遷移接在部署時的唯一 head，舊試片回滾不破壞新帳戶。
- [ ] 部署後能唯讀讀回 C10 帳戶、每筆操作、餘額、供應商可用額及 C03–C06 已歸因或全額保留的舊費用，才解除第一筆 TTS 停線。

## Steps

- [ ] 與 PR #1684 的 C03–C06 媒體守門、`2026-10-19-worker-video-languages-five` 的 TTS scope 協調；未釋出前不 `--force` 認領重疊路徑。
- [ ] 設計並實作所有付費路徑的 C10 預算歸因、資料庫帳戶與不確定費用保留，為實際變更縮窄或補齊本票 scope。
- [ ] 逐路徑測試、正常部署與正式帳戶讀回；舊費用不得因沒有發票就算成零。

## How to verify

按 `backend-conventions`、`dev-and-ci`、`deploy` 技能跑受影響 API／影片工具測試；部署後用帳本讀介面核對 C10 slug、US$25 上限、操作與可用額。另證明未知結果停在預留而非釋放。正式站沒有讀回前不得付費。

## Notes

2026-10-23 稽核：`main` `f2e311d`、PR #1684 均未登記 C10 slug；`reserve_pilot_call` 對未識別 slug 無單片預留。C05 曾有 79 次 TTS／79 次 ASR，C06 曾有 94 次 TTS／至少 71 次 ASR，另有可能的 C03／C04 費用；共享延遲總額不能按集分攤。PR #1684 只替已歸因的 C03–C06 媒體路徑設草稿守門，本機 TTS 仍未歸因。此票**只記錄未完工作，沒有執行任何付費、部署或解除 STOP**。C10 核准收據：`docs/videos/story-everyday-oxo-c10/reviews/owner-paid-pilot-approval.md`。
