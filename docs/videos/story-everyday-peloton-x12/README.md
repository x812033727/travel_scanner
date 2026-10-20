# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v12 離線候選，等待同版獨立 SEC 查核與兩位全新盲讀。** [v11 獨立來源審查](reviews/source-audit-v11-independent.md)對 v11 舊 SHA 判 PASS；全新[v11 盲讀 A](reviews/blind-a-v11-independent.md)及[盲讀 B](reviews/blind-b-v11-independent.md)均判 10/12、退回結尾回收與鄰近重複。這些收據不核准 v12。[v12 作者修訂表](reviews/blind-remediation-v12.md)只記改動，不代替獨立審查。本包有可重建的 86 句主片、21 個登記問答、80 景匿名插畫提示詞／6 張原生數字卡，以及兩支各七拍 Shorts。**尚無配音、插畫、試片、正式片頭片尾或公開影片網址，不能稱為成片。**

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：2021 已有 Precor 美國廠卻另規劃 Ohio 專屬產能，走到 2022 二月廠殼處置、七月代工、九月與 2023 年報售況。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件和逐句標註；作者矩陣不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、5 秒片頭／21 秒 v4 片尾、US$25、來源與待填 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

凍結候選 `video.json` SHA-256：`211314204863d9f61000423134fde7cc571a9554e936bcf270ceb035b6832090`；`shorts.json` SHA-256：`a56aba8dd550be7e65b56069dd0b12558fa9e4ba7dbf9aa7c868b94de87bba5d`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs` 與 `compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。任何改稿都要重算兩個 SHA，讓來源審查與雙盲讀依新檔重來。
