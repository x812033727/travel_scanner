# 獨立查核：crypto-news-fca-p2p-crypto-crackdown-20260917

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，五處一致，不改）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
20 條 `verbatim_quote` 逐條以**原始 HTML** 搜尋驗證連續性，9 月與 4 月兩篇新聞稿逐段對讀。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，任何請求都沒有帶入 email 或個人資料。

檢查的主張：**109 條**（正文 17 段、summary 4 句、FAQ 6 題的答句、兩個 callout、
表格 15 格與 caption、圖解 caption 與研究紀錄 `diagram` 四格、title、description）。
改了 **17 處**（其中 15 處是事實或範圍），另有 3 件留給站主。`hero.alt` 依規格未查未改。

## 重抓結果（三條 sources 都讀到正文）

| source | HTTP | bytes | 驗到的東西 |
| --- | --- | --- | --- |
| FCA 9 月新聞稿 `fca-and-partners-continues-crackdown-illegal-crypto-trading` | 200 | 175,753 | `<title>` 正確；First published／Last updated 皆 17/09/2026（`<time datetime="2026-09-17T10:31:33Z">`）；無 See all updates／Page updates 區塊；Notes to editors 的 10 September 2026、MLRs 2017、until October 2027；3 premises、cease and desist；兩段具名談話 |
| FCA 4 月新聞稿 `fca-leads-first-crackdown-illegal-crypto-trading` | 200 | 176,506 | First published 22/04/2026（`2026-04-22T05:10:53Z`）、Last updated 18/05/2026、修訂紀錄 `2026-05-18T14:05:33+01:00` 與頁尾「18/05/2026: Information changed」；5 月 18 日更新說明全句；8 premises、SWROCU；In June 2024 那句 |
| FCA Firm Checker 說明頁 | 200 | 85,989 | `<title>` 為 “FCA Firm Checker”；canonical `/consumers/fca-firm-checker`；authorised／permission 兩點、almost all financial firms、Information you won't find on this tool、FSCS／Financial Ombudsman 那段、won't remove all risk 那句 |

兩個取得面的發現：

1. `sources[2]` 原本記的是 `/consumers/check-if-firm-fca-authorised`，該路徑今天回 **301** 轉到
   `/consumers/fca-firm-checker`（也是頁面自己的 canonical）。依 BRIEF 型態 6／7「記最後落地的 URL」，
   已把內容包與研究紀錄的網址、以及兩條 `verified_facts` 的 `url` 改成落地網址。
   兩篇新聞稿內文連的仍是舊路徑，這一點寫進了 `sourcing_notes`。
2. 位元組數不是常數：4 月那篇三次抓取分別是 176,506／176,507／176,508 bytes。
   研究紀錄原本把 1 byte 之差判讀成「量測方式差異」並據此下結論，已改成「不可拿位元組數判斷內容變動」，
   三頁一律改記概數。

## 改掉的 17 處

1. **把「新聞稿沒有提到逮捕、起訴或裁罰」限縮成「沒有寫這次行動有人被逮捕、起訴或裁罰」**
   （第一段、第 1 節第 2 段、提醒 callout、FAQ 第 1 題、第 4 節第 1 段，共 5 處）。
   9 月新聞稿自己寫著 `The FCA has a track record of tackling illegal cryptoasset activity, including prosecuting the operator of an unlawful crypto ATM network and supporting the arrest of two individuals…`，
   4 月那篇也寫了 2024 年 6 月的逮捕。原句把「這次行動沒寫」放大成「整篇沒提」，
   正是 BRIEF 型態 2 與型態 6 的組合。FAQ 第 1 題另外補上一句說明那是別的案子。
2. **FAQ 第 1 題答句開頭「沒有。」→「新聞稿沒有寫。」**
   來源沒有說沒有人被捕，只是沒有寫；把「來源沒說」寫成「來源說沒有」是 BRIEF 型態 2。
3. **合作單位：HMRC 兩次都在，換掉的是警方單位**（第 4 節第 1 段、FAQ 第 4 題、summary 第 3 句）。
   9 月原文是 `Working with HM Revenue & Customs (HMRC) and the Metropolitan Police Service`，
   4 月是 `HMRC and the South West Regional Organised Crime Unit (SWROCU)`。
   原句「9 月這次合作單位換成倫敦警察廳」會被讀成 HMRC 退出，已改成「HMRC 仍在，警方單位換成倫敦警察廳」。
4. **summary 第 3 句「這是 FCA 今年第 2 次採取這類行動」→「FCA 表示這次行動接續 4 月那次」**。
   來源只印 4 月那篇是 `first crackdown`、9 月這篇是 `This operation follows…`／`further action`，
   沒有印出次數；而且 9 月那句用的是複數 `further operations`。次數是文章自己算的（BRIEF 型態 9），
   而且 summary 不得出現正文沒說的數字。
5. **第 4 節第 2 段的 `including` 清單拆成兩篇分寫**。9 月那篇的 `including` 同時涵蓋 ATM 起訴與
   `supporting the arrest of two individuals`（沒有日期、沒有合作單位）；4 月那篇的 `including` 只涵蓋
   ATM 起訴，逮捕 2 人是**下一句獨立句子**，並寫明 `In June 2024, the FCA worked with the Metropolitan Police Service`。
   原句把兩篇措辭接成一句、漏掉「6 月」，並把 9 月的「協助逮捕」寫成「合作逮捕」——BRIEF 型態 1 的接句。
6. **「兩次都只發出停止並終止通知書」刪掉「只」**（第 4 節第 1 段、FAQ 第 4 題）。
   4 月那篇另外寫了現場檢查（`on-site inspections`）與證據支援偵查，「只」不成立。
7. **summary 第 4 句「FCA 也提醒這個工具無法保證消除所有風險」→「使用已授權業者不會消除所有風險」**。
   來源那句的主詞是**業者**不是工具：`While it won't remove all risk, using an authorised firm with the correct permissions will greatly reduce your risk of harm.`
   正文第 5 節本來就寫對，是 summary 把主詞換掉了。
8. **三處「FCA 給消費者的建議」加上「這篇／9 月這篇新聞稿」的範圍**
   （summary 第 4 句、第 5 節第 1 段、FAQ 第 6 題）。
   4 月新聞稿另有一句給消費者的話（只與已登記業者往來、記得加密資產是高風險投資），
   寫成 FCA 的全稱建議會被同在 `sources[]` 的那一篇推翻。
9. **表格第 1 列第 1 欄「個人之間偶爾換一次加密資產」→「以個人身分進行的點對點交易」**。
   FCA 的但書是 `on a personal basis`，不是頻率；文章自己第 3 節也寫了「新聞稿沒有定義頻率、金額或是否對外招攬」，
   表格卻把頻率寫成判準。
10. **表格第 5 列第 2 欄「沒有法定強制工具」→「業者幾乎都須經授權或登記」**。
    前者三份來源都沒有依據；後者是 Firm Checker 頁原文 `In the UK, almost all financial firms must be authorised or registered by us`。
11. **表格第 5 列第 3 欄「FCA 建議用 Firm Checker，但不保證消除全部風險」→「建議用 Firm Checker，另有查不到的事項」**。
    同一個工具／業者主詞混用；改成該頁真的有的小標 `Information you won't find on this tool`。
12. **表格第 3 列第 3 欄「可能收到停止並終止通知書」→「這次 3 處都收到通知書」**。
    該欄欄名是「FCA 新聞稿的說法」，新聞稿寫的是這次 3 處，不是一般化的可能性。
13. **第 3 節第 1 段結尾的法律推論改成可查證的比對**。
    原句「兩篇新聞稿引用的是同一套登記義務，範圍不會因為只有一篇寫了但書就縮小」改成
    「兩篇新聞稿寫登記義務的那兩句話逐字相同，都限定在『以營業方式』從事的人」。
    實測：`Peer-to-peer trading is when individuals buy and sell crypto directly with each other. Anyone doing this by way of business in the UK requires appropriate registration.`
    在兩篇裡逐字相同，而 `personal basis` 只出現在 4 月那篇。
14. **第 5 節第 1 段「是否經 FCA 授權登記」→「是否經 FCA 授權」**。
    Firm Checker 頁那兩點寫的是 `is authorised by us`／`has our permission to provide the services you want`，
    「登記」是同頁另一句（almost all…）的用字，混在一起會讓讀者以為工具的說明本身寫了登記。
15. **第 5 節第 3 段刪掉「本次沒有查到台灣主管機關在同一時間有相關公告」**，改成「本文只寫英國的情況」。
    那個否定句靠的是**不在 `sources[]`** 的金管會搜尋，依 BRIEF 型態 7 不能當文章的依據；
    「不推測台灣是否會採取類似行動」與「要對照台灣需另找一手來源」兩句留著。
16. **description「查緝以營業方式經營卻未登記的點對點加密資產交易」→「查緝涉嫌非法的點對點加密資產交易」**。
    新聞稿對這 3 處用的是 `suspected`，「未登記」是 FCA 的法律理由、不是已認定的事實；
    「只及於以營業方式經營者」的重點在 description 後半句已經寫了。description 由 171 字降為 164 字。
17. **`sources[2]` 換成落地網址並改 title**（見上一節）。研究紀錄另修三處：
    兩條把渲染後的「First published: 17/09/2026」當 `verbatim_quote` 的欄位（原始 HTML 裡被標籤切開，
    不是連續字串）改記成可原樣搜尋的 `<time datetime="…">`；`including` 那條 fact 的敘述改成分篇說明。
    圖解第四格「登記家數0」→「點對點登記0」——英國並不是所有加密資產業者登記家數為零，
    零的只有點對點這一類（`cjk_units` 12.4 ≤ 15）。

## 查過而且正確的部分（沒有動）

- **兩個日期**：Notes to editors 逐字 `The action took place on 10 September 2026.`；頁面 First published／Last updated 皆 17/09/2026。
  slug 尾碼、`news_date`、正文第一段三者一致，全篇沒有把兩個日期混成一天。9/10 與 9/17 相差 7 天是兩個已印出的日期之差，且同句寫出兩個日期，不是無法回推的算術。
- **5 月 18 日的但書逐字無誤**：`On 18 May 2026 we updated paragraph two to say that where the activity is carried out by way of business in the UK, it requires appropriate registration. Without registration, that activity is illegal. Peer-to-peer transactions carried out on a personal basis do not require FCA registration.`
  正文第 3 節的中譯沒有增減任何限定詞，`personal basis` 確實只在 4 月那篇、9 月那篇沒有重複（`grep` 0 次）。
- **「登記家數為零」只引用新聞稿當下的陳述**：`There are currently no FCA registered peer-to-peer crypto businesses operating in the UK.` 在兩篇裡逐字相同。
  文章第 2 節第 3 段明寫不自行到登記名冊上清點，符合 BRIEF 型態 8；本代理也沒有去查活的名冊。
- **`until October 2027` 只掛在 9 月那篇**：4 月那篇同一句是 `…except for anti-money laundering and financial promotion.`，**沒有**時間條件。
  文章把 2027 年 10 月只歸給 9 月那篇，沒有混用；`largely`（大致上）與兩項例外都留著。
- **MLRs 2017** 是兩次行動共同法源（兩篇 Notes to editors 同一句），條文全名與括號英文正確。
- **20 條 `verbatim_quote` 有 18 條在原始 HTML 就是連續字串**（含 `FCA’s` 的 U+2019 彎引號、`It's`／`won't` 的 ASCII 直引號）；
  另 2 條已依上面第 17 點改掉。`sources[]` 三條網址全部出現在 `verified_facts` 裡。
- **免責 callout** 的 title 與 text 與 `crypto.md` 樣板**逐字相同**，「不是投資建議」六個字在內，查核日 2026-09-18；
  `checked_on` 在內容包三條 source、研究紀錄、第二段、表格 caption、免責 callout **五處一致**。
- **界線**：全文沒有幣價、漲跌幅、市值、交易量、資金流、殖利率或報酬；
  「漲跌幅」「買賣時機」只出現在制式免責句裡。沒有點名或比較任何交易所、錢包、兌幣管道，
  沒有「怎麼安全地面交」的操作指南，生活情境已標明是編輯設計的例子。沒有簡體字。
  唯一帶「投資」字樣的是 FCA 自己的 `Crypto is a high-risk investment`，已歸因給新聞稿。
- **缺「草案」字樣的句子：沒有**。本篇寫的是已生效的 MLRs 2017 與已發生的執法行動，
  2027 年 10 月只以「FCA 說明的現況會持續到那時」出現，沒有把任何未生效的制度寫成現行規則。
- **人名**：正文只用職稱（FCA 執法與市場監理執行董事、倫敦警察廳一名警官）引述，依指派訊息維持不動；
  兩段談話都寫成「表示」。
- 第一個結尾連結的 text 與 DELTA-4-5 指定的幣圈索引標題逐字相同。

## 留給站主的 3 件事

1. **`check_article.py` 仍留一條 FAIL**：第二個結尾連結的 text「英國 FCA 加密資產監理範圍最終指引」
   與同批 `crypto-news-fca-perimeter-guidance-20260916` 的 zh-TW title 尚未對齊。
   依指派訊息由協調者事後對齊，查核代理未動。這是本次唯一的 FAIL，與 baseline 相同。
2. **9 月那篇新聞稿到 2026-09-18 為止沒有修訂紀錄區塊**。FCA 會回頭修訂已發布的新聞稿——
   4 月那篇就是在 5 月 18 日才被補上「以個人身分進行的點對點交易不需要登記」這句關鍵但書。
   出刊前值得再看一次該頁的 Last updated；只讀最初版本會把整件事寫錯。
3. **段落字數由 2,920 增為 2,964**（上限 3,000）。翻譯或審稿若要再加句子，
   必須從別處刪等量的字，且不得刪任何限定詞或但書。

## 結論

`needs_second_round`。內容包改了 17 處、其中 15 處動到事實或範圍，超過規格的十處門檻。
但要說清楚：**骨幹四件事全部查核無誤**——兩個日期分得清楚、「以營業方式」與「個人身分」的界線正確、
點對點登記家數為零只引用新聞稿當下的陳述、Firm Checker 的界線寫得比來源還保守。
被改掉的大多是同一個毛病在不同區塊重複出現（否定句超出「這一頁沒有寫」的範圍），
以及 summary 與表格這兩個壓縮區塊在壓縮時掉了主詞或限定語。
第二輪可以只覆核本次的 17 處改動與翻譯，不需要重讀全部來源。

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 本來就一致且正確，未動）。
覆核 **98 條**，又改 **8 處**（內容包 8 處，研究紀錄另修 2 處敘述並加 `factcheck.second_round`）。
三條 sources 全部自行重抓、讀 body，任何請求都沒有帶入 email 或個人資料。

### 重抓結果

| source | HTTP | bytes | 本輪另外驗到的事 |
| --- | --- | --- | --- |
| 9 月新聞稿 | 200 | 175,753 | `inspection` 出現 **0 次**；`arrest`／`prosecut` 各 1 次，都在 `The FCA has a track record…` 那一句裡 |
| 4 月新聞稿 | 200 | 176,508 | `Evidence obtained during the on-site inspections…` 在；Notes to editors 那句**沒有** `until October 2027` |
| Firm Checker 說明頁 | 200 | 85,989 | 兩個項目符號 `is authorised by us`／`has our permission to provide the services you want`；`In the UK, almost all **financial** firms must be authorised or registered by us.` |

舊路徑 `/consumers/check-if-firm-fca-authorised` 今天仍回 **301** 轉到 `/consumers/fca-firm-checker`，第一輪換的落地網址正確。

### 20 條 `verbatim_quote`：全部通過，但第一輪的說法要更正

程式對**原始 HTML** 與**渲染後正文**各做一次連續字串比對：

- 18 條在原始 HTML 就是連續字串；
- 2 條 `<time datetime="…">` 只在原始 HTML（那是標籤，不是正文）；
- 2 條 `Working with HM Revenue & Customs…` 只在渲染後正文——原始 HTML 把 `&` 寫成 `&amp;`。

沒有一條需要換片段或刪事實，也沒有一條是把不同段落拼在一起。
但第一輪報告與研究紀錄寫的「另 2 條是渲染後的 First published 字串」**指錯了是哪兩條**（數字對、內容不對），研究紀錄該條已改寫。

### 又改掉的 8 處

1. **第 2 節第 2 段「在 FCA 的登記名冊上，目前找不到任何一家登記在案」→「依新聞稿當下的說法，以營業方式經營這類交易的業者沒有一家登記在案」**。
   原句把 FCA 當下的陳述改寫成對**活名冊**的現在式斷言，和下一段自己寫的「本文也不去 FCA 的登記名冊上自己數」直接矛盾（BRIEF 型態 8）。
   這一句同時是本輪騰出字數的來源。
2. **第 4 節第 1 段「兩次的處理方式相同：都發出停止並終止通知書」→「兩次都發出停止並終止通知書，4 月那次另有現場檢查」**。
   第一輪為了同一個理由刪掉了「只」，卻把「處理方式相同」留著——4 月那篇寫了
   `Evidence obtained during the on-site inspections is supporting a number of ongoing criminal investigations.`，而 `inspection` 在 9 月那篇是 0 次。
3. **FAQ 第 4 題結尾「處理方式相同」同上改掉。**
4. **第 4 節第 2 段「起訴一名非法經營加密資產 ATM 網路者」→「起訴非法加密資產 ATM 網路的經營者」**。
   該句寫的是 **9 月那篇**的 `including` 清單，9 月原文是 `prosecuting the operator of an unlawful crypto ATM network`；
   「一名」是 **4 月**那篇 `an individual` 的用字，第一輪拆句時把它留在了 9 月那篇名下。
5. **第 4 節第 3 段「是 MLRs 2017 已經生效多年」→「是 MLRs 2017 的登記規定已經生效」**。
   3 份來源都沒有印 MLRs 2017 的施行日，「多年」是從規則名稱裡的年份自己算的（BRIEF 型態 5）。
6. **表格第 5 列第 2 欄「業者幾乎都須經授權或登記」→「金融業者幾乎都須經授權或登記」**。
   原文是 `almost all **financial** firms`；掉了 financial 會被讀成所有行業都要向 FCA 登記。
7. **表格第 5 列第 3 欄「另有查不到的事項」→「查不到的事項見工具說明頁」**。
   該欄欄名是「FCA 新聞稿的說法」，但 `Information you won't find on this tool` 寫在 Firm Checker 說明頁、不在新聞稿裡；第一輪修好了主詞，出處卻記到了錯的文件上。
8. **第 1 節第 3 段「數位資產的複雜性」→「加密貨幣的複雜性」**。
   警官原話是 `The complex nature of cryptocurrency`；`digital assets` 是他**前一句**的用字，原譯把「複雜性」接到了另一句的主詞上。零字數增減。

### 覆核無誤、沒有動的部分

- **骨幹四件事複核無誤**：兩個日期分得清楚；登記義務句 `Peer-to-peer trading is when individuals… requires appropriate registration.` 在兩篇**逐字相同**，
  `personal basis` 只在 4 月那篇（9 月 0 次）；「點對點登記為零」只引用新聞稿當下的陳述；Firm Checker 的界線不比來源寬。
- **第一輪 5 處把否定句限縮成「這次行動」是必要的**：9 月那篇的 `arrest`／`prosecut` 各只出現 1 次，都落在 `track record` 那一句，未限縮的原句確實會被同一頁推翻。
  FAQ 第 1 題新寫的「那是別的案子」也撐得住——4 月那篇把逮捕 2 人繫在 **2024 年 6 月**。
- **合作單位**：`HM Revenue & Customs (HMRC) and the Metropolitan Police Service`（9 月）對 `…and the South West Regional Organised Crime Unit (SWROCU)`（4 月），
  HMRC 兩次都在，換掉的是警方單位；第一輪改的三處都正確。
- **次數**：全文沒有任何「第 N 次」；摘要第 3 句對應 `This operation follows action taken by FCA… in April.`，與 9 月自己的複數 `further operations` 不衝突。
- **改過的表格四格**逐字對得上：`on a personal basis`、`almost all financial firms must be authorised or registered by us`、
  `Cease and desist letters were issued at all 3 premises`、`Information you won't find on this tool`。
- **第 5 節的「經 FCA 授權」**對應 `is authorised by us`，「是否具有提供你要的服務的許可」對應 `has our permission to provide the services you want`，`sources[]` 與研究紀錄一致。
- **免責 callout** 與 `crypto.md` 樣板**以程式逐字比對相同**（只有查核日不同），未動。
- **刪掉的台灣否定句沒有以任何形式回來**：全篇「台灣主管機關」「金管會」「沒有查到」各 0 次。研究紀錄裡一條說「本文在文中明說沒有查到台灣的對應公告」的舊敘述已同步改掉。
- **界線**：沒有幣價、漲跌幅、市值、交易量、資金流或報酬；沒有點名或比較任何交易所、錢包、兌幣管道；唯一的「投資」字樣是 FCA 自己的 `Crypto is a high-risk investment`，已歸因。
- **字數**：2,964 → **2,955**。本輪加的字全部從第 1 點那句重複敘述裡扣回來，沒有刪任何限定詞或但書。

### 留給站主／協調者

1. **唯一的 FAIL 照舊**：第二個結尾連結的 text「英國 FCA 加密資產監理範圍最終指引」尚未對齊
   `crypto-news-fca-perimeter-guidance-20260916` 的 zh-TW title（2026-09-18 為
   「英國 FCA 發布加密資產監理範圍最終指引 PS26/18：申請 9 月 30 日開放、新制 2027 年 10 月生效」）。
   依指派訊息由協調者事後對齊，兩輪查核都未動，也未改寫那一篇。
2. **9 月那篇新聞稿到今天仍無修訂紀錄區塊**——4 月那篇是發布後 26 天才被補上「以個人身分進行的點對點交易不需要登記」這句關鍵但書。出刊前再看一次該頁的 Last updated。
3. **一句編輯過場句留著沒改**：第 4 節第 3 段「加密資產在英國的規範範圍本身還在擴大中」。
   來源只印 `…until October 2027`，沒有寫 2027 年 10 月之後會怎樣；下一句立刻歸因給 FCA 原文，所以本輪沒有動，但審稿若要更保守，可換成不帶方向的說法。

### 第二輪結論

`ok`。8 處都是措辭範圍與歸屬，沒有動到事實骨幹；自檢只剩允許的那一條 FAIL。
