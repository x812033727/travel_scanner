---
id: 2026-10-23-lock-c16-bialetti-v6-blind-reader
title: Lock C16 Bialetti v6 blind reader A receipt
status: review
priority: P1
area: docs
owner: codex-c16-blind-reader-a
claimed_at: 2026-10-23T07:08:08Z
created_at: 2026-10-23T07:07:54Z
completed_at:
branch: codex/c16-bialetti-v6-blind-a-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/blind-v6-reader-a.md
---

# Lock C16 Bialetti v6 blind reader A receipt

## Why

C16 v6 需要一位未先看作者材料的新讀者，對 81 句純旁白單獨判斷故事節奏，並確認讀到的投影與作者 PR #1704 指定 head 的旁白逐句相同。

## Definition of done

- [x] 在解盲前保存有時間與投影雜湊的唯讀初判，逐一回答 12 項並列行號。
- [x] 從 712bee76443af9cd24a57b2a405873180c88b95b 另建 worktree 和分支，檢查 81/81 ID、順序、旁白文字一致。
- [x] 只增補獨立收據，不改作者稿；以 draft PR 交付供作者修訂。

## Steps

- [x] 只讀指定旁白投影並寫入盲讀鎖檔，SHA-256 鎖定。
- [x] 解盲後從作者精確 head 取 script.md，按 ID 與旁白逐字比較。
- [x] 把初判與 parity 結果寫入 docs/videos/story-everyday-bialetti-c16/reviews/blind-v6-reader-a.md。

## How to verify

在本分支重跑 git rev-parse HEAD^ 取得精確作者基底、git diff HEAD^ --name-only 確認只增本收據與本 task；收據的 81/81 結果來自 git show 712bee7:docs/videos/story-everyday-bialetti-c16/script.md 的表格「ID／旁白」對指定投影 [ID] 旁白按序逐字比對。跑 npm run check:tasks 與 git diff --check。

## Notes

盲讀鎖定：2026-10-23T15:05:17.123+08:00。投影 SHA-256 C61956827036B6A0720565D52E2D973F72C20455860C416B996C099D04DDC6D2；鎖檔 SHA-256 2CFE211C007AE08287CAD0E7428FA2479DFAFD3D7333E9CF87665DCB4FEEF713。總判 HOLD，no_detour 與 no_recap 為必須項 HOLD。無真實 TTS 計時，無付費、匯入、上傳、合併。
