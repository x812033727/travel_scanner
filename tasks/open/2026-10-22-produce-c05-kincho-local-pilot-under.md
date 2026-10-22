---
id: 2026-10-22-produce-c05-kincho-local-pilot-under
title: Produce C05 Kincho local pilot under approved cap
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-c05-pilot
claimed_at: 2026-10-22T05:43:51Z
created_at: 2026-10-22T05:43:44Z
completed_at:
branch: codex/brand-story-kincho-c05-pilot
depends_on: []
scope:
  - docs/videos/story-everyday-kincho-c05/brief.md
  - docs/videos/story-everyday-kincho-c05/video.json
  - docs/videos/story-everyday-kincho-c05/story-lexicon
  - docs/videos/story-everyday-kincho-c05/reviews/owner-pilot-approval.md
  - docs/videos/story-everyday-kincho-c05/production-quote-erratum.md
  - docs/videos/story-everyday-kincho-c05/pilot-runlog.md
---

# Produce C05 Kincho local pilot under approved cap

## Why

C05 金鳥的 79 句劇本與逐鏡方向已由站主核准，另已核准本集本機試片整支 US$25、最多 86 張插圖／每張最多三次、79 句旁白及一首配樂。需把付費決定綁到固定稿件，先完成專屬發音字典、`video.json`、非付費檢查，再依實測聲音與費用停線；不匯入、合併、上傳或發布。

## Definition of done

- [ ] 有固定雜湊的站主試片核准收據、專屬發音字典、可 lint 的 `video.json` 與非付費乾跑。
- [ ] 一輪正式 TTS 後如供應商 429 即停且不重送；若成功，正文 02–06 章純配音實測至少 480 秒並通過音訊檢查後才可買圖。
- [ ] 圖片最多 86 張、每張最多三次，連同 TTS、配樂及所有未拆帳項累積不超過 US$25；完成狀態、費用與未完成關卡留在本集 runlog。

## Steps

- [x] 核對 PR #1675 的 script／visual、上游 Treatment／矩陣及整支估價雜湊；讀回工作目錄、STOP、既有媒體狀態。
- [x] 寫入站主本集試片核准收據，先安全初始化專屬發音字典，再建立 `video.json`。
- [x] lint、TTS／keyframes 乾跑，檢查張數與實際供應商報價；不以字數估計代替 480 秒。
- [ ] 只送一輪正式 TTS；429 或 STOP 即記錄並停，不重送。成功後量正文、音訊查核，再決定圖片關。
- [ ] 在固定額度內做後續合成與 QA；保持草稿 PR、no-auto-merge，不上傳／發布。

## How to verify

`Get-FileHash -Algorithm SHA256` 綁定四份內容與估價；`node tools/video/cli.mjs lint --slug story-everyday-kincho-c05`、`tts --dry-run`、`keyframes --dry-run --takes 3`；TTS 成功後以 `timeline.json`／音檔實際時長、`check-audio` 與媒體台帳核對 480 秒及 US$25。`npm run check:tasks`、repo-hygiene 與差異檢查。

## Notes

2026-10-22：試圖從劇本分支建立專用完整 worktree，Git 在取出約 80% 的 25,249 個檔案時遇到 C: 空間不足。Git 自動移除失敗的 checkout，經讀回目標不存在；改在既有乾淨 C05 劇本 checkout 切到 `codex/brand-story-kincho-c05-pilot`，避免再複製整個倉庫。舊 Treatment 工作樹遭政策阻擋的未追蹤重複票未碰。

劇本分支先把 `video.json` 從劇本票的 scope 移交本票，提交 `3e39aec702d17c9b6ba5211cb2b12bcef00cc3fc`，已推送 PR #1675。本票堆疊其上。C05 `video.json` 尚不存在，本集預設媒體工作目錄在檢查時尚不存在；全站／本集 STOP 均未見。上游四份內容雜湊與前次核准相同；估價 SHA-256 `73455BCB2E1A9A7A9E29023F6E39717E439DB20DCF27C1A02037868EFCD9DD36`。供應商曾對別集 C06 TTS 回 HTTP 429，C05 只許一輪正式 TTS；若 429 即停，不以本集重試測配額。

2026-10-22 續做：C: 有約 19.3 GiB 可用，腳本、視覺、Treatment、來源矩陣及原估價 SHA 全數與核准收據一致。新增工具需要的 `brief.md` 後 lint 為 0 errors／13 warnings；本機 `approvals.json` 綁定 79 句劇本 SHA。TTS 乾跑 79 句、2,353 billable characters；keyframes 乾跑 63 個 shot、最多 189 次生成，當下圖片費上界約 US$2.55（未含評審與其他）。`media-status` 為本集 US$0.00。原估價漏算句子且仍寫核准前狀態，保留原檔 SHA 並新增 `production-quote-erratum.md`。本集正式 TTS 須待共用供應商上的 C06 一輪完成，避免同時擠壓額度；其後依 480 秒與 US$25 停線。詳見 `pilot-runlog.md`。
