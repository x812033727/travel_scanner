# 獨立查核：crypto-news-fdic-genius-act-20260410

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，**不改**）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，研究紀錄的
`verbatim_quote` 以壓空白後的連續字串逐條回比對，條號以「前言敘述＋小節標題＋條文修正指示」三處互相驗證。
**沒有使用任何 `sources[]` 以外的新網址**，也沒有猜任何識別碼；任何請求（UA、查詢字串、標頭）都沒有放入
email、姓名或其他個人資料。

檢查的主張：**96 條**（正文 14 段的每一句、摘要 4 句、FAQ 8 題的答句、表格 5 列與 caption、
圖解 caption、兩個 callout、title 與 description）。**改了 6 處**，研究紀錄另訂正 2 處、補 4 條事實，
另有 7 件留給站主。

## 重抓結果（四條都還在、都是正文）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| 91 FR 18534 提案全文 `/documents/full_text/text/2026/04/10/2026-06974.txt` | 200 | 352,322 | 是（GPO `<pre>` 全文，46 頁） | `<title>` 為 Volume 91 Issue 69；報頭 `[Proposed Rules] [Pages 18534-18579]`；結尾署名 4 月 8 日、`Filed 4-9-26; 8:45 am` |
| FDIC 新聞稿 | 200 | 66,698 | 是 | 頁面日期與 `Last Updated` 都是 April 7, 2026；`Board of Directors today approved`；`June 9` 0 次 |
| FDIC 聯邦公報刊登與公眾意見清單頁 | 200 | 181,821 | 是（真表格） | 04/10/26 那一列五個儲存格齊全；列到 09/15/26 |
| 91 FR 45274 申報表格公告 `/…/2026/07/20/2026-14589.txt` | 200 | 23,283 | 是 | Volume 91 Issue 137；`[OMB No. 3064-0225]`；`[Pages 45274-45277]` |

bytes 與研究紀錄寫的完全相同，只有新聞稿頁 66,697→66,698 的 1 byte 漂移（已知型態，內容相同）。
聯邦公報的正規 HTML 文件頁今天仍是 302 到 `unblock.federalregister.gov` 的約 10.6 KB `Request Access`
攔阻頁——紀錄把它留在 `unverified_or_excluded`、沒有放進 `sources[]`，這個處置正確。

**58 條 `verbatim_quote` 今天在重抓的檔案上 100% 命中**（原 54 條全中，查核另補 4 條）。
沒有任何一條跨越 `[[Page NNNNN]]` 分頁標記或 `\NN\` 註腳標記，也沒有自製分隔符、省略號或被「訂正」的字元；
清單頁那一列的引文保留了頁面上的 en dash。

## 撰稿者自己點名的三個高風險句：全部成立

1. **擬議 12 CFR 330.11(a)(3) 與方向** — 成立，而且有三處互相佐證：前言小節標題（`Description of the
   Proposed Rule (Proposed Sec. 330.11(a)(3))`）、前言敘述（`…would add a new paragraph (3) to 12 CFR
   330.11(a).`）、條文修正指示（`Amend Sec. 330.11(a) by adding paragraph (3)…`，接著是 `Notwithstanding
   any other provision of this part…are deposits of the permitted payment stablecoin issuer's and insured
   as corporate deposits…`，來源自己的 `issuer's` 排印照留）。方向是「保給發行人（法人存款）、**不**以穿透
   方式保給持有人」，文章沒有寫反。加總與上限也對：330.11(a)(1) 那一句印著 `insured up to the SMDIA,
   currently $250,000, in the aggregate`，另一句印 `In other words, the SMDIA is $250,000 per depositor,
   per IDI, for deposits held in each ownership category.`（逐字存在、只出現一次），`currently $250,000`
   全文兩次。**擬議 12 CFR 330.3(k)** 同樣三處一致，方向相反（記帳技術不影響是不是存款）。
   查核另補了一條事實（前言那一句）進研究紀錄，讓這個條號有第二個佐證。
2. **建立在活清單上的否定句** — 今天重跑仍成立。該頁印的是 **en dash** `RIN 3064–AG19`（ASCII 連字號在
   該頁 0 次，但該頁本身混用兩種寫法，例如另一列印的是 `3064-AG28`）；以 `AG19` 子字串比對**全頁只出現
   1 次**，就在 04/10/26 那一列，該列印著 `Notice of proposed rulemaking`、`Comment Period End:`
   `June 9, 2026`、`91 FR 18534`。全頁唯一的 `Final rule` 屬於 RIN 3064–AG12（聲譽風險案），
   沒有同文號的最終規則列。這一頁列到 **09/15/26**，所以它是活的、涵蓋查核日，否定句撐得住。
   （順帶確認：該頁有一個 RIN 3064–AG30 出現兩次，證明同一文號真的會在這一頁多出一列，
   FAQ 第 8 題「同一個文號會再出現一列」的說法有頁面行為支撐。）
3. **生效日是來源自己印的** — 成立。那一句在提案的**註 5**，逐字含兩個分支與 `if earlier`，
   並註 `See 12 U.S.C. 5901 note`。文章歸因給法律、並明寫這份草案自己沒有生效日；查核另確認全文
   `2027` 只出現 1 次（即該註）、`Effective date`／`EFFECTIVE DATE` 0 次、`DATES` 欄只有意見截止日，
   唯一的 `effective date` 出現在 RCDRIA 那一段的一般性義務，不是本案的生效日。

## 改掉的 6 處

1. **第 2 節第 1 段補一句射程（唯一的事實性更正）。** 原稿把「管到誰」寫成只有三類：FDIC 監理的存款機構、
   它們獲准發行的穩定幣子公司、FDIC 監理的保管業者。來源在影響範圍那一節寫的是
   `The entities that fall under the direct scope of the proposed rule are all FDIC-supervised PPSIs,
   all FDIC-supervised PPSIs and IDIs that provide … custodial and safekeeping services, …, and **all IDIs
   maintaining tokenized deposits or deposits held as reserves backing a payment stablecoin.**`
   前言另有兩處寫 `provide clarity to all IDIs with respect to deposit insurance coverage…`，
   而擬議 330.11(a)(3) 與 330.3(k) 的條文主語都是 `an insured depository institution`，沒有限定於受 FDIC
   監理者。**這是把來源的範圍收窄（BRIEF 型態 3），而且收窄的正好是本文的骨幹段落**——存款保險那一半
   其實及於任何受保存款機構裡的準備金存款。已補上：「存款保險那一段的射程更寬：文件在影響範圍那一節，
   把所有維持代幣化存款或穩定幣準備金存款的受保存款機構都列為直接適用對象。」
2. **摘要第一句同步補上**「存款保險那一段還及於所有維持這類存款的受保存款機構」，
   否則摘要會與改後的正文不一致（摘要只能重述正文）。
3. **FAQ 第 6 題（台灣）同步補上**同一個範圍。這一句同時讓「不及於台灣」更清楚，
   因為「受保存款機構」的定義本身就把非美國機構排除在外。
4. **第 3 節第 2 段補「依擬議條文，」。** 原稿的「不論那是準備金還是營運開銷，發行人在同一家機構的存款
   都會加總」來自 `Under the proposed rule, all deposits maintained by a PPSI at an IDI would be added
   together…`，是一個操作性句子卻沒有帶提案標記，會被讀成現行規定
   （`corrections-crypto.md` 跨篇型態 6：把提案寫成已生效的規則）。
5. **第 5 節第 2 段的編輯情境加射程限定。** 原稿以「透過某個跨境服務拿到一筆美元穩定幣」起頭，
   緊接著就寫「照這份草案的提議，受保的是發行人存在銀行裡的那筆準備金」——**這會被讀成任何一枚美元
   穩定幣的準備金都有美國存款保險**，跨出了文件的範圍（同一篇的 FAQ 第 6 題才剛說文件沒有任何跨境規定）。
   已改成「照這份草案的提議，在它管得到的範圍內，受保的是……」。
6. **FAQ 第 3 題兩處。** 「發行人在同一家受保機構的法人存款會全部加總後適用這個上限」前加「依擬議條文，」；
   末句「持有人**不是**那家銀行的存款人，也不會各自獲得一份上限」改成「依這份草案的提議，持有人不會**被當成**
   那家銀行的**受保存款人**，也不會各自獲得一份上限」。原句是無限定的絕對句，而文件講的是
   「不以穿透方式把持有人當成受保存款人」，不是「持有人在那家銀行沒有任何存款關係」。

## 研究紀錄另外改的 2 處與補的 4 條

- **`sourcing_notes` 與 `corrections_applied` 的 must_add 3 兩處都寫「55 條」引文，實際只有 54 條。**
  已訂正並註明那是撰稿者的清點錯誤（BRIEF 型態 9）。
- 補 4 條 `verified_facts`（都在 `sources[0]`、引文連續且唯一）：直接適用對象三類那一句；
  前言的 `provide clarity to all IDIs` 那一句；前言的 `…would add a new paragraph (3) to 12 CFR 330.11(a).`；
  ADDRESSES 欄印出 `FDIC Website: https://www.fdic.gov/federal-register-publications` 那一行
  ——最後這條是讓 FAQ 第 8 題「那一頁也是 ADDRESSES 的遞送管道之一」可追溯，原紀錄只引了 ADDRESSES 的起首句。

## 協調者點名的數字與條次：逐條回到原句，全部正確

- **四個主管機關**：註 4 用的是 `are`（不是 `include`），列 FDIC、OCC、FRB、NCUA 並引 12 U.S.C. 5901(25)。
  寫「四個」成立。（同批 NCUA 那份文件用的是 `which include`，兩篇不可互抄。）
- **零家的基準時點**：經濟分析段先寫這份分析用的是 2025 年 9 月 30 日季末的資料，同一句接著
  `…insures 4,388 IDIs, supervises [[Page 18562]] 2,778 of these IDIs,\51\ and supervises zero PPSIs.`
  ——4,388 與 2,778 確實被分頁標記與註腳切開，文章只寫「零家」的取捨正確。
- **40% 集中度**：擬議 350.4(f) 條文含 `on each business day`、`any one eligible financial institution`、
  `regardless of instrument type`，分母是 `its reserve assets`。文章的「每個營業日」「任一合格金融機構」
  「準備資產的 40%」三個要素都對。（前言另加了 `across all brands of payment stablecoins issued by the
  PPSI`，那是條文之外的補充；沒寫進文章不構成誤述。FDIC 在第 47 題就這個百分比徵詢意見。）
- **重大贖回請求**：定義段與擬議條文第 (24) 款兩處都是 `aggregate redemption requests exceed 10 percent …
  within a single 24-hour period`。文章寫的「單一 24 小時內合計超過在外發行額的 10%」對；第 12 題就
  10% 與 24 小時兩者徵詢意見。
- **不遲於兩個營業日**：擬議 350.5(b)(1)，前言明寫兩個營業日是**上限**、發行人可以更短，並自陳
  `the market may expect redemptions to occur far more quickly than two business days`、就天數徵詢意見
  （第 71 題）。三項文章都寫了。
- **一枚以上與篩查／開戶**：擬議 350.5(a)(5) 條文尾端確實是 `…shall redeem any number greater than or
  equal to one payment stablecoin, subject to appropriate screening and onboarding.`
  文章正文與 FAQ 第 7 題兩處都寫了這個限定；表格的「不得高於一枚」對應前言的
  `the minimum number the PPSI will redeem may not be greater than one payment stablecoin`。
- **至少提前七個日曆日**：擬議條文寫的是「費用有**變動**就要至少提前七個日曆日通知，**但調降除外**」，
  前言寫的是 `any increases in the fees`。文章寫「調漲須至少提前七個日曆日通知」，
  兩版都撐得住，也沒有把調降也寫成要通知。
- **月報須經註冊會計師事務所查核**：擬議 350.4(h)(1) 要求上一個月月末報告揭露的資訊
  `examined by a registered public accounting firm which will issue a written report of findings to the
  PPSI's audit committee, or board of directors if there is no audit committee`。
  公布時點（每月最後一日收盤前）與所報時點（上一個月最後一日收盤）文章沒有寫混。
- **第 144／125／13 題**：以詞界比對，編號問題是 Question 1 至 144、**無缺號、最大為 144**，
  第 144 題之後接的是 `E. Executive Orders 12866 and 14192`，所以「一路編到第 144 題」不是自己清點的數字。
  第 125 題問的是這個擬議處理是否妥當、是不是對 GENIUS Act 與 FDI Act 最好的解讀（與文章敘述一致）；
  第 13 題問「持有人」是否應由 FDIC 定義，並列出「實質受益所有人」與「以數位錢包的持有或私鑰的控制認定」
  兩個選項（與 FAQ 第 5 題一致）。
- **OMB 3064-0225 與 2026-09-18**：7 月 20 日那份公告的 `[OMB No. 3064-0225]`、
  `DATES: Comments must be submitted on or before September 18, 2026.`、
  `weekly and quarterly reporting forms`、`(GENIUS Act or the Act) was enacted on July 18, 2025.`、
  `On April 10, 2026, the FDIC published the proposal that would add Part 350…` 全部對得上。
  `July 18, 2025` 在四月那份文件 **0 次**——文章明寫制定日只在 7 月那份公告，正確。
- **`currently $250,000` 與 `In other words, the SMDIA is …`**：兩串都逐字存在，前者全文兩次、
  後者一次。文章保留了 `currently` 這個限定詞（不是把 25 萬寫成固定值）。

## 查過而且正確、沒有動的部分

- **界線**：全文沒有幣價、市值、交易量、資金流或報酬；唯一的數字都是法規數字。沒有點名任何穩定幣、
  交易所、錢包或發行方（文件本身也沒有點名任何一個），「推薦」與「漲跌」兩個詞只出現在否定句裡。
  免責 callout 與 `crypto.md` 樣板**逐字相同**（tone、title、text 全等，含「不是投資建議」六個字），
  查核日 2026-09-17；本文另有一個提醒 callout，共兩個，符合幣圈規定。
- **界線的另一半（最容易被誤會的方向）**：文章沒有任何一句會被讀成「穩定幣持有人受美國存款保險」。
  反方向也沒有寫過頭：第 4 節末段與 FAQ 第 5 題都照 `must_fix 7` 的改寫寫成「沒有存款保險式的還款保證，
  **但**持有人債權在第 11 條清理程序中優先於非穩定幣債權人」，並帶上第 13 題「持有人」尚未定義。
- **提案字樣**：表格 5 列的狀態欄全是「提案」、caption 寫「表中每一項都還是提案」、圖解 caption 寫
  「四格都是擬議內容」，正文與 FAQ 的每個操作性句子在本次改完後都帶「提案／擬議／草案」。
  沒有任何一句寫這份規則已生效、已施行，或有東西從 2026-04-10 開始。
- **否定句都有範圍**：「以這份提案全文查核到 2026 年 9 月 17 日，未見任何關於非美國使用者、跨境提供或
  台灣業者的規定」——查核另跑 Taiwan、cross-border、non-U.S.、outside the United States、abroad、
  offshore、extraterritorial **各 0 次**，`foreign` 的 15 次逐條讀過，全部是外國銀行的受保州立分行、
  外國央行發行的貨幣、IDI 的境外分行與代理行、外國恐怖組織，**沒有一處在講境外使用者**。
  句型一律是「以 X 查核到 2026-09-17 未見」，沒有寫成「官方沒有」「從未」「第一份」。
- **日期沒有混用**：理事會通過 2026-04-07、署名 04-08、送存 04-09、刊登 04-10。文章只用 04-07 與 04-10
  並各自標明身分，callout 把「通過、刊登、生效是三件事」講開。新聞稿頁的 `Last Updated: April 7, 2026`
  沒有被當成事件日，該頁 `June 9` 0 次、意見截止日只取自聯邦公報原文。
- **「第二件規則制定」沒有寫進文章**（`must_fix 6` 的風險源），所以不存在「第二件也是最新的」問題。
- **`checked_on` 五處一致**（四條 source、第 2 段、表格 caption、免責 callout）且與研究紀錄相同，
  撰稿者讀到的內容與今天重抓的一致，因此**沒有改動**。
- **兩條站內 link** 的 `text` 與目標內容包的 zh-TW title 逐字相同（幣圈索引與台灣 VASP 那篇都已存在）。
- 全文無簡體字；FAQ 答案都是純文字、沒有網址；摘要的每個數字都在正文出現過。

## 留給站主的 7 件事

1. **事件日仍未定案**：`corrections-crypto.md` 認為依 `BRIEF.md` 的「slug 尾碼＝事件日」應為 20260407
   （理事會通過日），`WRITER.md` 第 2 節則要四篇美國聯邦規則一致採刊登日。本篇維持 2026-04-10，
   文章兩個日期都明寫。查核代理不代站主定案；若改採 04-07，slug、`news_date`、`display_order`
   與第 1 段、callout 的敘述要一起改。
2. **生效日的規格衝突維持原判斷**：`WRITER.md` 要「寫公式不寫日期」，但來源的註 5 自己印了日期與兩個分支，
   照 BRIEF 第 9 條「來源自己印出日期就照印的寫」處理。若站主要改成純公式，注意「制定日起 18 個月」
   這個算法在本篇四條來源裡**都沒有印**，不能寫。
3. **`sources[2]` 是活清單**：出刊當天要再抓一次。若屆時出現同文號的最終規則列，摘要第 4 句、
   第 1 節第 3 段、FAQ 第 1 題與第 1 個 callout **四處**的否定句都要改寫。
   搜尋時用 `AG19` 或 en dash 的 `3064–AG19`。
4. **RIN 的連字號**：文章提到文號時用的是聯邦公報原文的 ASCII 連字號 `3064-AG19`，而 FDIC 清單頁那一列
   印的是 en dash。兩者指同一個文號，查核已用兩種寫法各驗一次；若希望讀者能直接在該頁 Ctrl+F 找到，
   第 5 節最後一段可以改成只叫讀者找 2026 年 4 月 10 日那一列。
5. **第 1 段的「三天前的 2026 年 4 月 7 日」是兩個已刊日期之間的日差**（編輯換算，數值正確）。
   若要完全避免任何換算，刪掉「三天前的」四個字即可，句意不變。查核代理沒有代為刪。
6. **2026-09-18 是 7 月那份公告的意見截止日，也就是查核日的隔天。** 文章只寫「印的截止日是
   2026 年 9 月 18 日」，沒有寫它現在開著或關著；這個寫法在 9 月 18 日之後仍成立，
   翻譯與逐語審稿**不要**改寫成「目前仍可提交意見」。
7. **字數只剩 27 字**：zh-TW 段落改後為 2,973／3,000。之後若要補內容
   （例如 `unverified_or_excluded` 裡「FDIC 估計最初幾年 5 到 30 家」那條），必須從別處刪等量的字，
   **不可以刪但書或限定詞來湊字數**。

## 自檢

```
OK crypto-news-fdic-genius-act-20260410 zh-TW paragraphs 2973
```

## 結論

`ok`：96 條主張逐條回到一手原文核對，改了 6 處（1 處事實性的範圍更正、5 處補提案標記或收緊限定語），
研究紀錄訂正 2 處清點錯誤、補 4 條可追溯的事實。骨幹論述「準備金存款依法人存款規則保給發行人、
不穿透到持有人；代幣化存款相反」查證後成立，未動；三個高風險句與協調者點名的每一個數字與條次全部對得上原句。
留給站主的 7 件事都不是錯誤，是編務決定與活資料的定稿日重跑。

## 翻譯階段回頭抓到的一處（協調者更正，2026-09-17）

翻譯代理回報第 2 節那句「擬議的 subpart B 適用於受 FDIC 監理、提供穩定幣準備金、擔保品穩定幣或發行私鑰保管的業者」
讀起來像是「提供準備金的業者」，英譯也照字面譯成了 `provide payment stablecoin reserves`。
協調者重抓 91 FR 18534 全文核對，擬議 350.100 的原句是
`engaged in the business of providing custodial or safekeeping services for payment stablecoin reserves,
payment stablecoins used as collateral, or private keys used to issue payment stablecoins`——
中心語是「保管服務」，三樣東西都是被保管的標的。五個語系都已改成「以替穩定幣準備金、作為擔保品的穩定幣或發行用私鑰
提供保管服務為業者」的意思；`check_article.py --full` 重跑只剩連結標題那一條（等台灣篇的 zh-CN 併入）。
第一輪查核沒有抓到這一句，因為中文的歧義要到翻成別的語言才顯形。
