# tech-news-googlebook-launch-20260921 查核報告（第一輪）

- 查核者：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-googlebook-launch-20260921.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-googlebook-launch-20260921.json`
- 垂直：科技（`tech` / `tech-news` / `gadgets`）、`display_order` 321、`news_date` 2026-09-21
- 查了 104 條主張，改了 12 處（9 個不同的事實／歸因問題），0 條整句刪除

## 1. `sources[]` 今天的重抓結果

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機之間間隔 2 秒；UA、標頭、查詢字串、表單都沒有帶入任何人的姓名、email 或個人資料。

| # | 來源 | HTTP | bytes | 與紀錄的 bytes | 是否讀到正文 | 與撰稿代理留存的原始檔 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 預購公告 `.../googlebook/pre-order-googlebook/` | 200 | 376,349 | 一致 | 是（`Pricing, availability, and pre-order details` 小節、作者職稱、Related stories 都在） | 逐位元組相同 |
| 2 | 外觀設計 `.../googlebook/first-look-googlebook/` | 200 | 380,829 | 一致 | 是（`Five distinctive models` 五款清單、`Memory:`／`Battery:` 兩行都在） | 逐位元組相同 |
| 3 | 內建智慧 `.../googlebook/googlebook-built-in-intelligence/` | 200 | 372,293 | 一致 | 是（Magic Pointer／Rambler／Create My Widget 三節都在） | 逐位元組相同 |
| 4 | 5 月發表文 `.../platforms/android/meet-googlebook/` | 200 | 385,384 | 一致 | 是（Chromebook 開頭、Quick Access、代工夥伴那段都在） | 只差一個 `days_since_published` 分析計數（132→133），正文未變 |

補充驗證（不是 `sources[]`、沒有拿來補任何事實）：正文、FAQ 第 1 題與 callout 三處請讀者回去看的
`https://blog.google/products-and-platforms/devices/googlebook/` 今天同樣以該 UA 取得 200／381,521 B，頁面存在。

**研究紀錄 59 條 `verified_facts` 的 `verbatim_quote` 今天全部命中**：把原始 HTML 去掉 `<!-- -->`、`html.unescape`
之後逐條比對連續子字串，59／59 命中、0 落空；四條 `sources[]` 自己的 `verbatim_quote` 也全部命中。
`checked_on`（內容包四條 sources、研究紀錄、正文第二段、表格 caption、圖解 caption）本來就一致且等於我實際重抓的
2026-09-23，依規格不動。

## 2. 改掉的 12 處

### 2.1 「起價機型隨附」→「每一台 Googlebook 都隨附」（3 處，summary 第 5 條、軟體生態最後一段、FAQ 第 4 題）

- 原文：`起價機型隨附 12 個月 Google AI Pro……並附贈一年 GeForce NOW`
- 改成：`每一台 Googlebook 都隨附 12 個月 Google AI Pro……每一台也都附贈一年 GeForce NOW`
- 來源怎麼寫（預購公告，外觀設計與內建智慧兩篇一字不差地重複同一段）：
  `Starting at $899, every Googlebook includes 12 months of Google AI Pro providing 5TB of cloud storage and our
  Gemini Advanced tools, plus 3 months of YouTube Premium, Adobe Photoshop, and more.`
  GeForce NOW 那句是 `a complimentary year of GeForce NOW included with every purchase.`
- 為什麼：`Starting at $899` 是「價格從 $899 起」，`every Googlebook includes` 的主詞是**全系列每一台**，
  不是起價那一款。草稿把兩個子句接成「起價機型才有」，等於替 Google 加了一個官方沒有的組態限制。
  研究紀錄 `verified_facts` 第 46 條原本就寫對了（「隨機附的訂閱」），是草稿偏離了紀錄。

### 2.2 「例行功能更新」→「例行功能更新與各項更新」（2 處，summary 第 5 條與正文）

- 來源：`Googlebook OS also comes with regular feature drops and updates for up to 10 years.`
- 為什麼：原文是 `feature drops **and updates**` 兩項。研究紀錄 `not_said` 第 14 條明講「官方沒有寫是安全更新
  還是功能更新全包」，草稿只寫「功能更新」會讓讀者以為十年只涵蓋功能更新。`up to`→「最長」與「並非保證十年」
  草稿本來就有，保留。

### 2.3 「機身材質是鋁、鎂合金與碳纖維」→「機身採用鋁、鎂合金與碳纖維等高階材質」

- 來源（外觀設計）：`Every Googlebook is made from premium materials **like** aluminum, magnesium alloy, and carbon fiber`
- 為什麼：`like` 起頭的舉例清單被寫成全清單，違反 `must_not_write` 第 13 條。加「等」即可，不必改句型。

### 2.4 「全系列唯一的翻轉機」→「首波五款中唯一的翻轉機」（2 處，規格段與表格 Acer 列）

- 來源（外觀設計）：`Acer: The sole convertible **in the lineup**, it shifts from laptop to tablet with ease.`
- 為什麼：`in the lineup` 指的是這次上市的五款，草稿的「全系列」把範圍放大成整條 Googlebook 產品線。
  官方沒有說之後不會有第二款翻轉機。

### 2.5 表格 Dell 列補回「重量」

- 原文：`外型大膽，強調高度與螢幕的平衡` → 改成 `外型大膽，強調高度、重量與螢幕的平衡`
- 來源（外觀設計）：`Dell: Bold and flashy, its **height, weight, and display** are perfectly balanced.`
- 為什麼：三項被抄成兩項。Dell 那一款官方沒給任何規格數字，這一行是它唯一的官方描述，漏一項就少三分之一。

### 2.6 「背景代理 Gemini Spark」→「Gemini Spark 還會在背景……」

- 來源（內建智慧）：`You can even close your laptop while Gemini Spark works in the background to process complex
  requests and finish your tasks.`
- 為什麼：四篇官方文都沒有把 Gemini Spark 稱為「代理」，只說它「在背景執行」。站上另一篇
  `ai-news-gemini-spark-20260519` 寫過它的背景代理架構，但那不是這一篇 `sources[]` 裡的東西，
  依規格不可拿來替本篇補事實。

### 2.7 離線觀看不再只掛在 HBO Max 身上

- 原文：`串流服務則有 Netflix、HBO Max（支援離線觀看）等，這是官方舉例的清單`
- 改成：`串流服務則有 Netflix、HBO Max 等並支援離線觀看，以上都是官方舉例的清單`
- 來源（預購）：`watch shows on popular streaming platforms like Netflix and HBO Max **with offline viewing supported**`
- 為什麼：`with offline viewing supported` 掛的是整個串流子句，草稿的括號把它變成「HBO Max 才支援離線觀看」的對比。
  研究紀錄 `verified_facts` 第 39 條自己就是這樣寫的，草稿是照抄紀錄（見第 4 節）。

### 2.8 GeForce NOW 對應到 AAA 大作，不是「數千款 Android 遊戲」

- 原文：`Google 表示每台都附贈一年 GeForce NOW，可用來玩數千款 Android 遊戲或 AAA 大作`
- 改成：`Google 表示機上有數千款 Android 遊戲可以玩，AAA 大作則靠每台隨附的一年 GeForce NOW`
- 來源（預購）：`explore thousands of Android games **or** play AAA titles with a complimentary year of GeForce NOW
  included with every purchase.`
- 為什麼：數千款 Android 遊戲來自 Play 商店（同段前面才剛講完 Play 商店的 App），GeForce NOW 對應的是 AAA 大作。
  草稿把兩件事併成一件，等於宣稱串流服務可以跑 Android 遊戲。

### 2.9 summary 第 3、4 條補上歸因

- 原文：`首波五款機型由 Acer……` ／ `Gemini 功能 Magic Pointer、Rambler、Create My Widget 都內建在 Googlebook 上……`
- 改成：各在句首加一個 `Google 表示`
- 為什麼：`must_not_write` 第 7 條要求處理器、NPU TOPS、記憶體、電池、螢幕、喇叭、更新年限、安全認證一律
  「Google 表示」，而 summary 第 3、4 條把五款機型、$899、Intel／Snapdragon、45 TOPS 與三個 Gemini 功能的行為
  寫成事實。站上既有的
  `tech-news-windows-project-zenith-20260904`（「微軟表示，……」）與 `tech-news-apple-september-hardware-20260909`
  （「以上效能與健康感測數字均為 Apple 官方測試或宣稱」）都是這樣處理的。正文原本就掛了，只有 summary 漏掉。

## 3. 查過而且正確的部分（摘要）

**最重要的那一條完全站得住**：四篇官方文的正文裡沒有任何一處出現 `Taiwan` 或「台灣」，
唯一的「台灣 (中文)」是 blog.google 頁尾的語言／地區版本選單（同一份清單裡還有 `ประเทศไทย (ไทย)`、`Türkiye (Türkçe)`、
`New Zealand (English)` 等），研究紀錄 `not_said` 第 2 條已經先標好，草稿也沒有拿它當任何依據。
上市名單 `October 4 in the U.S., and October 5 in Canada, the U.K., Ireland, France, Germany, and Australia`
在三篇 9 月文各出現一次、國家與日期完全相同，交叉印證無誤；草稿的否定句一律限縮在「這幾頁沒有寫」，
沒有出現「Google 沒有要在台灣賣」這一類越界說法。

其他逐條核對過且正確的（不逐一展開）：

- **日期與時間線**：三篇 9 月文的 JSON-LD 都是 `"datePublished": "2026-09-21T13:00:00+00:00"`、頁面日期戳記
  `Sep 21, 2026`；5 月發表文 `2026-05-12T17:00:00+00:00`、戳記 `May 12, 2026`。slug 後綴 `20260921`、`news_date`
  `2026-09-21`、正文第一段「2026 年 9 月 21 日」三者一致。「5 月 12 日發表、9 月 21 日開放預購、10 月 4 日上架」
  的時間線在標題、description、第一段、第一節、FAQ 第 2 題與圖解四格都一致，沒有把 9/21 寫成發表日。
  5 月文的 `dateModified` 2026-09-18 沒有被當成事件日引用。
- **預購起日與通路**：`Googlebook pre-orders begin September 21, and they'll be on shelves October 4.` 出自預購頁自己的
  `<meta name="description">`／`og:description`／JSON-LD `description`（不是頁首那塊 AI 生成摘要），
  正文的 `Pre-orders are now open on the Google Store, Best Buy, and other select retailers.` 也對得上；
  草稿正確地寫了「這幾頁沒有寫預購開放給哪些國家或地區」。
- **規格**：五款旗艦（`five flagship models` 是官方自印的數字，不是編輯清點）、$899 起、Acer／ASUS／Dell／HP／Lenovo、
  Intel Core Ultra Series 3 或 Snapdragon X Elite、NPU `over 45 TOPS`、記憶體基線 16GB／部分機型 `up to` 32GB、
  觸控螢幕 `up to 2.8K`、只有預購那篇寫 OLED、喇叭 `up to six`、Dolby Atmos、抑噪麥克風、Glowbar 與開發者自訂動畫、
  電池 `up to 14 hours of video playback and 16 hours of web browsing`（預購篇只寫 `up to 14 hours of battery life`）、
  兩篇都沒有測試條件、Intel／Qualcomm／MediaTek 三家合作但上市清單只有前兩家 —— 全部命中，
  而且 `up to`／`over` 全部譯成了「最長／最高／超過」，沒有一處被吃掉。
- **手機連動與 Gemini 功能**：端對端加密的設定搬家、Continue On（工作列接續）、Files、Cast My Apps（叫外送與
  一次性驗證碼的例子）、Magic Pointer 的三個例子與「只在被晃動叫出來時才動作、沒用時關閉、可以關掉」、
  Rambler 的 Quick Insert 鍵位置／原生多語／句中換語言／條列與 emoji、Create My Widget 不需寫程式、
  Chrome 與 Android 既有 Gemini 功能開箱即有 —— 逐句命中。
- **軟體與安全**：桌面版 Chrome 加擴充功能、Play 商店 App、原生創作工具與串流服務都標明是舉例清單、
  Antigravity、完整的 Linux 終端機環境可跑 Claude Code 或 Antigravity CLI（這句出自內建智慧那篇，
  預購那篇同一件事只寫 `a full terminal environment`、沒有 `Linux`，草稿引的是有 `Linux` 的那一篇，正確）、
  Titan 硬體信任根、縱深防禦、裝置端惡意程式偵測、`a first for the laptop category: a Level 5 security-certified
  pKVM hypervisor` 有寫成 Google 的宣稱而不是事實。
- **界線（`tech.md`）**：沒有購買建議、沒有升級建議、沒有推薦式比價、沒有換算新台幣、沒有替未列出的市場推估定價或
  上市日、沒有寫成取代 Chromebook、沒有引用 `googlebook.google` 或 `googlebook.com` 這兩個行銷網域、
  沒有出現頁首「Read AI-generated summary」獨有的 `select countries` 說法、沒有多餘的免責 callout（科技篇只有一個 callout）。
- **讀者優先（DELTA-4-7 第 14 條）**：全篇 0 個「本文」，指涉自己一律「這一篇」；description 163 字、
  以「（2026 年 9 月查證）」結尾、沒有查證流水帳；標題、description、summary 都沒有編輯清點數字
  （「五款」是官方自印的 `five flagship models`）；第一段就講清楚台灣在不在名單上。
- **結構與連結**：`display_order` 321 與 DELTA-4-7 第 5 條一致；`topics` 的 `gadgets` 在 `taxonomy.py` 第 196 行有登記、
  站上另有 4 篇科技新聞用同一組；兩個結尾連結的 text 與目標內容包的 zh-TW `title` **逐字相同**——
  `2026 年科技新聞總整理：硬體、平台、電信與法規的重點`、`微軟發布 Project Zenith：Windows 開發機的統一記憶體與頻寬門檻`；
  五節的段落數 2／3／2／3／4，都在 2–4 之間。

## 4. 留給協調者與站主的事

1. **分類頁的導引驗證不到**：正文、FAQ 第 1 題與 callout 三處請讀者「之後自行到 blog.google 的 Googlebook 分類頁確認」。
   該頁今天 200／381,521 B，但伺服器送出的 HTML 只列到 5 月那一篇（`position_maximum` 為 `1`，
   三篇 9 月文的標題與網址一個都找不到），其餘要靠頁面自己的 `load-more` 由瀏覽器補上。
   導引本身沒有錯（分類頁確實存在，三篇 9 月文頁尾的 `Posted in: Googlebook` 都指向它），
   但用純抓取證明不了「新增的市場會出現在那裡」。要不要改成請讀者直接回預購那一頁看
   `Pricing, availability, and pre-order details` 那一段，請協調者決定——我沒有改。
2. **主圖不要把「六」畫出來**：`hero.alt`（依科技垂直規格不查也不改）寫「七個色塊標示美國與另外六個上市市場」。
   研究紀錄 `unverified_or_excluded` 第 2 條與 `must_not_write` 第 21 條都明令「六」是編輯清點、官方沒印，
   圖上不得出現。alt 不是圖，但它描述的構圖會把這個數字畫進去；請繪圖／協調者確認主圖列國名或不給總數。
   圖解四格與 `hero_label` 本身沒有這個問題（`check_article.py` 的「圖上數字必須在正文」也過了）。
3. **研究紀錄第 39 條的措辭**：紀錄自己就把離線觀看寫成「Netflix、HBO Max（支援離線觀看）」，草稿是照抄紀錄的。
   內容包已改成不指定單一平台；紀錄那一條我沒有動（那是撰稿當時的證據紀錄，改掉會失去追溯性），請第二輪知悉。
4. **正文兩處查證紀律**：「本站沒有查證其他廠商是否也有同等認證」（安全段）與「本站沒有另外測試驗證」（FAQ 第 5 題）。
   `must_not_write` 第 9 條要求把 Level 5 寫成宣稱，這兩句做到了；但 DELTA-4-7 第 14 條說查證紀律不要寫進正文。
   查核不改文風，留給審稿決定。另外全篇「官方」32 次、「Google 表示」14 次（含本輪新增的 3 次），
   以 2,784 字算偏高，但每一句掛的都是真的廠商宣稱，沒有可刪的無歸因句。
5. **一個文風建議（不是事實問題）**：「Antigravity 這個**自稱的** AI 代理開發平台」——原文是
   `Antigravity, our AI agent development platform`，「自稱的」帶了一點懷疑語氣，`Google 自家的` 更中性。
   我沒有改（查核不restyle），交給審稿。

## 5. 自檢輸出（原樣）

```
OK tech-news-googlebook-launch-20260921 zh-TW paragraphs 2784
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
字數 2,759 → 2,784，仍在 1,800–3,000 內；兩個檔案都是 LF、檔尾一個換行、非 ASCII 未跳脫。

## 6. 結論

`needs_second_round`（DELTA-4-7 第 12 條本來就要求第二輪）。本輪改了 **12 處**、涵蓋 **9 個不同的事實或歸因問題**，
其中一處（12 個月 Google AI Pro 與 GeForce NOW 的隨附對象）影響到 summary、正文與 FAQ 三個位置，
是骨幹級的誤讀。沒有任何主張因為找不到來源而被整句刪除。
第二輪請特別回查：本輪新寫的 12 句（尤其 2.1、2.8 兩處改動後的句子）、第 4 節第 1 點的分類頁導引，
以及五款機型表格的每一格（那是唯一一個官方只給形容詞、最容易被補詞的區塊）。
