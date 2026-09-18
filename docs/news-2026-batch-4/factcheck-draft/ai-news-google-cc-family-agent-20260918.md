# 獨立查核：ai-news-google-cc-family-agent-20260918

查核代理：未參與撰稿。查核日 **2026-09-18**（與文章的 `checked_on` 同一天，未更動）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial" --max-time 90` 重抓，
剝掉 `script`／`style`／標籤後讀完 body；RSS 用 XML 解析而非字串比對，逐個 `<item>` 取
`link` 與 `pubDate`；研究紀錄 25 條 `verbatim_quote` 以 NFKC 正規化後做連續字串比對；
`gemini.google` 頁尾那行細則另外回到原始 HTML 看 DOM 位置以確認適用範圍。
**任何請求的 UA、標頭、查詢字串都沒有放入 email、姓名或個人資料**，
也**沒有使用任何 `sources[]` 以外的新網址替文章補事實**。

檢查的主張：**139 條**（正文 54、摘要 5、FAQ 6 題的答句 16、callout 4、表格 16 格與 caption、
圖解 caption 與四格八句、`hero_label`、title 與 description、25 條 `verbatim_quote`、四條來源）。
**改了 16 處**（內容包 15 處、研究紀錄圖解 1 處），另有 4 件留給站主。

## 重抓結果（四條 sources 都還在、位元組數與撰稿紀錄完全相同）

| source | HTTP | bytes | body 是否為正文 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| blog.google `…/google-labs/cc-expanding-to-groups/` | 200 | 373,855 | 是，全文可讀 | byline `Sep 17, 2026`；作者 Tom Shane, Senior Product Manager, Google Labs；導言；三項功能與圖說 `CC can take action, like filling out forms, with your permission.`；自己的已驗證帳號與兩個限制；三種分享控制；`isolated cloud computer`；記憶分兩層；開放條件句（含 Google 自己漏掉的句點 `in the U.S`）；升級信件與候補名單 |
| blog.google `…/google-labs/cc-ai-agent/` | 200 | 388,980 | 是，全文可讀 | byline `Dec 16, 2025`；`delivering a "Your Day Ahead" briefing to your inbox every morning`；2025 年的開放條件句 `…18+ in the U.S. and Canada, starting with Google AI Ultra and paid subscribers.` |
| `gemini.google/overview/daily-brief/` | 200 | 152,234 | 是，全文可讀 | 推出橫幅 `Daily Brief is currently rolling out to eligible users in select regions.`；頁尾 `Availability varies. US-only. English-only. 18+.` |
| `blog.google/rss/` | 200 | 30,544 | 是，XML 可解析 | 20 則 `<item>`；本篇 `pubDate` = `Thu, 17 Sep 2026 18:15:00 +0000`；最新一則與 `lastBuildDate` 同為 `Thu, 17 Sep 2026 20:00:00 +0000`，feed 是活的 |

三個位元組數與撰稿代理、更早的探索代理記到的完全一樣，沒有出現漂移。
RSS 的 20 則只用來判斷 feed 是活的，**沒有寫進文章**（BRIEF 型態 4）。
研究紀錄正確地把 `labs.google/cc`（可讀文字只有 `CC Sign in` 的登入牆空殼）
留在 `unverified_or_excluded`、沒有進 `sources[]`。

## 改掉的 16 處

### 撰稿代理點名要重查的四件事

1. **(d) `Availability varies. US-only. English-only. 18+.` 的適用範圍，以及被漏掉的對沖詞。**
   回到原始 HTML 看 DOM：這一行**不屬於任何一則 FAQ、也不屬於某一個功能**，
   它單獨放在頁級的 `<div id="disclaimers">` 區塊裡，位置在 FAQ 區段的結束標籤與一個 spacer 之後、
   `footer` 之前，是 `<main>` 裡的最後一塊內容。它管的是
   `gemini.google/overview/daily-brief/` 這一頁，而整頁的主題就是 Daily Brief，
   所以它涵蓋**這一頁的 Daily Brief**，不涵蓋家庭版 CC（家庭版有自己在 blog.google 上的開放條件句）。
   草稿把範圍寫對了，但**掉了開頭的 `Availability varies.`**，已補成「供應情況不一」，
   並把位置寫成「頁面最下方的免責區塊……涵蓋整個 Daily Brief 頁面的條件」。
2. **(d) 同一段開頭「如果只是想找現在就能用的版本」——這是全文唯一會讓讀者以為台灣有東西可用的句子，已刪掉。**
   Daily Brief 的細則是 US-only、English-only，台灣讀者並沒有一個「現在就能用的版本」。
   改寫後的結尾明講「所以這個比較早的版本，台灣的使用者同樣用不到」。
3. **(c) 記憶分層那段「編輯設計的例子」確實暗示了官方沒說過的行為，已重寫。**
   原文寫「一位成員習慣早餐配咖啡，這類個人偏好照官方描述的設計原則，**理論上會被歸進屬於個人的那一層，
   不會被當成全家共用的規則**」。即使標了「編輯設計的例子」與「理論上」，後半句仍然是在預測
   CC 實際會怎麼分類——公告只列了兩組例子（`favorite family restaurants` 對 `dietary preferences`），
   從來沒有描述判斷規則。已改成用 Google 自己那兩個例子撐起來的**開放式問題**：
   「一家四口裡只有一個人不吃辣，那麼訂餐廳時的這項忌口，該算全家共用的規則還是一個人的偏好？
   公告沒有說明實際上怎麼判斷一件事屬於哪一層」。
4. **(a) 時間換算的依據成立，未改。** 見下面「查過而且正確的部分」第 1 條。
5. **(b) 訂閱門檻那一段本身是中立的，但摘要與 callout 把它改寫壞了。**
   正文第 4 節第 2 段與 FAQ 第 2 題寫的是「要**從** Google AI Ultra 與付費訂閱者**開始開放**」，
   貼著原文的 `starting with`；但**摘要第三句寫成「且要有 Google AI Ultra 或付費訂閱」、
   callout 寫成「且限 Google AI Ultra 或付費訂閱」**——把分批開放寫成硬性門檻（BRIEF 型態 3），
   而且把 `and` 寫成「或」。兩處都已補回 `starting with` 的語氣，四處現在一致。

### 其餘 11 處

6. **第一段刪掉「這個帳號不屬於任何一位成員」。** 公告只寫
   `It has its own Google account that gives CC a distinct identity and clear permissions model`，
   **從來沒有說這個帳號不屬於任何成員**；而且本篇第 5 節自己就寫「沒有寫這個帳號本身算是屬於誰的」，
   同一篇前後矛盾。這是 BRIEF 型態 2（把「來源沒說」寫成「來源說沒有」）。
   已改成官方原話的「官方說這讓 CC 有獨立的身分與清楚的權限範圍」。
7. **引號裡的「今年 5 月」改成「5 月」**（第 1 節第 2 段與 FAQ 第 5 題兩處）。
   公告寫的是 `in May we brought it to the Gemini App as Daily Brief`，
   **年份是上下文推出來的，不是 Google 印的**——研究紀錄自己的 `unverified_or_excluded`
   也這樣寫，前期研究紀錄更直接指定「寫 `官方寫的是「5 月」`」。
   把「今年」放進引號等於把一個來源沒寫的字算在 Google 頭上。已加上「沒有印出年份」。
8. **表格第一列的「台灣帳號收不收得到未寫明」改成「未寫明可用的語言」。**
   官方的開放條件已經寫明只有美國，說台灣收不收得到「未寫明」會讓讀者以為台灣**可能**在範圍內，
   和全文其他四處的寫法互相打架。語言則是公告真的沒有寫的東西
   （第 4 節第 1 段同步補上「或可用的語言」，讓表格那一格在正文有對應）。
9. **表格第一、二列「需要誰同意」欄的「不用，屬於摘要通知」「不用，屬於整理與追蹤」改掉。**
   公告只在**會採取行動**的功能上寫 `with your permission`，
   從來沒有說摘要與整理「不用」同意；實際上同意發生在更前面的分享設定
   （`Each member can easily choose what to share with CC and what to keep private`）。
   已改成「事前由各成員決定分享哪些內容」與「同上，只用成員分享出來的資訊」。
10. **第 2 節第 2 段補回兩個被刪掉的限定詞。** 原文是
    `pulling relevant shared information from across your group`，草稿寫成
    「散落在群組裡**各個成員手上**的相關資訊」——掉了 `shared`，會讀成 CC 看得到成員手上的全部資訊，
    正好推翻同一篇反覆強調的「CC 只看得到成員主動分享的內容」。
    原文的 `helps keep them up to date` 也被寫成「持續更新」，已改回「協助保持更新」。
11. **第 2 節第 3 段「代替家人處理一些耗時的行政工作」改成「官方寫的是協助你完成」。**
    原文是 `CC can also help you complete time consuming logistical tasks`——
    `help you complete` 不等於「代替」。同段補上歸因（整段原本沒有「官方」二字）
    與 `activity registration PDFs` 的 PDF。
12. **第 3 節第 1 段刪掉「在群組的信件或訊息串裡，CC 是用自己的帳號出現，就像另一位成員一樣，
    而不是借用某個人的帳號」。** 公告只寫 `This is how CC will show up when it interacts with the group`，
    沒有說信件或訊息串、沒有說像另一位成員、也沒有說不是借用誰的帳號。
    已改成貼著原文的「CC 在跟群組互動時就是用這個帳號現身」。
13. **研究紀錄圖解第一格的說明由「像成員一樣出現在信裡」改成「在群組裡用這個帳號現身」**，
    理由同上一條。圖解由協調者依這份紀錄繪製，留著會把同一個沒有來源的說法**畫到圖上**。
14. **第 4 節第 3 段「範例都是小孩的學校表單與活動」改成「舉的例子有不少是」。**
    公告的例子還包括獸醫、游泳中心、雜貨清單、餐廳與行車時間，不是全部跟小孩有關
    （BRIEF 型態 3：`such as` 的清單不是全清單，「都是」更不成立）。
    同句的「等於小孩沒辦法……」改成「照公告字面上的條件，小孩沒辦法……」，與 FAQ 第 3 題的寫法一致。
15. **第 5 節第 1 段刪掉「存放在哪裡」，並補上公告真的寫了的那一句。**
    公告有寫 `every CC runs on its own isolated cloud computer`，
    再說官方沒寫內容「存放在哪裡」會被這句推翻（型態 2）。
    保留期限與是否用於訓練模型兩個否定句成立，維持不動。已補成
    「也寫了每個 CC 都跑在自己獨立的雲端電腦上，但沒有寫……保留多久、會不會被用來改進 Google 的模型」。
    （依 `must_not_write`，`Antigravity` 與「最新的 Gemini 模型」都沒有寫進去，免得帶出版本號。）
16. **第 1 節第 1 段兩處、第 3 節第 2 段一處、第二段一處的貼合度修正。**
    公告標題的中譯由「一個為家庭打造的新 CC，AI 代理」改成「新版 CC：一個為家庭打造的 AI 代理」
    （原譯把 `The new CC, an AI agent built for families` 的同位語拆成兩截）；
    「開頭第一句話」改成「標題下的導言」——被引用的
    `Google Labs introduces a new experimental agent...` 是標題下的導言，
    正文第一句其實是 `When we launched CC, our goal was...`；
    第 3 節第 2 段的「直接轉寄信件、傳訊息」改成「用電子郵件或 Google Chat 傳給 CC」並補上 `or files`
    （原文 `via email or Google Chat`、`share a Drive folder or files with CC`）；
    第二段（查核聲明）**補上第四條來源 RSS 摘要**（`sources[]` 有四條，原本只列三條），
    並把「這個家庭版目前只開放美國的帳號」改成「官方列出的開放地區也只有美國」——
    原文 `for people (18+) in the U.S` 說的是**人在美國**，不是帳號屬於美國。

## 查過而且正確的部分（沒有動）

1. **事件日與兩個日期的處理成立。** 頁面 byline 印的是 `Sep 17, 2026`，
   RSS 這一則的 `pubDate` 是 `Thu, 17 Sep 2026 18:15:00 +0000`，台北 UTC+8 換算為 2026-09-18 02:15。
   slug 後綴、`news_date`、第一段三者一致（DELTA-4-5 第 6 點）。
   文章把**兩個日期都寫出來並說明原因**，讀者回頭對照原文不會以為文章寫錯——這一段的處理很好，沒有改。
   RSS 的 20 則只是取得成敗的判準，沒有被當成事實寫進文章。
2. **訂閱門檻那一段（正文與 FAQ）是中立的。** 兩句話各自標了日期
   （2026-09-17 的「個人 Google 帳號」對 2025-12-16 的 `starting with Google AI Ultra and paid subscribers`），
   明寫 Google 沒有說門檻是否改變，**沒有替讀者結論成「現在免費」或「還是要付費」**。
   加拿大只出現在 2025 年那一句裡，沒有被延用到家庭版，也沒有反過來斷言加拿大被拿掉。
3. **沒有讓讀者以為台灣可用。** 改完後全文出現台灣的五處
   （第 4 節第 1 段、第 5 節第 3 段、結語、FAQ 第 1 題、FAQ 第 5 題）都是
   「官方列出的開放地區只有美國」「台灣目前用不到」，而且五處都**沒有預測未來會不會開放**。
4. **AI 摘要面板沒有被引用。** 公告上方 `Read AI-generated summary` 面板寫的
   `...join the waitlist to start using it today` 與正文的 `in the coming days`／waitlist 互相矛盾；
   全文與研究紀錄都沒有出現面板的任何說法，文章寫的是「兩者都沒有給出確切要等多久」，貼著正文。
5. **界線檢查全部通過。** 沒有購買或訂閱建議；沒有推薦式比價（兩個開放條件只做並列與標日期）；
   廠商宣稱都有歸因（「公告寫道」「官方說明」「官方寫的是」，本輪又補了兩處）；
   沒有本站實測的說法；狀態詞完整（早期實驗、候補名單、升級信件「接下來幾天」都寫進去了）。
   **只有一個 callout，沒有投資免責段落**；`topics` 是 `ai`／`software`／`ai-news`，沒有掛 `finance`。
6. **沒有自己算出來的數字。** 全文只有 6（`up to six members`）、18（`18+`）與日期，
   三種都逐字來自來源；**圖解四格沒有任何數字**；摘要的數字都能在正文找到同樣的寫法。
7. **`verbatim_quote` 25 條全部通過連續字串比對**，`url` 全在 `sources[]` 內，
   包含 Google 自己漏掉句點的 `in the U.S with a personal Google account` 照抄未訂正（BRIEF 型態 1）。
8. **`checked_on` 2026-09-18 在六處一致**（內容包四條 source、研究紀錄、第二段、表格 caption、圖解 caption）。
   本輪重查沒有改動它。
9. **兩個結尾連結沒有動**，`check_article.py` 對它們沒有任何 FAIL。

## 留給站主的事

1. `gemini.google/overview/daily-brief/` 是**沒有日期的產品頁**，推出橫幅與頁尾細則都可能無預警改動。
   發布前（以及日後修訂時）要重讀一次那兩處，文章第 5 節第 3 段與 FAQ 第 5 題會跟著要改。
2. 文章目前寫「公告沒有列出任何擴大到其他地區的時間表或可用的語言」，這是 **2026-09-18 讀到的版面**。
   Google 若之後補發開放地區或語言說明，這兩句話會過期。
3. `display_order` 目前是 **166**，由協調者依 AI 垂直 161 起的排序決定，本代理沒有動。
4. **結論是 `needs_second_round`**，理由見下。

## 結論

`needs_second_round`。

依規格第 3 節的門檻——「你改了超過十處事實……選最後一個」——本輪在事實層面改了
內容包 15 處加研究紀錄 1 處，超過十處。

**但骨幹論述本輪沒有動**：美國限定、CC 有自己的帳號、每人各自決定分享、記憶分兩層、
訂閱門檻不下結論，五件事都維持原樣，文章的結構與角度也沒有改。
第二輪要做的是**逐句回來源查本輪新寫進去的句子**，重點三處：
記憶分層那段重寫後的例子與它的否定句、第 5 節第 1 段新增的「獨立的雲端電腦」、
以及表格四列改過的「需要誰同意」與「官方未說明的部分」兩欄。

自檢：

```
OK ai-news-google-cc-family-agent-20260918 zh-TW paragraphs 2881
```

（`paragraphs 2881` 在 1,800–3,000 內；改完之後**沒有留下任何 FAIL**——
DELTA-4-5 第 3、4 點說的索引標題不改、第二個連結指向既有已發布文章，兩條都成立，
所以規格裡「允許留下的兩種 FAIL」這次一條都沒有出現。）

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未更動）。
範圍不是整篇重做，而是覆核第一輪改動過的每一個段落、逐句回查第一輪**新寫進去的每一句**，
再把 `verbatim_quote`、摘要／FAQ ⊆ 正文、但書回掃與界線各掃一次。
**覆核 136 條主張，又改了 19 處**（內容包 16、研究紀錄 3）。結論 **`ok`**。

### 重抓結果（四條全部再抓一次，位元組數與第一輪一字不差）

| source | HTTP | bytes | body 是否為正文 |
| --- | --- | --- | --- |
| blog.google `…/cc-expanding-to-groups/` | 200 | 373,855 | 是，剝標籤後全文可讀 |
| blog.google `…/cc-ai-agent/` | 200 | 388,980 | 是，全文可讀 |
| `gemini.google/overview/daily-brief/` | 200 | 152,234 | 是，全文可讀（含頁尾細則） |
| `blog.google/rss/` | 200 | 30,544 | 是，XML 可解析；20 則，本篇 `pubDate` = `Thu, 17 Sep 2026 18:15:00 +0000` |

請求一律 `curl -sL -A "Mokaair-editorial" --max-time 90`；
**UA、標頭、查詢字串都沒有放入 email、姓名或任何個人資料**，
也沒有動用 `sources[]` 以外的網址替文章補事實。

### 又改掉的 19 處

#### 最重的三處

1. **第 3 節第 3 段：第一輪重寫的記憶分層例子，和它自己的前一句打架，已再改寫。**
   第一輪把例子改成開放式問題「一家四口裡只有一個人不吃辣，那麼訂餐廳時的這項忌口，
   **該算全家共用的規則還是一個人的偏好？**」。但同一段前一句才照公告寫過
   「也會記得只屬於一個人的資訊，**例如個人的飲食偏好**」——
   公告原文 `versus what belongs to one person (like dietary preferences or local timezones)`
   已經把飲食偏好指定在個人那一層，再問「該算哪一層」等於推翻自己剛引用的官方例子。
   已改成先照官方兩組例子定位、再問兩層怎麼互動：
   「照官方舉的例子，這項忌口屬於個人那一層，餐廳偏好卻屬於全家那一層，
   那麼全家一起訂餐廳時，兩層會怎麼互相影響？**公告只列了這兩組例子**，
   沒有說明實際上怎麼判斷一件事屬於哪一層」。否定句同時限縮到「公告只列了這兩組例子」。
2. **`meal` 被寫成「晚餐」，兩處都已改成「餐點」。**
   公告的功能句是 `crafting weekly meal plans`，`meal` 不是 dinner；
   正文第 2 節第 3 段的「草擬一週的**晚餐**計畫」與表格第三列的功能名
   「協助填表、購物與**晚餐**清單」都窄化了官方的說法（公告導言確實有
   `figuring out what's for dinner`，但那是情境描述，不是這一條功能的例子）。
3. **研究紀錄三條 `verbatim_quote` 帶著剝標籤造成的假空白，讀者在頁面上搜不到，已截短。**
   Google 的原始 HTML 是 `<a>Daily Brief</a>.`、`<a>Antigravity</a>,`、`<a>waitlist</a><i>.</i>`，
   剝掉標籤後變成 `Daily Brief .`、`Antigravity , and`、`waitlist .`——
   第一輪的比對是對剝標籤文字做的，所以三條都「命中」，
   但那三個字串在 Google 實際渲染的頁面上並不存在。
   第 4、18 條已截到連結結尾；第 15 條截到 `Google’s agentic harness` 為止
   （文章只用到 `isolated cloud computer` 那一半，且 `must_not_write` 禁止寫出
   Antigravity 與模型版本），並在 `fact` 欄寫明整句原貌。
   修正後 25 條在「剝標籤」與「頁面實際字串」兩種正規化下**都全數命中**。

#### 其餘 16 處

4. **FAQ 第 6 題刪掉「與 CC」。** 原本叫讀者去「Gemini 官方網站介紹 Daily Brief **與 CC** 的頁面」，
   但 `sources[]` 只驗到 `gemini.google/overview/daily-brief/`，Gemini 官網沒有任何查證過的 CC 頁面，
   而 `labs.google/cc` 是登入牆空殼（已在 `unverified_or_excluded`）。等於指路到一個沒查證存在的頁面。
5. **FAQ 第 2 題刪掉「即可」。** 原本寫「公告只寫使用個人 Google 帳號**即可**」，
   「即可」是「這樣就夠了」的推論，正好倒向本文刻意不下的那個結論（付費門檻已取消），
   也漏掉同一句裡的美國與 18 歲條件。正文第 4 節第 2 段本來就寫「只寫個人 Google 帳號」，現在兩處一致。
6. **FAQ 第 5 題的「5 月」與正文對齊**：「寫的是 5 月**才**被帶進 Gemini App」改成
   「寫的是「5 月」把它帶進 Gemini App」——補上引號標出這是官方原字，並刪掉「才」
   （原文 `in May we brought it` 沒有「遲至」的語氣）。
   五處（正文第 1 節第 2 段、FAQ 第 5 題、研究紀錄 `event_date_basis`、
   `unverified_or_excluded`、`must_not_write`）現在一致：只寫月份、都明說沒有印出年份，
   全文 `今年` 出現 **0** 次。
7. **第一段與第 3 節第 1 段的「清楚的權限範圍」改成「清楚的權限機制」**（第一輪新寫的兩句）。
   原文 `clear permissions model`：model 是權限的設計方式，不是權限的「範圍」。
8. **摘要第二句改寫成「最多可以有 6 位成員一起管理與協作，每人各自決定要跟 CC 分享什麼、保留什麼隱私，並且能隨時更改」。**
   原本寫「管理與**使用**」（正文寫的是「管理與協作」，摘要必須是正文的子集），
   而且把 `Each member can easily choose what to share with CC and what to keep private, and can make changes at any time`
   併進了「分享哪些**寄件者**的信件」——「隨時更改」被掛到另一個機制上。
9. **摘要第四句的「Google 沒有說明」改成「官方這篇公告沒有說明」**：否定句限縮到本文引用的那一頁與查核日。
10. **第 3 節第 2 段「訂票通知」改成「旅遊訂位通知」**（原文 `travel bookings`，含住宿與行程，不只票）；
    同段「資料夾**與**檔案」改成「資料夾**或**檔案」（原文 `share a Drive folder or files`）。
11. **第 1 節第 2 段「許多早期使用者」改成「許多早期測試者」**（原文 `many early testers`，當時是 early access）。
12. **第 3 節第 3 段「全家常去的餐廳」改成「全家最愛的餐廳」**（原文 `favorite family restaurants`）。
13. **表格第四列「需要誰同意」欄的「每人自行決定分享**對象**」改成「分享**範圍**」**：
    公告寫的是成員決定分享什麼內容與哪些寄件者，不是決定分享**給誰**。
14. **第二段（第一輪重寫的查核聲明）把來源清單裡的逗號改回頓號**——
    第一輪補上第四條來源時留下「原始公告**，**Gemini 官方產品頁面」，四項並列中間夾了一個逗號。

### 指派訊息點名的五件事

- **(a) 第一輪新寫的句子逐句回查。** 記憶分層那段見上面第 1 條（已再改）。
  第 5 節第 1 段新增的「也寫了每個 CC 都跑在自己獨立的雲端電腦上」**成立**
  （`every CC runs on its own isolated cloud computer`），
  同段兩個否定句（保留多久、會不會用來改進模型）重讀全文後確認公告確實沒寫，主語是「公告」。
  表格改過的兩欄**成立**：「需要誰同意」前兩列貼著
  `Each member can easily choose what to share…` 與 `pulling relevant shared information`，
  不再出現公告從未寫過的「不用同意」；「台灣帳號」那格改成「未寫明可用的語言」後，
  正文第 4 節第 1 段有對應句，也不再暗示台灣可能在範圍內。
- **(b) 分批開放四處一致。** 摘要第三句、正文第 4 節第 2 段、FAQ 第 2 題、callout
  都寫「要**從** Google AI Ultra 與付費訂閱者**開始開放**」，逐字對得上
  `starting with Google AI Ultra and paid subscribers`；沒有一處寫成硬性門檻，也沒有把 `and` 寫成「或」。
  FAQ 第 2 題的「即可」是唯一的殘留破口，已刪（見第 5 條）。
- **(c) 引文「5 月」五處一致**，見第 6 條。
- **(d) 頁級細則的適用範圍，本輪獨立重驗 DOM 後成立，而且正文沒有寫反。**
  原始 HTML 裡 `<div id="disclaimers">` 在 offset 48333，位於 FAQ 兩個 `</section>` 與一個 spacer 之後、
  `</main>`（48757）與 `<footer>`（48765）之前；整個區塊只有一個
  `<p>Availability varies. US-only. English-only. 18+.</p>`，全頁只出現這一次。
  它是 **Daily Brief 這一頁**的頁級細則，不屬於某一則 FAQ 或某一個功能，也沒有提到家庭版 CC。
  正文第 5 節第 3 段寫「涵蓋整個 Daily Brief 頁面的條件」、結論收在「這個**比較早的版本**，台灣的使用者同樣用不到」；
  FAQ 第 5 題的「跟家庭版一樣，台灣目前都用不到」比的是**結果**，不是把細則套到家庭版身上
  （家庭版用的是 blog.google 自己那句 `for people (18+) in the U.S`）。兩處都沒有寫反。
- **(e) 台北跨日維持第一輪的處理。** 本輪用 XML 解析重現 `Thu, 17 Sep 2026 18:15:00 +0000`
  （台北 2026-09-18 02:15）；正文第 1 節第 3 段兩個日期都寫、並說明原因，
  slug 後綴／`news_date`／第一段三者一致，未改。
- 另外：`ai-news-google-assistant-gemini-20260904` **完全沒有被碰**，兩個結尾連結也一字未改。

### 查過而且維持不動的部分

- **但書沒有為了字數被刪**：本輪只增不減（段落 2,881 → **2,916**，上限 3,000），
  刪掉的四個字（「即可」「才」「與 CC」）都是推論或未查證的指路，不是限定詞或歸因。
- **界線全部通過**：沒有購買、訂閱、升級或投資建議；沒有推薦式比價；廠商宣稱都有歸因；
  沒有本站實測；狀態詞（早期實驗、候補名單、「接下來幾天」）完整；
  只有一個 callout、沒有投資免責段落；`topics` 是 `ai`／`software`／`ai-news`，沒有 `finance`。
  全文「台灣」出現 11 次，沒有一次推定台灣可用，也沒有一次預測何時開放。
- **`checked_on` 2026-09-18 仍在六處一致**，本輪沒有改。
- 摘要每個數字（6、18 與日期）都在正文；圖解四格沒有數字；AI 摘要面板仍然沒有被引用。

### 留給站主的事

1. 第一輪的兩條照舊：`gemini.google/overview/daily-brief/` 是**沒有日期的產品頁**，
   推出橫幅與頁尾細則隨時可能改，發布前要重讀（正文第 5 節第 3 段與 FAQ 第 5 題會跟著要改）；
   「公告沒有列出任何擴大到其他地區的時間表或可用的語言」是 2026-09-18 的版面，Google 補發說明後會過期。
2. `display_order` 166 與兩個結尾連結由協調者決定，本輪沒有動。

### 結論

**`ok`。** 本輪的 19 處都是**貼合度與範圍**的修正，沒有一處動到骨幹論述——
美國限定、CC 有自己的帳號、每人各自決定分享、記憶分兩層、訂閱門檻不下結論，五件事全部維持原樣，
文章結構與角度也沒有改。第一輪點名要覆核的三個地方，兩個成立、一個（記憶分層例子）本輪再修一次。

自檢：

```
OK ai-news-google-cc-family-agent-20260918 zh-TW paragraphs 2916
```

（`paragraphs 2916` 在 1,800–3,000 內，`exit=0`；**沒有留下任何 FAIL 或 WARN**，
規格裡「允許留下的兩種 FAIL」這次同樣一條都沒有出現。）
