---
id: 2026-10-24-record-owner-approval-for-c08-short
title: Record owner approval for C08 short-v8 local pilot
status: done
priority: P1
area: docs
owner: codex-root-c08-approval
claimed_at: 2026-10-24T06:06:18Z
created_at: 2026-10-24T06:06:14Z
completed_at: 2026-10-24T06:07:40Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08-short-v8/README.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/brief.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/owner-pilot-approval-20261024.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/production-quote.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/pilot-readiness.md
---

# Record owner approval for C08 short-v8 local pilot

## Why

站主在完整 C08 short-v8 條件式報價送審後核准整支本機試片 US$25 上限。若專案檔仍標成未核准，後續代理可能重複詢問；若只標「可做」又可能跳過未接通的帳本與供應商核價。需用精確報價雜湊、短版來源雜湊和站主答覆留下核准與停線邊界。

## Definition of done

- [x] 專案收據綁定站主核准答覆、原報價 SHA 與 36 句／36 鏡來源 SHA，且精確列出次數與 US$25 總額。
- [x] 簡報、README、報價及就緒表一致區分「費用上限已核准」與「首筆付費仍 HOLD」。
- [x] 無預算解鎖、供應商請求、正式站匯入、上傳或發布。

## Steps

- [x] 讀回站主對 C08 報價的答覆與 PR #1811 的核准前報價原件，固定內容 SHA-256 `28f983bc35272c216ce9026855bf881e0b29f03eadd7169f908d1284d2926948`；後續 rebase 不改授權範圍。
- [x] 加入核准收據並修訂跨檔狀態，維持預算路由、供應商價格及實測語音關卡。
- [x] 用 task-board 與 diff 檢查確認無雙份票與無超範圍變更。

## How to verify

對 PR #1811 核准前報價的 Git 檔案內容算 SHA-256，應得 `28f983bc35272c216ce9026855bf881e0b29f03eadd7169f908d1284d2926948`；`git diff --check`、`npm run check:tasks`；`rg -n '核准|HOLD|US\$25' docs/videos/story-everyday-kikkoman-c08-short-v8 -g '*.md'` 並人工核對張數／次數不變。

## Notes

2026-10-24：站主精確答覆「核准 C08 本機試片，US$25 上限」。這不含後台匯入、上傳、排程或發布；也不替代 C08 專屬帳本、舊費用／未明請求、實際模型價格及停線測試。`apps/api/app/video_budget/models.py` 的 `C_SERIES_PILOT_LIMITS_USD` 目前沒有 C08，任何首筆付費仍禁止。未來 C08 製片由開放票 `2026-10-24-complete-c08-short-v8-local-pilot` 接續；本票只保存授權及前製狀態。
