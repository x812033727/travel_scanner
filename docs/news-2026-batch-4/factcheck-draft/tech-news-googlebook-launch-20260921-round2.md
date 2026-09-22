# tech-news-googlebook-launch-20260921 查核報告（第二輪）

- 查核者：獨立查核代理（第二輪），沒有參與撰稿，也沒有參與第一輪
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-googlebook-launch-20260921.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-googlebook-launch-20260921.json`
- 第一輪報告：`docs/news-2026-batch-4/factcheck-draft/tech-news-googlebook-launch-20260921.md`
- 垂直：科技（`tech` / `tech-news` / `gadgets`）、`display_order` 321、`news_date` 2026-09-21
- 查了 88 條句級主張，改了 9 處（4 項協調者裁定共 8 處，外加 1 處來源忠實度修正），沒有任何主張因為找不到來源被整句刪除

## 1. 我自己重抓的來源（不沿用第一輪的檔案）

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機之間間隔 2 秒；UA、標頭、查詢字串、表單、暫存檔名都沒有帶入任何人的姓名、email 或個人資料。

| # | 來源 | HTTP | bytes | 與紀錄 | 與第一輪的抓取 | 與撰稿代理留存的原始檔 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 預購公告 `.../googlebook/pre-order-googlebook/` | 200 | 376,349 | 一致 | 逐位元組相同 | 逐位元組相同 |
| 2 | 外觀設計 `.../googlebook/first-look-googlebook/` | 200 | 380,829 | 一致 | 逐位元組相同 | 逐位元組相同 |
| 3 | 內建智慧 `.../googlebook/googlebook-built-in-intelligence/` | 200 | 372,293 | 一致 | 逐位元組相同 | 逐位元組相同 |
| 4 | 5 月發表文 `.../platforms/android/meet-googlebook/` | 200 | 385,384 | 一致 | 逐位元組相同 | 只差 `days_since_published` 132→133 的分析計數，正文未變 |

另外獨立抓了一次 `https://blog.google/products-and-platforms/devices/googlebook/`（200／381,521 B），
只用來驗證協調者裁定一的前提，沒有拿它補任何事實。

**研究紀錄 59 條 `verified_facts` 的 `verbatim_quote`，對我自己的抓取做連續子字串比對：59／59 命中、0 落空**
（去 `<!-- -->`、`html.unescape` 之後）；四條 `sources[]` 自己的 `verbatim_quote` 也全部命中。
**沒有任何一條引文含 `...`、`…` 或 `|`**，所以不存在「把不同段落拼成一句」的問題——這是第二輪規格第 2 點特別要查的，結果是乾淨的。
`checked_on`（內容包四條 sources、研究紀錄、正文第二段、表格 caption、圖解 caption）五處一致且等於我實際重抓的
2026-09-23，依規格不動。

## 2. 第一輪那 12 處改動的覆核：**12 處全部成立，沒有一處需要回退**

逐條回到我自己抓的正文：

| 第一輪的改動 | 一手來源原文 | 覆核 |
| --- | --- | --- |
| 「起價機型隨附」→「每一台 Googlebook 都隨附」（3 處） | `Starting at $899, every Googlebook includes 12 months of Google AI Pro...`／`a complimentary year of GeForce NOW included with every purchase` | **成立，而且有旁證**：同一頁前面還有一句同構的 `Starting at $899, every Googlebook features premium materials like aluminum, magnesium alloy, and carbon fiber`。同一個句型在同一頁用了兩次，`every Googlebook` 兩次都指全系列，不是指起價那一款 |
| 「例行功能更新」→「例行功能更新與各項更新」（2 處） | `regular feature drops and updates for up to 10 years` | 成立。`feature drops` 與 `updates` 是兩項；改後也沒有踩到 `not_said` 第 14 條（沒有寫成安全更新） |
| 「機身材質是…」→「…等高階材質」 | `made from premium materials **like** aluminum, magnesium alloy, and carbon fiber` | 成立。預購文寫同一件事也用 `features premium materials like ...`，兩篇都是 `like` 起頭的舉例 |
| 「全系列唯一的翻轉機」→「首波五款中唯一的翻轉機」（2 處） | `The sole convertible **in the lineup**` | 成立。`the lineup` 的先行詞是同一節開頭的 `five flagship models`，不是整條產品線 |
| 表格 Dell 列補回「重量」 | `its height, weight, and display are perfectly balanced` | 成立。三項就是三項 |
| 「背景代理 Gemini Spark」→「Gemini Spark 還會在背景…」 | `You can even close your laptop while Gemini Spark works in the background to process complex requests and finish your tasks.` | 成立。四篇官方文沒有一處把 Spark 稱為「代理」（`agent` 只出現在 `AI agent development platform` 與 `autonomous agents` 這兩個別的東西上） |
| 離線觀看不再只掛 HBO Max | `watch shows on popular streaming platforms like Netflix and HBO Max **with offline viewing supported**` | 成立。`offline` 在四篇裡只出現一次，就是這一處，掛的是整個串流子句 |
| GeForce NOW 對應 AAA 大作 | `explore thousands of Android games **or** play AAA titles with a complimentary year of GeForce NOW included with every purchase.` | 成立。`with...` 介系詞片語掛在 `play AAA titles` 上；前一段才剛講完 Play 商店的 App |
| summary 第 3、4 條補上「Google 表示」 | `must_not_write` 第 7 條 | 成立。補完之後全篇歸因密度仍在上限內（見第 5 節） |

**第一輪新寫進去的每一句都逐字回過一手來源**（上表右欄就是那些句子的依據），沒有一句帶進來源沒寫的東西，
也沒有一句為了塞字數刪掉 `up to`／`over`／「預計」這類限定詞：改後全篇「最長／最高／超過」一個都沒少
（14 小時、16 小時、2.8K、32GB、10 年、45 TOPS、六顆喇叭前面的限定詞全在）。

## 3. 本輪改的 9 處

### 3.1 協調者裁定一：三處「去 Googlebook 分類頁看」改成「回預購公告的 Pricing 小節看」

先自己驗過裁定的前提：`https://blog.google/products-and-platforms/devices/googlebook/` 今天 200／381,521 B，
但**伺服器送出的 HTML 裡三篇 9 月文的 slug 與標題各出現 0 次**（`pre-order-googlebook`、`first-look-googlebook`、
`googlebook-built-in-intelligence` 都是 0），只列到 5 月那一篇 `Introducing Googlebook, designed for Gemini Intelligence`，
其餘要靠頁面自己的 `load-more`。同時確認 `Pricing, availability, and pre-order details` 這個小節標題
**確實存在於 9 月三篇**（5 月發表文沒有），上市名單與 $899 都印在那一節。

- 正文第一節（`block6`）：
  - 改前 `…這幾頁都沒有寫台灣的上市時程，讀者之後可以自行到 blog.google 的 Googlebook 分類頁確認有沒有更新。`
  - 改後 `…這幾頁都沒有寫台灣的上市時程；上市名單就印在預購公告的 Pricing, availability, and pre-order details 一節，讀者之後可以回那一節確認有沒有更新。`
- FAQ 第 1 題：
  - 改前 `想確認最新狀況，可以直接到 Google 官方部落格的 Googlebook 分類頁查看有沒有更新。`
  - 改後 `想確認最新狀況，可以回到 Google 官方部落格的預購公告，上市名單就印在那一篇的 Pricing, availability, and pre-order details 一節。`
- callout：
  - 改前 `…可以直接到 Google 官方部落格的 Googlebook 分類頁查看是否已有更新；`
  - 改後 `…可以回到 Google 官方部落格的預購公告，上市名單就印在那一篇的 Pricing, availability, and pre-order details 一節；`
- 來源：`https://blog.google/products-and-platforms/devices/googlebook/pre-order-googlebook/`
- 改完全篇「分類頁」0 次。

### 3.2 協調者裁定二：`hero.alt` 不得帶清點數字

- 改前：`…右側是一張以色塊分區的地圖剪影，七個色塊標示美國與另外六個上市市場的相對位置，台灣的位置留白未上色…`
- 改後：`…右側是一張以色塊分區的地圖剪影，美國與加拿大、英國、愛爾蘭、法國、德國、澳洲各以一個色塊標示相對位置，台灣的位置留白未上色…`
- 裁定只點名「六個」，但「七個色塊」是同一個清點數字換個說法（7 = 美國 + 6），照
  `unverified_or_excluded` 第 2 條與 `must_not_write` 第 21 條的用意一併拿掉，改成**把市場名字列出來、不給任何總數**。
  改完 `hero.alt` 裡「六個」「七個」各 0 次，長度 104 字。
- `hero_label`（`預購開跑，台灣不在名單`）、圖解四格與研究紀錄的 `diagram.nodes` 本來就沒有這個問題，沒有動。

### 3.3 協調者裁定三：刪掉兩句查證紀律

- 安全段（`block23`）：`…或執行自主代理；筆電品類首見是 Google 自己的說法，本站沒有查證其他廠商是否也有同等認證。`
  → `…或執行自主代理；筆電品類首見是 Google 自己的說法。`
  保留前半句，是因為 `must_not_write` 第 9 條要求把 `a first for the laptop category` 寫成 Google 的宣稱；
  刪掉的只有查證紀律那半句。
- FAQ 第 5 題：`…使用者也可以直接把它關掉；這是 Google 官方的說法，本站沒有另外測試驗證。`
  → `…使用者也可以直接把它關掉。`
  這一題的答案本來就以「Google 說明」開頭，歸因沒有掉。
- 改完全篇「本站」0 次、「本文」0 次。

### 3.4 本輪自己抓到的一處：Antigravity 的「自稱的」

- 改前：`開發者另外用得到 Antigravity 這個自稱的 AI 代理開發平台`
- 改後：`開發者另外用得到 Antigravity 這個 Google 自家的 AI 代理開發平台`
- 原文（預購公告）：`Googlebook includes Antigravity, **our** AI agent development platform`；
  內建智慧那篇另寫 `Google Antigravity comes with every Googlebook`。
- 為什麼算事實不算文風：`our` 是所有格，不是存疑的限定詞。「自稱的」等於替 Google 的自我描述加上一個原文沒有的
  懷疑語氣，方向與整篇「宣稱要歸因、但不要替來源加料」的原則相反。第一輪把它列為文風建議沒有改；
  它落在第一輪改過的同一段（GeForce NOW 那一段），依第二輪規格第 1 點屬於必須覆核的範圍，所以本輪改掉。
  歸因密度不受影響（那一段的歸因短語仍只有一個「Google 表示」）。

### 3.5 協調者追加裁定：刪掉第二段最後那句查證紀律，歸因往下移

追加裁定（工作中收到）：把第二段剩下的那句「這一篇沒有實機測試…」刪掉，
它原本承載的歸因，若最近的規格主張會因此變成沒有歸因，就補一個「Google 表示」上去。

- 第二段：
  - 改前 `這一篇的資料在 2026 年 9 月 23 日查核，讀的是…以及 5 月 12 日的發表文；這一篇沒有實機測試，規格與功能一律是 Google 官方頁面自己的說法，也不提供購買或升級建議。`
  - 改後 `這一篇的資料在 2026 年 9 月 23 日查核，讀的是…以及 5 月 12 日的發表文。`
  - 刪掉的那句同時帶著「不提供購買或升級建議」，但 callout 裡本來就有一模一樣的一句
    （`這一篇不提供購買或升級建議`），這條界線沒有掉。
- 歸因往哪裡移：刪掉那句總括歸因之後，逐段清點**只有電池那一段（`block10`）沒有「Google 表示」**——
  其餘規格段（`block8` 五款機型與處理器、`block9` 記憶體螢幕喇叭、`block21`／`block23`／`block24`）本來就各有一個。
  而 `must_not_write` 第 7 條偏偏把「電池」列進一律要掛「Google 表示」的清單，所以補在那裡：
  - 改前 `電池方面，外觀設計那篇寫最長 14 小時影片播放、16 小時網頁瀏覽，預購那篇的說法較籠統，只寫最長 14 小時電池續航，…`
  - 改後 `電池方面，Google 表示最長 14 小時影片播放、16 小時網頁瀏覽，這是外觀設計那篇的寫法；預購那篇較籠統，只寫最長 14 小時電池續航，…`
  - 來源沒變：`Battery: up to 14 hours of video playback and 16 hours of web browsing`（外觀設計）與
    `up to 14 hours of battery life`（預購）；「最長」兩處都還在，「兩篇都沒有列出測試機型或螢幕亮度等條件」也還在。
- 改完該段的歸因短語是 1 個（「Google 表示」），沒有一段超過上限；
  「外觀設計那篇／預購那篇」是指出數字出自哪一篇官方文的來源標示，不是「X 表示」型的歸因短語，不計入。
- 字數 2,806 → **2,769**，仍在 1,800–3,000 內；`check_article.py` 要求的查核日仍在第二段句首、事件日仍在第一段。

## 4. 隨機抽驗的 25 條（種子 20260923，抽自第一輪確認的 77 條）

抽到 `2, 4, 5, 6, 8, 18, 28, 30, 34, 39, 43, 45, 51, 54, 56, 59, 63, 65, 71, 74, 75, 78, 80, 81, 87`，
**25 條全部 CONFIRMED，0 條需要改**。其中值得記下來的幾條：

- **#8「同步發出三篇文章」**：三篇 9 月文的 JSON-LD `datePublished` 是同一秒 `2026-09-21T13:00:00+00:00`，
  「同步」不是修辭。
- **#5／#9「台灣不在名單上」（全篇最重要的一條）**：四篇正文裡 `Taiwan` 出現 **0 次**；
  「台灣」只出現 2 次，兩次都在頁尾的語言／地區版本選單（同一份清單裡還有 `ประเทศไทย (ไทย)`、`Türkiye (Türkçe)`、
  `New Zealand (English)`）。草稿沒有拿它當任何依據，否定句也一律限縮在「這幾頁沒有寫」。
- **#22（順帶再驗）OLED 只在預購那篇**：`OLED` 在預購文出現 1 次、在外觀設計／內建智慧／5 月文各 0 次，
  正文寫「只有預購那篇把這片螢幕寫成 OLED」正確。
- **#21（順帶再驗）MediaTek**：`MediaTek` 只在外觀設計出現 1 次（`We teamed up with Intel, Qualcomm, and MediaTek`），
  上市可選處理器那句沒有它，正文的寫法正確。
- **#63 Chromebook**：四篇正文裡 `Chromebook` 只在 5 月文出現一次（`Over 15 years ago, we introduced the Chromebook...`），
  其餘都是頁首導覽選單。FAQ 第 3 題寫「官方頁面沒有說明這會不會影響 Chromebook 既有產品線」正確。
- **#77／#80／#83／#86 四條 sources 的 title**：與各頁的 `og:title`／JSON-LD `headline` **逐字相同**
  （四頁的 `<title>` 是另一組行銷用標題，內容包用的是文章標題那一組，正確）。
- **#75 第二個結尾連結的 text**：與 `tech-news-windows-project-zenith-20260904` 的 zh-TW `title`
  `微軟發布 Project Zenith：Windows 開發機的統一記憶體與頻寬門檻` 逐字相同；
  #73／#74 的索引標題與網址也與 DELTA-4-7 第 6 條逐字相同。
- **#4 `gadgets`**：`apps/api/app/guides/taxonomy.py` 第 196 行有登記。

## 5. 界線與讀者優先的再掃（第二輪規格第 3–5 點）

- **`summary` ⊆ 正文**：五條 summary 的每個數字（$899、45 TOPS、12 個月、10 年、10/4、10/5）在正文都有；
  `check_article.py` 自己的「summary 說了而正文沒說的數字」檢查也過。
- **FAQ 的答案 ⊆ 正文、圖解 nodes 的數字都在正文**：過（`check_article.py` 的 `missing_diagram_numbers`）。
- **否定句**：全篇的「官方沒有寫／這幾頁沒有寫」一律限縮到「這一篇引用的這幾頁、2026 年 9 月 23 日」，
  沒有一句寫成「Google 沒有要在台灣賣」。
- **界線**：`topics` 沒有 `finance`，只有一個 callout、沒有投資免責 callout；沒有購買／升級／訂閱建議；
  沒有換算新台幣；沒有引用 `googlebook.google`／`googlebook.com`；沒有出現只在頁首 AI 摘要裡的
  `select countries`（該字串只在內建智慧那篇的摘要區塊出現 1 次，正文四處市場名單都來自 `Pricing` 小節）；
  沒有寫成取代 Chromebook；沒有與站上既有 AI 文章矛盾（Gemini Spark 只帶一句，沒有重寫
  `ai-news-gemini-spark-20260519` 的架構分析）。
- **歸因密度**（協調者核可的規則）：開場段 1 個歸因短語（`Google 公布`），
  其餘每段最多 2 個（只有安全那段是 2：`Google 表示` + `Google 自己的說法`），**沒有一段超標**。
  改完全篇「官方」30 次、「Google 表示」15 次，2,769 字。
- **讀者優先**：「本文」0 次、「本站」0 次（本輪裁定三刪掉的就是那 2 次）；
  `description` 163 字、句尾只帶「（2026 年 9 月查證）」；標題與 description 沒有編輯清點數字
  （「五款」是官方自印的 `five flagship models`）；第一段就講清楚台灣在不在名單上。

## 6. 留給協調者與站主的事

1. ~~正文第二段還留著一句同類的話~~ **已由協調者追加裁定解決**（見 3.5）：那一句已刪，
   它承載的總括歸因改以「Google 表示」補在電池那一段；`check_article.py` 與 lint 都重跑過，結果不變。
2. **研究紀錄有兩條措辭與內容包不一致，兩輪都沒有動**（那是撰稿當時的證據紀錄，改掉會失去追溯性）：
   `verified_facts` 第 39 條把離線觀看寫成「Netflix、HBO Max（支援離線觀看）」，第 10 條把 Acer 寫成
   「全系列唯一的翻轉機」。原文分別是 `...like Netflix and HBO Max with offline viewing supported` 與
   `The sole convertible in the lineup`；內容包兩處都已由第一輪改正、本輪覆核無誤。要不要在紀錄上加註，請協調者決定。
3. **主圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug。構圖請照改後的 `hero.alt`——
   **圖上不可以出現「六」或「七」這種清點數字**，要嘛列出市場名字、要嘛不給總數。
4. **`pack_cli relink` 還沒跑**：兩個結尾連結目前仍是 raw URL（lint 的 `raw_internal_url` 警告）。

## 7. 自檢輸出（原樣）

```
OK tech-news-googlebook-launch-20260921 zh-TW paragraphs 2769
check_article exit=0
```

```
tech-news-googlebook-launch-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-googlebook-launch-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-googlebook-launch-20260921/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

只剩規格預期的 `image_missing`（圖還沒畫）與 `raw_internal_url`（還沒 relink）。
字數 2,784 → 2,769（追加裁定後），仍在 1,800–3,000 內；`title` 38 字、`description` 163 字；兩個檔案都是 LF、檔尾一個換行、非 ASCII 未跳脫，
研究紀錄加上 `factcheck.second_round` 之後仍然 parse 得過。

## 8. 結論

**`ok`。** 本輪改了 **9 處**：協調者四項裁定共 8 處（分類頁導引 3 處、`hero.alt` 1 處、查證紀律 2 處、追加裁定的第二段刪句與電池段補歸因 2 處），
加上 1 處本輪自己抓到的來源忠實度問題（`our` 被譯成「自稱的」）。
**第一輪那 12 處改動逐條回一手來源覆核，12 處全部成立，沒有一處需要回退**；
它新寫的每一句也都對得上原文，沒有為了字數刪掉任何限定詞或歸因。
研究紀錄 59 條 `verbatim_quote` 對我自己的抓取 59／59 命中、0 條引文是拼接的。
沒有任何主張因為找不到來源被整句刪除，本篇不需要第三輪。

## 9. 完整主張表（88 條）

「主張（節錄）」欄位引的是**第二輪開始時**的文字，所以標成 CHANGED 的那幾列看到的是改前的原文；
改後的文字在第 3 節。

| # | 位置 | 主張（節錄） | 本輪處理 | 判定 | 依據（一手來源原文／今天重抓） |
| --- | --- | --- | --- | --- | --- |
| 1 | `meta:slug` | tech-news-googlebook-launch-20260921 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | slug 後綴 20260921 = news_date = 第一段的 2026 年 9 月 21 日 |
| 2 | `meta:news_date` | 2026-09-21 | 隨機抽驗 | CONFIRMED | 三篇 9 月文 JSON-LD 都是 2026-09-21T13:00:00+00:00，台北 21:00 同日 |
| 3 | `meta:display_order` | 321 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | DELTA-4-7 第 5 條的表：科技接 321 起，本篇第一篇 |
| 4 | `meta:topics` | tech,tech-news,gadgets | 隨機抽驗 | CONFIRMED | taxonomy.py 第 196 行登記 gadgets；tech／tech-news 同檔 |
| 5 | `title` | Googlebook 開放預購：10 月 4 日起在美國上架，台灣不在名單上 | 隨機抽驗 | CONFIRMED | pre-orders begin September 21／on shelves October 4；四篇正文 0 個 Taiwan |
| 6 | `description` | 2026 年 9 月 21 日，Google 開放預購 5 月發表的筆電新品類 Googlebook，10 月 … | 隨機抽驗 | CONFIRMED | 市場名單、$899、five flagship models；163 字、句尾（2026 年 9 月查證） |
| 7 | `hero.alt` | 原創插圖：畫面左側是一個抽象的筆電幾何外框，右側是一張以色塊分區的地圖剪影，七個色塊標示美國與另外六個上市市場的… | 裁定覆核＋改寫 | **CHANGED（本輪）** | 改：市場名字照 Pricing 小節列出，不給任何總數 |
| 8 | `block1:paragraph` | 2026 年 9 月 21 日，Google 在官方部落格同步發出三篇文章，宣布 5 月 12 日發表的筆記型電… | 隨機抽驗 | CONFIRMED | 三篇 datePublished 同一秒，「同步發出」成立 |
| 9 | `block1:paragraph` | Google 公布的這份上市名單沒有台灣，四篇官方文章也都沒有提到台灣的上市時程、售價或預購通路。 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 四篇正文 0 個 Taiwan；「台灣 (中文)」只出現在頁尾語言選單 |
| 10 | `block2:paragraph` | 這一篇的資料在 2026 年 9 月 23 日查核，讀的是 Google 官方部落格同日發出的預購公告、外觀設計… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 查核日 2026-09-23 = 我實際重抓那一天；checker 要求前兩段出現查核日 |
| 11 | `block3:summary[1]` | Google 在 2026 年 9 月 21 日開放預購 5 月 12 日發表的新筆電品類 Googlebook… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | October 4 in the U.S., and October 5 in Canada, the U.K., Ireland, France, Germany, and Australia（三篇一致） |
| 12 | `block3:summary[2]` | 官方公布的上市名單沒有台灣，官方頁面也沒有提到台灣的上市時程、售價或預購通路。 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 否定句限縮在「這幾頁沒有寫」 |
| 13 | `block3:summary[3]` | Google 表示首波五款機型由 Acer、ASUS、Dell、HP 與 Lenovo 打造，起價 $899，處… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | five flagship models…starting at $899；At launch, you can choose between Intel Core Ultra Series 3 and Snapdragon X Elite…over 45 TOPS。第一輪補的「Google 表示」成立 |
| 14 | `block3:summary[4]` | Google 表示 Gemini 功能 Magic Pointer、Rambler、Create My Widg… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | 三個功能名與 It only springs into action when summoned by a wiggle。第一輪補的「Google 表示」成立 |
| 15 | `block3:summary[5]` | Google 表示每一台 Googlebook 都隨附 12 個月 Google AI Pro，Googlebo… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | Starting at $899, every Googlebook includes 12 months of Google AI Pro…；regular feature drops and updates for up to 10 years |
| 16 | `block4:heading` | 5 月發表、9 月預購：時間線與上市名單怎麼讀 | 結構／提問 | OUT OF SCOPE |  |
| 17 | `block5:paragraph` | Google 把 Googlebook 定位成建在 Android 技術堆疊上、搭配來自 ChromeOS 桌面… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | Built on the Android technology stack and paired with desktop foundations from ChromeOS；stay tuned as we will share more when devices become available this fall |
| 18 | `block6:paragraph` | 預購從 9 月 21 日起在 Google Store、Best Buy 與其他部分零售商開放，這幾頁沒有寫預購… | 隨機抽驗 | CONFIRMED | Pre-orders are now open on the Google Store, Best Buy, and other select retailers. |
| 19 | `block6:paragraph` | 以 2026 年 9 月 23 日查核，這幾頁都沒有寫台灣的上市時程，讀者之後可以自行到 blog.google… | 裁定覆核＋改寫 | **CHANGED（本輪）** | 改：Pricing, availability, and pre-order details 這個小節標題今天確實在預購文裡 |
| 20 | `block7:heading` | 五款機型、$899 起：規格與定價 | 結構／提問 | OUT OF SCOPE |  |
| 21 | `block8:paragraph` | Google 表示首波推出五款旗艦機型，分別由 Acer、ASUS、Dell、HP 與 Lenovo 打造，起價… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | five flagship models…$899；At launch, you can choose between…；We teamed up with Intel, Qualcomm, and MediaTek；MediaTek 全站只在 first-look 出現 1 次、不在上市清單 |
| 22 | `block9:paragraph` | Google 表示 Googlebook 全系列記憶體基線 16GB、部分機型最高上看 32GB，機身採用鋁、鎂… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | premium materials like…；up to 2.8K resolution…without a glare；OLED 只在預購文出現 1 次；up to six speakers with Dolby Atmos |
| 23 | `block9:paragraph` | 機身上的燈條 Glowbar 回歸，開機時有動態、可掃出電量，並開放給開發者製作自訂的互動動畫。 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | We are also opening Glowbar access to developers…；lights up at startup, sweeps to show your battery charge level |
| 24 | `block10:paragraph` | 電池方面，外觀設計那篇寫最長 14 小時影片播放、16 小時網頁瀏覽，預購那篇的說法較籠統，只寫最長 14 小時… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | up to 14 hours of video playback and 16 hours of web browsing／up to 14 hours of battery life；兩篇都沒有測試條件 |
| 25 | `block10:paragraph` | 五款機型裡，官方頁面只具體寫了三項：Acer 是首波五款中唯一的翻轉機、ASUS 寫重 2.2 磅、Lenovo… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | The sole convertible in the lineup／2.2 pounds／15-inch display；Dell 與 HP 只有形容詞 |
| 26 | `block11:table[r1c1]` | Acer | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 27 | `block11:table[r1c2]` | 首波五款中唯一的翻轉機 | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | The sole convertible in the lineup ——「in the lineup」指這次的五款 |
| 28 | `block11:table[r1c3]` | 官方未列出 | 隨機抽驗 | CONFIRMED | Acer 那一行沒有任何數字 |
| 29 | `block11:table[r2c1]` | ASUS | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 30 | `block11:table[r2c2]` | 官方形容為羽量級的旅行良伴 | 隨機抽驗 | CONFIRMED | ASUS: Feather-light at just 2.2 pounds, it is the ultimate travel companion |
| 31 | `block11:table[r2c3]` | 2.2 磅，官方未給公制換算 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 32 | `block11:table[r3c1]` | Dell | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 33 | `block11:table[r3c2]` | 外型大膽，強調高度、重量與螢幕的平衡 | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | its height, weight, and display are perfectly balanced（三項） |
| 34 | `block11:table[r3c3]` | 官方未列出 | 隨機抽驗 | CONFIRMED | Dell 那一行沒有任何數字 |
| 35 | `block11:table[r4c1]` | HP | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 36 | `block11:table[r4c2]` | 外型簡約優雅 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 37 | `block11:table[r4c3]` | 官方未列出 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 38 | `block11:table[r5c1]` | Lenovo | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 39 | `block11:table[r5c2]` | 訴求生產力的大螢幕機型 | 隨機抽驗 | CONFIRMED | Lenovo: With a spacious 15-inch display built for productivity, it is the ultimate workhorse |
| 40 | `block11:table[r5c3]` | 15 吋螢幕（五款中唯一列出的尺寸） | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 41 | `block11:table.caption` | 五款首發機型官方頁描述的特色與規格數字，查核日 2026 年 9 月 23 日。 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 表格三欄全部回到 first-look 的五行；查核日與四處一致 |
| 42 | `block12:heading` | 跟 Android 手機連動：搬家、接續與跨裝置操作 | 結構／提問 | OUT OF SCOPE |  |
| 43 | `block13:paragraph` | Google 表示，使用者登入 Googlebook 時，Android 手機的設定、已儲存的密碼、Wi-Fi … | 隨機抽驗 | CONFIRMED | When you sign in, your Android phone’s settings, saved passwords, Wi-Fi networks, and messages will move with you, backed by end-to-end encryption；It starts with setting up your device |
| 44 | `block14:paragraph` | 手機連動另有三個功能：Continue On 讓使用者在手機上開始的工作，直接在筆電的工作列接續處理；Files… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | Continue On／Files／Cast My Apps 三段原文，含 order dinner 與 one-time code 兩個例子 |
| 45 | `block15:image.alt` | 四格圖解：5 月 12 日發表、9 月 21 日開放預購、10 月 4 日起在美國上架，以及台灣尚未列入官方公布… | 隨機抽驗 | CONFIRMED | 四格的數字（5/12、9/21、10/4）都出現在正文 |
| 46 | `block15:image.caption` | 2026 年 9 月 21 日 Google 對 Googlebook 開放預購，與 5 月 12 日的發表文對… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 同上；查核日與四處一致 |
| 47 | `block16:heading` | 三個 Gemini 功能：Magic Pointer、Rambler、Create My Widget | 結構／提問 | OUT OF SCOPE |  |
| 48 | `block17:paragraph` | Magic Pointer 是晃一下游標就能把 Gemini 叫到螢幕上正在看的內容旁邊的功能，Google 說… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | Wiggle your cursor…；It only springs into action when summoned by a wiggle, and stays off；三個例子含 suspicious email |
| 49 | `block18:paragraph` | Google 表示 Rambler 原生支援多語、可以句子講到一半換語言，能把雜亂的口述內容整理成條列重點並自動… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | natively multilingual…switch languages mid-sentence；structured bullet points…add relevant emoji；next to the Quick Insert key；no coding experience required |
| 50 | `block19:paragraph` | Google 表示，Chrome 與 Android 上既有的 Gemini 功能，包括任務自動化、Gemini… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | You can even close your laptop while Gemini Spark works in the background…；四篇都沒有把 Spark 稱為「代理」 |
| 51 | `block20:heading` | 軟體生態、開發者工具與安全設計 | 隨機抽驗 | CONFIRMED |  |
| 52 | `block21:paragraph` | Google 表示 Googlebook 的軟體生態是桌面版 Chrome 瀏覽器（可裝擴充功能）加上 Play… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | desktop-class Chrome browser with extensions；like Adobe Photoshop, Adobe Lightroom, and CapCut；like Netflix and HBO Max with offline viewing supported（掛的是整個串流子句） |
| 53 | `block22:paragraph` | 遊戲與開發者用途上，Google 表示機上有數千款 Android 遊戲可以玩，AAA 大作則靠每台隨附的一年 … | 裁定覆核＋改寫 | **CHANGED（本輪）** | explore thousands of Android games or play AAA titles with a complimentary year of GeForce NOW；our AI agent development platform；full Linux terminal environment…Claude Code or Antigravity CLI |
| 54 | `block23:paragraph` | Google 表示 Googlebook 的安全架構沿用 ChromeOS、以 Google Titan 硬體信… | 裁定覆核＋改寫 | **CHANGED（本輪）** | Google Titan hardware root of trust…；a first for the laptop category: a Level 5 security-certified pKVM hypervisor；isolated Linux environment…execute autonomous agents |
| 55 | `block24:paragraph` | Google 表示，每一台 Googlebook 都隨附 12 個月 Google AI Pro（含 5TB 雲… | 第一輪改動覆核 | CONFIRMED（第一輪改動成立） | Starting at $899, every Googlebook includes…plus 3 months of YouTube Premium, Adobe Photoshop, and more；up to 10 years |
| 56 | `block25:faq[1].q` | 台灣買得到 Googlebook 嗎？ | 隨機抽驗 | CONFIRMED |  |
| 57 | `block25:faq[1].a` | 以 2026 年 9 月 23 日查核，Google 公布的上市名單只有美國（10 月 4 日）與加拿大、英國、… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 市場名單三篇一致；四篇正文 0 個 Taiwan |
| 58 | `block25:faq[1].a` | 想確認最新狀況，可以直接到 Google 官方部落格的 Googlebook 分類頁查看有沒有更新。 | 裁定覆核＋改寫 | **CHANGED（本輪）** | 改：改指預購公告的 Pricing 小節 |
| 59 | `block25:faq[2].q` | Googlebook 是 9 月才發表的新產品嗎？ | 隨機抽驗 | CONFIRMED |  |
| 60 | `block25:faq[2].a` | 不是。 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 61 | `block25:faq[2].a` | Google 在 2026 年 5 月 12 日就已經發表這個筆電品類，9 月 21 日這幾篇文章公布的是開放預… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | May 12, 2026 與 2026-05-12T17:00:00+00:00；Devices arrive on shelves starting October 4 |
| 62 | `block25:faq[3].q` | Googlebook 跟 Chromebook 是什麼關係？ | 結構／提問 | OUT OF SCOPE |  |
| 63 | `block25:faq[3].a` | Google 表示 Googlebook 建在 Android 技術堆疊上、搭配來自 ChromeOS 的桌面基… | 隨機抽驗 | CONFIRMED | Built on the Android technology stack…；四篇裡只有 5 月文的正文提到 Chromebook（Over 15 years ago…），沒有寫兩條產線的關係 |
| 64 | `block25:faq[4].q` | $899 的起價包含什麼？ | 結構／提問 | OUT OF SCOPE |  |
| 65 | `block25:faq[4].a` | Google 表示每一台 Googlebook 都隨附 12 個月 Google AI Pro（含 5TB 雲端… | 隨機抽驗 | CONFIRMED | every Googlebook includes…；included with every purchase；$899 沒有幣別代碼 |
| 66 | `block25:faq[5].q` | Magic Pointer 平常會一直讀取螢幕內容嗎？ | 結構／提問 | OUT OF SCOPE |  |
| 67 | `block25:faq[5].a` | Google 說明 Magic Pointer 只有在使用者晃動游標把它叫出來時才會動作，沒有使用時是關閉狀態，… | 裁定覆核＋改寫 | **CHANGED（本輪）** | It only springs into action when summoned by a wiggle, and stays off；Gemini only acts when you ask it to, and you can switch it off |
| 68 | `block25:faq[6].q` | Rambler 能不能用中文口述？ | 結構／提問 | OUT OF SCOPE |  |
| 69 | `block25:faq[6].a` | 官方頁面只說明 Rambler 原生支援多語、可以句子講到一半切換語言，並沒有列出實際支援的語言清單，因此無法判… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | natively multilingual…without losing a beat；四篇都沒有語言清單 |
| 70 | `block26:callout.title` | 上市名單之後可能再更新 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 71 | `block26:callout.text` | Google 目前公布的上市時間是 10 月 4 日在美國、10 月 5 日在加拿大、英國、愛爾蘭、法國、德國與… | 隨機抽驗 | CONFIRMED | 市場名單；四篇都沒有寫會不會加其他市場 |
| 72 | `block26:callout.text` | 這一篇的資料在 2026 年 9 月 23 日查核，讀者想確認最新狀況，可以直接到 Google 官方部落格的 … | 裁定覆核＋改寫 | **CHANGED（本輪）** | 改：改指預購公告的 Pricing 小節 |
| 73 | `block27:link.text` | 2026 年科技新聞總整理：硬體、平台、電信與法規的重點 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | DELTA-4-7 第 6 條的索引標題，逐字 |
| 74 | `block27:link.url` | https://mokaair.com/zh-TW/life/tech-news-2026-index | 隨機抽驗 | CONFIRMED | DELTA-4-7 第 6 條的索引網址 |
| 75 | `block28:link.text` | 微軟發布 Project Zenith：Windows 開發機的統一記憶體與頻寬門檻 | 隨機抽驗 | CONFIRMED | 與 tech-news-windows-project-zenith-20260904 的 zh-TW title 逐字相同 |
| 76 | `block28:link.url` | https://mokaair.com/zh-TW/life/tech-news-windows-project… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | DELTA-4-7 第 7 條 |
| 77 | `source[1].title` | Googlebook: The laptop your Android phone has been waiti… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | og:title／headline = Googlebook: The laptop your Android phone has been waiting for |
| 78 | `source[1].url` | https://blog.google/products-and-platforms/devices/googl… | 隨機抽驗 | CONFIRMED | 今天 200／376,349 B |
| 79 | `source[1].checked_on` | 2026-09-23 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 80 | `source[2].title` | Premium materials and striking design set Googlebook apa… | 隨機抽驗 | CONFIRMED | og:title／headline = Premium materials and striking design set Googlebook apart |
| 81 | `source[2].url` | https://blog.google/products-and-platforms/devices/googl… | 隨機抽驗 | CONFIRMED | 今天 200／380,829 B |
| 82 | `source[2].checked_on` | 2026-09-23 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 83 | `source[3].title` | Googlebook’s built-in intelligence reinvents the way you… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | og:title／headline = Googlebook’s built-in intelligence reinvents the way you use your laptop |
| 84 | `source[3].url` | https://blog.google/products-and-platforms/devices/googl… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | 今天 200／372,293 B |
| 85 | `source[3].checked_on` | 2026-09-23 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
| 86 | `source[4].title` | Introducing Googlebook, designed for Gemini Intelligence… | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） | og:title／headline = Introducing Googlebook, designed for Gemini Intelligence |
| 87 | `source[4].url` | https://blog.google/products-and-platforms/platforms/and… | 隨機抽驗 | CONFIRMED | 今天 200／385,384 B |
| 88 | `source[4].checked_on` | 2026-09-23 | 第一輪已確認，本輪未重查 | （第一輪 CONFIRMED） |  |
