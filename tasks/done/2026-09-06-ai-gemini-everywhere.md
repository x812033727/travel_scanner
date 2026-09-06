---
id: 2026-09-06-ai-gemini-everywhere
title: AI 行程規劃、行程文字解析與景點 AI 搜尋也能選 Gemini
status: done
priority: P2
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T07:54:31Z
created_at: 2026-09-06T07:54:30Z
completed_at: 2026-09-06T08:23:57Z
branch: claude/ai-gemini-everywhere
depends_on: []
scope:
  - apps/api/app/ai/itinerary.py
  - apps/api/app/ai/trip_parser.py
  - apps/api/app/ai/gemini.py
  - apps/api/app/ai/structured_output.py
  - apps/api/app/ai/catalog.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_ai_itinerary.py
  - apps/api/tests/test_ai_trip_parser_llm.py
  - apps/api/tests/test_hotspot_ai_search.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_structured_output.py
  - apps/api/tests/test_ai_catalog.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/admin-hotspot-guides-panel.tsx
  - apps/web/components/admin-hotspot-guides-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/hotspotAdmin.json
  - apps/web/messages/ja/hotspotAdmin.json
  - apps/web/messages/ko/hotspotAdmin.json
  - apps/web/messages/zh-CN/hotspotAdmin.json
  - apps/web/messages/zh-TW/hotspotAdmin.json
  - .env.example
---

# AI 行程規劃、行程文字解析與景點 AI 搜尋也能選 Gemini

## Why

「AI 供應商與金鑰」卡片已經收了 Gemini 的金鑰與 Base URL，但只有「Gemini 多語文章搜尋」
用得到它。「AI 行程規劃」的來源只能選 OpenAI／Claude／MiniMax（`ai_planner_mode`、
`ai_planner_priority`），行程文字解析沿用同一份名單，「AI 景點介紹搜尋」的預設供應商
（`hotspot_guide_ai_default_provider`）也沒有 Gemini。後台明明設好了金鑰，三個功能卻選不到。

## Definition of done

- [x] 後台「AI 行程規劃」的來源與自動備援順序可以選 `gemini`，並有自己的「Gemini 模型」欄位。
- [x] 行程文字解析（`trip_parser_providers`）對 Gemini 規劃供應商有對應的解析 adapter。
- [x] 「AI 景點介紹搜尋」的預設供應商可以選 Gemini，並可另設模型（留空沿用規劃模型）。
- [x] 三者共用「AI 供應商與金鑰」卡片上既有的 Gemini 金鑰與 Base URL，不新增金鑰欄位。
- [x] 後台的測試連線對 `ai_planner`（mode=gemini）與 `ai_guide_search`（default=gemini）走 Gemini。

## Steps

- [x] `structured_output.gemini_response_schema`：把 pydantic JSON Schema 轉成 Gemini 接受的子集
      （展開 `$ref`／`$defs`、`anyOf` null → `nullable`、丟掉 title／default／pattern／maxItems…）。
- [x] `GeminiPlannerProvider`（itinerary）、`GeminiTripParserProvider`（trip_parser）、
      `GeminiResearchProvider`（hotspots.ai_search），全部包 `GeminiStructuredProvider`。
- [x] config：`gemini_model`、`hotspot_guide_ai_gemini_model`，`hotspot_guide_ai_default_provider`
      Literal 加 gemini，`ai_planner_priority` 預設加 gemini。
- [x] catalog `MODEL_FIELDS`／`OPTIONAL_MODEL_FIELDS`，admin 卡片欄位、`_configured`、驗證允許值。
- [x] 後台面板：`AiVendor` 加 gemini、兩張卡片的模型欄位、選單選項；admin.json 五語系欄位文案；
      景點介紹面板供應商清單與 hotspotAdmin.json 標籤。
- [x] 測試：schema 轉換、三個 adapter 的 MockTransport、名單／覆寫、admin 狀態與驗證、面板 vitest。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_structured_output.py tests/test_ai_itinerary.py tests/test_ai_trip_parser_llm.py tests/test_hotspot_ai_search.py tests/test_admin_provider_settings.py tests/test_ai_catalog.py
```

```bash
npm run lint:web && npm run typecheck:web && npm run check:i18n && npx vitest run components/admin-settings-panel.test.tsx components/admin-hotspot-guides-panel.test.tsx --root apps/web
```

部署後到 /admin/settings →「AI 服務」：AI 行程規劃來源選 Gemini → 測試連線應回
`gemini / gemini-3.8-flash 結構化行程驗證成功`；AI 景點介紹搜尋預設供應商選 Gemini → 測試連線。

## Notes

- Gemini 的 `responseSchema` 是 OpenAPI 子集：不吃 `$ref`、`additionalProperties`、`pattern`、
  `maxItems`（`candidate_generation.py` 已有註記）。轉換器只留 type／description／enum／
  properties／required／items／nullable／propertyOrdering，其他交給 pydantic 事後驗證。
- Gemini 沒有獨立的金鑰欄位：沿用 `hotspot_guide_gemini_api_key`／`hotspot_guide_gemini_base_url`
  （都在 `ai_vendors` 卡片）。規劃與解析的模型是新的 `gemini_model`，與文章搜尋用的
  `hotspot_guide_gemini_model` 分開，因為文章搜尋需要 grounding 能力的模型。
- `test_integration_postgres_redis.py:834` 的 provider 集合沒加 gemini（不在 scope；CI 沒有
  Gemini 金鑰，永遠是 catalog）。
