# 翻譯代理共用規格：新聞批次 4.3 AI（en、ja、ko、zh-CN）

你負責把**一篇**已經過兩輪獨立查核的繁中文章翻成四個語言。繁中原稿是唯一依據：翻譯不再查新資料、不增刪事實。發現原稿疑似錯誤時**不要自己改**，寫進回報。

- repo 根目錄（worktree）：`C:/Users/x8120/mokaair/.claude/worktrees/travel-guide-articles-planning-eab8c5`（以下稱 `<ROOT>`）
- 暫存目錄：`C:/Users/x8120/AppData/Local/Temp/claude/C--Users-x8120-mokaair--claude-worktrees-travel-guide-articles-planning-eab8c5/6bc15b49-339e-47bf-9727-38b4d1d65292/scratchpad`（以下稱 `<SCRATCH>`）

## 0. 先讀

1. `<ROOT>/docs/news-2026-batch-4/BRIEF.md` 的「翻譯」一節，與 `<ROOT>/docs/news-2026-batch-4/ai.md`（重點是「不可以寫」的界線：不是訂閱／購買／升級／投資建議、廠商宣稱一律歸因、不推定台灣可用、沒有投資免責 callout）。
2. 原稿：內容包 `<ROOT>/apps/api/app/guides/content/<slug>.json` 的 `locales["zh-TW"]`，以及研究紀錄 `<ROOT>/docs/ai-news-2026-09-late/research/<slug>.json`（`verified_facts` 的 `verbatim_quote` 是來源原文；翻 en 時產品名、功能名、方案名、機關名、文件名、條文用語以英文原文為準，**不要從中文回譯**）。

## 1. 每個語言交一份 GuideDocument

寫到 `<SCRATCH>/agents/tr-ai/<slug>.<locale>.json`（先 `mkdir -p` 那個 `tr-ai` 目錄；locale 是 `en`、`ja`、`ko`、`zh-CN`），內容是 `{"title","description","hero","blocks","sources"}`，形狀與 zh-TW 完全相同：

- blocks 的型別、順序、heading level、table 的 header 欄數與 rows 列數、summary 的句數、faq 的題數，全部照原稿。
- `hero.src` → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`；image 區塊的 `src` → `/guides/<slug>/diagram-1-<en|ja|ko|zh-cn>.svg`（檔名裡的 locale 一律小寫）；width、height、credit 不變；alt 與 caption 要翻譯。
- `sources`：title 翻譯（公司名、機關名與文件原名保留原文或用該語言的官方名稱），**url 與 checked_on 不變、順序不變**。
- 兩個結尾 link：`url` 換成 `https://mokaair.com/<locale>/life/<目標 slug>`（locale 大小寫照 `en`、`ja`、`ko`、`zh-CN`）。
  - 第一個連結指向索引 `ai-news-2026-january-september-index`，它的標題這一批會改名，`text` **逐字**用下面這一行（不要用內容包裡現在的舊標題）：
    - en：`2026 AI News Roundup: Highlights and Daily Life Applications from January to September`
    - ja：`2026年AIニュース総まとめ：1月から9月までの重要動向と実生活への応用`
    - ko：`2026년 AI 뉴스 총정리: 1월부터 9월까지의 핵심과 일상 적용`
    - zh-CN：`2026 年 AI 新闻总整理：1 月至 9 月的重点与生活应用`
  - 第二個連結的 `text` 必須逐字等於目標內容包在該 locale 的 `title`。目標是同一批的另一篇，多半還沒有該語言：**先用你對該標題的翻譯**，並在回報裡寫明（協調者會在全部定稿後用工具統一對齊）。
- **AI 篇沒有投資免責 callout。** 原稿只有一個一般的 callout（查核日、來源範圍、本站沒有實測、不是訂閱或投資建議之類），照譯即可，不要自己加免責句，也不要把它擴寫。

### 寫法

- 讀起來要像該語言原生的 AI 新聞解析，不是逐字直譯；但**每個日期、數字、金額、百分比、版本號、模型名、方案名、條號、機關名、條件、但書、歸因（「OpenAI 表示」「Google 說明」「依 NVIDIA 的說法」「官方寫明將…」「本站沒有實測」「編輯設計的例子」「本文引用的這幾頁沒有寫」）都要保留，不可變強或變弱**。
  - 限定詞一個都不能掉：「預計／plans to」「將／will」「陸續推出／rolling out」「最高／up to」「約」「至少」「可能／may」「例如／like」「內部評測／in internal evaluations」「私人預覽／private preview」「即將推出／coming soon」「視地區而定／may vary by region」。
  - **狀態不可升級**：「官方寫明將取代」不可譯成「已取代」；「陸續推出」不可譯成「已全面開放」；「計畫」「目標」不可譯成既成事實；tape-out 不是量產；保密遞交 S-1 草稿不是「申請上市」「即將上市」。
  - 「官方沒有寫」「這幾頁沒有提到」不可以譯成「沒有這件事」「官方否認」。
- **保留台灣讀者視角**：「台灣讀者」照譯，不改成讀者所在地；原稿寫「官方頁面沒有寫出台灣是否開放」就照譯，**不可以自己補上日本、韓國、美國或中國大陸的開放情形、價格或語言支援**。美元價格照原稿寫，不換算當地幣別。
- 日期依語言習慣：en `June 30, 2026`；ja `2026年6月30日`；ko `2026년 6월 30일`；zh-CN `2026 年 6 月 30 日`。
- **數量級逐一驗算**：中文「億」＝10⁸、「兆」＝10¹²。en：1,220 億美元＝$122 billion、300 億＝30 billion、47 億＝4.7 billion、1 兆＝1 trillion、9 億（每週用戶）＝900 million；ja「億／兆」、ko「억／조」與中文同級可直接對應；zh-CN「亿／万亿」（台灣的「兆」在 zh-CN 寫「万亿」）。功率單位「百萬瓦」zh-CN 寫「兆瓦」（MW）、「十億瓦」寫「吉瓦」（GW）。寫完把每個語言的數字與原稿逐一對過一遍。
- 專有名詞：
  - 公司、產品、模型名四個語言都用拉丁字母原名（OpenAI、ChatGPT、GPT-5.5 Instant、GPT-Live-1、Codex、Google、Gemini、Gemini 3.8 Live、Vertex AI、NVIDIA、Hugging Face、Broadcom、Celestica、SoftBank、Amazon、Microsoft、Astral、uv、Ruff、Artificial Analysis、Sierra），不要音譯（不要「オープンAI」「엔비디아」「谷歌」「英伟达」）。
  - 方案名保留英文原名（Free、Go、Plus、Pro、Business、Enterprise、Edu、Google AI Pro、Google AI Ultra）。
  - 功能名、介面名：en 用廠商英文原名（研究紀錄的 `verbatim_quote` 或來源頁）；ja／ko 若廠商自己的日文／韓文官方頁（例如 `openai.com/ja-JP/…`、`openai.com/ko-KR/…`、Google 的日文／韓文部落格）有同一則公告，功能名以它為準（可以上網查這一件事），查不到就保留英文原名，不要自己發明譯名。**原稿括號裡給繁中讀者看的介面名，不要原樣塞進其他語言。**
  - 美國機關與文件：SEC＝en `Securities and Exchange Commission (SEC)`／ja `米証券取引委員会（SEC）`／ko `미국 증권거래위원회(SEC)`／zh-CN `美国证券交易委员会（SEC）`；EDGAR、Form S-1、Form D、Form D/A、draft registration statement、Rule 135、`15 U.S.C. §77f`、`91 FR 30086`、Federal Register 這類名稱與編號照原樣（可在第一次出現時附該語言的說明，但說明不可超出原稿的意思）。
  - 站方語氣：「本站」＝this site／we、`当サイト`（不用「本サイト」）、`본 사이트`（不用「당 사이트」）、`本站`。「本站沒有實測」：en 照語境寫（we have not tested … ourselves）；ja「当サイトは実地の検証を行っておらず」（講裝置時才用「実機での検証」）；ko 一律「본 사이트는 직접 시험해 보지 않았고」（不要寫「검증하지 않았고」，會讀成沒有查證；也不要「실측」）；zh-CN「本站没有实测」。「不是訂閱或購買建議」＝ja「契約や購入を勧めるものではありません」、ko「구독이나 구매를 권하지 않습니다」。「不是投資建議」＝en `not investment advice`、ja「投資助言ではありません」、ko「투자 조언이 아닙니다」、zh-CN「不是投资建议」。「編輯設計的例子」＝en `an example designed by the editors`、ja「編集部が作成した例」、ko「편집부가 만든 예시」、zh-CN「编辑设计的例子」。
  - ja：です・ます體。ko：합니다體。
  - zh-CN：簡體字與大陸常用詞，**不可混入繁體字，也不要只轉字不轉詞**：軟體→软件、硬體→硬件、晶片→芯片、記憶體→内存、頻寬→带宽、網路→网络、作業系統→操作系统、伺服器→服务器、資料→数据、資料中心→数据中心、資訊→信息、資安→网络安全、程式→程序、程式碼→代码、程式語言→编程语言、套件→软件包、開源→开源、應用程式→应用、智慧型手機→智能手机、螢幕→屏幕、語音→语音、即時→实时、推論→推理、運算→计算、算力→算力、雲端→云端、開發者→开发者、支援→支持、預設→默认、透過→通过、使用者→用户、帳號→账号、廣告→广告、訂閱→订阅、募資→融资、營收→营收、上市（IPO）→上市、遞交→递交、專案→项目、檔案→文件、儲存→存储、數位→数字、品質→质量、最佳化→优化。
- 金融相關的三篇（`ai-news-openai-funding-20260331`、`ai-news-openai-s1-20260608`、`ai-news-chatgpt-financial-services-20260910`）：譯文不可比原稿多出任何利多、看好、搶進的語氣（不要 `soars`、`blockbuster`、`mega-round`、「大型調達に沸く」「대박」「重磅」這一類渲染詞），不可出現原稿沒有的估值判斷或上市時程。
- en 允許比中文長；lint 的 `text_length` 超過 6,000 字元只是警告，不要為此刪內容。ja／ko／zh-CN 的段落總字數不得少於原稿的 45%。
- 不要 Markdown、不要 emoji、不要加原稿沒有的句子，FAQ 答案不得有網址。description 不超過 500 字元、summary 一句不超過 300 字元、FAQ 答案不超過 1,000 字元、表格儲存格不超過 300 字元、image alt 不超過 200 字元。
- **CJK 字元要逐字確認**：ja 不可以出現日文沒有的漢字或簡體字、ko 不可以出現不存在的音節或夾雜漢字；en／ko 引用中文原文時要從原稿複製，不要憑記憶打。

## 2. 合併（不要直接編輯內容包 JSON，也不要改 zh-TW）

**每完成一個語言就先合併那一個語言**，不要四個都寫完才合併（中途被切斷時，已完成的語言才留得下來）：

```bash
cd "C:/Users/x8120/mokaair/.claude/worktrees/travel-guide-articles-planning-eab8c5/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/merge_locale.py <slug> <locale> "<你的檔案路徑>"
```

印出 `REFUSED:` 就修你的檔案再合併。順序 en、ja、ko、zh-CN。

## 3. 研究紀錄加 `translations`

在 `<ROOT>/docs/ai-news-2026-09-late/research/<slug>.json` 加上（用 Edit 工具只加這個鍵，其他欄位不動）：

```json
"translations": {"en": {"hero_label": "…", "diagram": {"title": "…", "caption": "（逐字等於該語言內容包 image 區塊的 caption）", "nodes": [["小標","說明"],["…","…"],["…","…"],["…","…"]]}}, "ja": {…}, "ko": {…}, "zh-CN": {…}}
```

對照研究紀錄裡 zh-TW 的 `hero_label` 與 `diagram`（title、caption、四個 nodes）翻。圖上的字會畫在 640px 寬的卡片裡，要短：en 小標 ≤ 18 字元、說明 ≤ 30 字元、hero_label ≤ 24 字元、圖解 title ≤ 38 字元；ja／ko／zh-CN 小標 ≤ 10 字、說明 ≤ 17 字、hero_label ≤ 15 字、title ≤ 25 字。**圖上的每個數字都必須出現在該語言的正文；圖上的狀態詞（將、陸續、計畫、最高）不可以因為要短而拿掉。**

## 4. 自檢

```bash
cd "C:/Users/x8120/mokaair/.claude/worktrees/travel-guide-articles-planning-eab8c5/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug> --full
```

不帶 `--assets`（圖像是下一階段）。允許留下的 FAIL 只有兩種：「link text must be the title of ai-news-2026-january-september-index」（索引改名還沒套用），以及「link text must be the title of <第二個連結的目標>」或該目標還沒有該語言——其他 FAIL 都要修到過。

用 Write／Edit 工具寫檔（含非 ASCII 的檔案不要用 heredoc、`sed -i`、`perl -pi`）。不要用 `uv run`，不要跑 `pack_cli lint`、`pytest`。不要 git add／commit。除了內容包（只經由 merge_locale.py）與研究紀錄的 `translations` 鍵，不動任何 repo 檔案；**不要在 repo 裡留下暫存檔（`out.txt` 之類一律寫到 `<SCRATCH>`）**。任何網路請求（User-Agent、標頭、查詢字串、表單）都不得帶任何人的 email 或個人資料，User-Agent 一律 `Mokaair-editorial`（翻譯原則上不需要上網；只有查某語言的官方產品／功能／機關名稱時才查）。

## 5. 回報（繁體中文，12 行以內）

1. 自檢最後輸出（原樣）。
2. 四個語言各自的 title。
3. 你拿不準的譯名（原文、你的譯法、依據），最多五個。
4. 你懷疑原稿有錯的地方（不要自己改）。
