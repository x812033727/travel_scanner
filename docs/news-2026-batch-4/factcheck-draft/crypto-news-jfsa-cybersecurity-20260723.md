# 獨立查核：crypto-news-jfsa-cybersecurity-20260723

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，未改）。
查核方式：`sources[]` 四條全部以 `curl -sS -L -A "Mokaair-editorial"` 重抓並讀 body，兩份 PDF 用**系統 Python**
的 pypdf 重新抽文字（`03.pdf` 讀完全文，`rp_en.pdf` 核對第 1–9、29–34、38–42、46、61、63、65、79、83、112、124 頁）。
任何請求都沒有放入 email、姓名或個人資料。**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，也沒有猜任何網址。

檢查的主張：文章側 **104 條**（正文 15 段拆成 46 句、摘要 4 句、FAQ 8 題的答句拆成 26 句、兩個 callout 的 7 句、
表格 12 格與 caption、圖解 caption 與四格、`hero_label`、title、description）；
研究紀錄側另外逐條複驗 **47 條 `verified_facts`** 與 **12 條 `not_said`**。
**改了 12 處**（3 處是協調者的編輯決定、4 處是事實或範圍問題、5 處是用語統一），另有 5 件留給站主。

## 重抓結果（四條 sources 都還在、內容沒變）

| source | HTTP | bytes | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- |
| 日文政策頁 `/policy/bgin/innovationtop.html` | 200 | 42,889 | 是（`<h1>`「イノベーション推進に向けた金融庁の取組み」） | 頁首三行「令和４年11月４日／令和８年７月23日更新／金融庁」；最新情報 2026 年第一項就是本報告，底下三個 PDF 連結＋「（合同会社デロイトトーマツとの合同研究）」，下一個 `<li>` 是免責語 |
| 報告英文版 `ResearchPaper_dtc_20260630_en.pdf` | 200 | 3,337,715 | 是（125 頁，第 1 頁封面／第 2 頁 Disclaimer／第 5 頁目次） | 封面 June 30, 2026 與 Deloitte Tohmatsu LLC；第 8、9 頁研究發現摘要；第 5 頁目次的 (1)–(10)；第 63、65 頁個案教訓 |
| 2026-04-03 公布頁 `/news/r7/sonota/20260403/20260403.html` | 200 | 38,261 | 是（`<h1>` 是取組方針（案）公眾意見結果） | 頁首兩行日期；令和８年２月10日至３月11日徵詢、「計18件のコメント」；別紙１〜４與「令和８年７月23日、以下の英語版を公表しました。」 |
| 取組方針英文版 `/news/r7/sonota/20260403/03.pdf` | 200 | 258,085 | 是（9 頁＝未編號封面＋印刷正文 1–8） | 文首 April 3, 2026／Financial Services Agency；第一章至第五章全文 |

四條**零轉址、零擋阻頁**，位元組數與撰稿當天完全相同，PDF 的 `CreationDate`／`ModDate` 也一字不差
（`rp_en.pdf` D:20260721113802／114825，`03.pdf` D:20260706150955／20260722091407）。
所以 `checked_on` 維持 2026-09-17，**沒有因為我今天重查而改動**。

**`verbatim_quote` 全面複驗**：47 條（含我新增的 3 條）以「只把 PDF 換行壓成一個半形空格、其餘一字不動」比對，
**47/47 在今天抓到的來源裡找得到**，而且每一條的 `url` 都在 `sources[]` 四條之內。紀錄自己宣告的抽取器瑕疵
（`ha s become`、`large- scale`、`F rom Program Year`、`A s shown`、`( Delta)`、`widely -used`）在我這台機器的 pypdf 同樣出現，
引文確實全部避開了那些字串。

## 改掉的 12 處

### 協調者的三個編輯決定

1. **title 過度概括**（title 與研究紀錄 `title` 同步）。
   「不是金鑰被偷，是簽章前的系統被動手腳」→
   **「日本金融廳公布加密資產資安研究報告：有一類外流不是金鑰被偷，而是簽章前的系統被竄改」**（41 字）。
   報告第 8 頁只寫 “we confirmed attacks that **did not involve** the theft of signing keys themselves, but instead tampered with
   components…”，是確認「有這一類」；`03.pdf` 印刷第 1 頁也只寫 “**not necessarily** caused by the theft of signing keys”。
   原標題把兩個限定詞都吃掉了。順帶把 `description` 的「說明報告怎麼重新解釋近年的資產外流」改成
   「說明報告把**哪一類**資產外流重新歸因到簽章前的系統」（146 字，仍在 120–200）。
   摘要第二句原本就寫「有一類」，FAQ 第 3 題也是，兩處不必改。
2. **刪掉十個個案的具名清單**。原文「依序是 Bybit、SwissBorg、Radiant Capital、Balancer v2、Euler Finance、
   Kokomo Finance、Resolv、Drift、Litecoin、Kelp DAO／LayerZero；本文只把它們當成報告記載的資安事件列出。」整串刪除。
   改寫成報告自己撐得住的描述：「報告的個案研究從 (1) 編到 (10)，依報告自述，它分析的是含 DeFi 在內的加密資產相關服務
   近期案例，聚焦造成重大損失的主要攻擊手法，舉的例子是第三方遭攻破、智慧合約弱點、閃電貸攻擊與惡意程式攻擊。
   本文不點名個案的業者與協議……」。
   - 「(1) 編到 (10)」對回**第 5 頁目次**（兩欄排版，逐字讀過去是 `(1) Bybit (6) Kokomo Finance`）。
   - 分類照**報告自己的軸線**：第 8 頁 “focusing on major attack methods that resulted in large losses, **such as**
     third-party compromises, smart contract vulnerabilities, rug pulls, flash loan attacks, and malware attacks”；
     第 30、31 頁把這些手法當欄位標題、各挑代表性案例（Third-party Vulnerability→(1)(2)、Contract vulnerability→(4)、
     Rug pull→(6)、Flash loan attack→(5)、Malware attack→(3)），第 32 頁另收 2026 年 2 月之後的事件（(7)–(10)）。
   - **注意一個反例**：協調者示意的「中心化交易業者與去中心化金融協議」**不是**報告對這十個個案的分類。
     報告的分類軸是攻擊手法；CEX 與 DeFi 出現在第 3、4 頁講產業結構與研究背景的地方，不是個案的分桶依據。
     依「類別怎麼寫以報告目次與內文實際的分類為準」，我沒有照抄那個寫法。
   - 「本文不寫個案的損失金額與件數統計」保留，並補上「不點名個案的業者與協議」。
   - FAQ、摘要、圖解四格、`hero_label`、`hero.alt` 逐一查過：**原本就沒有任何具名平台、協議或資產**，不必處理。
     以太坊基金會／Clear Signing／ERC-7730 保留，全部對回第 65 頁（見下）。
3. **用語統一**。第 4 節第 2 段、第 5 節第 1 段、FAQ 第 2、6、7 題的「虛擬資產」全部改成「加密資產」；
   第一次出現（第 4 節第 2 段）寫成「**加密資產交換業者（日文『暗号資産交換業者』）**」，之後一律「加密資產交換業者」。
   其中 FAQ 第 6 題的「防止**虛擬資產**遭未授權移轉」對回報告第 9 頁 “measures to prevent unauthorized transfers of
   crypto-assets”，本來就該是加密資產。日文文件標題與機關日文名照原文保留（兩個 callout 裡的
   「暗号資産関連業者における…」「暗号資産交換業等における…」沒有動）。
   **全篇唯一剩下的「虛擬資產」是第二個站內連結的文字**，那是台灣那篇的正式 title，`check_article.py` 逐字比對，不可改。
   研究紀錄的 `editorial_brief`（原本寫「法規語境寫虛擬資產」）與 `must_not_write` 已同步改寫，否則翻譯階段會照舊規則改回去。

### 四處事實或範圍問題

4. **第 4 節第 3 段第四個否定句超出「這份文件沒有寫」**。
   「TLPT 也沒有寫是哪幾家或**結果是否公開**」→「TLPT 沒有寫是哪幾家，**只寫結果個別回饋受測業者、共通課題回饋業界**」。
   `03.pdf` 印刷第 7 頁確實寫了結果怎麼分送：“provide assessment results to the targeted service providers individually
   and extracted common issues to the industry as a whole”。原句雖然字面成立（文件沒寫會不會對外公開），
   但會被讀成文件對結果一字未提。
5. **第 1 節第 1 段的「這一則不是以獨立新聞稿發布的。」整句刪除**，改成「報告是掛在政策專頁的最新情報清單裡公布的」。
   那個否定句的依據是 `/news/index.html` 與 `/en/news/index.html`，**兩者都不在 `sources[]` 裡**，而且寫成了無範圍的否定。
6. **第 5 節第 1 段拆開一個跨頁的因果接合**。原文「仍應確認該第三方……等控制，**因為**外部服務商被攻破可能外溢到
   業者自家服務或使用者資產」把第 63 頁與第 9 頁接成一個因果。第 63 頁的原文是 “it is **important** — even if signing keys
   are not entrusted to the third party — to confirm that…”（重要，不是「應」），而第 9 頁的外溢句是「因此**要建立自保措施**」
   的理由，不是「因此要確認第三方控制」的理由。已改成「……等控制**仍然重要**；**報告另外寫**，外部服務商被攻破可能外溢到……」。
7. **「報告用一整節講「盲簽」」是對報告結構的誤述**。第 65 頁是 “Lessons learned from case study (3/4)”，
   頁首那句是 “It is important to verify transaction details at the time of signing through multiple measures, including
   wallet functions that improve message readability.”；報告**沒有任何一節以盲簽為標題**
   （blind sign 出現在第 36、37、39、41、42、53、65、66、72 頁，都不是節名）。
   已改成「報告**有一頁專門談簽章當下的確認與「盲簽」**」，FAQ 第 4 題的「報告用一整節說明」同步改成
   「報告在個案教訓的其中一頁說明」。

### 兩處補回與對齊

8. **補上 CSSA 到底是什麼**（第 4 節第 2 段）。`corrections-crypto.md` must_add 7 說這是全篇唯一能讓讀者知道
   CSSA 實際內容的一段，研究紀錄的 `corrections_applied` 也聲稱「已寫進文章第 4 節」——**實際上沒有**，
   原稿只寫「資安自我評估（CSSA）」五個字。已依 `03.pdf` 註 10 補上：「註十寫 CSSA 是用與金融業資安指引一致的問題自評，
   讓業者看到自己在業界中的位置、藉此自主改善」，並把紀錄裡那句不實的 `corrections_applied` 改掉。
   同段把插入後斷掉的主語接回來（「方針也會檢討提高……」→「金融廳也會檢討提高……」，
   `03.pdf` 裡做這件事的主體是 the FSA）。
9. **摘要第四句與正文對齊**：「取組方針對監督指引只寫到檢討」→「只寫到檢討**與設法提高水準**」，
   否則 “endeavor to raise the levels … by revising the Guidelines for Supervision” 這半句在摘要裡消失，
   會讀成金融廳只說了「再想想」。`hero_label` 也從「簽章前那一步被動手腳」同步成
   **「簽章前那一步被竄改」**（9 單位，與改過的 title 一致；圖解標題、四格與 caption 原本就沒問題，沒有動）。

### 研究紀錄另外改的兩處（文章沒有寫這兩句，所以只動紀錄）

10. **`not_said` 第 7 項被推翻**。原本寫「研究報告與取組方針都沒有提到使用者資產被盜時的賠償、保險或求償機制」——
    報告第 20 頁把保險公司列為供應鏈上的參與者、第 112 頁把 `Insurance Coverage` 列在業者的 Accounting & Reporting
    控制項目下、第 124 頁的外包契約檢查項目有 “Company's right to be compensated in certain circumstances”，
    第 46、61 頁的個案敘述也出現賠償。能寫的只有「兩份文件都未見**存款保險或投資人保護制度**」
    （`deposit insurance`、`investor protection` 在兩份文件各 0 次）。已改寫成這個範圍。
11. **`not_said` 第 12 項收緊**。原本寫「這次公布沒有任何與價格、市值、交易量或報酬有關的**官方意見**」，
    把兩份說話者不同的文件混成一個主體。已改成「取組方針全文未見任何金額、幣價、市值、交易量或報酬數字」
    （`$`、`円`、`JPY` 各 0 次，四位數以上的數字只有年份、ISO/IEC 14888 與註腳網址），並寫明研究報告相反、
    但它不代表金融廳見解，依 `crypto.md` 一律不寫。

（第 12 處是第 2 點連動的三個檔內欄位改寫：`editorial_brief` 的個案處理界線、`must_not_write` 新增兩條
「不可點名十個個案」「不可寫成虛擬資產交換業者」、新增 3 條 `verified_facts` 承載新的第 3 節句子、
第 65 頁的頁首句與第 4 頁的研究目的。）

## 撰稿者自己點名的三個高風險句子：逐句結果

**第 3 節個案研究那句** —— 名單已刪（上面第 2 點）。編號「(1) 編到 (10)」對回**第 5 頁目次**無誤，
十個編號與名稱一字不差；類別改用報告自己的攻擊手法軸線，並保留「舉的例子是」這個非全清單的標記。
第 29 頁還有一句可以佐證取樣邏輯（“Incidents categorized as ‘Private key leakage’ often have unknown details …
therefore we **did not sample** from this category for further case study.”），但那是關於取樣的方法論，
寫進去會超字數，留給站主。

**第 4 節那個跨頁的日本事案句** —— **沒有把兩段的因果接錯。**
- 前半「日本曾實際發生使用者寄存的加密資產外流事案」：`03.pdf` 印刷第 1 頁末句接第 2 頁首句，
  “Japan … has requested service providers to take measures against the risks of an outflow of cryptoassets and
  properly manage system risks, **as a case of an outflow of cryptoassets deposited by users had actually occurred**.”
  文章只取了「曾發生」這個事實，沒有把它擴寫成別的因果；`corrections-crypto.md` must_fix 2 指定的正是這個寫法。
- 後半「在談重點監理的段落它另寫，鑑於過去發生過大規模的外流，金融廳一直密集監控……」：
  `03.pdf` 印刷第 3 頁「1. Intensive Monitoring of the Industry」首句 “**In light of the occurrence of the large-scale
  outflow** of cryptoassets in the past, the FSA **has intensively monitored** countermeasures against outflow risks and
  system risk management of individual cryptoasset exchange service providers…”——因與果都在同一句裡，對得起來。
- 兩半各自標明了出處段落（「方針也寫到」／「在談重點監理的段落它另寫」），沒有互相代換。
  文章也沒有寫 `03.pdf` 第 2 頁同句裡的 “Japan was the first nation to introduce regulations…”，符合「不可寫第一」。

**第 4 節那四個否定句** —— 逐句對 `03.pdf` 全文，三個成立、一個已改（上面第 4 點）：
- 「沒有罰則」：`penalt`／`sanction`／`fine`／`enforce`／`obligat`／`mandator`／`shall` 各 **0 次**。
- 「對監督指引只寫到檢討與設法提高水準，沒有列出修正條文也沒有寫生效日」：`amend`／`article`／`provision`／
  `effective date`／`2027`／`2028` 各 **0 次**；全文只有 “**revising** the Guidelines for Supervision”、
  “endeavor to **raise the levels**” 與 “**For example**, the FSA will **deliberate** on the following points”＋三個小圓點。
- 「三年內全部參加沒有寫起算基準日」：`three year` 只出現 **1 次**
  （“aiming to achieve the participation of all service providers within three years.”），沒有任何起算日，也沒有寫未參加的後果。
- 「TLPT 沒有寫是哪幾家」：成立；「結果是否公開」那半句已改成文件實際寫的分送方式。

## 查過而且正確的部分（沒有動）

- **五個日期全部復驗通過，四個寫進了文章與表格**：草案徵詢令和８年２月10日（火）至令和８年３月11日（水）與
  「計18件のコメント」（逐字）、取組方針訂定 2026-04-03（該頁頁首＋`03.pdf` 文首 April 3, 2026）、
  報告封面 June 30, 2026、公布與英文版補登 2026-07-23（日文政策頁「令和８年７月23日更新」＋
  20260403.html「令和８年７月23日、以下の英語版を公表しました。」後接別紙３、別紙４）。
  文章沒有把頁面更新日當成事件日，反而明寫「那是頁面的更新日，頁面再更新就會換一個日期」；
  PDF 的時間戳一個都沒有進文章。
- **「誰在說話」這條主軸站得住**：日文刊登頁的「※上記リサーチペーパーは、当庁の見解、意見等を示すものではありません。」
  在頁上出現三次（每個研究報告一次），報告第 2 頁的 “The contents of this report do not represent the official views of the
  Financial Services Agency.” 與 “any errors in this report are the sole responsibility of Deloitte Tohmatsu LLC, the
  contractor.” 都逐字存在，致謝也真的列了 “as well as officials from the Financial Services Agency”。
  全篇沒有一處把報告的分析寫成「金融廳指出」，也沒有寫成「金管會」。
- **「五個優先領域」的「五」是報告自己印的**：第 9 頁 “**five areas** were extracted and examined as priority areas”，
  FAQ 第 6 題的五項名稱與該頁逐項對得上，不是數出來的。
- **`03.pdf` 的專有名詞逐一對回**：From Program Year 2026 onward、within three years、
  within 2026 … TLPT targeting several service providers、Delta Wall（註 17 解釋 Delta 是自助／共助／公助的三位一體加上 Wall）、
  information sharing organizations, **such as** JPCrypto-ISAC（註 13 是官網）、
  本文只寫 the self-regulatory organization 而 JVCEA 只出現在**註 11** 的組織圖連結。文章的寫法與這個區分一致。
  CSSA 那句的 “or will **otherwise** have dialogues … **as required**” 與「或視需要與業者對話」對得上，限定詞沒有掉。
- **Clear Signing 三條全部對回第 65 頁**：“On **May 12, 2026**, the Ethereum Foundation, together with wallet developers,
  security firms, and other ecosystem participants, announced Clear Signing”、“ERC-7730, the core technology of Clear
  Signing, is a JSON-based descriptor standard”、“the information presented through Clear Signing **should not be treated
  as unconditionally safe**”。日期 2026-05-12 正確；文章沒有寫以太坊基金會公告本身的任何細節（那份公告不在 `sources[]`）。
- **資安界線**：文章停在報告的摘要與歸因層次。元件名（UI、API、CI/CD、未簽章交易產生邏輯、正式環境程式、
  雲端 IAM／KMS）都在，但**沒有任何一步一步的手法、時序、被竄改的檔案或端點，也沒有入侵指標**。
  報告第 34 頁那種逐分鐘的攻擊時序、第 40–42 頁的惡意程式細節一句都沒有進文章；
  FAQ 第 3 題還自己寫明「本文不寫更細的手法，也不寫入侵跡象」。
- **行情界線**：全文沒有幣價、漲跌幅、市值、交易量、ETF 資金流、殖利率、質押或空投報酬。
  報告轉引的外部統計（TRM、SlowMist、Chainalysis）一個數字都沒有出現。刪掉具名清單之後，
  全篇不再有任何交易所、錢包、託管商的名字，也沒有任何比較或推薦；剩下的專名只有主管機關、業界演習、
  自律機構、資訊共享機構、承包商，以及技術標準與其發表者。
- **「以下是編輯設計的例子，不是官方建議」那句仍在**（第 5 節第 3 段），而且它後面那個例子是一般性的提問，
  不涉及任何產品；「本文查核到的版本沒有給一般使用者的自保清單」這個否定句也有範圍——
  以 `users should` 查核，報告 **0 次**（第 65 頁那句的對象是 `signers`，文章正是這樣寫的）。
- **免責 callout 與 `crypto.md` 的樣板逐字相同**（tone、title、text 全等），含「不是投資建議」六個字，查核日 2026-09-17。
  文章另有一個「哪一句話出自哪一份文件」的提醒 callout，共兩個，符合幣圈規定。
- **摘要四句的每一個數字都在正文出現過**；FAQ 八題的答案都是純文字、沒有網址；全文沒有簡體字、列表、Markdown、emoji。
- **兩個站內連結的 text 與目標內容包的 zh-TW title 逐字相同**（幣圈索引與台灣《虛擬資產服務法》那篇），
  索引內容包在查核日已經存在，`check_article.py` 不再卡在那一條。
- **`sources[]` 之外的事實沒有外溢**：日文概要版、`01.pdf`、`02.pdf`、`04.pdf`、英文政策頁與英文新聞索引頁上的事實
  （日文書名、「国際共同研究」說法、意見徵詢截止 17 時 00 分、英文頁基準日 2023-03-17、日文概要版把個案重新編號）
  一句都沒有進文章。

## 留給站主的 5 件事

1. **報告本身的公布日只能靠推論**：`sources[]` 四條裡沒有一條印出「本報告於 2026-07-23 公布」——
   日文政策頁只有頁首的「令和８年７月23日更新」加上「2026 年第一項就是它」，而 20260403.html 印的 7 月 23 日
   是**取組方針英文版**的公布日。文章已經把依據寫在第 1 節。若要更硬的依據，英文新聞索引頁
   `/en/news/index.html` 的清單項目印著 `(July 23, 2026)`，但那要佔掉 `sources[]` 的第五個名額（現在 4 條已滿）。
2. **`hero.alt` 沒有查、也沒有改**（依 FACTCHECK.md 由協調者依實際畫面改寫）。`hero_label` 已同步成
   「簽章前那一步被竄改」，圖解標題、四格與 caption 未動。
3. **第 3 節的攻擊手法清單刻意少譯一項**：報告第 8 頁的 `such as` 清單還有 `rug pulls`，中文沒有穩定的對應詞，
   自己造詞就變成編輯的歸類，所以沒有寫。清單前有「舉的例子是」，不是全清單；要補請照報告的英文原詞。
4. **兩份官方文件對案例地域範圍互相矛盾，文章兩邊都沒寫**：報告第 4 頁寫 “representative **domestic and
   international** cyberattack cases”、`03.pdf` 印刷第 5 頁寫 “picked up representative cyberattacks that had occurred
   **in and outside Japan**”，但英文報告十個個案裡沒有日本的受害者。這個張力留在 `unverified_or_excluded`；
   要寫必須同時說明是哪一份文件這樣寫（`BRIEF.md` 型態 8）。
5. **字數只剩 41 字**（zh-TW 段落 2,959／3,000）。翻譯與逐語審稿若要補回任何條件或限制，
   得從別處刪等量的字，**不可以刪但書或限定詞來湊**。

## 自檢

```
OK crypto-news-jfsa-cybersecurity-20260723 zh-TW paragraphs 2959
```

## 結論

`ok`：文章側 104 條主張加紀錄側 59 條逐條核對後，12 處已改，四條來源今天全部讀到正文，47 條引文逐字複驗通過，
骨幹論述（誰在說話、四個日期、有一類外流不是金鑰被偷、光靠冷錢包不夠、沒有新增法定義務）沒有被推翻。
留給站主的 5 件事都不是擋刊的缺陷。
