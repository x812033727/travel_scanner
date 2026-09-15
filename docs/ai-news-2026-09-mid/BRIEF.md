# 撰稿規格：2026 年 9 月中 AI 新聞（第三批，7 篇）

給研究／撰稿、查核與翻譯代理的共同規則。前兩批見 `docs/ai-news-2026-09`、`docs/ai-news-2026-ytd`，
格式範本是 `apps/api/app/guides/content/ai-news-chatgpt-work-20260709.json`。

## 篇目

| 事件日 | slug | 讀者角度 | 相關新聞連結（第二個 link） |
|---|---|---|---|
| 2026-07-08 | `ai-news-gpt-live-voice-20260708` | ChatGPT 語音能邊聽邊說、可插話；各方案用哪個模型；API 價格只帶過 | `ai-news-gemini-live-20260826`（Gemini Live 生產力更新：用語音處理郵件與待辦） |
| 2026-09-04 | `ai-news-google-assistant-gemini-20260904` | Android 手機、平板、Wear OS、耳機、Android Auto 的 Assistant 由 Gemini 取代；哪些裝置暫留；換手前要檢查的習慣與設定 | `ai-news-gemini-spark-20260519`（Gemini Spark 與 Daily Brief：AI 從晨間摘要走向背景辦事） |
| 2026-09-10 | `ai-news-anthropic-threat-report-20260910` | 七類濫用與代理化攻擊鏈；一般人防詐、帳號與 API 金鑰保護 | `ai-news-project-glasswing-20260407`（Project Glasswing 與 Mythos Preview：AI 找到漏洞後，真正的工作才開始） |
| 2026-09-10 | `ai-news-openai-agents-api-20260910` | Codex harness 成為公開 beta API：它是什麼、計費、資料位置與 ZDR 限制；對「會用 AI 工具的非工程師」意味著什麼 | `ai-news-gpt-6-astra-20260903`（GPT-6 Astra 發布：從回答問題到完成電腦工作） |
| 2026-09-10 | `ai-news-deepseek-v41-flash-20260910` | V4.1-Flash 上線、舊模型改導向、V4-Pro 去留公告的先後；模型汰換對使用 DeepSeek 服務或串接工具的人有何影響 | `ai-news-qwen-35-20260216`（Qwen3.5 開放權重：可下載模型，與能在自己電腦運作差在哪？） |
| 2026-09-12 | `ai-news-pace-the-frontier-20260912` | Amodei〈We Must Pace the Frontier〉的主張與不主張；誰公開表態支持、用什麼方式；對一般使用者的意義（不是產品新聞） | `ai-news-claude-fable-51-20260901`（Claude Fable 5.1 與 Mythos 5.1：功能、開放對象與限制） |
| 2026-09-14 | `ai-news-siri-ai-ios-27-20260914` | 9/9 發表會、9/14 iOS 27 與 Siri AI 推出；語言、地區、機型條件；台灣與繁體中文使用者現在能用什麼 | `ai-news-gemini-personal-intelligence-20260114`（Gemini Personal Intelligence：AI 連結郵件與相簿後，便利從哪裡來？） |

第一個 link 一律是索引：
`{"type":"link","text":"2026 年 AI 新聞總整理：1 月 1 日至 9 月 14 日的重點與生活應用","url":"https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index"}`，
第二個 link 是上表的相關新聞（text 用括號內的標題，url `https://mokaair.com/zh-TW/life/<slug>`）。

## 查證規則（最重要）

- **只用一手來源**：廠商官網公告、官方部落格、說明中心／支援頁、API 文件、當事人本人發表的原文。
  新聞媒體可以拿來找線索與交叉確認日期，但文章的 `sources` 只放一手來源（至少 2 條、最多 4 條）。
  aiweekly、llm-stats、releasebot、各種「AI 新聞整理」部落格一律不當來源，它們寫的數字要回官方頁核對，找不到就不寫。
- 查核日 `checked_on` 一律 `2026-09-15`。
- 每一個日期、價格、百分比、方案名、地區、語言、機型，都要能指到一條 source 的原文。查不到的寫「官方未說明」或不寫。
- 廠商宣稱的能力、評測數字一律寫成「OpenAI 表示／Apple 說明」，不寫成事實；本站沒有實測，不可寫「我們試用」。
- 分批開放、beta、預覽、地區限制、方案限制分開寫，不把美國首發推定成台灣帳號都能用。
- 生活情境要標明是編輯設計的例子。
- 網路請求：**不得在任何請求（包含 User-Agent、查詢字串、表單）放入使用者的 email 或任何個人資料**。
  需要自訂 User-Agent 時一律用 `Mokaair-editorial`。WebFetch 被 403／451 擋時，換同一官方站的其他頁、官方 RSS、或 Google 快取以外的官方鏡像（如 `apple.com/<國家>/newsroom`），不要改用整合站。

## 內容包格式（zh-TW）

檔案 `apps/api/app/guides/content/<slug>.json`：

```json
{"slug":"<slug>","kind":"life","destination_id":null,"topics":["ai","software"],"valid_until":null,
 "featured":false,"display_order":<見下>,
 "locales":{"zh-TW":{"title":"…","description":"…",
   "hero":{"src":"/guides/<slug>/hero.jpg","alt":"…的原創插圖","width":1600,"height":900,
           "credit":{"author":"Mokaair","license":"© Mokaair","source_url":null}},
   "blocks":[…],
   "sources":[{"title":"廠商：頁面名稱","url":"https://…","checked_on":"2026-09-15"}]}}}
```

display_order：gpt-live 142、google-assistant 143、threat-report 144、agents-api 145、deepseek 146、pace-the-frontier 147、siri 148。
topics 只能從 `ai daily finance gadgets misc productivity software tutorial` 選，第一個是 `ai`（Siri／Assistant 可用 `["ai","gadgets"]`）。

blocks 依序：
1. paragraph：事件是什麼（第一句寫出事件日期，例如「2026 年 9 月 10 日」）。
2. paragraph：寫「本文於 2026 年 9 月 15 日查核」，並說明開放狀態／本文不做實測的界線。
3. 五個 `{"type":"heading","level":2,"text":"…"}` 小節，每節 2–4 個 paragraph。
4. 第 2 節結尾放一個 table：`{"type":"table","header":[3–4 欄],"rows":[3–6 列，每列欄數與 header 相同],"caption":"2026 年 9 月 15 日查核；…"}`。**最多 4 欄**，儲存格短（手機會擠）。
5. 第 3 節結尾放 diagram：`{"type":"image","src":"/guides/<slug>/diagram-1.svg","alt":"…","width":1600,"height":900,"caption":"…","credit":{"author":"Mokaair","license":"© Mokaair","source_url":null}}`。
6. 第 5 節後放 callout：`{"type":"callout","tone":"info","title":"…","text":"…"}`。
7. 兩個 link（見上）。

篇幅：**所有 paragraph 的 text 串起來（含標點）1,800–3,000 字**；title ≤ 60 字、description 120–200 字。
用台灣繁體中文與台灣用語（「使用者」「帳號」「影片」「軟體」），不可出現簡體字。不要列表、不要 Markdown、不要 emoji。
文字語氣照前兩批：平實、具體、不聳動、不下投資或醫療建議。和既有 31 篇不重寫同一件事（例如 GPT-Live 篇不要重講 ChatGPT Work）。

## 研究紀錄

檔案 `docs/ai-news-2026-09-mid/research/<slug>.json`：

```json
{"slug":"…","event_date":"YYYY-MM-DD","title":"（同 zh-TW title）",
 "sources":[同內容包 sources],"checked_on":"2026-09-15",
 "verified_facts":["每條一個可查的事實，句尾括號寫出處 URL"],
 "unverified_or_excluded":["看到但查不到一手來源、因此沒寫進文章的說法，以及原因"],
 "editorial_brief":"原創情境與這篇刻意不談的範圍",
 "hero_label":"主圖下方標語，繁中 ≤ 12 字",
 "diagram":{"title":"圖解標題 ≤ 20 字","caption":"（同內容包 diagram caption）",
            "nodes":[["小標 ≤ 8 字","說明 ≤ 14 字"],[…],[…],[…]]}}
```

圖解是 2×2 四格卡片（左上→右上→左下→右下），`nodes` 剛好 4 組。**圖上任何數字都必須出現在文章正文。**

## 自檢

```bash
cd apps/api
PYTHONIOENCODING=utf-8 /c/Users/x8120/mokaair/apps/api/.venv/Scripts/python.exe ../../docs/ai-news-2026-09-mid/check_article.py <slug>
```

輸出 `OK` 才算完成；有 `FAIL` 就修到過。只寫自己那篇的兩個檔案，不要動其他檔案、不要 git commit。

## 翻譯（第二階段才做）

把 en、ja、ko、zh-CN 四個 locale 加進同一個內容包，順序 `zh-TW, en, ja, ko, zh-CN`：
- blocks 型別與順序、table 的欄列數、sources（title 可譯，url 與 checked_on 不變）完全對應。
- hero.src → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`，diagram src → `diagram-1-<…>.svg`，alt／caption 翻譯。
- 兩個 link 的 url 換成 `https://mokaair.com/<locale>/life/<slug>`，text 用目標內容包該 locale 的正式 title。
- 日期寫法照目標語言習慣，但年月日數字不變；價格幣別不變。
- 研究紀錄加 `translations.<locale>.{hero_label, diagram{title,caption,nodes}}`。
- 自檢加 `--full`。
