# X12 Peloton｜Ohio Output Park 品牌故事前製包

**狀態：v11 離線候選，等待同版獨立 SEC 查核與兩位全新盲讀。** [v10 獨立來源審查](reviews/source-audit-v10-independent.md)對 v10 舊 SHA 判 PASS；[v10 盲讀 A](reviews/blind-a-v10-independent.md)判 8/12、[v10 盲讀 B](reviews/blind-b-v10-independent.md)判 10/12，均退回敘事。這些收據不核准 v11。[v11 作者修訂表](reviews/blind-remediation-v11.md)只記改動，不代替獨立審查。本包有可重建的 96 句主片、22 個劇情鉤子、90 景匿名插畫提示詞／6 張原生數字卡，以及兩支各七拍 Shorts。**尚無配音、插畫、試片、正式片頭片尾或公開影片網址，不能稱為成片。**

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：2021 已有 Precor 美國廠卻另規劃 Ohio 專屬產能，走到 2022 二月廠殼處置、七月代工、九月與 2023 年報售況。
- [作者原件矩陣](source-matrix.md)與[逐句來源矩陣](line-source-matrix.md)：五份 SEC 原件和逐句標註；作者矩陣不是獨立 PASS。
- [逐句稿](script.md)、[主片編排](video.json)、[Shorts 編排](shorts.json)與[兩支 Shorts 稿](shorts-script.md)：正式媒體尚未製作。
- [視覺計畫](visual-plan.md)、[預算護欄](production-quote.md)、[上架交接](publishing-handoff.md)：畫風、5 秒片頭／21 秒 v4 片尾、US$25、來源與待填 YouTube 連結。
- `drafts/narration.md`、`compose-video.mjs`、`compose-shorts.mjs`：作者稿面與可重建腳本。改稿後重編、重算 SHA、重做獨立審查。

凍結候選 `video.json` SHA-256：`c66ea0f17970f19d4a3b3a9df4e26286dcc4872f2258beb83a294026c26013b9`；`shorts.json` SHA-256：`8602834e0e4d4baa09267c191492307b90dc823360ad69fc4af17ef0b9ba6f1d`。執行 `node docs/videos/story-everyday-peloton-x12/compose-video.mjs` 與 `compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-peloton-x12` 檢查主片。任何改稿都要重算兩個 SHA，讓來源審查與雙盲讀依新檔重來。
