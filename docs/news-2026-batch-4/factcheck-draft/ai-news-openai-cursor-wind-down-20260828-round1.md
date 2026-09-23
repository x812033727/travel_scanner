# 查核報告（第一輪）：`ai-news-openai-cursor-wind-down-20260828`

- 垂直／批次：AI／4.4，`display_order` 179
- 查核者：獨立查核代理（round 1）
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-openai-cursor-wind-down-20260828.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-cursor-wind-down-20260828.json`
- 工具：`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-openai-cursor-wind-down-20260828-r1\`
  （`textutil.py`、`quotes.py`、`body.py`、`packcheck.py`、`links.py`、`edit.py`、`record.py`、`count.py`）
- 結論：**72 條主張，確認 70、更正 2、查無 0**；`sourcing_verdict` **維持 `partial`**，需要第二輪。

---

## 0. 特殊處置：公告頁重抓（協調者指定的第一件事）

指定做法是「最多 3 次、間隔 ≥60 秒、用編輯 UA 重抓公告頁；200 就重驗引文並把 `sourcing_verdict` 改成 `full`，仍是 500 就維持 `partial`」。

**結果：仍是 500，維持 `partial`。**

| 時間（台北） | 目標 | 狀態 | bytes |
| --- | --- | --- | --- |
| 09:11:45 | `openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/` | **500** | 9,262 |
| 09:12:37 | 同上 | **500** | 9,262 |
| 09:13:33 | 同上（另做 `curl -I`） | **500** | 9,262 |
| 09:14:42 | 同上 | **500** | 9,262 |
| 09:15:04 | 同一則、不帶尾斜線（RSS 印的網址） | **500** | 9,262 |
| 09:30:26 | 同上（收工前最後一次，等邊緣快取過期） | **500** | 9,262 |
| 09:12:42 | `openai.com/news/company-announcements/`（卡片） | 200 | 423,308 |
| 09:15:07 | `openai.com/index/advisory-group-on-mathematics-and-ai/`（對照組） | 200 | 373,080 |

- 間隔：09:11:45 → 09:13:33 → 09:14:42 三次符合 ≥60 秒（09:12:37 那次隔了 52 秒，額外多做的，一併列出）；09:30:26 是收工前的第五次，等了 15 分鐘讓邊緣快取的 500 過期，仍是 500。
- 回應標頭：`x-matched-path: /500`、`x-vercel-cache: MISS`、`cf-cache-status: DYNAMIC`、`Age: 3401`、`server: cloudflare`。
- **不是 UA 被擋**：同一個編輯 UA、同一分鐘讀 `openai.com/index/` 底下另一篇回 200，證實是這條路由本身在伺服器端壞掉（與研究紀錄第 (3) 點的判斷一致）。
- **卡片仍在**：清單頁今天仍印出「Our decision on Cursor following its acquisition by SpaceX」「Company Aug 28, 2026」。
- **RSS 仍在**：`openai.com/news/rss.xml`（09:15:36、200、744,049 bytes、1,219 筆），該則 `<pubDate>` 仍為 `Fri, 28 Aug 2026 06:00:00 GMT`。

因此本輪的正文引文核對，仍以研究紀錄指定的同一天 07:14 HTTP 200 副本（`_raw/ai-news-openai-cursor-wind-down-20260828/discovery-copy-0714.html`，370,301 bytes）為準。**協調者要持留本篇到頁面恢復**；頁面一恢復只要重跑 `quotes.py` 即可改 `full`。

## 1. 來源今天的狀態

| # | URL | 今日狀態 | bytes | 讀到正文？ |
| --- | --- | --- | --- | --- |
| 1 | `openai.com/index/our-decision-…-spacex/` | **500** | 9,262 | ✗（改用同日 07:14 的 200 副本，370,301 bytes） |
| 2 | `openai.com/news/company-announcements/` | 200 | 423,308 | ✓ 卡片與日期都在 |
| 3 | `cursor.com/blog/joining-spacex` | 200 | 153,547 | ✓ |
| 4 | `cursor.com/` | 200 | 626,754 | ✓（活資料，與研究當時 644,897 不同） |
| 佐證 | `cursor.com/blog` | 200 | 413,424 | ✓ 正文 `OpenAI` 0 筆 |
| 佐證 | `cursor.com/changelog` | 200 | 203,618 | ✓ 正文 `OpenAI` 0 筆 |
| 佐證 | `x.ai/news` | 200 | 271,663 | ✓ 正文 `OpenAI` 0 筆 |
| 佐證 | `openai.com/news/rss.xml` | 200 | 744,049 | ✓ 1,219 筆 |

引文比對（去 HTML 註解 → 去標籤 → `html.unescape` → 空白收斂 → 連續子字串）：**研究紀錄 23 條 `verbatim_quote` 全部通過，0 failures**；內容包內嵌的兩句英文引文也逐字相符。UA 一律 `Mokaair-editorial/1.0`，請求未帶任何姓名或 email。

---

## 2. 主張表（72 條）

判定：**C**＝confirmed、**CH**＝changed、**NF**＝not found、**S**＝style／out of scope。

### 中繼資料

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 1 | slug 尾碼 `20260828` | C | DELTA-4-4 第 3 條 |
| 2 | `news_date` `2026-08-28` | C | RSS `Fri, 28 Aug 2026 06:00:00 GMT` → 台北 08-28 14:00，同日 |
| 3 | `display_order` 179 | C | DELTA-4-4 第 3 條表 |
| 4 | `kind` life、`topics` ai／ai-news、無 finance | C | 規格 |
| 5 | title「OpenAI 將停供 Cursor 的模型：建議斷供日 11 月 12 日」 | C | 與研究紀錄 `title` 相同；用「建議斷供日」不是「終止日」 |
| 6 | description 全句（結尾「（2026 年 9 月查證）」） | C | 見第 4 節開放問題 3 的措辭註記 |
| 7 | `hero_label`「OpenAI 建議斷供日」 | C | 同上 |

### 開頭兩段

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 8 | 2026 年 8 月 28 日 OpenAI 在官方網站公告 | C | 公告頁印 `August 28, 2026`／`Company`；清單頁卡片同 |
| 9 | 已通知 SpaceX | C | `Today, we notified SpaceX…` |
| 10 | 打算終止提供 OpenAI 模型給 Cursor 的合約 | C | `…we intend to wind down our contract providing OpenAI models to Cursor` |
| 11 | 提出 2026 年 11 月 12 日為「建議斷供日」 | C | `…with a proposed shutoff date of November 12, 2026.` |
| 12 | 原文用 intend／proposed，不是已生效的終止日 | C | 同上；全篇無「確定斷供日」「正式終止日」「生效日」 |
| 13 | 第二段：2026-09-23 查核，讀四個頁面 | C（附但書） | 四個網址即 `sources[]`；公告頁那一項見開放問題 4 |
| 14 | 第二段：本站沒有實測、不提供購買或替代建議 | C | 全篇無推薦、比價、勸進語句 |

### summary 五條

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 15 | 通知 SpaceX＋11/12 建議斷供日 | C | 引文一 |
| 16 | 通知對象是 SpaceX，不是 Cursor；Cursor 8/14 宣布被收購 | C | Cursor 部落格 `Aug 14, 2026` |
| 17 | 11/12 是合約允許的最長通知期，用意是讓存取時間最大化；同一決定也不再提供未來新模型 | C | `To maximize the time…maximum notice provided by our contract.`＋`…while not providing future models to Cursor.` |
| 18 | 理由：無法確信 SpaceX 會在服務條款內使用其技術，舉 Twitter、xAI 為例 | C | 引文二＋兩段舉例 |
| 19 | 只承諾盡力支援、沒有具體措施；未點名其他供應商或任何國家 | C | 全文 refund／discount／migration／credit／Anthropic／Gemini／Google／SpaceXAI／Taiwan／region 均 0 筆 |

### §「OpenAI 通知 SpaceX：合約走向終止，但日子還沒到」

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 20 | 內嵌英文引文一 | C | 程式比對逐字相符 |
| 21 | 引文一的中文譯注 | C | 忠於原意 |
| 22 | 「這是 OpenAI 單方面提出的計畫」 | C | intend／proposed |
| 23 | 收到通知的是 SpaceX，不是 Cursor | C | 引文一 |
| 24 | Cursor 8/14 於自家部落格宣布正式被 SpaceX 收購 | C | `Aug 14, 2026`＋`Cursor has officially been acquired by SpaceX.` |
| 25 | 「完成了 4 月開始的收購程序」 | C | `This completes the acquisition process that started in April…` |
| 26 | 兩家之間原是供應模型給 Cursor 產品的客製合約 | C | `Our custom agreement with Cursor…`＋引文一 |

### §「為什麼是 11 月 12 日」

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 27 | 客製協議讓 OpenAI 在控制權變更後有「一段有限的時間窗」可取消 | C | `gives us a limited time window to cancel it after a change of control.` |
| 28 | 「收購完成兩週後、也就是 8 月 28 日」 | C | 8/14→8/28 恰為 14 天，兩個日期都是來源印出的 |
| 29 | 為了讓存取時間最大化，用的是合約提供的最長通知期 | C | `To maximize the time…maximum notice provided by our contract.` |
| 30 | 11/12 是「最晚」不是「最快」 | C | `hold the contract cancellation to the latest date we can` |
| 31 | 決定押到最晚，同時不再提供未來的新模型 | C | 同上句後半 `while not providing future models to Cursor` |
| 32 | 「11 月 12 日之後，未來推出的新模型不會再供應給 Cursor」 | **CH** | 見第 3 節第 1 處 |
| 33 | 公告沒有寫這個日期會不會再調整 | C | 全文無任何調整條件 |

### 表格與 caption

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 34 | 2026-08-14 列：Cursor 宣布被 SpaceX 收購／Cursor 官方部落格 | C | 今日 200 重抓確認 |
| 35 | 2026-08-28 列：OpenAI 通知 SpaceX／OpenAI 公告 | C | 引文一 |
| 36 | 2026-11-12 列：建議斷供日，尚未到期／OpenAI 公告 | C | 查核日 9/23 < 11/12 |
| 37 | 2026-09-23 列：Cursor 首頁仍列 OpenAI 為可選供應商／Cursor 官方首頁 | C | 今日 200、該句仍在 |
| 38 | caption「整理自…查核日 2026 年 9 月 23 日」 | C | — |

### §「OpenAI 給的理由」

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 39 | 內嵌英文引文二（理由句） | C | 逐字相符，含 `Musk's` 的**直式**撇號 |
| 40 | 引文二的中文譯注 | C | 忠於原意 |
| 41 | 公告沒有引用 SpaceX／Cursor／xAI 的任何回應 | C | 全文無第三方說法 |
| 42 | Twitter 例：Musk 收購 Twitter（現屬 SpaceX）後違反合約條款 | C | `After Musk acquired Twitter, now part of SpaceX, the company broke … the terms of our contract (alongside many others).`；歸因於「OpenAI 舉了兩個例子」 |
| 43 | xAI 例：Musk 今年在宣誓作證時承認 xAI 違反 OpenAI 服務條款 | C | `Under oath earlier this year, Musk admitted … that xAI, now also part of SpaceX, had violated OpenAI's terms of service` |
| 44 | 「那些條款與 xAI 自己的條款相似」 | C | `(terms which are similar to xAI's own)` |
| 45 | 公告沒寫案件、沒寫違反哪一條、沒提法院判決或和解 | C | 全文 lawsuit／court／settlement 均 0 筆 |
| 46 | Astra 是「即將推出的模型」，8/28 尚未發布 | C | `our upcoming model, Astra` |
| 47 | Astra 已在 9 月 3 日發布，是另一篇報導的主題 | C | 站上既有 `ai-news-gpt-6-astra-20260903`，`news_date` 2026-09-03；未與 Astral 混淆 |
| 48 | 公告全文未點名 Cursor 其他模型供應商 | C | Anthropic／Gemini／Google／SpaceXAI／Grok／Claude／Copilot 全 0 筆 |

### 圖解

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 49 | 圖解 caption | C | 與研究紀錄 `diagram.caption` 逐字相同 |
| 50 | 節點 1「母公司換人／8 月 14 日收購完成」 | C | Cursor 部落格 |
| 51 | 節點 2「取消條款生效／變更控制權後可取消」 | C | `limited time window to cancel it after a change of control` |
| 52 | 節點 3「發出終止通知／8 月 28 日給最長通知」 | C | 引文一＋最長通知句 |
| 53 | 節點 4「建議斷供日／11 月 12 日停供模型」 | C | 引文一 |

### §「對開發者的影響」

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 54 | 受影響最大的是在 Cursor 裡依賴 OpenAI 模型的開發者 | C | `We know that the people most affected by this decision are the developers who rely on OpenAI models in Cursor.` |
| 55 | 會在意轉換期體驗，準備盡力協助 | C | `We care about their experience in this transition and we're ready to go above and beyond to support them.` |
| 56 | 沒有窗口、折扣、遷移工具、時程 | C | 全文 refund／discount／migration／credit 均 0 筆 |
| 57 | Anthropic、Google、SpaceXAI 完全沒出現 | C | 同 #48 |

### §「現在是什麼狀態」

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 58 | 9/23 Cursor 首頁仍列 OpenAI、Anthropic、Gemini 與 SpaceXAI | C | 今日 200，`Choose between every cutting-edge model from OpenAI, Anthropic, Gemini, SpaceXAI, and Cursor.` 仍在；文中已註明是當天狀態 |
| 59 | Cursor 部落格、changelog、SpaceXAI 新聞頁截至查核日都沒查到說明 | C（來源歸屬見開放問題 2） | 三頁今日皆 200，正文 `OpenAI` 均 0 筆；RSS 1,219 筆裡 08-28 之後無任何續篇 |
| 60 | 公告沒提任何國家或地區，也沒寫時區 | C | Taiwan／Europe／region／UTC／timezone 均 0 筆 |

### FAQ 五題

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 61 | Q1「11/12 之後就不能用了嗎」→ 還不確定，是建議斷供日 | C | intend／proposed |
| 62 | Q2「是通知 Cursor 嗎」→ 不是，是通知 SpaceX；控制權變更後可取消 | **CH** | 見第 3 節第 2 處（限定詞） |
| 63 | Q3「會得到什麼補償」→ 只承諾盡力支援，沒有具體做法 | C | 同 #55、#56 |
| 64 | Q4「跟台灣有關係嗎」→ 沒有台灣特別待遇 | C | 同 #60 |
| 65 | Q5「之後還有哪些公司的模型」→ 公告未點名；當天首頁列出四家 | C | 同 #48、#58 |

### callout、結尾連結、sources

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 66 | callout：進行中的通知、11/12 未到、沒有實測與替代建議 | C | AI 篇只有一個 callout，無投資免責段落 |
| 67 | 連結一文字＝`ai-news-2026-january-september-index` 的 zh-TW title | C | 程式逐字比對通過 |
| 68 | 連結二文字＝`ai-news-gpt-53-codex-20260205` 的 zh-TW title | C | 程式逐字比對通過（含全形問號） |
| 69 | `sources[0]` OpenAI 公告 | C（標題正確） | 今日 500；引文對同日 200 副本通過 |
| 70 | `sources[1]` OpenAI 公司公告清單 | C | 今日 200 |
| 71 | `sources[2]` Cursor `joining-spacex` | C | 今日 200 |
| 72 | `sources[3]` Cursor 首頁 | C | 今日 200 |

---

## 3. 改了 2 處

### 第 1 處（骨幹論述）：「不再提供未來新模型」被寫成 11/12 之後才發生

- **原文**：「也就是說，11 月 12 日之前，現有模型仍可透過 Cursor 使用；11 月 12 日之後，未來推出的新模型不會再供應給 Cursor，但公告沒有寫這個日期會不會再調整。」
- **改成**：「這兩件事是同時的，不是先後：在建議斷供日之前，開發者仍可透過 Cursor 使用 OpenAI 的模型，但在這段期間，之後推出的新模型不會再提供給 Cursor；至於 11 月 12 日會不會再調整，公告沒有寫。」
- **來源原文**：`Given all of this, we've decided to hold the contract cancellation to the latest date we can while not providing future models to Cursor.`
- **為什麼**：`while` 是「同時」，不供新模型是「把取消押到最晚」的交換條件，從公告當下起算，不是 11/12 之後才開始；而且 11/12 之後公告提的是整份合約斷供，不只「未來的新模型」。原句也和它前面那一句（「同時不再提供未來的新模型」）自相矛盾。
- **來源**：`https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/`

### 第 2 處（限定詞被刪）：FAQ 的取消權

- **原文**：「OpenAI 與 Cursor 之間的客製合約，因此在控制權變更後讓 OpenAI 有權選擇是否取消。」
- **改成**：「而 OpenAI 與 Cursor 之間的客製合約，在控制權變更之後給 OpenAI 一段有限的時間可以取消。」
- **來源原文**：`Our custom agreement with Cursor gives us a limited time window to cancel it after a change of control.`
- **為什麼**：`limited time window` 這個限定詞在 FAQ 被安靜拿掉，變成無期限的選擇權；正文同一件事寫對了（「有一段有限的時間窗」），FAQ 要一致。
- **來源**：同上

---

## 4. 留給協調者的問題

1. **公告頁仍 500，`sourcing_verdict` 維持 `partial`。** 依研究紀錄 `must_not_write` 最後一條與 `live_data_warnings` 第 2 條，本篇要持留到頁面恢復。頁面一恢復，重跑 `_tools/…-r1/quotes.py`（23 條應全過）即可改 `full`；不需要重寫任何句子。
2. **「未查到回應」那一句的來源不在 `sources[]`。** 正文寫「本站也查看了 Cursor 的部落格、changelog，以及 SpaceXAI 的官方新聞頁」，這三個網址（`cursor.com/blog`、`cursor.com/changelog`、`x.ai/news`）不在內容包 `sources[]` 裡。我今天三個都抓到了（全 200，413,424／203,618／271,663 bytes，正文 `OpenAI` 均 0 筆），句子本身也是研究紀錄 `unverified_or_excluded` 核可的寫法，但依查核規格「每條主張要在 `sources[]` 找得到支撐」這是一個缺口。請裁定：把三個網址補進 `sources[]`，或把這句收成只提 `sources[]` 已有的頁面。**本輪未自行更動 `sources[]`。**
3. **「11 月 12 日是合約允許的最長通知期」這個簡寫。** description、summary 第三條與 callout 都這樣寫。原文實際是 `we are giving the maximum notice provided by our contract` 加上 `proposed shutoff date of November 12, 2026`——嚴格說 11/12 是「用滿最長通知期得出的日期」，不等於通知期本身。因為派工說明也用同一種簡寫，本輪未改；若要精確，可改成「這是用滿合約允許的最長通知期得出的日期」。
4. **正文第二段寫「讀的是 OpenAI 這則公告的全文」。** 在公告頁 500 的前提下，這句成立的依據是同一天 07:14 的 200 副本。若最後決定在頁面未恢復的狀態下上線，這句要一併重審。

## 5. 界線與可讀性檢查

- **購買建議／推薦式比價**：無。全篇沒有「值得換」「建議改用」這類語句，也沒有把 Codex、Claude Code、Copilot 寫成替代方案。
- **廠商宣稱未歸因**：無。OpenAI 的每一項說法都帶「OpenAI 表示／公告寫的是／OpenAI 舉了兩個例子」，Twitter 與 xAI 兩段是歸因轉述，沒有寫成已被認定的事實，也沒有「判決」「裁定」「封殺」「報復」「決裂」這類定性詞。
- **預告／草案狀態**：正確。11/12 全篇都是「建議斷供日」，並寫明截至查核日尚未到期。
- **相對時間詞**：全篇無「最近」「本週」「日前」「這幾天」。
- **「本文」**：0 筆。
- **description**：以「（2026 年 9 月查證）」結尾；title／description／summary 無篩選篇數。
- **歸因密度**：每個正文段落至多 2 個歸因語。開頭段有「OpenAI 在官方網站公告」1 個歸因語，另加「原文用的是 intend 與 proposed」這個**逐字用語引述**——後者是本篇的核心分界（研究紀錄 `must_not_write` 第 2 條要求保留），因此判定不算超標，提請覆核者確認。
- **可讀性（未改，建議覆核者處理）**：
  - 「讀不到不等於沒有發生，只能寫成目前查不到，不能寫成『沒有回應』或『拒絕說明』」把編輯台的查證紀律寫進了正文，是站上退過稿的同一種毛病；建議收成「截至查核日，這三個官方頁面都沒有相關說明」。
  - 開頭段的「截至查核日」出現在讀者還不知道查核日是哪一天之前（下一段才交代）。
- **結構**：段落字數 2,554（1,800–3,000 內），五節各 2–3 段，summary 與圖上的每個數字都出現在正文。

## 6. 自檢輸出

```
check_article.py exit=0
OK ai-news-openai-cursor-wind-down-20260828 zh-TW paragraphs 2554
```

```
pack_cli lint exit=1
ai-news-openai-cursor-wind-down-20260828
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-openai-cursor-wind-down-20260828/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-cursor-wind-down-20260828/diagram-1.svg
1 entries checked
```

兩項都在允許範圍內（`image_missing` 與 `raw_internal_url` 在繪圖與 relink 之前是預期的）。

## 7. 結論

**需要第二輪。** 事實更正 2 處，其中第 1 處動到骨幹論述（「不再提供未來新模型」的時間點），第二輪要逐句回來源重查這兩處與新寫進去的每一句，另抽查三分之一的已確認項。

另外：`sourcing_verdict` 仍是 `partial`，公告頁今天五次重抓（含收工前隔 15 分鐘的最後一次）全部 500 —— 依派工說明，本篇由協調者持留。
