# S60 R2｜作者的史料措辭與書面畫面修訂

2026-10-22 UTC。狀態：**作者候選，等待另一位工作者按新雜湊獨立覆核**。本回條回應 [R1 HOLD](r1-independent-source-visual.md)；它不是來源、盲讀或媒體 PASS。沒有 TTS、插圖、音樂或其他付費媒體呼叫。

## 修訂範圍

- `video.json` 的 **104/104 個 shot 提示詞**改成各自對應該句旁白的動作和時序。R1 發現 24 個逐字重複提示詞；修訂後 104 個提示詞有 104 個不同文字。數量大是因舊稿重用畫面橫跨多章；場景 ID、順序、章節、6 張字卡、11 個伏筆、攝影欄、來源、開頭與片尾配置均未改。
- 救橇 `s60019–024` 顯示墜落的是橇、繩與備用橇的救援，以及維斯汀繫繩下去綁箱；首次升旗 `s60045–046` 顯示五人共同扶起帶旗的桿；第二營 `s60067–074` 先完成量測與兩人外走，再另架小帳並留兩封不同收件人的信。
- 返程 `s60085–089` 留在回程路標與另一隊南下；`s60098` 畫面沒有提前出現小帳；`s60103` 回到弗拉姆之家小屋；`s60105` 用無人物的雪埋帳篷與合上的日記，避免畫出正在返程的史考特。`claims.md` 的畫面界線改成同一時序的原創示意，特別註明五人扶旗與死亡畫面。
- 旁白只動 4 句：`s60052` 說初算 89°56′ 且隊員滿意，`s60053` 說三人照原先安排外走，避免錯把初算當作外走決策原因；`s60102` 只說史考特在阿蒙森小帳留下到訪字條，不把後來另地的升旗合照合併；`s60105` 限定史考特本人未活著返回。研究 P09 與 `s60087` 主張補入 A13184–13189 的約 20 時實際出發記錄，保留 A13097–13118 的太陽在背後／減少眩光記錄。

## 凍結與可逆差分

初稿基線是作者檢查點 `806f4493d`，亦即 R1 審閱的三個檔案雜湊。[精確結構差分](r2-author-structured-diff.json) 保存全部 104 個提示詞、4 句旁白及 `claims.md` 每欄的前後文字，含 `research.md`、`script.md` 的 unified diff；其 SHA-256 為 `b633aec0f3488ffdfd83d4598f8cb62dadbda98fbf6930942947cff6e0e0b608`。

| 檔案 | R1 SHA-256 | R2 SHA-256 |
| --- | --- | --- |
| `brief.md` | `357f2c2706bd1fca6c77e9ccad45771a745ddadc91ba41da4d73f656ab2c5acc` | 同左，未改 |
| `research.md` | `d518e956f5bc3ed87d67429c4eabe82c0fda1ff0e8fabd852acfa7fe7049d92b` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` |
| `claims.md` | `b2bee88a40c01f115a3913ac4a0badf2f725fffe1a2aa386f88a380ea6e89556` | `4d7bd1388b9382219623bb9ce454677edd2eca6415c05ec4ccb0bbbf59421909` |
| `script.md` | `a6577011a6b1132abf1dd04375dab18f05db7537b51c2f46ea131a747d2740c2` | `1ac4ee6548edae5a61f507c4e99edd75f5a81668d9acfa418b0ec22de8ea8b91` |
| `video.json` | `e4e79c80b67fb811ca32245c6bef5c6ddaa3cf20c260f4a6f0a409c2d3493e23` | `bf8d95565857f0a8b976ef6f2d89e730fd88fabcab44201e75a05bd67dabba9c` |

結構差分確認 `video.json` 只有 104 個 `data.prompt` 與 4 個 `lines[0].text` 改動；所有頂層欄位、其餘場景資料均相同。`claims.md` 改 104 列畫面界線、4 列旁白、1 列 P09 錨點。兩份固定原始文本及其 SHA-256 沒有變動。

## 作者驗算與下一關

`VIDEO_WORKDIR=/tmp/s60-video-work node tools/video/cli.mjs script --slug curio-s60` 已重新產出劇本；`lint --slug curio-s60 --json` 得 **0 errors、0 warnings**，110 句、104 shot／6 card、11 個伏筆、估 10.836 分鐘，濃縮開頭後的第二章在 00:49。104 個提示詞逐字去重檢查為 104 個唯一值。

請不同工作者先核對新 `video.json`、`claims.md`、`research.md` 的來源與全 110 句書面畫面，再進行兩名隔離盲讀及正式合併；作者回條不代替這些判定。實際開頭動畫、配音、插圖、片尾連結與影片尚未製作或驗收。
