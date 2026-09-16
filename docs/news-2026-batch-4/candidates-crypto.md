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

### C3 — SEC 對加密資產適用證券法的解釋令
- **事件日** 2026-03-23（聯邦公報刊登日與生效日）
- **建議 slug** `crypto-news-sec-crypto-interpretation-20260323`
- **一手來源**（`sec.gov` 實測 403，改用聯邦公報，這是官方刊登管道）
  - Federal Register, Rule：「Application of the Federal Securities Laws to Certain Types of
    Crypto Assets and Certain Transactions Involving Crypto Assets」
    `https://www.federalregister.gov/documents/2026/03/23/2026-05635/application-of-the-federal-securities-laws-to-certain-types-of-crypto-assets-and-certain`
    （type: Rule；publication_date 2026-03-23；effective 2026-03-23）
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

## 還沒查的方向（要補足 10–12 則重要 + 4–6 則次要）

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
