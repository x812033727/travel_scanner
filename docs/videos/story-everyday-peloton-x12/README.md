# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v4 離線候選，等待同版來源增量複查與兩位全新盲讀。** [v3 來源審查](reviews/source-audit-v3-independent.md)只對 v3 雜湊給出 PASS；v3 [盲讀 A](reviews/blind-a-v3-independent.md)、[盲讀 B](reviews/blind-b-v3-independent.md)與[合併判定](reviews/combined-v3-independent.md)因開場洩底、倒敘、目錄語與重述判 FAIL。[v4 修訂表](reviews/blind-remediation-v4.md)列出本版逐句處置。更早的 v1／v2／v3 收據完整保留。此版有可重建的 114 句主片、15 個劇情鉤子、101 景匿名插畫提示詞／13 張原生數字卡，以及兩支 Shorts 稿；**沒有配音、插畫、試片、正式片頭片尾或公開影片網址**。不能將本資料夾稱為成片。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：一座 Ohio 廠從增產計畫轉為尋買家的單線故事。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件及計畫、投入、出售意向的邊界。逐句表是作者標註，不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、片頭片尾、US$25、真實來源與待填的 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者單一稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

目前主片 `video.json` SHA-256：`dd65d2827eb09ca53a75e5510955e0d351fe1bfbc57b855eb21292210943b4ab`；兩支 Shorts `shorts.json` SHA-256：`848b32cd211d4504eba90f33bee30d3de3c4d406a36c369ae7cc720f4ebf2a14`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs`、`compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。這些 SHA 隨候選稿微調會更新；以凍結交審時的最終值為準。
