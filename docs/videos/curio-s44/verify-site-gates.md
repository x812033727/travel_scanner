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

## 10:36 UTC 大綱決定與其後續

`review-pull --gate outline` 現回 `outline: already recorded`，本機 `approvals.json` 記錄網站於 **2026-10-20 10:36:26 UTC** 核准上述 `brief.md` 的精確 SHA，備註 `chose outline A`。上段保留的是當時的待決歷史；現在 A 案已選定。原 `/tmp` 暫稿只用作素材與反例，已另行改寫、重新對原文逐句對照。劇本的獨立查核和網站 script gate 仍各有自己的回條；大綱核准沒有自動批准後續語音或付費圖像。

## 11:34 UTC A 案劇本送審

現行 [`script.md`](script.md) SHA-256 `0b5053192d0ca3747811bb789dbde224bc83ba8307708b61f89843d075a37651`；[`video.json`](video.json) SHA-256 `6572e05b1deb0ba86bbb7b3aea507e04ca8bc51af9af41e7432d9defd866c16c`。兩位彼此獨立、只讀這一版正文及官方題本的讀者各回 **13/13 yes**；合併的本機 `review/narrative.json` SHA-256 `e76849d1b0da85cc0f1a8cb100cfa629185ace2828d62354bd1844c4acb02988`，保留 `readers: 2`、`passed: true`；精確收據見 [`verify-1.md`](verify-1.md)。`review/script-check.json` 以當前腳本綁定，SHA-256 `295ebf9a7f0b473d3ccf1078eb22c2d76663c982832c033d59ba99e8a5ad9600`；來源／畫面文字覆核由完整讀稿加逐版差分完成。

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work` 環境下：`review-push --report-only` 成功且未提交；`review-push --gate script` 回 `script submitted for review (pending)`；隨後 `review-pull --gate script` 回 `script: waiting for the owner`，exit 3。本站將此片視為人工交稿（工作目錄沒有 `auto.json`），所以 **網站劇本核准仍待決**；本機盲讀通過不是站主核准。尚未合成 S44 旁白、圖片、配樂或成片，也沒有可點的 YouTube 影片連結。
