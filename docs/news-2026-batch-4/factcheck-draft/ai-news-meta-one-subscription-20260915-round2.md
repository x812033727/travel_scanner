# ai-news-meta-one-subscription-20260915 查核報告（第二輪）

- 查核者：獨立查核代理（第二輪），未參與撰稿，也未參與第一輪
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/ai-news-meta-one-subscription-20260915.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-meta-one-subscription-20260915.json`
- 第一輪報告：`C:\Users\x8120\mokaair-work\news47\factcheck\ai-news-meta-one-subscription-20260915-round1.md`
- 覆核 62 條：CONFIRMED 50／CHANGED 12／NOT FOUND 0
- 事實類更動 8 處、協調者裁定 4 處（幣別改寫波及全篇；「併品牌」框架的裁定在交件後追加，見第 8 節）

## 1. 來源今天重抓的結果（第二輪自己抓，不沿用第一輪的檔）

UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 ≥2 秒；
UA、標頭、查詢字串、表單都沒有帶入任何人的姓名或 email。原始檔留在
`C:\Users\x8120\mokaair-work\news47\_r2raw\ai-news-meta-one-subscription-20260915\`。

| # | 網址 | HTTP | bytes | 轉址 | body 是否為正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://about.fb.com/news/2026/09/introducing-meta-one-subscription-service-more-features-ai/` | 200 | 713,186 | 0 | 是。`entry-content` 6,091 字元、`highlights-container`（Takeaways）390 字元、JSON-LD `articleBody` 6,343 字元／`wordCount` 991 |
| 2 | `https://about.fb.com/news/` | 200 | 307,920 | 0 | 是。這一則的 `<article>` 卡片同時印 `2026-09-15T08:00:59-07:00`（published）與 `2026-09-16T13:22:09-07:00`（updated） |
| 3 | `https://about.fb.com/news/2026/09/presentation-de-...-se-demarquer/` | 200 | 855,949 | 0 | 是。正文 8,725 字元，含全部歐元定價 |

三條的 bytes 與第一輪、與研究紀錄完全相同，頁面沒有在這幾小時內再被改動。

**逐字比對（程式做連續字串比對，彎引號／NBSP／破折號正規化後）**：研究紀錄 32 條 `verified_facts`
加 3 條 `sources[]` 共 35 條 `verbatim_quote`、內容包裡 4 段英文引文，**39 條全部命中，0 條落空**；
沒有任何一條含 `...`／`…`／`|` 的拼接引文，所以不需要逐片段拆檢。
其中 f21、f22、f25、f26、f27 只在 JSON-LD 的 `articleBody` 裡連續命中（渲染文字被 `<a>` 切開），
已另外確認那份 `articleBody` 就是頁面自己的正文（6,343 字元、不含研究紀錄警告的 `ay-eye` 朗讀器文字）。

**三個第一輪沒有自己驗、本輪補驗的機械事實**：
- `highlights-container`（Takeaways）的開標籤在 552,290 的 `entry-content` 之前（551,066），
  **摘要欄位確實排在正文前面**——第一輪的「寫在正文前方獨立的摘要欄位」成立。
- 全頁 `editor` 只出現 2 次，兩次都在 WordPress 的內嵌 CSS 裡；`entry-content` 內 `Update` 0 次。
  「9 月 16 日改過但沒有編輯說明」成立。
- 全頁 `USD` 0 次、`dollar` 0 次、`currency` 0 次、`Taiwan` 0 次（法文版同樣四項全 0）。

## 2. 覆核表

「為何查」：**R1改**＝第一輪改過的段落；**R1新**＝第一輪新寫進去、沒有人查過的句子；
**抽查**＝第一輪判 CONFIRMED 而本輪抽到的（72 條抽 35 條，超過三分之一）；**裁定**＝協調者指名。
判：C＝CONFIRMED、X＝CHANGED。來源縮寫：EN＝主來源、NR＝新聞總覽頁、FR＝法文版。

| # | 為何查 | 欄位 | 主張 | 來源怎麼寫 | 判 |
| --- | --- | --- | --- | --- | --- |
| 1 | R1改 | title | 「核心**體驗**維持免費」 | EN `The core experience across our apps and Meta AI` | C |
| 2 | R1改 | 研究紀錄 | `title` 已與內容包同步 | checker 的 `research title differs` 通過 | C |
| 3 | R1改/R1新 | §1 p1 | 「公告正文把這句話放在**前段**」 | 被引句在 `entry-content` 第二段 | C |
| 4 | R1新 | §1 p1 | 「頁首的摘要欄位則寫成未來式的 will stay free」 | Takeaways 第三條 `The core experience … will stay free.`；FR「restera gratuite」 | C |
| 5 | R1新 | §1 p1 | 「前一句講的是過去到現在，後一句才指向之後」 | `has always been free` 對 `will stay free` | C |
| 6 | R1改 | §2 p1 | Premium＝Core 全部＋「在 Meta AI 與旗下 App 家族裡最多的創作空間」 | EN `the most room to create content with Meta AI and across our family of apps` | C |
| 7 | R1新 | §2 p2 | Expert／Max「內容是最高等級的功能存取與 Meta Business Agent 容量，給大規模經營的團隊」 | EN `our highest levels of feature access and Meta Business Agent capacity for teams managing at scale` | C |
| 8 | **R1新** | §2 p3 | 「**Advanced 以上**再加上更多回覆則數」 | EN 只在 Advanced 寫 `even more Meta Business Agent responses`；Expert／Max 寫的是 `capacity`。FR 同樣只在 Advanced 寫 `un nombre encore plus important de réponses` | **X** |
| 9 | R1新 | §2 p3 | 「這次公告把這項額度列在收費的商家方案裡」 | EN 三階商家方案都列了 Business Agent | C |
| 10 | R1改 | §2 p3 | 已刪掉 2026-08-19 那則公告的事實，改用公告自己的字 | 全段已無 `sources[]` 以外的事實 | C |
| 11 | R1改 | §2 p3 | 「讓客服代理不分日夜回覆顧客」 | EN `respond to customers day and night` | C |
| 12 | R1改 | 表格 | 單一產品列 2.99／3.99 不寫「起」 | EN `WhatsApp Plus ($2.99/mo)`、`Instagram Plus ($3.99/mo)`、`Facebook Plus ($3.99/mo)` | C |
| 13 | R1改 | 表格 | 個人組合列 7.99／19.99 不寫「起」 | EN `Core ($7.99/mo)`、`Premium ($19.99/mo)` | C |
| 14 | R1新 | 表格 caption | 「創作者與商家四階原文標的是 starting at，其餘是公告直接標示的月費」 | EN 四階皆 `starting at`，五個單價皆 `($X/mo)` | C |
| 15 | R1改 | §4 p2 | 「**名列**最主要的訂閱原因」 | EN `among the top reasons`；FR `figurent parmi les principales raisons` | C |
| 16 | R1改 | §5 p1 | 「並把更多 AI 生成用量與商家客服代理額度放進付費層」（已刪「原本免費試用」） | EN 沒有寫這些原本免費試用 | C |
| 17 | R1新 | §5 p1 | 「公告的說法是核心體驗維持免費，Meta AI 的日常使用也仍然免費」 | EN `Meta AI will still be free for everyday use` | C |
| 18 | **R1新** | §5 p3 | 「想知道自己的帳號有哪些**方案與**功能可用」 | EN `To see the specific **features** available to your account` 只寫 features；同一輪改過的 FAQ2 已是「功能」 | **X** |
| 19 | R1新 | FAQ2 | 「要知道自己的帳號有哪些功能可用，官方寫的做法是開始訂閱流程來查看」 | 同上 | C |
| 20 | R1改 | FAQ2 | 「但**同一頁**也寫明」 | `may vary` 在正文倒數第二段，`now available globally` 在「How to Get Started」開頭，確非同段 | C |
| 21 | **R1改** | FAQ2 | 「價格、權益與供應情形**會**因地區、App 與帳號而異」 | EN `may vary`；summary 第三條與 §3 p2 都寫「可能」，只有這裡把情態動詞刪掉 | **X** |
| 22 | R1新 | FAQ4 | 「單一產品與個人組合方案則是直接標一個月費」 | EN 五個單價皆 `($X/mo)` | C |
| 23 | R1新 | FAQ4 | 「公告本身沒有列出更高階的完整定價區間，只寫方案、權益、價格與供應可能因地區、App 與帳號而異」 | EN 未印區間；唯一理由是 `may vary by region, by app, and by account` | C |
| 24 | R1改 | §1 p2／FAQ6 | Instagram 內建 AI 工具的「使用」（非「使用次數」） | EN `more use of in-app AI tools like Restyle on Instagram` | C |
| 25 | R1改 | 第二段 | 已刪查證流水帳，只剩查核日、無實測、不給訂閱建議 | DELTA-4-7 第 14 條 | C |
| 26 | R1改 | §3 p2 | 「頁首摘要欄位的措辭又是逐步推出，跟正文的現已全球提供不是同一句話」 | Takeaways `rolling out gradually` 對正文 `now available globally` | C |
| 27 | R1改 | §3 p3 | 「這只代表這一則公告沒有寫台灣，不等於台灣訂不到」 | EN `Taiwan` 0 次；否定句已限縮 | C |
| 28 | R1改 | §3 p3 | 「把美元數字換算成新台幣不會是台灣的售價」 | EN／FR 價格不成換算關係 | C（幣別用字改，見裁定 2） |
| 29 | R1改 | §4 p2／§4 p3 | 已刪兩句編務說明，預告三項事實未動 | 逐句比對 EN | C |
| 30 | R1改 | §5 p2 | 「Muse 模型本身的能力，站上另一篇也寫過」 | 編務用語已改成讀者看得懂的說法 | C |
| 31 | 抽查 | title／description | 台灣價格沒有寫 | EN／FR `Taiwan` 各 0 次 | C |
| 32 | 抽查 | description | 事件日 2026-09-15 | JSON-LD `datePublished 2026-09-15T15:00:59+00:00` | C |
| 33 | **抽查** | description | 「價格與供應官方寫明因地區而異」 | EN `may vary` 的 **may 被刪成肯定句** | **X** |
| 34 | 抽查 | 第一段 | 事件日＝slug 尾碼＝`news_date`＝2026 年 9 月 15 日 | 三者一致；NR 卡片 published 同日 | C |
| 35 | 抽查 | 第一段／§2 | 兩種個人組合、四種創作者及商家 | EN 逐行列名 Core／Premium、Essential／Advanced／Expert／Max | C（見待決 2） |
| 36 | 抽查 | 第二段 | 查核日 2026 年 9 月 23 日 | 三條 source、研究紀錄、正文、表格 caption、圖說六處一致 | C |
| 37 | 抽查 | 第二段／FAQ5 | 9 月 16 日又改過一次、沒有編輯說明 | `dateModified 2026-09-16T20:22:09+00:00`；NR 卡片 `updated` 印 September 16, 2026；全頁無編者註 | C（見待決 4） |
| 38 | 抽查 | summary 1 | 2026-09-15 宣布、三個舊方案、兩種個人組合＋四種創作者商家 | EN 三個小標 | C |
| 39 | **裁定** | summary 1 | 「Facebook、Instagram、WhatsApp 與 Meta AI 的核心體驗」 | 被引句（正文與 Takeaways）寫的是 `across our apps`；四個 App 只出現在 NR 的摘要，而同一頁另提 Messenger、Edits | **X** |
| 40 | 抽查 | summary 2 | 單一產品 2.99 起／個人組合 7.99 起／創作者商家 14.99 起 | EN `start at just $2.99 … $7.99 … $14.99`（分組層級的起始價） | C |
| 41 | **裁定** | summary 2／表格標頭／表格 caption／正文 | 把 `$` 寫成「美元」 | EN 全文 `USD` 0、`dollar` 0、`currency` 0；只印 `$` | **X** |
| 42 | 抽查 | summary 3 | 「現已在全球提供」＋「可能因地區、App 與帳號而異」＋「逐步推出」三句並存 | EN 正文＋EN Takeaways | C |
| 43 | 抽查 | summary 4 | 超過 50 項功能、1,500 萬份訂閱與試用，未拆分 | Takeaways 逐字 | C |
| 44 | 抽查 | §1 p1 | 引文 `The core experience … that's not changing.` | 逐字命中 | C |
| 45 | 抽查 | §1 p2 | 訂閱解鎖更專門的功能與更多 AI 用量 | EN `Subscriptions unlock more specialized capabilities and expanded AI usage…` | C |
| 46 | 抽查 | §1 p2 | 建立與編輯圖片、Muse 模型生成影片 | EN `creating and editing images and generating videos powered by Muse models` | C |
| 47 | 抽查／**裁定** | §1 p3 | 三個方案今年稍早就已推出；留存表現強勁、沒有數字 | EN `Earlier this year, we launched Meta One single product plans…`／`These plans are seeing strong retention` | **X**（「併品牌」框架，見第 8 節） |
| 48 | 抽查 | §2 p1 | WhatsApp Plus 2.99、IG／FB Plus 各 3.99、Core 7.99、Premium 19.99 | EN 五行逐一命中 | C |
| 49 | 抽查 | §2 p2 | 四階都標 starting at；Essential 14.99／Advanced 49.99／Expert 149／Max 499 | EN 四行逐一命中 | C |
| 50 | 抽查 | §2 p2 | 防冒名保護與驗證徽章「須先通過驗證才會啟用」 | EN `(pending successful verification)` | C |
| 51 | 抽查 | §3 p1 | 引文 `Meta One plans are now available globally…`、小標「How to Get Started」 | 逐字命中、小標存在 | C |
| 52 | 抽查 | §3 p2 | 引文 `Plans, benefits, pricing, and availability may vary…` | 逐字命中 | C |
| 53 | 抽查 | §3 p3 | 公告全文沒有 Taiwan，也沒有列出任何國家或地區名單 | EN `Taiwan` 0 次、無地區清單 | C |
| 54 | 抽查 | §3 p3 | 法文版 Core 6.99 歐元／Premium 20.99 歐元，高低順序翻轉 | FR `Core (6,99 €/mois)`、`Premium (20,99 €/mois)`（另：Essential 16,99 €、Expert 169 €、Max 549 € 也全部高於英文版，翻轉更明顯） | C |
| 55 | 抽查 | §4 p1 | 規模數字寫在正文前方獨立的摘要欄位 | DOM 位置已驗：`highlights-container` 551,066 < `entry-content` 552,290 | C |
| 56 | 抽查 | §4 p1 | 引文 `Meta One plans are rolling out gradually…`；不能當付費人數 | 逐字命中；EN 未拆分 | C |
| 57 | 抽查 | §4 p2 | 早期測試中超過一半的訂閱者同時使用 AI 與表達功能；沒有樣本數 | EN `In early testing, more than half of subscribers engaged with both…` | C |
| 58 | 抽查 | §4 p3 | WhatsApp Plus 備份與 Focus Schedules、Edits Plus 與 Edits 助理都是預告 | EN `will soon test`／`soon we'll bring`／`the upcoming Edits assistant` | C |
| 59 | **抽查** | §4 p3 | 「擴展到 Edits **與** AI 眼鏡」 | EN `will expand to Edits, AI glasses, **and more** over time`——`and more` 被刪，兩個例子被寫成全部 | **X** |
| 60 | 抽查 | FAQ3 | 1,500 萬原文逐字、不是付費人數 | Takeaways 逐字 | C |
| 61 | 抽查 | callout／topics | 只有一個 callout、不帶 finance、沒有投資免責、沒有訂閱建議與比價 | `ai.md`；`topics` 為 ai／software／ai-news | C |
| 62 | 抽查 | 兩個結尾連結 | text 與目標 pack 的 zh-TW `title` 逐字相同 | 程式比對：索引與 `ai-news-meta-muse-spark-20260408` 皆 SAME | C |

（另有兩處依附改動：圖說與研究紀錄 `diagram.caption` 的 `may`、研究紀錄 `verified_facts` 24 自己的敘述，列在第 3 節。）

## 3. 改掉的 11 處

### 協調者裁定的 3 處

1. **summary 第一條**（裁定 1）`官方表示 Facebook、Instagram、WhatsApp 與 Meta AI 的核心體驗一直是免費的`
   → `官方表示 Meta 旗下的 App 與 Meta AI 的核心體驗一直是免費的`。
   被引的那一句在正文與 Takeaways 寫的都是 `across our apps`；四個 App 的名字只出現在新聞總覽頁對這一則的摘要裡，
   而同一頁還提到 Messenger 與 Edits，`our apps` 的範圍比四個大。（EN／NR）

2. **表格價格欄標頭**（裁定 2）`官方標價（每月，美元）` → `月費（$）`。
   今天重抓全文 `USD` 0 次、`dollar` 0 次、`currency` 0 次，公告只印 `$`；標頭直接寫「美元」等於把推論寫成事實，
   而且與同一格 caption 自己寫的「未附幣別代碼」互相矛盾。（EN）

3. **表格 caption**（裁定 2）`金額為官方所印的美元數字（未附幣別代碼）`
   → `金額照公告所印；公告只印 $ 這個符號，沒有寫是哪一種幣別。`（caption 改後 113 字，上限 200。）（EN）

   裁定 2 的「不可把美元寫成事實」本輪**一併套用到全篇**：改前全文 23 次「美元」，其中
   summary 第二條、§2 p1（四個價）、§2 p2（四階）、§3 p1 的引文中譯、§3 p3 的英法對照、§5 p3、FAQ4 的提問
   都把 `$` 直接寫成「美元」。全部改成公告自己印的 `$2.99`／`$3.99`／`$7.99`／`$19.99`／`$14.99`／`$49.99`／`$149`／`$499`，
   **改後全篇 0 次「美元」**，標頭、正文、summary、FAQ 四處不再互相矛盾。歐元不動：法文版印的 `€` 只對應一種幣別。
   研究紀錄 `not_said` 2 原本允許「加註後可寫美元」，裁定比它嚴，本輪照裁定。

### 事實類的 8 處

4. **§2 p3**（第一輪新寫的句子）`Advanced 以上再加上更多回覆則數`
   → `Advanced 那一階再加上更多回覆則數`。公告只在 Advanced 那一階寫
   `Plus, even more Meta Business Agent responses.`；Expert 與 Max 寫的是
   `our highest levels of feature access and Meta Business Agent capacity`——是 capacity，不是 responses。
   「以上」把只對一階說的話推到三階。法文版同樣只在 Advanced 寫
   `un nombre encore plus important de réponses`。（EN／FR）

5. **§5 p3**（第一輪改過的句子）`想知道自己的帳號有哪些方案與功能可用`
   → `想知道自己的帳號有哪些功能可用`。原文是
   `To see the specific features available to your account, start the subscription process.`——只寫 features。
   第一輪已把 FAQ2 改成「有哪些功能可用」，正文這一句漏改，同一篇兩處說法不一致。（EN）

6. **FAQ2**（第一輪改過的段落）`價格、權益與供應情形**會**因地區、App 與帳號而異`
   → `……**可能**因地區、App 與帳號而異`。原文是 `may vary`；summary 第三條與 §3 p2 都寫「可能」，
   只有 FAQ2 把情態動詞刪成肯定句。（EN）

7. **description** `價格與供應官方寫明因地區而異` → `價格與供應官方寫明可能因地區而異`。同上；
   改後 description 170 字，仍在 120–200 之間。（EN）

8. **圖說＋研究紀錄 `diagram.caption`** `價格與供應官方寫明因地區、App 與帳號而異`
   → `……官方寫明可能因地區、App 與帳號而異`。同上；兩邊一起改，維持逐字一致（checker 會比對）。（EN）

9. **§4 p3** `公告寫功能未來會擴展到 Edits 與 AI 眼鏡`
   → `公告寫功能未來會擴展到 Edits、AI 眼鏡等`。原文是
   `will expand to Edits, AI glasses, and more over time`，`and more` 被刪掉，兩個例子被寫成完整清單。（EN）

10. **§2 p3 的行文**（依附第 4 點）`Advanced 再加上` 讀起來會被誤接成上一句的延續，定稿寫成
    `Advanced 那一階再加上更多回覆則數`。

11. **研究紀錄 `verified_facts` 24 自己的白話敘述**
    `Instagram 的 Restyle 與語音效果是最常被提到的訂閱原因`
    → `……名列最主要的訂閱原因（原文是 among the top reasons，不是最高級）`。
    那一條的 `verbatim_quote` 是對的，錯的是紀錄自己的敘述——**第一輪在內容包改掉的那句最高級就是照它寫的**，
    不改這裡，下一個讀這份紀錄的人還會再犯同一個錯。（EN）

## 4. 查過而且正確、本輪未動的部分

- **第一輪四處動到論述的改動全部成立**：§1 p1 補上 Takeaways 的未來式（`will stay free`，法文版 `restera gratuite` 佐證）、
  §2 p3 刪掉 2026-08-19 那則不在 `sources[]` 的公告、表格拿掉五個固定月費的「起」、
  §5 p1 把免費界線改寫成 `Meta AI will still be free for everyday use`——四處逐句回一手來源都對。
- **`verbatim_quote`**：35 條連續字串比對全部命中，0 條落空，沒有拼接引文；內容包 4 段英文引文也逐字通過。
- **但書與限定詞**：本輪沒有為了字數刪掉任何但書；相反地補回三處 `may`（description、FAQ2、圖說）與一處 `and more`。
  `starting at`、`(pending successful verification)`、`In early testing`、`to-date`、`will／soon／upcoming`、
  `more than half`、`among the top reasons` 全部在位。
- **字數**：正文 2,884 字（上限 3,000），比第一輪的 2,902 少 18 字，離上限還有 116 字——幣別改寫省下的空間
  正好吸收了補回的限定詞。五節各三段不變。
- **`summary` ⊆ 正文、FAQ 答案 ⊆ 正文、圖上數字**：summary 的 10 個數字全部在正文；
  `diagram.nodes` 四格（核心體驗／單一產品方案／個人組合方案／創作者與商家）不含任何數字，四格文字都在正文出現。
- **日期一致性**：slug 尾碼 `20260915`＝`news_date`＝正文第一段「2026 年 9 月 15 日」；
  `checked_on` 2026-09-23 在三條 source、研究紀錄、正文第二段、表格 caption、圖說六處一致，本輪重抓同日、未改。
- **界線（`ai.md`）**：沒有購買、升級、續訂或退訂建議；沒有與 ChatGPT／Gemini 或任何服務比價；沒有台幣換算；
  沒有推定台灣可用或不可用；廠商宣稱（留存表現強勁、超過一半的訂閱者、50 項功能與 1,500 萬、各方案效益）全部有歸因；
  只有一個 callout、不帶 `finance` 主題、沒有投資免責段落。`meta.com` 方案頁全篇 0 次提及。
- **歸因密度**：沒有任何一段出現三個以上的「X 表示／依 X 公告」式歸因；「公告沒有寫……」這類是規格要求的限縮否定句，
  不是裝飾性歸因。全篇 0 次「本文」。
- **兩個結尾連結**：程式比對 text 與目標 pack 的 zh-TW `title` 逐字相同，兩個目標 pack 都存在，本輪未動。

## 5. 留給協調者／站主的事

1. ~~**「把原本分開的三個方案併入同一品牌」這個框架**（出現在 description、第一段、summary 第一條、§1 p3 四處）。~~
   **已由協調者 2026-09-23 裁定並改完，見第 8 節。**
2. **「兩種個人組合方案與四種創作者及商家方案」是分組清點數**，公告沒有印。`must_not_write` 13 禁的是總數
   （例如「九個方案」），而四階在公告裡逐行列名，本輪維持；若認為連分組數都要避開，§2 兩段與第一段要一起改。
3. **§2 p3 把 `more access to Meta Business Agent` 譯成「更多 Meta Business Agent 額度」。**
   公告對 Essential 寫 `more access`、對 Expert／Max 寫 `capacity`（容量），兩個詞不同；本輪認為「額度」讀得通而未改，
   要更貼字面可改成「更多 Meta Business Agent 的使用權限」。
4. **「9 月 16 日又改過一次」用的是頁面印出的美西日期。** `dateModified` 換算台北是 9 月 17 日 04:22。
   研究紀錄 `must_not_write` 7 與 `unverified_or_excluded` 3 明文指定寫法就是「9 月 16 日」（照頁面印的 `<time class="updated">
   September 16, 2026`），本輪照紀錄維持；事件日不受影響，仍是 9 月 15 日。
5. **摘要的「起」與表格的固定月費並存**：summary 第二條與 §3 p1 照「How to Get Started」那一句寫分組起始價（`start at just`），
   表格照每個方案自己標的價寫，FAQ4 負責解釋兩者的差別。三處都對，但讀者若只看表格會覺得與摘要不一致——若要再明確，
   只能在 summary 第二條加字，會吃掉正文剩下的 41 字餘裕。
6. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 仍沒有這個 slug，本輪照 DELTA-4-7 第 15 條沒有跑 `--assets`。
   圖說與研究紀錄 `diagram.caption` 本輪一起改過（補 `may`），目前仍逐字一致，之後改任一邊都要同步。

## 6. 自檢輸出（原樣）

```
OK ai-news-meta-one-subscription-20260915 zh-TW paragraphs 2959
check_article exit=0
```

```
ai-news-meta-one-subscription-20260915
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

兩個 log 檔：`_out/fc2_check_ai-news-meta-one-subscription-20260915.log`、
`_out/fc2_lint_ai-news-meta-one-subscription-20260915.log`。
lint 只剩規格允許的 `image_missing`（圖還沒畫）與 `raw_internal_url`（還沒 relink），與第一輪相同。

## 7. 結論

`ok`。覆核 62 條、改 11 處，其中 8 處是事實類（`Advanced 以上`、`方案與功能`、三處被刪掉的 `may`、
`and more`、行文一處、研究紀錄自己的最高級敘述），3 處是協調者裁定（`our apps`、表格標頭、幣別）。
沒有 NOT FOUND，沒有一句掛在讀不到的來源上，字數與界線都在規格內。
留給站主的只有第 5 節第 1 項（「併入同一品牌」的框架）需要決定，其餘五項是可選的收斂。

## 8. 追加：協調者裁定「併品牌」框架（2026-09-23，第二輪交件後）

第 5 節第 1 項的待決事項，協調者裁定照公告原文改寫：**單一產品方案今年稍早就以 Meta One 的名字推出，
這次公告新增的是個人組合方案與創作者商家方案**。依裁定改了五處（內容包四處＋研究紀錄一處）。

| # | 位置 | 改前 | 改後 |
| --- | --- | --- | --- |
| 1 | `description` | 將 Instagram Plus、Facebook Plus、WhatsApp Plus **併入同一品牌**並新增個人與商家方案 | Instagram Plus、Facebook Plus、WhatsApp Plus **今年稍早就以 Meta One 單一產品方案推出**，這次在同一個名字下新增個人組合與商家方案 |
| 2 | 第一段 | 把原本分開的 Instagram Plus、Facebook Plus、WhatsApp Plus 三個方案**併入同一品牌**，再加上兩種個人組合方案與四種創作者及商家方案 | Instagram Plus、Facebook Plus、WhatsApp Plus **今年稍早就以 Meta One 單一產品方案推出**，這次在同一個名字下新增兩種個人組合方案與四種創作者及商家方案 |
| 3 | summary 第一條 | 把 Instagram Plus、Facebook Plus、WhatsApp Plus **三個舊方案併入同一品牌**，並新增兩種個人組合與四種創作者及商家方案 | 同上句型 |
| 4 | §1 p3 | 三個方案今年稍早就已推出，**這次是併入 Meta One 這個品牌**，再疊上個人與商家的組合方案 | ……今年稍早就以 Meta One 單一產品方案推出，**公告原文寫的是 `Earlier this year, we launched Meta One single product plans`**，這次新增的是個人組合方案與創作者商家方案 |
| 5 | 研究紀錄 `summary` | 把原本分開賣的……**併進同一個品牌**，再往上加兩種個人組合方案（Core、Premium）與四種創作者／商家方案 | ……今年稍早就以「Meta One 單一產品方案」的名義推出（附公告原文），這次是在同一個名字下新增兩種個人組合方案與四種創作者／商家方案 |

依據：主來源 `Earlier this year, we launched Meta One single product plans — Instagram Plus, Facebook Plus, and
WhatsApp Plus`（研究紀錄 `verified_facts` 22，本輪已逐字命中）。這一頁沒有描述任何「改名／併品牌」的動作，
原本的寫法是推論。§1 p3 順手刪掉「公告也提醒讀者」這個歸因，讓新增的「公告原文寫的是」不會讓該段變成三次歸因；
全篇沒有再出現「併入同一品牌」「併進同一個品牌」「三個舊方案」。

**改後數字**：正文 2,959 字（上限 3,000，剩 41 字；裁定的改寫淨加 75 字）、`description` 197 字（上限 200）。
自檢重跑：

```
OK ai-news-meta-one-subscription-20260915 zh-TW paragraphs 2959
check_article exit=0
```

```
ai-news-meta-one-subscription-20260915
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

研究紀錄 `factcheck.second_round.changes` 已補上這一條（共 12 條），`open_questions` 第一項標記結案。
結論不變：`ok`。第 5 節剩下的五項都是可選的收斂，沒有待決事項。
