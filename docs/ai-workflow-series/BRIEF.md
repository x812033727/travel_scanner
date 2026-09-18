# 「多模型 AI 工作流」系列：撰稿規格（每篇原文重用）

你要為 Mokaair（台灣的旅遊網站，另有「生活分享」專區）寫**一篇**教學文章，主題是 AI 工作流與「把不同模型串起來」。
讀者是台灣的一般使用者與會寫一點程式的人；入門篇不假設會寫程式，技術篇假設讀者會跑 Python 與命令列。
你會拿到這份規格加一段「指派」（slug、標題、切角、程度、必連的站內文章、不可重複的既有文章、來源種子網址、`display_order`）。

- repo 根目錄（worktree）：`C:\Users\x8120\mokaair\.claude\worktrees\travel-guide-articles-planning-eab8c5`（以下 ROOT）
- 暫存目錄：`C:\Users\x8120\AppData\Local\Temp\claude\C--Users-x8120-mokaair--claude-worktrees-travel-guide-articles-planning-eab8c5\6bc15b49-339e-47bf-9727-38b4d1d65292\scratchpad`（以下 SCRATCH）
- 系列工作區：`ROOT\docs\ai-workflow-series\`（`README.md`、`series.py`、`check_article.py`、`models-seen.json`、`research/`）

## 0. 先讀

1. `ROOT\docs\ai-workflow-series\models-seen.json`：查證當日官方模型頁抄下的模型 id 清單（id、url、verbatim、checked_on）。**正文與程式裡出現的模型 id 只能用這份清單裡的**；清單沒有而你需要的，自己到官方模型頁查證後**加進去**（一樣要 verbatim 與 url），不可以憑記憶寫。
2. 站上與你這篇相鄰的既有文章（指派會列 slug）：用 Read 讀 `ROOT\apps\api\app\guides\content\<slug>.json` 的 zh-TW `title` 與前幾段，**不要重寫它們講過的事**，該引用時用結尾的 link。
3. 一篇已完成的同系列文章（指派若有給）當形狀範本。

## 1. 交付物（只動這兩個檔）

| 檔案 | 內容 |
| --- | --- |
| `ROOT\apps\api\app\guides\content\<slug>.json` | 內容包（第 2 節），**先寫這個**，寫完就存 |
| `ROOT\docs\ai-workflow-series\research\<slug>.json` | 研究紀錄（第 5 節） |

不要在 repo 裡留任何暫存檔（`out*.txt` 一律寫到 `SCRATCH\agents\workflow\<slug>\`）；不要 git add／commit；不要跑 `pack_cli ingest`（它會拒絕子主題）；圖檔由協調者依你的研究紀錄畫，你不畫圖。

## 2. 內容包的形狀

```json
{"slug":"<slug>","kind":"life","destination_id":null,"topics":["ai","tutorial","ai-coding"],"valid_until":null,"news_date":null,
 "featured":false,"display_order":<指派>,"locales":{"zh-TW":{"title":"…","description":"…",
 "hero":{"src":"/guides/<slug>/hero.jpg","alt":"…","width":1600,"height":900},"blocks":[…],"sources":[…]}}}
```

- `title` ≤ 60 字、含關鍵詞、說清楚讀完能做到什麼；`description` 120–200 字，第一句就是結論。
- `hero.alt` ≤ 200 字：先寫「原創插圖：」再一句話描述畫面（協調者畫完會改成實際畫面）。
- `sources`：3–8 筆，**全部是官方一手頁面**（供應商文件、定價頁、模型頁、套件官方文件、GitHub 官方 repo 的 README／docs、RFC／規格書）；每筆 `{"title","url","checked_on"}`，`checked_on` 寫你實際重讀那一天（`date +%F`）。不放新聞、部落格轉述、影片、整合站。網址不得帶追蹤參數。

區塊骨架（照順序，每種都要有）：

1. 兩段 `paragraph` 導言：第一段用一句話講清楚這篇回答什麼問題與結論；第二段講讀者做完會得到什麼、需要什麼前提（入門篇：不用寫程式；技術篇：Python 3.11+、哪些套件、哪些金鑰）。
2. `summary`：2–5 句，每句 ≤ 300 字，放在第一個 heading 之前；每一句都要是正文裡有的事實。
3. 三到六個 `{"type":"heading","level":2}` 章節，每節一到三段 `paragraph`；步驟用 `{"type":"list","ordered":true}`；技術篇在講到的那一節放 `code` 區塊（第 3 節規則）。
4. 一張圖解：`{"type":"image","src":"/guides/<slug>/diagram-1.svg","alt":"四格圖解：…／流程圖：…","width":1600,"height":900,"caption":"…（含查證年月）"}`，放在它解釋的那一節之後；圖上的字由研究紀錄的 `diagram` 決定，**圖上出現的每一個數字都必須出現在正文**。
5. 一個 `table`（≤ 6 欄、≤ 30 列、格子 ≤ 300 字、`caption` 寫查證年月）：比較矩陣、參數表或估算表。
6. 一個 `callout`（`tone` 為 `tip`／`warning`／`info`）：最常踩的坑或最重要的提醒；**整篇只有一個**，不寫免責聲明。
7. `faq`：3–8 題，`question` ≤ 200、`answer` ≤ 1,000 字；答案不得有網址；答案 ⊆ 正文。
8. 結尾兩個 `link` 區塊（純 link，協調者事後用工具轉成站內文章連結）：
   - 第一個指向系列目錄：`{"type":"link","text":"多模型 AI 工作流教學：從拆任務到串接不同模型","url":"https://mokaair.com/zh-TW/life/ai-workflow-tutorials"}`（text 逐字照抄）。
   - 第二個指向指派給的既有文章：text 打開那個內容包抄它 zh-TW 的 `title`，逐字相同。
   正文中間**不要**再放 `link` 區塊；提到別篇用文字點名即可，協調者會用 `pack_cli autolink` 處理。

字數：正文 1,800–3,000 個中文字（不含標題、表格、程式、FAQ）；寫滿一個主題就停。區塊裡不能有 HTML、Markdown 語法或控制字元；不放截圖，介面用文字描述。

## 3. 程式範例（技術篇必備）

- 技術篇（指派標「進階」）**至少兩個** `code` 區塊：`{"type":"code","label":"檔名或用途（需要哪些套件）","language":"python|bash|json|yaml","code":"…"}`；入門篇可以零個或一個。
- 每塊 **≤ 80 行**、2 空白縮排；能單獨執行或單獨看懂；Python 一律 `python -m py_compile` 得過（協調者的檢查器會抽出來編譯），bash 要過 `bash -n`，json 要能 `json.loads`，yaml 要能 `yaml.safe_load`。
- **金鑰一律從環境變數讀**（`os.environ["OPENAI_API_KEY"]`、`"$ANTHROPIC_API_KEY"`），不寫字面金鑰、不寫 `<YOUR_KEY>` 這種佔位；網路呼叫帶 `timeout`；不用 `eval`、不寫刪檔命令。
- 用的套件、函式簽名、參數名、端點路徑、CLI 旗標，**每一個都當天查官方文件**並記進研究紀錄（`verified_facts` 帶 verbatim）；不確定的參數就不要用。範例裡的模型 id 只能用 `models-seen.json` 裡的。
- 範例要示範這一篇的主題（路由、交接、互審……），不是套件的 hello world；同一個範例分兩段解說時，第二段用新的 `code` 區塊，不要重貼整段。
- 範例輸出不要捏造：要寫「跑出來像這樣」就用「示意」字樣，或不寫輸出。

## 4. 文字規則

- **事實先查再寫**：方案名、價格、免費額度、模型名、功能是否已推出、速率限制、上下文長度，全部今天到供應商官網確認並寫進 `sources` 與研究紀錄；官網打不開就寫「以官網為準」，不猜數字。今天的日期用 `date +%F` 取得；你訓練資料裡的模型與價格多半已過時，**不能憑記憶寫**。
- 系列統一用語：token（不寫「詞元」）、上下文視窗、提示詞、推理模型、代理（Agent）、工具呼叫（tool calling）、結構化輸出、路由（routing）、級聯（cascade）、評審模型（judge）、追蹤（tracing）、評測（evals）、幻覺；第一次出現可括號附英文。台灣用語（軟體、網路、資料、程式、使用者、品質）。
- 廠商宣稱一律歸因（「OpenAI 表示」「Google 的文件寫」）；比較速度、品質時只引官方公布的數字，不寫自己沒測過的排名；本站沒有實測就寫「本站沒有實測」。
- 不寫「作為一個 AI」「總結來說」這類贅語；不用驚嘆號；不對任何產品做人身式的褒貶；不寫訂閱、購買或投資建議；不寫「台灣可用」除非官方頁寫了。
- 提到 Claude Code、Codex、Gemini CLI 等本站已有系列的工具時，只講本篇需要的用法，其餘連到既有文章（指派會給 slug）。

## 5. 研究紀錄 `ROOT\docs\ai-workflow-series\research\<slug>.json`

```json
{"slug":"<slug>","title":"<逐字等於 zh-TW title>","checked_on":"<date +%F>","level":"入門|進階",
 "sources":[{"title":"…","url":"…","checked_on":"…"}],
 "verified_facts":[{"fact":"…","url":"<sources 之一>","is_vendor_claim":true|false,"verbatim_quote":"<來源頁上原樣搜尋得到的連續字串>"}],
 "unverified_or_excluded":["查了但沒寫的事與原因（不可空白）"],
 "must_not_write":["這篇刻意不寫的東西"],
 "editorial_brief":"這篇的切角與跟相鄰文章的分工，2–4 句",
 "code_samples":[{"label":"<與內容包 code 區塊的 label 相同>","language":"python","lines":42,"compiled_on":"<date +%F>","checked_against":["<官方文件網址>"]}],
 "hero_label":"≤ 12 字（畫在主圖上的一句話）",
 "diagram":{"layout":"flow|grid","title":"≤ 20 字","caption":"<逐字等於內容包 image 的 caption>",
            "nodes":[["小標 ≤ 8 字","說明 ≤ 14 字"], … 3–5 格（flow 是左→右的步驟，grid 是 2×2 四格）]}}
```

- `verified_facts` 每一條的 `url` 必須是 `sources[]` 之一；`verbatim_quote` 是你抓到的正文裡的**連續字串**（不用 `...` 拼接）；每個參數名、旗標、價格、限額、模型 id 都要有一條。
- 研究紀錄的 `title`、`sources`（順序與內容）、`diagram.caption` 與內容包完全一致。

## 6. 網路與工具

- 抓頁用 `curl -sL -A "Mokaair-editorial"`（主機拒絕這個 UA 時可退回 curl 預設 UA，不可自訂別的）；**任何請求的 UA、標頭、查詢字串、表單都不得帶入任何人的 email 或個人資料**。GitHub 官方 repo 的 README 可用 `raw.githubusercontent.com`。PDF 用系統 `python`（有 `pypdf`）抽字。
- 自檢（從 `apps/api`，不要用 `uv run`）：
  `cd "C:/Users/x8120/mokaair/.claude/worktrees/travel-guide-articles-planning-eab8c5/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/ai-workflow-series/check_article.py <slug>`
  要印出 `OK` 才算完成；只允許留下的 FAIL 是「link text must be the title of ai-workflow-tutorials」（目錄篇還沒寫好時）。不可以為了過檢查而刪掉查證過的條件或限制。
- 用 Write／Edit 寫檔（含非 ASCII 的檔案不要用 heredoc、`sed -i`、`perl -pi`）。

## 7. 回報（最後一則訊息，繁體中文，12 行以內）

1. 自檢最後輸出（原樣）。
2. 標題、字數、code 區塊數與各自行數。
3. 你查證過但決定不寫的事（最多五條）。
4. 你不確定、想請查核代理優先重看的句子（最多五條）。
5. `models-seen.json` 有沒有新增模型 id。
