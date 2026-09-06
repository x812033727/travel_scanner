---
id: 2026-09-06-intro-ai-vendor-settings
title: 後台可以挑選景點介紹的 AI 供應商與模型
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T19:50:08Z
completed_at:
branch:
depends_on: []
scope:
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

景點介紹的產生工作已經上線，設定也都在（`hotspot_intro_ai_*`：啟用開關、預設供應商、四家的模型覆寫、逾時、token 上限、每日執行與呼叫額度），但**後台的「AI 供應商與金鑰」頁面沒有這張卡**。

實務後果：想把介紹改用 Gemini 寫、或指定一個比較便宜的模型，只能改環境變數重新部署。搜尋景點介紹（`ai_guide_search`）已經有這張卡，兩者體驗不一致。

## Definition of done

- [ ] `/admin/settings` 出現「AI 景點介紹撰寫」卡片，可選供應商與各家模型。
- [ ] 設定存進 `provider_configs`，`load_runtime_settings` 讀得到（也就是產生工作會照著跑）。
- [ ] 金鑰沿用「AI 供應商與金鑰」那張卡，不要再輸入一次。

## Steps

- [ ] `apps/api/app/admin/service.py`：`PROVIDER_DEFINITIONS["hotspot_intros"]`（放在 `ai_guide_search` 之後）、加進 `AI_FEATURE_PROVIDERS`、`_configured` 分支（選中的供應商有金鑰就 ready）、`_validate_provider_values` 的 `hotspot_intro_ai_default_provider` 選項、`_test_provider` 分支。
- [ ] `apps/api/app/ai/catalog.py`：四個 `hotspot_intro_ai_*_model` 加進 `MODEL_FIELDS` 與 `OPTIONAL_MODEL_FIELDS`（能力與 guide search 那四個相同）。
- [ ] `apps/web/components/admin-settings-panel.tsx`：`providerCategoryOf`、`fieldMeta`、`aiFeatureCards` 三處。
- [ ] `apps/web/messages/*/admin.json` ×5：`providerFields.hotspot_intro_ai_*` 的標籤與說明。
- [ ] 測試：`test_admin_provider_settings.py` 的欄位選項與遮蔽迴圈、`admin-settings-panel.test.tsx` 照現有卡片案例加一個。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_provider_settings.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

`/admin/settings` 把「AI 景點介紹撰寫」設成 Gemini，再到 `/admin/hotspots#intros` 產生一次，確認 run 的 `provider` 是 gemini。

## Notes

- 功能**現在就能用**，只是只能用設定檔裡的預設供應商（`hotspot_intro_ai_default_provider`，預設 minimax）。這張任務是把選擇權交給後台，不是修 bug。
- `apps/web/messages/*/admin.json` 當時被 `2026-09-06-admin-panels-i18n-remaining` 佔著，這也是當初沒有一起做的原因；開工前先確認那張任務的狀態。
- 模型解析已經寫好了：`intro_model()` 先看自己的覆寫，沒有就退回 guide search 的模型，所以卡片留空是合理預設。
