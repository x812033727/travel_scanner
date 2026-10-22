---
id: 2026-10-22-independently-recheck-c11-ucc-c110410-one
title: Independently recheck C11 UCC c110410 one-line repair
status: done
priority: P1
area: docs
owner: codex-c11-independent-source-v5-recheck
claimed_at: 2026-10-22T17:26:44Z
created_at: 2026-10-22T17:26:33Z
completed_at: 2026-10-22T17:28:15Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v5-c110410-recheck.md
---

# Independently recheck C11 UCC c110410 one-line repair

## Why

V5 獨立來源收據對 `c110410` 的虛構精確中文品名判 HOLD；作者只修此句，舊 SHA 的 HOLD 不能直接變成新版 PASS。新稿須由未改稿者重讀 UCC 原頁及相鄰句、鏡頭。

## Definition of done

- [x] 對新 script、來源註記與未改的兩份視覺稿雜湊寫一份獨立 PASS／HOLD 收據，舊 HOLD 保留為歷史紀錄。

## Steps

- [x] 直接重讀 UCC 2026 與 2025 原頁，核 1969 年 4 月、含奶產品及正式日文品名。
- [x] 比對父提交與現行 `c110410`，連讀 `407–411` 和相應鏡頭／字卡。
- [x] 只寫獨立審查收據，不改作者旁白、來源註記或分鏡。

## How to verify

核對 `Get-FileHash` 的四檔 SHA；`git diff 1d17ca716 1ec6fd87a -- <四檔>` 證明正文只修一個旁白 ID、兩份視覺稿未改；解析三份稿件仍各 78 ID 同序；`git diff --check`、`npm run check:tasks`。細節見 `docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v5-c110410-recheck.md`。

## Notes

判定：新 SHA 的 `c110410` 來源差異 PASS。UCC 兩份原頁都記 1969 年 4 月推出 `UCCコーヒーミルク入り`；新句「UCC 這款含奶罐裝咖啡」是產品描述，沒有聲稱中文正式品名。上下文仍區分塗層、反覆試作、商品化及可攜，後製日期卡無錯誤品名。其餘 v5 已過的逐 ID 來源與畫面文字預檢只因逐字未改而延用。兩位新的純旁白盲讀、成圖、TTS、站主與付費關卡仍待辦。

`npm run check:tasks` 退出 1，原因僅是本 worktree 原有八份不屬本票的 untracked `tasks/open/` 舊副本，與已完成的 `tasks/done/` 同 ID；不刪改它們。本票 own open 副本在 `done` 寫出結案檔後已刪除。
