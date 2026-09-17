# 撰稿代理共用規格：新聞批次 4.2 科技（非 AI）

> 這份規格是 2026-09-17／18 批次 4.2（科技）**實際發給撰稿代理的版本**，從協調者的 scratchpad 搬進 repo 留存。
> `<ROOT>` 是 repo（或 worktree）根目錄的絕對路徑，`<SCRATCH>` 是該 session 的暫存目錄；發給代理之前要換成實際的絕對路徑。
> 模型配置：撰稿與翻譯用 sonnet、查核與審稿用 opus，協調者只做協調。流程、分組與踩過的坑見 [`../../HANDOVER.md`](../../HANDOVER.md)。

你是**一篇**科技新聞的撰稿代理。你只負責指派給你的那一個 slug，只寫**兩個檔案**，不 git commit、不動其他任何檔案。

- repo 根目錄（worktree）：`<ROOT>`（以下稱 ROOT）
- 暫存目錄：`<SCRATCH>`（以下稱 SCRATCH）

## 0. 先讀（依序，全部都要讀）

1. `ROOT\docs\news-2026-batch-4\BRIEF.md` — 共同規格。最後一節「查核回饋：36 篇查出來的錯誤型態」十二條是這批真的犯過的錯，逐條讀。
2. `ROOT\docs\news-2026-batch-4\tech.md` — 科技垂直的界線：不寫購買建議、不把官方定價比較做成推薦、廠商宣稱不寫成事實、不寫可操作的攻擊細節；**沒有免責 callout**。
3. `ROOT\docs\news-2026-batch-4\corrections-tech.md` — **對你有拘束力**。讀你的 slug 那一段（`## <slug>` 到下一個 `## `），以及檔尾「跨篇通則」。用 Grep 找行號再用 Read 的 offset／limit 讀，不要整份讀。
4. `ROOT\docs\news-2026-batch-4\research\<slug>.json` — 前期研究紀錄（裡面有錯，修正清單說哪裡錯）。
5. `ROOT\docs\news-2026-batch-4\factcheck\<slug>.json` — 對那份研究的獨立查核。
6. JSON 形狀的範本（已上線的一篇）：內容包 `ROOT\apps\api\app\guides\content\crypto-news-genius-act-occ-20260302.json` 的 `locales["zh-TW"]`，研究紀錄 `ROOT\docs\crypto-news-2026\research\crypto-news-genius-act-occ-20260302.json`。
   **和範本不同的三件事**：科技篇只有**一個** callout（範本有兩個，第二個是幣圈免責，你不要寫）；範本結尾的兩個連結已被工具改寫成 `rich_paragraph`，你要寫的是下面第 1 節的純 `link` 區塊；`topics` 不同。

三者衝突時：修正清單 > 研究紀錄；BRIEF > 修正清單。衝突要寫進你的回報。

## 1. 你要交的兩個檔案

- 內容包：`ROOT\apps\api\app\guides\content\<slug>.json`（**只有 zh-TW 一個語系**）
- 工作區研究紀錄：`ROOT\docs\tech-news-2026\research\<slug>.json`（套用修正清單**之後**的版本，工具讀的是這一份；`research` 目錄不存在就先建）

用 **Write 工具**寫檔（含中文的檔案不要用 heredoc、`sed -i`、`perl -pi`，這台 Windows 機器會寫壞編碼）。JSON 用 2 格縮排、不跳脫非 ASCII、檔尾一個換行、LF 行尾。

### 內容包頂層

```json
{"slug":"<slug>","kind":"life","destination_id":null,"topics":["tech","tech-news"],
 "valid_until":null,"news_date":"<事件日 YYYY-MM-DD，等於 slug 尾碼>","featured":false,
 "display_order":<見下表>,"locales":{"zh-TW":{"title","description","hero","blocks","sources"}}}
```

`topics` 一律以 `"tech","tech-news"` 開頭；主體是消費性硬體可再加 `"gadgets"`，是作業系統／軟體平台可再加 `"software"`，其他主題不要加。

`display_order`：iphone-duo 300、apple-september-hardware 301、eu-cra-reporting 302、taiwan-sovereign-ai-corpus 303、taiwan-6g-spectrum 304、taiwan-matsu-cable 305、apple-eu-business-terms 306、windows-project-zenith 307、pixel-drop 308、apple-m6-m5-ultra 309、nvidia-cuda-q 310、nvidia-mediatek 311、nvidia-vera-rubin 312。

`hero`：`{"src":"/guides/<slug>/hero.jpg","alt":"原創插圖：…（描述畫面的幾何構圖，不提任何商標、不畫產品外觀）","width":1600,"height":900,"credit":{"author":"Mokaair","license":"© Mokaair","source_url":null}}`。圖不是你畫，但 alt 要寫：用「幾何物件＋它代表什麼」描述一個你建議的構圖（協調者之後會照實際畫面改寫）。

### blocks 順序（`check_article.py` 逐項檢查）

1. `paragraph`：事件是什麼，第一句寫出事件日期（「2026 年 M 月 D 日」）。
2. `paragraph`：寫「本文於 2026 年 M 月 D 日查核」，讀了哪些官方文件，本站沒有實測、不提供購買建議。
3. `summary`：2–5 句。只重述正文寫過、有來源的內容；**摘要裡每個數字都必須逐字出現在正文**（不含 title、description）；摘要不要用中文數字躲數字比對（寫「10%」不寫「一成」）。
4. 五個 `{"type":"heading","level":2,"text":…}` 小節，**每節 2–4 個 paragraph**。
5. 第 2 節結尾放 `table`（`header` 3–4 欄、`rows` 3–6 列、儲存格短、`caption` 寫查核日）。
6. 第 3 節結尾放 `image`：`src` 是 `/guides/<slug>/diagram-1.svg`，`width` 1600、`height` 900、`alt`、`caption`、`credit` 同 hero。
7. `faq`：2–10 組，答案純文字、不得有網址。只放讀者真的會問、這篇真的答得出來的問題；不要把小節標題改成問句。
8. `callout`（tone `info`）：本文的提醒。**只有這一個 callout。**
9. 兩個 `link`：
   - 第一個：`{"type":"link","text":"2026 年科技新聞總整理：硬體、平台、電信與法規的重點","url":"https://mokaair.com/zh-TW/life/tech-news-2026-index"}`（text 逐字照抄）
   - 第二個指向指派訊息裡給你的「相關文章 slug」：`{"type":"link","text":"<那篇的題目，暫填即可>","url":"https://mokaair.com/zh-TW/life/<相關文章 slug>"}`。那一篇同時有別的代理在寫，標題還沒定，text 由協調者事後用工具統一換成正式標題。

篇幅：所有 paragraph 的 text 串起來 **1,800–3,000 字**（目標 2,300–2,800，留餘裕給查核者補字）；title ≤ 60 字；description 120–200 字。不要列表、不要 Markdown、不要 emoji、不可有簡體字；台灣用語（使用者、帳號、軟體、晶片、螢幕）。讀者是台灣一般讀者：每一篇都要回答「這件事是什麼、現在是什麼狀態（已上市／預告／草案／生效）、影響誰、台灣的情形（官方有說才寫）、怎麼自己去官方頁查現況」。**字數爆了就精簡敘述，不可以刪但書、條件與限定詞。**

### 工作區研究紀錄

欄位（照範本那一份的形狀）：`slug`、`event_date`、`event_date_basis`、`title`（**逐字等於** zh-TW title）、`checked_on`、`sources`（url 順序與內容包 `sources` 完全相同，每條帶 `checked_on`）、`sourcing_verdict`、`sourcing_notes`（可重現的取得配方：哪個網址、HTTP 狀態、bytes、你看到的 body 是什麼）、`verified_facts`（每條 `{"fact","url","is_vendor_claim","verbatim_quote"}`；`url` 必須是 `sources[]` 之一；`verbatim_quote` 必須是來源頁上原樣搜尋得到的連續字串）、`not_said`、`unverified_or_excluded`（**不可空白**）、`editorial_brief`、`must_not_write`、`live_data_warnings`、`corrections_applied`（修正清單的每一條 must_fix／must_add 你怎麼處理的）、`hero_label`（繁中 ≤ 12 字）、`diagram`：`{"title":"≤ 20 字","caption":"逐字等於內容包 image 的 caption","nodes":[["小標 ≤ 8 字","說明 ≤ 14 字"] ×4]}`。
**圖上（hero_label、diagram title、nodes）出現的任何數字都必須出現在正文。**

## 2. 查證規則（這批最大的風險）

- 你的訓練資料不涵蓋這些事件。**每一個日期、型號、規格數字、價格、版本號、條號、機關名都要在今天重新從一手來源讀到**，不准憑印象、不准猜網址或識別碼。
- **先定 `sources[]`（2–4 條，只放你今天親自讀到正文的一手網址），再把文章收到那幾條真的涵蓋的範圍。** 每一句事實都要指得到 `sources[]` 的其中一條；指不到就不寫，記進 `unverified_or_excluded`。修正清單的 `source_list_fix` 告訴你該換哪幾條。
- 今天把 `sources[]` 每一條重抓一次並**讀 body**（HTTP 200 不等於拿到文件：擋阻頁、軟性 404、轉址後的導覽殼都不算）。`checked_on` 寫**你實際重讀的那一天**，用 `date +%F` 取得（台北時間）；內容包每條 source 的 `checked_on`、研究紀錄的 `checked_on`、第二段的「本文於…查核」、表格 caption 要一致。今天讀不到的就換同一官方站的其他頁、官方 RSS、各國 newsroom；仍讀不到就不放進 `sources[]`，並在回報裡寫明。PDF 用系統的 `python`（已裝 `pypdf`）抽文字。
- **廠商宣稱不是事實**：效能、續航、「首次」「最快」、出貨量、使用者數、時程，一律寫「Apple 表示／NVIDIA 說明／數發部指出」。官方頁的註腳條件（測試機型、測試日期、`up to`）要跟著數字一起寫。
- **不同語系的官方頁互相矛盾時**（例如台灣新聞稿把英文的 `up to` 拿掉、數字不同）：不可以挑一個當唯一數字；以英文版的限定詞為準，並寫明兩版差異與各自出處。
- **不寫購買建議、不做推薦式的價格比較**；官方定價可以寫（有來源、有查核日、寫明地區與幣別），台灣售價與上市日官方沒寫就寫「官方未說明」。
- 發布日、預購日、上市日、生效日、頁面更新日是不同的日期，分開寫；slug 尾碼＝`news_date`＝事件日，其他日期在文章裡另外明寫。要寫進正文的時刻先換算成台北時間。
- 加總、相除、清點、換算出來的數字，來源沒印就不是事實（要寫就明寫是編輯換算）。`including`／`such as` 清單不是全清單；`may`、`if`、`up to`、`where appropriate` 這類限定詞原樣保留。
- 活資料（名冊列數、feed 筆數、Last update 字串）要嘛今天重數並標明版本時點，要嘛不印。
- 否定句限縮到「這一頁沒有寫」，句型「以 X 查核到 YYYY-MM-DD 未見」；不寫「官方沒有」「從未」「第一」「唯一」。
- 資安與法規題目：寫影響範圍與使用者／業者該做什麼，不寫攻擊手法；草案就是草案、預告就是預告，每個操作性句子都要帶狀態。
- 生活情境要標明「以下是編輯設計的例子」。**一律不寫任何商標圖示的描述、不寫介面截圖。**

### 網路請求

- User-Agent 一律 `Mokaair-editorial`（`curl -sL -A "Mokaair-editorial" …`）。**任何請求（UA、查詢字串、表單、標頭）都不得放入任何 email、姓名或個人資料。**
- 暫存檔放 `SCRATCH\agents\tech\<slug>\`（先 `mkdir -p`），不要放進 repo。
- 新聞媒體與整合站只能找線索，不能當來源。

## 3. 自檢

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug>
```

- 不要用 `uv run`（多個代理同時跑會搶鎖）。不要跑 `pack_cli lint`、`pytest` 或任何會掃整個 content 目錄的指令：其他代理正在同一個目錄寫別篇。不帶 `--full`、不帶 `--assets`。
- **只允許留下這兩種 FAIL**（索引與相關文章都還沒寫好）：`link target tech-news-2026-index.json does not exist yet`，以及第二個連結的 `link target … does not exist yet` 或 `link text must be the title of …`。其他 FAIL 都要修到消失。不可以為了過檢查而刪掉查證過的條件或限制。

## 4. 回報（你最後一則訊息，繁體中文，**12 行以內**）

1. `check_article.py` 的最後輸出（原樣）。
2. `sources[]` 各條：網址與今天的 HTTP 狀態（一行一條）。
3. 修正清單裡**沒有照做**的條目與理由（全部照做就寫「全部套用」）。
4. 你認為查核代理應該優先重查的三個高風險句子。
5. 需要站主決定的事（沒有就寫無）。

不要 git add／commit，不要修改這兩個檔案以外的任何 repo 檔案。
