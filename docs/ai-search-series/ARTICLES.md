# 搜尋最佳化名詞系列編輯清單

搜尋截止：2026-09-14。10 篇專文加一篇總索引，全部新增、全部 zh-TW、全部 `kind: life`。
規格在 [`brief.md`](brief.md)，逐篇指派在 [`catalogue.json`](catalogue.json)，
任務票是 `2026-09-14-ai-search-terms-series`。

**尚未發布。** 這份清單是編輯總表，不記錄「寫了沒」——
`apps/api/app/guides/content/<slug>.json` 存在就是寫了。

## 為什麼做這個系列

這組名詞的中文搜尋結果幾乎全是行銷公司的內容，彼此定義互相矛盾。本系列的價值不是再給一個定義，
而是把**各家定義的分歧點**講清楚，並分清楚哪些是官方文件說明的機制、哪些是業界慣例、
哪些只是廠商的行銷主張。

## 篇目

| # | slug | 標題 | 主軸 | 時效 |
| --- | --- | --- | --- | --- |
| 1 | `ai-search-seo` | SEO 是什麼：搜尋引擎最佳化在 AI 時代沒有改變的那一半 | 地基篇。 |  |
| 2 | `ai-search-geo` | GEO（生成引擎最佳化）是什麼：論文定義與行銷業用法的落差 | 出身與指標。 |  |
| 3 | `ai-search-aeo` | AEO（答案引擎最佳化）是什麼：生成式 AI 之前就存在的做法 | 它比 LLM 更早。 |  |
| 4 | `ai-search-aio` | AIO 是什麼：同一個縮寫的三種用法，以及怎麼分辨 | 這是命名碰撞，不是一門方法。 |  |
| 5 | `ai-search-llmo` | LLMO 是什麼：和 LLMOps 差在哪，哪些說法無法驗證 | 最投機的詞，加上一個真實的名稱衝突。 |  |
| 6 | `ai-search-eeat` | E-E-A-T 是什麼：品質評分指南裡的概念，不是可以設定的排名訊號 | 重點在「它不是什麼」。 |  |
| 7 | `ai-search-structured-data` | 結構化資料與 Schema.org：能換到什麼、換不到什麼 | 資格 vs 排名。 |  |
| 8 | `ai-search-llms-txt` | llms.txt 是什麼：一份提案，以及 robots.txt 真正能做的事 | 提案 vs 已部署的機制。 | 易變 |
| 9 | `ai-search-generated-answers` | AI 摘要與 AI 模式：生成式答案怎麼組出來，站長能控制什麼 | 講機制，不講操作（操作歸既有那兩篇）。 | 易變 |
| 10 | `ai-search-measuring-citations` | 怎麼量 AI 引用：測得到的、測不到的，與不能相信的分數 | 量測邊界。 | 易變 |
| 11 | `ai-search-terms-index` | GEO、AEO、AIO 與 SEO 名詞總索引：10 篇看懂差在哪 | 系列總索引兼旗艦比較表。 |  |

「易變」欄打勾的三篇要定期回查：llms.txt 的採用狀況、AI 模式的開放地區、
Search Console 生成式 AI 報表都還在變。life 內容包不走到期邏輯，`valid_until` 維持 null。

## 五個必須逐條點名的真實分歧

總索引的核心。不可以寫成好像有公認標準：

1. GEO 是 SEO 的上位、子集，還是改名？三種用法都在流通；提出這個詞的論文把它框成針對生成引擎評估的內容端技巧，不是取代 SEO。
2. GEO 與 AEO 是不是同一件事？有人混用；也有人主張 AEO 是擷取式答案、GEO 是生成式答案。兩種用法都現行。
3. AIO 指 Google 的 AI Overviews 功能、一門叫 AI Optimization 的服務，還是舊文案裡的 All-in-One？三個所指同時在用。
4. LLMO 的範圍只含檢索當下，還是也包含想辦法進入訓練資料？後者流傳很廣，而且從外部無法驗證。
5. llms.txt 到底有沒有作用？支持者說是新興標準；沒有主流引擎承諾消費它，部分還明講不讀。兩邊都可引用，照來源寫，不要越過來源去裁決。

## 不重複既有文章

站上已有三篇相鄰文章，它們負責「怎麼操作」，本系列講名詞與機制，互連但不重寫：

| 既有文章 | 它負責什麼 |
| --- | --- |
| `google-ai-overviews-for-site-owners` | 站長用 Search Console 看生成式 AI 成效的操作流程 |
| `google-ai-mode-search` | 讀者怎麼用 AI 模式追問與判讀來源 |
| `chatgpt-search-vs-google` | 讀者什麼時候該用 ChatGPT 搜尋、什麼時候用 Google |

`ai-search-generated-answers` 與 `ai-search-measuring-citations` 最容易漂過去，
這兩篇的第一段就要明寫「這篇不重複⋯⋯」並附上連結。

## slug 前綴為什麼是 `ai-search-`

這系列存在的目的就是拆解「哪個縮寫才是上位概念」這個爭議。用 `geo-` 或 `seo-term-` 當前綴，
等於在 11 個永久網址裡先替其中一方站隊。`ai-search-` 對爭議中立、不撞名，
形狀也和既有的 `ai-term-`、`claude-code-`、`gemini-cli-` 一致。

## 產製與發布

```bash
# 撰稿代理自驗（什麼都不會寫）
cd apps/api && uv run python -m app.guides.pack_cli ingest \
  --from ../../docs/ai-search-series/staging --slug <slug> --dry-run

# 協調者正式收件（渲染 hero.svg 成 hero.jpg 並寫進 repo）
cd apps/api && uv run python -m app.guides.pack_cli ingest \
  --from ../../docs/ai-search-series/staging --slug <slug>

# 全批 lint 並渲染 PNG 供目視。不要加 --catalogue，見任務票 Notes
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life \
  --slug ai-search-seo ... --render-dir ../../docs/ai-search-series/renders --warnings
```

發布時 **10 篇正文先上，總索引最後上**：`/life` 公開列表是 `published_at` 由新到舊排，
總索引靠最後發布落到列表最上方。
