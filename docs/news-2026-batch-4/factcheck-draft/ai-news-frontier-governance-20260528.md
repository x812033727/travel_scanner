# 獨立查核：ai-news-frontier-governance-20260528

查核者：獨立查核代理（未參與撰稿）。查核日 **2026-09-18**（與內容包、研究紀錄的 `checked_on` 一致，未更動）。
方法：四條 `sources[]` 全部當天以 `curl -sL -A "Mokaair-editorial"` 重抓並讀正文；兩份 PDF 以系統 `python` + pypdf 6.16 重抽文字；
leginfo 頁剝成純文字整頁讀完；RSS 以標題與 canonical link 定位項目（不記筆數）。
逐條核對 **96 條主張**（正文每句、summary 五句、表格每格與 caption、圖解四格與 caption、兩個 callout 欄位、FAQ 每題答句、title、description）。
**改了 19 處**，其中 4 處是來源直接推翻的說法。

---

## 1. 來源重抓結果（2026-09-18）

| # | URL | HTTP | bytes | 落地是否正文 |
|---|-----|------|-------|--------------|
| 1 | `cdn.openai.com/pdf/e37d949b…/openai-frontier-governance-framework.pdf` | 200 | 6,136,955 | 是。md5 `efeae18be97ece7b1a71e7afcf2019d6`（與紀錄相同）、`Last-Modified: Wed, 27 May 2026 16:04:12 GMT`、22 頁、抽出 30,700 字、metadata 只有 `Super PDF Plugin`（無 CreationDate／ModDate） |
| 2 | `leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=BPC&…chapter=25.1.&article=` | 200 | 160,832 | 是。剝成 21,390 字純文字，22757.10–22757.16 七條完整；`Effective January 1, 2026.` 出現 **7** 次、`Amended by` **0** 次 |
| 3 | `cdn.openai.com/pdf/18a02b5d…/preparedness-framework-v2.pdf` | 200 | 170,399 | 是。`Last-Modified: Mon, 09 Jun 2025 21:27:02 GMT`、22 頁、抽出 67,259 字，封面 `Version 2. Last updated: 15th April, 2025` |
| 4 | `openai.com/news/rss.xml` | 200 | 736,773 | 是。XML 正文；FGF 項目的 title／link／category `Safety`／pubDate `Thu, 28 May 2026 00:00:00 GMT` 與紀錄逐字相同 |

四條全部讀得到正文，沒有擋阻頁、軟性 404 或轉址殼。`openai.com/index/*` 今天未再測（本文沒有任何句子掛在它上面）。
**第 2 條的 160,832 bytes 與撰稿者記的 161,728 不同**，差在 JSF 的 ViewState token，不是條文；七條與其註記完全一致。這是活值，不是錯誤。

`verbatim_quote` 逐條做連續字串比對（NFKC＋引號＋連字號＋PDF 斷字正規化後）：**27 條有引文的全部通過**。
唯一一條表面 MISS 是 `Safety and Security Model Report (referred to as "Transparency Reports"…)`——
pypdf 把它抽成 `T ransparency`，同一份抽取裡還有 `T ype II`、`U pdate`、`F rontier`、`G overnance`，是抽取的字距假象，不是文件的字。

---

## 2. 改掉的 19 處

### 2.1 來源直接推翻的（4 處）

**(1) 誰被管到 —— S2P3 與 S4P3。**
原文：「只有和關係企業合計、前一年營收超過 5 億美元的『大型前沿開發者』，才必須公開這份框架並負擔後面提到的申報與罰則義務，OpenAI 屬於這一類。」
第四節接著把「大型前沿開發者」當主詞一路帶到透明報告與事故通報。
法條寫的：22757.12(a)、(b)、(d) 與 22757.15（罰則）的主詞是 `A large frontier developer`；
但 **22757.12(c)(1)**「Before, or concurrently with, deploying a new frontier model…, **a frontier developer** shall clearly and conspicuously publish… a transparency report」
與 **22757.13(c)(1)**「**a frontier developer** shall report any critical safety incident… within 15 days」的主詞是**所有前沿開發者**。
→ 兩段都改成分兩層寫。另外「OpenAI 屬於這一類」**沒有任何來源**（四份來源都沒印 OpenAI 的營收），
改成文件自己說得出口的事：OpenAI 在 FGF 裡把這份文件稱為自己依 TFAIA 提出的『前沿人工智慧框架』。
**為什麼重要**：原寫法把透明報告與事故通報的義務縮小到最大的幾家，等於寫錯了「誰被管到」。

**(2)「實體財產」—— S2P2。**
原文：「所以 10 億美元算的是實體財產與人身安全，不是市值蒸發。」
法條 22757.11(l) 逐字：`"Property" means tangible or intangible property.`
→ 改成照抄法條的「有形或無形財產」，並把 22757.16 的股權除外寫成它自己的範圍（只排除股權價值損失），不再推廣成「只算實體」。

**(3) CBRN 第 2 級的對象 —— S3P2。**
原文：「讓**不具專業背景**的人也能製造已知的生化威脅」。
FGF 逐字：`to novice actors (**anyone with a basic relevant technical background**)`——是「具備基本相關技術背景」的新手，意思相反。
同段「比較基準是『2021 年時**任何人都能取得**的工具』」也不是原文；原文是 `relative to **unlimited access to baseline of tools** available in 2021`。
→ 兩處都改回原文的意思。

**(4)「沒有指名特定第三方」—— S1P3。**
FGF 第 5 頁自己就點名了：`industry bodies **such as the Frontier Model Forum**`。
→ 負面句收窄到真正成立的那一個：**沒有指名任何第三方評測機構**（第 5 節只有 `This may include independent third-party evaluators`，全文 `third` 只出現 2 次，都是通稱）。
同段另外兩個問題一併修：「主要靠公司內部研究」的「主要」不在原文（`draws on our own internal research and signals`）；
「原文是『可能徵詢』」把第 2.1 節（`where appropriate`）與第 5 節（`We may solicit and obtain input from external experts`）**兩句不同段落的話接成一句**，現在各自歸位。

### 2.2 限定詞、範圍與歸因（9 處）

| 位置 | 原文 | 改成 | 來源怎麼寫 |
|---|---|---|---|
| S1P1、表格「適用依據」 | 「FGF 要**同時滿足兩地**法定要求」／「加州 TFAIA 與歐盟行為準則」 | 「要滿足多部前沿人工智慧法規的**基本**法定要求，文件**舉出兩項**」／「加州 TFAIA、歐盟行為準則**等**」 | `Our FGF is designed to meet the **baseline** legal requirements of **various** frontier AI laws, **including**:` |
| S1P1 | 「整理公司對…四類」 | 「整理公司**目前**對…四類」 | `this FGF definition **currently** addresses the following systemic risk categories` |
| S1P2 | 「與既有的 PF **有重疊**」 | 「**在某些方面**與…重疊」 | `The FGF overlaps **in some areas** with our existing Preparedness Framework` |
| S2P1、summary 2 | 「定義**為**…50 人**以上**死亡或 10 億美元**以上**」 | 「定義**『包含』**…**超過** 50 人死亡或 10 億美元」；SB 53 側補回「**或重傷**」 | FGF：`definition of systemic risk **includes**… **including** risks that a model will materially contribute to **greater than** 50 fatalities`；法條：`the death of, **or serious injury to**, **more than** 50 people or **more than** one billion dollars` |
| S2P2 | 「以**類似**形式公開取得」 | 「以**『實質上類似』**的形式」 | `otherwise publicly accessible in a **substantially similar** form` |
| S3P3、FAQ 5 | 「這類風險**更適合**靠部署後監控處理」 | 「**OpenAI 認為**這類風險**『可能』**更適合…」 | `OpenAI believes that these risks **may** be best addressed through system level mitigations` |
| S4P2 | 「會在完成評估後更新」；「或依行為準則附錄認定模型**同樣安全**」 | 補回「**視情況**」、「同樣安全**或更安全**」、「**計畫**在不到一個月內」 | `we will update our Model Report **as appropriate**`；`similarly safe **or safer** (under Appendix 2.2…)`；`**we plan to** release a more capable model in less than a month` |
| S4P3 | 「**部署新模型前**要公開一份透明報告」 | 「部署新的前沿模型**或其實質修改版本之前或同時**」；24 小時的門檻改成法條的「**死亡或嚴重身體傷害**的立即風險」 | `Before, **or concurrently with**, deploying a new frontier model **or a substantially modified version of an existing frontier model**`；`poses an **imminent risk of death or serious physical injury**` |
| S4P4、FAQ 4 | 「每項違規**最高可能面臨** 100 萬美元民事罰鍰」、「發布不實聲明」 | 「**依情節輕重**、每項違規**不超過** 100 萬美元」、「做出**重大不實或誤導**陳述」，FAQ 4 補上善意除外 | `a civil penalty **in an amount dependent upon the severity of the violation** that does not exceed one million dollars`；22757.12(e)(2) `does not apply to a statement that was made **in good faith** and was reasonable under the circumstances` |

### 2.3 分級那一段的過度概化（S3P1）

原文：「文件說這是『可量化的門檻』，用來做內部決策依據，只是沒有把量化結果印出來」——一句話套在三類上。
文件對三類用了**三個不同的動詞**：

- 網路攻擊：`a tier system that **seeks to quantify** model capabilities… We use these **measurable thresholds** for decision-making related to offensive cyber capabilities.`
- CBRN：`a tier system that **quantifies** model capabilities against weapons and threat development uplift metrics.`
- 喪失控制：`a tier system that **describes** model capabilities…` 而且緊接著 `**Outside of risks related to AI self-improvement, these risk tiers remain exploratory and may evolve substantially.**`

→ 改成各自照抄，並補上喪失控制那句限定。原稿把「仍在探索」寫成只有有害操弄才有的狀態，
而文件對喪失控制的分級也這麼說——這是撰稿者提醒要重看的第 3 點的同一種問題，只是出現在別的地方。

### 2.4 用檔案標頭證明「就是當初那一版」（S1 第 1 段、第二段開頭）

原文：「文件檔案自 5 月 27 日上傳後不曾更動，本文今天重新下載比對雜湊值，**確認讀到的就是當初發布的版本**」與
「確認今天讀到的 FGF 內容與發布當時相同」。
md5 相同＋`Last-Modified` 只能證明**這一個檔案沒有被原地覆寫**（這正是修正清單 `live_data_warnings` 說的），
不能證明別的網址沒有新版。→ 兩處都改成有餘地的寫法。
同理，S1P2 的「OpenAI **目前公開的** PF 是 2025 年 4 月 15 日更新的第 2 版」原本只靠 blob 標頭，
現在改由 **source 4** 撐住：新聞頻道最後一則 Preparedness Framework 更新公告的 pubDate 是 `Tue, 15 Apr 2025`，今天的抓取裡之後沒有更新的 PF 項目。

### 2.5 撰稿者點名要重查的三句

**(a)「TFAIA 生效約五個月後 OpenAI 才公布 FGF」——刪掉了。**
兩個日期各自有來源（2026-01-01 印在法典頁七條每一條底下；2026-05-28 是 RSS 的 pubDate），
但「約五個月」是編輯自己減出來的，而「**才**」暗示了一個沒有來源的評價（拖延／落後）。
BRIEF 錯誤型態 9 的規則是「來源沒印就不是事實」。修正清單 must_fix 11 建議寫「生效約五個月後」，
但 BRIEF 與修正清單衝突時以 BRIEF 為準，撰稿者自己也提了「站不住就改成只並列兩個日期」的退路。
→ 現在只並列：「法典頁這一章七條都標注 2026 年 1 月 1 日生效、沒有一條標注修正，FGF 公布日則是同年 5 月 28 日。」
生效日這個一手事實仍然寫在文章裡，must_fix 11 的實質目的達成。

**(b) 六個月模型報告與歐盟法的範圍限定句 —— 順序對，但斷言太滿。**
FGF 第 18 頁的順序確實是「EU AI Act 範圍句 → 六個月」，原稿的順序忠實。
問題在原稿寫「**限於**受歐盟人工智慧法規範…的模型」**涵蓋整節**，而文件只把範圍句放在第一個條件句上，
六個月那句用的是 `We will **in any event** determine whether…`，並沒有明文說自己也受同一個範圍限制。
→ 改成報告文件的順序與用字（「開頭限定在…」「接著文件寫『無論如何』」），不替文件下範圍結論。

**(c)「OpenAI 目前公開的 PF 是 2025-04-15 的第 2 版」會不會被讀成「FGF 指的就是這一版」。**
原稿已經有「FGF 提到『既有的 PF』時並未指名版本」，方向對。
改動是把「目前公開的」這個現狀斷言換成可追的證據（見 2.4），語序也調成先講「沒有指名版本」再講 PF 的日期，
讓兩件事的關係只停在「這是目前找得到的那一版」，不延伸成「FGF 指的是它」。

### 2.6 兩個 must_add 判定為「不寫就會誤導」，已補進 FAQ

撰稿者列了四個因名額與篇幅沒寫的 must_add。逐一判：

| must_add | 判定 | 理由 |
|---|---|---|
| **FGF 與 PF 分級文字重疊** | **補**（新 FAQ 7） | 文章的表格把兩份文件的分級並排成「兩套不同的制度」。實際上今天逐字比對：FGF CBRN Tier 2／Tier 3 與 PF 生化類別 High／Critical **逐字相同**（只差 `novice` 外面的引號）；Cyber Tier 3 與 PF 資安 Critical 只差一個冠詞與兩處連字號寫法。不寫，讀者會把 FGF 的分級當成新東西——這正是「不寫就會誤導」。 |
| **SB 53 聯邦安全港 22757.13(h)-(j)** | **不補** | 它只讓開發者「deemed in compliance with **this section**」（＝22757.13 事故通報），碰不到文章真正的那句（沒遵守自己寫的框架 → 罰則，走 22757.12／22757.15）。而且它雙重附條件：OES 要先以規則指定某個聯邦法規，開發者還要聲明採用——四份來源都沒說這兩件事發生過。寫進去要帶的但書比事實本身還長。留給站主。 |
| **AG 年度報告 22757.14(d)** | **不補** | 那是吹哨者（covered employee）報告的年度彙整，與本文主線隔一層。改補了更貼題的近親：**22757.13(g)** 緊急服務辦公室自 2027-01-01 起的年度事故彙整報告（在新 FAQ 8）。 |
| **歐盟行為準則 Measure** | **不補** | 那份歐盟安全與資安章 PDF 不在這一輪的四條 `sources[]` 裡，今天也沒讀。要寫就得換掉一條來源。維持撰稿者的處理。 |

**另外自行補了一個 must_add（新 FAQ 8），理由與前者同級：**
第四節的標題是「公布之後，**誰能追蹤**這份文件有沒有兌現」，標題本身也是「**誰追得到**」，
原稿卻列了七項公布與通報義務、完全沒說「公布」是有洞的：

- **22757.12(f)**：開發者可以為保護營業秘密、自身資安、公共安全或美國國安，對公開文件做必要遮蔽（要說明遮蔽的性質與理由，並保留未遮蔽版本五年）。
- **22757.13(f)**：通報給緊急服務辦公室的事故報告、22757.12 的內部使用風險評估摘要，**依法排除在加州公共紀錄法之外**，一般人調不到。
- **22757.13(g)(1)**：緊急服務辦公室自 2027-01-01 起每年公布去識別化、彙整過的事故報告——這是讀者真正讀得到的那一份。

同時把原稿第四節結尾那句編輯結論「公開這份文件，等於讓 OpenAI 的承諾多了一層可以被追究的法律效力」刪掉：
那是文章自己的推論，而且正好是上面兩條限縮的對象。

### 2.7 其餘（負面句、summary、callout、篇幅）

- **所有絕對否定句都收窄**成「以本文 2026-09-18 抽取全文、用詞界比對，未見 X」。
  實際比對結果（區分大小寫不敏感、詞界）：Taiwan 0、Japan 0、Korea 0、China 0、United Kingdom 0、India 0、Canada 0、Singapore 0、Australia 0；Ireland 4、California 1、United States 1、European 2。
  另查 `10^26`／`500`／`five hundred`／`million` 在 FGF 全文各 0 次——這正是文章能把那兩個數字歸給法條、不歸給 OpenAI 的依據。
- 「ChatGPT 介面**不會**因此變化」是預測，改成「文件**沒有宣告**任何介面調整」。第五節標題同步改成「文件未提到台灣，也沒有介面公告」。
- **callout**：「FGF 是一份揭露文件，**不是新的安全承諾**」是文章自己的定性，而 FGF 裡確實有承諾（12 個月總檢視、30 天 changelog）。
  改成「不是**產品或服務公告**」，並把重疊那句改回文件的「在某些方面」。
- **summary** 第 2、4、5 句跟著正文改（`包含` 不是 `定義為`、`超過` 不是 `以上`、罰則補上主詞、台灣那句加上查法）。
- **篇幅**：補進上述限定詞與條件後正文一度到 3,443 字。**沒有刪掉任何但書或限定詞**來湊字數，
  改的是敘述：刪掉與 FAQ 6 幾乎逐字重複的第五節第三段、把第二節第四段的編輯評語收掉、
  把兩個 must_add 放進 FAQ（FAQ 不計入 1,800–3,000 的段落字數）。最終 **2,988 字**。

---

## 3. 查過而且正確、不用改的部分

- **事件日**：RSS 項目的 title／canonical link／`category Safety`／`pubDate Thu, 28 May 2026 00:00:00 GMT` 與紀錄逐字相同。
  `00:00:00 GMT` 是這個 feed 的佔位時刻（BRIEF 錯誤型態 11），文章只用日期不用時刻；GMT 5/28 00:00 在台北仍是 5/28。
  `news_date`、slug 尾碼、`display_order 153` 都對。
- **FGF 是同一份檔**：md5、bytes、頁數、metadata 全部與紀錄一致。
- **法條七條的生效日與「仍是現行法」**：`Effective January 1, 2026.` × 7、`Amended by` × 0，今天重驗。法典頁把算力門檻印成字面的 `10^26`。
- **PF 的嚴重危害註腳**含撰稿者已補上的中間那句，逐字無誤；PF v2 的三個 Tracked Categories（生化、資安、AI 自我改良）與 High／Critical 兩個門檻，
  就是表格第二、三列寫的，正確（Nuclear and Radiological、Long-range Autonomy 等是 Research Categories，沒有被誤列）。
- 12 個月「至少」、30 天 changelog、兩個董事會機構、100 萬美元上限與州檢察長專屬訴權、三項排除、股權除外、
  10^26 與 5 億美元的定義、Model Report 與 Transparency Report 的對應、四類風險與有害操弄沒有分級表——全部逐字對得上。
- **`27/7/365`** 確認仍印在 FGF 第 17 頁；撰稿者不引用、不自行改成 24/7 的處理**維持不動**。
- **界線檢查**：沒有購買建議、沒有推薦式比價（本文不涉定價）、沒有未歸因的廠商宣稱（FGF 的每一項承諾現在都寫成「OpenAI 承諾／表示」或「文件寫道」）、
  沒有把預告／草案／分批開放寫成已生效（FGF 是已公布的文件，不涉分階段開放）。
  `topics` 是 `["ai","ai-news"]`，不帶 `finance`，**只有一個 callout**，沒有投資免責段落。

---

## 4. 留給站主的事

1. **聯邦安全港（22757.13(h)-(j)）刻意沒寫**，理由見 2.6。若站主要寫，需要自己的一句話與自己的但書。
2. **兩個結尾連結**：索引標題與 `ai-news-gpt-55-instant-20260505` 的標題都還是暫填，兩個自檢 FAIL 就是這兩條（批次規格允許），由協調者的 align_links 處理。
3. **歐盟行為準則安全與資安章**仍不在 `sources[]`，所以文章對 Measure 1.1／7.6／10.1／10.2 一個字都沒寫，
   包含「Measure 1.1 要求的時程估計 FGF 沒有公布」這個可查核的缺口。要寫就得花掉四條來源的一格。
4. **法典頁的 bytes 是活值**（今天 160,832、撰稿者 161,728，差在 ViewState），研究紀錄 `sourcing_notes` 保留撰稿者自己那次抓取的數字，沒有改。
5. 研究紀錄的圖解第三格由「3 級看監控可否辨識」改為「**3 級，但仍屬探索性質**」——原標籤雖然對得上 FGF 的 Tier 3 描述，
   但改稿後正文不再解釋它；新標籤與 S3P1 的敘述一致。**畫圖時請用新的。**

---

## 5. 自檢輸出（原樣）

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-gpt-55-instant-20260505
```

只剩批次規格允許的兩條連結 FAIL。正文 2,988 字（1,800–3,000）、description 190 字、title 37 字、
五節各 3／4／3／4／2 段、一個 table（4 欄 4 列）、一個圖解、summary 5 句、FAQ 8 題、**1 個 callout**、2 個連結。

---

## 6. 結論

**`needs_second_round`** —— 改了 19 處，其中 4 處是來源直接推翻的事實（誰被管到、財產的定義、CBRN 第 2 級的對象、「沒有指名第三方」），
另有一處刪掉了第四節的骨幹結論、兩處補進新的 FAQ。
動到骨幹論述的幅度足以觸發規格第 3 節的門檻，建議第二輪只做一件事：
**把第一輪新寫進去的每一句（S1P1、S1 三段、S2 全部四段、S3P1、S3P2、S3P3、S4 四段、S5 兩段、summary 2／4／5、表格兩格、callout、FAQ 2／4／5／7／8）逐句再回一次來源**，
其餘已確認的部分不必重做。

---

## 第二輪

查核者：第二輪獨立查核代理（未參與撰稿，也未參與第一輪）。查核日 **2026-09-18**（三處 `checked_on` 一致，未更動）。
方法：四條 `sources[]` 全部自己重抓、自己重抽，沒有沿用第一輪留在暫存區的檔案。
範圍依第二輪規格：第一輪**改動過的每一段**與**新寫進去的每一句**，共 **71 條主張**；`verbatim_quote` 全部以程式做連續字串比對。
**改了 14 處**，其中 3 處是法條直接推翻的說法——三處都落在第一輪自己新寫的材料裡。

---

## 7. 來源重抓結果（2026-09-18，第二輪自己抓）

| # | HTTP | bytes | 落地是否正文 | 與第一輪比對 |
|---|------|-------|--------------|--------------|
| 1 FGF PDF | 200 | 6,136,955 | 是。22 頁、抽出 30,722 字、md5 `efeae18be97ece7b1a71e7afcf2019d6` | 完全相同 |
| 2 leginfo | 200 | **161,280** | 是。剝成 21,390 字，22757.10–22757.16 七條完整 | 第三個不同的 bytes（撰稿者 161,728、第一輪 160,832）——ViewState，不是條文 |
| 3 PF v2 PDF | 200 | 170,399 | 是。22 頁、抽出 67,281 字、md5 `648b1dfe1af9fa3fe37bc17100835371`、封面 `Version 2. Last updated: 15th April, 2025` | 相同 |
| 4 RSS | 200 | 736,773 | 是。解析出 1,207 筆（不寫進文章） | FGF 項目 title／link／category／pubDate 逐字相同 |

`verbatim_quote`：有引文的 **43 條全部通過**。兩條表面 MISS 都是 PDF 抽取假象——
pypdf 把 `Transparency` 抽成 `T ransparency`（同一次抽取還有 `T ype II`、`U pdate`、`F rontier`、`G overnance`），
以及 FGF 把 `self-improvement` 斷在連字號上。PF 那一條（第 42 則）因為 LaTeX 把 `pro-vide`、`counterfac-tual` 斷行，
要用忽略連字號的比對才對得上；文件本身沒有差異。

法條今天重數：`Effective January 1, 2026.` **7** 次、`Amended by` **0** 次。
FGF 詞界重數：Taiwan／Japan／Korea／China／United Kingdom／India／Canada／Singapore／Australia／ChatGPT／language(s)／price／region／subscription 全部 **0**；
Ireland 4、California 1、United States 1、European 2、third 2；`10^26`／`500`／`five hundred`／`million` 各 0，`$1 billion` 與 `50 fatalities` 各 1。
`27/7/365` 仍在第 17 頁（1 次），文章裡 0 次，`24/7` 也 0 次。

---

## 8. 第二輪改掉的 14 處

### 8.1 法條直接推翻的（3 處，全在第一輪的新材料裡）

**(1) 2027 年那份年度報告不是「公布」給大眾的 —— FAQ 7（第一輪的「新 FAQ 8」）。**
第一輪寫：「緊急服務辦公室要從 2027 年 1 月 1 日起**每年公布**一份去識別化、彙整過的事故報告。」
22757.13(g)(1) 的動詞是 `shall **produce** a report`，(g)(3) 是
`shall **transmit** a report … **to the Legislature**, pursuant to Section 9795, **and to the Governor**`。
法條從頭到尾沒有寫「公布」。
→ 改成「每年**做出**一份…，**送交州議會與州長**」。
**為什麼重要**：這一題的標題就是「一般人看得到多少」，主旨是「公開≠看得到」，
結果最後一句反而告訴讀者有一份年度報告可以看——正好把整題的結論推翻。

**(2) 遮蔽的理由少了一項、限縮少了一句 —— FAQ 7。**
22757.12(f)(1) 印的是**五項**理由：營業秘密、自身資安、公共安全、美國國安，
以及 `**or to comply with any federal or state law**`。第一輪只寫了四項。
22757.12(f)(2) 的說明義務還帶一句限縮：
`shall describe the character and justification of the redaction in any published version of the document **to the extent permitted by the concerns that justify redaction**`，第一輪也沒有。
另外法條是 `retain the unredacted **information**`，不是「未遮蔽**版本**」。
→ 三處全部補回；遮蔽權的範圍也照法條限在「為履行公布義務而公開的文件」。

**(3)「FGF 新增的主要是第 1 級」是評價，不是比對結果 —— FAQ 6（第一輪的「新 FAQ 7」）。**
第一輪的結語：「換句話說，FGF 新增的主要是比 PF 的 High 更低的第 1 級，以及整套對應法規的治理與申報安排，**不是最上面兩級的門檻本身**。」
兩份文件都沒有這樣說；而且那是拿 CBRN 與網路攻擊兩類的比對，推廣到整套框架。
→ 刪掉，換成比對真正的範圍：只涵蓋 CBRN 與網路攻擊，
FGF 的喪失控制與有害操弄在 PF 的三個 Tracked Categories 裡沒有對應項，兩份文件也都沒說自己的分級可以互相對照。

### 8.2 指派訊息點名的兩題，逐句重做

**FAQ 6：自己重跑一次連續字串比對（用會標記斷行連字號、而不是直接刪掉它的正規化）。**

| 比對對象 | 結果 |
|---|---|
| FGF CBRN **Tier 3** ↔ PF 生化 **[Critical]** | **完全逐字相同**（byte-identical） |
| FGF CBRN **Tier 2** ↔ PF 生化 **[High]** | 只差 `novice` 外面的引號：FGF `to novice actors`、PF `to "novice" actors` |
| FGF **Cyber Tier 3** ↔ PF 資安 **[Critical]** | 兩處：FGF `OR the model can devise`／PF `OR model can devise`；FGF `a high-level desired goal`／PF `a high level desired goal` |

第一輪寫的「CBRN 第 2 級與第 3 級…**逐字相同**」對第 2 級不成立（引號），
「只差一個冠詞與**兩處**連字號寫法」的第二處是 `real-world`——**證明不出來**：
PF 正好把它斷行在連字號上，抽取分不出那是原本就有的連字號還是 TeX 斷字，而 FGF 印的是沒斷行的 `real-world`。
→ FAQ 6 現在**點名兩個差異**，不再報數字；第 2 級的引號差異也寫進去了。
同時補上一句第一輪沒寫的義務層次（見 8.3）。

**FAQ 7：三個條號逐句回原文，條號、主詞、年份、誰對誰報告都對過。**
22757.12(f) 遮蔽權（主詞 `a frontier developer`）、22757.13(f) 排除公共紀錄法（三類報告，文章寫其中兩類）、
22757.13(g) 年度報告（主詞 OES、起算日 2027-01-01、對象州議會與州長）。
另外「一般人**無法調閱**」收窄成「**無法循該法**調閱」——排除於公共紀錄法之外，只證明不能靠那部法調卷。

### 8.3 「誰被管到」：兩個定義、兩層義務（4 處）

| 位置 | 問題 | 改成 | 法條 |
|---|---|---|---|
| S1P1、summary 1 | 「TFAIA **要求公布的**『前沿人工智慧框架』」——只有**大型**前沿開發者才有公布框架的義務（22757.12(a)），而 S2P3 自己也這樣寫；這等於替 OpenAI 歸類成大型前沿開發者，正是第一輪從 S2P3 拿掉的那個推論 | 「TFAIA **所稱的**『前沿人工智慧框架』」 | FGF：`Under California's TFAIA, this FGF is our Frontier AI Framework` |
| S2P3 | 「和關係企業合計、前一年總營收超過 5 億美元的，是『大型前沿開發者』」——**整句沒有主詞**，而同一句後半的「所有前沿開發者」在全文從未定義過 | 補上 22757.11(h) 的定義，讓大型那一層成為它的子集；`preceding calendar year` 補成「前一**曆**年」 | `"Frontier developer" means a person who has trained, or initiated the training of, a frontier model…` |
| S4P3 | 「重大安全事故要在發現後 15 天內通報」——**主詞被省略**，而且前兩個子句的主詞才剛從「大型前沿開發者」換成「所有前沿開發者」 | 「**前沿開發者**發現重大安全事故後，要在 15 天內通報」 | 22757.13(c)(1) `a frontier developer shall report…` |
| FAQ 7 | 透明報告被寫成兩層一模一樣 | 補上 22757.12(c)(2)：**風險評估、評估結果、第三方評測參與程度等摘要只有大型前沿開發者要附** | `a large frontier developer shall include in the transparency report required by paragraph (1) summaries of all of the following…` |

放在 FAQ 而不是 S4P3，是因為正文當時距離 3,000 字上限只剩 12 字。

### 8.4 10 億美元那一段的兩個字（2 處，正文與 FAQ 2 各一份）

- 22757.11(c)(1)**(A)** 是 `Providing expert-level assistance **in the creation or release of** a … weapon`。
  第一輪寫「提供專家級**的化生放核武器協助**」，把協助的範圍放掉了 → 「提供專家級**協助製造或釋放**化生放核武器」。
- 22757.11(c)(1)**(C)** 是 `Evading the control of its frontier developer **or** user`。
  第一輪寫「擺脫開發者**與**使用者的控制」 → 「擺脫**前沿開發者或**使用者的控制」。

22757.11(l)（`tangible or intangible property`）、22757.16（股權除外）、
(c)(2) 三項排除與補回的 `substantially`（「實質上類似」）今天逐字重核，**全部正確，未動**。
文章沒有出現「50 人」以外的人數，也沒有自己算出來的數字。

### 8.5 分級那一段與其餘（5 處）

- **S2P1**：「**這不是 OpenAI 自訂的數字**」是文章自己的推論，沒有來源這樣說（FAQ 2 本來就寫對了）。
  → 「**FGF 沒有註明這兩個數字的出處，但它說**加州這一側處理的是…」。
- **S3P1**：`a tier system that quantifies model capabilities **against** weapons and threat development uplift metrics`——
  被量化的是**模型能力**，提升指標是尺規。第一輪寫成「『量化』**能力提升**」，把受詞換掉了 → 「『量化』**模型能力**」，三個動詞的對比保留。
  同段 `for decision-making related to offensive cyber capabilities` 沒有 internal → 「做**內部**決策」的「內部」刪掉。
- **S3P3、FAQ 5**：FGF 是**兩句、兩個主詞**——`OpenAI's **approach** … remains exploratory` 與 `This **risk tier** is subject to further research and may be substantially changed`。
  第一輪把兩句併成一個引號掛在「作法」上 → 拆開。
  同段類別描述補回文件自己的第一項 `influence operations`（原本被併進「操縱輿論」）。
- **S5P1**：「**沒有一手來源**顯示」範圍不明 → 「**本文查核的四份一手來源**都沒有顯示」。
- **圖解第三格**：「3 級，但仍屬探索性質」→「**3 級，除自我改良外探索中**」。
  FGF 的句子是 `**Outside of risks related to AI self-improvement**, these risk tiers remain exploratory`；正文有這個但書，標籤沒有。**畫圖請用新的。**

### 8.6 騰字的方式（沒有刪掉任何但書）

補上 8.3 與 8.4 之後正文會超過 3,000 字。刪的是 **S5P2 的最後一句**
「依 OpenAI 的說法，FGF 是寫下公司目前的技術與組織流程、說明如何履行法規義務。」——
這句話在 S1P2（「文件寫道，OpenAI 建立 FGF 是為了說明如何履行法規義務、記錄目前…的作法」）
與 callout（「OpenAI 自己說…作用是說明公司如何履行法規義務、記錄目前的作法」）各出現過一次，**連歸因一起**。
刪掉的是第三次重複，沒有任何但書、限定詞或歸因因此消失。
正文 **2,988 → 2,987 字**。

---

## 9. 第二輪查過、確認正確、沒有動的部分

- **第一輪那四處來源推翻的改動全部成立**：22757.12(c)(1)、22757.13(c) 的主詞確實是 `a frontier developer`，
  而 22757.12(a)(b)(d) 與 22757.15 確實是 `large`；`"Property" means tangible or intangible property.`；
  CBRN 第 2 級確實是 `novice actors (anyone with a basic relevant technical background)` 與 `unlimited access to baseline of tools available in 2021`；
  FGF 確實點名 `industry bodies such as the Frontier Model Forum`，也確實沒有指名任何第三方評測機構（`third` 全文 2 次，都是通稱）。
- **第一輪刪掉的那一段沒有帶走任何東西**：被刪的是第五節第三段，內容與「要怎麼自己找到這份文件核對」那題幾乎逐字重複。
  該題今天仍完整保留查證方法（OpenAI 官網找 PDF、加州立法資訊網用 SB 53 或 BPC 第 25.1 章），callout 也重複了同樣的指引。
  **summary 五句今天重驗，每一句都仍有正文句子撐住。**
- **兩個日期並列之後沒有留下評價**：「才」「終於」「遲了」「拖延」「落後」「約五個月」「五個月」在整個內容包各 **0** 次；
  S2P1 只並列 2026-01-01 與 2026-05-28。
  **六個月那一段沒有替文件下範圍結論**：S4P2 照文件的順序與用字寫「開頭限定在…」「接著文件寫『無論如何』」，沒有說六個月那句也受歐盟法範圍限制。
- **`27/7/365`**：仍印在 FGF 第 17 頁，文章裡不引用、不改成 24/7，兩個字串在內容包各 0 次。維持不動。
- **事件日與版本**：RSS 的 FGF 項目（title／link／`Safety`／`Thu, 28 May 2026 00:00:00 GMT`）、
  `Our updated Preparedness Framework`（`Tue, 15 Apr 2025`，今天的抓取裡沒有更新的 PF 項目）、PF 封面第 2 版，全部逐字對得上。
- **界線**：`topics` 是 `["ai","ai-news"]`、不帶 `finance`、**只有一個 callout**、沒有投資免責段落；
  沒有購買／訂閱／升級建議，沒有推薦式比價（FGF 全文 price／subscription／region／language 各 0 次）；
  廠商宣稱全部歸因；第二段明寫「不提供法律意見」；沒有推定台灣適用；**沒有評價 OpenAI 守不守法**。

---

## 10. 第二輪留給站主的事

1. **聯邦安全港（22757.13(h)-(j)）維持不寫**，第二輪重讀後同意第一輪的理由：(i)(2)(A) 只讓開發者「deemed in compliance with **this section**」（＝22757.13），
   而且雙重附條件（OES 要先訂規則指定聯邦法規、開發者要聲明採用），四份來源都沒說這兩件事發生過。
2. **文章全篇不印條號**，所以要核對 FAQ 7 的讀者得自己在 BPC 第 25.1 章裡找 22757.12(f) 與 22757.13(f)-(g)。
   加上條號有助查證，但會引進這一批其他文章沒有的引註體例——請站主決定。
3. **22757.13(f) 排除了三類報告，文章只寫兩類**；第三類是吹哨員工（covered employee）的報告，與 22757.14(d) 一樣刻意留在範圍外。
4. **正文只剩 13 字的空間**（2,987／3,000）。之後要往正文加東西，必須先從正文拿掉等量的字。
5. 第一輪列的四點（安全港、兩個結尾連結、leginfo 的 bytes 是活值、歐盟行為準則不在 `sources[]`）**全部仍然成立**，沒有變動。

---

## 11. 第二輪自檢輸出（原樣）

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-gpt-55-instant-20260505
```

只剩批次規格允許的兩條連結 FAIL。正文 **2,987 字**（1,800–3,000）、五節各 3／4／3／4／2 段、
summary 5 句、FAQ 8 題、1 個 table、1 個圖解、**1 個 callout**、2 個連結，title 37 字、description 190 字。

---

## 12. 第二輪結論

**`ok`** —— 71 條主張重查、14 處改動。
最重的三處都在第一輪自己新寫、沒有人查過的兩題 FAQ 裡：
2027 年的年度報告是「做出並送交州議會與州長」而不是「公布」、遮蔽理由少一項且少一句限縮、
以及把「文字相同」寫成「FGF 新增的主要是第 1 級」這個文件沒有下的結論。
骨幹論述沒有再被更動，來源沒有換，`checked_on` 沒有改。
剩下的都是站主決定的事（條號體例、安全港），不需要第三輪。
