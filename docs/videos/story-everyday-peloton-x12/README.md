# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v2 候選稿，等待同版來源複查與兩位盲讀。** [獨立來源審查 v1](reviews/source-audit-independent-v1.md)保留原稿 SHA 與問題；[逐項修訂表](reviews/source-audit-remediation-v2.md)對照此版修正。已有可重建的 118 句主片、12 個鉤子、103 景匿名插畫提示詞／15 張原生數字卡，以及兩支完整 Shorts 稿；**沒有配音、插畫、試片、正式片頭片尾或公開影片網址**。不能將本資料夾稱為成片。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：一座 Ohio 廠從增產計畫轉為尋買家的單線故事。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件及計畫、投入、出售意向的邊界。逐句表是作者標註，不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、片頭片尾、US$25、真實來源與待填的 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者單一稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

目前主片 `video.json` SHA-256：`2d53384cf3400bcc3ca829676edd4342b8092d47e65ba33c4939c75d95f6999b`；兩支 Shorts `shorts.json` SHA-256：`197babe5aeb46a8fddbe122fa94f77329f9ba0f069d6b2c1c9090141b036575e`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs`、`compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。這些 SHA 隨候選稿微調會更新；以凍結交審時的最終值為準。
