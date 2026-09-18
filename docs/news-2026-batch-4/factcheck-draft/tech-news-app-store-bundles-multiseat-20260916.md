# 獨立查核：tech-news-app-store-bundles-multiseat-20260916

查核日 2026-09-18。約 95 條主張逐條對照四個官方網址的正文，改了 16 處。
所有請求都用 `curl -sL -A "Mokaair-editorial"`，沒有任何 email、姓名或個人資料進入 UA、標頭、查詢字串或表單。

## 重抓結果（三條 sources 都還在、內容沒變，另外補進第四條）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| developer.apple.com/news/?id=likeohx4 | 200 | 117,728 | 是，2,869 字正文 | 日期行 September 16, 2026；兩個小節（Request access to Bundles and Suites／Multiseat purchasing enabled in App Store Connect）；Starting today 那句；Volume Purchasing launches on October 22, 2026 那句；Suite 的 from a single developer |
| developer.apple.com/app-store/subscriptions/bundles-and-suites/ | 200 | 115,481 | 是，5,238 字正文 | Up to five developers；同週期規定；**Request access and submit for review** 標題；Multi-Developer Bundle Program Legal Addendum；confirming your pricing and go-live date；**Q&A 三題**（5 個訂閱／15 個 App、既有訂閱升級與按比例退款、下個續訂日生效） |
| developer.apple.com/help/.../manage-purchase-options-for-auto-renewable-subscriptions | 200 | 370,868 | 是，4,582 字正文 | September 14, 2026 那句（**or**，不是 and）；group purchaser 定義；自訂 App 不能退出；turn them on at any time；關閉後果（Apple 自己有逗號接句的錯字，照抄） |
| 同一頁的 **/tw/** 版本〈管理自動續訂型訂閱的購買選項〉 | 200 | 370,996 | 是，1,816 字正文 | **本次新增的第四條 source。**多名額購買／名額／群組購買者／Apple 商務／Apple 校務管理／大量採購等官方繁中用詞；「家人共享」和多名額購買整節 |

另外測過但沒進 sources：`/tw/news/?id=likeohx4` → 404（81,990 bytes 軟 404）、
`/tw/app-store/subscriptions/bundles-and-suites/` → 404（82,022 bytes）、
`/cn/news/?id=likeohx4` → 200（118,619 bytes，完整簡體中文版）。

## 改掉的 16 處

**1. 「三個頁面都只有英文版、/tw/ 網址回傳 404」是錯的（第二段）。**
原文這樣寫，是拿公告那一個 /tw/ 網址的 404 推論到三頁。今天逐一測：公告的繁中網址確實 404，
Bundles 頁的繁中網址也 404，但**說明頁的 /tw/ 回 200，而且是完整翻譯**，標題〈管理自動續訂型訂閱的購買選項〉；
公告另有完整的簡體中文版。第二段改成逐頁交代，並把該頁加為第四條 source。

**2. 全篇用詞改用 Apple 自己發布的繁體中文（連帶改了 title）。**
既然繁中說明頁存在，`BRIEF.md`「介面名稱對照各語言的官方說明頁，不要自己翻」就適用。
Apple 繁中頁寫的是 **多名額購買**（multiseat purchases）、**名額**（seat）、**群組購買者**（group purchaser）、
**自動續訂型訂閱**、**「Apple 商務」**、**「Apple 校務管理」**、**大量採購**、**以群組形式購買**。
原稿自創的多人席次購買／席次／團體購買人／量購／團體購買全部換掉。
Bundle 與 Suite 沒有任何中文官方頁（簡中公告連到 Bundles 頁時自己標「(英文)」），
所以組合方案／套組維持本站翻譯，並在第二段寫明哪些是 Apple 的、哪些是本站的。

**3. 9 月 14 日那兩個條件的中文會被讀成「兩個都要」。**
原文「沒有使用 StoreKit 2 或開啟家人共享」在中文裡可以解成「沒有（使用 StoreKit 2 或開啟家人共享）」。
來源是 `Subscriptions created prior to September 14, 2026 that do not use StoreKit 2 **or** that have Family Sharing turned on are set to opted out by default.`
——兩個獨立條件、符合其一即可。正文、summary、FAQ 三處都改成
「只要未使用 StoreKit 2、或是開啟了家人共享，兩個條件符合其中一個」並加一句「不是要兩個條件同時成立」。

**4. 家人共享：兩個官方語言版本說法相反，原稿只看了英文版。**
英文頁：`only the group purchaser's access will include Family Sharing`（兩者可同時開啟）。
繁中頁多了一整節，寫「開啟家人共享會自動關閉多名額購買」「『家人共享』無法與多名額購買同時啟用」，
而且「所有開啟『家人共享』的現有訂閱，Apple 會自動關閉其多名額購買功能」。
比對確認：英文頁 `Family Sharing and multiseat` 出現 0 次，繁中頁「9 月 14 日」出現 0 次。
第四節加一段寫出兩版差異並註明本文以英文版為準。兩份研究紀錄原本都說「官方沒說兩者能不能並存」，那是錯的。

**5. 漏掉自訂 App 這個例外（第四節）。**
原稿寫「開發者若不想要就到 App Store Connect 關掉」，沒有但書。
來源：`Managing purchase options is not available for subscriptions in custom apps. … you may not opt out of multiseat purchases.`
已補「自訂 App 甚至沒有選擇……不能停用多名額購買」。

**6. 漏掉兩個官方有印的數量上限（第二節、表格、FAQ 1）。**
Bundles 頁 Q&A：`You can include up to 5 subscriptions in a Bundle. A Suite can provide a subscription across up to 15 apps.`
原稿完全沒提，讀者很容易把「最多五個開發者」誤當成訂閱數上限。已補「最多放五個訂閱」「最多可橫跨十五個 App」。

**7.「不管是組合方案還是套組，都可以只保留其中一項」放大了來源（第二節）。**
Bundles 頁的部分保留只寫在 Bundle 上（`Rather than cancelling an entire Bundle, subscribers also have the option to keep one or more individual subscriptions included in the Bundle.`），
Suite 只寫得到整個取消。已改成「取消整個組合方案或套組；只保留其中一兩項這個選擇，官方只寫在組合方案上」。

**8. 漏掉生效時點這個限定詞（第二節、表格、FAQ 2）。**
`Any cancellations or partial changes will take effect at the next renewal date. Upgrades take effect immediately…`
原稿只寫「隨時調整」，讀起來像立刻生效。已補「取消與部分變更於下一個續訂日生效，升級則立即生效」，
表格「事後調整」列的「官方未說明期限」改成「下一個續訂日生效」。

**9. 表格「套組｜僅限單一開發者」是來源沒說的否定句。**
Apple 只把 Suite **定義**成 `a set of apps from a single developer`，沒有寫「不得跨開發者」。
改成「同一開發者，最多十五個 App」，FAQ 1 也改成「官方把套組定義在同一個開發者之內」。

**10.「公告裡唯一給出的確定日期」是絕對否定句（第三節）。**
公告的日期行 September 16, 2026 本身就是日期。改成「公告正文只寫出一個明確的未來日期」。

**11.「三個頁面都沒有提到任何地區、國家或商店前台」與本文自己的第三節打架。**
說明頁明明有 App Store／Apple 商務／Apple 校務管理三個銷售管道，第三節也寫了。
改成只講國家與地區，並補一句「那是管道，不是地區」。逐頁比對過：四頁正文的
Taiwan／台灣／country／region／storefront／國家／地區全部 0 次，所以「沒有國家或地區」這句站得住。

**12.「價格……同樣沒有寫」太寬（第五節）。**
Bundles 頁其實寫了 `confirming your pricing and go-live date`。
改成「沒有公布」＋「Apple 只說通過申請後會與開發者確認定價，沒有任何金額」，
並補上每個組合方案各自談上線日這件事（也解釋了為什麼官方只肯說「今年稍晚」）。

**13. 漏掉多開發者組合方案的兩道額外門檻（第一節、第五節、FAQ 5）。**
`Each participating developer will need to sign the Multi-Developer Bundle Program Legal Addendum…`
已補「每個開發者各自送件，並簽署多開發者組合方案計畫法律附約」，
第五節也說明分潤問題官方沒答、附約內容未公開。

**14.「多人席次購買有一半當天生效」是編輯發明的比例（第一節、callout）。**
來源只說開發者端的預設開關當天生效。改成「開發者端的設定在公告當天就已經生效」。
同段「開發者不需要另外申請」是來源沒說的否定句，改成「公告沒有像組合方案那樣要求送件申請」。

**15. 兩條 `verbatim_quote` 的不斷行空格位置是錯的，等於搜尋不到。**
第 3 條寫 `With` + U+00A0 + `Suites`，但該頁是普通空格；第 11 條寫 `Volume` + U+00A0 + `Purchasing`，
但那一句也是普通空格（同一頁的另一句才是 U+00A0）。
把研究紀錄 30 條引文全部拿去對存下來的頁面做精確子字串比對，現在 30/30 通過。

**16. 台灣用語與兩個研究紀錄裡的錯誤否定句。**
正文「訪問權」改掉（該詞是中國用法，已改寫成「共用創作工具的協作者」）、「續約」→「續訂」、「計費週期」→「期間長度」。
研究紀錄 `not_said` 兩條被來源推翻、已改寫並標明：
（a）「官方沒說既有單獨訂閱者能不能轉成組合方案、剩餘期間怎麼算」——Q&A 明明寫了立即升級＋按比例退款；
（b）「官方沒說家人共享與多名額購買能不能並存」——見第 4 點。
`editorial_brief` 原本說保留訊息 API 是「公告裡第三個項目」，其實它在 Bundles 頁，不在公告裡，已更正。

## 查過而且正確的部分（沒有動）

- **Suite 與 Bundle 的定義沒有混寫**：Suite ＝一個訂閱通用同一開發者的一組 App，來源是公告自己那句
  `With Suites, people get access to a single subscription that seamlessly works across a set of apps from a single developer.` 撰稿的處理是對的。
- **`Request access and submit for review` 確實在 Bundles 頁、確實不在公告頁**（兩頁都搜過）。
  前期研究把它掛在公告網址是錯的，撰稿已改掛 Bundles 頁，覆核通過。
- **9 月 14 日的條件確實是 or**，而且確實與「對所有自動續訂型訂閱預設開啟」並存；原稿邏輯沒錯，只有中文寫法有歧義。
- **2026-10-22（大量採購）與 this winter（群組購買）在公告同一句**；說明頁那句更籠統的「今年稍晚」在另一頁，兩者掛的頁面都正確。
- **保留訊息 API 全篇沒有任何一句提到**：整包搜尋「保留訊息」「retention」「Retention」「挽留」「取消前」全部 0 次。
- 三條原 sources 今天都回 200 且拿到真正的正文，沒有轉址殼、軟 404 或擋阻頁。
- `checked_on` 2026-09-18 在四處一致（每條 source、研究紀錄、第二段、表格與圖解 caption），且就是撰稿者實際讀到來源那天，**未更動**。
- 界線：沒有購買建議、沒有推薦式比價、沒有投資免責 callout（科技垂直不帶）、只有一個 callout；
  Apple 的示範案例與受眾說法都標成「Apple 官方示範」「Apple 自己舉的情境」。
- `news_date`、slug 日期後綴、第一段日期三者都是 2026-09-16，與 `event_date` 一致。
- 簡體字 0 個；圖解四格的文字與數字都出現在正文。

## 留給站主的 5 件事

1. **用詞決定要拍板。** 本文改用 Apple 發布的繁中詞（多名額購買／名額／群組購買者／大量採購／群組購買／
   Apple 商務／Apple 校務管理），**title 因此改了**，索引條目要重新對齊，已經排定的主圖或圖解文字也要跟著改。
2. **四語翻譯要從新用詞出發，而且 zh-CN 不能照搬繁中詞。** Apple 自己的簡體用詞是
   套装／套件／多席位购买／席位／批量购买／群组购买／Apple 校园教务管理。
3. **Apple 自己前後不一致。** 同一份說明頁的英文版與繁中版，在家人共享能否與多名額購買並存這件事上說法相反，
   繁中版還少了 9 月 14 日那個日期。本文兩邊都寫出來並聲明以英文版為準；Apple 之後若修好，第四節末段與 FAQ 最後一題要重看。
4. **sources 從三條變四條**（多了同一份說明頁的繁中版），因為正文現在引用了它的內容。仍在 2–4 條的規定內，但請確認要不要保留。
5. `hero.alt` 依規格沒有動（協調者會依實際畫面改寫）；第二個結尾連結的文字照抄 `tech-news-apple-att-eu-20260916` 的現行標題，也沒有動。

## 自檢

```
OK tech-news-app-store-bundles-multiseat-20260916 zh-TW paragraphs 2994
```

## 結論

`needs_second_round`。改了 16 處事實，其中第 1、2、4 點動到骨幹：
文章的來源狀態描述、全篇專有名詞（含 title）與第四節的論述都變了。
建議第二輪看三件事：新用詞在五個語系的一致性、第四節那段語言版本差異的寫法，以及第四條 source 要不要留。

## 第二輪

查核日 2026-09-18（同一天）。範圍是第一輪改過的每一段與新寫進去的每一句，
加上指派訊息點名的六個疑點，約 62 條主張，又改了 12 處。
四條 sources 全部用 `curl -sL -A "Mokaair-editorial"` 重抓，沒有任何 email、姓名或個人資料
進入 UA、標頭、查詢字串或表單。

### 重抓結果（四條全部 200，位元組數與前兩次完全相同）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| developer.apple.com/news/?id=likeohx4 | 200 | 117,728 | 是（日期行 September 16, 2026、兩個小節都在） |
| .../app-store/subscriptions/bundles-and-suites/ | 200 | 115,481 | 是（含 Q&A 三題全文） |
| .../help/.../manage-purchase-options-for-auto-renewable-subscriptions | 200 | 370,868 | 是 |
| 同一頁 **/tw/** 版 | 200 | 370,996 | 是（含「家人共享」和多名額購買整節） |

另外測了八個本地化網址（都不進 sources）：公告 `/cn/` 200、`/jp/` 200（標題
〈iOS 27に向けたサブスクリプションの準備〉）、`/kr/` 200、`/tw/` 404；
Bundles 頁 `/tw/`、`/cn/`、`/jp/` 全部 404；說明頁 `/cn/` 200。

### 引文機械比對

研究紀錄原有 30 條 `verbatim_quote`，今天對重抓的頁面做精確連續子字串比對：**30/30 通過**，
第一輪修掉的兩個不斷行空格沒有回退。本輪新增 3 條（見下），現在 **33/33 通過**。
每條 `url` 都在 `sources[]` 裡，內容包與研究紀錄的四條 source 完全一致、`checked_on` 四處都是 2026-09-18。

### 又改的 12 處

**1.（骨幹）第四節末段：兩版矛盾的描述本身是錯的。**
第一輪寫成「英文版說可以並存、繁體中文版說不能」。逐句讀下來不是這樣：
英文版兩次寫可以並存（`when both multiseat purchases and Family Sharing are turned on` 與
`All other seats will be for individual use only`，加上文末那則 Note），從來沒有否認過；
**繁體中文版把英文那兩句都忠實譯進去了**（「只有群組組織者具備使用「家人共享」的資格，所購買的其餘份數僅供個人使用」），
卻在同一段接著寫「系統會自動關閉其多名額購買功能」與「「家人共享」無法與多名額購買同時啟用」。
也就是說，矛盾發生在**繁中多出來的那一節與其餘內容之間**，繁中頁自己前後打架。
整段改寫：點出繁中頁自己不一致、英文版的關鍵子句逐字引出、繁中的「無法…同時啟用」逐字引出，
並把「以英文版為準」的理由換成可查證的那一個（相反的說法只出現在繁中多寫的那一節），
最後明寫「哪一版正確本文不判斷」。原本的理由（「因為 9 月 14 日那個分界只寫在英文版」）是推論，已刪；
那個事實本來就還在 FAQ 最後一題裡。

**2. 第二段「公告只有簡體中文版」是錯的。**
今天逐一測：公告的日文版（200，126,192 bytes）與韓文版（200，124,432 bytes）都在。
第一輪只測了 `/tw/` 與 `/cn/` 就下了「只有簡體中文版」的結論，是同一種以偏概全。
改成只寫實測過的語言；同時第一次測了 Bundles 頁的 `/cn/` 與 `/jp/`（都是 404），
這才真正撐得住「Bundles 頁沒有中文版」。「三頁的中文版狀況」也改成「三頁的翻譯狀況」。

**3. 表格「事後調整」那一列把「只保留一項」又放大回套組。**
第一輪在正文把部分保留限縮到組合方案，卻沒動表格；那一列坐在一張上面兩列分別是組合方案與套組的表裡，
「可保留個別項目或取消整包」讀起來就是兩者都可以。改成「組合方案可只保留部分項目，兩者都可取消整包」。
另外確認正文與 FAQ 1、FAQ 2 三處都沒有再把套組寫成可只保留一項。

**4. 第五節「另外兩個支援頁」的數字沒跟著 source 改。**
第一輪把 sources 從三條加到四條，這句留在原地。改成「另外三個官方頁」。

**5. callout 標題「三個時程」是編輯自己數的。**
callout 內文列了四個時程（今年稍晚、9 月 16 日、10 月 22 日、今年冬天）。改成「這幾個時程不要混在一起」。

**6. 第五節兩處語氣與範圍。**
「台灣也完全沒有被提到」去掉強化詞「完全」；
「不是台灣可用，也不是台灣不可用」改成「不能推論台灣可用或不可用」，守則不變，FAQ 6 也還在。

**7–12. 六處等量刪減，全部是重複敘述，沒有動任何但書、限定詞或歸因。**
第二節第三段第三次出現的四個系統全名（完整清單留在第一節、表格與 FAQ 5）、
「官方用的字是「無縫」」（FAQ 1 保留）、「沒有限定新舊」（與前一句重複）、
「避免影響顧客」後面的英文原文、「月費和年費不能包在同一個組合方案裡」→「不能混包」、
以及兩處重複的「共用創作工具」與「這幾個官方頁面」。
段落字數 2,994 → 2,996，仍在 1,800–3,000 內。

### 研究紀錄的改動

新增 3 條 `verbatim_quote`（30 → 33）：英文版那句 `when both … are turned on`（正文現在引它，原本沒有任何一條引文涵蓋）、
繁中頁自己那句可以並存的話、以及繁中頁「Apple **會**自動關閉」既有訂閱的那則注意（標明是「會」不是「已」）。
兩條 `CORRECTED` 的 `not_said` 與兩條對應的 `must_not_write` 全部重寫；
`sourcing_notes` 補上完整的本地化矩陣；`factcheck` 底下加了 `second_round`。

另外更正一件會影響翻譯的事：**群組購買不是 Apple 發布的繁中詞**。
繁中說明頁上「群組購買」出現 5 次，5 次都在「群組購買者」裡面；Apple 對這個動作用的是「以群組形式購買」。
「大量採購」則確實是 Apple 印出來的名詞（兩次）。所以本站自譯的詞是組合方案、套組與群組購買三個，
第一輪的報告與紀錄把群組購買算進 Apple 的詞裡，已更正。

### 為了反駁而讀、但沒有進 sources 的一頁

說明頁的**簡體中文版**（`/cn/`，200，370,625 bytes）是同一份文件的第三個版本，
它同樣有那一整節、同樣有自動關閉那一句，
但最後一句寫的是「你可以随时开启多名额购买，但『家人共享』不适用于多名额购买的其他名额」——
講的是其他名額，和英文版相容，**繁中那句「無法同時啟用」在三個版本裡是唯一的例外**。
這一頁沒有加進 `sources[]`（規格禁止用 sources 以外的網址替文章補事實，而且已達四條上限），
文章「以英文版為準」的理由也只建立在 sources 裡的事實上。已記進 `unverified_or_excluded`。
同一頁另外兩個 Apple 自己的問題也記下來了：簡中版同樣沒有 9 月 14 日，
而且把條件寫反成「未开启『家人共享』」。

### 查過而且正確、沒有動的部分

- 指派訊息點名要逐字核的四句全部對上：`you may not opt out of multiseat purchases`、
  `You can include up to 5 subscriptions in a Bundle. A Suite can provide a subscription across up to 15 apps.`、
  `Any cancellations or partial changes will take effect at the next renewal date.`，Q&A 三題全文都讀過。
- `this winter` 保留英文原詞，「沒有寫是哪一年或哪個半球」還在；
  「今年稍晚」「需申請審查」「預告」這些狀態詞在正文、表格、圖解四格與 callout 都還在。
- 國家與地區：四頁**正文**（去掉左側導覽與頁尾）裡 Taiwan／台灣／country／countries／region／storefront／國家／地區
  全部 0 次。繁中正文有「店面」1 次，出自「可供銷售的店面」，就是那三個銷售管道，文章已經講明那是管道不是地區。
- title 54 字（≤60）、description 188 字、簡體字 0 個、保留訊息相關字串 0 個。
- 兩個結尾連結的文字與目標都沒有動，也沒有碰 `tech-news-apple-att-eu-20260916`；`hero.alt` 依規格未動。
- `checked_on` 2026-09-18 本來就正確也一致，沒有更動。
- 界線：沒有購買建議、沒有推薦式比價、沒有投資免責 callout、只有一個 callout；
  Apple 的示範與受眾說法都有歸因。

### 留給站主的事

1. 第一輪那三件（用詞拍板、四條 source、Apple 自相矛盾）仍然成立，但**請讀更正後的版本**——
   第一輪對後兩件的描述不準確。
2. 查證屬實、但為了字數沒有寫進正文的一件事：繁中頁說 Apple **會**自動關閉所有已開啟家人共享的既有訂閱的多名額購買。
   這對台灣開發者是實際影響，引文已經在 `verified_facts` 裡，若協調者挪得出字數，它屬於第四節。

### 自檢

```
OK tech-news-app-store-bundles-multiseat-20260916 zh-TW paragraphs 2996
```

### 結論

`ok`。
