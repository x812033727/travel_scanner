---
id: 2026-10-22-independently-recheck-c11-ucc-v5-source
title: Independently recheck C11 UCC v5 source and visual delta
status: done
priority: P1
area: docs
owner: codex-c11-independent-source-v5
claimed_at: 2026-10-22T17:11:36Z
created_at: 2026-10-22T17:11:24Z
completed_at: 2026-10-22T17:15:14Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v5.md
---

# Independently recheck C11 UCC v5 source and visual delta

## Why

V4 的獨立來源／分鏡文字覆核 PASS，但兩位純旁白盲讀 HOLD；作者又改了 14 個旁白 ID、8 個 JSON 物件並刪去 5 個 ID。V4 整檔 SHA 收據不能套到 v5，須由未改稿者重新核原發行者來源與新版鏡頭。

## Definition of done

- [x] 一份綁定 v5 四檔 SHA 的獨立 PASS／HOLD 收據，逐 ID 記錄新增來源與畫面界線、未改列承接範圍及付費停線。

## Steps

- [x] 直接重讀 UCC 2026／2025、博物館、沿革與濱田市／島根縣原頁。
- [x] 用 Git 與解析腳本比對 v4→v5 的改字、刪除、三份檔案 ID 和 JSON／Markdown 鏡像。
- [x] 將判定寫入原草稿 PR 的窄 review scope，作者稿件不改字。

## How to verify

`Get-FileHash` 核對四檔 SHA；`git diff HEAD^ HEAD -- <四檔>` 查看差異；解析三檔 ID、JSON／Markdown 鏡像、69 shot／9 stats 與最多兩連卡；`git diff --check`；`npm run check:tasks`。判定與原頁連結見 `docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v5.md`。

## Notes

判定：**來源 HOLD**，因 `c110410` 新增「當時名叫」卻以「UCC 咖啡牛奶罐」取代原頁當時品名 `UCCコーヒーミルク入り`；須改描述句或忠實譯名，並由另一獨立人員對新 SHA 重核。其餘 13 個改寫旁白 ID 來源 PASS，8 個改寫鏡頭物件文字預檢 PASS。U1/U2 確有專家協助、反覆試作及流通品質目標，但沒公開最終配方／逐次試驗；1978 第二代包裝開法未述，1981 第三代才明列免開孔器拉環。新版盲讀、實圖、TTS 時長及站主核准仍待辦，未付費。

本 worktree 在開始前已有八份不屬本票的 untracked `tasks/open/` 舊副本，與已提交的 `tasks/done/` 同 ID；沒有刪改它們。`npm run check:tasks` 退出 1，精確原因是八份舊 `tasks/open/` 與已完成的 `tasks/done/` 使用相同 ID；本票不以修改他人 scope 當作修復。`git diff --check` 通過，四份作者稿 SHA 未變。
