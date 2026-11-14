# curio-w05-seiko-quartz-astron 查核第一輪

- 查核者：獨立查核代理（Claude Opus 5.5，沒有參與寫稿），日期 2026-11-02。逐句讀 `script.md` 的旁白、`video.json` 的字卡與說明欄，對原始來源，撰稿者的 `claims.md` 只當線索。
- 重新打開的頁面：ETHW 兩份 Milestone 與 Frei 的 First-Hand；Plus9Time 比賽表與原始型錄；Seiko 博物館 milestone_03、milestone_04、company/003、collect020、knowledge/relation_11（英文與日文）；Seiko Astron 50 週年故事、Astron History、2019 新聞稿；Toyota 1966 發表資料；Europa Star；swissinfo；Watchonista；Grail Watch Wiki；Gear Patrol；Swatch Group 沿革；Donzé 2011 論文與 Twinam 逐字稿（兩份 PDF 都轉成文字後搜尋）。
- 撰稿者沒開、這輪新開而且改變結論的：**Donzé 本人 2011-01-19 在 Le Temps 的投書**（全文，下稱 Le Temps）；Seiko 博物館 knowledge/relation_11 的**日文版**；Hodinkee Japan。
- 打不開：瑞士歷史辭典（HLS，Cloudflare 驗證）；The Seiko Guy（同，只讀到搜尋片段）；Epson 35SQ 頁（403）。shmj develop53 的 PDF 加密，文字抽不出來。驗證頁沒有繞過。
- 列號與 `claims.md` 相同；#48–#51 是這輪新增。

## 這輪改了什麼

| 行 | 問題 | 改法 |
|---|---|---|
| t048 | 「手上握著領先的東西，主席說沒興趣」時序錯：主席那句是 1966 年，Beta 1 第一支原型 1967 年 7 月才裝好（#18）。當時業界認為做不出來，手上沒有領先的東西 | 「那時原型還沒做出來，可是隔年包辦前十的，就是這裡」 |
| t106、t107、說明欄 | 把 Donzé 的論文當成跟他自己相反的學界分歧。投書明寫日本靠量產好錶勝出，論文寫日本競爭引發危機，兩者不衝突（#39）；真正的不同看法是 Twinam | t106 改成他沒說日本無關、算在量產不算在石英；「學界沒講成一句話」移到 t107 |
| t099、說明欄 | 「只讀到 swissinfo 轉述」已可換一手：Le Temps 是他本人寫的，用詞是 légende（#38） | 「二〇一一年在瑞士報紙上寫：石英兇手這個說法，是傳說」；說明欄留 swissinfo 的 mythe |
| t101 | 「一九七一年才放棄」只有 swissinfo；Donzé 自己寫 Statut horloger（1934-1965）（#38） | 「一九三四年立……一九六〇年代中才拆」；衝突記在 `claims.md` |
| t094–t097、`fx-share` 字卡 | 只講占比下跌，暗示瑞士在美國賣少了。Le Temps：金額 5,960 萬 → 8,840 萬美元還在漲；那幾年日本進口「pour l'essentiel」是機械錶（#37）。把這個放進來才是這段該有的證據 | t096「占比掉了一大截，金額其實還在漲」；t097 補機械錶；字卡標 Donzé 2011 |
| t123 | 「那三千支」是 Seiko 所有早期石英款的統計，不是那支金錶（#26） | 「到一九七一年，它全部的石英錶才這麼多」 |
| t121、outro 字卡、第 4 章章名 | 「瑞士先做」「原型更早」比來源強：Seiko 同年也有原型，日期沒公開，Frei 自己也這樣寫（#49）。能確定的是比賽贏過、早於開賣兩年 | t121「在開賣前兩年就贏過比賽」；字卡「瑞士腕錶先奪冠」；章名「瑞士也做出來了，然後呢」 |
| t077 | 「結果擺在眼前」把 1979 年的產量說成公開專利的結果，來源沒有這個因果 | 「不管條件是什麼」 |
| t067 | 「降到」「比當初便宜七成」：是另一款新機型，不是降價，材質也不同（#26） | 「賣十三萬五千日圓，比那支金錶便宜七成」 |
| t018、t019 | 只給 ±20 秒，比型錄舉的機械錶例子（月差 1 分鐘，約日差 2 秒）差十倍，對比被放大（#5） | 兩個都講；t019 為了 lint 的 12 秒上限縮短 |
| t017 | 「憑準」單一原因：18K 金殼是定價的一部分，型錄的高階機械錶也要 19.5–30 萬 | 「憑金殼，也憑準」 |
| 第 2 章章名 | 「比一台車還貴」與片中自己的但書不符（豪華型比它貴） | 「跟一台車一樣貴的錶」 |

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 1969-12-25 東京上市；研發十年 | CONFIRMED | 「introduced in Tokyo on December 25, 1969」「After ten years of research」；Frei 記成 12-26 | ETHW | https://ethw.org/Milestones:Electronic_Quartz_Wristwatch,_1969 | ✅ |
| 2 | 45 萬日圓，18K 金 | CONFIRMED | 「450,000 Yen (18K gold-cased)」；型錄同 | Seiko 博物館；型錄 | https://museum.seiko.co.jp/en/seiko_history/milestone/milestone_03/ | ✅ |
| 3 | 約一台大眾車 | CONFIRMED（自述） | 「about the price of popular car in those days」 | Seiko 博物館 | https://museum.seiko.co.jp/en/seiko_history/company/company/003/ | ✅ |
| 4 | Corolla 價格與開賣日 | CONFIRMED | 11 月 5 日；東京 Standard ¥432,000、Deluxe ¥495,000（另有 Special ¥472,000） | Toyota | https://global.toyota/jp/detail/14002042/ | ✅ |
| 5 | 月差 5 秒、日差 0.2 秒；機械錶比較 | CHANGED | 博物館「daily difference of mechanical watches was ±20 seconds」；型錄「1 minute of monthly difference (2 seconds on average daily difference)」。兩個都是 Seiko 的資料，基準不同，旁白改成都講 | Seiko 博物館；型錄 | https://www.plus9time.com/blog/2019/6/7/seiko-quartz-astron-first-quartz-watch-promotional-brochure | ✅ |
| 6 | 8,192 次／秒 | CONFIRMED | 「8,192 cycles per second」；博物館 8,192HZ | ETHW；Seiko 博物館 | https://ethw.org/Milestones:Electronic_Quartz_Wristwatch,_1969 | ✅ |
| 7 | 1969 年 12 月做出 20 支 | CONFIRMED（自述） | 「69年の12月にようやく20本の腕時計を作り上げた」 | Seiko 週年故事 | https://www.seikowatches.com/jp-ja/products/astron/special/story_qa50th_1 | ✅ |
| 8 | 一週賣 100 支，1,250 美元 | CONFIRMED | 「Within one week of the introduction, 100 18-karat gold watches had been sold」「$1,250」 | ETHW | https://ethw.org/Milestones:Electronic_Quartz_Wristwatch,_1969 | ✅ 原文／⚠ 與 #7 不合 |
| 9 | 總產量查不到 | CONFIRMED（到讀過的範圍） | 沒有官方數字。又一個版本：Hodinkee Japan「ゴールドケースの100本限定」；The Seiko Guy 的搜尋片段說不是限量、序號追到 48，全文打不開。兩支衝突旁白照講，沒有替它解釋，站得住 | Hodinkee Japan；The Seiko Guy 片段 | https://www.hodinkee.jp/articles/four-revolutions-quartz-revolution | ⚠ |
| 10 | 1958 CBC，文件櫃大 | CONFIRMED | 「the size of a filing cabinet」 | ETHW | 同 #1 | ✅ |
| 11 | 1959 年 59A，船用時計 | CONFIRMED | 「59A Project」「led to the creation of the marine chronometer」 | ETHW | 同 #1 | ✅ |
| 12 | 1963 第 10–12 名；約 45 天 | CONFIRMED | 「tenth, eleventh and twelve places」「approximately 45 days」 | Plus9Time | https://www.plus9time.com/blog/2019/6/16/seiko-at-the-neuchtel-competitions-quartz-entries | ✅ |
| 13 | 1964 機械腕錶第 144、153 名 | CONFIRMED（有省略） | 「144th (7.97 points) and 153th (8.47 points)」。同年 Seiko 船用組第 2–7 名（Plus9Time），旁白沒講；「不是一出場就贏」仍成立，但 t034 問「怎麼追上來」時這是現成答案，留給撰稿者取捨 | Seiko 博物館；Plus9Time | https://museum.seiko.co.jp/en/seiko_history/milestone/milestone_04/ | ✅ |
| 14 | 東京奧運官方計時 | CONFIRMED | 「official timing for the Tokyo Olympics」 | ETHW | 同 #1 | ✅ |
| 15 | 1967 納沙泰爾名次 | CONFIRMED | 腕錶組 1–10 全 CEH、第 11 W-004（0.301）；口袋錶組 Suwa 第 1，15 名中只有第 6、8 是 Ebauches | Plus9Time 表 | 同 #12 | ✅ |
| 16 | 前四名平均 0.166、0.873 | CONFIRMED（自算吻合） | 「0.166 and 0.873」；(0.152+0.160+0.166+0.188)/4=0.1665；(0.301+0.525+1.053+1.614)/4=0.873 | Frei；Plus9Time | https://ethw.org/First-Hand:The_First_Quartz_Wrist_Watch | ✅ |
| 17 | CEH 1962、納沙泰爾、20 家 | CONFIRMED | Grail「consortium of 20」；Gear Patrol「no fewer than 20」；IEEE 與 Frei 都只有 1962，沒有家數 | Grail；Gear Patrol；ETHW | https://wiki.grail-watch.com/index.php/Centre_Electronique_Horloger | ✅ 年／△ 家數 |
| 18 | 1965 專案；1966 主席沒興趣 | CHANGED（t048） | 「May 7, 1965」；1966 年對 Frei 與 Lochinger 說「not interested」，原文是轉述句不是引句，前一句寫專家認為做不到。只有 Frei 單方，旁白標了。t047 的「說」站得住，t048 的「領先」不成立 | Frei | https://ethw.org/First-Hand:The_First_Quartz_Wrist_Watch | △ 單一當事人 |
| 19 | 1968 日內瓦腕錶組 1–3 名瑞士石英 | CONFIRMED | 「took the 1st to 3rd place positions」；Seiko 機械第 10 | Seiko 博物館 | https://museum.seiko.co.jp/en/seiko_history/milestone/milestone_04/ | ✅ |
| 20 | 服部正次叫停音叉、一年內商品化 | CONFIRMED（自述） | 「1年以内に……商品化することを厳命した」；頁面沒有把比賽當原因，t054 站得住 | Seiko 週年故事 | 同 #7 | ✅ |
| 21 | 1970-04-10、1,000 支、16 家 | CONFIRMED | IEEE 同；Frei 與 Hodinkee 寫約 20 家，字卡與旁白標 16 家沒問題 | ETHW | https://ethw.org/Milestones:Pioneering_Work_on_the_Quartz_Electronic_Wristwatch,_1962-1967 | ✅ |
| 22 | 音叉型石英、開放式步進馬達、省電 | CONFIRMED | 「open type step motor」；週年故事記 18μA、每秒通電一次 | Seiko 博物館；週年故事 | https://museum.seiko.co.jp/en/seiko_history/company/company/003/ | ✅ |
| 23 | 第一的兩說 | CONFIRMED | 「first quartz wristwatch marketed commercially」；Frei「world first quartz wrist watch was Beta 1」 | Seiko 博物館；Frei | https://museum.seiko.co.jp/en/collections/watch_latestage/collect020/ | ✅ |
| 24 | 約 6,000 支；馬達與 CMOS | CONFIRMED | 「Some 6000 units」「a severe strategic error」；CMOS「only after 1972」。Frei 自己當事人；Grail 評 flop 但無數字 | Frei | https://ethw.org/First-Hand:The_First_Quartz_Wrist_Watch | △ 單一當事人 |
| 25 | 1972 Omega 賣最多 | CONFIRMED（公司自述） | SSIH Management Services：「Omega has sold more quartz watches than all other competing firms together」。沒有第二來源，旁白 t065 標了不能全信 | Europa Star | https://www.europastar.com/the-watch-files/archives-heritage/1004093671-debunking-the-quartz-crisis.html | △ |
| 26 | 38SQ 13.5 萬；3,000；170 萬 | CHANGED | Watchonista「3,000 had been produced by then」，主詞是 first quartz models；Le Temps「3000 pièces en 1971」，同一作者兩種寫法，「到一九七一年」都涵蓋。1975 年 170 萬為年產。38SQ 的材質沒查到一手型錄，所以不寫降價 | Watchonista；Le Temps | https://www.watchonista.com/editorial/history/the-history-of-quartz-weekend-part-1-the-seiko-revolution/ | ✅ 數字／△ 價格單一 |
| 27 | Seiko 公開大部分專利，同業採用 | CONFIRMED（自述） | 「disclose a large part of the patents」；「subsequently opened the patents to the world」；日文「パテントを一般公開し」 | Seiko 博物館；Astron History | https://www.seikowatches.com/global-en/products/astron/astron-history | ✅ 自述 |
| 27a | 年份、條件、是否收費 | CONFIRMED 查不到（到讀過的範圍） | 兩次英日文搜尋與 Seiko 五頁都沒有。the-shashi 本文沒提專利、費用或授權。**專利局公報沒查**，「紀錄裡沒有」只到公開文章與 Seiko 自述 | 同列 | https://the-shashi.com/en/tse/8050/decisions/quartz-revolution-1969/ | ⚠ |
| 28 | Bulova 理由 | CONFIRMED（自述） | 「keep the technology proprietary confidential hindered commercial success」；日文頁另寫目的是「デファクト・スタンダード化」 | Seiko 博物館 | https://museum.seiko.co.jp/en/seiko_history/company/company/003/ | ✅ |
| 29 | 流傳版本 | CONFIRMED（標成流傳） | Le Temps：多數史家與經濟學者這樣解釋；Wikipedia 這輪只讀到搜尋結果，沒有重開 | Le Temps | https://www.letemps.ch/economie/crise-horlogere-suisse-19751985-revue-corrigee | ✅ |
| 30 | 從業與公司家數 | CONFIRMED | 90,000 → 33,000（1984）、1,600+ → 不到 600；Donzé 89,000 → 33,000（1985）；swissinfo 約 9 萬／1,500 → 3 萬／500–600；Twinam 約 6 萬、三分之二。1993 年報紙 1,618 家（搜尋片段）。HLS 打不開，舊企劃的 7 萬沒有確認也沒進稿 | Seiko 博物館；Donzé；swissinfo；Twinam | https://museum.seiko.co.jp/en/knowledge/relation_11/ | ✅ |
| 31 | 出口只剩 1974 高峰一半 | CONFIRMED | Seiko 博物館；Springer 摘要 8,440 萬 → 1982–84 平均 3,130 萬（搜尋片段，比一半還少） | Seiko 博物館 | 同 #30 | ✅ |
| 32 | 城鎮少約 8% | CONFIRMED | 「lost around 8 percent of their populations between 1970 and 1980」；Twinam 在 William and Mary | Twinam | https://tradetalkspodcast.com/wp-content/uploads/2023/06/Episode-185-Transcript-Complete.pdf | ✅ |
| 33 | quartz crisis 1993；1977 社論 | CONFIRMED | 只限 Europa Star 自己的刊物，旁白有說 | Europa Star | 同 #25 | ✅ |
| 34 | 1980 日本總產量超過 | CONFIRMED | Seiko 博物館 1980；Donzé 以產值算是 1981–85，旁白說總產量沒問題 | Seiko 博物館；Donzé | 同 #30 | ✅ |
| 35 | 1979 約 6,000 萬、55% | CONFIRMED | 兩處都是 Seiko 博物館 | Seiko 博物館 | 同 #30 | ✅ 單一 |
| 36 | 匯率與三倍價 | CONFIRMED | 4.3、2.5（1975）、1.5（1978-10）；「three times as much in 1978」；Le Temps 另寫日圓固定匯率到 1977，瑞郎是相對劣勢 | Europa Star；Le Temps | 同 #25 | ✅ |
| 37 | 83% → 不到 59% | CHANGED | 「83,1% ... plus que 58,8% en 1975」；金額 59,6 → 88,4 百萬美元；「pour l'essentiel de montres mécaniques」。不再是單一來源，但 swissinfo 看來同源於 Donzé。另有案例研究寫 1970 年約 70%（搜尋片段，定義不明） | Le Temps | https://www.letemps.ch/economie/crise-horlogere-suisse-19751985-revue-corrigee | ✅ |
| 38 | Donzé：迷思、石英加重；法規；Seiko 合併 | CHANGED | 本人：「C'est une légende!」「n'est pas à l'origine de la crise mais en renforce les effets」「Statut horloger (1934-1965)」「à l'exception de Rolex」；swissinfo「mythe」「abandonné en 1971」。C'est une légende 在導言，可能是編輯下的，但正文有「véritable légende de la crise」 | Le Temps；swissinfo | 同 #37 | ✅ |
| 39 | Donzé 論文：日本競爭引發 | CHANGED（解讀） | 「Japanese competition triggered a major crisis」。原文存在，但不是反駁他自己，見改動表 | Donzé 2011 | https://mpra.ub.uni-muenchen.de/30736/1/MPRA_paper_30736.pdf | ✅ |
| 40 | Twinam：貿易與技術衝擊 | CONFIRMED | 主持人「trade and technology shock」；Twinam「big technology shock」是石英 | Twinam | 同 #32 | ✅ |
| 41 | 快倒、銀行找海耶克 | CONFIRMED | 「banks turned to the consultant Nicolas G. Hayek」；swissinfo UBS、SBS；Swatch「brink of insolvency」 | Donzé；swissinfo；Swatch | 同 #39 | ✅ |
| 42 | 1983 合併 | CONFIRMED | Donzé、Le Temps 同；Swatch 頁寫 1985 改名 SMH、1998 改 Swatch Group，旁白「後來的」站得住 | Donzé；Le Temps | 同 #39 | ✅ |
| 43 | Swatch 51 零件、50 法郎、累計 | CONFIRMED（自述） | 「51 components」；「50 francs」；2,300 萬（1986）、1 億（1992）只有 Seiko 博物館 | Swatch；Seiko 博物館 | https://www.swatchgroup.com/en/swatch-group/swatch-group-history | ✅／△ 累計 |
| 44 | 廣場協議日圓走強 | CONFIRMED（衝突已解） | 同一頁日文版：「急激な円高ドル安が進む中、日本メーカーが急速に競争力を失っていった」。英文版 weakening 確定是翻譯錯。Le Temps、swissinfo 同 | Seiko 博物館日文版 | https://museum.seiko.co.jp/knowledge/relation_11/ | ✅ |
| 45 | 真正的力量不是 Swatch | CONFIRMED | 摘要「rather than product innovation (Swatch), it was the rationalization」；內文「did not play the overwhelming role」，也說是主要利潤來源 | Donzé 2011 | 同 #39 | ✅ |
| 46 | IEEE 兩塊牌 | CONFIRMED | 2002-09-28 Neuchâtel；2004-11-25 Tokyo | ETHW | 同 #21 | ✅ |
| 47 | 各占幾成無人量化 | CONFIRMED（反面，只到讀過的範圍） | Le Temps 也只寫「complexité des liens」 | Le Temps | 同 #37 | ⚠ |
| 48 | Seiko 石英量到 1979 才超過機械（新增，未進稿） | CONFIRMED | 1971–74 只占總產量 1.4%；658,000（1974）；2,550 萬（1980）。t068 之後可用 | Le Temps | 同 #37 | ✅ |
| 49 | 誰的原型先（新增） | UNVERIFIED | Beta 1 1967 年 7 月；8 月 13 日起送測；Seiko 11 月 11 日送件；Frei 寫 Seiko 不公開細節。送測先後不等於製作先後 | Frei | https://ethw.org/First-Hand:The_First_Quartz_Wrist_Watch | ⚠ |
| 50 | 服部正次卒年（畫面規則，新增） | WRONG in `brief.md`、`NOTES.md` | president.jp「服部正次(1900~1974)」；1987 是服部謙太郎（來源較弱）。仍未滿 70 年，不畫的決定不變，也不進旁白 | president.jp | https://president.jp/articles/woman-print/80067 | △ |
| 51 | 提示詞不含真名（新增） | 沒重掃 | 撰稿者說掃過，這輪沒有改提示詞，也沒有重掃 | — | — | ⚠ |

## 其他判定

- **t005、t071「給全世界」**：這是 Seiko 自己的句子（「opened the patents to the world」），不是坊間誇大。旁白已標成自述，t076 只否定「免費」。
- **t025「二十支，怎麼賣出一百支」**：兩邊的原文都對，時間也都在 12 月底前後，衝突是真的。理論上開賣後還能再做，所以旁白只說對不上、不解釋，站得住。
- **t065「看起來可不像快倒」**：意見，出口高峰確實在 1974 年，站得住。
- **t104「又好又便宜」**：swissinfo 與 Le Temps 同。
- **t106「他算在量產，不算在石英」**：是把投書與論文合起來讀的解讀；投書明寫量產，論文那句沒有寫原因。
- **標題**是問句，沒過頭。**縮圖**「Seiko／兇手？」同理，片中直接回答未結。
- **t126、t127**：「未結」與 #47 一致。
- **風險**：沒有暗示違法；真實公司的不利說法（Beta 21、主席那句、Omega）都標了出處。

## 仍只有單一或當事人來源

主席說沒興趣與 Beta 21 約 6,000 支（Frei 單方）；Omega 賣最多（SSIH 自述，只有 Europa Star 引）；38SQ 13.5 萬（Donzé，Watchonista）；Swatch 累計銷量與 1979 年日本產量（Seiko 博物館）；83% → 59%（Donzé，swissinfo 同源）；1971 年與 1965 年的法規終點（沒有 HLS 可以裁定）；Seiko 公開專利（只有 Seiko 自述，年份條件未知，專利公報沒查）。

## 交回撰稿者，這輪沒改

`brief.md` 的「手握領先的主席」與服部卒年、`NOTES.md` 的服部卒年，都不在這輪可改的範圍，要照 t048 與 #50 更新。NOTES 第 3 點的比賽終止年：Plus9Time 寫公開賽到 1967，沒進稿，不影響旁白。narrative 雜湊變了，盲評要用現在這一版。
