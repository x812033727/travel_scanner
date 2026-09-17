# 翻譯代理共用規格：新聞批次 4.1 幣圈（en、ja、ko、zh-CN）

> 這份規格是 2026-09-17 批次 4.1（幣圈）實際發給代理的版本，從協調者的 scratchpad 搬進 repo 留存。
> `<ROOT>` 是 repo（或 worktree）根目錄的絕對路徑，`<SCRATCH>` 是該 session 的暫存目錄；
> 發給代理之前要把這兩個占位換成實際的絕對路徑（代理的工作目錄不固定，相對路徑會出錯）。
> 科技與 AI 兩個垂直沿用時，把 `crypto-news-2026`、`corrections-crypto.md`、`crypto.md` 換成對應的工作區與補充規格，
> 並拿掉幣圈專屬的免責 callout 要求。流程與踩過的坑見 [`../HANDOVER.md`](../HANDOVER.md)。

你負責把**一篇**已經獨立查核過的繁中文章翻成四個語言。繁中原稿是唯一依據：翻譯不再查新資料、不增刪事實。發現原稿疑似錯誤時**不要自己改**，寫進回報。

repo 根目錄（worktree）：`<ROOT>`（以下稱 `<ROOT>`）

## 0. 先讀

1. `<ROOT>/docs/news-2026-batch-4/BRIEF.md` 的「翻譯」一節，與 `<ROOT>/docs/news-2026-batch-4/crypto.md` 的「每篇必帶免責 callout」「其他語言用自己的標記」。
2. 原稿：內容包 `<ROOT>/apps/api/app/guides/content/<slug>.json` 的 `locales["zh-TW"]`，以及研究紀錄 `<ROOT>/docs/crypto-news-2026/research/<slug>.json`（`verified_facts` 的 `verbatim_quote` 是來源原文，翻 en 時機關名、文件名、條文用語以原文為準，不要從中文回譯）。

## 1. 每個語言交一份 GuideDocument

寫到 `<SCRATCH>/agents/tr/<slug>.<locale>.json`（先 `mkdir -p` 那個 `tr` 目錄；locale 是 `en`、`ja`、`ko`、`zh-CN`），內容是 `{"title","description","hero","blocks","sources"}`，形狀與 zh-TW 完全相同：

- blocks 的型別、順序、heading level、table 的 header 欄數與 rows 列數、summary 的句數、faq 的題數，全部照原稿。
- `hero.src` → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`；image 區塊的 `src` → `/guides/<slug>/diagram-1-<en|ja|ko|zh-cn>.svg`（檔名裡的 locale 一律小寫）；width、height、credit 不變；alt 與 caption 要翻譯。
- `sources`：title 翻譯（機關名與文件原名保留原文或用該語言的官方名稱），**url 與 checked_on 不變、順序不變**。
- 兩個 link：`url` 換成 `https://mokaair.com/<locale>/life/<目標 slug>`（locale 大小寫照 `en`、`ja`、`ko`、`zh-CN`），`text` 必須**逐字等於**目標內容包在該 locale 的 `title`——打開 `<ROOT>/apps/api/app/guides/content/<目標 slug>.json` 複製 `locales[<locale>].title`。目標若還沒有該語言，**先不要自己編**，在回報裡寫明，並暫時用你對該標題的翻譯（協調者會在目標定稿後統一換掉）。
- **免責 callout 用該語言自己的標記，不是中文那句的翻譯**（逐字包含）：
  - en：`not investment advice`（例："This article is an information summary and is not investment advice."）
  - ja：`投資助言ではありません`
  - ko：`투자 조언이 아닙니다`
  - zh-CN：`不是投资建议`
  其餘句子忠實翻譯樣板的意思（不推薦任何加密資產、交易所、錢包或發行方；不含價格、漲跌幅與買賣時機；以主管機關與業者當期公告為準；查核日；價格波動大、可能全額損失、部分服務不受存款保險或投資人保護制度保障；以官方公告或合格專業人員意見為準）。

### 寫法

- 讀起來要像該語言原生的法規新聞解析，不是逐字直譯；但**每個日期、數字、金額、條號、文號、機關名、條件、但書、歸因（「OCC 表示」「草案」「提案」「建議」「本站沒有實測」「編輯設計的例子」）都要保留，不可變強或變弱**。「草案／proposed rule」「意見書／Opinion」「建議報告」這類定位詞一個都不能掉。
- 保留台灣讀者視角（「台灣讀者」「台灣的虛擬資產服務法」照譯，不改成讀者所在地）。
- 日期依語言習慣：en `June 30, 2026`；ja `2026年6月30日`；ko `2026년 6월 30일`；zh-CN `2026 年 6 月 30 日`。年月日數字不變，幣別與金額不變。
- 專有名詞：
  - en：外國機關、法案、文件用其官方英文名（Office of the Comptroller of the Currency、Federal Register、notice of proposed rulemaking、Markets in Crypto-Assets Regulation (MiCA)）。台灣的機關與法律用官方英文名（Financial Supervisory Commission；Virtual Asset Service Act 若來源沒有官方英譯就寫 "Virtual Asset Service Act (虛擬資產服務法)" 並維持一致）。
  - ja：暗号資産、ステーブルコイン、金融庁、です・ます體。法規語境用「暗号資産」，不用「仮想通貨」。
  - ko：가상자산、스테이블코인、합니다體。
  - zh-CN：簡體字與大陸常用詞（账号、软件、信息、监管、稳定币、虚拟资产／加密货币），**不可混入繁體字**；台灣法律名稱寫《虚拟资产服务法》。
  - 美國 CFR 條次、Release No.、FR 引註（91 FR 10202）、EU 文件編號照原樣，不翻。
- en 允許比中文長；lint 的 `text_length` 超過 6,000 字元只是警告，不要為此刪內容。ja／ko／zh-CN 的段落總字數不得少於原稿的 45%。
- 不要 Markdown、不要 emoji、不要加原稿沒有的句子，FAQ 答案不得有網址。

## 2. 合併（不要直接編輯內容包 JSON，也不要改 zh-TW）

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/merge_locale.py <slug> <locale> "<你的檔案路徑>"
```

印出 `REFUSED:` 就修你的檔案再合併。四個語言依序 en、ja、ko、zh-CN 合併。

## 3. 研究紀錄加 `translations`

在 `<ROOT>/docs/crypto-news-2026/research/<slug>.json` 加上（用 Edit 工具只加這個鍵，其他欄位不動）：

```json
"translations": {"en": {"hero_label": "…", "diagram": {"title": "…", "caption": "（逐字等於該語言內容包 image 區塊的 caption）", "nodes": [["小標","說明"],["…","…"],["…","…"],["…","…"]]}}, "ja": {…}, "ko": {…}, "zh-CN": {…}}
```

圖上的字會畫在 640px 寬的卡片裡，要短：en 小標 ≤ 18 字元、說明 ≤ 30 字元、hero_label ≤ 24 字元、圖解 title ≤ 38 字元；ja／ko／zh-CN 小標 ≤ 10 字、說明 ≤ 17 字、hero_label ≤ 15 字、title ≤ 25 字。**圖上的每個數字都必須出現在該語言的正文。**

## 4. 自檢（要印出 OK）

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug> --full
```

不帶 `--assets`（圖像是下一階段）。唯一允許留下的 FAIL 是「link text must be the title of <目標>」且原因是目標內容包還沒有該語言——其他 FAIL 都要修到過。

用 Write／Edit 工具寫檔（含非 ASCII 的檔案不要用 heredoc、`sed -i`、`perl -pi`）。不要用 `uv run`，不要跑 `pack_cli lint`、`pytest`。不要 git add／commit。除了內容包（只經由 merge_locale.py）與研究紀錄的 `translations` 鍵，不動任何 repo 檔案。任何網路請求都不得帶 email 或個人資料，User-Agent 一律 `Mokaair-editorial`（翻譯原則上不需要上網；要查某語言的官方機關名稱時才查）。

## 5. 回報（繁體中文，精簡）

1. 自檢最後輸出（原樣）。
2. 四個語言各自的 title。
3. 你拿不準的譯名（列出原文、你的譯法、依據）。
4. 你懷疑原稿有錯的地方（不要自己改）。
