# 獨立查核：ai-news-anthropic-pace-metrics-20260917

查核代理：未參與撰稿。查核日 **2026-09-18**（與內容包、研究紀錄原本的 `checked_on` 同一天，未改動）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，主來源抽成 28,942 字純文字後逐句比對；
研究紀錄的 `verbatim_quote` 以程式做連續字串比對（同時比對可見文字與 RSC payload 解碼後的字串）。
**沒有使用 `sources[]` 以外的任何網址替文章補事實**，也沒有猜任何網址。
任何請求都沒有帶 email 或個人資料。

檢查的主張：正文 13 段每一句、summary 四句、FAQ 六題答句、callout、表格 16 格與 caption、
圖解 caption 與研究紀錄四格與 `hero_label`、title、description，約 **101 條**；
另加研究紀錄 **41 條**引文的逐字比對。**改了 12 類、共 23 處**，另有 4 件留給站主。

## 重抓結果（三條都還在，位元組數與撰稿紀錄完全相同）

| source | HTTP | bytes | 轉址 | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- | --- |
| anthropic.com/institute/measuring-pace-of-ai-development | 200 | 217,865 | 0 | 是（Next.js 頁，正文在 `<p class="…post-text">`） | 全文含附錄與兩條註腳；三項指標的每個數字、每個期間、每個限定詞 |
| anthropic.com/news | 200 | 462,587 | 0 | 是 | FeaturedGrid 區塊為本篇印 `<time>Sep 17, 2026</time>`，RSC payload 對應欄位 `"date":"2026-09-17"`；摘要句逐字相符 |
| anthropic.com/policy-on-the-ai-exponential | 200 | 140,750 | 0 | 是 | Advanced AI Framework 那一句；**全文沒有任何發布日期** |

三條都不是擋阻頁或軟性 404。風險報告 PDF 與未署日期的 `/institute/recursive-self-improvement`
都沒有進 `sources[]`，文中也沒有引用其內容——這一點撰稿者做對了。

## 改掉的 12 類（依嚴重度排序）

1. **「第三方評估者常駐是計畫，不是已經在做的事」被來源自己的句子推翻**（第 3 節第 2 段）。
   撰稿者只讀到前言的 `We plan to embed independent third-party evaluators…`，
   漏了第二節結尾的 `As described above, we are now setting up external third party evaluators at Anthropic.`
   ——**現在進行式**。已改成把兩句都寫出來（前言「計劃常駐」、第二節「目前正在建立」），
   結論維持「都不等於已經有人查核過」。連帶改了 `description`、summary 第四句、FAQ 第三題、callout
   與圖解第四格（`第三方評估者仍是計畫` → `外部評估者正在建立`）。
2. **「罕見事件」那句錯了三件事**（第 2 節第 3 段、表格第三列、FAQ 第二題）。
   原文是 `In our monitoring data to date, individual agents rarely misbehave. But when there are
   millions or billions of agents operating in the economy, even rare events can happen regularly.`
   (a) **位置**：這句在第二節開頭的 `Why measure oversight of agents?`，不在 0.002% 那一格之後，
   所以「官方緊接著提醒」不成立，已改成「官方在原文這一節的開頭先提醒」；
   (b) **規模**：`operating in the economy` 是整個經濟體，草稿寫成「代理人多到數百萬、數十億個時」，
   讀起來像 Anthropic 平台上的代理人變多，已補回經濟體；
   (c) **語氣**：`can happen regularly` 是「可能經常發生」，草稿寫「也會定期發生」——`can` 被刪掉，
   `regularly` 被讀成「定期」。同段也補回 `In our monitoring data to date`（「就目前的監控資料看」）。
3. **「這篇專文也沒有替『安全研究』訂出外部人士能套用的明確定義」是錯的**（第 5 節第 2 段）。
   附錄白紙黑字印著 `Safety work was defined as work whose dominant purpose is making AI systems
   safer, more understandable, or more secure.`，還附了分類器提示詞節錄與邊界案例。
   官方自己說的是「這只是眾多合理選擇之一，換一家開發者或主管機關可能畫在別的地方」。
   已改寫成正面陳述，並把「各家公司也應該事先談好共通定義」降回原文的
   `would benefit from converging on a shared definition`（「會有好處」）；
   「這類分類方式應該和數字一起公開、讓第三方查核」也降回 `Any frontier developer could publish…`。
4. **「同一天，Anthropic 另一份政策頁面……」的「同一天」沒有依據**（第 5 節第 2 段）。
   `policy-on-the-ai-exponential` 全文 `datePublished`／`article:published_time`／`Published` 各 0 次，
   可見文字裡沒有任何日期，唯一的 `2026-09` 字串是整站 `siteSettings._updatedAt`。已刪掉「同一天」。
   同句「提交給**各國政府**的治理提案路線圖」也改掉——同一頁另有一句
   `Our framework is written primarily with the US federal government in mind.`，
   已改成「該頁寫明這份框架主要是為美國聯邦政府而寫」。
5. **四個限定詞被刪，全部補回**：
   離線監控每週約 50 則漏了 `the highest priority flags`（已補「優先度最高的」，否則讀成隨機抽 50 則）；
   算力保守規則的 `as much as`（「一樣多」）被寫成「同時對能力提升與安全研究有貢獻」，
   那把規則放寬成任何沾到能力的都不算，已改成「一個 token 對能力提升的貢獻若和對安全一樣多」；
   `about 6%`／`about 12%` 漏了 `about`，正文與表格已補「約」；
   AL3／AL4 的定義漏掉 `can`（`it can do large chunks…`／`it can complete most of the task…`），
   那是等級的能力定義不是已發生的事，已補「能」。
6. **`compare like with like, across developers and over time` 被砍掉一半**（第 3 節第 3 段）。
   草稿寫「意義在於未來跟自己比較」，把 `across developers` 刪掉了。
   已改成「意義在於能跨開發者、跨時間做同類比較」。
7. **「官方自己列出研發自動化指數的兩個限制」誤讀了結構**（第 3 節第 1 段）。
   原文是 `Two obstacles stand in the way of cross-lab comparison on this type of reporting.`
   ——兩個障礙都掛在「跨實驗室比較」上，草稿把「不能跟其他公司比」只掛在第一個障礙。
   已改成「兩個擋在跨實驗室比較前面的障礙」。同段「評審評某個月份時只看得到……」的主體也改回原文：
   原文限制的是 `the research agents that do the ratings`，不是評審。
8. **6%／12% 的分母是 `allocated toward safety`（safety work），不是「安全研究」**。
   附錄定義的 safety work 涵蓋能力研究以外的安全相關工作，比「安全研究」寬。
   正文、表格第四列、summary 第三句三處已改成「分給安全工作」；
   只有官方確實寫 `Safety research tends to use less compute…` 的那一句保留「安全研究」。
9. **「Anthropic 在專文開頭寫道，現在外界看不到 AI 實驗室內部在發生什麼事」出處寫錯**（第 1 節第 1 段）。
   那句是**新聞總覽頁精選區塊的摘要**，不在專文裡；專文開頭是
   `AI systems are becoming exponentially more powerful…the public needs more information.`
   已改成「Anthropic 官方新聞總覽頁為這篇專文寫的摘要是……專文本身則把這件事和 Amodei 的呼籲連在一起」。
10. **AI 垂直不帶投資免責**：第二段的「也不提供投資建議」已刪除（全篇沒有任何財經內容，
    `topics` 也沒有 `finance`，這句會變成樣板免責）。
11. **FAQ 第五題「沒有給出下一次公布的日期或固定方法」後半不成立**——附錄整節就是方法論。
    已改成「沒有寫出下一次公布的日期，也沒有承諾往後會沿用同一套方法」，
    並補上原文 `we plan to rebuild the basket of tasks periodically and re-version our published
    automation numbers as appropriate`。
12. **三處小訂正**：約 3 萬個代理人做的是 `research and engineering work`（改成「研究與工程工作」，
    不是「研發工作」）；「其他開發者也可以」改成原文的「任何前沿開發者都可以」；
    「沒有提到任何國家」改成「沒有點名任何國家或市場」——原文確實出現過
    `labs in democratic countries` 這個類別說法。

### 研究紀錄的 `verbatim_quote`：3 條不是連續字串，已修

- 26%／逾 90%／未完全自主是原文**三個並列的列表項目**，紀錄用空格接成一句，在頁面上搜尋不到。
  已拆成三條各自的引文。
- `review latency , which is the time…` 逗號前多一個空格——那是 `<em>` 標籤的殘留。
- `…our offline monitoring platform .` 句點前多一個空格——那是 `</a>` 的殘留。
  （附帶發現：這句的超連結指向 `www-cdn.anthropic.com` 上的 Redacted Risk Report August 2026 PDF。）

另新增 **10 條**本輪才讀進來的引文：`now setting up`、AL3 定義、`Two obstacles`、
`compare like with like`、`Safety work was defined`、`would benefit from`、
`Any frontier developer could publish what share`、`rebuild the basket`、
`US federal government in mind`、政策頁無日期。研究紀錄現有 41 條引文，重跑比對 **0 條失敗**。

## 查過而且正確的部分（沒有動）

- **事件日 2026-09-17 成立**。專文頁面確實不印任何日期（218KB 全文中 `datePublished`／
  `article:published_time`／`Published` 各 0 次，唯一的 2026-09-18 是整站 `siteSettings._updatedAt`）；
  新聞總覽頁的 FeaturedGrid 為本篇印 `Sep 17, 2026`／`"date":"2026-09-17"`。
  原文全程沒有印任何時刻，文章也沒有替它安上時刻或台北時間換算——這一點撰稿者處理得很乾淨。
  新聞總覽頁只被用來撐日期，沒有引用它的清單或計數，符合指派訊息的限制。
- **三個核心數字都繫著自己的期間與範圍**：26%／逾 90% 繫 2026 年 8 月；
  約 3 萬個代理人、100%／100% 涵蓋率、每週 10 萬則、0.002%（約 1/47,000）都繫 2026 年 8 月
  且都寫明只涵蓋內部最常用的一個平台；6%／12% 繫 7 月 13 至 20 日那一週。
  **分母不同這件事在正文、表格、summary 三處都寫明**，全篇沒有把兩者相加、相除或跟別家比。
- **指派訊息點名的三件事都成立**（改完之後）：(a) 26% 對應 AL4「主導」、AL5 官方寫「一個我們尚未達到的等級」，
  第 4 節與 FAQ 第一題都拆解過，沒有一處寫成「AI 自己做完不用人管」；
  (b) 0.002% 每次出現都帶著規模警語，沒有只截前半；(c) 6% 與 12% 的分母沒有被合併或比較。
- **界線檢查全部通過**：沒有購買建議、沒有推薦式比價、沒有價格或方案內容；
  廠商宣稱一律帶「官方寫道／官方表示／官方稱」；沒有「首次」「唯一」「業界第一」；
  沒有把預告寫成已完成；**全篇沒有出現 OpenAI**，沒有替 Anthropic 建立與同日 OpenAI 框架的任何關聯；
  callout 只有一個。
- **與既有 `ai-news-pace-the-frontier-20260912` 沒有重疊也沒有矛盾**。逐段讀過那篇 zh-TW 全文：
  它的三步驟表格第一列是「一：常駐評估者」，本篇只用一句話點出關聯、細節交給文末連結，
  沒有重講三步驟內容。第二個連結的 text 與該內容包 zh-TW title **逐字相同**。
- **`not_said` 逐條沒踩到**：沒有暗示台灣使用者受影響、沒有其他實驗室的數字、
  沒有算力絕對值、沒有員工人數、沒有替遞迴自我改進加時間表。
- summary 四句的每個數字都在正文出現；FAQ 六題答案都是純文字、沒有網址；
  圖解四格與 `hero_label` 都沒有數字；表格 4 欄 4 列、caption 帶查核日；
  `checked_on` 在內容包三條 source、研究紀錄、第二段、表格 caption 四處都是 2026-09-18（今天），未改。

## 留給站主的 4 件事

1. **`from July 13 to July 20` 沒有印年份。** 同一頁其餘六處 July 全部是 `July 2026`
   （抽樣週、凍結基準、一月對照組），文章因此寫「2026 年 7 月 13 日到 20 日」。
   這是編輯依同頁其他日期做的判讀，不是原文印出來的字串。
   若要嚴格照印，正文、表格第四列與 summary 第三句三處要同步拿掉「2026 年」。
2. **三步驟計畫是跨篇引用。** 正文與 FAQ 提到「Amodei 那篇提出三步驟計畫、第一步是邀請外部評估者常駐」，
   依據是本站既有的 `ai-news-pace-the-frontier-20260912`（其來源是 `darioamodei.com`），
   不在本篇 `sources[]` 裡。Anthropic 專文本身只寫 `as called for by Anthropic CEO Dario Amodei`
   並超連結到那篇文章，所以「提及」有依據，但三步驟的**內容**是跨篇引用。
   若站主要求每一句都指得到本篇 `sources[]`，這兩處要改寫成只說「Amodei 稍早呼籲放慢前沿」。
3. **`labs in democratic countries` 出現過一次。** 文章寫的是「沒有點名任何國家或市場」，
   那句成立（`Taiwan`／`China`／`United States` 等字串各 0 次），
   但之後若有人改寫成「完全沒有提到國家」就不成立。
4. **8 月風險報告 PDF 仍未讀。** 官方寫 `We published all of these measurements in our recent risk report.`
   那份 PDF（`www-cdn.anthropic.com`，約 4.57MB）本輪與前一輪都沒讀，
   所以文章沒有引用它，也沒有寫「這些數字首次公布」。
   若站主想補這條脈絡，必須先完整讀那份 PDF 並把它列為第四條來源。

## 自檢

```
OK ai-news-anthropic-pace-metrics-20260917 zh-TW paragraphs 2955
```

零 FAIL、零 WARN。兩個結尾連結的目標都已存在，索引標題逐字相符（批次 4.5 不改索引標題）。
段落字數 2,955／3,000——只剩 45 字的餘裕，**翻譯階段若要再補句子，得先從別處等量精簡**，
但不可以刪任何但書或限定詞。

## 結論

`needs_owner`：23 處已改完，文章本身可刊；擋在前面的只有上面第 1、2 兩件編輯取捨
（July 的年份、三步驟計畫的跨篇引用），兩件都不是事實錯誤，而是「要多嚴格」的政策問題。
改動雖然超過十處，但沒有一處動到骨幹論述——三項指標、它們的期間與分母、
「自報不等於已查證」這條主線在查核前後完全相同，因此不需要第二輪。

---

## 第二輪

第二輪代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未改動）。
`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓，請求的 UA、標頭、查詢字串都沒有帶
email 或個人資料；主來源抽成 28,948 字可見純文字，另把 Next.js 的 RSC payload 解碼成 128,541 字對照。
**沒有使用 `sources[]` 以外的任何網址替文章補事實。**

覆核範圍：第一輪改動過的每一段與新寫進去的每一句（12 類 23 處）逐句回原文，
研究紀錄全部引文以程式做連續字串比對，另加指派訊息點名的九個疑點（a–i）——
合計約 **118 條**主張、**41→43 條**引文。**又改了 5 處**。

### 重抓結果（三條與前兩輪逐位元組相同）

| source | HTTP | bytes | 轉址 | body 是正文？ |
| --- | --- | --- | --- | --- |
| anthropic.com/institute/measuring-pace-of-ai-development | 200 | 217,865 | 0 | 是 |
| anthropic.com/news | 200 | 462,587 | 0 | 是 |
| anthropic.com/policy-on-the-ai-exponential | 200 | 140,750 | 0 | 是 |

### 又改掉的 5 處

1. **跨篇引用被寫成事實陳述，三處（最重）。** 第一輪把這件事留給站主（留給站主第 2 條），
   但指派訊息說得更明白：本篇不可用非 `sources[]` 的頁面撐句子。三處都是本站
   `ai-news-pace-the-frontier-20260912`（來源 darioamodei.com）的內容：
   (a) 第 1 節第 1 段「Amodei 主張放慢前沿 AI 的能力提升速度，讓風險防範有時間跟上」；
   (b) 第 5 節第 3 段「Amodei 那篇提出放慢前沿 AI 的三步驟計畫，第一步是邀請外部評估者常駐」；
   (c) FAQ 第六題同一句。
   (a) 換成本篇真正印出來的 `Together, these proposed measurements and policies are a starting
   point for monitoring the pace of AI development from outside the labs.`；
   (b)(c) 改成「三步驟計畫與『第一步是外部評估者常駐』出自本站另一篇整理，不在本文引用的頁面裡」。
   附帶結果：「邀請」一詞歸零——原文的動詞是 `embed`／`setting up`，不是 invite。
2. **兩層 `could` 被壓成一層，還把對方的錯誤講成既成事實**（第 3 節第 1 段）。
   原文是 `which could mean that the “judge” model could make the same kinds of errors as the
   model it is checking`；第一輪寫「評分者可能重複被評分對象**犯過的**同一種錯誤」，
   「犯過的」斷言被檢查的模型已經犯錯，原文沒有這個意思。
   已改成「官方自己寫這可能表示擔任評審的模型，會犯下和被它檢查的模型同一種錯誤」。
3. **`can` 只補了兩處，summary 漏掉**。第一輪在正文與 FAQ 補了 AL4 的「能」，
   summary 第二句仍是「人類監督下由 AI 完成大部分工作」——讀起來像已發生的事，不是等級定義。
   已改成「人類監督下、AI 能從高層次指令出發完成大部分工作」，與正文一致。
   （全篇「完成大部分工作」四處，現在四處都帶「能」。）
4. **字數等量騰出**：上面三處淨加字，同段把「先蒐集**每個項目的**證據，再由**另一個**獨立的 Claude
   擔任評審」精簡成「先蒐集證據，再由獨立的 Claude 擔任評審」——刪的是重複敘述，
   **沒有刪任何但書或限定詞**；第一輪特地改回原文的「做評分的代理人只看得到那個月或更早的證據」原封不動。
5. **研究紀錄新增 2 條引文**：`Together, these proposed measurements and policies are a starting
   point…`（撐改寫後的第 1 節）與 `as called for by Anthropic CEO Dario Amodei`
   （記錄專文對 Amodei 只有一句話加一個超連結、沒有複述，而且全文可見文字裡 `We Must Pace` 0 次，
   那個標題只在超連結網址的 slug 裡）。引文 41 → 43，重跑比對 **0 條失敗**。

### 引文比對

43 條全部以連續字串比對通過，**0 條失敗**；沒有一條含 `...`、`…` 或 `|`，所以沒有跨段落拼接的風險。
其中 4 條（Epoch AI 量表、三個監督指標的定義、METR 紅隊、`As described above, we are now setting
up…`）只在**渲染後**的可見文字裡連續，在原始碼與 RSC payload 裡被 `<em>`／`<a>` 切開——
第一輪把那兩個標籤殘留的多餘空格修掉是對的。

### 指派訊息點名的九件事

- **(a) 第三方評估者**：兩句時態都在。前言 `We plan to embed independent third-party evaluators…
  comparable to what internal risk assessment teams have.`；第 2 節結尾
  `As described above, we are now setting up external third party evaluators at Anthropic.`
  第一輪連帶改的六處（`description`、summary 第四句、FAQ 第三題、callout、第 3 節第 2 段、
  圖解第四格「外部評估者正在建立」）**逐句對過原文，六處互相一致**，
  結論都停在「不等於已經有人查核過」；沒有一處把 `setting up` 讀成 `set up`。**成立，未動。**
- **(b)「罕見事件」句**：位置在第 2 節 `Why measure oversight of agents?` 的第二段
  （在 `What we measured`／`What we found` 與 0.002% 那一格**之前**），正文寫「這一節的開頭」成立；
  規模 `operating in the economy` 在正文、表格第三列、FAQ 第二題三處都寫成「經濟體裡」；
  `can` 在——三處都是「也可能經常發生」，全篇「定期發生」0 次。**成立，未動。**
- **(c) 安全工作定義**：附錄確有 `Safety work was defined as…`，正文照寫成正面陳述，
  沒有任何「沒有定義」殘留；共通定義照 `would benefit from` 寫成「會有好處」不是「應該」；
  `Any frontier developer could publish…` 照寫成「任何前沿開發者都可以」。**成立，未動。**
- **(d) 政策頁日期**：重抓全文 `datePublished`／`article:published_time`／`Published` 各 0 次，
  可見文字裡唯一的四位數年份是頁尾 `© 2026 Anthropic PBC`，原始碼裡唯一的 `2026-09` 仍是
  `siteSettings._updatedAt`。內容包全文「同一天」**0 次**、「各國政府」**0 次**，
  `Our framework is written primarily with the US federal government in mind.` 逐字對得上。**成立。**
- **(e) 補回的限定詞**：`the highest priority flags (approximately ~50 per week)`→「優先度最高的約 50 則」；
  `as much as`→「貢獻若和對安全一樣多」；`about 6%`／`about 12%`→正文與表格都有「約」；
  `compare like with like, across developers and over time`→「能跨開發者、跨時間做同類比較」。
  AL3／AL4 的 `can` 正文與 FAQ 在、**summary 缺**（已補，見上面第 3 處）。
- **(f) July 的年份**：`from July 13 to July 20` 確實沒印年份。**第一輪的計數要訂正**：
  同頁 July 共出現 **七次**，其中 **五次**是 `July 2026`（抽樣週兩次、彙整句、凍結基準、一月對照組），
  另一次是 `the January and July baskets of tasks`，本身也沒有年份，只是回指前一句的 July 2026。
  第一輪報告寫「其餘六處全部是 `July 2026`」不準確。依指派訊息**本輪先保留**「2026 年」的寫法，
  並把訂正寫進研究紀錄的 `left_for_the_owner`。
- **(g) 三步驟計畫的跨篇引用**：**沒有成立，已改**（見上面第 1 處）。
- **(h) OpenAI**：內容包與研究紀錄全文 `OpenAI` **0 次**；主來源與政策頁全文也都是 **0 次**，
  沒有替 Anthropic 建立與同日 OpenAI 那篇的任何關聯。**成立。**
- **(i) 字數與引文**：段落 2,955 → **2,986**／3,000，加字全部等量騰出，
  **沒有刪任何但書或限定詞**；41 條引文以程式連續字串比對，全數通過（新增 2 條後 43 條仍全過）。

### 其餘覆核（正確、未動）

- **事件日 2026-09-17 獨立複現**：專文全文 `datePublished`／`article:published_time`／`dateModified`／
  `Sep 17`／`2026-09-17` 各 0 次；新聞總覽頁 FeaturedGrid 為本篇印 `<time>Sep 17, 2026</time>`，
  RSC payload 對應物件是 `"_type":"featuredGridLink","date":"2026-09-17"`，標題與摘要逐字相符。
- **界線**：`topics` 沒有 `finance`；「投資」「免責」「推薦」「值得」「購買」「訂閱」「首次」「唯一」
  「業界第一」各 0 次；callout 只有一個且沒有投資免責語；廠商宣稱一律帶「官方寫道／表示／稱」；
  沒有推定台灣可用（只寫使用方式不會因此改變，且已限縮到本文查核到的內容）。
- **與既有文章**：`ai-news-pace-the-frontier-20260912` 寫的是「Anthropic 打算在近期邀請一支外部審查團隊
  常駐」「第一步由 Anthropic 單方面承諾」——本篇改寫後只說那是本站另一篇整理的內容，
  沒有重講也沒有牴觸；第二個結尾連結的 text 與該內容包 zh-TW title 逐字相同。
- **`summary` ⊆ 正文、FAQ ⊆ 正文**：四句每個數字都在正文；六題答案都能對到正文段落
  （第六題本輪隨正文同步改寫）；圖解四格與 `hero_label` 沒有數字；表格 4 欄 4 列、caption 帶查核日；
  `checked_on` 四處都是 2026-09-18，未改。

### 留給站主的 4 件事

1. **July 的年份**（同第一輪第 1 件，計數已訂正為「五處 `July 2026`」）。要嚴格照印，
   正文、表格第四列與 summary 第三句三處同步拿掉「2026 年」。
2. **〈We Must Pace the Frontier〉這個標題本篇沒有印出來**，只在超連結網址的 slug
   與本站另一篇的標題裡。本輪已讓兩處提到它的地方緊接著「出自本站另一篇整理」；
   若要更嚴，可整個拿掉書名號、只寫「Amodei 那篇」。
3. **8 月風險報告 PDF（約 4.57MB）三輪都沒有讀**，文章因此沒有引用它，也沒有寫「首次公布」。
   要補這條脈絡得先完整讀 PDF 並列為第四條來源。
4. **段落 2,986／3,000，只剩 14 字餘裕。** 翻譯階段若要補句子，得先從別處等量精簡，
   且不可刪任何但書或限定詞。

### 自檢

```
OK ai-news-anthropic-pace-metrics-20260917 zh-TW paragraphs 2986
```

零 FAIL、零 WARN（批次 4.5 不改索引標題，兩個結尾連結的目標都已存在，所以連允許的兩條 FAIL 也沒有）。

### 第二輪結論

`needs_owner`：又改了 5 處，最重的是把三處跨篇引用從事實陳述降回「本站另一篇整理過」——
那是第一輪留給站主、而指派訊息要求本輪處理掉的一件。骨幹論述（三項指標、期間與分母、
「自報不等於已查證」）兩輪前後完全相同。擋在前面的只剩上面第 1、2 兩件編輯取捨，
兩件都不是事實錯誤，而是「要多嚴格」的政策問題。
