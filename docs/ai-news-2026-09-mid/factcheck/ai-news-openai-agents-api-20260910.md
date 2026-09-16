# 查核紀錄：ai-news-openai-agents-api-20260910

- 查核日：2026-09-15
- 對象：`apps/api/app/guides/content/ai-news-openai-agents-api-20260910.json`（zh-TW）與研究紀錄
- 取頁方式：curl，User-Agent `Mokaair-editorial`，未帶任何個人資料
- 讀過的一手頁面：
  - https://openai.com/index/introducing-the-agents-api/ （撰稿時 WebFetch 403，curl 可讀全文）
  - https://developers.openai.com/api/docs/changelog （September, 2026 / Sep 10 條目）
  - https://developers.openai.com/api/docs/guides/agents-api/overview
  - https://developers.openai.com/api/docs/guides/agents-api/observability
  - https://developers.openai.com/api/docs/guides/your-data
  - 輔助：agents-api/quickstart、sessions、architecture、multi-agent；https://openai.com/news/rss.xml
- 自檢：`check_article.py` 輸出 OK（paragraph 2,989 字，description 181 字）

## 結果總覽

共檢查 56 條主張（title 1、description 4、開頭兩段 10、第 1 節 9、第 2 節 9、表格 6、第 3 節 10、圖解 1、第 4 節 5、第 5 節 5、callout 5，部分重疊合併計）。

| 分類 | 條數 |
|---|---|
| 正確 | 43 |
| 需要改寫 | 12 |
| 錯誤 | 1 |
| 查無出處 | 0（原本「規格仍在發展中」無出處，已改成引用公告的說法，計入需要改寫） |

## 改動明細

1. description（需要改寫，過度肯定）
   - 原：資料只在美國且不支援零資料保留的意思
   - 改：資料落地只支援美國且不支援零資料保留的意思
   - 依據：overview「currently supports data residency only in the United States」。這句說的是「資料落地控制只能選美國」，不是「資料只存在美國」；your-data 頁另寫 system data 可能在所選地區外處理、MCP 等第三方不適用資料落地。https://developers.openai.com/api/docs/guides/agents-api/overview 、https://developers.openai.com/api/docs/guides/your-data

2. 第 1 段（需要改寫，來源升級＋過度詮釋）
   - 原：OpenAI 在 API 更新紀錄中宣布以公開 beta 推出……上下文壓縮與中斷後的復原由 OpenAI 處理
   - 改：OpenAI 發表〈Introducing the Agents API〉，以公開 beta 推出……上下文壓縮與復原（recovery）由 OpenAI 處理
   - 依據：公告日期 September 10, 2026；overview 只寫「recovery」，沒有限定是「中斷後」。https://openai.com/index/introducing-the-agents-api/ 、https://developers.openai.com/api/docs/guides/agents-api/overview

3. 第 2 段（需要改寫，原為無出處的通論）
   - 原：依據 OpenAI 的 API 更新紀錄……公開 beta 代表開發者現在就能使用，但規格仍在發展中
   - 改：依據 OpenAI 的發布公告……OpenAI 表示公開 beta 即日起開放開發者使用，期間會依回饋快速調整、朝正式版推進
   - 依據：公告「available in public beta today to all developers」「During the public beta, we'll iterate quickly based on your feedback as we work toward general availability」。https://openai.com/index/introducing-the-agents-api/

4. 第 1 節第 2 段（需要改寫，小幅偏離原文）
   - 原：工作階段是一個持續存在的代理實例，可以接續處理任務
   - 改：工作階段是一個持續存在的代理實例，負責處理任務並回應新的輸入
   - 依據：「Session: A durable instance of an agent that works on tasks and responds to input.」https://developers.openai.com/api/docs/guides/agents-api/overview

5. 第 1 節第 3 段（錯誤：數目不符）
   - 原：執行環境有兩種來源。更新紀錄寫到，代理可以跑在 OpenAI 代管的沙箱，也可以接上開發者自己的基礎設施或官方支援的沙箱供應商。……也影響誰要負責開關機器
   - 改：執行環境可以自己選。OpenAI 在公告中寫到，代理的運算環境可以是 OpenAI 代管的沙箱、開發者自己的基礎設施，或官方合作的沙箱供應商；選代管沙箱時，由 OpenAI 建置與管理沙箱。……也影響機器由誰負責管理
   - 依據：公告「in an OpenAI-managed sandbox, on your own infrastructure, or with one of our sandbox partners」「OpenAI provisions and manages the sandbox」，原文列三種，「兩種來源」與後句自相矛盾；「開關機器」原文沒有。https://openai.com/index/introducing-the-agents-api/

6. 第 2 節第 1 段（需要改寫，可明確歸因）
   - 原：文件沒有另列一筆 Agents API 本身的費用項目，但這不代表一件自動化工作的總價容易估。
   - 改：OpenAI 在公告中也表示，使用 Agents API 本身沒有額外費用，但沒有平台費不代表一件自動化工作的總價容易估。
   - 依據：公告「There are no additional fees for using the Agents API – you simply pay for the tokens and tools your agents use」。研究紀錄原本把這句列為查無一手來源，已更正。https://openai.com/index/introducing-the-agents-api/

7. 表格最後一列（需要改寫，計價依據不準）
   - 原：["重試與第三方", "各自計費", "重試也要算進去"]
   - 改：["重試", "照模型與工具計費", "失敗重做也算"] 與 ["第三方服務", "依服務商收費", "要另外加總"]（5 列 → 6 列，仍在上限內）
   - 依據：重試不是獨立計費項目，而是再次的模型／工具呼叫；官方原文「Account for root-agent and subagent work, including retries, plus any applicable tool, sandbox compute, and third-party service charges」。https://developers.openai.com/api/docs/guides/agents-api/observability

8. 第 3 節第 2 段（需要改寫，漏掉例外）
   - 原：預設最多保存 30 天。
   - 改：預設最多保存 30 天（法律要求或為防止危害而需要時例外）。
   - 依據：「retained for up to 30 days, unless longer retention is required by law, or is reasonably necessary to protect our services or any third party from harm」。https://developers.openai.com/api/docs/guides/your-data

9. 第 3 節第 3 段（需要改寫，把 ZDR 的說明延伸到資料落地）
   - 原：這個 API 目前就不符合條件，換成自架沙箱也改變不了。
   - 改：這個 API 目前就不符合條件；至少在 ZDR 這一點，官方已明說換成自架沙箱也改變不了。
   - 依據：overview 只說「Choosing a self-hosted sandbox does not make the Agents API ZDR-eligible」，沒有說自架沙箱與資料落地的關係。https://developers.openai.com/api/docs/guides/agents-api/overview

10. 圖解 alt 與 caption（需要改寫，同第 1 條＋漏「預設」）
    - 原 alt：只在美國、不支援 ZDR……；原 caption：資料落地只在美國、不支援 ZDR、濫用監控紀錄最多 30 天……
    - 改 alt：落地只支援美國、不支援 ZDR……；改 caption：資料落地目前只支援美國、不支援 ZDR、濫用監控紀錄預設最多 30 天……
    - 研究紀錄 diagram 同步：caption 一致；第一格 ["只在美國", "資料落地目前僅支援美國"] → ["落地只支援美國", "不能選其他地區"]
    - 依據：同第 1、8 條。

11. 第 4 節第 1 段（需要改寫，工具不全是開發方自備）
    - 原：Agents API 的工具由開發的一方提供
    - 改：Agents API 的工具由開發的一方提供或選用
    - 依據：overview「your application provides tools」，但公告也寫「supports MCP, custom functions, and built-in tools like web search」，計價段落另有 OpenAI tools。https://openai.com/index/introducing-the-agents-api/

12. 第 5 節第 2 段（需要改寫，補歸因）
    - 原：公開 beta 也意味著細節還會變。官方文件自己就提醒，
    - 改：公開 beta 也意味著細節還會變，OpenAI 自己就說 beta 期間會依回饋快速調整。官方文件也提醒，
    - 依據：同第 3 條。

13. 第 5 節第 3 段、callout（需要改寫，同第 1 條）
    - 原：資料只在美國、不支援零資料保留／目前資料只在美國，且不支援零資料保留
    - 改：資料落地目前只支援美國、不支援零資料保留／資料落地目前只支援美國，且不支援零資料保留
    - 依據：同第 1 條。

14. sources 與研究紀錄
    - sources 第 1 條：API Changelog → OpenAI〈Introducing the Agents API〉（公告同時支撐日期、公開 beta、開放對象、無額外費用、三種運算環境，Changelog 能證的它都能證；sources 上限 4 條）。
    - 研究紀錄 verified_facts：Changelog 兩條與 RSS 一條合併為「交叉確認（未列 sources）」；新增公告四條；Session 定義與 30 天例外補上原文。
    - unverified_or_excluded：刪除「沒有額外平台費查無一手來源」「官方部落格讀不到」兩條，改記更正經過、刻意不寫的客戶引言數字、開放對象未說明地區。

## 確認正確、未改的重點

- 2026-09-10 公開 beta（公告、Changelog、RSS 三處一致）。
- 四個核心概念、沙箱能力（執行程式、編輯檔案、MCP、成果檔、子代理）、計價三類。
- 用量說明：多次模型呼叫、快取規則、輸入組成、推理 token 算輸出、長歷史重複處理、子代理計費、usage 為 best-effort／可能 null／不是帳單、Trace retrieval 不在 public beta API。
- 資料控制表 /v1/agents：訓練 No、濫用監控 30 days、Application state Until deleted、ZDR eligible No；ZDR 需 OpenAI 事先核准；MCP 為第三方、適用對方資料落地政策。
- 官方完整範例：Incident response agent（request approval for recovery actions）、Data analyst（read-only SQL）。
- 平台後台 platform.openai.com/logs?api=agents 的 Agents 分頁可看 turns、tool calls、subagents。

## 讀者角度

- 沒有暗示本站實測；第 2 段明寫不串接測試，委託情境標為編輯設計的例子。
- 建議（先唯讀、改動資料保留人工確認、先用在出錯可修正且不含客戶機密的內部工作）屬一般審慎做法，不是投資或法律建議。
- 與 `ai-news-gpt-6-astra-20260903` 有輕度重疊：兩篇都談「需要確認的動作」與「從出錯後能修正的任務開始」。本篇重心在計費、資料落地、ZDR 與委託外包的提問，第 5 節也明確區分模型（Astra）與框架（Agents API），判斷不構成重寫同一件事，未刪。

## 仍不確定的點

- 「開放所有開發者」是否含地區或帳號層級限制：公告與 quickstart 都沒寫（quickstart 只要求 API 金鑰具 api.agents.read／write 與 api.responses.write）。文章寫成「OpenAI 表示」，未推定台灣帳號一定可用。
- 不用資料落地控制時，Agents API 的資料實際存放在哪個地區：官方未說明。文章只寫「資料落地目前只支援美國」，不寫「資料只存在美國」。
- 刪除工作階段後，已產生的濫用監控紀錄是否同步刪除：表格把 Application state（Until deleted）與濫用監控（30 days）分列，但未明說刪除的連動；文章沒有宣稱刪除會清掉監控紀錄。
- recovery 的具體範圍（例如串流中斷、環境失敗）overview 未定義；sessions 頁只談斷線後重新取回 session 與 items。文章已改為不加限定的「復原」。
- 容器價格計時方式（20 分鐘 session 價 vs 按分鐘、5 分鐘最低）定價頁兩處說法不一，文章維持不寫金額。
- 正文 2,989 字，距上限 3,000 只剩 11 字，翻譯或後續修改若要加字需同時刪減。
