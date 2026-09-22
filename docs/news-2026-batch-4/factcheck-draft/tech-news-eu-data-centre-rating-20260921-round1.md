# 查核報告（第一輪）tech-news-eu-data-centre-rating-20260921

- 查核代理：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-23（台北）
- 垂直／順序：科技／`display_order` 322；事件日 2026-09-21；`kind` life
- 內容包：`apps/api/app/guides/content/tech-news-eu-data-centre-rating-20260921.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-eu-data-centre-rating-20260921.json`
- 依據：`FACTCHECK-47.md`、`DELTA-4-7.md`（優先）、`DELTA-4-6.md`、`DELTA-4-5.md`、`agents/tech/FACTCHECK.md`、`ASSIGNMENTS.md` T2 列

## 1. 來源重抓結果（2026-09-23 台北 01:21，即 2026-09-22T17:21Z）

全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒；
UA、標頭、查詢字串都沒有帶任何人的姓名、email 或個人資料；只做 GET，沒有填寫或送出任何表單。
PDF 用系統 `python` 的 pypdf 抽文字；HTML 去 `<!-- -->`、去 `script`／`style`、去標籤、`html.unescape`、NBSP 轉半形空白。

| # | 來源 | 狀態 | bytes | 是否讀到正文 | 與撰稿代理 00:48–00:49 抓到的差異 |
| --- | --- | --- | --- | --- | --- |
| S1 | `…/presscorner/api/files/document/print/en/ip_26_1667/IP_26_1667_EN.pdf` | 200 | 85,753 | 是。2 頁、6,010 字元，Next steps／Background／兩段引言全讀到 | **逐位元組相同** |
| S2 | `energy.ec.europa.eu/document/download/b073ba9b…_EN_ACT_part1_v9.pdf` | 200 | 261,042 | 是。15 頁、43,483 字元，說明備忘錄＋前言 (1)–(19)＋第 1–7 條全讀到 | **逐位元組相同** |
| S3 | `energy.ec.europa.eu/document/download/45309975…_annexe_acte_autonome_part1_v7.pdf` | 200 | 432,803 | 是。12 頁、24,752 字元，附件一表 1／表 2、附件二 (I)–(XVIII) 與第 3 點、附件三全讀到 | **逐位元組相同** |
| S4 | `energy.ec.europa.eu/news/minimum-performance-standards-…-2026-09-21_en` | 200 | 86,956 | 是。伺服器端渲染，正文與 `Publication date 21 September 2026` 都在 | **逐位元組相同** |

另外複驗兩個「讀不到」的頁面（不是 `sources[]`，只為了核對正文的否定句）：

| 頁面 | 狀態 | bytes | 去標籤後 | 結論 |
| --- | --- | --- | --- | --- |
| `ec.europa.eu/commission/presscorner/detail/en/ip_26_1667` | 200 | 22,157 | 34 字元 | 導覽外殼，正文寫法正確 |
| `…/have-your-say/initiatives/19293-Data-centres-in-Europe-minimum-performance-standards_en` | 200 | 4,055 | 13 字元（`Have your say`） | Angular 外殼，今天仍讀不到 |
| `energy.ec.europa.eu/publications/commission-delegated-regulation-…-and-annexes_en` | 200 | 88,891 | 2,282 字元 | 出版頁，檔案標題與正文所寫相符 |

`verbatim_quote` 連續字串比對：研究紀錄 `verified_facts` **63 條全部命中**（0 條失效），`url` 全部在 `sources[]` 內；
`sources[]` 四條的 `verbatim_quote` 也全部命中。研究紀錄本身沒有發現捏造或錯置的引文。

## 2. 主張逐條核對

Verdict：C＝CONFIRMED，**CH＝CHANGED**，NF＝NOT FOUND，OOS＝OUT OF SCOPE（風格）。
「來源」欄 S1–S4 對應第 1 節。共 118 條。

### 2.1 title／description（1–12）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 1 | 「歐盟通過資料中心評等制度」 | S1 `the delegated act adopted by the Commission`；S2 末頁 `Done at Brussels, 21.9.2026` | C |
| 2 | 「A 到 G 七級」 | S3 附件一表 1、表 2 各七列 | C |
| 3 | 「2027 年 8 月發第一批標籤」 | S2 第 3 條第 1 項；S1 `expected to be displayed in 2027` | C |
| 4 | title ≤ 60 字、與研究紀錄 `title` 逐字相同 | 程式比對 True | C |
| 5 | description：2026-09-21、執委會通過授權規則 | S1／S2 | C |
| 6 | description：替境內資料中心建立共同評等制度 | S2 第 1 條 | C |
| 7 | description：電力使用效率與用水效率各分 A 到 G 七級電子標籤 | S3 附件一 | C |
| 8 | description：500 kW 門檻 | S1 | C |
| 9 | description：最低效能標準未定案 | S4 | C |
| 10 | description：三方協議未定案 | S1 | C |
| 11 | description 長度 146 字（120–200），句尾只帶「（2026 年 9 月查證）」 | DELTA-4-7 §14 | C |
| 12 | title／description／summary 沒有本篇自己的選材計數 | 逐句看過 | C |

### 2.2 前言兩段（13–20）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 13 | 第一段日期 2026-09-21 ＝ `news_date` ＝ slug 後綴 | 三者一致（程式比對） | C |
| 14 | 文號 C(2026) 3472 final | S2 第 1 頁 | C |
| 15 | 目的：提高能源使用透明度、支持永續整合進歐洲能源系統 | S1 `aimed at increasing transparency on their energy use and supporting their sustainable integration into Europe's energy system` | C |
| 16 | 建立在《能源效率指令》與 2024 年通報制度之上 | S1 `building on the Energy Efficiency Directive and the 2024 reporting scheme for data centres` | C |
| 17 | 「（EU）2024/1364 那套 2024 年就上線」 | S2 前言 (8) `The database became operational in September 2024` | C |
| 18 | 「不是從零開始的新制度」 | S2 備忘錄 `As a second step, this Regulation sets out rules…` | C |
| 19 | 第二段查核日 2026-09-23，與四條 `sources.checked_on`、研究紀錄 `checked_on`、表格 caption、圖說、FAQ、callout 七處一致 | 程式比對 | C |
| 20 | 第二段「不比較資料中心或雲端服務，也不建議台灣業者該怎麼因應」 | 科技垂直界線 | C |

### 2.3 summary 五句（21–31）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 21 | 第 1 句：同 #5–#7 | S1／S2／S3 | C |
| 22 | 第 2 句：2 個月審查期 | S1 `is now subject to 2-month scrutiny period by the European Parliament and the Council before entering into force` | C |
| 23 | 第 2 句：兩院只能否決、不能修改 | S1 `they cannot propose changes to the text` | C |
| 24 | 第 2 句原寫「之後刊登《歐盟官方公報》，滿 20 天才生效」 | 四份文件都沒有印「審查期過後才刊登」的順序 | **CH**（見 3.4） |
| 25 | 第 3 句：涵蓋單一容量 500 kW 以上 | S1 | C |
| 26 | 第 3 句：500 kW 以下與尚未營運可自願參加 | S2 第 5 條新增之 3(5)、3(6) | C |
| 27 | 第 3 句原寫「2027 年 8 月 15 日起由歐洲資料庫自動產生」 | S2 第 3 條第 1 項 `By 15 August 2027` | **CH**（見 3.1） |
| 28 | 第 4 句：12 週公眾諮詢、2026-12-14 截止 | S4 | C |
| 29 | 第 4 句：草案要等 2027 年第二季 | S4 `the legislative proposal planned for the second quarter of 2027` | C |
| 30 | 第 5 句原寫「2024 年的 68 TWh」 | S1 `around 68 TWh` | **CH**（見 3.6） |
| 31 | 第 5 句：114 TWh、超過 3%、歸給國際能源署 | S1 `expected to virtually double to 114 TWh by 2030 - reaching more than 3% … according to the International Energy Agency` | C |

### 2.4 第一節「9 月 21 日通過了什麼」（32–52）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 32 | 法律形式：依（EU）2023/1791 第 33(3) 條作成的授權規則 | S2 `in particular Article 33(3) thereof` | C |
| 33 | 同時修正（EU）2024/1364 | S2 抬頭 `and amending Commission Delegated Regulation (EU) 2024/1364` | C |
| 34 | 規則有 7 條 | S2 `This Regulation includes seven articles.` | C |
| 35 | 另帶 3 份附件 | S2 `The Regulation's three Annexes`；S3 `ANNEXES 1 to 3` | C |
| 36 | 歐盟希望未來 5 到 7 年把容量變三倍 | S1 `triple its data centre capacity over the next five to seven years` | C |
| 37 | 「沒有印出基準年或目標容量，只能當政策意向」 | 研究紀錄 `unverified_or_excluded` 第 8 條；S1 確實沒有印 | C（敘述屬編務說明，見第 5 節） |
| 38 | Ribera 職銜「執委會執行副主席」 | S1 `Executive Vice-President for Clean, Just and Competitive Transition` | C |
| 39 | Ribera 引言逐字 | S1 該句為連續子字串 | C |
| 40 | 引言的中文轉寫沒有超出原文 | 逐字對讀 | C |
| 41 | 「Teresa Ribera」首次出現沒有中文名 | WRITER-47「外國名字首次出現要帶中文」 | OOS（留給協調者，見第 5 節） |
| 42 | 「9 月 21 日通過的是授權規則，不等於生效」 | S1 Next steps | C |
| 43 | 原寫「規則寫明，現在要先經過……2 個月的審查期」 | 2 個月審查期只印在 S1，S2 全文沒有提到審查期 | **CH**（見 3.3） |
| 44 | 兩個立法機關只有反對權、不能修改條文 | S1 | C |
| 45 | 原寫「審查期過後規則要刊登在《歐盟官方公報》」 | 順序未印 | **CH**（見 3.4） |
| 46 | 公報刊出滿 20 天生效 | S2 第 7 條 `on the twentieth day following that of its publication in the Official Journal` | C |
| 47 | 查核當天沒有正式（EU）編號 | S2 抬頭 `(EU) …/…`；註腳 50 的 `2026/7000` 連 OJ 與 ELI 都留空 | C |
| 48 | 查核當天沒有刊登公報的日期 | 同上 | C |
| 49 | 原寫「2024 年的 68 TWh」（正文） | S1 `around 68 TWh` | **CH**（見 3.6） |
| 50 | 114 TWh、超過 3%，歸給 IEA | S1 | C |
| 51 | 原寫「規則本文的說明備忘錄則寫更精確的 3.2%」 | S2 備忘錄印 `reaching 3.2% of the electricity demand of the Union`，但註腳 3 指向另一份歐洲電力需求資料（68／114 TWh 則註到 IEA） | **CH**（見 3.5） |
| 52 | 原寫「這組數字是執委會引用國際能源署的推估」（涵蓋 3.2%） | 同上 | **CH**（見 3.5） |

### 2.5 第二節「標籤上會印什麼」與表格（53–76）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 53 | 不是另外派人查核，而是用已通報的資訊與 KPI 發標籤 | S2 第 1 條 `shall rate data centres by means of electronic labels issued based on information and key performance indicators communicated by data centre operators` | C |
| 54 | 附件一把 PUE 與 WUE 各切成 A 到 G 七級 | S3 附件一 | C |
| 55 | 原寫「計算方式沿用（EU）2024/1364 附件三，這份規則本身沒有改變算法」 | S3 附件三第 (3)(a) 點取代 2024/1364 附件三的 (b) 點：`WUE = WIN-FRE/EIT`；S2 備忘錄 `replace existing definitions (e.g. for EDC, ERES-TOT, location, grid functions, and WUE)`、`the replacement of 'potable water input' by 'freshwater input'` | **CH**（見 3.2） |
| 56 | PUE 的算法沒有動 | S3 附件一 `in accordance with point (a) of Annex III of … (EU) 2024/1364`；附件三沒有修改 (a) 點 | C |
| 57 | 規則沒有寫「幾級算合格」、附件一不含最低門檻 | S2／S3 全文讀過，未見任何門檻值 | C |
| 58 | 標籤會印「有沒有提供電網彈性」 | S3 附件二 (XV) | C |
| 59 | 標籤會印「是不是具備廢熱再利用條件」 | S3 附件二 (XVI) | C |
| 60 | 標籤會印所在地區 | S3 附件二 (V) | C |
| 61 | 地點用 Eurostat 的 NUTS3 區域代碼、不是街道地址 | S3 附件三 (1)(a) `the EU NUTS3 code … in accordance with the validated 2024 EU LAU tables published by Eurostat` | C |
| 62 | 標籤會印通報對應的規模級距 | S3 附件二 (VI) | C |
| 63 | 原寫「可以掃描連到細節的 QR code」 | S2 第 2 條：`links to the location in the publicly accessible space of the European database where this label is stored` | **CH**（見 3.7） |
| 64 | 每張標籤附一份執委會準備、所有標籤共用的說明文件 | S3 附件二第 3 點 | C |
| 65 | 說明文件解釋 PUE 與當地氣候的關係 | S3 附件二 3(I)（CDD） | C |
| 66 | 說明文件解釋 PUE 與規模、屋齡的關係 | S3 附件二 3(II) `the relation between PUE and data centre size or age` | C |
| 67 | 說明文件解釋 PUE 與 WUE 的取捨 | S3 附件二 3(III) | C |
| 68 | 個別通報的資訊與 KPI 一律視為機密 | S2 第 5 條 (3) 取代之 5(5) | C |
| 69 | 只有標籤上呈現的那部分公開 | 同上 `With the exception of the information that is part of the label … and in the form in which it appears on the label` | C |
| 70 | 標籤以電子形式提供給任何提出要求的人 | S2 第 4 條第 1 項 | C |
| 71 | 業者可指向自己管理的免費網站或歐洲資料庫 | 同上 `can refer to a free-access website they manage or to the European database` | C |
| 72 | 不得製作或展示模仿官方標籤的標示 | S2 第 4 條第 2 項 | C |
| 73 | 表格 A 列：PUE 1.15 以下、WUE 0.1 以下 | S3 `A PUE ≤ 1.15`／`A WUE ≤ 0.1` | C |
| 74 | 表格 B 列：PUE 1.15 至 1.25、WUE 0.1 至 0.2 | S3 `B 1.15 < PUE ≤ 1.25`／`B 0.1 < WUE ≤ 0.2` | C |
| 75 | 表格 D 列：PUE 1.35 至 1.5、WUE 0.4 至 0.6；G 列：高於 1.9／高於 1.0 | S3 `D 1.35 < PUE ≤ 1.5`／`D 0.4 < WUE ≤ 0.6`／`G PUE > 1.9`／`G WUE > 1.0` | C |
| 76 | 表格 caption：只列部分級距、完整級距見附件、查核日 2026-09-23 | 站主裁定四級呈現可以；caption 已自述 | C |

### 2.6 第三節「管到誰」與圖說（77–92）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 77 | 涵蓋單一容量 500 kW 以上 | S1 `will cover individual data centres with a capacity above 500 kW` | C |
| 78 | 「這是既有通報制度就有的門檻，不是這份規則新訂的」 | 四份 `sources[]` 沒有一份逐字印出；站主已裁定照寫 | C（依裁定；缺口見第 4 節） |
| 79 | 低於 500 kW 可自願參加 | S2 新增之 3(5) | C |
| 80 | 「裝置 IT 電力需求」的口徑 | 同上 `installed information technology power demand` | C |
| 81 | 尚未營運可自願參加 | S2 新增之 3(6) | C |
| 82 | 通報設計值或預期營運兩個日曆年後可達到的指標 | 同上 `designed or expected to achieve after two calendar years of operation` | C |
| 83 | 之後從營運第一年起補報實際值 | 同上 `as of the first year of operation` | C |
| 84 | 國防與民防資料中心的豁免對象定義 | S2 第 5 條 (2)(a) | C |
| 85 | 豁免內容是免向資料庫通報，不是不受制度管 | 同上 `be exempt from communicating to the European database the information and key performance indicators set out in Annexes I and II` | C |
| 86 | 原寫「從 2027 年 8 月 15 日起、其後每年」（正文） | S2 第 3 條第 1 項 `By 15 August 2027 and every year thereafter` | **CH**（見 3.1） |
| 87 | 由歐洲資料庫自動產生電子標籤 | 同上 | C |
| 88 | 效期從發出當年 8 月 15 日到隔年 8 月 15 日 | S2 第 3 條第 3 項 | C（但書未寫，見第 4 節） |
| 89 | 新聞稿用「預計」在 2027 年顯示第一批標籤 | S1 `expected to be displayed in 2027` | C |
| 90 | 2028 年 12 月 31 日前、其後每三年檢討並提報告 | S2 第 6 條 | C |
| 91 | 圖說四個時間點；原寫「2027 年 8 月 15 日起」 | 同 #86 | **CH**（見 3.1） |
| 92 | 圖說與研究紀錄 `diagram.caption` 逐字相同（改後仍相同） | 程式比對 True | C |

### 2.7 第四節「還沒定案的部分」（93–101）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 93 | 同一天開了 12 週的公眾諮詢與證據徵集 | S4；S1 `has launched a call for evidence and public consultation` | C |
| 94 | 題目是資料中心的最低效能標準 | S4 標題與首句 | C |
| 95 | 2026 年 12 月 14 日截止 | S1／S4 `by 14 December 2026` | C |
| 96 | 意見要支援「規劃在 2027 年第二季」的立法提案準備工作 | S4 | C |
| 97 | 「最低效能標準現在連草案都還沒有」 | S4（只有 preparatory work）；研究紀錄 `not_said` 第 6 條 | C |
| 98 | 2026 年 6 月簽的是「意向聲明」 | S1 `the Declaration of intent signed in June 2026` | C |
| 99 | 與業者、電網業者、能源供應商、公部門合作 | S1 | C |
| 100 | 「朝向」「下半年」，沒有名單、簽署日或內容 | S1 只印 `towards a tripartite agreement … in the second half of the year` | C |
| 101 | 沒有正式編號／公報日期／生效日；沒有罰則 | S2 全文；研究紀錄 `not_said` 第 3、5 條 | C |

### 2.8 第五節「跟台灣的關係」（102–107）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 102 | 「四份文件……未見與台灣有關的說法，也未見提到任何亞洲國家」 | 四份 body 全文檢索：taiwan／china／chinese／japan／korea／india／asia／singapore／hong kong 全部 0 次 | C |
| 103 | 對台灣的意義寫成「可以參考的作法」，不是「我們也要照做」 | 研究紀錄 `must_not_write` 第 9 條 | C |
| 104 | press corner 網頁版只是導覽外殼，全文要看列印版 PDF | 今天複驗：200／22,157 bytes／去標籤 34 字元 | C |
| 105 | 規則本文與附件在 DG ENER 出版頁，標題為 `Commission Delegated Regulation establishing a common Union rating scheme for data centres` | 出版頁檔案標題逐字相同 | C |
| 106 | 諮詢在「Have your say」平台上 | S1／S4 都連到該平台 | C |
| 107 | 「讀到的只是頁面外殼，問卷實際題目本站沒有查到」 | 今天複驗：200／4,055 bytes／去標籤 13 字元 | C |

### 2.9 FAQ 六題與 callout（108–116）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 108 | 第 1 題：還沒生效、2 個月審查期、只能否決 | S1 | C |
| 109 | 第 1 題原寫「審查期過後規則要刊登《歐盟官方公報》」 | 順序未印 | **CH**（見 3.4） |
| 110 | 第 2 題：500 kW 不是這次新訂，新增的是自願參加 | S2 新增之 3(5)、3(6)；站主裁定 | C |
| 111 | 第 3 題原寫「從 2027 年 8 月 15 日起、其後每年」 | S2 第 3 條第 1 項 | **CH**（見 3.1） |
| 112 | 第 4 題：A–G 不是及格線，最低效能標準另案徵詢 | S3 附件一；S4 | C |
| 113 | 第 5 題：不會全部公開，只有標籤上那部分 | S2 第 5 條 (3) | C |
| 114 | 第 6 題：沒有提到台灣、亞洲國家或非歐盟業者 | 同 #102；S2／S3 只規範 `data centres in the Union` | C |
| 115 | callout：查核當天還沒生效、審查期與公報刊登都還沒發生、第一批標籤預計 2027 年 8 月 | S1／S2 | C |
| 116 | 全篇只有一個 callout、沒有投資免責段落 | 科技垂直規格 | C |

### 2.10 sources[] 與結尾連結（117–118）

| # | 主張 | 來源 | Verdict |
| --- | --- | --- | --- |
| 117 | `sources[]` 四條的網址、順序與研究紀錄相同，`checked_on` 全部 2026-09-23 | 程式比對；四條今天重抓全部 200 且為正文 | C |
| 118 | 兩個結尾連結的 text 與目標內容包 zh-TW `title` 逐字相同（`tech-news-2026-index`／`tech-news-eu-cra-reporting-20260911`） | 程式逐字比對 True | C |

**統計：查了 118 條主張，CONFIRMED 103、CHANGED 14、NOT FOUND 0、OUT OF SCOPE 1。**
14 條 CHANGED 是 **7 個不同的事實問題**（第 3 節的 3.1–3.7），在內容包裡共 11 個位置，另在研究紀錄改 4 處。

## 3. 改掉的七處（每處：原文 → 改成什麼 → 來源怎麼寫 → 為什麼）

### 3.1 第 3 條的發標時點：「起」改成「前」（四個位置：摘要第 3 句、正文第三節、FAQ 第 3 題、圖說＋研究紀錄 `diagram.caption`）

- 原文：`從 2027 年 8 月 15 日起、其後每年，由歐洲資料庫自動……`
- 改成：`2027 年 8 月 15 日前、其後每年，由歐洲資料庫自動……`
- 來源（S2 第 3 條第 1 項）：`By 15 August 2027 and every year thereafter, an electronic label in the format set out in Annex II shall be automatically generated by the European database`
- 為什麼：`By` 是期限不是起算日。同一篇把第 6 條的 `By 31 December 2028` 正確寫成「2028 年 12 月 31 日前」，兩處原本互相矛盾。效期條款（第 3 條第 3 項 `valid from 15 August`）沒有動，讀者仍看得到「標籤自 8 月 15 日起生效」。研究紀錄的 `summary` 與該條 `verified_facts` 也一併訂正，並在 fact 裡附上原文，避免第二輪再被同一句誤導。

### 3.2 WUE 的算法其實被這份規則改寫了（正文第二節）

- 原文：`計算方式沿用（EU）2024/1364 附件三，這份規則本身沒有改變算法。`
- 改成：`兩個指標都照（EU）2024/1364 附件三的方法算；PUE 那一點沒有動，WUE 那一點則由這份規則的附件三改寫成「淡水取水量除以資訊設備用電量」。`
- 來源（S3 附件三 (3)(a)）：`Annex III is amended as follows: (a) point (b) is replaced by the following: '(b) Water Usage Effectiveness (WUE) WIN-FRE … shall be used to calculate the WUE of a data centre: WUE = WIN-FRE/EIT;'`；S2 備忘錄：`improve or replace existing definitions (e.g. for EDC, ERES-TOT, location, grid functions, and WUE)`、`the replacement of 'potable water input' by 'freshwater input'`
- 為什麼：原句的全稱否定（「沒有改變算法」）與附件三的明文修正相反，屬「安靜強化來源」。PUE 的 (a) 點確實沒有被動到，所以改寫成分開講。研究紀錄對應的 `verified_facts` 一併訂正。

### 3.3 兩個月審查期寫在新聞稿，不在規則裡（正文第一節）

- 原文：`規則寫明，現在要先經過歐洲議會與理事會 2 個月的審查期……`
- 改成：`新聞稿寫明，規則現在要先經過歐洲議會與理事會 2 個月的審查期才會生效……`
- 來源（S1 Next steps）：`The Delegated Regulation establishing the common rating scheme is now subject to 2-month scrutiny period by the European Parliament and the Council before entering into force.`
- 為什麼：S2 全文（含第 7 條與前言 (1)–(19)）沒有任何一句提到審查期。歸錯文件會讓讀者以為條文裡查得到。

### 3.4 「審查期過後才刊登公報」是推論（三個位置：正文第一節、摘要第 2 句、FAQ 第 1 題）

- 原文：`審查期過後規則要刊登在《歐盟官方公報》，公報刊出滿 20 天才正式生效。`
- 改成：`規則第 7 條則寫明，生效日是刊登在《歐盟官方公報》之後的第二十日。`（摘要與 FAQ 用同義的短句）
- 來源（S2 第 7 條）：`This Regulation shall enter into force on the twentieth day following that of its publication in the Official Journal of the European Union.`
- 為什麼：兩件事各自有來源——新聞稿寫審查期在生效之前，第 7 條寫生效日的算法——但沒有任何一份文件印出「刊登發生在審查期之後」。把兩件事串成時序是自己補的。改寫後兩個條件都在，且都指得到原文。

### 3.5 3.2% 不是 IEA 的數字（正文第一節）

- 原文：`規則本文的說明備忘錄則寫更精確的 3.2%。這組數字是執委會引用國際能源署的推估，不是執委會自己量到的。`
- 改成：`規則本文的說明備忘錄寫的則是 3.2%，而且在註腳把這個比例指向另一份歐洲電力需求統計，不是同一個出處。兩個百分比都是推估，不是執委會自己量到的。`
- 來源（S2 備忘錄第 1 節）：`In 2024, data centres in the EU consumed 68 TWh of electricity1. This consumption is expected to rise to 114 TWh by 20302, reaching 3.2% of the electricity demand of the Union3.` —— 註腳 1、2 是 IEA，**註腳 3 指向另一份歐洲電力需求資料**。
- 為什麼：原句把 IEA 的歸因蓋到 3.2% 上，那是兩個不同的資料來源。「更精確」也是編輯判斷：兩個百分比的分母來源不同，不是同一個數字的精確版。站主的「>3% 與 3.2% 要分開」這個裁定仍然照做。

### 3.6 `around 68 TWh` 的限定詞（正文第一節與摘要第 5 句）

- 原文：`從 2024 年的 68 TWh`
- 改成：`從 2024 年的約 68 TWh`
- 來源（S1 Background）：`consuming around 68 TWh of the EU's electricity in 2024 alone`
- 為什麼：該句歸給新聞稿，限定詞不可省。（S2 的備忘錄另外印不帶 `around` 的 68 TWh，兩處不衝突。）

### 3.7 QR code 連到哪裡（正文第二節）

- 原文：`以及可以掃描連到細節的 QR code。`
- 改成：`以及掃了就連回歐洲資料庫上這張標籤的 QR code。`
- 來源（S2 第 2 條）：`'quick-response (QR) code' means a matrix barcode included on the label of the data centre that links to the location in the publicly accessible space of the European database where this label is stored.`
- 為什麼：連過去的是這張標籤本身，不是「更多細節」。

## 4. 留給站主／協調者的事

1. **「500 kW 是既有門檻」的來源缺口**：站主已裁定照寫，但四份 `sources[]` 沒有一份逐字印出這一點。S1 只印「涵蓋 500 kW 以上」，S2 只在新增的第 3 條第 5 項印「低於 500 kW 可自願參加」。逐字支持它的是 DG ENER 的最低效能標準研究頁（研究紀錄 `unverified_or_excluded` 第 2 條，因 `sources[]` 四條上限沒有納入）。要把這句話寫得更穩，就得把研究頁換進 `sources[]`（會擠掉現有四條之一）。本輪未動。
2. **標籤效期的但書沒寫**：第 3 條第 3 項還有一段——會員國若沒有在 8 月 15 日前向資料庫表示「境內通報已完成」，該座資料中心的標籤效期會延長到補完為止，最晚到當年 12 月 31 日。正文與 FAQ 只寫了基本規則。段落字數改後 2,840 字（上限 3,000），還塞得下一句，是否補由協調者決定。
3. **外國人名沒有中文**：`Teresa Ribera` 與 `Eurostat` 首次出現都只有英文。查核不替人名造中譯（造了就是沒有來源的新事實），留給協調者決定要不要補。
4. **正文仍帶一點查證口吻**：第二段（「這一篇的資料在……查核，讀的是……」）是科技垂直 `check_article.py` 的固定結構；第五節的「問卷實際題目本站沒有查到」是研究紀錄 `must_not_write` 第 16 條指定的寫法（要寫成「讀不到」而不是「沒有寫」）。兩處都保留；若站主要進一步淡化，得連規格一起改。
5. **`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug**，圖上的四個時間點要照改後的圖說畫（第三格是「2027 年 8 月 15 日前」）。

## 5. 讀者優先檢查

- 「本文」在正文出現 5 次，全部是「**規則**本文」（指 C(2026) 3472 final 的條文），不是文章自稱；文章自稱一律用「這一篇」。符合 DELTA-4-7 §14。
- 「這篇」只出現 1 次，指的是新聞稿（「IP/26/1667 這篇公告」），不是文章自己。
- 「官方」在正文 3 次，沒有「官方頁寫」這類句型；每段最多一個歸因語（第一節那段原本有「規則寫明」＋「官方」兩個，改寫後只剩清楚指名的兩份文件）。
- `description` 146 字，句尾只有「（2026 年 9 月查證）」，沒有查證流水帳、沒有選材計數。
- 第一段就寫出事件日與「通過 ≠ 生效」；台灣的位置寫在第五節（四份文件都沒提到台灣）。
- 沒有購買建議、沒有推薦式比價、沒有把標籤講成挑雲端服務的依據；沒有投資免責 callout。
- 日期一致：slug 尾碼 `20260921` ＝ `news_date` `2026-09-21` ＝ 正文第一段「2026 年 9 月 21 日」。

## 6. 自檢（改完後，原樣）

```
OK tech-news-eu-data-centre-rating-20260921 zh-TW paragraphs 2840
EXIT_CODE=0
```

```
tech-news-eu-data-centre-rating-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-eu-data-centre-rating-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-eu-data-centre-rating-20260921/diagram-1.svg
1 entries checked
EXIT_CODE=1
```

`image_missing` 與 `raw_internal_url` 是出圖與 relink 之前的預期輸出，與撰稿代理當時的輸出相同。

## 7. 結論

`needs_second_round`（依 DELTA-4-7 §12，第一輪一律要有第二輪）。本輪改了 **7 處事實**，分佈在 11 個位置（摘要 3 句、正文 4 段、圖說、FAQ 2 題、研究紀錄 4 處）。其中 3.1（發標時點）與 3.2（WUE 算法）動到骨幹敘述，請第二輪逐字回 S2 第 3 條、S3 附件三複核，並複核本輪新寫進去的每一句。研究紀錄本身品質很好：63 條 `verbatim_quote` 今天全部命中，四條來源與撰稿時逐位元組相同；本輪的錯誤有兩處源自研究紀錄自己的中文轉寫（3.1、3.2），已在研究紀錄一併訂正。
