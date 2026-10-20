# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v9 離線候選，等待同版獨立來源複查與兩位全新盲讀。** [v8 來源審查](reviews/source-audit-v8-independent.md) HOLD、[盲讀 A](reviews/blind-a-v8-independent.md) HOLD、[盲讀 B](reviews/blind-b-v8-independent.md) HOLD，僅適用舊 SHA；[v9 作者修訂表](reviews/blind-remediation-v9.md)記錄本次改動。此版有可重建的 102 句主片、16 個劇情鉤子、93 景匿名插畫提示詞／9 張原生數字卡，以及兩支 Shorts 稿；**沒有配音、插畫、試片、正式片頭片尾或公開影片網址**。不能將本資料夾稱為成片。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：一座 Ohio 廠從增產計畫轉為尋買家的單線故事。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件及計畫、投入、出售意向的邊界。逐句表是作者標註，不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、片頭片尾、US$25、真實來源與待填的 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者單一稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

目前主片 `video.json` SHA-256：`670de33997becaee126d9932e61c1a97a952a63905a0a257c41d4bd082463985`；兩支 Shorts `shorts.json` SHA-256：`9a63b6fa1a14834c9dfe6a151403bc4d93d2d57015c86b2d65eb940181894649`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs`、`compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。任何改稿都要重算 SHA、重做獨立來源與盲讀。
