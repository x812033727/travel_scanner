# S53 R1｜獨立史料與題材可行性覆核

2026-10-20 UTC。**題材 A 可行、固定來源核對 PASS；這不是完整劇本、逐句主張或插圖簽核。** 本覆核未修改作者的 `brief.md` 或 `research.md`，以下兩項用語須在全稿前收窄。

## 固定對象與重開方法

| 對象 | SHA-256／核對 |
| --- | --- |
| [brief.md](../brief.md) | `4b5d5761b4bde467dbc1e9a70482c7df76046a442b560329063e03bb91871ec7` |
| [research.md](../research.md) | `a099f81971d834c2d95042bb17c3500ce818d20c273b4419bb8b72b3e0478eef` |
| 作者的 [R：1913 救濟調查](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt) | 從固定提交另行下載，HTTP 200，`d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；與暫存 clone 逐位元相同 |
| 作者的 [C：1906 新聞編書](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt) | 從固定提交另行下載，HTTP 200，`4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`；與暫存 clone 逐位元相同 |

讀的是兩本固定原文，而非作者引文。R 的書名頁與序言 [L205–283](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L205-L283)證明其為 **1913 年六人編纂的救濟調查**，兩位作者曾任救濟機構職務；住房篇 [L10183–10220](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10183-L10220)說明 1908 年訪查、會議紀錄、個案紀錄和剪報的使用。它對機構數字與決定有直接價值，但沒有獨立證成每個決定的第二份原檔。本次未取得可直接重開的公園委員會會議原檔，正片提及清場要求時須寫成「1913 年救濟調查記載」。C 的營地敘述 [L2588–2623](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt#L2588-L2623)無具名報導者、用語誇張，只可有歸屬地說「當年編書描寫……」，或不用。

## 逐項核對

| 作者主張 | 獨立結果與原文定位 |
| --- | --- |
| F01 地震與大火 | PASS。R [L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)寫 4 月 18 日 5:12 及隨後大火；不要由此推出傷亡總數。 |
| F02 帳篷與尋人告示 | **僅有歸屬背景 PASS。** C [L2591–2609](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt#L2591-L2609)如此描寫；「九成帳篷」及「數千紙條」是這段的修辭，不能當計數，亦不能重演有姓名個案為已核事實。 |
| F03 5,610 建造 | PASS。R [L4855–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4855-L4870)寫 9 月 10 日動工；[L10450–10460](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10450-L10460)寫至 1907 年 3 月 19 日建成 5,610 棟（4,068 三房、1,542 二房），另有 19 棟二層公寓。是各營地總數。 |
| F04 租約與購屋契約 | PASS，須分先後。R [L4899–4930](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4899-L4930)先講租約設計；住房篇 [L10482–10500](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10482-L10500)明說市有地收租受特別條例阻擋，改為按月付的買賣契約，符合條件者後來獲退還款項。勿說居民一律免費或一律已付清；開頭「屋子是居民的」須寫出附條件取得與遷走的關係。 |
| F05 臨時用地與清場 | PASS，限 R 的記載。R [L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)明說委員會**無正式准許權**，1906 年 8 月 17 日同意一年內不干預；[L4983–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4983-L4994)載 1907 年 6 月提出 8 月 17 日清場要求。未如期完成。 |
| F06 遷屋與 Lobos Square | PASS。R [L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994)列承租或買地、自費遷屋，也列延遲、驅離／拆屋；Lobos Square 留到 1908 年 6 月 30 日兼有貧困戶安置與衛生管理因素，不能全歸於住戶不願搬。 |
| F07 5,343 遷出 | PASS。R [L4998–5026](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5026)列 5,343 棟搬出，絕大多數作住宅，也列慈善機構搬修。這是搬屋數，不是買地戶數或永久保留數；不能把剩下 267 棟擅自定義成拆毀。 |
| F08 訪查、買地與扣屋 | **數字 PASS，樣本須分開。** R [L10502–10520](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10520)寫嘗試查 1,137 個搬出小屋的地址，取得 680 份較完整紀錄；其餘 457 未取得紀錄中，報告**另知** 23 起因地租被地主取走。70 戶買地才是 680 戶受訪者中的數字，[L10997–11005](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10997-L11005)。`research.md` 的「當中僅 70 戶買地，23 起……」文法容易誤認兩數同母體，全稿必須拆句。 |
| F09 偏好 | HOLD 百分比，非主線必需。R [L10974–10979](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10974-L10979)的原句是「558，或 82%，**曾住出租房間者**偏好舊住處」，但 [L10821–10848](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10821-L10848)另列 680 戶中 15 戶原有房屋、661 戶原住處類型；558／680 約 82%，而出租房間子集合的分母未明。作者已把 82% 排除正片；維持排除，亦不要把 558 當全體災民比例。 |

## A 案敘事與畫面界線

本題與目前集數企劃、開票搜尋未見同一場事件的單集。A 案有可按時間敘述的六個轉折：1906 災後安置、9 月建屋、租約改買賣契約、1907 清場要求、1907–08 遷出、1908 訪查。原文在每個轉折都有日期、制度或後果，可支持約 8–11 分鐘的**待撰稿與計時**故事；目前沒有全稿，不能宣稱長度已達標。

**全稿前必修兩句：**(1) 企劃 A 說要解「房子究竟怎麼搬」；R 只證成有搬遷、付費、慈善機構與部分木工參與，[L10932–10944](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10932-L10944)給價格，**沒有**可核的搬運機械步驟。懸念改成「誰付搬遷費、要搬往哪種土地？」(2) `research.md` F08 拆開 70／680 與失訪部分中的 23，讓旁白不混母體。

畫面可用原創可愛示意的一棟普通二／三房小屋，及「營地 → 租／買的地」概念卡；R [L10887–10911](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10887-L10911)有營地密集屋列、木地基等大致背景。不得畫成可考證的某戶、偽造個人清場通知、發明搬運工具、把全數小屋放進金門公園，或讓模型生成可讀契約。日期、數字與出處交後製卡片；原創插圖不是當年的照片。

**下一關：**作者修上述兩句並寫全稿及逐句主張／分鏡，再做另一位工作者的逐句史料與書面畫面覆核、兩位盲讀、政策與旁白關卡。此 PASS 只讓題材進入撰稿；不核准媒體支出或上架。
