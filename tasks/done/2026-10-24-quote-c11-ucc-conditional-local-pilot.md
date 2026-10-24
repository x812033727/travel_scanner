---
id: 2026-10-24-quote-c11-ucc-conditional-local-pilot
title: Quote C11 UCC conditional local pilot
status: done
priority: P2
area: docs
owner: codex-c11-conditional-quote
claimed_at: 2026-10-24T07:10:53Z
created_at: 2026-10-24T07:10:47Z
completed_at: 2026-10-24T07:14:08Z
branch: codex/c11-ucc-conditional-quote-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/production-quote.md
  - docs/videos/story-everyday-ucc-c11/pilot-readiness.md
---

# Quote C11 UCC conditional local pilot

## Why

C11 已有站主核准、綁定 SHA 的 78 句／78 鏡稿件與已合併的非付費 `video.json`，但缺整支付費提案及逐關停線。前製進度不能當成有帳本、配音、圖像或成片；本票只作可審閱的繁中本機試片條件式報價。

## Definition of done

- [x] `production-quote.md` 精確綁定核准稿，列出 69 圖／9 卡、逐類最高請求次數、整支 US$25 提案、公開價與正式帳戶上界的差別，以及先配音實測 ≥480 秒才購圖。
- [x] `pilot-readiness.md` 將核准、非付費前製、付費路由、真實媒體、正式站匯入與上架分開，並標示 HOLD。
- [x] 另一位代理唯讀核算張數、算術和關卡；必要本機檢查通過，任務在本 PR 內搬入 `tasks/done/`，PR 為草稿且帶 `no-auto-merge`。

## Steps

- [x] 讀取 `AGENTS.md`、brand-story／youtube-video／task-board 技能、現行 C11 核准原件與轉檔收據；確認共用 checkout 原 C20 分支乾淨且已推送，從最新 `origin/main` 開專用分支並正常認領本票。
- [x] 寫兩份非付費文件，只改本票 scope；核對官方公開價和程式帳本限制，不把估額當上界。
- [x] 另一代理獨立唯讀覆核報價；依意見修正。
- [x] 跑 `npm run check:tasks`、`git diff --check` 及文件關聯／SHA 的定點讀回；在 PR 內結案、提交推送草稿 PR。

## How to verify

`Get-FileHash -Algorithm SHA256` 讀回四份核准原件及 `video.json`；解析 `video.json` 驗 78／69／9、21 個候選 `say`；以獨立算式驗 69×3＝207、207×0.0035＝0.7245、207×0.01＝2.07、加一首 0.08＝2.8745。`npm run check:tasks`、`git diff --check`、PR `no-auto-merge`／草稿讀回。

## Notes

2026-10-24：原稿四個 SHA 與遠端 main 的 Git blob 完全相同，PR #1813 已合併。C11 現行機器稿 78 句／78 鏡、69 插圖／9 字卡，正文純語音紙上 384.96 秒；沒有本集付費核准、單集預算帳戶、實際音檔或成片。Minimax／Google 官方公開價已於今日讀取；圖審 US$0.01 是專案規劃值，不是可保證的帳號最壞費用。本票不觸發付費、後台匯入、上傳或發布。

另一位代理 `c11_quote_independent` 只讀覆核 **PASS（僅條件式報價與準備表）**：五份 SHA 與現行檔一致，69×3＝207 圖及圖審、78×2＝156 TTS 與轉寫、四批最多 40 句 Jev、US$0.7245＋2.07＋0.08＝US$2.8745 均正確；本集付費仍 HOLD。它特別確認紙上正文比 480 秒短 95.04 秒，若實測不足須停圖、重核並再報。`npm run check:tasks` exit 0（既有其他票警告），核准原件與 `video.json` SHA 讀回吻合，機器稿 78／69／9、21 個候選 `say`；`git diff --check` PASS。
