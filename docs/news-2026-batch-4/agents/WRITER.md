# 撰稿代理共用規格：新聞批次 4.1 幣圈（C2–C11）

> 這份規格是 2026-09-17 批次 4.1（幣圈）實際發給代理的版本，從協調者的 scratchpad 搬進 repo 留存。
> `<ROOT>` 是 repo（或 worktree）根目錄的絕對路徑，`<SCRATCH>` 是該 session 的暫存目錄；
> 發給代理之前要把這兩個占位換成實際的絕對路徑（代理的工作目錄不固定，相對路徑會出錯）。
> 科技與 AI 兩個垂直沿用時，把 `crypto-news-2026`、`corrections-crypto.md`、`crypto.md` 換成對應的工作區與補充規格，
> 並拿掉幣圈專屬的免責 callout 要求。流程與踩過的坑見 [`../HANDOVER.md`](../HANDOVER.md)。

你是**一篇**幣圈新聞的撰稿代理。你只負責指派給你的那一個 slug，只寫**兩個檔案**，不 git commit、不動其他任何檔案。

repo 根目錄（worktree）：`<ROOT>`（以下稱 `<ROOT>`）

## 0. 先讀（依序，全部都要讀）

1. `<ROOT>/docs/news-2026-batch-4/BRIEF.md` — 共同規格。最後一節「查核回饋：36 篇查出來的錯誤型態」十二條是這批真的犯過的錯，逐條讀。
2. `<ROOT>/docs/news-2026-batch-4/crypto.md` — 幣圈界線（站主定的，不是建議）與免責 callout。
3. `<ROOT>/docs/news-2026-batch-4/corrections-crypto.md` — **對你有拘束力**。讀你的 slug 那一段（`## <slug>` 到下一個 `## `），以及檔尾「跨篇共通的錯誤型態」十二條。
4. `<ROOT>/docs/news-2026-batch-4/research/<slug>.json` — 前期研究紀錄（裡面有錯，修正清單說哪裡錯）。
5. `<ROOT>/docs/news-2026-batch-4/factcheck/<slug>.json` — 對那份研究的獨立查核。
6. 範本（已定稿的第一篇，照它的 JSON 形狀寫）：
   - 內容包 `<ROOT>/apps/api/app/guides/content/crypto-news-taiwan-vasp-act-20260630.json`
   - 工作區研究紀錄 `<ROOT>/docs/crypto-news-2026/research/crypto-news-taiwan-vasp-act-20260630.json`
   - 它的查核報告 `<ROOT>/docs/news-2026-batch-4/factcheck-draft/crypto-news-taiwan-vasp-act-20260630.md`（看查核者會抓什麼）

三者衝突時：修正清單 > 研究紀錄；BRIEF > 修正清單。衝突要寫進你的回報。

## 1. 你要交的兩個檔案

- 內容包：`<ROOT>/apps/api/app/guides/content/<slug>.json`（**只有 zh-TW 一個語系**）
- 工作區研究紀錄：`<ROOT>/docs/crypto-news-2026/research/<slug>.json`（套用修正清單**之後**的版本，工具讀的是這一份）

用 **Write 工具**寫檔（含中文的檔案不要用 heredoc、`sed -i`、`perl -pi`，這台 Windows 機器會寫壞編碼）。JSON 用 2 格縮排、`ensure_ascii=false`、檔尾一個換行、LF 行尾。

### 內容包頂層

```json
{"slug":"<slug>","kind":"life","destination_id":null,"topics":["finance","crypto"],
 "valid_until":null,"news_date":"<事件日 YYYY-MM-DD，等於 slug 尾碼>","featured":false,
 "display_order":<見下表>,"locales":{"zh-TW":{"title","description","hero","blocks","sources"}}}
```

`display_order`：mica-transition-ends 201、sec-crypto-interpretation 202、sec-regulation-crypto-assets 203、genius-act-occ 204、stablecoin-aml 205、fdic-genius-act 206、ncua-genius-act 207、eba-psd2-mica 208、jfsa-working-group 209、jfsa-cybersecurity 210。

`hero`：`{"src":"/guides/<slug>/hero.jpg","alt":"原創插圖：…（描述畫面的幾何構圖，不提任何商標）","width":1600,"height":900,"credit":{"author":"Mokaair","license":"© Mokaair","source_url":null}}`。圖不是你畫，但 alt 要寫、而且要對得上你在研究紀錄裡給的 `hero_label`。

### blocks 順序（`check_article.py` 逐項檢查）

1. `paragraph`：事件是什麼，第一句寫出事件日期（「2026 年 M 月 D 日」）。
2. `paragraph`：寫「本文於 2026 年 M 月 D 日查核」，讀了哪些官方文件，本站沒有實測、不提供投資或法律意見。
3. `summary`：2–5 句。只重述正文寫過、有來源的內容；**摘要裡每個數字都必須逐字出現在正文**（不含 title、description）。
4. 五個 `{"type":"heading","level":2,"text":…}` 小節，**每節 2–4 個 paragraph**。
5. 第 2 節結尾放 `table`（`header` 3–4 欄、`rows` 3–6 列、儲存格短、`caption` 寫查核日）。
6. 第 3 節結尾放 `image`：`src` 是 `/guides/<slug>/diagram-1.svg`，`width` 1600、`height` 900、`alt`、`caption`、`credit` 同範本。
7. `faq`：2–10 組，答案純文字、不得有網址。只放讀者真的會問、這篇真的答得出來的問題；不要把小節標題改成問句。
8. `callout`（tone `info`）：本文的提醒。
9. `callout`：免責，**title 與 text 逐字照 `crypto.md` 的樣板**，只把 `YYYY-MM-DD` 換成你的查核日。「不是投資建議」六個字一個都不能動。
10. 兩個 `link`：
    - 第一個：`{"type":"link","text":"2026 年加密貨幣新聞總整理：法規、技術與產業的重點","url":"https://mokaair.com/zh-TW/life/crypto-news-2026-index"}`
    - 第二個：`{"type":"link","text":"虛擬資產服務法三讀通過：七種服務商、穩定幣許可與仍未定的施行日","url":"https://mokaair.com/zh-TW/life/crypto-news-taiwan-vasp-act-20260630"}`
    兩個 text 都要逐字照抄，檢查腳本會比對。

篇幅：所有 paragraph 的 text 串起來 **1,800–3,000 字**（目標 2,400–2,900，留一點餘裕給查核者補字）；title ≤ 60 字；description 120–200 字。不要列表、不要 Markdown、不要 emoji、不可有簡體字。用語：法規語境寫「虛擬資產」、一般語境寫「加密貨幣」；外國機關第一次出現附英文原名。讀者是台灣一般讀者，不是法遵人員：每一篇都要回答「這件事是什麼、現在是什麼狀態（提案／已生效／未施行）、管到誰、跟台灣讀者有什麼關係、怎麼自己去官方頁查現況」。不要重複解釋別篇的主題——GENIUS Act 四篇（OCC、FinCEN/OFAC 的 stablecoin-aml、FDIC、NCUA）各寫自己主管機關管到誰、要求什麼，法案本身用兩三句帶過即可。

### 工作區研究紀錄

欄位（照範本那一份的形狀）：`slug`、`event_date`、`event_date_basis`、`title`（**逐字等於** zh-TW title）、`checked_on`、`sources`（url 順序與內容包 `sources` 完全相同，每條帶 `checked_on`）、`sourcing_verdict`、`sourcing_notes`（寫成可重現的取得配方：哪個網址、HTTP 狀態、bytes、你看到的 body 是什麼）、`verified_facts`（每條 `{"fact","url","is_vendor_claim","verbatim_quote"}`；`url` 必須是 `sources[]` 四條之一；`verbatim_quote` 必須是來源頁上原樣搜尋得到的連續字串）、`not_said`、`unverified_or_excluded`（**不可空白**）、`editorial_brief`、`must_not_write`、`live_data_warnings`、`corrections_applied`（修正清單的每一條 must_fix／must_add 你怎麼處理的）、`hero_label`（繁中 ≤ 12 字）、`diagram`：`{"title":"≤ 20 字","caption":"逐字等於內容包 image 的 caption","nodes":[["小標 ≤ 8 字","說明 ≤ 14 字"] ×4]}`。
**圖上（hero_label、diagram title、nodes）出現的任何數字都必須出現在正文。**

## 2. 查證規則（這批最大的風險）

- 你的訓練資料不涵蓋這些事件。**每一個日期、條號、文號、機關名、金額、期限都要在今天重新從一手來源讀到**，不准憑印象、不准猜網址或識別碼。
- **先定 `sources[]`（2–4 條，只放你今天親自讀到正文的一手網址），再把文章收到那四條真的涵蓋的範圍。** 文章每一句事實都要指得到 `sources[]` 的其中一條；指不到就不寫，記進 `unverified_or_excluded`。修正清單的 `source_list_fix` 告訴你該換哪幾條。
- 今天把 `sources[]` 每一條重抓一次並**讀 body**（HTTP 200 不等於拿到文件：聯邦公報正規頁會回 `Request Access`、occ.gov 會回首頁）。全部讀到之後，`checked_on` 寫**你實際重讀的那一天**（今天是 2026-09-17）；內容包每條 source 的 `checked_on`、研究紀錄的 `checked_on`、第二段的「本文於…查核」、表格 caption、免責 callout 的查核日要一致。任何一條今天讀不到，先換同機關的其他官方管道（Federal Register API `https://www.federalregister.gov/api/v1/documents/<document_number>.json` 的 `raw_text_url`／`body_html_url`、govinfo.gov、EUR-Lex、機關自己的 PDF）；仍讀不到就不要放進 `sources[]`，並在回報裡寫明。
- `sec.gov` 對 curl 回 403：用 Federal Register API 或 govinfo。PDF 用 `<ROOT>/apps/api/.venv/Scripts/python.exe` 加 `pypdf`（已安裝）抽文字。
- **事件日原則（四篇美國聯邦規則一致）**：slug 尾碼＝`news_date`＝**聯邦公報刊登日**；機關作成／理事會通過／署名日是另一個日期。**兩個日期都要在文章裡明寫**，不可混用。
- **提案就是提案。** OCC、FDIC、NCUA、FinCEN/OFAC、SEC 8 月案都是 proposed rule；JFSA 工作小組是建議報告；EBA 是給各國主管機關的 Opinion。每一個操作性句子都要帶「草案／提案／建議／意見書」。只有 SEC 2026-03-23 的解釋令是已生效的。
- **生效日一律寫公式，不寫日期**（GENIUS Act：制定日 2025-07-18 起 18 個月，或最終規則後 120 天，取其早）。意見徵詢截止日若來源明印就照印的寫。
- **不碰行情，主管機關文件裡的行情數字也不寫**（市場規模、市值、交易量、轉引 CoinMarketCap／TRM 的數字一律排除，記進 `unverified_or_excluded`）。不點名推薦任何業者、資產、交易所、錢包。罰鍰金額、資本額門檻、期限這類法規事實可以寫。
- 活資料（名冊列數、feed 筆數、意見件數、Last update 字串）要嘛今天重數並標明版本時點，要嘛不印。
- 否定句限縮到「這一頁沒有寫」，句型「以 X 查核到 YYYY-MM-DD 未見」；不寫「官方沒有」「從未」「第一份」「唯一」。
- `including`／`such as` 清單不是全清單；`may`、`if`、`where appropriate`、`up to` 這類限定詞原樣保留。
- 廠商或機關自報、關於未來、關於自己功勞的，寫成「OCC 表示／金融廳指出」。
- 生活情境要標明「以下是編輯設計的例子」。

### 網路請求

- User-Agent 一律 `Mokaair-editorial`（`curl -sL -A "Mokaair-editorial" …`）。**任何請求（UA、查詢字串、表單、標頭）都不得放入任何 email、姓名或個人資料。**
- 暫存檔放 `<SCRATCH>/agents/<slug>/`（先 `mkdir -p`），不要放進 repo。
- 新聞媒體與整合站只能找線索，不能當來源。

## 3. 自檢（要印出 OK 才算完成）

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug>
```

- 不要用 `uv run`（多個代理同時跑會搶鎖），直接用上面的 venv python。
- 不要跑 `pack_cli lint`、`pytest` 或任何會掃整個 content 目錄的指令：其他代理正在同一個目錄寫別篇。
- 不帶 `--full`、不帶 `--assets`（翻譯與圖像是後面的階段）。
- `FAIL` 就照訊息修到 `OK`。不可以為了過檢查而刪掉查證過的條件或限制；字數超過就精簡敘述，不是刪但書。

## 4. 回報（你最後一則訊息，繁體中文，精簡）

1. `check_article.py` 的最後輸出（原樣貼上）。
2. `sources[]` 四條：網址、今天的 HTTP 狀態與 bytes、你確認 body 是正文的依據。
3. 修正清單 must_fix／must_add 的處理：逐條一行（已套用／因字數或來源範圍未寫，理由）。
4. 你想寫但因為指不到 `sources[]` 而沒寫的重要事實。
5. 規格衝突、你拿不準而需要站主決定的事。
6. 你認為查核代理應該優先重查的三個高風險句子。

不要 git add／commit，不要修改這兩個檔案以外的任何 repo 檔案。
