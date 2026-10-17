# A01 r10 獨立全文審查：HOLD

日期：2026-10-18。審查對象為本目錄 `candidate/`；`manifest.json` 的 SHA-256 是 `6F60A5ECA2E907AB494BC0FCEA44D70B323E7968AC8AE435678C08F7449D5701`。此報告只對該版本有效，不能沿用為後續修稿或正式機六章稿的核准。

審查者逐鏡讀了 65 個場景、76 句口播、74 筆 `claims.md` 主張、11 組登錄回路、64 張靜圖提示詞，並比對 r8 獨立全文審稿與 r9 片長決定。`node …/A01-editorial-candidate-20261018-r10/build.mjs --check` 通過；74 筆場景主張與主張表一對一，沒有缺漏或孤兒 ID；`video.json.sources` 與有來源的主張恰為同一組 16 個網址，解決 r8 的來源索引 P1。這些是**離線資料一致性**結果，不是史實、敘事或成片品質自動過關。

**結論：HOLD。** 沒有發現必須廢棄題目的 P0。下列 P1 須先修，P2 須納入下一版與實音、畫面審查。全部逐句主張仍是 `PENDING`；本檔不是 `story/reviews/script-review.json`，沒有簽發正式審稿收據，也沒有生成圖片、合成配音、讀寫正式機或執行付費製作。

## P1：史料歸屬與公開說明

| 位置 | 問題與證據 | 修訂要求 |
| --- | --- | --- |
| `hook-06`／`jtmg`、`turn-09`，主張 `h6`／`t7`（`candidate/script.md:33,224`；`candidate/claims.md:11,71`） | 口播與主張表說 [Travelpro 沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)記載「1987 年在車庫製作 Rollaboard」。該文直接記 **1987 年直立雙輪拉桿設計**，另記 **1989 年從車庫搬倉**，沒有直接記車庫初作的精確年份；[Plath 本人 2024 年校友刊簡歷，第 17 頁](https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf)寫 1988 年發明。兩個年份尚有分歧，不能把兩條 Travelpro 記載合成它直接證實的「1987 年車庫製作」。 | 將設計年份和車庫經過拆開，明確保留公司歸屬及年份分歧；或只說 1980 年代末的車庫階段。同步改兩句口播、兩筆主張和車庫畫面年代，不以一張插畫證明精確日期。 |
| `candidate/video.json:59` 的 `youtube.description` | 公開說明仍寫「1997／2000 年的四輪設計」，但現行 76 句／74 主張只講 `now-01`／`n1` 的 1997 年。2000 年雖見於 [Samsonite 2011 年招股書年表](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf)，本稿沒有該年的播出主張或解釋；描述不能冒充已審過的影片內容。 | 用現行有主張支撐的 1997 年內容重寫說明；若確要納入 2000 年，先獨立補播出內容、主張與史料覆核。正式機重併企劃時，再核對實際說明欄。 |

## P2：故事、口語與畫面

| 位置 | 發現 | 建議 |
| --- | --- | --- |
| `idea-memory`／`r14i01`，主張 `i35`（`candidate/script.md:80`；`candidate/claims.md:28`） | [Sadow 自述訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)說因帶孩子同行，兩只 27 吋箱塞得滿滿；沒有說箱內**全是孩子們的行李**。 | 改為「因為帶孩子同行，兩只二十七吋箱都塞得滿滿」一類窄說法，主張表同步修。阿魯巴返程與安妮塔一家的故事仍須分開。 |
| `hook-06`／`x7r4` → `now-1993-retail`／`r3n03`（第 5→56／65 鏡；`candidate/video.json:220,1281`） | 大問題「還缺什麼，才能走進旅客日常？」隔約 322.5 秒紙上時間才回收。回收句列出機組採用、旅客看見、1993 年店面有售；[1993 年記者原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)能證明多品牌可買，不能單憑此推出市場銷量或普及率。社會習慣、零售採納與使用設計三道障礙的因果答案要到片尾才明說。 | 在長回路中途用已證實的阻力維持問題，於 `r3n03` 明白回答到哪一步，或將登錄回路限縮為「通路可得」；不要把 1993 年有售寫成已普及。 |
| `now-outro`／`g5b8`（`candidate/script.md:291`；`candidate/video.json:1443`） | 同一句塞入三個障礙、三個解法及無直接傳承的史料但書，共 63 口語單位，300 CPM 紙上約 12.9 秒。整張片尾卡三句約 20.6 秒；若後接預定的獨立 21 秒頻道片尾動畫，收束可能拖長，也壓縮觀眾理解最後因果句的時間。 | 把已查核的因果回答前移到正文最後的轉折或分成短句；片尾卡保留簡短回扣、留言與訂閱。以實際配音／剪輯時間決定，不靠加速語速。 |
| `origin-budget`／`r14o01`、`engine-porter`／`r17e01`（`candidate/video.json:341,722`） | 分別 44、42 口語單位，超過 lint 的 40 單位提醒。`engine-porter` 同時要聽懂 Shiller→助理→Sadow→採購的多層轉述。 | 分句並保留層級，勿把轉述改成採購一手文書。這是口語清晰度問題，非史實 P1。 |
| `hook-06` 與 `turn-09` 車庫圖；`hook-01`、`idea-memory`、`idea-wife` 的 Sadow 連續性 | 兩個車庫提示詞現在指定相同工作檯、燈位和鏡位，解決 r8 的文字規劃缺口；但尚無已核准像素。`traveler-heavy` 角色參照只在 `hook-01` 掛上，其後回到 Sadow 家庭的插畫未掛同一參照。 | 待圖片階段用核准的開場車庫圖作回場參考，聯絡表驗構圖；檢查 Sadow 相關鏡頭能否辨認為同一位匿名故事人物，同時維持「非真人肖像重建」。 |

## 已修復與限制

- r8 指出的 `origin-budget` 車站定位已移除；畫面也不再指定車站。[Winnetka 歷史學會](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)只記搭火車到新地方後安妮塔與孩子守行李，等候地點不明。
- `origin-06` 與 `idea-r12-02` 的重複／難畫技術段落已刪；`now-1993-retail` 已移到記者的個別試箱之前，外袋問句後立刻接她這只箱的結果，與[原報導](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)的個案界線一致。1939 年一場茶會與 1928 年箱子的實物連續性未被說成已證實。
- 300／275／250 CPM 文字代理分別估正文 **439.7／474.6／514.8 秒**。420–480 秒門檻仍須實測旁白；250 CPM 代理已超出。5 秒片頭與 21 秒片尾不可補正文時長。沒有試音、盲聽、生成圖、聯絡表或 720p 成片，因此不能宣稱觀看留存與畫面品質已過。
- 300 CPM 的 lint 無 error，有長句與畫面字詞提醒。`drama-craft` 的角色對話比例、2–4 秒鏡頭等指標對純旁白品牌故事不適用；「logo」「suitcase」頻率多來自負面提示與片題，不能單憑字頻退稿。靜圖長度與視覺變化仍須看實際素材。
- 本地 16 網址索引不能保證正式工人維持同一份來源：現行 worker 會把企劃來源重併，正式機六章稿、來源清單、說明欄、工作與預算必須唯讀核對。可**並行做正式機唯讀資料銜接**；在 P1 修正、再複核、實音與畫面關卡、正式收據及主機安全前檢完成之前，不匯入此候選、不呼叫付費供應商，也不啟動 B18 或後五集。
