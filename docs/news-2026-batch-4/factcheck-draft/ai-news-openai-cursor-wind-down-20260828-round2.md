# 查核報告（第二輪）：`ai-news-openai-cursor-wind-down-20260828`

- 垂直／批次：AI／4.4，`display_order` 179
- 查核者：獨立查核代理（round 2，未參與撰稿，也未參與第一輪）
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-openai-cursor-wind-down-20260828.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-cursor-wind-down-20260828.json`
- 工具：`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-openai-cursor-wind-down-20260828-r2\`
  （`textutil.py`、`quotes2.py`、`body2.py`、`negatives.py`、`sample.py`、`links2.py`、
  `rssitem2.py`、`edit_pack2.py`、`record2.py`、`packscan2.py`）
- 結論：**查了 25 條主張，維持 confirmed 25、新發現的事實錯誤 0**；
  另依協調者裁定刪掉一整段。**公告頁已復原，`sourcing_verdict` 由 `partial` 改為 `full`。**
  判定 **`ok`**。

---

## 0. 公告頁重抓：**已復原，第一次嘗試就是 200**

派工指定「最多再試 3 次、間隔 ≥60 秒、用編輯 UA；200 就重跑 `quotes.py` 並把
`sourcing_verdict` 改成 `full`」。**第 1 次嘗試就回 200，因此只用掉 1 次配額**；
為了確認不是瞬間抖動，間隔 3 分 44 秒後又抓了一次，仍是 200。

| 時間（台北） | 目標 | 狀態 | bytes | `x-matched-path` |
| --- | --- | --- | --- | --- |
| 09:32:33 | `openai.com/index/our-decision-…-spacex/` | **200** | 372,450 | `/[locale]/[country]/[flags]/[...slug]` |
| 09:36:17 | 同上（確認用） | **200** | 372,420 | 同上 |

- 第一輪（09:11–09:30，五次）全部是 9,262 bytes 的 Next.js 錯誤頁、`x-matched-path: /500`；
  本輪的 `x-matched-path` 已變回真正的路由，`Age: 0`，證明是伺服器端修好了，不是快取。
- 兩次相差 30 bytes，是 build nonce 一類的動態字串，不是內容變動。
- **拿到的是真正的正文，不是回 200 的錯誤頁**：`<title>` 為
  `Our decision on Cursor following its acquisition by SpaceX | OpenAI`；
  `August 28, 2026`、`notified SpaceX`、`November 12, 2026`、
  `while not providing future models` 等標記都在，`Something went wrong` 0 筆。
  抽出的正文長度 1,879 字元，與第一輪所用的 07:14 副本一致。
- UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，
  同一主機間隔 ≥2 秒，請求未帶任何姓名或 email。

**引文重驗**：`quotes2.py`（同 `quotes.py` 的比對規則：去 HTML 註解 → 去標籤 →
`html.unescape` → 空白收斂 → 連續子字串），但這次**四個來源全部是本人今天自己抓到的正文**，
公告頁不再依賴探索代理的副本：

```
checked=23 failures=0
```

23 條 `verbatim_quote` 全過（其中 15 條打在公告頁上）。研究紀錄 `sourcing_notes` 第 (7) 點
與 `live_data_warnings` 第 2 條的條件因此滿足：

- `sourcing_verdict` `partial` → **`full`**（文字取代）
- `sources[0]` 的 `fetched_at` `2026-09-23T07:14+08:00` → `2026-09-23T09:36+08:00`，
  `bytes` `370301` → `372420`（同一段落所述，`sourcing_notes` 明文要求）

**協調者不必再持留本篇。** 第一輪 open question 1 與 4（「讀的是公告全文」這句在 500
的前提下靠副本成立）一併解消：本輪確實讀到了公告頁全文。

---

## 1. 今天各來源的狀態（全部本人自抓）

| # | URL | 狀態 | bytes | 讀到正文？ |
| --- | --- | --- | --- | --- |
| 1 | `openai.com/index/our-decision-…-spacex/` | **200** | 372,420 | ✓ 正文 1,879 字元 |
| 2 | `openai.com/news/company-announcements/` | 200 | 423,311 | ✓ 卡片＋`Aug 28, 2026` |
| 3 | `cursor.com/blog/joining-spacex` | 200 | 153,547 | ✓ |
| 4 | `cursor.com/` | 200 | 626,754 | ✓（活資料，與紀錄的 644,897 不同） |
| 佐證 | `openai.com/news/rss.xml` | 200 | 744,049 | ✓ 1,219 筆 |

RSS 該則逐字：`<title>` `Our decision on Cursor following its acquisition by SpaceX`、
`<pubDate>` `Fri, 28 Aug 2026 06:00:00 GMT`（台北 08-28 14:00，同日）、`<category>` `Company`。
1,219 筆裡提到 Cursor／SpaceX／Musk／xAI 的只有 5 筆，**2026-08-28 之後沒有任何續篇**
（其餘 4 筆是 2024–2025 年的舊文）。

---

## 2. 協調者裁定（先執行，已寫進 `factcheck.second_round.coordinator_rulings`）

### 裁定（1）＋（2）：整段刪除

兩項裁定指向的是**同一段**的前後兩半句，合起來就是整段，故整段移除。

- **刪掉的整段**：
  「本站也查看了 Cursor 的部落格、changelog，以及 SpaceXAI 的官方新聞頁，截至查核日都沒有查到任何與這項決定有關的說明；讀不到不等於沒有發生，只能寫成目前查不到，不能寫成「沒有回應」或「拒絕說明」。」
- 裁定（1）的理由：那三個網址（`cursor.com/blog`、`cursor.com/changelog`、`x.ai/news`）
  不在內容包 `sources[]` 裡，而且這是查證過程的敘事。
- 裁定（2）的理由：後半句把編輯台的查證紀律寫進正文，是站上退過稿的同一種毛病。
- **執行結果**：`blocks` 28 → 27，正文段落 15 段，段落字數 2,554 → **2,444**（仍在 1,800–3,000）。
- **連帶效果**：正文只寫 OpenAI 公告了什麼；`changelog` 與 `x.ai` 在內容包中現為 0 筆，
  **不再有任何句子依賴 `sources[]` 以外的頁面**——第一輪 open question 2 的缺口隨之解消，
  `sources[]` 維持四條、未增刪。
- **銜接**：該節剩兩段，「首頁供應商現況（9/23）」→「公告沒提任何國家或地區」，讀起來完整；
  五節的段數為 2／3／3／3／2，仍在 2–3 段的範圍。

### 裁定（3）：保留第一輪關於 `while` 的更正

已對本人自抓的公告正文重核，**維持不動**，詳見第 3 節。

---

## 3. 覆核第一輪改過的兩處（逐子句回來源）

### 第 1 處（骨幹論述）：`while not providing future models`

來源逐字（本人自抓的正文）：

> `Given all of this, we've decided to hold the contract cancellation to the latest date we can while not providing future models to Cursor.`

現行正文：「…這兩件事是同時的，不是先後：在建議斷供日之前，開發者仍可透過 Cursor 使用
OpenAI 的模型，但在這段期間，之後推出的新模型不會再提供給 Cursor；至於 11 月 12 日會不會再調整，公告沒有寫。」

| 子句（第一輪新寫的每一句） | 判定 | 來源依據 |
| --- | --- | --- |
| 「這兩件事是同時的，不是先後」 | **C** | `while` 無論讀成「同時」或「儘管」都是並行；沒有任何讀法能得出「11/12 之後才開始」。第一輪的更正正確。 |
| 「在建議斷供日之前，開發者仍可透過 Cursor 使用 OpenAI 的模型」 | **C** | `To maximize the time that developers can retain access to our models through Cursor, we are giving the maximum notice provided by our contract.` |
| 「但在這段期間，之後推出的新模型不會再提供給 Cursor」 | **C** | `while not providing future models to Cursor` |
| 「至於 11 月 12 日會不會再調整，公告沒有寫」 | **C** | 調整／延期用語（`subject to change`、`may change`、`adjust`、`extend`、`revise`、`reconsider`、`final date`、`unless`、`if SpaceX`）在正文全部 0 筆。否定句的範圍是「這則公告」，界定明確。 |

被換掉的原句確實有兩個毛病：時間點錯（把並行寫成先後），而且 11/12 之後斷的是整份合約、
不只「未來的新模型」。**維持第一輪的改法。**

### 第 2 處（限定詞）：FAQ 的取消權

> `Our custom agreement with Cursor gives us a limited time window to cancel it after a change of control.`

現行 FAQ：「…而 OpenAI 與 Cursor 之間的客製合約，在控制權變更之後給 OpenAI 一段有限的時間可以取消。」
→ **C**。`limited time window` 這個限定詞回來了，且與正文同一件事的寫法（「有一段有限的時間窗可以取消合約」）一致，
符合「FAQ 答案 ⊆ 正文」。

---

## 4. 抽查：第一輪 70 條 confirmed 的三分之一（23 條）

抽樣可重現：種子為 slug，程式 `sample.py`，抽中
**#2、#9、#10、#11、#12、#13、#16、#17、#25、#27、#28、#30、#33、#42、#45、#46、#48、#52、#55、#63、#64、#65、#67**。

| # | 主張 | 判定 | 本輪依據 |
| --- | --- | --- | --- |
| 2 | `news_date` `2026-08-28` | C | RSS `<pubDate>` `Fri, 28 Aug 2026 06:00:00 GMT` → 台北 08-28 14:00，同日；公告頁印 `August 28, 2026` |
| 9 | 已通知 SpaceX | C | `Today, we notified SpaceX…` |
| 10 | 打算終止提供 OpenAI 模型給 Cursor 的合約 | C | `…we intend to wind down our contract providing OpenAI models to Cursor` |
| 11 | 提出 11 月 12 日為建議斷供日 | C | `…with a proposed shutoff date of November 12, 2026.` |
| 12 | 原文用 intend／proposed | C | 兩詞各 1 筆；`確定斷供日`／`正式終止日`／`生效日` 在內容包 0 筆 |
| 13 | 第二段：9/23 查核，讀四個頁面 | **C（但書解除）** | 四頁今天全由本人抓到 200 並讀到正文，公告頁亦然；第一輪的但書不再需要 |
| 16 | 通知對象是 SpaceX；Cursor 8/14 宣布被收購 | C | Cursor 部落格 `Aug 14, 2026` |
| 17 | 最長通知期／存取時間最大化／不再供未來新模型 | C | `To maximize the time…maximum notice provided by our contract.`＋`while not providing future models to Cursor`（措辭見第 6 節開放問題 1） |
| 25 | 「完成了 4 月開始的收購程序」 | C | `This completes the acquisition process that started in April, when we announced our partnership with SpaceXAI…` |
| 27 | 控制權變更後有一段有限的時間窗可取消 | C | `gives us a limited time window to cancel it after a change of control.` |
| 28 | 「收購完成兩週後、也就是 8 月 28 日」 | C | 8/14 → 8/28 恰 14 天，兩日期都由來源印出 |
| 30 | 11/12 是「最晚」不是「最快」 | C | `hold the contract cancellation to the latest date we can` |
| 33 | 公告沒寫日期會不會再調整 | C | 調整／延期用語 9 詞全 0 筆 |
| 42 | Twitter 例 | C | `After Musk acquired Twitter, now part of SpaceX, the company broke … the terms of our contract (alongside many others).`，正文歸因為「OpenAI 舉了兩個例子」 |
| 45 | 沒寫案件／哪一條／判決或和解 | C | `lawsuit`、`court`、`settlement`、`judge`、`ruling`、`injunction`、`complaint`、`damages` 全 0 筆 |
| 46 | Astra 是「即將推出的模型」，8/28 尚未發布 | C | `our upcoming model, Astra`（1 筆）；正文未與 Astral 混淆 |
| 48 | 公告未點名其他模型供應商 | C | `Anthropic`、`Gemini`、`Google`、`SpaceXAI`、`Grok`、`Claude`、`Copilot`、`Llama`、`Mistral` 全 0 筆 |
| 52 | 圖解節點 3「8 月 28 日給最長通知」 | C | 引文一＋最長通知句 |
| 55 | 在意轉換期體驗、準備盡力協助 | C | `We care about their experience in this transition and we're ready to go above and beyond to support them.` |
| 63 | FAQ Q3：只承諾盡力支援，無具體做法 | C | `refund`、`discount`、`migration`、`credit`、`rebate`、`transition plan`、`timeline` 全 0 筆 |
| 64 | FAQ Q4：沒有台灣特別待遇 | C | `Taiwan`、`Europe`、`region`、`country`、`UTC`、`timezone` 全 0 筆 |
| 65 | FAQ Q5：公告未點名；當天首頁列四家 | C | 同 #48；`cursor.com` 今天仍印 `Choose between every cutting-edge model from OpenAI, Anthropic, Gemini, SpaceXAI, and Cursor.` |
| 67 | 連結一文字＝索引篇 zh-TW title | C | `links2.py` 逐字比對 PASS（連結二也一併驗過，PASS，含全形問號） |

**23 條全部維持 confirmed，本輪未發現任何新的事實錯誤。**

---

## 5. 回掃：有沒有為了字數刪掉但書、限定詞或歸因

- **沒有。** `intend`／`proposed`／「建議斷供日」（10 筆）／「截至查核日尚未到期」／
  「OpenAI 表示」這類但書與歸因都還在；第一輪的兩處改動都是**補回**限定詞，不是刪。
- 本輪唯一的刪除是協調者裁定的整段，刪掉的是查證敘事與編輯台紀律，**不是任何但書**。
- 段落字數 2,444 < 3,000。

### 界線與可讀性（`packscan2.py`）

- 禁用詞：`本文`、`最近`、`本週`、`日前`、`這幾天`、`確定斷供日`、`正式終止日`、`生效日`、
  `封殺`、`報復`、`決裂`、`開戰`、`建議改用`、`值得換`、`沒有回應`、`拒絕說明`
  **全部 0 筆**；`changelog`、`x.ai` 也已降為 0。
- `description` 以「（2026 年 9 月查證）」結尾；title／description／summary 無篩選篇數。
- **歸因密度**：開頭段 1 個（`OpenAI 在官方網站公告`），其餘每段至多 2 個——符合規則。
  第一輪自陳「開頭段另有『原文用的是 intend 與 proposed』」一項，本輪判定那是**逐字用語引述**
  而非歸因語（研究紀錄 `must_not_write` 第 2 條要求保留），不計入密度，維持不改。
- `topics` 只有 `ai`／`ai-news`，不帶 `finance`；只有一個 `info` callout、無投資免責段；
  沒有訂閱、購買、升級、換工具或投資建議；沒有推定台灣可用；廠商宣稱全部歸因給 OpenAI。
- `summary` 五條的關鍵詞全部出現在正文；FAQ 五題的答案都能在正文找到；
  圖解四個節點的日期與說法都在正文。
- 日期一致：slug 尾碼 `20260828` ＝ `news_date` ＝ 第一段「2026 年 8 月 28 日」＝ DELTA-4-4 第 3 條。
- `sources[]` 四條的 `checked_on` 均為 `2026-09-23`。

---

## 6. 留給協調者的事

1. **（沿用第一輪 open question 3，本輪仍未改）「11 月 12 日是合約允許的最長通知期」這個簡寫。**
   原文是 `we are giving the maximum notice provided by our contract` 加上
   `proposed shutoff date of November 12, 2026`——嚴格說 11/12 是「用滿最長通知期得出的**日期**」，
   不等於通知期本身。這個寫法出現在 `description`、`summary` 第 3 條與 callout **三處**，改一處就要改三處。
   它不是事實錯誤（讀者取走的意思「這是合約允許的最晚」是對的），且派工說明本身用同一種簡寫，
   因此本輪不動；若要精確，三處一起改成「用滿合約允許的最長通知期得出的日期」。
2. **（純可讀性，未改）** 開頭第一段的「截至查核日」出現在讀者還不知道查核日是哪一天之前，
   下一段才交代 2026 年 9 月 23 日。屬順序問題，不是事實問題。
3. 第一輪的 open questions **1、2、4 已解消**（1 與 4 因公告頁復原，2 因裁定（1））。

---

## 7. 自檢輸出

`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-openai-cursor-wind-down-20260828-r2\exit-codes.txt`：

```
check_article.py exit=0
pack_cli lint exit=1
```

```
OK ai-news-openai-cursor-wind-down-20260828 zh-TW paragraphs 2444
```

```
ai-news-openai-cursor-wind-down-20260828
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-openai-cursor-wind-down-20260828/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-cursor-wind-down-20260828/diagram-1.svg
1 entries checked
```

兩項都在允許範圍內（`image_missing` 與 `raw_internal_url` 在繪圖與 relink 之前是預期的）。

---

## 8. 結論

- 查了 **25 條**（第一輪 2 處改動逐子句 ＋ 隨機抽出的 23 條 confirmed），**維持 confirmed 25，新發現的事實錯誤 0**。
- 改了 **1 處**：協調者裁定（1）＋（2）的整段刪除。裁定（3）確認保留。
- **`sourcing_verdict` 已由 `partial` 改為 `full`**：公告頁今天 09:32 第一次嘗試即回 HTTP 200，
  09:36 再確認一次仍 200，23 條引文對本人自抓的正文全過（0 failures）。
  **本篇不需要再持留，可以進這一波。**
- 只動了三個檔（內容包、研究紀錄、本報告），未執行任何 git 指令，repo 內未留暫存檔。
- 判定：**`ok`**。
