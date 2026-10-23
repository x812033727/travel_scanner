---
id: 2026-10-23-attribute-c15-frixion-whole-film-spend
title: Attribute C15 FriXion whole film spend before paid calls
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-23T05:38:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_budget
  - apps/api/migrations
  - tools/video/tts
  - tools/video/media
  - tools/video/automation
  - docs/videos/story-everyday-frixion-c15/reviews
---

# Attribute C15 FriXion whole film spend before paid calls

## Why

站主已在 2026-10-23 核准 C15《FriXion》本機試片整片 **US$25** 上限，詳見草稿 PR #1701 的 `docs/videos/story-everyday-frixion-c15/reviews/owner-paid-pilot-approval.md` 與 `production-quote.md`。核准的是可執行上限，不是已可下單。正式使用的 TTS voice／模型／供應商區域、可計費字元或音訊 token、音訊檢查與重錄上界還未讀回；目前也沒有證明每次 TTS、ASR／judge、圖片、配樂、文字審查及未知結果都能歸因到 C15 同一 US$25 帳戶。已有 C03–C06 舊費用需另行歸因，不能把全域 media cap 當單集餘額。

## Definition of done

- [ ] C15 的實際 TTS voice／模型／帳戶／區域及當時官方與帳戶單價都鎖定，按 87 句與有限重錄額度列出可預留的上界；未知單價或供應商餘額不足就 fail closed。
- [ ] C15 單片 US$25 預算帳戶可讀回，所有付費階段先按穩定操作 ID 預留、重試不重置、未知 POST 結果保留全額，舊費用對帳或全額保留，不擅自當零。
- [ ] 用完整測試和正式環境只讀帳本／供應商讀回證明任意付費上界不越線，才解除第一句 TTS 停線；TTS 片頭後正文實測 ≥480 秒才可買圖，成片插圖時間 ≥70% 另驗。

## Steps

- [ ] 與尚開的 C10 OXO 預算路由票、C03–C06 舊費用歸因及工人語音 scope 協調；認領時檢查活動任務與 PR，若 scope 重疊則等釋出，不強領或另開重複帳本。
- [ ] 實作／設定各付費路由的 C15 slug、單片上限、未知結果與重試預留，補遷移和必要測試；把本票 scope 精確更新為實際改動路徑。
- [ ] 在首次付費前，讀回 C15 帳本、既有實支／未結費用、可用額、所有費用路由與供應商價格，另保留實際旁白音檔／時長收據。

## How to verify

按 `backend-conventions`、`dev-and-ci`、`youtube-video`、`brand-story` 規則測試受影響路由。用可重現的拒絕案例驗證無帳戶、失價、超額、未知結果、重送同一操作 ID 均無第二次付費發送；部署後唯讀核對 C15 slug、US$25 cap、每項預留／實支／可用額與供應商帳單。關卡未通過不啟動 TTS、圖片或配樂。

## Notes

本票只把 C15 付費前的技術停線列入共享佇列，不認領與現有 C10／工人任務重疊的程式 scope，不進行付費或部署。站主的稿件與上限核准均已綁定精確雜湊；任何實質稿件或報價擴張須重新核准。

本機 `npm run check:tasks` 在此作者工作樹仍因兩份**未追蹤**的舊 `tasks/open/2026-10-23-record-c15-...` 結案副本而失敗；其 `tasks/done` 正本已在 PR。精確刪除先前遭自動政策以 `blocked by policy` 拒絕，不能改用別的方法繞過。本票只提交新檔；須以 PR 乾淨檔案集或隔離的乾淨工作樹再驗證 task check。
