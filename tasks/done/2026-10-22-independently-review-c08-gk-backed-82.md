---
id: 2026-10-22-independently-review-c08-gk-backed-82
title: Independently review C08 GK-backed 82-line script and visuals
status: done
priority: P2
area: docs
owner: codex-gpt6-c08-independent-r1-82
claimed_at: 2026-10-22T13:30:40Z
created_at: 2026-10-22T13:30:33Z
completed_at: 2026-10-22T13:33:00Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-r1-82.md
---

# Independently review C08 GK-backed 82-line script and visuals

## Why

PR #1681 的 C08 82 句新稿導入 GK Report No.34 第 23–24 頁。舊來源收據只綁舊 SHA，需另一名代理直接重讀 K1、K2a、K3、D1、R1、M1，對本次旁白及同 ID 畫面留下可追溯的獨立判定。

## Definition of done

- [x] 對 82／82 句及 82／82 列畫面留下綁定本次三檔 SHA 和 PR head 的獨立來源判定；指出需修稿的 ID 與直接來源位置。

## Steps

- [x] 直接打開 K1、K2a、K3、D1、M1，下載 GK Report 官方 PDF 並目視重讀印刷頁 23–24。
- [x] 每句及同 ID 畫面比對，另分 1961 上市、2018 商標、補充口／倒取嘴尖、累計銷售口徑與未授權來源圖片。

## How to verify

讀 docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-r1-82.md；對三個輸入檔執行 Get-FileHash -Algorithm SHA256 並核對收據首段；從官方原頁讀 K3 登錄／公告日期和 GK Report 印刷頁 23–24。執行 npm run check:tasks、git diff --check；逐句表的 ID 須與 script.md 完全相同。

## Notes

本輪總判 HOLD：旁白 c080304 與 R1 握持姿勢不夠貼合，c080601 把 2018-03-30 註冊日寫成公司宣布日，c080603 省掉 K3「食品容器」的少見範圍；視覺 c080401 的工作台酒杯可能暗示實際比較試驗。其他句逐 ID 判定在收據。新稿任何字或畫面變動都須新 SHA 的獨立覆核；不宣稱站主核准、TTS 長度、付費或發布。
2026-10-22：本機 tasks done 已寫出 done 票，但 open 原檔仍在；對該已核對絕對路徑的單檔 Remove-Item 被自動審查 blocked by policy。未改用其他刪除方式；本 PR 僅納入 done 票與查核收據，不納入未追蹤的 open 副本。提交後需以 PR/CI 對已提交樹重新確認 check:tasks。
