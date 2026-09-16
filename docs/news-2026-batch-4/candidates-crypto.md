# 幣圈候選題目（待站主圈選）

前三批的作法是**站主從候選清單裡挑題目**（`docs/ai-news-2026-09-mid/README.md`：
「題目由站主在 2026-09-15 從候選清單選定」）。這份是幣圈垂直的候選。

界線見 [`crypto.md`](crypto.md)：**只寫法規、技術與產業，不碰行情。**
下面每一則都是這個界線內的題目。

## 狀態說明

| 標記 | 意思 |
| --- | --- |
| ✅ 已驗 | 已經在一手來源讀到，網址與關鍵數字列在下面，可以直接開稿 |
| ⚠️ 待驗 | 只有線索（整合站、法律事務所部落格），**還沒回到一手來源**，開稿前必須自己查 |
| ❌ 查否 | 查過一手來源，**與線索說法不符或官方未說明**，不能照線索寫 |

查核日：2026-09-16。

先讀 [`candidates-tech-and-ai.md`](candidates-tech-and-ai.md) 開頭那張**官方 feed 對照表**：
廠商的官方 RSS/Atom 比抓網頁可靠（`openai.com` 網頁 403、feed 200），
而且日期是官方給的。幣圈這邊的主管機關多數沒有 feed，
但 Federal Register 有 API（見 C3、C4），是同一個道理：
**找官方的結構化管道，比猜網址可靠。**

---

## ✅ 已驗：可以直接開稿

### C1 — 台灣《虛擬資產服務法》三讀通過
- **事件日** 2026-06-30
- **建議 slug** `crypto-news-taiwan-vasp-act-20260630`
- **一手來源**
  - 金管會新聞稿「立法院院會三讀通過『虛擬資產服務法』」
    `https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0&mcustomize=news_view.jsp&dataserno=202606300002&dtable=News`
  - 金管會主管法規共用系統 法規內容「虛擬資產服務法」
    `https://law.fsc.gov.tw/LawContent.aspx?id=GL004301`
- **新聞稿明載**：七種服務商（交換商、交易平台商、移轉商、保管商、承銷商、借貸商及其他）；
  境內發行穩定幣須經中央銀行與金管會許可，並「維持十足準備資產及交付信託」；
  既有業者「應於本法案施行後 12 個月內向金管會申請許可，並於本法案施行後 21 個月內
  經金管會許可及取得許可證照」，得展延 3 個月。
- **讀者角度**：從洗錢防制登記制改成許可制，對一般使用者代表什麼——
  手上在用的平台會不會消失、過渡期多長、怎麼查一家業者的狀態。
- **不要寫**：哪家交易所會活下來、該不該換平台。

### C2 — 歐盟 MiCA 過渡期結束
- **事件日** 2026-07-01（ESMA 於 2026-06-23 發出公開聲明）
- **建議 slug** `crypto-news-mica-transition-ends-20260701`
- **一手來源**
  - ESMA「Public Statement: MiCA transitional period ends」（2026-06-23）
    `https://www.esma.europa.eu/sites/default/files/2026-06/ESMA75-113276571-1710_Public_Statement_MiCA_transitional_period_ends.pdf`
  - ESMA「Statement on the end of transitional periods under MiCA」（2026-04）
    `https://www.esma.europa.eu/sites/default/files/2026-04/ESMA75-113276571-1679_Statement_on_the_end_of_transitional_periods_under_MiCA.pdf`
  - ESMA 各會員國過渡期長度對照表（MiCA 第 143(3) 條）
    `https://www.esma.europa.eu/sites/default/files/2024-12/List_of_MiCA_grandfathering_periods_art._143_3.pdf`
- **要點**：過渡期 2026-07-01 全歐結束；祖父條款只在原會員國有效、沒有 passporting；
  各會員國過渡期長度不同，要用 ESMA 那張對照表，不要一概而論。
- **讀者角度**：台灣讀者用到的歐洲平台可能因此停止對歐盟客戶服務，
  以及「有沒有牌照」要去哪裡查。

### C3 — CFTC 與 SEC 聯名：加密資產適用證券法的解釋令
- **事件日** 2026-03-23（聯邦公報刊登日與生效日）
- **建議 slug** `crypto-news-sec-crypto-interpretation-20260323`
- **一手來源**（`sec.gov` 實測 403，改用聯邦公報，這是官方刊登管道）
  - Federal Register, Rule：「Application of the Federal Securities Laws to Certain Types of
    Crypto Assets and Certain Transactions Involving Crypto Assets」
    `https://www.federalregister.gov/documents/2026/03/23/2026-05635/application-of-the-federal-securities-laws-to-certain-types-of-crypto-assets-and-certain`
    （type: Rule；publication_date 2026-03-23；effective 2026-03-23）
- **❌ 一個已經修正的錯誤**：這不是 SEC 單獨發布。
  聯邦公報的 `agencies` 欄位寫的是
  **Commodity Futures Trading Commission, Securities and Exchange Commission**，
  是兩個機關**聯名**。文章寫成「SEC 發布」就是錯的。
- **⚠️ 開稿時要釐清**：法律事務所的整理說 SEC 是 **3/17 發布**、3/23 生效。
  聯邦公報的刊登日是 3/23。**發布日與刊登日是兩件事，文章要寫清楚是哪一個**，
  並以能指到原文的那一個為準。
- **不要寫**：哪些幣「被認定不是證券所以可以買」。分類是法律地位，不是投資評價。

### C4 — SEC 提出 Regulation Crypto Assets
- **事件日** 2026-08-21（聯邦公報刊登日）
- **建議 slug** `crypto-news-sec-regulation-crypto-assets-20260821`
- **一手來源**
  - Federal Register, Proposed Rule：「Regulation Crypto Assets」
    `https://www.federalregister.gov/documents/2026/08/21/2026-17183/regulation-crypto-assets`
    （評論截止 **2026-10-20**，來自 Federal Register 的 `comments_close_on`）
- **⚠️ 同 C3**：線索說 8/18 提出、聯邦公報 8/21 刊登，兩個日期要分清楚。
  評論期的長度要從刊登的原文讀，不要抄整理文章。
- **讀者角度**：這還只是**草案**，不是生效的規則——把「提出」和「通過」分開寫，
  是這篇最重要的事。

### C5 — EBA 對 PSD2 與 MiCA 銜接的意見書
- **事件日** 2026-02-12（意見書），過渡期 2026-03-02 結束
- **建議 slug** `crypto-news-eba-psd2-mica-20260212`
- **一手來源**
  - EBA/OP/2026/01「Opinion on the end of the NAL transition period」（2026-02-12）
    `https://www.eba.europa.eu/sites/default/files/2026-02/3b8b6f18-ca26-4ce1-83eb-d060276f3301/Opinion%20on%20the%20end%20of%20the%20NAL%20transition%20period.pdf`
  - EBA 新聞稿「EBA advises national authorities on actions to take at the end of the
    transition period under its No-Action Letter…」
    `https://www.eba.europa.eu/publications-and-media/press-releases/eba-advises-national-authorities-actions-take-end-transition-period-under-its-no-action-letter`
- **要點**：2025-06-02 的 No-Action Letter 給 CASP 九個月，處理「移轉電子貨幣代幣
  構成支付服務、因此需要 PSD2 授權」的問題；過渡期 2026-03-02 結束；
  意見書列出各國主管機關可以讓 CASP 在尚未取得 PSD2 授權時繼續提供 EMT 服務的條件。
- **⚠️ 不要照抄的說法**：某整合站寫這「等於讓合規成本加倍」——那是評論，不是官方說法。

---

### C6–C9 — 美國 GENIUS Act 的落地：四個主管機關同時提規則

【Guiding and Establishing National Innovation for U.S. Stablecoins Act】（GENIUS Act）
在 2026 年由四個主管機關分別提出實施規則。
**這是純法規題材，完全落在站主定的界線內**，
而且四則可以合成一篇「美國穩定幣法怎麼落地」，也可以拆開。

全部來自 Federal Register API（`sec.gov` 被 403 擋掉時的官方刊登管道），
含機關、標題與評論截止日：

| 代號 | 刊登日 | 機關 | 評論截止 |
| --- | --- | --- | --- |
| C6 | 2026-03-02 | Treasury / OCC | 2026-05-01 |
| C7 | 2026-04-10 | Treasury / OFAC / FinCEN | 2026-06-09 |
| C8 | 2026-04-10 | FDIC | 2026-06-09 |
| C9 | 2026-05-18 | NCUA | 2026-07-17 |

- **C6** `crypto-news-genius-act-occ-20260302`—「Implementing the Guiding and Establishing
  National Innovation for U.S. Stablecoins Act for the Issuance of Stablecoins by Entities
  Subject to the Jurisdiction of the Office of the Comptroller of the Currency」
  `https://www.federalregister.gov/documents/2026/03/02/2026-04089/implementing-the-guiding-and-establishing-national-innovation-for-us-stablecoins-act-for-the`
- **C7** `crypto-news-stablecoin-aml-20260410`—「Permitted Payment Stablecoin Issuer
  Anti-Money Laundering/Countering the Financing of Terrorism Program and Sanctions
  Compliance Program Requirements」
  `https://www.federalregister.gov/documents/2026/04/10/2026-06963/permitted-payment-stablecoin-issuer-anti-money-launderingcountering-the-financing-of-terrorism`
- **C8** `crypto-news-fdic-genius-act-20260410`—「GENIUS Act Requirements and Standards for
  FDIC-Supervised Permitted Payment Stablecoin Issuers and Insured Depository Institutions」
  `https://www.federalregister.gov/documents/2026/04/10/2026-06974/genius-act-requirements-and-standards-for-fdic-supervised-permitted-payment-stablecoin-issuers-and`
- **C9** `crypto-news-ncua-genius-act-20260518`—「Implementing the … U.S. Stablecoins Act for
  the Issuance of Stablecoins by Entities Subject to the Jurisdiction of the National Credit
  Union Administration」
  `https://www.federalregister.gov/documents/2026/05/18/2026-09915/implementing-the-guiding-and-establishing-national-innovation-for-us-stablecoins-act-for-the`

**讀者角度**：穩定幣在美國從「沒人管」變成「誰可以發、要守什麼規矩」，
對台灣使用者來說最直接的影響是跨境支付與儲值服務的對手方是誰。
**不寫**哪一樣穩定幣比較安全、該不該持有。

### C10、C11 — 日本 FSA

從 FSA 自己的 2026 年英文新聞稿索引讀到，**不是整合站**：

- **C10**｜2026-02-16｜`crypto-news-jfsa-working-group-20260216`
  「Publication of the Report by the Working Group on Crypto-asset Systems of the
  Financial System Council」
- **C11**｜2026-07-23｜`crypto-news-jfsa-cybersecurity-20260723`
  「Cybersecurity Issues and Countermeasures in Crypto-Asset-Related Businesses」

索引頁 `https://www.fsa.go.jp/en/news/index.html`，開稿時點進各自的新聞稿讀內文。

⚠️ **整合站說「2026 年 4 月內閣通過修正金商法與資金決濟法的法案」，
FSA 的新聞稿索引上沒有這一則。** 要寫必須另外找到官方出處。

### ⚠️ 待驗：新加坡 MAS 的穩定幣論詢

線索：2026-09-01 就修正《支付服務法》以落地穩定幣框架提出論詢，
2026-10-16 截止，範圍是恞定星幣或任一 G10 貨幣的單一貨幣穩定幣。

**這個容器連不到 MAS**（兩個網址都回 service unavailable），
所以上面那些數字**都還沒有回到一手來源核對**。要寫先在別的環境驗過。
網址：`https://www.mas.gov.sg/news/media-releases/2026/mas-consults-on-legislative-amendments-to-implement-stablecoin-regulatory-framework`

---

## ❌ 查否：線索與一手來源不符

### 以太坊 2026 年的升級日期
整合站（CoinGecko、beincrypto、lbank 等）寫 Glamsterdam「targeting mainnet Q3 2026」、
Hegota「H2 2026」，並給了 EIP 編號與 gas limit 目標。

**但 `ethereum.org/en/history/`（官方）把 Amsterdam-Gloas（Glamsterdam）與
Bogotá-Heze（Hegotá）都列為「TBD」，沒有主網日期。**

所以：**不能寫「以太坊將在 Q3 2026 升級」**。如果要做以太坊的題目，
要嘛改寫成「下一次升級的內容與目前的狀態（官方未公布日期）」，
要嘛等官方公布日期。EIP 編號與內容要回 EIPs 原文查，不要抄整合站。

這一則保留在這裡，是因為它示範了 `crypto.md` 的白名單為什麼存在。

---

## 還沒查的方向

**現況：11 則已驗（C1–C11）＋1 則待驗（MAS）。重要新聞那 10–12 則的量已經到了。**
還缺的是 8/1 起的次要新聞 4–6 則，以及下列方向：

依 `crypto.md` 的界線，下列方向還沒查，開票前要補：

- 台灣：金管會 VASP 登記／許可名單的變動、調查局洗錢防制處的名單、
  金管會對虛擬資產的裁罰、央行對穩定幣的說法。
- 台灣稅務：虛擬通貨的個人所得申報實務。**已搜過 `mof.gov.tw`／`etax.nat.gov.tw`／
  `ntbt.gov.tw`，沒有找到 2026 年的專門公告**，可能沒有新聞可寫，或要換關鍵字再查。
- 亞太：日本 FSA、韓國 FSC／FIU、新加坡 MAS、香港 SFC 的 2026 年動作。
- 美國：CFTC、FinCEN、OCC；穩定幣立法的進度。
- 技術：比特幣的 BIP 動態、各 L2 的治理與規格變更、具名稽核報告。
- 產業：交易所與託管商的合規事件、資安事件、停止服務公告。

**每一則都要回一手來源。** 上面 C3／C4 的日期落差與以太坊那則，
就是不回一手來源會寫錯的實例。
