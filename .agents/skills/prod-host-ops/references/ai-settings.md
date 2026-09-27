# AI 設定：卡片、優先順序、驗證、診斷

## 設定在哪裡

AI 相關的卡片不在 `/admin/settings`，在 **`/admin/ai-accounts` 的「API」分頁**：`/zh-TW/admin/ai-accounts?tab=api&provider=<卡片 id>`（加 `&field=<欄位>` 會捲到那一欄）。同頁的「訂閱帳號」分頁只有站主看得到，見 `ai-accounts.md`。卡片定義在 `apps/api/app/admin/service.py` 的 `PROVIDER_DEFINITIONS`，web 端的清單是 `apps/web/lib/admin-settings-ownership.ts` 的 `AI_SETTINGS_PROVIDERS`。

| 卡片 id | 標題 | 放什麼 |
| --- | --- | --- |
| `ai_vendors` | AI 供應商與金鑰 | OpenAI、Claude、MiniMax、Gemini、Jev 的金鑰與 Base URL；`jev_daily_call_budget`；`anthropic_connection`（Claude 連線方式：`api_key`／`subscription`）與 `ai_subscription_max_usage_percent`（預設 80）。後兩欄只有站主能改。這張卡永遠啟用（`ALWAYS_ENABLED_PROVIDERS`），所以秘密不會因停用被清空；web 只送有變的欄位 |
| `ai_planner` | AI 行程規劃 | `ai_planner_mode`（`auto`／`openai`／`anthropic`／`minimax`／`gemini`／`fallback`／`disabled`）、`ai_planner_priority`（程式預設 `openai,anthropic,minimax,gemini`）、各家模型 `openai_model`／`anthropic_model`／`minimax_model`／`gemini_model`、逾時、輸出上限、使用者與 IP 預算。行程文字解析共用這份名單 |
| `ai_guide_search` | AI 景點介紹搜尋 | `hotspot_guide_ai_default_provider`，各家模型覆寫 `hotspot_guide_ai_{openai,anthropic,minimax,gemini}_model`；留空＝沿用行程規劃那家的模型（`app/hotspots/ai_search.py` 的 `research_model`） |
| `hotspot_intros` | AI 景點介紹撰寫 | `hotspot_intro_ai_default_provider` 與各家模型；留空＝沿用景點介紹搜尋的模型 |
| `gemini_guides` | Gemini 多語文章搜尋 | `hotspot_guide_gemini_model`、逾時、每日搜尋預算、`catalog_review_max_calls`、啟用開關；候選產生 CLI 也用這個模型 |

- **Gemini 沒有自己的金鑰欄**：行程規劃、介紹搜尋與 Gemini 文章搜尋都讀 `ai_vendors` 的 `hotspot_guide_gemini_api_key`／`hotspot_guide_gemini_base_url`。
- **優先順序**：`provider_configs` 的列 > 程式預設；而且只讀回列所屬定義上列出的欄位。欄位搬家要 migration（金鑰從各功能卡搬到 `ai_vendors` 的是 `0047_ai_vendor_settings`）；舊列還帶著搬走的欄位時，快照會附上「請執行資料庫 migration 0047」。
- **模型下拉**的選項來自 `apps/api/app/ai/catalog.py`（快照的 `field_options`）；「自訂…」接受 `[A-Za-z0-9._:-]{1,128}` 的任何 id（`MODEL_ID_PATTERN`）。加一個模型＝在 catalog 加一筆 `ModelEntry`，`apps/api/tests/test_ai_catalog.py` 釘住預設值必須在目錄裡。
- **Claude 連線方式選「訂閱帳號」**：介紹搜尋、介紹撰寫、介紹審查、簡體名稱與新聞各階段的 Claude 呼叫改走主機 AI 帳號代理（`apps/api/app/ai/subscription.py`），不用金鑰；所有帳號都到用量上限時改用 MiniMax。**行程規劃與行程文字解析不走訂閱**，永遠只用 API 金鑰（讀者等不了 CLI）。

## 改設定

平常用後台表單改：點欄位、`ctrl+a`、打字、按「儲存設定」，成功的狀態文字是「<卡片> 設定已加密儲存並立即套用。」。自動化驅動表單的做法與坑在 `admin-browser.md`。API 是 `PUT /api/travel/admin/provider-settings/<卡片 id>`，body `{"config": {...}, "secrets": {...}}`；未知欄位回 422 `provider_setting_unknown`，列舉欄位不在允許值內也會 422。從頁面 JavaScript 打這個 PUT 在 auto 模式會被分類器擋，用表單或請站主按。

## 逐張驗證

改完（或部署後）每張卡按「測試連線」（`POST /api/travel/admin/provider-settings/<id>/test`）：

| 卡片 | 測試做什麼 | 正常 |
| --- | --- | --- |
| `ai_vendors` | 每家列一次模型（MiniMax 國際版的 `/v1/models` 存在） | 每家 200 |
| `ai_planner` | 用東京真實的候選景點排一次行程（候選來自資料庫，壞掉的種子資料也會在這裡現形） | 成功，約 20–30 秒 |
| `ai_guide_search` | 一次多語搜尋規劃的結構化輸出 | 「<供應商> / <模型> AI 景點搜尋結構化輸出驗證成功」，約 15 秒 |
| `hotspot_intros` | 一次介紹撰寫的結構化輸出 | 「<供應商> / <模型> AI 景點介紹結構化輸出驗證成功」 |
| `gemini_guides` | 一次有 Google 搜尋接地的查詢 | 成功，約 10 秒 |

`gemini_guides` 的測試連線走有接地的路徑。只想確認某個 Gemini 模型 id 能用正式站的金鑰、又不想動設定：在 api 容器裡 `python -m app.cli generate-hotspot-candidates --city TPE --count 3 --dry-run --model <id>`（一次 API 呼叫、只印出結果、什麼都不寫；這是不接地的路徑）。

資料庫層面的核對用唯讀 psql，一個呼叫一句簡單的 select（skill `deploy` 的 post-deploy 有格式）；秘密欄位只看「有沒有」，不要 select 出值。

## 在主機上診斷行程規劃

1. **先讀 log**：`docker compose -f docker-compose.prod.yml logs --since 2h api | grep 'ai planner provider'`。每次供應商失敗都記一行 `ai planner provider <名> failed: <原因>`，含狀態碼與回應摘錄。
2. **看有效設定，不看環境變數**：容器的 `printenv` 會說沒有金鑰，因為金鑰在資料庫。要看有效值就在 api 容器裡跑 `load_runtime_settings`，只印非秘密欄位與 `bool(金鑰)`：

   ```python
   import asyncio
   from app.admin.service import load_runtime_settings
   from app.db import SessionFactory, engine

   async def main():
       async with SessionFactory() as session:
           s = await load_runtime_settings(session)
       print(s.ai_planner_enabled, s.ai_planner_mode, s.ai_planner_priority, s.minimax_model,
             s.minimax_api_base_url, bool(s.minimax_api_key), bool(s.hotspot_guide_gemini_api_key),
             s.ai_planner_timeout_seconds, s.ai_planner_total_timeout_seconds,
             s.ai_planner_max_output_tokens)
       await engine.dispose()

   asyncio.run(main())
   ```

   送法：本機 base64 後用 `docker compose -f docker-compose.prod.yml exec -T api python -` 經 SSH 餵進去。**auto 模式的分類器會擋任何灌進容器的腳本**（base64 或 stdin 都算）：切 Manual 或把指令交給站主跑。要重現一次呼叫就用 app 自己的 `_providers()`（`apps/api/app/ai/itinerary.py`）建 provider，讓金鑰留在 app 裡，只印狀態碼與摘錄。
3. **名單是空的**：`ai_planner_enabled` 關、mode 是 `fallback`／`disabled`、指定的那家沒有金鑰，或 `auto` 的優先順序裡沒有一家有金鑰，`_providers()` 都回空名單，規劃器直接走內建備援。

## MiniMax 的坑

- **國際版與中國版的金鑰不通用**。程式預設的 `minimax_api_base_url` 是中國版 `https://api.minimaxi.com/v1`；國際平台的金鑰要配 `https://api.minimax.io/v1`，配錯回 `401 invalid api key (2049)`。改 `ai_vendors` 卡的 MiniMax Base URL。
- **推理模型不支援 json_schema 結構化輸出**（MiniMax-M3 會忽略 `text.format`，把 JSON 包在 code fence 或改形狀）。程式把 schema 寫進 prompt、剝 fence、寬鬆解析再由 `normalize_draft` 修；輸出偏差是機率性的，看到偶發的驗證失敗先看 log 的回應摘錄。
- **推理 token 算在輸出上限裡**：輸出上限 12000 會把 M3 餓死，正式站可用的組合是單家逾時 45 秒、總逾時 50 秒、輸出上限 24000。
- **BFF 也有逾時**：web 的 `API_PROXY_TIMEOUT_MS` 預設 15000；規劃要 25–30 秒，正式站 `.env` 要 60000，否則 API 還在算、瀏覽器已經拿到逾時。改 `.env` 要站主同意，而且要重建 web 容器才生效。
- 單一供應商模式沒有備援；要韌性就用 `auto` 加第二把金鑰。
