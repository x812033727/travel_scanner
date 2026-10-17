# A01 r8 獨立全文審稿：HOLD

日期：2026-10-18。審查對象是凍結的 `A01-story-depth-candidate-20261018-r8/candidate/`，其 `manifest.json` SHA-256 為 `3475E820D22DF7F9D8FD850764D450F17630A2DCDD390949F9147D03062C42B8`。本審查與既有的 r6→r8 **增量鉤子快審**分開；讀了 67 鏡、78 句、71 筆主張、10 組登錄回路與 66 張正文靜圖的提示詞，對照下列原始史料。71 個場景主張參照與 `claims.md` 逐筆一對一，沒有孤兒 ID。沒有生成圖片、試音、盲聽、正式機讀寫或付費呼叫。

**結論：不核准匯入或製作。** 未發現需要廢棄整個題目的 P0；下列 P1 來源索引與 P2 事實邊界、鉤子回收和視覺敘事需修正後重新審查。這不是正式 `story/reviews/script-review.json`，不把任何 `PENDING` 主張改成 `CONFIRMED`。

## P1：可公開來源索引與逐句主張不一致

`candidate/claims.md` 使用 16 個不同的來源 URL，`candidate/video.json.sources` 只列 13 個；其中 **8 個實際引用的來源漏列**，另有 5 個列出的來源沒有被這 71 筆主張引用。漏列包括 [1939 年 Midland 當地報紙](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)、[Winnetka 第一趟旅行文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)、[Winnetka 家族資料](https://www.winnetkahistory.org/who-were-the-burnhams/)、[2008 年 Yale Shiller 講稿](https://oyc.yale.edu/economics/econ-252-08/lecture-3)、[2011 年 Yale Shiller 講稿](https://oyc.yale.edu/economics/econ-252-11/lecture-3)、[Emmer 本人回憶，PDF 第 46–47 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)、[Travelpro 時任執行長訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)與[1993 年《洛杉磯時報》記者實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)。

未被目前 71 筆主張引用的清單有 NASA Apollo 11、維基百科行李箱條目、Ms. Magazine 關於 Katalin Karikó 的文章、US2392926A 舊專利，以及 Smithsonian 的二手回顧。前 3 項尤其與本片無關。`tools/video/core/metadata.mjs` 的 `composeDescription` 會直接把 `video.sources` 寫進上傳說明，故這不只是工作檔整潔問題。修訂版須用**已審過的逐句主張**重建來源清單，再重跑打包檢查；不要把 r8 的增量快審冒充全文來源 PASS。

## P2：逐鏡修訂項

| 場景／句 ID | 發現 | 建議與證據界線 |
| --- | --- | --- |
| `origin-budget`／`r14o01`，主張 `o30` | 旁白說安妮塔在「車站」帶四個孩子守行李，畫面也指定 1921 年車站候車區。[Winnetka 歷史學會記錄](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)說搭火車抵達新地方後，丈夫去找便宜住處，安妮塔與孩子、行李等候；沒有逐次指明等候地點就在車站。 | 旁白刪「在車站」；畫面改成未定位的旅途中等候，避免把合理推測拍成確定地點。 |
| `hook-06`／`jtmg`、`x7r4` → 登錄回收 `turn-09b`／`3zwf` | 開場真正的問題是「還缺什麼，才能走進旅客的日常？」；`turn-09b` 只揭露直立雙輪伸縮拉桿。旅客採用與通路證據仍在 `now-crew-request` 至 `now-1993-retail`。現在的回路表把大承諾提前標成已回答。 | 保留外形揭露為一個中途答案；在機組、旅客和 1993 年零售證據處明確回扣開場，再把大回路的 payoff 指到那個真正回答的句子。[Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage/)、[時任執行長訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)、[1993 年一手測試](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html/)各自只能證其陳述的階段。 |
| `origin-06`／`83ew` → `idea-memory`／`r14i01`，且呼應 `hook-01`／`3rdw` | 開場已交代 Sadow 提兩只沉箱；`origin-06` 又說一家提傳統箱，下一鏡才新增阿魯巴返程、兩只 27 吋和孩子行李。連續兩鏡在重建同一負擔。 | 合併時代轉場與新增的阿魯巴／尺寸細節，讓每句提供新資訊。[Sadow 當事人訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)可支持新細節。 |
| `idea-r12-02`／`r12e02` | 口播解釋專利把箱蓋與箱身合成底面兩半；提示詞卻要求把底部藏起來，只顯示普通箱頂部和提把。聽者無法從畫面理解這句偏技術性的描述。 | 若此專利差別確實推動故事，展示與[專利文字／圖](https://patents.google.com/patent/US3653474A/en)一致的剖面或底部示意；否則刪去這句，把時間留給採購阻力。不要讓 MiniMax 猜讀專利圖。 |
| `now-consumer-question`／`r3n01` → `now-1993-stow`／`r4n01` | 問觀眾外袋多裝後是否放得進機艙，答案前插入 `now-1993-retail`／`r3n03` 的通路概述，暫時離開記者與同一只箱子。 | 將零售資訊移到問句之前，或在記者試箱結果之後承接通路擴張；維持問句後連續追蹤同一只箱子。[記者原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html/)分得清一般市場敘述與自己的外袋個案。 |
| `now-outro`／`g5b8` | 收尾列「自製、進貨、改直立」，但標題問的是輪子早有、為何普及仍等很久。列表沒有直接說清社會習慣、零售採納及可使用設計各自阻礙了哪一步。 | 用一句能聽懂的因果回答標題，再接留言與訂閱；只綜合片中已獲證實的阻礙，不宣稱 Anita、Sadow、Plath 有直接發明傳承。[Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)、[Plath 專利](https://patents.google.com/patent/US4995487A/en)、[1993 年記者測試](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html/)的證據層級應維持分開。 |
| `hook-06` 與 `turn-09` 的畫面提示 | 兩鏡各自描述一間泛稱車庫，但沒有指同一張已核准圖片／相同構圖。開場預告的車庫未必能在後段讓觀眾認出，削弱長回路的視覺兌現。 | 在製作分鏡時以同一張已核准圖或可驗證的同一構圖回收，再在 `turn-09b` 揭露直立設計。這是提示詞審查，尚無生成像素可判。 |

## 鉤子與片長判讀

開場有 Sadow 的機場場景，加上 Anita、百貨採購、Plath 車庫三個不同時間的預告，並未提前揭露採購結果或完成的直立拉桿。`hook-anita`／`r17h01` 在 `origin-1939-case`／`r3o01` 回收時，只能說 **1939 年一場**茶會現場報導記她帶有輪箱；不能說那是 1928 年同一只實物或 1928–1939 年逐年連續使用。[1939 年原報](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)支持目前旁白的窄說法。

`validation.json` 在 300 口語單位／分鐘的**文字代理**下，67 鏡共 443.1 秒，來源事件標記最長間隔 40.4 秒；這不等於每一段都真的留得住觀眾。10 組登錄回路中，`r12t01→3zwf` 只有 21.4 秒、`r15n02→jspd` 15.5 秒、`r3n01→r4n01` 25.8 秒，屬短轉折，不能算成 10 個有重量的延遲鉤子。明示問句最長相隔 131.7 秒；不宜只為湊 45 秒插入假問句。需要以實際台灣口音音檔、分鏡與不知稿情的聽者確認事件轉折和答案是否足以維持 7–8 分鐘。`e37u→r14i02` 的「Sadow 說了一句話」回收只是預期中的「行李也該裝輪子」，特別需要聽者測試其前段留存價值。

站主已改 A01 為約 7–8 分鐘，但 **r8 凍結檔仍是 `target_minutes: 9`，舊 `validation.json` 仍標 540 秒門檻 HOLD**；後續 r9 的片長決定應獨立於本文件。若沿先前試音約 300 單位／分鐘，r8 的紙上旁白 443.1 秒，加 5 秒片頭、21 秒片尾約 **469.1 秒（7:49）**；275 單位／分鐘則是 478.2 + 26 = **504.2 秒（8:24）**。這些不是實際 TTS 或合成成片秒數，也不能拿片頭片尾補足正文門檻。

## 核對過的史料邊界

- [Winnetka 輪箱收藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)記 1928 年兒子用舊嬰兒車兩輪和木製伸縮把手改箱、丈夫譏笑；[家族資料](https://www.winnetkahistory.org/who-were-the-burnhams/)記第二趟家族旅程與母女用畫換餐宿。[1939 年當地原報](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)記一場茶會的斗篷、帽子、輪箱；它不證同一實物或逐年使用。
- [Sadow 本人 2010 年受訪](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)記兩只 27 吋箱、機場輪板、樣品、百貨遭拒、Macy 副總裁試拉與人偶展示；[1970 年 2 月提交的專利](https://patents.google.com/patent/US3653474A/en)支持四輪、拖帶及底面構造。[Yale Shiller 2008](https://oyc.yale.edu/economics/econ-252-08/lecture-3)講助理打給 Sadow 聽來的 porter 理由，還有自己用過拖帶箱會搖擺；[2011 講稿](https://oyc.yale.edu/economics/econ-252-11/lecture-3)泛論轉角翻倒，不能當第二次個人測試。
- [Emmer 本人 2016 年回憶，PDF 第 46–47 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)確認既有 Jet Eze 輪袋、Plath 欣賞上層取物又嫌做工、向製作者展示草圖、兩週後遭婉拒；文中沒有標明這段與[Plath 安檢回憶](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)的先後，也不能把兩種箱體或 Shiller 自用的箱子畫成同一物。[Plath 1989 年申請專利](https://patents.google.com/patent/US4995487A/en)談外置推車反覆拆裝的限制。
- [Travelpro 公司的回顧](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage/)寫 1987 年設計、1989 年搬倉、1991 年離職；[Plath 自己的 2024 年校友刊簡歷，第 17 頁](https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf)寫 1988 年發明。r8 口播把 1987 歸給 Travelpro，未說兩者已定讞；下一版也不可無歸屬地講成唯一確定年份。
- [Travelpro 時任執行長 2007 年訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)記同事請 Plath 代做；[2010 年《紐約時報》文章，重印在 RNPA PDF 第 48 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)記空服員帶動可見度；[1993 年記者實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html/)的外袋收納失敗只是一只箱的一次測試；[Samsonite 2011 年招股書第 80 頁](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf)記其 1997 年平衡四輪直立箱。2010 年空服員談過度裝箱是她的觀察，不能嫁接到 1993 年記者的動機。

此稿的主線「多位互不確證有直接傳承的人，各自處理拿、賣、拖穩與機艙使用」在史料下可以成立；上述修訂完成、逐句來源重整、實音與分鏡盲評過關前，**A01 仍 HOLD；B18 和後五集未受本審查核准。**
