# A01 r44 Travelpro 單線替代提案（ALTERNATE_PROPOSAL／HOLD）

本目錄從固定的 r43 候選及其獨立盲讀、來源審查、畫面史實稽核產生一次**離線**窄修。已核准的 A01 標題、縮圖、1970 年 Macy's 上架主題和 `stories.json` 均未修改；此版以 Travelpro Rollaboard 產品線為主角，須由站主另行審核企劃方向，不能沿用舊企劃核准。r43 與更早候選只讀，`build.mjs --write` 僅能首次建立本目錄輸出，`--check` 逐檔重算位元組。

提案標題：**Rollaboard：機師做出會滾的登機箱，為何最後仍得拆包？**

提案縮圖：匿名記者與一只深藍、無商標的直立雙輪箱，機艙座位下與頭頂櫃都顯得狹窄；完全遮住外袋結構，保留原因懸念。後製主字 **「會滾卻放不下？」**。不得生成歷史真人、真實商標或可讀的年份／專利文字。

故事第一句便提出 1993 年 Travelpro Rollaboard 放不進座位下與頭頂櫃、為何得取物的問題；接著點名機師 Plath 的負重與他未標年的安檢回憶，先不說外袋原因。前方旅客的箱子材質未載；硬殼的是 Plath 後來的螺絲樣品。片中要**聽得見**兩個界線：螺絲樣品如何變成成品沒有記錄；1993 年那只上市箱是產品線的後期個體，不是車庫的同一實物。1987／1988 成品年份只在研究檔保留，原 PDF 第 17 頁未目視；1989 專利是後見文件，不能當成成品問世年。記者先前另帶輪具的經驗不是本次測試當班；陡路緣與樓梯不定先後，最後加衣書與取出的確切地點沒有來源。片中機艙走道只作她對當時輪箱類型的概述，不重建這只 Travelpro 的當次行程。1993 段先讓收納失敗發生，再揭外袋衣書與膨脹原因，最後只演一次取物後收好的解決動作。

r43 獨立盲審已通過故事關卡；本版只修另外兩份報告定位的來源與畫面問題。Plath 自己的螺絲樣品推車不指定材質或笨重程度，安檢對話只引用他說「拿不下來」，螺絲由旁白另述；車庫畫面從未接合的箱與推車開始。路緣、樓梯、四牌比較及行李轉盤均不補造同地點或事件順序。成品、樣品與 1993 年箱子的提示詞改用獨立完整句；在 `now-pocket` 前完全遮蔽可擴外袋，揭曉後也不指定外袋總數與每袋裝物分布。拉鍊局部不指定箱上部位，航站目擊畫空服員。`source-map.json` 與 `source-alignment.json` 的狀態均應標 r44；r43 三份報告只作改稿依據，不是 r44 核准。

`candidate/video.json` 的公開來源清單只收現行主張引用的 URL；`research-plan-25-series.json` 保存 25 筆較廣的研究提案，未引用來源不冒充正片來源。每筆 claim 都是 `PENDING`。104 事件鏈只作舊基線識別，不是今天正式機狀態；本版不具主機匯入、正式審稿收據或付費媒體授權。MiniMax `image-01` 可愛插圖、可關閉繁中 CC、片頭片尾動畫、A01 US$25 總上限仍是後續製作規劃；紙面估時不是真實 TTS／成片長度。

本機逐條讀過組裝後的 50 條圖片提示詞，並在 builder 加入共用字串語法與揭曉前遮蔽的機械斷言。這只能檢查提示詞；生成後畫面仍須獨立驗收。

可重算輸入閉包：本目錄的 `story-data.mjs`、`brief.md`、`README.md` 與 `reference/r43/` 下凍結的 `manifest.json`、`candidate/video.json`、`candidate/series.json`、`candidate/lexicon.json`、`research-plan-25-series.json`、三份 r43 獨立審稿報告；`reference/snapshot104-host-readback.md` 只釘住過去 104 事件鏈的識別雜湊，不是新主機擷取。builder 鎖定原 manifest 與各必要輸入 SHA；執行時只另讀倉庫已追蹤的 `tools/video/core/{screenplay,timeline,lint}.mjs` 及 `tools/video/automation/story.mjs`。不讀本工作樹的 r24–r43 sibling 未追蹤目錄，也不把複製的 r43 審稿當 r44 核准。`reference/r43/` 是**最小輸入快照**，不是整個 r43 候選的重製；完整 r43 仍在原先隔離目錄。

本機重算：

```powershell
node build.mjs --preview
node build.mjs --write
node build.mjs --check
```

故事須再由不參與撰稿的讀者盲讀，史料、畫面、實際語速與六章正式流程逐項過審。**不得直接匯入、推送、合併、部署、啟動付費或上傳。**
