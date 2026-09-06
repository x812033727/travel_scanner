---
id: 2026-09-06-intro-ai-vendor-settings
title: 後台可以挑選景點介紹的 AI 供應商與模型
status: in-progress
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T20:35:59Z
created_at: 2026-09-06T19:50:08Z
completed_at:
branch: claude/intro-vendor-settings
depends_on: []
scope:
  - apps/api/app/hotspots/intro_generation.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_admin_readiness.py
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/api/app/admin/service.py
  - apps/api/app/ai/catalog.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# 後台可以挑選景點介紹的 AI 供應商與模型

## Why

景點介紹的產生工作已經上線，設定也都在（`hotspot_intro_ai_*`），但**後台的「AI 供應商與金鑰」頁面沒有這張卡**。想把介紹改用 Gemini 寫、或指定一個比較便宜的模型，只能改環境變數重新部署。搜尋景點介紹已經有這張卡，兩者體驗不一致。

## Definition of done

- [x] `/admin/settings` 出現「AI 景點介紹撰寫」卡片，可選供應商與各家模型。
- [x] 設定存進 `provider_configs`，`load_runtime_settings` 讀得到。
- [x] 金鑰沿用「AI 供應商與金鑰」那張卡，不要再輸入一次。

## Steps

- [x] `admin/service.py`：`PROVIDER_DEFINITIONS["hotspot_intros"]`、`AI_FEATURE_PROVIDERS`、
      `CONNECTION_TESTED_PROVIDERS`、`_configured` 分支、`_validate_provider_values` 的選項、
      `_test_provider` 分支。
- [x] `ai/catalog.py`：四個 `hotspot_intro_ai_*_model` 加進 `MODEL_FIELDS` 與 `OPTIONAL_MODEL_FIELDS`。
- [x] `intro_generation.py`：`test_intro_provider()`——連線測試跑真的 schema、真的 prompt 常數、
      真的輸出守衛。
- [x] `admin-settings-panel.tsx`：`providerCategoryOf`、`fieldMeta`（新的 `inheritGuideSearch`
      空值選項）、`aiFeatureCards` 三處。
- [x] `messages/*/admin.json` ×5。
- [x] 測試：後端三個（欄位選項、驗證與拒絕、`_configured` 的兩層模型 fallback）、
      前端一個（空值選項寫「沿用景點 AI 搜尋的模型」、切供應商只留那一家的模型欄）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest   # 1169 passed
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web   # 559 passed
```

`/admin/settings` 把「AI 景點介紹撰寫」設成 Gemini、按連線測試，再到 `/admin/hotspots#intros`
產生一次，確認 run 的 `provider` 是 gemini。

## Notes

- **空值選項不是沿用行程規劃，是沿用景點 AI 搜尋。** `intro_model()` 先看自己的覆寫，沒有就退回
  `research_model()`，所以卡片的空值標籤必須說對是哪一層，否則管理員會以為自己選的是規劃器的模型。
  為此 `FieldMeta.emptyOption` 多了 `inheritGuideSearch`。
- 連線測試沒有只做「打得通」：它送真的 `IntroBatch` schema、真的 `INTRO_PROMPT`，回來的段落還會過一次
  `forbidden_claims()`。一家答得出來但守不住 schema、或無視營業時間禁令的供應商，會在這裡就失敗，
  而不是在第一個真的景點上。
- `CONNECTION_TESTED_PROVIDERS` 漏了會被 `test_admin_readiness.py` 擋下來——那個測試就是為了讓新卡片
  不能默默看起來像已驗證。
- 卡片標題來自後端 `ProviderDefinition`（中文），和其他卡片一致；那是 admin 全站 i18n 的另一件事。
