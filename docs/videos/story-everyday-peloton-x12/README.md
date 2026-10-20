# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v7 離線候選，等待同版來源複查與兩位全新盲讀。** [v6 來源審查](reviews/source-audit-v6-independent.md)因遺漏 2022 年 2 月 Ohio 廠殼「完工後出售」計畫判 HOLD；v5 [盲讀 A](reviews/blind-a-v5-independent.md)、[盲讀 B](reviews/blind-b-v5-independent.md)與[合併判定](reviews/combined-v5-independent.md)因重複口播判 FAIL。[v7 修訂表](reviews/blind-remediation-v7.md)列出本版逐句與 Shorts 時序處置。更早的 v1–v6 收據完整保留。此版有可重建的 112 句主片、15 個劇情鉤子、101 景匿名插畫提示詞／11 張原生數字卡，以及兩支 Shorts 稿；**沒有配音、插畫、試片、正式片頭片尾或公開影片網址**。不能將本資料夾稱為成片。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：一座 Ohio 廠從增產計畫轉為尋買家的單線故事。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件及計畫、投入、出售意向的邊界。逐句表是作者標註，不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、片頭片尾、US$25、真實來源與待填的 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者單一稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

目前主片 `video.json` SHA-256：`4a758f3587a2d669a84bb9000b70429d7b1d74b9747fff3cf4a7d84d16143190`；兩支 Shorts `shorts.json` SHA-256：`69b91f56e3b4a2dc2626cdf826aeb7843a26b422a2fde036d0915fd5935842c9`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs`、`compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。這些 SHA 隨候選稿微調會更新；以凍結交審時的最終值為準。
