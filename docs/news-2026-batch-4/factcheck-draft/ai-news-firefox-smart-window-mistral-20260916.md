# 獨立查核：ai-news-firefox-smart-window-mistral-20260916

查核代理：未參與撰稿。查核日 **2026-09-18**（與撰稿者的 `checked_on` 同一天，四處一致，**不改**）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀完 body，
研究紀錄原有的 20 條 `verbatim_quote` 全部用程式對今天存下來的 HTML 做連續字串比對（Unicode 正規化後）。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**；全站導覽、JSON-LD 與電子報國別 `<select>`
只用來檢驗否定句，沒有進文章。任何請求都沒有帶 email、姓名或個人資料。

檢查的主張：**94 條**（title、description、開頭兩段、摘要 4 句、11 段正文每一句、FAQ 5 題答句、
callout、表格 16 格與 caption、圖解 caption、研究紀錄的 4 個 `diagram` 節點與 `hero_label`）。
**改了 15 處**，另有 4 件留給站主。

## 重抓結果（三條都還在、都是正文）

| source | HTTP | bytes | 驗到的東西 |
| --- | --- | --- | --- |
| mistral.ai/news/mistral-x-mozilla/ | 200 | 243,456 | `September 16, 2026` + `By Mistral and Mozilla`；開頭句；`now powered by Mistral models`；市場句；`Mistal’s`（原文錯字）；零資料保留兩句；Enzor-DeMeo 與 Mensch 兩段引言 |
| blog.mozilla.org/.../mozilla-mistral-partnership/ | 200 | 69,671 | `September 16, 2026`；`Mistral Small 4 is coming to … becoming a new AI model …`；`still choose from a multitude of other AI models`；`planning additional European expansion later this year`；`CEO of Mozilla Corporation` |
| blog.mozilla.org/.../firefox-smart-window/ | 200 | 71,906 | `August 18, 2026`；`Update on September 16, 2026: … now rolling out in France`；`several months building and testing`；`Smart Window is optional … which AI model you want to use`；`AI Controls … turning it off entirely`；`currently available in English to people in the U.S. and Canada`；Exa 那段 |

Mozilla 合作公告今天是 **69,671 bytes**，與探索代理當天記的數字相同，
撰稿代理記的 69,692 是同一頁在不同時刻的漂移——這一頁一天內出現過三種大小，
**位元組數只能當「抓到了沒有」的判準，不能當版本識別**（已寫進研究紀錄 `live_data_warnings`）。

原有 20 條 `verbatim_quote`：**20/20 逐字命中**，含來源自己的錯字 `Mistal’s`（彎引號 U+2019）。
本次新加的 5 條同樣先比對再寫入，合計 **25/25**。

## 撰稿代理點名要重查的三件事

**(a) 「Mistral 公告沒寫版本名稱」——成立，但範圍要收緊。**
`Mistral Small 4` 在 mistral.ai 這一頁出現 **2 次**，兩次都在全站共用的導覽卡片
（`class="text-h6 font-mistral"`，「Latest models」清單，與 Mistral OCR 4／Medium 3.5／Voxtral TTS 並列），
**公告內文 0 次**；內文只有 `Firefox Smart Window (beta), Mozilla’s AI browsing assistant, is now powered by Mistral models.`
依 BRIEF 型態 2，句子已改成「Mistral 自己的**公告正文**只提到『Mistral 的模型』」，
並把查法與查核日寫進正文（表格與 FAQ 3 同步）。

**(b) 「兩家公司目前都沒有提到台灣」——成立，沒有滑向「台灣不能用」。**
`Taiwan`／`Japan`／`Korea` 在兩個 Mozilla 頁各命中 1–2 次，逐一讀過前後 HTML，
**全部落在電子報的國別 `<select>`**（`<option value="tw">Taiwan</option>`）；mistral.ai 三個字串各 0 次；
`Asia` 三頁皆 0 次。正文、callout、FAQ 1 三處都明寫「不是『台灣用不到』」，守住了。
**但是撰稿代理漏掉一件事**：Mozilla 8 月原文其實有一句自己的開放範圍宣告——
`It’s currently available in English to people in the U.S. and Canada. If it’s not available where you are yet, you can sign up to be notified when it is.`
那是**列入清單**不是**排除清單**，所以原本的守門句仍然成立；
但對一個正在問「台灣用得到嗎」的讀者藏起一手來源自己寫的開放範圍，是錯的謹慎。已補進正文與 FAQ 1。
（研究紀錄原本寫「Mozilla 從來沒有列舉市場」，那是錯的，已在 `not_said` 標明更正。）

**(c) 「Mozilla 執行長」——不可接受，已改。**
兩頁印的都是 `said Anthony Enzor-DeMeo, CEO of Mozilla Corporation`。
Mozilla 基金會與 Mozilla Corporation 是兩個法人，來源只支撐後者，已改成「Mozilla Corporation 執行長」。
順帶查到這段引言**兩份公告都有**（mistral.ai 版寫 `Anthony Enzor-DeMeo, CEO, Mozilla Corporation`），
所以「在公告中被引述」也改成「在兩份公告中都被引述」，是可驗證的加強。

## 改掉的 15 處

1. **最重的一處，牽動 9 個地方：這不是「換模型」。**
   Mozilla 寫的是 `Mistral Small 4 is coming to Firefox Smart Window beta …, becoming a **new** AI model for
   Smart Window users in the US and Canada`，同一段緊接著
   `Across all markets where Smart Window beta is available, Firefox users can still choose from a multitude of other AI models.`
   Mozilla 自己從 8 月原文連出去的 Mozilla Connect 討論串，slug 就是
   `smart-window-expands-to-france-with-**mistral-as-a-new-model**`。
   草稿卻在 9 處寫成「換模型」「改用」「換上」「模型換人」「換了模型供應商」——那是把「多一個選項」寫成「取代」，
   而且與草稿自己引用的「仍可選其他模型」互相矛盾。已全部改成「多一個模型選項」：
   第一段、摘要第 2／3 句、第一節標題、第一節第 1／3 段、第二節第 1 段、第三節第 3 段、FAQ 2、表格 Mozilla 列、
   以及研究紀錄的 `diagram` 節點（「美加換模型」→「美加多一個模型」）。
2. **刪掉自己生出來的日期**「從 9 月 16 日起，美國與加拿大的使用者將改用 Mistral 的模型」。
   Mozilla 沒有給任何起始日，用的是 `is coming to`（未來式／進行中）。
   已改成照原文的時態與措辭：「Mistral Small 4『即將加入』Smart Window 測試版，成為美國與加拿大使用者『一個新的 AI 模型』」。
3. **「Smart Window 在 2026 年 8 月 18 日已經推出」不成立**（4 處：第一段、摘要第 3 句、第一節第 3 段、FAQ 2）。
   8/18 那篇自己寫 `We’ve spent the last several months building and testing Smart Window in beta with our community.`
   與 `Today, we’re adding new capabilities …`——那天加的是**新功能**，Smart Window 在那之前就已經在測試。
   已改成照 Mozilla 那天寫的話敘述；文章的主論點（Smart Window 早於 9/16）不受影響，而且現在來源撐得住。
4. **「Mozilla 執行長」→「Mozilla Corporation 執行長」**，理由見 (c)。
5. **補上 Mozilla 自己對「預設值與開關」的答案**（原稿完全沒有，卻是讀者第一個會問的）：
   `Smart Window is optional. You choose when to use it, what browsing context it can use to help with a task,
   and which AI model you want to use.` 與 `Firefox’s AI Controls gives you one place to manage Smart Window,
   including turning it off entirely …`。加在第三節與 FAQ 3。
6. **補上 Mozilla 的開放範圍句與登記通知**（第五節第 1 段與 FAQ 1），理由見 (b)。
7. **「Mistral 自己的公告只提到」→「公告正文」**，並寫出查法，理由見 (a)。表格 Mistral 列同步加「正文」。
8. **「Mozilla 這次只點名法文」是假的否定句。** 8 月原文寫 `currently available in **English**`。
   已改成「Mozilla 點名的語言只有法文與英文（8 月原文寫的是目前以英文提供）」，
   研究紀錄 `not_said` 的「No language list beyond French」同步更正。
9. **「已經變成」→「已經從…擴大到…」。** 原文是 `competition has **expanded from** “which AI model is best?” **to** …`，
   expanded 是擴大不是取代，原寫法把 Mozilla 的說法改強了。
10. **「Smart Window 正式在法國推出」→「『開始在法國推出』」。** 更新區塊寫的是 `is now rolling out in France`，
    下一句還是 `People in France **will be able to** download and try the Smart Window beta in French`。
    「正式」對一個仍在 beta、仍在 rolling out 的東西講太滿。
11. **否定句加上範圍與日期**：「以查證範圍來說」→「以 2026 年 9 月 18 日查核的這三頁正文來說」；
    語言那段的「兩份公告都沒有提到」→「三頁都沒有提到」（否定句其實是在三頁上驗的）。
12. **表格兩格**：Mozilla 列的「『規劃』歐洲擴展」補回原文的限定詞 →「『規劃』今年稍後歐洲擴展」；
    8 月更新列的「無新增計畫」→「更新區塊未再提」——那一頁本身有 `What’s next`（瀏覽歷程、代填表單），
    沒有後續的是更新區塊，不是那一頁。
13. **資料那一段與 FAQ 4 補上讀者真正想知道、而官方沒寫的那一項**：對話會不會送到 Mistral 的伺服器處理，三頁都沒寫。
    同一句的「兩份公告」→「三個來源頁面」——三篇正文裡每一個 `<a>` 都列出來看過，
    沒有任何隱私、資料或 AI Controls 的政策文件連結，這個否定句是在三頁上驗的。
14. **第二段刪掉英文標題**〈Mistral x Mozilla: Private, Multilingual AI Browsing〉。
    那是該頁的 `<title>`／`og:title`，但頁面上的 `<h1>` 與 JSON-LD `headline` 都是
    `Mistral and Mozilla are bringing open, private and multilingual AI to your web browser`，
    把前者當成「這篇公告的標題」寫進正文撐不住。`sources[]` 仍保留頁面標題，已在研究紀錄記下這個分歧。
15. **四處純敘述性精簡**（「讀者可以自己比較」「或其他常用軟體」與本次新增句內的兩處縮寫），
    只為了把字數壓回 3,000 以內。**沒有刪掉任何但書、限定詞或歸因**。

## 查過而且正確的部分（沒有動）

- **日期沒有混寫**：三頁分別印 `September 16, 2026`、`September 16, 2026`、`August 18, 2026` 與
  `Update on September 16, 2026`；slug 尾碼、`news_date`、第一段三者一致。沒有任何自己換算出來的日期。
- **兩份市場說法沒有被合併**。Mistral 的句子與 Mozilla 的句子在正文、摘要、表格、圖解四處都分開印、各自標出處，
  沒有任何一處出現合併後的清單——這是這篇最容易出錯的地方，撰稿代理做對了。
- **沒有一句寫成「台灣不能用」**，見 (b)。
- **界線乾淨**：沒有購買或升級建議、沒有推薦式比價、沒有價格、沒有市占或使用者數、沒有跑分數字、
  沒有競爭法或 DMA 的角度、沒有把任何公司點名成 Mozilla「Big Tech」那句話的對象。
  廠商宣稱一律帶「Mistral 表示」「Mozilla 說明」，並兩度寫明本站沒有實際使用過。
  **一個 callout、info tone、沒有投資免責段落**，符合 AI 垂直規格。
- **預告語氣都還在**：英德是「預計今年稍後」、Mozilla 的歐洲擴展是「規劃」，
  beta 身分在標題區、摘要、表格、callout 與三段正文都寫了。
- **摘要與圖上的數字都在正文出現過**，圖解本身不含任何數字。
- **Exa 與聊天模型分得清楚**，且正確掛在 8 月原文上。
- **`verbatim_quote` 25/25 逐字**，`sources[]` 與研究紀錄的 URL 清單完全一致，`checked_on` 四處一致。

## 留給站主的 4 件事

1. **Mistral 公告裡還有第三個一手來源的不一致，文章沒有印**：它兩次寫這次合作觸及的是
   `people who use Firefox **worldwide**`／`reach their consumers **worldwide**`，
   但自己的市場句只點名四個國家。那是「為什麼不能從沉默推論出『台灣用不到』」最漂亮的例子，
   但 zh-TW 段落已經是 **2,990／3,000**，要塞進去就得砍掉等量的字——這是編輯取捨，查核代理不代決定。
2. **Smart Window 的身世還能再往前推**：8 月原文寫 `Last November, we shared an early concept called “AI Window”`。
   同樣因為字數沒進文章，不是因為可疑。
3. **`sources[]` 第一條的標題是 mistral.ai 的 `<title>`，不是頁面上的 `<h1>`**（兩者不同，見第 14 點）。
   若站上的體例是引用可見大標，內容包與研究紀錄兩處都要換成長的那一串；正文現在不依賴任何一個。
4. **這一頁的位元組數今天出現過三種**（69,671／69,692／69,671）。之後重查請讀正文，不要比大小。

## 自檢

```
OK ai-news-firefox-smart-window-mistral-20260916 zh-TW paragraphs 2990
```

零 FAIL——批次 4.5 的索引標題不改，所以規格允許保留的那兩條 FAIL 這次都沒有出現。

## 結論

`needs_second_round`：15 處已改，其中第 1 點（「換模型」→「多一個模型選項」）動到了骨幹論述，
牽動標題以外的九個位置與圖解節點，依規格第 3 節第 6 項應該再過一輪。
文章本身在 94 條主張逐條核對後沒有留下無來源的句子。

---

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 四處一致，**不改**）。
範圍照 `agents/ai/SECOND-ROUND.md`：第一輪**改動過的每一個段落**與**新寫進去的每一句**，逐句回 `sources[]` 原文。
三條來源全部自己重抓（`curl -sL -A "Mokaair-editorial"`，任何 UA、標頭、查詢字串、表單都沒有帶 email、姓名或個人資料），
三頁都是 HTTP 200 且拿到正文：mistral.ai **243,456** bytes、合作公告 **69,692** bytes、8 月原文 **71,906** bytes。
合作公告這個數字是同一天的**第四個**——它回到撰稿代理記的那一個，再次證實 `live_data_warnings` 的結論：
**位元組數只是「抓到了沒有」，不是版本識別**。

`verbatim_quote` **25/25** 用程式對今天存下的 HTML 做連續字串比對（NFC 正規化＋空白收斂）逐字命中，
含來源自己的錯字 `Mistal’s`（彎引號 U+2019）；**25 條都不含 `...`／`…`／`|`**，沒有把不同段落拼成一條引文的情形。
重新核對 **38 條**主張（15 處第一輪改動、它們新寫出來的句子、4 個 `diagram` 節點、`hero_label`、摘要、表格、5 題 FAQ 答句）。
**又改了 6 處**，其中只有第 1 處是事實錯誤，其餘五處是把否定句收回它真正驗過的範圍。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實。**

### 又改的 6 處

1. **唯一的事實錯誤，在 FAQ 3——第一輪自己新寫的句子把「選模型」放進了 AI Controls。**
   原文寫「也可以在 Firefox 的「AI Controls」裡決定要用哪個模型、或把功能整個關掉」。
   Mozilla 8 月原文是**相鄰但分開的兩句**：
   `Smart Window is optional. You choose when to use it, what browsing context it can use to help with a task, and which AI model you want to use.`
   與 `Firefox’s AI Controls gives you one place to manage Smart Window, including turning it off entirely, so you can easily choose the browsing experience you want.`
   **選模型不是掛在 AI Controls 底下的，掛在它底下的只有關閉。** 值得記一筆的是**正文第三節寫對了**
   （「使用者自己決定…用哪一個 AI 模型，並可在…「AI Controls」統一管理，包含完全關閉」），
   是 FAQ 的複述把兩句併成一句。已改回兩句分開，並點明出處是 8 月原文而不是 9/16 的公告。
2. **「三個來源頁面都沒有附上完整的政策文件連結」對「頁面」不成立**（第四節第 2 段與 FAQ 4）。
   三頁的頁尾或電子報表單都掛著全站的 Privacy Policy 連結。對**正文**才成立，而第一輪的紀錄也說它驗的是正文。
   本輪重新把三篇正文裡每一個 `<a>` 列出來確認：mistral.ai 只連 Smart Window 那篇與 firefox.com；
   合作公告只連 mistral.ai 與 Smart Window 那篇；8 月原文連 firefox.com/smart-window、Mozilla Connect、
   `?view=enable`、Exa 那篇與 AI Window 那篇——**沒有任何隱私、資料保留或 AI Controls 的政策文件**。
   已改成「這三頁的正文都沒有附上完整的政策文件連結」，同句尾的「官方頁面上都沒有寫」→「正文都沒有寫」。
3. **語言那句的「三頁都沒有提到」同一個毛病**（第五節第 2 段）。`正體中文` 確實出現在兩個 Mozilla 頁上——
   在全站電子報的**語言**下拉選單裡（和 Deutsch、Español、Русский 並列），
   正是這份紀錄已經為 Taiwan 國別選單記下的同一個陷阱；拉丁字串 `Chinese` 三頁皆 0。
   已改成「三頁正文都沒有提到」，讓這個否定句在字串層級上也為真，並寫進研究紀錄 `not_said`。
4. **FAQ 1 的「兩份公告都沒有列出排除地區的清單」→「這三頁都沒有」。**
   那句話的前一個子句才剛引用完 8 月原文（第三頁），把否定句限縮在兩頁是自相矛盾；這個否定句是在三頁上驗的。
5. **Mistral 對產品的描述被悄悄改窄又加了時間副詞**（第一節第 2 段）。
   原文 `remember something important you clicked away from`：沒有「剛」，而且是 `something important` 不是「頁面」。
   已改成「記得使用者點開後又離開的重要內容」。
6. **圖解節點 4「仍可改用其他模型」→「仍可選用其他模型」。**
   說法本身正確（`Firefox users can still choose from a multitude of other AI models`），
   但「改用」是第一輪從正文清掉的那組換模型動詞最後殘留的一處，且「選用」與正文「仍可以…中選擇」同一個詞。

### 覆核第一輪、確認無誤（沒有再動）

- **骨幹改寫在九個位置都站得住，而且彼此不矛盾。** 今天在完整上下文中重讀 Mozilla 那一段：
  `Mistral Small 4 is coming to Firefox Smart Window beta …, becoming a new AI model for Smart Window users in the US and Canada, while expanding Smart Window beta access and French-language support to Firefox users in France.`
  緊接著就是 `Across all markets where Smart Window beta is available, Firefox users can still choose from a multitude of other AI models.`
  第一段、摘要 2／3、第一節標題、第一節第 1／3 段、第二節第 1 段、第三節第 3 段、FAQ 2、表格 Mozilla 列與圖解節點全部一致。
  第一輪的 Mozilla Connect 佐證也成立：Mozilla 從 8 月原文連出去的那串解析為
  `…/smart-window-expands-to-france-with-mistral-as-a-new-model/m-p/138422/thread-id/56209`。
- **指派點名的三句逐字對得上**：「多一個模型選項」對 `a new AI model`；「仍可選其他模型」對 `can still choose from a multitude of other AI models`；
  「可在 AI Controls 完全關閉」對 `including turning it off entirely`。
- **全篇沒有自生日期**。掃過每一個讀者看得到的字串（title、description、段落、摘要、標題、表格、caption、FAQ、callout、連結文字），
  日期只有 2026-09-16、2026-08-18、2026-09-18 三種；文章裡每一個「起」都是「一起」或「存起來」，**沒有任何「9 月 16 日起」**。
- **`Mistral Small 4` 在 mistral.ai 的原始 HTML 剛好 2 次，兩次都在全站「Latest models」導覽卡片**
  （與 Mistral OCR 4／Medium 3.5／Voxtral TTS 並列），**公告內文 0 次**；內文的模型講法只有 `now powered by Mistral models`。
  正文那句限縮寫法與今天頁面上的事實一致。
- **8 月的開放範圍句自始至終被當成「列入清單」**。第五節與 FAQ 1 都連同 Mozilla 自己的條件句一起印
  （`If it’s not available where you are yet, you can sign up to be notified when it is`），然後當場拒絕那個推論。
  **整個內容包沒有任何一句寫成或暗示「台灣不能用」。**
- **`sources[].title` 三條在內容包與研究紀錄之間完全一致，每一串都是頁面上真有的字串。**
  mistral.ai 那條用的是 `<title>`／`og:title`，而該頁 `<h1>` 與 JSON-LD `headline` 是另一串——維持第一輪的處置，沒有自行更動（理由見下）。
- **圖解與正文一致**：節點 1 對 Mistral 的市場句、節點 2 對 Mozilla 的、節點 3 對台灣／亞洲的否定句、節點 4 對「仍可選其他模型」；
  `diagram.caption` 與內容包 image caption 逐字相同，`hero_label` 對得上第三節標題，圖上沒有任何數字。
- **界線再掃一次乾淨**：`topics` 不含 `finance`、只有一個 info callout、沒有投資免責段落、沒有購買／升級／訂閱／投資建議、
  沒有推薦式比價、沒有價格、市占、使用者數或跑分、沒有競爭法與 DMA 角度、沒有點名 Mozilla「Big Tech」那句話的對象。
  廠商宣稱全部有歸因，預告語氣全部保留（英德「預計今年稍後」、Mozilla 歐洲擴展「規劃」）。
  **本輪的增補沒有刪掉任何但書、限定詞或歸因**；騰出來的字是把 6 個字的「三個來源頁面」換成同長度寫法、
  以及把「官方頁面上」縮成「正文」得來的。
- **「是多一個選項，不是把原本的換掉」這句刻意保留。** 它是緊接在自己引號裡的原文之後的白話複述，
  而且 Mozilla 同一段就寫了使用者仍可選別的模型，兩句合起來直接支撐它；沒有改。

### 留給站主（第一輪 4 件，本輪把第 3 件變成一行決定）

1～2、4 沿用第一輪（`worldwide` 的第三個一手矛盾、`AI Window` 的身世、位元組數不可當版本識別）。
**第 3 件現在不必再猶豫**：`sources[]` 另外兩條**已經都在引用 `<h1>` 而不是 `<title>`**——
Mozilla 合作公告的 `<title>` 是 `Mozilla and Mistral partner to expand AI competition, user choice`，
`sources[]` 收的卻是 `<h1>`；8 月原文的 `<title>` 是 `Smart Window, privacy-first, AI-powered browsing with Firefox`，
`sources[]` 收的也是 `<h1>`。**三條裡二比一偏向 `<h1>`，只有 mistral.ai 那條例外。**
兩串都是頁面上真有的字串、內容包與研究紀錄也一致，所以本輪沒有自行更動；
站主若確認體例是可見大標，要改的就一處：`sources[0].title` 改成
`Mistral and Mozilla are bringing open, private and multilingual AI to your web browser`，**兩個檔都要改**。

### 自檢

```
OK ai-news-firefox-smart-window-mistral-20260916 zh-TW paragraphs 2993
```

零 FAIL（批次 4.5 索引標題不改、第二個連結指向既有文章，所以規格允許保留的兩條 FAIL 都沒有出現）。
段落字數 2,990 → **2,993／3,000**，仍在上限內。

### 結論

`ok`。第一輪的骨幹改寫經逐句回原文覆核後成立，九個位置一致、圖解與正文一致、沒有自生日期。
本輪再改的 6 處裡只有 FAQ 3 是事實錯誤（AI Controls 被寫成可以選模型），其餘五處是把否定句收回驗過的範圍。
沒有留下無來源的句子，也沒有需要站主先裁決才能發布的事項。
