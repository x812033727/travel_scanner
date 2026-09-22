# `ai-news-openai-math-advisory-20260921` 查核報告（第二輪）

- 查核者：independent factcheck agent, round 2（沒有參與撰稿，也沒有參與第一輪）
- 查核日：2026-09-23
- 垂直／順序：AI，`display_order` 171，事件日 2026-09-21
- 內容包：`apps/api/app/guides/content/ai-news-openai-math-advisory-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-math-advisory-20260921.json`
- 第一輪報告：`factcheck/ai-news-openai-math-advisory-20260921-round1.md`（13 處事實／表述＋8 處漏空格）
- 結論：**ok**。本輪改了 **3 處**，三處都是協調者裁定要改的；沒有新發現的事實錯誤。

## 1. 自己重抓來源（2026-09-23 01:25–01:26 台北）

四條都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒。
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料；
`agmai.org` 的 `/input` 意見表單與 `mathandai.org` 的 Endorsers 分頁**沒有開啟、沒有填寫、沒有送出**。
抽字腳本是本輪自己寫的（去 HTML 註解、去 `script`／`style`、`html.unescape`、正規化 U+2011／NBSP／彎引號），不是沿用第一輪的。

| # | URL | HTTP | bytes | 抽出正文 | 與第一輪比 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://openai.com/index/advisory-group-on-mathematics-and-ai/` | 200 | 370,858 | 4,942 字元 | 字數完全相同 |
| 2 | `https://agmai.org/` | 200 | 67,954 | 2,508 字元 | 字數完全相同 |
| 3 | `https://mathandai.org/` | 200 | 10,873 | 6,290 字元 | 字數完全相同 |
| 4 | `https://openai.com/index/navier-stokes-solution/` | 200 | 457,115 | 11,975 字元 | 字數完全相同 |

- `openai.com/index/*` 本輪兩次請求都沒有 403。
- bytes 與第一輪差幾十到十幾位元組（Next.js chunk 清單、WordPress.com nonce），**抽出的正文字元數四頁都與第一輪完全一致**，
  來源在兩輪之間沒有改動，所有「截至查核當天」的狀態句今天仍然成立。

## 2. 範圍與方法

依 `agents/ai/SECOND-ROUND.md`，本輪不是整篇重做：

- **(a) 第一輪改動的 13 處**逐條回一手來源重驗。
- **(b) 第一輪新寫進去的字**逐句回原文：summary 2 的「OpenAI 表示」、P2／FAQ A5／callout 的「OpenAI 的兩份公告」、
  P14／FAQ A5 的「四份／四個官方頁面」、callout 的「這一篇寫的是」。
- **(c) 隨機三分之一的 CONFIRMED**：`random.seed(47)` 從第一輪 87 條 CONFIRMED 抽 29 條
  （第 2、3、4、5、8、11、17、20、36、37、38、40、42、45、50、53、55、59、60、63、64、65、68、71、76、80、81、84、100 條）。
- **(d) 指派訊息點名的五條協調者裁定。**
- **(e) 回掃第一輪有沒有為了字數刪掉但書、限定詞或歸因**：把第一輪自己留下的 `dump.txt` 與 `dump-after.txt` 逐行 diff，
  確認它只動了報告列出的那 13 處，**一個但書、限定詞或歸因都沒有刪**（反而在 summary 2 加了「OpenAI 表示」）。

另外跑了五組機械檢查（腳本在 `_tools/ai-news-openai-math-advisory-20260921-r2/`）：

| 檢查 | 結果 |
| --- | --- |
| 32 條英文引句對本輪正文做連續子字串比對 | 32/32 命中，且都命中在**正確的那一頁** |
| `Princeton`／`普林斯頓`（四頁正文＋原始 HTML） | 全部 0 筆 |
| `Taiwan`／`Asia`／`Japan`／`Korea`／`China`／`countries`（四頁正文） | 全部 0 筆；`navier` 唯一的 `region` 是 `This central region shrinks` 的流體描述 |
| 九位成員名單兩頁逐行比對 | 九對九一致，唯一差異是 OpenAI 頁的錯字 `Simons Institue`（未被抄入文章） |
| 九位成員 vs 宣言頁列出的名字 | 只有 Hairer 重疊，其餘八位皆無 |
| `agmai.org` 是否已刊出建議 | 全站仍只有 Purpose／Independence, Transparency, and Accountability／Advisory Group Members／Current Task 四節；站內連結只有 `/input`、`ias.edu` 與 WordPress 平台連結，**沒有任何建議頁** |
| 內容包禁用字元 | U+2011／NBSP／零寬字元／BOM／`Institue` 皆 0；`GPT-6` 用一般連字號 U+002D |
| CJK 與拉丁字母之間漏空格 | **0 處**（第一輪的 8 處已全部修掉） |
| 兩個結尾連結 text vs 目標內容包 zh-TW title | 兩條皆字元級完全相同 |
| 圖解 caption vs 研究紀錄 `diagram.caption` | 逐字相同 |
| 圖解 nodes 的數字（100）是否出現在正文 | 是 |

## 3. 主張表（45 條）

判定：C＝CONFIRMED、CH＝CHANGED、S＝排版。

### 3.1 第一輪改動的 13 處（逐條回一手來源）

| # | 位置 | 第一輪改後的寫法 | 判定 | 本輪依據 |
| --- | --- | --- | --- | --- |
| R1-1 | title | 「與 OpenAI 合作的數學顧問小組…」 | C | `agmai`：`This group operates independently of any AI company`；`advisory`：`we're working with mathematicians who have established an independent mathematics advisory group`。協調者裁定第 1 條維持；紀錄 `title` 與內容包 title 逐字相同 |
| R1-2 | description | 「公告**正**與一群數學家合作」 | C | 原文 `we're working with`（現在進行式）；`agmai` 的 `We are currently facing…advising OpenAI` 佐證 |
| R1-3 | P1 | 同上 | C | 同上 |
| R1-4 | summary 1 | 「正與…」＋「高等研究院（Institute for Advanced Study）」 | C | 同上；`hosted at the Institute for Advanced Study` |
| R1-5 | P1 | 刪「普林斯頓」 | C | 四頁正文與原始 HTML 搜尋 `Princeton` 皆 0 筆。協調者裁定第 2 條維持 |
| R1-6 | P5 | 刪「普林斯頓」 | C | 同上 |
| R1-7 | summary 2 | 「**OpenAI 表示**它除了解出…」 | C | 紀錄 `is_vendor_claim: true`；`this model has now resolved more than 100 long-standing open problems across most areas of mathematics` |
| R1-8 | P2 | 「OpenAI 的**兩份**公告」 | C | 正文確實用到第四條來源（`significantly more capable than GPT-6 Astra` 只在 navier 頁）。**用字見第 5 節第 2 點** |
| R1-9 | P4 | 刪「更」審慎 | C | 原文 `Their criticisms highlight the need for thoughtful engagement of AI companies with the math community.`，沒有比較級 |
| R1-10 | P14 | 「**四份**官方頁面…都沒有提到台灣、亞洲或任何特定地區」 | C | 四頁地區關鍵字機械掃描全 0 筆，否定句對四份都成立 |
| R1-11 | FAQ A5 | 「兩份公告…這**四個**官方頁面」 | C | 同上；2＋1＋1＝4 |
| R1-12 | callout | 「內容整理自 OpenAI 的兩份公告…」 | C | 同 R1-8 |
| R1-13 | callout | 「**這一篇寫的是** 2026 年 9 月 23 日查核當天的狀態」 | C | DELTA-4-7 §14；全篇「本文」仍為 0 |
| R1-T | 全篇 | 8 處中英文之間補空格 | S | 機械掃描今天 0 處殘留 |

### 3.2 隨機抽驗的 29 條 CONFIRMED（`seed=47`）

| 原編號 | 位置 | 主張 | 判定 | 本輪依據 |
| --- | --- | --- | --- | --- |
| 2 | title | 小組是獨立的 | C | `The group will operate independently from OpenAI.` |
| 3 | title | 能公開意見 | C | `make its advice public` |
| 4 | title | 不管內部進度 | C | `Importantly, the group will not be responsible for advising us on how to pace our internal progress on mathematics.` |
| 5 | desc | 2026-09-21 OpenAI 公告 | C | 頁首逐字 `September 21, 2026` ＋分類 `Company` |
| 8 | desc | 未發布內部模型解出超過 100 題 | **CH** | 事實成立，但依裁定第 5 條補歸因（見 4.2） |
| 11 | desc | 也沒有決策權 | C | `we do not have decision making power at any AI company` |
| 17 | P1 | 小組全名 Advisory Group on Mathematics and Artificial Intelligence | C | 兩頁逐字 |
| 20 | P1 | 模型自 8 月 28 日開始訓練、尚未發布 | C | `On August 28, we began training a new internal model.`；「尚未發布」見第 5 節第 3 點 |
| 36 | P3 | 進展速度讓 OpenAI 內部數學家意外 | C | `has surprised the mathematicians within OpenAI` |
| 37 | P3 | 引發內部討論如何讓數學界提早準備 | C | `This has led to internal discussions on the best way to inform the community of the rapid progress to prepare and adapt the field.` |
| 38 | P4 | 公開信標題與 9 月 11 日 | C | `Published 11 September 2026 · DOI 10.5281/zenodo.22737750` |
| 40 | P4 | 倉促公布／來不及寫論文／釐清新方法／引用他人研究 | C | `Often these solutions are announced in a rush, leaving no time for a proper writeup, the isolation of new methods and ideas, and citing relevant previous work of others.` |
| 42 | P5 | 公告原文「與已經成立獨立數學顧問小組的數學家們合作」 | C | 逐字 |
| 45 | P5 | 成員不由 OpenAI 支薪 | C | `Its members will not be paid by OpenAI` |
| 50 | P7 | 截至 9/23 沒有刊出任何一份建議 | C | 今天重掃 `agmai.org` 全站四節、站內連結只有 `/input` 與 `ias.edu` |
| 53 | 表格列 3 | 不負責建議調整內部進度節奏｜OpenAI 公告 | C | 同 R1 引句 |
| 55 | 表格 caption | 查核日 2026-09-23、51 字（≤200） | C | 程式量測 51 字 |
| 59 | P9 | Current Task「所報告」 | C | `…that they report have been produced by their internal model` |
| 60 | P9 | 小組沒有自己驗證或背書 | C | 兩頁都沒有驗證／背書敘述，`agmai` 用的是 `they report` |
| 63 | 圖解 caption | 與研究紀錄 `diagram.caption` 逐字相同 | C | 程式比對 `True` |
| 64 | P11 | 成立經過引句 | C | `This group came together after OpenAI approached some of its members about establishing an external advisory board. In agreement with OpenAI, they decided to instead create an independent group and invite the others to join.` |
| 65 | P11 | 改走獨立路線是成員自己的決定 | C | 同上句 `they decided to instead create an independent group` |
| 68 | P12 | Hairer 那一句 | **CH** | 依裁定第 3、4 條改寫（見 4.1） |
| 71 | P13 | 目前工作對象是 OpenAI 及其原因 | C | `We are currently facing the very specific challenge of advising OpenAI on how to coordinate the release of a large number of significant results in mathematics…` |
| 76 | P15 | 能追的官方頁面有兩個 | C | 公告頁＋`agmai.org`（後者逐字承諾 `We will publish our recommendations to AI companies on this website.`） |
| 80 | P16 | Amodei 是 Anthropic 執行長、9 月稍早發表〈We Must Pace the Frontier〉 | C | 站上已發布的 `ai-news-pace-the-frontier-20260912`：`news_date` 2026-09-12、`display_order` 147，description 逐字「Anthropic 執行長 Dario Amodei 於 2026 年 9 月 12 日發表」；早於本篇事件日 9/21 |
| 81 | FAQ A1 | 不是監督機構 | C | `agmai` 無決策權句＋公告的 `Importantly` 句 |
| 84 | FAQ A4 | 兩份官方頁面都沒寫能否否決、延後或有無拘束力 | C | 掃 `veto`／`approve`／`approval`／`binding`／`delay`／`postpone`／`final say`：兩頁合計只有 1 筆 `approval`，是意見表單的「未經你同意不會公開」，與發布無關 |
| 100 | meta | 無 U+2011／NBSP／零寬字元；未抄入 `Simons Institue` | C | 機械掃描全部 0 筆 |

### 3.3 協調者裁定（3 條）

| # | 裁定 | 處置 |
| --- | --- | --- |
| 裁定 1 | 新標題維持 | 已核對紀錄 `title` 與內容包 title 逐字相同（`check_article.py` 會比對），未動 |
| 裁定 2 | 「高等研究院（Institute for Advanced Study）」不加「普林斯頓」 | 四頁 `Princeton` 皆 0 筆，未動 |
| 裁定 3 | 刪 P12 的「不是兩個互斥陣營」 | **已刪並改寫成事實** |
| 裁定 4 | 宣言頁那些名字：無人數、無「連署人」標籤 | **已改寫；`sources[2]` 標題的「連署名單」也一併拿掉** |
| 裁定 5 | description 補「OpenAI 表示」 | **已補**，改後 166 字（120–200） |

**小計：本輪查核 45 條、CONFIRMED 42、CHANGED 3、NOT FOUND 0。**

## 4. 改掉的 3 處

### 4.1 P12：刪掉編輯推論，並拿掉「連署人／連署名單」標籤（裁定 3＋4）

- **改前**：…值得一提的是，其中的 Martin Hairer 同時也是 9 月 11 日那封公開信的**連署人之一**（**連署名單**標註他是 2014 年費爾茲獎得主），**顯示這場討論不是「支持顧問小組」與「連署公開信」兩個互斥的陣營**。
- **改後**：…值得一提的是，其中的 Martin Hairer，名字也出現在 9 月 11 日那封公開信的頁面上，頁面在他的名字後面標註 2014 年費爾茲獎。
- **來源**：`https://mathandai.org/`
- **理由**：今天重抓確認，那份名字清單**上方沒有任何標題**（前一行還是宣言正文的最後一段），
  下方才是「Add your name／Endorse the Declaration」，另有一個獨立的 Endorsers 分頁（兩輪都未開啟）。
  「連署人」「連署名單」是來源沒有印出的標籤。「不是兩個互斥陣營」是編輯推論，沒有任何來源這樣寫，
  支撐它的只有 Hairer 一個重疊個案。改寫後的兩句都逐字核對過，且仍然沒有印出任何人數。

### 4.2 description：補上廠商宣稱的歸因（裁定 5）

- **改前**：…起因是**一個尚未發布的內部模型解出超過 100 題數學難題**。
- **改後**：…起因是一個尚未發布的內部模型：**OpenAI 表示它**解出超過 100 題數學難題。
- **來源**：`https://openai.com/index/advisory-group-on-mathematics-and-ai/`
- **理由**：研究紀錄把「超過 100 題」標為 `is_vendor_claim: true`；summary 第 2 句與正文第三段都有歸因，description 之前沒有。
  改後 166 字，仍在 120–200 區間，結尾維持「（2026 年 9 月查證）」。

### 4.3 `sources[2]` 標題：拿掉「連署名單」（同裁定 4）

- **改前**：`A Severe Misalignment of AI in Mathematics（數學家公開信全文與連署名單）`
- **改後**：`A Severe Misalignment of AI in Mathematics（數學家公開信全文）`
- **理由**：同 4.1；來源清單是讀者在文章頁上看得到的文字，不該用來源沒有印出的標籤。
  內容包與研究紀錄兩邊同步改（`check_article.py` 只比對 `sources` 的 `url`，不比對標題）。

## 5. 留給協調者的事

1. **第一段**仍把「解出 Navier–Stokes」與「超過 100 題」寫在「OpenAI 在官方網站公告」的框架裡，沒有另掛一次「OpenAI 表示」。
   裁定第 5 條只點名 description，而 FACTCHECK-47 的歸因密度規則是「開頭段最多一個歸因語」，第一段已經有「OpenAI 在官方網站公告」，
   再加就超標，因此**沒有動**。若站主要求第一段也逐句歸因，要同時放寬那條密度規則。
2. **「OpenAI 的兩份公告」這個用字**：navier-stokes 那一頁的頁首分類印的是 `Research Publication`（顧問小組公告頁印的是 `Company`）。
   叫它「公告」是可通的中文說法但不是逐字對應，同一批文字在 P14 用的是精準的「四份官方頁面」。**屬用字而非事實，未改**，
   若要統一可把 P2／FAQ A5／callout 的「兩份公告」改成「兩份官方頁面」。
3. **「尚未發布的內部模型」的「尚未發布」是推論**：兩頁都只寫 `internal model`，`not_said` 也記著「沒有寫是否會對外發布」。
   研究紀錄自己的 `must_not_write` 用的就是「至今未發布」，所以照留；這是全篇唯一一個沒有逐字來源的限定詞。
4. **`agmai.org` 的 `/input` 表單與 `mathandai.org` 的 Endorsers 分頁兩輪都沒有開啟**。
   「截至查核當天尚未刊出任何一份建議」只以首頁四節與站內連結為據；上線前若要更新狀態句，要再看一次那一頁。
5. **繪圖**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug（DELTA-4-7 §15 是刻意的）。
   圖上會用到的數字在本輪定稿後仍是 **9、100、8/28、9/11、9/21**，四個節點文字與 caption 兩輪都沒有動過。

## 6. 自檢輸出（原樣）

```
OK ai-news-openai-math-advisory-20260921 zh-TW paragraphs 2352
check_article exit=0
```

```
ai-news-openai-math-advisory-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-openai-math-advisory-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-math-advisory-20260921/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

兩個 `image_missing` 與一個 `raw_internal_url` 是 DELTA-4-7 預期的（繪圖與 relink 都還沒做），其餘沒有任何問題。
段落字數 2,384 → **2,352**（<3,000）。

## 7. 結論

**ok**。第一輪的 13 處變更逐條回一手來源全部成立，抽查的 29 條 CONFIRMED 全部成立，
32 條英文引句全部命中正確的來源頁，機械掃描（`Princeton`／地區字詞／成員名單／漏空格／禁用字元／結尾連結／圖解 caption）全部乾淨。
本輪的 3 處變更都是協調者裁定要改的，沒有新發現的事實錯誤。
只動了內容包、研究紀錄與這份報告三個檔；沒有 `git add`／`commit`，repo 裡沒有留任何暫存檔。
