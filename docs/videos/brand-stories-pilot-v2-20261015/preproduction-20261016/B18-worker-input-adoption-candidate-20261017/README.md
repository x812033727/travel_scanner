# B18 最終分鏡對應的 worker 輸入資料列候選

**狀態：離線結構候選；獨立資料列／來源審查、正式 worker、主機匯入與付費製作全部 HOLD。**

本目錄只從 `../B18-claim-granularity-candidate-20261017/` 精確雜湊凍結的最後版本產生新的單集 `B18.json`。原 `episodes/B18.json`、`episodes/reviews/B18.json`、已編譯 `stories.json`、正式站和媒體均未改。`build.mjs` 不寫匯入檔、不呼叫網路或模型。

## 這一版解決什麼

- 分鏡的 `series.plan` 已有六個來源和十三筆故事要點；匯入 `storyProblems` 僅允許 `must_verify` 四至十筆。候選資料列用十筆**代表性必查主張**，將首店時地和店面／售價合在同一筆，沒有刪除分鏡的任何逐景主張。
- [claim-coverage.json](claim-coverage.json) 列出全部 **65 筆逐景 `UNCHECKED`** 主張：42 筆同時映到代表性必查主張與原來源、23 筆只綁原來源。每筆保留原 `scene`、來源索引與原十三筆的 fact 索引；新索引僅是候選資料列的對照，**沒有反寫原分鏡或冒充正式查核**。本目錄另有 [series-adoption.json](series-adoption.json) 與 `remapped-chapters/` 六章隔離副本，供後續採用路徑審查。副本只改了 19 個 `claim.fact` 指標；65 筆主張的文字、景號、來源、`UNCHECKED`、所有場景與旁白保持不變。離線 `composeStory` 前後產生完全相同的影片文件。
- 原十三筆中，索引 9 的舊市場數字、索引 11 的給茶設備年份分歧不在最終口播；兩者仍明列於對照和 caveat。來源陣列保持六筆、順序與 `series.plan` 完全相同，避免把逐景的索引指向別的出版者。
- 原資料列以「1978 年一項權利期滿」驅動轉折；本候選照[日本法院判決理由](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)的第 579776 號實用新案 **1972 年**期滿，將 J-Net21／發明協會的 1978 年版本留作未解來源差異。沒有把所有新業者出現歸因於單一年份。[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的後場直線路線、[石野集團年表](https://www.ishino-group.com/history/)的 1980 旁通／1986 ㄇ字型路線，分別屬於後來的不同業者或設備，不說成元祿首店同一台機器的連續改裝。[機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)的 1985 年堺東店機器和另存的早期板片也維持兩件物件。

## 機械驗證和邊界

`node build.mjs --write` 只產生本目錄的候選資料列、對照、隔離副本與驗證結果；`node build.mjs --check` 重算並逐位元組比對。它先驗父版 manifest 的 SHA-256 `1016d3de91236af487eec891e256f43214d71a06ba806409084831f47584e198` 與全部列舉檔案，再檢查官方 `storyProblems`：**零問題**。候選的 canonical story SHA-256 是 `29993db8333f26ea5df68c09137f0b0cae924056602e7c1e49a1dfb2cbb9c059`；舊 B18 審稿收據被 `reviewProblems` 以內容改動明確拒絕。只在記憶體中核對 A01/B18 兩列的序號與 series 形狀，沒有產生可匯入的 `stories.json`。後端 `check_story_file` 對記憶體中的兩列也回 `problems=[]`、`refused=[]`；這只表示結構可讀，不表示可匯入正式站。

這些是格式和對位檢查，不是獨立史料審查，也不代表來源頁本次已全部重讀。候選的 `sources[].checked` 保留父版的實際日期。法院 PDF 的關鍵日期可能在正式工人端只以企劃 `supports` 出現，獨立 reviewer 還須決定新收據的 `reviewer_only` 範圍。**新 B18 row 必須另有獨立、hash 綁定的 `reviews/B18.json`，再重編兩集匯入檔。** 真工人對所有 65 筆逐景主張的查核、聽眾審稿、十三題敘事關卡、TTS 片長、插圖／CC／成片及站主觀看仍各自待辦；#1518 的作者章稿採用路徑另有既知阻擋，不因本 row 變有效。

逐項審查請見 [review-request.md](review-request.md)。
