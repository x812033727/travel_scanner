---
id: 2026-09-06-configured-readiness-beyond-key-presence
title: 供應商就緒狀態只看金鑰有無，卡片會綠燈但功能不通
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T15:15:11Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_readiness.py
---

# 供應商就緒狀態只看金鑰有無，卡片會綠燈但功能不通

## Why

`_configured()`（`apps/api/app/admin/service.py:564`）決定 `/admin/settings` 每張卡片顯示
「已設定」還是「待設定」。多數分支判斷的只是「金鑰欄位有沒有值」：

```python
configured = bool(settings.google_maps_api_key)          # :688
configured = bool(settings.hotspot_guide_youtube_api_key) # :721
configured = bool(settings.hotspot_guide_brave_api_key)   # :728
configured = bool(settings.hotspot_guide_gemini_api_key)  # :735
```

金鑰存在不代表它有效、沒過期、沒超額、對應的 API 沒被停用。所以一張卡可以顯示綠燈，而使用者
那一側的功能是壞的。這正是 `2026-09-06-tokyo-planner-duration-500` 期間的實況：後台一路綠燈，
東京的 AI 行程規劃卻每一次都回 500。

`last_test_status == "failed"` 時卡片會轉成「連線失敗」（`settings_snapshot`），所以資訊其實
存在，只是**沒有測試過的供應商和測試成功的供應商長得一模一樣**。分不出「已驗證可用」與
「填了金鑰但從沒驗證過」，是這張任務要解掉的東西。

## Definition of done

- [ ] 卡片能區分三種狀態：已通過連線測試、有金鑰但尚未驗證、缺少金鑰。
- [ ] 「有金鑰但尚未驗證」在視覺上不等同於「可用」。
- [ ] 已經有 `_production_test_required` 強制測試的供應商行為不變。

## Steps

- [ ] 在 `settings_snapshot` 既有的 `last_test_status` 判斷上擴充：`row is None` 或
      `last_test_status is None` 時給一個獨立的 status（例如 `unverified`），不要併進 `ready`。
- [ ] 前端 `apps/web/components/admin-settings-panel.tsx` 的狀態徽章對應新值；新字串走
      `apps/web/messages/*/admin.json`（`check:i18n` 會擋 tsx 內的新中文）。**注意該檔案目前被
      其他任務佔用，動工前確認 scope。**
- [ ] 決定「上次測試成功但已隔很久」要不要降級。建議先不做，避免製造雜訊。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_readiness.py -q
```

在 `/admin/settings` 找一個有金鑰但從未按過測試連線的供應商，它不應該和剛測試成功的那些長得一樣。

## Notes

這張任務來自 2026-09-06 用 40 個代理搜尋「stored data → 有界 pydantic Field → 未處理
ValidationError → 500」那一類缺陷時的副產物。它在該輪被判定**事實成立但不屬於那個類別**
（沒有例外、沒有 500），所以另立在這裡。

刻意**不**把「呼叫外部 API 驗證」放進 `_configured()`：那個函式在每次載入設定頁時對每個供應商
各跑一次，變成網路呼叫會讓後台首頁變慢並燒掉額度。要驗證就是按「測試連線」，這張任務要做的是
讓畫面誠實反映「有沒有測過」，不是自動去測。

相關：`2026-09-06-booking-demand-test-parses-an-offer` 是同一個形狀的另一半——那張講的是測試本身
測得不夠深，這張講的是沒測過的東西被顯示成測過。
