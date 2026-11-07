# C06 Play-Doh｜r2 獨立來源與書面配鏡查核

查核日：2026-10-25。來源與全文覆核者：`/root/c03_admission_current`；完整書面配鏡協查：`/root/c03_admission_current/c06_r2_written_visual`。兩位均未撰寫這份中文稿，未讀敘事盲讀、讀者答案或panel內容。

**結論：SOURCE PASS／WRITTEN VISUAL PASS。** 本輪完整重讀167句、141個shot prompts及1個outro；不是只解除r1兩項問題，也沒有承接r1的歷史HOLD作為通過。

## 綁定輸入

| 輸入 | SHA-256 |
| --- | --- |
| video.json | `3384f25844ebcf4ab2eedc9b1131e2cc873bae0df79da16d96c78153b82dc616` |
| script.md | `ef59781aafdf9c65ab708e65852af00b8237d705d31ee444d5dda1d9fbf833c9` |
| narration-only.json | `fd88f5a342dd791fbb7e2488f1322eb598cb3e00e05ac57ac7ef774651ed4df7` |
| claims.json | `d1fe2be51929af1388869b364269c80409d15a0fe2b2710840ff254156224490` |
| reviews/source-r2-independent.json | `4a379cbf7648fc343c9092da905bf6ddb237e8e02f09a69f19a574a07193ee50` |

167句的ID／文字／順序與video、narration-only、作者script、claims一致；claims與source-anchors的逐句來源及逐景投影一致。逐句文字SHA、實際原件bytes SHA、精確段落／PDF頁欄及全部逐景結果保存在上述JSON收據。

## 原件與實際讀取

沿用2026-10-25已實際HTTP 200讀取的原件快取，本輪重新讀取其內容並核對bytes SHA；未冒稱另發新的網路請求。P1原始PDF另重讀全文及第3、4頁掃描影像。

| 原件 | URL | 實際bytes | 原件SHA-256 |
| --- | --- | ---: | --- |
| H1 | https://newsroom.hasbro.com/node/34691 | 35397 | `12c3a40ee1f8b19012447903cfbcad820ee55bc6e80fde8cd494b948b164ee78` |
| H2 | https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent | 36534 | `faf0487550b58005ae7f073583ab5a07f9cdabab37cc769e966884d3be8d8cfc` |
| H3 | https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience | 34631 | `59479f5fd92ec190bccbf0dad30d3be50d096ccab14b36ad5f8e5b193f1a1392` |
| K1 | https://www.kutol.com/kutols-story/ | 314017 | `e703d65813edf4c52278228a431f9394b953f88cd3e96239b15bf2252ad2a209` |
| M1 | https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/ | 415288 | `704a6072eefcdab78b8a1d52ee49c23d936ac67a5ace7b3566cdc1f14db42fc4` |
| M2 | https://www.toyhalloffame.org/toys/play-doh/ | 399913 | `5295caa008a71a3c7a618974131735d7c316022171ef4868e4278b9a93969b77` |
| P1 | https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf | 699681 | `725a8c64f41c4eedd8c69202e047e19f447f49eadd3adcb1e8708c0faaab27f6` |

M2實際重開快取的SHA為5295caa…，與早期研究表7139f858…不同；本輪依實際快取第162段核對，不將早期研究表的bytes冒作新讀取。G2先前503／404且沒有raw bytes，本輪未重讀；G1、G2、H4、H5均未被現稿167句引用，不借它們證明現稿。

## 核心界線

- 1933的Kroger故事、1949接手、1955教師提議及設備沿用，均保留公司／館方回顧歸屬；未聲稱讀到1933原始合約或同期教室紀錄。M1與M2屬同一The Strong機構。
- Kay姓名與姻親身分由K1第108段及M1第163段支持，M2第162段另支持黏土過硬與送校試用。1956為Rainbow Crafts／校園推廣及公司回顧的品牌生日，非已核首單。
- 1957紅黃藍與較柔軟材料、Captain Kangaroo至少每週使用的安排、1960兩位工程師與Fun Factory低力擠形，均直接核對館方原文；不加精確電視合約日、費率或銷量因果。
- P1保型稠度在claim 9。1960年5月申請與1965年1月核發分開；後出的專利不是1933、1955或今日每罐的完整配方證明。
- 混合／熱水／均勻糊化團塊／攪拌機型非關鍵／製造後立即密封，皆為P1所述製法。黏結成分為可選；包覆機制保留作者認為／文件描述。沒有寫成獨立實驗、現代工廠見證或DIY配方。
- 最長三年是P1對密閉保存並玩後放回的文本聲稱，未改為今日效期或本次實測。空氣乾硬、可上色與充分乾硬後不能重揉的取捨，亦限於該文本描述。
- 2024逾五億為公司年出貨罐數；2026成人線首個定位、套件步驟及噴霧維持數月均保留公司公告歸屬。不加入健康療效、銷售成功或授權計畫已落實的推論。
- 硬黏土圖明確呈現firm clay受挫，之後才轉pliable材料；粒子與攪拌圖為概念模型，密封圖不冒作保存試驗。全部配鏡匿名、無真人品牌名、無可讀偽史料或實際歷史場面重建。

## 逐句來源表

PASS代表本句在其回顧／公告／專利主張／假想／觀點界線內有充分依據；不將假想、觀點或來源自己的性能聲稱升格成獨立實驗事實。無任何旁白或作者檔案由本覆核者修改。

| # | 位置 | 句子 | 精確anchors／URL | HTTP | 判定 | 改動 |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | c6sh001 / c06r2-h00 | 如果你捏的形狀，手一放就垮，還會再拿這罐嗎？ | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 2 | c6sh021 / c06r2-h02 | 孩之寶二〇二四年說，Play-Doh年出貨逾五億罐。 | H1-scale；[H1](https://newsroom.hasbro.com/node/34691) | 200（當日快取） | PASS | 無 |
| 3 | c6sh011 / c06r2-h01 | 想像你在一九五〇年代的辛辛那提，正打開一罐壁紙清潔材料。 | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 4 | c6sh031 / c06r2-h03 | 但在你眼前，牆上的煤灰正在變少。你取出材料，手感還好好的，卻得找個理由， | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 5 | c6sh032 / c06r2-h03-p2 | 讓人再次打開這罐。 | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 6 | c6sh041 / c06r2-h04 | 我覺得最棘手的，是材料還能用，原本的工作卻正在縮小。 | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 7 | c6sh051 / c06r2-h05 | 有一雙更小的手，正被另一團材料難住。 | M2-hard；[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 8 | c6sh061 / c06r2-h06 | 另一張桌上，一束剛做完的花，還得過最後一關。 | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 9 | c6sh071 / c06r2-h07 | 今天跟著Play-Doh，追一團材料怎麼在不同人的手上留下來。 | K1-kay、P1-store、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[K1](https://www.kutol.com/kutols-story/)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 10 | c6sh081 / c06r2-h08 | 拿它的手換了，它究竟要替那個人做對什麼？ | K1-kay、P1-goals、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[K1](https://www.kutol.com/kutols-story/)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 11 | c6so011 / c06r2-o01 | 開場那罐材料，得先接到一份清潔訂單。史壯玩具博物館把故事的這一步， | M1-kroger；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 12 | c6so012 / c06r2-o01 | 放在一九三三年。 | M1-kroger；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 13 | c6so021 / c06r2-o02 | 克里奧・麥克維克替Kutol接下克羅格的生意，要做現成的壁紙清潔材料，放到商店裡賣。 | K1-cleo、M1-kroger；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 14 | c6so031 / c06r2-o03 | 麻煩的是，館方說他們以前沒做過這種東西。訂單到手了，誰把材料做出來？ | M1-kroger；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 15 | c6so041 / c06r2-o04 | 依這篇回顧，負責產品開發的兄弟諾亞拿出了配方；柔軟、像黏土的清潔材料， | M1-noah；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 16 | c6so042 / c06r2-o04-p2 | 就接上了這份工作。 | M1-noah；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 17 | c6so051 / c06r2-o05 | 如果你家牆面沾了煤灰，手裡這團能變形的材料，就有了一個要處理的目標： | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 18 | c6so052 / c06r2-o05 | 牆上那層髒污。 | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 19 | c6so061 / c06r2-o06 | 想像你把它攤開，再收回手心；你在意的是，手上這次動作，能不能讓那片壁紙好看一點。 | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 20 | c6so071 / c06r2-o07 | 我覺得，這時候你需要留下的，是剛才那團形狀嗎？ | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 21 | c6so072 / c06r2-o07-p2 | 牆面乾淨，這個動作就能收手；手裡的外形，只是過程。 | M1-wall；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 22 | c6so081 / c06r2-o08 | 館方接著記下，一九四九年克里奧去世，兒子約瑟夫接手了生意。 | M1-1949；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 23 | c6so082 / c06r2-o08-p2 | 輪到他想辦法讓公司繼續做下去。 | M1-1949；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 24 | c6so091 / c06r2-o09 | 但一筆生意，能不能只靠原來那面牆，一直做下去？ | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 25 | c6so101 / c06r2-o10 | 回到開場那面煤灰變少的牆：館方說，二戰後家庭改用燃油或天然氣，到了五〇年代初， | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 26 | c6so102 / c06r2-o10-p2 | 壁紙清潔材料的銷售開始下滑。 | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 27 | c6so111 / c06r2-o11 | 如果你家的煤灰問題少了，這罐東西就可能留在櫃子裡；它做得到原來的工作， | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 28 | c6so112 / c06r2-o11-p2 | 也未必等得到你再買一罐。 | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 29 | c6so121 / c06r2-o12 | 我覺得，這比做壞一批貨更難想：材料還在，原本要處理的麻煩卻變少了， | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 30 | c6so122 / c06r2-o12-p2 | 再努力擦同一面牆，也找不回那個需求。 | M1-demand；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 31 | c6so131 / c06r2-o13 | 你若接住約瑟夫手上的材料，會讓它去見誰？ | K1-kay、M1-kay；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 32 | c6so132 / c06r2-o13 | 有沒有一雙手，根本不打算拿它擦牆？ | K1-kay、M1-kay；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 33 | c6sk011 / c06r2-k01 | 這雙不想擦牆的手，來自幼稚園。Kutol的公司史裡，老師凱・祖法爾是約瑟夫的姻親。 | K1-kay、M1-kay、M2-hard；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 34 | c6sk021 / c06r2-k02 | 博物館把她提出手工用途，放在一九五五年。還記得開場那雙小手嗎？ | K1-kay、M1-kay、M2-hard；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 35 | c6sk022 / c06r2-k02-p2 | 名人堂說，一般塑形黏土太硬，孩子不好操作。 | K1-kay、M1-kay、M2-hard；[K1](https://www.kutol.com/kutols-story/)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 36 | c6sk031 / c06r2-k03 | 想像你要做一隻小動物，連身體都壓不出來，耳朵怎麼接？ | M2-hard；[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 37 | c6sk032 / c06r2-k03 | 作品還沒出現，手就先被難住了。 | M2-hard；[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 38 | c6sk041 / c06r2-k04 | 名人堂回顧，約瑟夫送材料讓老師試；Kutol記下她把它帶進幼稚園，受到了歡迎。清潔材料， | K1-kay、M2-hard；[K1](https://www.kutol.com/kutols-story/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 39 | c6sk042 / c06r2-k04-p2 | 碰上了要塑形的小手。 | K1-kay、M2-hard；[K1](https://www.kutol.com/kutols-story/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 40 | c6sk051 / c06r2-k05 | 換到容易推動的材料，你可以先壓一個身體，再接上一對耳朵；這樣的用途， | M2-hard、M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 41 | c6sk052 / c06r2-k05-p2 | 有沒有真的讓經營者看見？ | M2-hard、M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 42 | c6sk061 / c06r2-k06 | 博物館接著寫，約瑟夫到學校看了孩子的作品，回去把產品重新調整、改作玩具， | M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 43 | c6sk062 / c06r2-k06-p2 | 使用原有的設備和製造空間。 | M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 44 | c6sk071 / c06r2-k07 | 我喜歡這個具體的來回：他到桌邊看做出了什麼，再把這種用途帶回製造的地方， | M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 45 | c6sk072 / c06r2-k07-p2 | 材料的評分方式已經變了。 | M1-kay；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 46 | c6sk081 / c06r2-k08 | 教室願意用，下一步由誰把它當玩具來做？ | M1-brand、H2-birthday；[H2](https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 47 | c6sk082 / c06r2-k08 | 館方把Rainbow Crafts的成立，放在一九五六年。 | M1-brand、H2-birthday；[H2](https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 48 | c6sk091 / c06r2-k09 | 那是Kutol的子公司，向辛辛那提一帶的小學推廣Play-Doh； | M1-brand、H2-birthday；[H2](https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 49 | c6sk092 / c06r2-k09 | 孩之寶也把品牌的誕生放在這一年。 | M1-brand、H2-birthday；[H2](https://corp.hasbro.com/news-releases/news-release-details/hasbro-trademarks-favorite-smell-childhood-play-doh-scent)、[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 50 | c6sk101 / c06r2-k10 | 但你做出一隻鳥，還想替它選嘴巴的顏色，只有原來那一團，夠不夠？ | M1-colors、M2-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 51 | c6sk111 / c06r2-k11 | 一九五七年，館方記下紅、黃、藍加入；名人堂的回顧還提到，材料變得更柔軟。 | M1-colors、M2-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/)、[M2](https://www.toyhalloffame.org/toys/play-doh/) | 200（當日快取） | PASS | 無 |
| 52 | c6sk121 / c06r2-k12 | 你現在可以挑一小塊，讓嘴巴和身體不同色；想法不再只靠外形表現，選哪一塊接上去， | M1-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 53 | c6sk122 / c06r2-k12-p2 | 也成了創作。 | M1-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 54 | c6sk131 / c06r2-k13 | 我覺得，顏色最有意思的地方，是它讓你做選擇。材料不是只等著被壓扁， | M1-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 55 | c6sk132 / c06r2-k13-p2 | 它得跟得上你想做的東西。 | M1-colors；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 56 | c6sk13a1 / c06r2-k13a | 但光把罐子交到你面前，你會知道能做什麼嗎？ | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 57 | c6sk13a2 / c06r2-k13a | 這時，讓人看見手怎麼動，也成了一件工作。 | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 58 | c6sk13b1 / c06r2-k13b | 更麻煩的是，博物館說約瑟夫沒有大筆廣告預算；他便和《袋鼠船長》的主持人安排， | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 59 | c6sk13b2 / c06r2-k13b-p2 | 至少每週在節目裡用一次產品。 | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 60 | c6sk13c1 / c06r2-k13c | 如果你坐在電視前，看見材料被壓、被接起來，原本密封在罐裡的東西， | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 61 | c6sk13c2 / c06r2-k13c-p2 | 就有了可以照著試的動作。 | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 62 | c6sk13d1 / c06r2-k13d | 我覺得，這種展示讓材料多走了一步：你不必先想出一整套玩法， | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 63 | c6sk13d2 / c06r2-k13d-p2 | 可以從看見的一個動作開始，再改成自己的作品。 | M1-television；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 64 | c6sk141 / c06r2-k14 | 可是，如果你想再替作品加一排細長條，每根都慢慢搓，要怎麼讓它們長得像你要的樣子？ | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 65 | c6st011 / c06r2-t01 | 剛才要你慢慢搓的長條，可以改從一個出口擠出來；博物館把Fun Factory這件工具的推出， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 66 | c6st012 / c06r2-t01-p2 | 放在一九六〇年。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 67 | c6st021 / c06r2-t02 | 館方說，約瑟夫請兩位工程師開發能有多種用途的配件，結果是用不大的力氣， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 68 | c6st022 / c06r2-t02-p2 | 把材料擠成不同形狀。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 69 | c6st031 / c06r2-t03 | 想像你先放進材料，再壓下手柄；原來要靠手指一段段搓出來的形狀， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 70 | c6st032 / c06r2-t03 | 現在讓材料通過出口。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 71 | c6st041 / c06r2-t04 | 那你是不是什麼都不用做了？ | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 72 | c6st042 / c06r2-t04 | 擠出來的長條，要放在哪一個位置，還是得由你選。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 73 | c6st051 / c06r2-t05 | 你可以想像，拿一段圍在作品旁，試試彎成一圈；工具替你做出形狀，接下來怎麼組合， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 74 | c6st052 / c06r2-t05-p2 | 作品才會變成你的。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 75 | c6st05a1 / c06r2-t05a | 如果你這次只需要短短一段，出口能替你決定長度嗎？ | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 76 | c6st05a2 / c06r2-t05a | 這又得回到你手上。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 77 | c6st05b1 / c06r2-t05b | 想像你讓材料伸出一小段，取下來，試著放到作品旁；還不夠長，就再壓一次。你控制何時停， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 78 | c6st05b2 / c06r2-t05b-p2 | 長度才跟著眼前的用途走。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 79 | c6st061 / c06r2-t06 | 我喜歡這個分工：手不必包辦每一段細節，卻沒有把選擇交出去；一個小出口， | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 80 | c6st062 / c06r2-t06-p2 | 改掉的是你施力的方法。 | M1-factory；[M1](https://www.museumofplay.org/blog/the-history-of-play-doh-good-clean-fun/) | 200（當日快取） | PASS | 無 |
| 81 | c6st071 / c06r2-t07 | 還記得開場你手一放，形狀就垮的問題嗎？ | P1-header；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 82 | c6st072 / c06r2-t07 | 工具幫你擠出來，放開後的形狀，材料自己得接住。 | P1-header；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 83 | c6st081 / c06r2-t08 | 同在一九六〇年五月，諾亞和約瑟夫提出一件美國專利申請，受讓人列Rainbow Crafts。 | P1-header；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 84 | c6st091 / c06r2-t09 | 它談的是兒童玩耍用塑形材料，寫下了玩具要面對的要求。 | P1-header；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 85 | c6st101 / c06r2-t10 | 你擠出的長條，本來要接在作品旁；假如放下就變扁，連把它搬到作品上的那一下， | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 86 | c6st102 / c06r2-t10-p2 | 都得重新想辦法。 | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 87 | c6st111 / c06r2-t11 | 但若材料硬得推不動，又回到那雙小手的困境；這件申請，究竟只顧你動手， | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 88 | c6st112 / c06r2-t11 | 還是也顧你放手？ | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 89 | c6sb011 / c06r2-b01 | 這兩個要求，在一九六五年一月核發的文本裡被放在一起：材料要可塑， | P1-header、P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 90 | c6sb012 / c06r2-b01-p2 | 也要有能保留形狀的稠度。 | P1-header、P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 91 | c6sb021 / c06r2-b02 | 對你來說，意思很直接：動手時能改它，放開以後，又希望看得出自己剛才做了什麼； | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 92 | c6sb022 / c06r2-b02-p2 | 只往一邊走，都會卡住。 | P1-shape；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 93 | c6sb031 / c06r2-b03 | 但你只准自己做這一次嗎？ | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 94 | c6sb032 / c06r2-b03 | 如果明天想把動物變成船，材料還得替你留什麼？ | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 95 | c6sb041 / c06r2-b04 | 文本把慢乾、可以反覆改形列為目標；捏完一個東西，並不必把材料下一次能做的事， | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 96 | c6sb042 / c06r2-b04 | 一起用掉。 | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 97 | c6sb051 / c06r2-b05 | 我覺得這是很寬容的玩法：你可以推翻剛才的決定，再從同一團開始；不滿意， | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 98 | c6sb052 / c06r2-b05-p2 | 不一定要換一份材料。 | P1-goals；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 99 | c6sb061 / c06r2-b06 | 可你把它從桌上拿起來，另一個問題就來了：手和桌面都黏住，作品還能好好移動嗎？ | P1-clean；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 100 | c6sb071 / c06r2-b07 | 所以，乾淨、不黏手、不沾染，也是這份專利明列的要求；你玩完後怎麼把材料帶走， | P1-clean；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 101 | c6sb072 / c06r2-b07 | 也在設計裡。 | P1-clean；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 102 | c6sb081 / c06r2-b08 | 它要自己合成一團，碰到你的手又別黏著不放；專利作者怎麼解釋這個差別？ | P1-film；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 103 | c6sb091 / c06r2-b09 | 他們認為，烴類餾分會包覆固體顆粒，形成薄膜；文件把柔軟、滑順和不黏的觸感， | P1-film；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 104 | c6sb092 / c06r2-b09 | 連到這層包覆。 | P1-film；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 105 | c6sb101 / c06r2-b10 | 文件再描述，包覆的麵粉顆粒經濕熱糊化，合成柔軟、均勻而不結塊的材料； | P1-film；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 106 | c6sb102 / c06r2-b10-p2 | 這是作者對其組成的解釋。 | P1-film；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 107 | c6sb111 / c06r2-b11 | 那裡面要怎麼合成一團？ | P1-binding；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 108 | c6sb112 / c06r2-b11 | 文件還允許加入有黏結作用的成分；表面要滑順，裡面也得合得起來。 | P1-binding；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 109 | c6sb10a1 / c06r2-b10a | 可是一碗分開的材料，怎麼變成你手裡均勻的一團？ | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 110 | c6sb10a2 / c06r2-b10a | 文件裡還有製造時的動作。 | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 111 | c6sb10b1 / c06r2-b10b | 它描述用攪拌機混合材料，再把熱水與其餘成分拌成均勻團塊； | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 112 | c6sb10b2 / c06r2-b10b-p2 | 甚至舉出一般麵糰攪拌機，說機型不是關鍵。 | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 113 | c6sb10c1 / c06r2-b10c | 想像你正壓出一片平面，指下突然遇到硬結塊，還能照原來的力氣推嗎？ | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 114 | c6sb10c2 / c06r2-b10c-p2 | 製造時追求均勻，到了桌面上才有意義。 | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 115 | c6sb10d1 / c06r2-b10d | 我覺得，從攪拌機到你的手，這裡接得很清楚：前面得讓材料一致，後面你才不用每捏一處， | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 116 | c6sb10d2 / c06r2-b10d-p2 | 就重新猜它肯不肯動。 | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 117 | c6sb10e1 / c06r2-b10e | 在文件的製法裡，材料混成可塑團塊後，立刻放進密閉容器；還沒交給玩的人， | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 118 | c6sb10e2 / c06r2-b10e-p2 | 保存這件事就已經開始。 | P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 119 | c6sb121 / c06r2-b12 | 還記得前面替小鳥挑的嘴巴嗎？ | P1-color；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 120 | c6sb122 / c06r2-b12 | 如果加了顏色，卻把容易下手的手感弄丟，這個選擇還划算嗎？ | P1-color；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 121 | c6sb131 / c06r2-b13 | 文本也要求，能加入不同顏色，而不影響可塑性；讓你選外觀的同時，材料還得配合塑形。 | P1-color；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 122 | c6sb141 / c06r2-b14 | 還記得製造後立刻收起材料的容器嗎？ | P1-store、P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 123 | c6sb142 / c06r2-b14-p2 | 玩到這裡，你要去做別的事了；這次用剩的，還能回得去嗎？ | P1-store、P1-mixing；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 124 | c6sb151 / c06r2-b15 | 文件寫到，玩過後也能放回密閉容器。你蓋上的，不只是今天剩下的一團， | P1-store；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 125 | c6sb152 / c06r2-b15-p2 | 也是下次改主意的機會。 | P1-store；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 126 | c6sb15a1 / c06r2-b15a | 蓋起來，只是留到明天嗎？ | P1-store；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 127 | c6sb15a2 / c06r2-b15a-p2 | 文本聲稱，這樣保存可讓可塑性與工作特性，最長維持三年；同一罐東西， | P1-store；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 128 | c6sb15a3 / c06r2-b15a-p3 | 還有以後被打開的日子。 | P1-store；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 129 | c6sb161 / c06r2-b16 | 那如果你偏要把成品留在外面呢？ | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 130 | c6sb162 / c06r2-b16 | 這份文本，也描述了另一個方向。 | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 131 | c6sb171 / c06r2-b17 | 它說，材料放在空氣中幾天會乾硬，乾硬後可以上色；但充分乾硬以後， | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 132 | c6sb172 / c06r2-b17-p2 | 就不能再揉回原來的狀態。 | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 133 | c6sb17a1 / c06r2-b17a | 你若等作品乾硬後再上色，顏色落到的是已經定下來的外形；你可以改表面， | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 134 | c6sb17a2 / c06r2-b17a-p2 | 卻得接受下面那個輪廓不再任你揉。 | P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 135 | c6sb17b1 / c06r2-b17b | 還記得剛才替鳥接上去的黃色嘴巴嗎？ | P1-color、P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 136 | c6sb17b2 / c06r2-b17b-p2 | 那時你把色塊揉成形，現在則能在乾硬的作品上下筆；選哪個時機，連手上的動作都不同。 | P1-color、P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 137 | c6sb181 / c06r2-b18 | 假設你今天做了一艘船，你得選：把材料收起來，明天重新做，還是接受不能重來， | P1-store、P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 138 | c6sb182 / c06r2-b18 | 留下眼前這件。 | P1-store、P1-dry；[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 139 | c6sb201 / c06r2-b20 | 如果你決定留下作品，而且想把它擺進家裡，最後這一步，有沒有另一種產品來幫你？ | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 140 | c6sn011 / c06r2-n01 | 這個留下來展示的方向，到了二〇二六年七月，被孩之寶放進一套成人花藝產品； | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 141 | c6sn012 / c06r2-n01-p2 | 公司稱它是首個專為成人設計的系列。 | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 142 | c6sn021 / c06r2-n02 | 我覺得有趣的，是你這次買回來，要完成的是一束能放進生活裡的花；成人的手， | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 143 | c6sn022 / c06r2-n02-p2 | 有了被明確安排的動作。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 144 | c6sn031 / c06r2-n03 | 一團材料，怎麼變成整束花？ | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 145 | c6sn032 / c06r2-n03 | 公告裡的套件，從花瓣開始帶你做。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 146 | c6sn041 / c06r2-n04 | 工具和模具幫你塑形，再把花組起來，最後排成花束；官方還提供每款的教學影片， | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 147 | c6sn042 / c06r2-n04-p2 | 讓步驟跟著套件一起到手。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 148 | c6sn04a1 / c06r2-n04a | 假設你第一次做花，先只管眼前這片花瓣；模具讓你有個可以靠近的形狀， | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 149 | c6sn04a2 / c06r2-n04a-p2 | 手再把細節調到自己想要的位置。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 150 | c6sn04b1 / c06r2-n04b | 可做完一朵，為什麼還沒結束？ | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 151 | c6sn04b2 / c06r2-n04b | 你得把它放進整束裡，看它和旁邊的花要怎麼站。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 152 | c6sn04c1 / c06r2-n04c | 想像你拿起一朵，往旁邊移一點，再把另一朵靠近；這時候改的已經不只是單片形狀， | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 153 | c6sn04c2 / c06r2-n04c-p2 | 而是整個擺在桌上的樣子。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 154 | c6sn051 / c06r2-n05 | 想像你挑好位置，把花放進瓶子；做第一片花瓣時，你想調整，整束排好以後， | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 155 | c6sn052 / c06r2-n05-p2 | 你卻想讓它別再亂動。 | H3-kit；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 156 | c6sn061 / c06r2-n06 | 還記得開場那束要過最後一關的花嗎？ | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 157 | c6sn062 / c06r2-n06 | 現在花束已經排好，要怎麼把這個形狀留下？ | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 158 | c6sn071 / c06r2-n07 | 孩之寶說，套件裡特製的最後處理噴霧，能幫花維持結構數月； | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 159 | c6sn072 / c06r2-n07-p2 | 這是公司對這款產品的保存說明。 | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 160 | c6sn081 / c06r2-n08 | 我喜歡它和剛才那個蓋子的對照：前面收起材料，是替下一回留餘地；這裡， | P1-store、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 161 | c6sn082 / c06r2-n08-p2 | 最後一步要保住的是你已經選好的位置。 | P1-store、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 162 | c6sn091 / c06r2-n09 | 你若把它放到自己的桌邊，材料的工作，只到你放手的那刻嗎？ | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 163 | c6sn092 / c06r2-n09-p2 | 它要進入每天看得到的地方，完成後的用途也跟著改變。 | H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience) | 200（當日快取） | PASS | 無 |
| 164 | c6sn101 / c06r2-n10 | 回到開場那罐等待被打開的材料，我的答案是：它得先接住眼前這雙手，真正要完成的事， | K1-kay、P1-store、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[K1](https://www.kutol.com/kutols-story/)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 165 | c6sn102 / c06r2-n10-p2 | 才有下一次被需要的機會。 | K1-kay、P1-store、H3-display；[H3](https://newsroom.hasbro.com/news-releases/news-release-details/hasbro-introduces-blooms-play-doh-new-creative-experience)、[K1](https://www.kutol.com/kutols-story/)、[P1](https://patentimages.storage.googleapis.com/04/b2/91/3e71db79829152/US3167440.pdf) | 200（當日快取） | PASS | 無 |
| 166 | c6snct1 / c06r2-outro | 如果是你，會把一團材料反覆揉回去玩，還是留下一件完成的作品？留言告訴我，你最想做什麼。 | — | — | PASS（editorial CTA） | 無 |
| 167 | c6snct2 / c06r2-outro | 想繼續看熟悉的日用品，如何被使用者推著換工作，歡迎訂閱這個頻道。 | — | — | PASS（editorial CTA） | 無 |

## 書面配鏡表

141個shot逐一核對當景旁白、動作、材料與匿名界線；兩位覆核均PASS。只覆核生成前的文字計畫，不宣稱已看成圖。

| 場景 | prompt SHA-256 | 判定 |
| --- | --- | --- |
| c06r2-h00 | `2696feadfc7141ef84a2e3b140c94d5e0267e3aae541c99c6ac56392c05502e0` | PASS |
| c06r2-h02 | `acf6b8ae1a7320f0bc168761a09165c537a50163ac96e10950ed36ca124bc82c` | PASS |
| c06r2-h01 | `05d6690a12c0e89b4adf9753a7e0d4d03a8297a7678034910d67f9217d61a784` | PASS |
| c06r2-h03 | `4258702091ceef5346f0fe3d77686541dd4860a1b3d39b7446adc87b5317e379` | PASS |
| c06r2-h03-p2 | `c96cbd3c7e235b77f00ca0563497a65067c955e5bc003ed9e97a235f6a212ddd` | PASS |
| c06r2-h04 | `391c57e97d470516d300ede898d252e74a868a313f59200b1d237ecfa391f7f0` | PASS |
| c06r2-h05 | `0af781c474f545c454774b57a044954e99d216698ca8b28d72d8f024e0d5ced7` | PASS |
| c06r2-h06 | `2501ca3b07dd91c9d12395f85130844e6a65546750aeb91d7d1f9e93fd4075de` | PASS |
| c06r2-h07 | `bc000d4dd3ff62ac9a5af6074e025535981c6ffb9faa0c98fb24ce4f36ee03f1` | PASS |
| c06r2-h08 | `af72121466316f5823bf229623ccc459197a1dd82d252c64355c1258ad669537` | PASS |
| c06r2-o01 | `e944ace3f7ca9454469fd908d8e0dd1ec971874a260200ffcefecce48a6289f3` | PASS |
| c06r2-o02 | `93f338c72a98765e154cf8aa8545e40ecd626e4bee725373645f2835d4ccd26b` | PASS |
| c06r2-o03 | `1880aa70f4769ba4afb8c9578cfd05803172fb7e9e89409d944c52346fc800b3` | PASS |
| c06r2-o04 | `9153f15118de72a28c1da877a2fb1c1848e8501189853d9392906cf97d045d28` | PASS |
| c06r2-o04-p2 | `b1cc0f0e70fbaede0a363b86bef8a949e7212a0fa173cdcfbf670fe69b0d543f` | PASS |
| c06r2-o05 | `dd4d53fadf856c2a499093234ab5afcb93e17d8b9a506ed894575e5896f2ab52` | PASS |
| c06r2-o06 | `189a19371eb7527a09bd300981b29891b4ba807bdf2ee6cf5620365d6676c50e` | PASS |
| c06r2-o07 | `cf1c36c22eb06ded582d6fc4cfd2f24abe5d99d2b1933c9314c1250012d69ebf` | PASS |
| c06r2-o07-p2 | `609cb67db48a54ec1f0a5692def3b1451e460f154d1a671a675ef01e0d189a44` | PASS |
| c06r2-o08 | `a8b510efeb026cdf4ad39ab7ce9eb2764c2b06d4d9272b03b63f78fd91bdf091` | PASS |
| c06r2-o08-p2 | `cce5cbdfe753193b75e3e35e464931a9f04d1c2a7ca6e4a3380fa1e66b2f7877` | PASS |
| c06r2-o09 | `ddd36542fd4212de7a5a89e36a3cf1ca79afaaee65fe33f2b87a981e81431396` | PASS |
| c06r2-o10 | `8904858de3adf568781bdb8cc9cb3447d34f892beaae7bee1f76dfc16fd7f0c7` | PASS |
| c06r2-o10-p2 | `ec3d21067d0abd5861a1c8bbd8cdb08a4841ae3f3924f635e74a8fcbcde6c35c` | PASS |
| c06r2-o11 | `d53028a0b53dacedb4cc23248f253941d21041a43895e26c8b8a1d0fa6d7ab96` | PASS |
| c06r2-o11-p2 | `18ed7046812c61f94d3989ee7518cb5c8f853e4ea475c03affb8f7ba1afc2f78` | PASS |
| c06r2-o12 | `b80c1d559baad6fb0352dc682302ce79dfcd7f131560dc7ba8ea37f99067926d` | PASS |
| c06r2-o12-p2 | `9e0d8e2b1aec8308829a0e4de6401b753c917fc66fc4764b36f839a1e478923c` | PASS |
| c06r2-o13 | `c0bbacb6214e3e0287898e729e46bbcb30cd57965595a269736a26e2dd99cfc6` | PASS |
| c06r2-k01 | `1aca5626495d8cae8666eb6b1a335584970d919e4754be81ff35f13deac4c0dc` | PASS |
| c06r2-k02 | `d9f21435b6bba457b466441d45e474a1f0f48bde8873878dc1928a6ef7609337` | PASS |
| c06r2-k02-p2 | `a5d45131155e7525f16e05c19e5f393b342e51b58b849823bdda35936866cb59` | PASS |
| c06r2-k03 | `2613b1db562e38b6bd7a37a3ff04d3489d25ccedca8b507570586a1f69924b82` | PASS |
| c06r2-k04 | `e2f714743f687b3035a31e408d14e65eb5f68ab342afd549afcfa46518f4b260` | PASS |
| c06r2-k04-p2 | `e5249d356bbd9a43bbfa618f425785737317f5d0bbe201733b85e562c9d14cb2` | PASS |
| c06r2-k05 | `9f1f4a50fac867f3c8511fdaf2a8260746e49b7436bf4c9712484ae70abe68e4` | PASS |
| c06r2-k05-p2 | `6aa5f20ade09cd12fcc53133afa2c6aeb779ae0ecab8e069889a723d7be0676c` | PASS |
| c06r2-k06 | `70f355863b41c2b02a4e51465ef48d8d16d66e0282631e449729dc374e9c096b` | PASS |
| c06r2-k06-p2 | `946875bc9e01e81a145b5aabcbd56fcd7d1fa76e1b60672ec9ded1068a1c31e9` | PASS |
| c06r2-k07 | `343f4f9fd3261f6eaad3e9490ea645f2ff8439946d6d1e0acda6db0e365b6b99` | PASS |
| c06r2-k07-p2 | `629dc83abafb989cc4e1be608ddc4e5f3271b2d7fb88b8483f279159e841f4e3` | PASS |
| c06r2-k08 | `bfdf03fccf71933093646d142632a2664f0653663e2ed409d832612871683a1b` | PASS |
| c06r2-k09 | `a583b6095a02fc419d91eaaaab9503aef6ea4d9552eb34a9743641674c1cf85f` | PASS |
| c06r2-k10 | `a4357ecf808d1e115584d06262695049a96718560e13f031836dfb6612b79177` | PASS |
| c06r2-k11 | `f24cfbebd1b02d3714843daa90ad6058e1ef969667ca6662f232a9c6dd137077` | PASS |
| c06r2-k12 | `79317e86a3943ba97eba900b9ebc79dc25aa5e532d29615eac034a35eacb9ec3` | PASS |
| c06r2-k12-p2 | `58121f791a04509f31281029a9268a86d3f9b12a61a043a8621c5bfdb691aaa9` | PASS |
| c06r2-k13 | `0575f93e9ba1e17927f14bdcc3ed4cef3996bef4533b65dc0a2cb47f32056216` | PASS |
| c06r2-k13-p2 | `69541778ddfc13894a284df538b813793c13902e2fe4ac6f480e8dc519df5f96` | PASS |
| c06r2-k13a | `ee96f1a910e6af090356f38e6075d004cc3015b2b437007b5cdb90d01fbcd4c2` | PASS |
| c06r2-k13b | `0557670a881a89bb82834769392b3a1aa807dc29a65d2e9e7e2e3749b130222d` | PASS |
| c06r2-k13b-p2 | `8e0d2f9766cdff714b77bce9001d8a163e45f22d39249497ac11a1071f40f4a7` | PASS |
| c06r2-k13c | `d5e12631f80c0b728f803633f1f92a221652935e008fea97c12e6ac84f933775` | PASS |
| c06r2-k13c-p2 | `ec292983fe0d0acfd6d246e1e9c03d55fee61832d87ba68f3e3d8e6adabab6ff` | PASS |
| c06r2-k13d | `17f01cead40acb7d1fc84a1fbb3884150dc4262fafdc3e5ea6efd98a941595cc` | PASS |
| c06r2-k13d-p2 | `fd6d3b9b690c172d37e98bf77ec8a6b443f77f9f9ea88b3547bd8fd2b2834a77` | PASS |
| c06r2-k14 | `72af29c0c2f9c5df2f5b0e6d3d4499fc8c931b02f30188f89238617ae9a5b349` | PASS |
| c06r2-t01 | `92ecfe97baacc777a2e4f4f10a93a3892dfd8b3148971ff6d8eeaa1a7a286e58` | PASS |
| c06r2-t01-p2 | `ec70b2b8f9f3ae5c3ddf63edb39c619716a51ec47a052337ee9db83674146cae` | PASS |
| c06r2-t02 | `0b3a66671b448f1c98fab11336321d990150636d314bf16dbd62357d18f1a41e` | PASS |
| c06r2-t02-p2 | `4a2fb132a47a627dddadd3b4ab4af73a23ea1b59fe12d7283900c6f12ce04453` | PASS |
| c06r2-t03 | `509ddb2f62a3525716a64b3a8a9e126df6a873b23c43ab900dc46d7b75c7d723` | PASS |
| c06r2-t04 | `310dcdcf823a86d4952bd3252fc01bf7be3f5b652a46de45966f944adc3f3a0e` | PASS |
| c06r2-t05 | `9c5dd2bc8dc45f6847c571f3ab1e800d1ec55813cf2fa4ad3beb1b29200cee94` | PASS |
| c06r2-t05-p2 | `bb1eb4cff478f190cee751e8ac762384e3d7347b67fd9f505a563231e61e8ddf` | PASS |
| c06r2-t05a | `dac0558f75c9e61adbec15d6de25f97c2d9b849dbec19a79cadccd2d6114a765` | PASS |
| c06r2-t05b | `9d7043fad49b5bcc7b7254a20c2dfacdbe1fb3278581d5ce405b12c8abe5a9a2` | PASS |
| c06r2-t05b-p2 | `060707a98ccf43246234fc34af4bcc280a0a06f032c98a45fc0e1a9868bc0504` | PASS |
| c06r2-t06 | `df47660ac89258fe727f45b2b3a8193ddb20561f799e316ef0ba43bbcb8f2db8` | PASS |
| c06r2-t06-p2 | `b995be5406e4586e9836830e7c6fcaf026aa935dcdee6528128fd047c1a8f30c` | PASS |
| c06r2-t07 | `9af96a25a0ff8e6f720c0999d91cf299d9b3ecbfa114f1175f1354b0044e50ef` | PASS |
| c06r2-t08 | `f42eae4c8c1fc3d9a81bf768642638d10d938bf46cbf4c8bc151004c71845a78` | PASS |
| c06r2-t09 | `2b745c1bebb6c4a33ec6a8a2b09491368c7a0eb63f103cbca0d441c089a6005b` | PASS |
| c06r2-t10 | `f951de7384ae48c858f503bf359e887f32fdf5d0c22f7effa17e6fbe9f37df53` | PASS |
| c06r2-t10-p2 | `52e97e779ef9c4bb44b6835cfbee66455d06d8485cf3d1d3351bab3047913b97` | PASS |
| c06r2-t11 | `1423015d548798ddc60f29c7e16b85579c39582a9796b37c7866fc2bf5cdb3aa` | PASS |
| c06r2-b01 | `a58ca75b4470672fad055e989895d66eda527f463afd0787a397201a4b76ef23` | PASS |
| c06r2-b01-p2 | `c17a33654c842040a0bd9f0b55ecbebf6cd2af860a12963e24ebd2d7f61d254a` | PASS |
| c06r2-b02 | `fcab70f7d6f80177bd7fec36b832174859e4b2b13b9428d0e9bbb8bc8d60043a` | PASS |
| c06r2-b02-p2 | `a3c0093b3aa67cd10469d1b46ae6e2d23aca91537cf548a890b42b504b37a1a7` | PASS |
| c06r2-b03 | `b0366ca76c7dda742470769207e3ca3b5d4c4d2d9220658d17ee09dead45140f` | PASS |
| c06r2-b04 | `2bb46c15ccafb41ed3b4b278cc4d51e22f847736aa9e94dff49868191f91a156` | PASS |
| c06r2-b05 | `0398dc5e31a51f77e0a00a0eda211afcea2e1bf568fe16078e61fdc16cf3ddc0` | PASS |
| c06r2-b05-p2 | `248039128da8e34147501fab7957397df535c85ca3a3f31ecae7d9574a18aee9` | PASS |
| c06r2-b06 | `0be1d130a373610cd74934cd3c3bfeee5c7d241aaeadc3c5e6d73a3fa02eb97d` | PASS |
| c06r2-b07 | `e318f1358b5ca38e9dc75f63ccba0d876333898f83821e8b0783a46c9fd54fc0` | PASS |
| c06r2-b08 | `90237ae205f3fd3156939c3353832a78f961c91b090d4385c4ae142e4e247b43` | PASS |
| c06r2-b09 | `67ab619ae7d481577e0d80e9461a8d28bc670f1a2ccab06ef97e9773dd0e6f71` | PASS |
| c06r2-b10 | `56eec3153b4a1cb1bef490ad183a3fb9f491823efc43c489d8f3b8a325ed1fcc` | PASS |
| c06r2-b10-p2 | `b2128a82373682a321418869620c5ab02d6ca3879a909f0e26833e192b507171` | PASS |
| c06r2-b11 | `f1aabb9d64879b28d943933c626cd5d3d3fb0a84ff8cea3a872bd8a25a35c920` | PASS |
| c06r2-b10a | `e08e7e8c5135007e066fd0e73ff3a14a1fc1e1a5152a18e11b20a2ab48667565` | PASS |
| c06r2-b10b | `4717b6ed2d6d53857ed3944a927a8d25aeb0c903cacb08c7ac47545ca2802d16` | PASS |
| c06r2-b10b-p2 | `b05721c03e8c0604b3a2896429ae96e5645cf4bb5c153c0e4bf9c9cb529654ae` | PASS |
| c06r2-b10c | `cb14a990be016123269045a245094d00faaa9c39adb63c840e8b1da4c93fc7e7` | PASS |
| c06r2-b10c-p2 | `44c28e162b4617de2b7e05b00bffe2c9a464b77db2ca1d7803219553e01eb657` | PASS |
| c06r2-b10d | `8ff886e654fa1718991b8fd0c4e52908819a21d0a1870c1ebb8dd9b0ab768f4b` | PASS |
| c06r2-b10d-p2 | `3e04cff7f856a7bd906a9dba7424e10bef2f82f39c84c3382197cdbb4276b0dd` | PASS |
| c06r2-b10e | `e2e3b3dfa96cd2d8667f0d40e2a508e14760e7c238ffb78abeb44391a05bf903` | PASS |
| c06r2-b10e-p2 | `8f09c1cf44f852751477c18489a8debedcb4b129fd134bbfe1072018a3bb0efb` | PASS |
| c06r2-b12 | `5dab24bc692a8cdec479bb3e941ef77a6c3855f598ae84733ba9ea4ee9b2a907` | PASS |
| c06r2-b13 | `49cc4643ae084846d95126d0663d4a2c142fd1b5976b58141e39adc395a944eb` | PASS |
| c06r2-b14 | `78c054b817bef690fc5582a26df7a3647f250838cc79ead6b7646cb261c8b74b` | PASS |
| c06r2-b14-p2 | `5b6827f53de5e2e4be1e4622725241d28150546475380c658b9ecc7fbbc275a4` | PASS |
| c06r2-b15 | `b0f5c45b48d5c8198bffcf1b36de64b45f67d1daa6b8b09b43460ffa6e00a8ce` | PASS |
| c06r2-b15-p2 | `8d33291ab9b019d6c0fd33bea074925c0c7c9cb3da72cada67a05668bc498393` | PASS |
| c06r2-b15a | `b297e19101208c286e6d4d66357e9b1d00ae7ae27e98fb926b80ca755e4647de` | PASS |
| c06r2-b15a-p2 | `2b3cd470dbbc2c41db59ae5f2d263978b21c48dfd69d7b65fa779013e862d297` | PASS |
| c06r2-b15a-p3 | `8f8c30bdacccc936e4cf4d3cf89f36701b0a7760c5500d140aa358ae0eaac71f` | PASS |
| c06r2-b16 | `ecc3275ced887956f46f91fd8014093c65de25dbe2ad0c9e200f5b815b9519f4` | PASS |
| c06r2-b17 | `1055de45ad1b135a131353098eb153d871d82c210581cca2b5093bbd35c2f761` | PASS |
| c06r2-b17-p2 | `1c1c86b97e2ae4ff6ae9f68df1c35ad4e75d4c11d7107e8b78d1746aa6033594` | PASS |
| c06r2-b17a | `cee06e921780b7a3ca2979a13e0d4b9950a18356dfd26a9da03d9344a4527412` | PASS |
| c06r2-b17a-p2 | `c3a56bc2c10cf5aa44f121aef3758d4a888f94721ec2bd72e24e166b9314495b` | PASS |
| c06r2-b17b | `a3cdcaab7f9e255ca250617529d27c70aa0d1d37d9d1ad3e332417943fe341d4` | PASS |
| c06r2-b17b-p2 | `6d03fa9a74fc77aa4892076afff346dc15bf032ff88c15bfb4f4fc15f0d5e7d4` | PASS |
| c06r2-b18 | `b29d2bbe3378b5d5a59e7be142484022dcd7d56da1651d1c27cd2e128fcf27c9` | PASS |
| c06r2-b20 | `5a1d53a305ae026fd05cbeecddd30aba8a50e3a13443095b6b099a56d1453bc9` | PASS |
| c06r2-n01 | `00467d81101ed6d7bbf89907ea55229c47a97f51ecb2990c0726f16650ffcfee` | PASS |
| c06r2-n01-p2 | `951aee5b1554233bb54d79b8f43c095f33baf100e555741b50c7dad2ccf6d3a3` | PASS |
| c06r2-n02 | `3f9ee720a0f729160943cda0a62fce39fe743f8a71354f7f680e027f28e7f456` | PASS |
| c06r2-n02-p2 | `b28c46ad58a3420b128360b96bf286699f44368e34fa10813d526db5dc8ddac9` | PASS |
| c06r2-n03 | `44315399ae916503eee678bda5094d133c0069b2fb12742ae473c1cf8f3343ae` | PASS |
| c06r2-n04 | `bdd76cce1fd55a7558b2dcf2f070f54e25bf1a3cab469915b5fa7cd9bbd6afb1` | PASS |
| c06r2-n04-p2 | `e9b8bf827ff2b9a58cb6898a1721918926c5d25737348e97dc7cca6571462891` | PASS |
| c06r2-n04a | `26a05512471e6798ec822da917752a3f56dd4d3bf3026e92c6487942e46b085c` | PASS |
| c06r2-n04a-p2 | `d3339464fefb7ee2105fe8062582c0893f36fa61696cdd2db3a84942903bebc3` | PASS |
| c06r2-n04b | `ce05c30643f7b928ca0a71b69c9428db68cd3a72b2dff5411a9e53503021ad2f` | PASS |
| c06r2-n04c | `9f9e31082430e5e93e1c78be9ff2b9a2fc8e1212f6898220a0efb544e4b9e69f` | PASS |
| c06r2-n04c-p2 | `7a62d796f91e86356b3b9f131c500ea5d96d9e86ac332ce7f9e152e8ebbdbae3` | PASS |
| c06r2-n05 | `9b1a47821c64859b7040c78e71b43c51bf1ea1acbe3413ac91e3009f8749b231` | PASS |
| c06r2-n05-p2 | `ded3ebd9ae84cafb67c5d10f665fcee95f4bc70973bd98e17f97a8c2d21c6347` | PASS |
| c06r2-n06 | `5dde4aed2a08614492ba45dfd35140ae54d153984a37d98d646a0fc755b7cd07` | PASS |
| c06r2-n07 | `6365eef752af28f345ce8410e23725c598be3f33c4cd1f3e51ff8a1ca4a26cd1` | PASS |
| c06r2-n07-p2 | `714f9cdd6aa9c9c5e7f77a89c2b1070fac0b1ee1b73d20b092833b33f1d30df5` | PASS |
| c06r2-n08 | `3523b7ec98246da8b8d66a593fb8fbc84a909058e11c460661bfc0c136815cbf` | PASS |
| c06r2-n08-p2 | `06318b6c8fcb41ed509523430e8702cca46bfac9e9dacf248b4627fcdf83d77c` | PASS |
| c06r2-n09 | `f0f7e5afa730ac035b0cfce0f9027e01fe8c64bdd293a3af405f46ce60ee37dd` | PASS |
| c06r2-n09-p2 | `4b0dfed5ff457c7ac886fb9edf10de519e1332389e7f1adce7c0219e6aa55d39` | PASS |
| c06r2-n10 | `752eb03f5cbc5a2ef328264d10fb96e3c6c9c0231b43e9c8d531f5d0c58b8c6e` | PASS |
| c06r2-n10-p2 | `83e7dccf387dbb157729644312165d573970f942761d5a6259ac348d3e562f76` | PASS |
| c06r2-outro | 編輯收束文字，非新外部史實 | PASS |

## 範圍與保留

r1收據與history原樣保留，其HOLD沒有被回改。本輪發現需修事項0、作者事實修改0；無未解來源或書面配鏡問題。

這份verify-1只記錄來源與書面配鏡通過，綁定上述r2四輸入；不判定敘事panel、實際時長、音訊、生成圖片、字幕時間軸、費用或站主批准。本輪未重跑native lint；未改作者稿，原生lint／流程狀態由其既有關卡各自確認。沒有付費／provider／後台命令。
