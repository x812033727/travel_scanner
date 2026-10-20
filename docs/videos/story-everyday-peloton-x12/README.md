# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v3 候選稿，等待同版來源增量複查與兩位新盲讀。** [v2 獨立來源審查](reviews/source-audit-v2-independent.md)對 v2 雜湊給出 PASS，但 [盲讀 A](reviews/blind-a-v2-independent.md)與[盲讀 B](reviews/blind-b-v2-independent.md)指出轉場、結尾回顧與視覺辨識問題；[v3 修訂表](reviews/blind-remediation-v3.md)逐項對照。更早的 [v1 來源收據](reviews/source-audit-independent-v1.md)與[v2 修訂](reviews/source-audit-remediation-v2.md)均保留。此版有可重建的 114 句主片、12 個鉤子、99 景匿名插畫提示詞／15 張原生數字卡，以及兩支 Shorts 稿；**沒有配音、插畫、試片、正式片頭片尾或公開影片網址**。不能將本資料夾稱為成片。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：一座 Ohio 廠從增產計畫轉為尋買家的單線故事。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件及計畫、投入、出售意向的邊界。逐句表是作者標註，不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、片頭片尾、US$25、真實來源與待填的 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者單一稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

目前主片 `video.json` SHA-256：`8a130ccf40c2c9e7cf1be5ae903aeeb29a1e8910e0ff6c721ebc313392267c36`；兩支 Shorts `shorts.json` SHA-256：`b16ef0178a09b11ce9cd23f8f5955e506979d4614571050281853cc5b1e563c0`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs`、`compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。這些 SHA 隨候選稿微調會更新；以凍結交審時的最終值為準。
