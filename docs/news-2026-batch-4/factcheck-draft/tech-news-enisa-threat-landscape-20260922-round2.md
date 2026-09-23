# 查核報告：tech-news-enisa-threat-landscape-20260922（第二輪）

- 查核者：第二輪獨立查核代理（Claude Opus 5, 1M context），沒有參與撰稿，也沒有參與第一輪
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-enisa-threat-landscape-20260922.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-enisa-threat-landscape-20260922.json`
- 第一輪報告：`factcheck/tech-news-enisa-threat-landscape-20260922-round1.md`（98 條、改 14 處）
- 本輪主張數 62：**CONFIRMED 55、CHANGED 7、NOT FOUND 0**
- 結論：**ok**

---

## 1. 來源重抓與 PDF 自行重抽（2026-09-23 台北）

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機之間間隔 2 秒。**任何請求的 UA、標頭、查詢字串與表單都沒有帶入任何人的姓名、email 或其他個人資料。**

| # | 來源 | HTTP | bytes | 轉址 | 讀到正文 | md5 與 `_raw`／第一輪 `r1` 副本 |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | ENISA 新聞稿 | 200 | 62,053 | 0 | 是 | `be0a821e…` 相同 |
| S2 | ENISA 出版品頁 | 200 | 52,427 | 0 | 是（`Publication date: September 22, 2026`、Download、Language 只有 EN） | `4442dc5e…` 相同 |
| S3 | 報告全文 PDF | 200 | 8,377,315 | 0 | 是 | `b68957da…` 相同 |

三個檔案都沒有換版（`live_data_warnings` 第 2 條要求的 bytes／md5 比對通過）。

**PDF 沒有沿用任何既有的抽文字檔**（撰稿代理的 `etl2026.txt`、第一輪的 `r1/etl2026.txt` 都沒有讀）：
用系統 python 的 pypdf 6.16.2 自己逐頁重抽，101 頁、248,588 字元，逐頁存成 `pdf_pages.json`，
之後所有頁碼與檢索都以這一份為準（本輪的字元數與第一輪回報的 250,702 不同，是抽取參數差異，不是換版——
md5 相同）。HTML 自己去 `<script>`／`<style>`／`<!-- -->`、去標籤、`html.unescape` 後再檢索。

工具在 `C:\Users\x8120\mokaair-work\news47\_tools\tech-news-enisa-threat-landscape-20260922-r2\`
（`extract_r2.py`、`find.py`、`quotes_r2.py`、`validate_r2.py`、`fix_pack_r2.py`、`fix_record_r2.py`），
重抓的原始檔在 `_r2raw\tech-news-enisa-threat-landscape-20260922\`。

---

## 2. 查核範圍

1. 第一輪改動的 **14 處全部**（C1–C14）。
2. 第一輪**新寫進內容包的每一句**（台灣三處、C4 的但書、C7 的表格備註、C12 的授權條件——第一輪自己點名沒有人查過的四處）。
3. 第一輪 76 條 CONFIRMED 裡用固定亂數種子（`random.seed("enisa-round2-2026-09-23")`）抽出的三分之一，
   25 條：**1、7、8、9、27、28、39、41、45、47、48、50、52、53、60、69、70、73、75、76、78、81、85、93、95**。
4. `verified_facts` **全部 50 條** `verbatim_quote` 的連續字串比對。
5. 全篇機械檢查與界線檢查。

---

## 3. 第一輪 14 處改動的複查

| 第一輪 | 複查結果 | 本輪自己抓到的判準 |
| --- | --- | --- |
| C1 description 的數字出處 | **成立** | 報告 **p.11**「Across incidents of unauthorised access for which ENISA was able to identify an intrusion vector (5.2%), 60.4% were seen leveraging a vulnerability」；新聞稿印 `(5%)`／`60%`。（第一輪報告把這一句寫成 p.12，實際橫跨 p.11 頁尾；內容包沒有印頁碼，文章不受影響） |
| C2 台灣 | **成立，但寫法再收**（見第 4 節 R2-1／R2-2） | 大小寫不敏感全文檢索：`Taiwan` 2 次、**都在 p.78 同一段**；`Taipei`／`Chinese Taipei`／`Formosa` 各 0 次；新聞稿與出版品頁 0 次 |
| C3 「同一句話交代」的出處 | **成立** | `To shape our understanding…observed from 1 January to 31 December 2025` 在新聞稿 4 次、出版品頁 3 次、**報告 PDF 0 次** |
| C4 補回報告的但書 | **成立，但主詞要收窄**（R2-3） | p.9「For this ETL, ENISA also expanded the number of tracked cybercrime activities (including data breaches and fraud). **While this** was observed to have an impact on the numbers…, it did not substantially change the trends and rankings **observed in the previous iteration**.」 |
| C5 CVE 22% 不寫「全球」 | **成立** | p.90「Overall, more than 48 thousand new vulnerabilities were published in 2025…a 22% increase from the previous year.」——沒有地理範圍；同章 p.89 講 DDoS 才寫「At a global level」 |
| C6 新聞稿那句在開頭不在標題 | **成立** | 新聞稿 `<h1>`／麵包屑是「Exploring the evolution…」；該句在 `Press Release / Sep 22,2026` 之後的前言段 |
| C7 表格第三列不同軸 | **成立** | p.7 動機軸：ideology 57.3%／financially motivated 29.3%／cyberespionage 5.9%；p.13「Unauthorised access follow with 39.5%, **dominated by financially motivated activities (63.9%)**」——兩軸確實重疊（約 25 個百分點同時落在兩列） |
| C8 5.2% 不指定基數 | **成立** | p.11 只印 `(5.2%)`；對照 p.60 寫得出分母（`in only 20% of the recorded incidents`） |
| C9 偏誤在方法論不在附錄 | **成立** | p.9 章名就是 `Methodology`，原文限定詞是 `inherent to open-source reporting`；Appendix A（p.97）是執法行動表、Appendix B（p.100）是可能性用語表 |
| C10 「擴大攻擊面」是新聞稿的話 | **成立** | `expand the attack surface`、`new level of vigilance` 在報告 101 頁全文各 **0 次** |
| C11 不是「轉趨謹慎」 | **成立** | p.8／p.96 同段先寫「ENISA assess artificial intelligence will **highly likely** increasingly support malicious operations」，再用 likely 寫攻擊鏈那一句 |
| C12 CC BY 4.0 的條件 | **成立** | p.2「**Unless otherwise noted**, the reuse of this document is authorised under the CC BY 4.0 licence…reuse is allowed, **provided appropriate credit is given and any changes are indicated**」；p.3「Copyright for the image on the cover © Shutterstock」；p.3 ISBN 978-92-9204-807-5（與 `sources[]` 第三條的標題一致） |
| C13／C14 callout 的台灣句與 CVE 句 | **成立** | 同 C2／C5；callout 其餘五句逐條複查後保留 |

第一輪四處「自己新寫、沒有人查過」的句子，本輪逐句回原文：台灣三處（**改**，見 R2-1／R2-2）、
C4 的但書（**主詞改**，見 R2-3）、表格第三列備註（**成立，保留**）、CC BY 4.0 條件（**成立，保留**）。

---

## 4. 本輪改掉的 7 處（before → after）

**R2-1 — 第二段的台灣句：拿掉查證流水帳，收成一句中性轉述**
- before：`報告統計的是歐盟會員國與設在歐盟的組織，沒有任何台灣機關或企業的事件；新聞稿與出版品頁沒有提到台灣，報告全文只有一處寫到台灣——在直接取材自歐盟對外事務部（EEAS）資訊操弄報告的那一章，台灣與香港、新疆、西藏被列為中國相關敘事經常出現的題目。`
- after：`報告統計的是歐盟會員國與設在歐盟的組織，沒有任何台灣機關或企業的事件；報告談資訊操弄的那一章（內容取自歐盟對外事務部 EEAS 的資訊操弄報告）把台灣列為中國相關敘事經常出現的題目之一。`
- 依據：協調者裁定（一句中性轉述、歸給報告的 FIMI 章、不做延伸；第二段除批次固定的查核日句外不留查證流水帳）。
  另外「報告全文**只有一處**寫到台灣」本身也不精確——`Taiwan` 出現的是**兩次**，同在 p.78 同一段。
  FIMI 章的出處以報告自己的兩個寫法為準：p.74「This section was directly drawn from the EEAS 4th report on Foreign Information Manipulation and Interference, published in March 2026」、p.9「Incidents documented in the FIMI chapter were drawn from the European External Action Service's (EEAS) FIMI Threat Landscape 2025」。
  <https://www.enisa.europa.eu/sites/default/files/2026-09/ENISA%20Threat%20Landscape%202026_Final.pdf>

**R2-2 — FAQ 第二題：同一個處理**
- before：`…沒有任何台灣機關或企業的事件；新聞稿與出版品頁完全沒有提到台灣。報告全文提到台灣的地方只有一處：在直接取材自…那一章，台灣與香港、新疆、西藏被列為中國相關敘事經常出現的題目——那是被討論的題目，不是被統計的事件。`
- after：`…沒有任何台灣機關或企業的事件。報告談資訊操弄的那一章（內容取自歐盟對外事務部 EEAS 的資訊操弄報告）把台灣列為中國相關敘事經常出現的題目之一——那是被討論的題目，不是被統計的事件。`
- 依據：同 R2-1。FAQ 的答案仍然是正文的子集。

**R2-3 — 報告那句但書的主詞被放大了**
- before：`新增了資料外洩與詐騙，這些改變都會影響報告裡的數字（報告同時寫明，這並沒有實質改變趨勢與排名）。`
- after：`新增了資料外洩與詐騙；報告同時寫明，追蹤範圍的擴大會影響報告裡的數字，但沒有實質改變前一版觀察到的趨勢與排名。`
- 依據：p.9 的 `While this…` 承接的是**前一句**「ENISA also expanded the number of tracked cybercrime activities」，
  不是「曆年制＋六個月重疊＋擴大範圍」這三件事；原句也漏掉 `observed in the previous iteration` 這個限定。
  改寫後在兩種讀法下都成立，「不比較年增減」的理由（六個月重疊）不受影響。

**R2-4 — 8,257 起事件的資料來源少了「mainly」**
- before：`資料來自三個管道：公開來源、歐盟會員國匿名分享的資訊，以及透過 ENISA Cyber Partnership Programme 取得的資訊；`
- after：`資料主要來自公開來源，另有歐盟會員國與 ENISA Cyber Partnership Programme 成員匿名分享的資訊；`
- 依據：p.9「collected and analysed 8 257 incidents, **mainly** based on information from open sources, as well as anonymised information shared by EU Member States (EU MSs) **and members of** the ENISA Cyber Partnership Programme」。
  這一段講的是報告內頁的方法論（新聞稿沒有印 8,257，本輪重新確認 `8 257`／`8257`／`8,257` 在新聞稿與出版品頁都是 0 次），
  所以要照報告的寫法：「主要靠公開來源」＋「會員國與 CPP 成員匿名分享」，不是三個並列的管道。限定詞不能刪。

**R2-5 — 29.3% 沒有指明出自哪一章**
- before：`報告把以牟利為目的的活動（占所有紀錄事件 29.3%，特別是勒索軟體）稱為…`
- after：`報告的執行摘要把以牟利為目的的活動（占所有紀錄事件 29.3%，特別是勒索軟體）稱為…`
- 依據：報告自己有兩個數字——p.7 執行摘要「Financially motivated activities (**29.3%** of all recorded incidents)」、
  p.13 第 1 章「financially motivated operations (**29.2%**)」（p.38 第 3 章另寫網路犯罪占 29.3%）。
  研究紀錄 `unverified_or_excluded` 第 5 條要求「寫『約 29%』或明寫是哪一章的數字」；
  表格 caption 早就寫明「依報告執行摘要整理」，正文這一句補上同樣的出處後，summary 第三句與 FAQ 第五題的同一個數字才有依據。

**R2-6 — 表格第一列的「短時間」來源沒有印**
- before：`["DDoS", "51.3%", "件數最多，多屬短時間灌爆，衝擊通常有限"]`
- after：`["DDoS", "51.3%", "件數最多，報告寫這一類是低衝擊的攻擊"]`
- 依據：報告 p.12 與新聞稿寫的是 **low-impact**（低衝擊），沒有為 ENISA 這份歐盟資料集印過任何「持續時間短」的描述。
  報告裡唯一講 DDoS 時長的是 p.89「In Q3, 71% of HTTP DDoS attacks and 89% of network-layer attacks **globally** ended in under 10 minutes」
  ——那是全球資料，而且本篇刻意沒有引用 p.89。整篇文章在教讀者看範圍與分母，表格自己不能多加一個來源沒印的性質。

**R2-7 — AI 那一段只取了報告的前半句**
- before：`…而不是取得突破性的新能力。值得一提的是，ENISA 自己也在報告裡揭露：…所有產出都經過人員審閱驗證…`
- after：`…而不是取得突破性的新能力——但緊接著的但書是，模型的進步已經被觀察到在加速漏洞的發掘與利用。值得一提的是，ENISA 自己也在報告裡揭露：…所有產出都經過領域專家審閱驗證…`
- 依據：p.15 在「attackers primarily use consumer-grade AI tools to augment existing skills and adapt attack vectors rather than to achieve breakthrough capabilities」
  之後**緊接著**寫「While attackers primarily use AI to augment existing skills, **model improvements have already been seen accelerating vulnerability discovery and exploitation**.」
  正文用「AI 的角色沒有那麼戲劇化」起頭卻只取前半句，等於把來源往單一方向加強一格。
  另外 p.4 的免責聲明寫的是 `reviewed and validated by **subject-matter experts**`，「領域專家」比「人員」貼近原文。

---

## 5. 抽樣複查的 25 條 CONFIRMED（全部再次成立）

| 抽中的第一輪編號 | 主張 | 本輪判準 |
| --- | --- | --- |
| 1 | 標題：報告名稱 2026、統計 2025 一整年 | S2＋報告 p.9 |
| 7 | 2026-09-22 同日發布報告與新聞稿 | 新聞稿 `Sep 22,2026`、出版品頁 `Publication date: September 22, 2026` |
| 8 | 範圍是歐盟會員國與設在歐盟的組織 | p.10「a snapshot of threats faced by EU MSs and EU-based organisations」；p.7 同義 |
| 9 | 報告名稱 2026、統計 2025 全年 8,257 起 | p.9 |
| 27 | 與上一版有六個月重疊 | p.9 |
| 28 | 擴大追蹤範圍，新增資料外洩與詐騙 | p.9 |
| 39 | 新聞稿開頭那句是 ENISA 對整份報告下的總結 | 新聞稿前言段的位置與語氣（「The 2026 ENISA Threat Landscape confirms that…」） |
| 41 | DDoS 件數最多、51.3% | p.7／p.11／p.12；新聞稿寫 51% |
| 45 | 新聞稿：勒索軟體仍是短期衝擊最大 | 新聞稿 Key highlights 第一條逐字 |
| 47 | 公共行政 81.8% 是意識形態驅動的 DDoS | p.20 |
| 48 | 「網站被灌爆，不是被入侵」 | p.20「Public-facing websites and portals…repeatedly targeted」 |
| 50 | 未授權存取 39.5%、件數第二 | p.11「followed by unauthorised access (39.5%)」；p.13 |
| 52 | 表格三個數字都在執行摘要 | p.7（51.3%／39.5%／29.3%） |
| 53 | 新聞稿最容易被誤讀的是「60% 是利用漏洞」 | 新聞稿逐字 |
| 60 | 那 20% 的子集合裡 70% 是漏洞利用 | p.60 |
| 69 | 71% 的漏洞把攻擊向量標為 Network | p.91 |
| 70 | 也就是有可能被遠端利用 | p.91「potential risk of remote exploitation」 |
| 73 | 讀者做法是編輯整理、不是 ENISA 的清單 | 報告全文沒有這種清單，正文也自陳 |
| 75 | 正文不含 CVE 編號與品牌型號 | 機械檢查：`CVE-\d{4}-\d+` 0 筆、六個廠牌名各 0 筆 |
| 76 | 供應鏈與第三方攻擊持續被觀察到 | p.12 |
| 78 | 報告舉 Shai-Hulud 行動為例 | p.12 |
| 81 | 威脅類別界線持續模糊 | 新聞稿逐字 |
| 85 | 報告揭露只在有限範圍內用 AI | p.4 DISCLAIMER |
| 93 | 這份報告沒有替任何人新增法律義務 | p.2 LEGAL NOTICE「It does not endorse a regulatory obligation…」；全文無義務性條文 |
| 95 | NIS2 的義務來自指令本身 | p.18／p.19 只把 NIS2 當比較與分類基準 |

## 6. `verified_facts` 的 `verbatim_quote`（50 條全查）

程式做連續字串比對（NFKC 正規化、彎引號與破折號統一、空白收斂；含 `...`／`…`／`|` 的引文逐片段查）：

- **49 條**在本輪自己抓到的正文裡找得到**連續**字串，沒有一條是把不同段落拼起來的。
- 第 2 條 `/sites/default/files/2026-09/ENISA%20Threat%20Landscape%202026_Final.pdf` 是出版品頁的下載路徑，
  在 `pub.html` 原始碼裡找得到（去標籤後的可見文字裡當然沒有）——**不是問題**。

## 7. 機械檢查與界線

- 「本文」：內容包 **0 次**。
- 歸因密度：每段 ≤2（最多的 P04、P07、P08、P10 各 2），開頭兩段 ≤1。
- `description` 191 字、以「（2026 年 9 月查證）」收尾、沒有挑選數量、沒有查證流水帳。
- 日期一致性：slug 尾碼 `20260922` ＝ `news_date` `2026-09-22` ＝ 第一段「2026 年 9 月 22 日」；
  三條 `sources[].checked_on` 與研究紀錄 `checked_on` 都是 `2026-09-23`（本輪重抓日相同，依規格**未更動**）。
- 圖解 caption 與研究紀錄 `diagram.caption` **逐字相同**；`summary` 四句與圖解四個節點的每個數字都出現在正文。
- 兩個結尾連結的 text 與 `tech-news-2026-index.json`、`tech-news-cisa-kev-linux-kernel-20260918.json` 的
  zh-TW `title` 程式比對 `==` 為 **True**（後者 `news_date` 2026-09-18、`display_order` 318，與正文「前不久」相符）。
- `hero.alt` 依規格未查、未改。
- 段落總字數 **2,710**（1,800–3,000）；五個小節、每節 2–4 段；只有一個 `info` callout，沒有投資免責段落、沒有 `finance` 主題。
- 界線（`tech.md`）：沒有購買建議或推薦式比價；沒有沒歸因的廠商宣稱；沒有把 likely 的前瞻評估寫成已發生；
  沒有可操作的攻擊細節、入侵指標、CVE 編號或機型；沒有推定台灣可用或適用；沒有最高級（「首次」「史上最多」）。

## 8. 留給站主／協調者的事

1. **台灣那三處**已照協調者裁定收成一句中性轉述（第二段、FAQ 第二題、callout，用語一致）。
   若還要再收，最多只能收到「統計範圍是歐盟會員國與設在歐盟的組織」為止；
   **不可以恢復「報告沒有提到台灣」**——本輪重抓、重抽、重新全文檢索的結果仍然是報告 p.78 寫到台灣兩次。
2. 「**沒有任何台灣機關或企業的事件**」是從報告自印的統計範圍推得的（報告不列受害組織，`must_not_write` 第 24 條也不許寫）。
   這個推論 `must_not_write` 第 15 條已明文允許，本輪照留；要更保守可改成「統計範圍限於歐盟會員國與設在歐盟的組織，台灣不在其中」。
3. **報告內部有兩套數字**：金錢動機 29.3%（p.7 執行摘要）對 29.2%（p.13 第 1 章）、網路間諜 5.9%（p.7）對 6.3%（p.13）。
   本篇只用 29.3% 並在正文與表格 caption 寫明出自執行摘要（`unverified_or_excluded` 第 5 條允許）。
   若站主希望正文點出這個內部不一致，要同時改 `summary` 第三句與 FAQ 第五題。
4. `live_data_warnings` 第 5 條把「vulnerability-lookup 的 CVE 統計」列為 ENISA 轉述的第三方數字。
   本輪逐字看過 p.90：腳註 627（vulnerability-lookup.org）掛在「未修補的老舊 IoT 與邊緣裝置」那一句，
   **48,000／22% 那一句沒有腳註**，新聞稿也是以 ENISA 自己的口吻寫。本篇因此維持「報告另外統計了漏洞面」的寫法；
   若站主認為仍要歸因給 vulnerability-lookup，第 13 段要改寫。
5. 第一輪報告把 5.2%／60.4% 那一句標成報告 p.12，實際橫跨 **p.11** 頁尾。內容包不印頁碼，文章不受影響；
   協調者把報告併進 `factcheck-draft/` 時若要引頁碼，以本輪的 p.11 為準。
6. 新聞稿「Additional resources」那一條的 href 仍是含個人資料夾名稱的本機檔案路徑（ENISA 的貼上失誤）。
   本輪同樣**沒有引用、沒有抄錄**那個字串到任何檔案或回報。
7. 研究紀錄 `verified_facts` 第 3 條寫「每頁頁首印 TLP:CLEAR」，本輪重數是 **101 頁中的 100 頁**（封底沒有）。
   內容包沒有用到這個說法，本輪同樣只記錄、未改。

## 9. 自檢輸出（原樣）

```
OK tech-news-enisa-threat-landscape-20260922 zh-TW paragraphs 2710
EXIT:0
```

```
tech-news-enisa-threat-landscape-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-enisa-threat-landscape-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-enisa-threat-landscape-20260922/diagram-1.svg
1 entries checked
EXIT:1
```

`pack_cli lint` 只剩 `image_missing` 與 `raw_internal_url` 兩種，與 FACTCHECK-47 的預期一致（出圖與 relink 之前本來就會有）。

## 10. 結論

**ok**。本輪查了 62 條、改了 7 處，沒有一處推翻論述骨幹：
第一輪的 14 處改動全部成立，其中兩處（C2 的台灣寫法、C4 的但書主詞）本輪再收緊，
另外五處是撰稿階段留下的限定詞與出處問題（`mainly`、29.3% 的章節、表格的「短時間」、AI 那一段的但書、subject-matter experts）。
研究紀錄的 `factcheck.second_round` 已寫入（`verdict: "ok"`）。只動了內容包與研究紀錄兩個檔案，沒有 git 操作，repo 裡沒有留暫存檔。
