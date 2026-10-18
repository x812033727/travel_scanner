# A01 r18 盲讀與限縮史料抽查 — HOLD

- 日期：2026-10-19。
- 審查者：Codex 獨立盲讀者。先完整讀 `candidate/script.md`，未看既有審查、主張表或來源映射；其後才對照 `candidate/video.json`、`candidate/claims.md`、`source-alignment.json` 與下列原始來源。
- 綁定 r18 `manifest.json` SHA-256：`6228FA78CBB686E01E10A5B1053204A53B71F248FCDA93AE364C501CCE518B4C`。
- 綁定口播稿 `candidate/script.md` SHA-256：`42088C3BDDFEF3422FC9AA9E49F7FF68EF532693D533C289D685F079B1A2CABF`。
- 綁定 `candidate/video.json` SHA-256：`41DE853C3A1E05BD40463B060ABEB72757B64AD1171B9959666A8A75841A4E31`；`candidate/claims.md`：`8770EB08C5B621CEA4903103CC6B2B51B0F6A058B45EA75435DD6273FA2DF787`；`source-alignment.json`：`EB445C5198F5E8B5D37B4BC335711579F6C3ACFFB4284CDD2654142159D52BA5`。
- 結果：**P0 0、P1 1、P2 3；HOLD。** 這份收據不是全部 73 筆 `PENDING` 主張的正式查核、正式機劇本核准或 `story/reviews/script-review.json`。

## 盲讀意見

故事由 1928 年家庭自製輪箱、1970 年 Sadow 的百貨推銷、Plath 對機組與安檢難題的處理，推進到 1993 年旅客實測。開場的安妮塔旅後是否仍帶箱、樣品能否上架、安檢員如何回答，以及「輪箱為何尚未走進日常」均有後文回收。章序與台灣華語用字大致順口，沒有發現需把三人寫成直接師徒傳承的理由。

以下 P2 是離線編輯意見，不是事實錯誤：

1. `engine-porter` 第 26 鏡首次說「Shiller 說」，沒有交代他是誰；後面 `engine-wobble-01/02` 再引用他的個人用箱經驗，第一次可簡短介紹身分。
2. `turn-09/jm3w` 的 1987／1988 差異已各自歸屬來源，卻正好落在安檢回覆的揭曉之後，口播節奏略停。可試聽後決定是否保留在旁白，或將差異放進來源字卡；不可抹平未定年份。
3. `now-outro/g5b8` 的「三人的故事沒有可證實的直接傳承」是必要的史實界線，但片尾口語較書面。可考慮在 1939→Sadow 轉場交代，再讓結尾專注回收「願意拉、買得到、用得順手」。

`validation.json` 的文字代理估時為 436.0 秒（300 單位／分）、470.6 秒（275）、510.3 秒（250）；這不是 TTS 或剪輯量測，不能判定實際旁白已達 7–8 分鐘。也沒有聽音、看圖片聯絡表或成片。

## P1：安檢揭曉場景漏綁主張

`turn-05/crcw` 說 Plath 在安檢隊伍看到旅客費力處理箱子與金屬推車，掛 `t5`。現有 `t5` 的完整主張是：Plath 受訪回憶前方旅客解彈力繩、把箱子從外置金屬推車卸下；與 Emmer 未標年份的草圖回憶無法排定先後。`t5` 的企劃來源索引為 **5**，公開索引為 **10**，URL 為 [2012 年 Plath 受訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)。

下一鏡 `turn-06/iu9y` 才明說「箱子用彈力繩綁在笨重的金屬推車上；旅客得解開繩子，再把箱子卸下來」，但 `candidate/video.json` 該鏡 `claims: []`。內容本身有受訪報導與 [Plath 1989 年專利](https://patents.google.com/patent/US4995487A/en)的背景支持；問題是關鍵揭曉鏡頭沒有自己的場景級事實綁定。現有 `source_index_matches_claims: true` 只證既有 73 筆來源索引互相對得上，沒有偵測到這一漏綁。

下一份**隔離候選**的最小清楚修法：保留 `t5` 給 `turn-05`，新增一筆綁 `turn-06` 的主張，明列彈力繩與卸箱，引用同一受訪 URL／來源索引；重算主張數、`source-map.json`、`source-alignment.json`、manifest 與審查收據。不要將專利的一般限制說成其已獨立證實那位特定旅客的動作。r18 原候選未在本審查中修改。

## 史料抽查與未覆核範圍

- [Winnetka 歷史學會的輪箱收藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)支持兒子以舊嬰兒車輪與木把手改箱、丈夫嘲笑、旅後繼續帶輪箱；[另一館方文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)支持 1921 年低預算旅行與等候行李；館方 [Burnham 家族頁](https://www.winnetkahistory.org/who-were-the-burnhams/)支持母女以繪畫換餐食或房間。1939 年 [Midland 當地報紙](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)搜尋擷取支持黑斗篷、實用帽與帶輪箱出席茶會。
- [2010 年 Sadow 第一手訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支持波多黎各機場輪板、四腳輪拖繩樣品、百貨拒絕與 Macy 副總裁試拉；[耶魯 Shiller 2008 課堂逐字稿](https://oyc.yale.edu/economics/econ-252-08/lecture-3)支持搬運工異議與他自己的左右晃擺經驗，[2011 課堂](https://oyc.yale.edu/economics/econ-252-11/lecture-3)支持轉彎可能翻倒的概述。
- [2012 年 Plath 受訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)與其 [1989 年申請的專利](https://patents.google.com/patent/US4995487A/en)支持安檢推車困擾；[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)記 1987 年，[Plath 自填的 2024 年校友刊第 17 頁](https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf)記 1988 年。這是來源分歧，稿件有歸屬，未把任一年當定讞。
- [Judi Dash 1993 年親測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)明列四家受測品牌，並說相關型號在主要百貨**或**行李專門店可買、Travelpro 起初郵購、外袋放衣物和書後無法收進座位下或頭頂櫃。`now-1993-retail/r3n03` 的「或」與單次實測界線相符。[Samsonite 公司文件](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf)支持 1997 年平衡四輪直立箱；[Travelpro 樓梯比較](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)只支持「有些旅客」的困難。

以上是**抽查**，不是 73 筆逐項復核。RNPA 2016 年 Emmer 回憶 PDF 本輪只讀到搜尋擷取的前段，未逐頁核查後段草圖與拒絕細節；Chinook 第 17 頁以官方校友會 PDF 的搜尋擷取核對，未直接下載大檔逐頁比對。所有正式主張仍待獨立完整查核。沒有實際配音、付費圖片、主機接續、正式收據、成片或上傳；保持 **HOLD**。
