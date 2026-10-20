# S44 大綱人工關卡回條（2026-10-20）

## 固定提案與來源

- [`brief.md`](brief.md) SHA-256 `44f332d8c1a4d50550c4ba17927964523ed0a7a2fc0a2ebf5227fba898ff63de`；網站解析器 `outlineOptions` 返回兩個完整選項 A、B，均含一行說明與開場鉤子。
- [`research.md`](research.md) SHA-256 `018132f973a8aa1359876f54d532123137fc8cf5b31937527a9263120c2195ca`；固定 John Snow 1855 年第二版原文 commit `6a27453cc0bb85c3fc125c5e13900c8f3a8b48db`，raw SHA-256 `3f3e71972f603e5fa50a0e71045afffa994ae38a86a8912dda3e90c8babb37af`。
- 兩位獨立唯讀讀者重新抓取原文及地圖、核實拆把手／發病曲線的先後，並檢索 S01–S43 和 H/M/P/U/L 題庫無重複；詳細行號及邊界寫入 [`research.md`](research.md)。這是**選題和來源可行性查核**，尚不是完整劇本逐句／畫面驗收。

## 站台動作和實際狀態

1. `review-push --slug curio-s44 --report-only`：`reported to /admin/videos; nothing submitted`。
2. `review-push --slug curio-s44 --gate outline`：Jev 建議 A（1.00），但工具同時回報 `not a video the worker made (no auto.json): the owner decides at every gate`、`outline submitted for review (pending)`。
3. `review-pull --slug curio-s44 --gate outline`：`outline: waiting for the owner`，exit 3。**站主尚未選定。**

站台上只有**大綱待決**；未提交 script gate，亦未申請或花費 TTS、圖片、配樂預算。這次為了站台讀取影片格式，曾以本地暫稿 `video.json` 執行 outline handoff；未經驗證的劇本、逐句表和完整 `video.json` 已移出 repo，暫存 `/tmp/s44-preoutline-draft-20261020/`，**不能視為定稿或搬回後直接進媒體**。最終 `script.md`、`video.json`、`claims.md` 必須在 A／B 決定後重寫或覆核；先跑 0/0 lint、兩位來源隔離的同版十三題盲讀及完整逐景來源／視覺查核，再提交人工 script gate。若站主選 B，不能套 A 的稿或驗收。成片之後的品牌 5 秒片頭與 21 秒片尾、Short 和 Studio 可點連結仍屬規劃，尚無 S44 媒體。
