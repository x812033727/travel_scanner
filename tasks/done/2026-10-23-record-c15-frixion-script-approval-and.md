---
id: 2026-10-23-record-c15-frixion-script-approval-and
title: Record C15 FriXion script approval and full film quote
status: done
priority: P2
area: docs
owner: codex-c15-approval-quote
claimed_at: 2026-10-23T05:17:28Z
created_at: 2026-10-23T05:17:07Z
completed_at: 2026-10-23T05:20:21Z
branch: codex/brand-story-frixion-c15-script
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15/reviews/owner-script-approval.md
  - docs/videos/story-everyday-frixion-c15/production-quote.md
---

# Record C15 FriXion script approval and full film quote

## Why

站主在 2026-10-23 核准了 C15 目前的劇本與逐鏡方向。必須把決定綁定 PR #1701 核准前精確作者 head 和四份 Git blob 位元組，並為另一個付費關卡準備整集、非只有圖片的報價。這張票僅記錄核准及有停線條件的報價，不生媒體、不匯入、不上傳。

## Definition of done

- [x] 獨立站主劇本／逐鏡核准收據綁定 `be7bad23848f925dda3495701802bafa0f8f43c4` 和四份原稿 SHA-256，明確排除費用及媒體階段。
- [x] 整集報價列出 72 插圖、15 字卡、87 句 TTS、1 首配樂、至多 12 個額外圖槽／每圖三次、US$25 整片硬上限與已知／未知分界。
- [x] 報價明定可歸屬的預算路由、付費授權、片頭後實測正文 ≥480 秒及實際插圖時間 ≥70% 的停線。

## Steps

- [x] 核對 PR #1701 的 head／draft／`no-auto-merge` 與四份 Git blob 雜湊。
- [x] 核對 #1721 及 #1724／#1725 的該版 PASS 收據和官方 MiniMax／Google 價目。
- [x] 撰寫獨立核准收據與非執行性整集報價。
- [x] 在原 PR #1701 更新交接，維持 draft 與 `no-auto-merge`；提交後讀回 CI。

## How to verify

`git show HEAD:docs/videos/story-everyday-frixion-c15/<檔>` 經 SHA-256 計算，四值與收據相符；`python` 讀 `visual-plan.json` 得 87 列、72 shot、15 card，片頭後稿件 2,138 字符（紙上 513.12 秒）。`npm run check:tasks`、`git diff --check` 與 PR #1701 head／label／CI 讀回。

## Notes

來源／配鏡最後差異 PR #1721 PASS；兩位最終旁白盲讀 #1724／#1725 對相同投影 PASS。本稿不把它們的 draft 狀態寫成已合併。圖片官方單價 US$0.0035；Lyria 3.5 官方 US$0.08；每圖 Gemini judge US$0.01 是本庫帳本預留而非 Google 固定售價。TTS 路由／實支未核，不能啟動付費。

PR #1701 內文已改為這次精確站主核准與另外的報價邊界；程式與原四份素材未修改。提交後須讀回新的 PR head、四份 Git blob 雜湊與 CI；這些遠端檢查不算本票的付費執行。
