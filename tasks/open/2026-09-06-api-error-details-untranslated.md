---
id: 2026-09-06-api-error-details-untranslated
title: 263 個錯誤碼裡只有 15 個有翻譯，其餘語系一律拿到同一句通用訊息
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T20:35:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/i18n.py
  - apps/api/tests/test_error_localization.py
---

# 263 個錯誤碼裡只有 15 個有翻譯，其餘語系一律拿到同一句通用訊息

## Why

`app/problems.py` 的 `app_error_handler` 這樣決定 `detail`：

```python
detail = exc.detail if locale == "zh-TW" else ERROR_DETAILS[locale].get(
    exc.code, GENERIC_DETAILS[locale]
)
```

機制是對的——非繁中讀者不會拿到中文，這點沒問題。問題是覆蓋率：

| | 數量 |
| --- | --- |
| API 裡實際 raise 的相異錯誤碼 | 263 |
| `ERROR_DETAILS` 有翻譯的 | 15 |
| 退回通用句的 | **249** |

（量法：`grep AppError(<status>, "<code>"` 收集所有碼，對照 `i18n.py` 的 `ERROR_DETAILS["en"]`。）

所以一個英文讀者不管撞到什麼，看到的都是
「The request could not be completed. Please try again.」——航班已存在、日期超出範圍、
次數不足、行程被別人改過，全部同一句。繁中讀者則拿到 429 句寫得很具體的訊息。

這是這個站在多語系上最後一塊明顯的落差：畫面上的字都翻好了，出錯時的字沒有。

## Definition of done

- [ ] 使用者真的會撞到的錯誤碼（公開端點，非後台）四個語系都有具體訊息。
- [ ] 有一個測試會在新增錯誤碼卻沒補翻譯時失敗——不然這張票會再長回來。
- [ ] 繁中的訊息一字不改（`exc.detail` 仍是繁中的唯一來源）。

## Steps

- [ ] 先分類 263 個碼：公開端點 vs 後台端點（後台目前是繁中優先，可以晚一步）。
      量過的分布：`trips/router.py` 74、`hotspots/admin_router.py` 42、
      `foods/admin_router.py` 37、`auth/oauth.py` 22、`places/router.py` 20、
      `restaurants/admin_sources_router.py` 17、`search/router.py` 14、
      `hotspots/router.py` 12、`deployments/service.py` 11、`line/router.py` 11。
      扣掉 admin 的 117 個，公開的是 146 個。
- [ ] 從公開的 146 個開始，一碼四句（en／ja／ko／zh-CN），照 `OAUTH_ERROR_DETAILS` 的體例
      分組寫進 `ERROR_DETAILS`。
- [ ] 加守門測試：掃描 `app/` 收集所有 `AppError` 的碼，斷言公開清單全部在 `ERROR_DETAILS["en"]`
      裡（後台的碼放一份明確的豁免清單，並在註解寫下為什麼）。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' 'https://mokaair.com/api/travel/destinations?country_code=ZZ' | python -c "import json,sys; print(json.load(sys.stdin))"
```

拿到的 `detail` 應該說清楚是什麼問題，而不是一句通用的。

## Notes

- 不要把 `exc.detail` 直接丟給翻譯——那是繁中的原文，走機器翻譯會讓四個語系的品質不一致，
  而且錯誤訊息正是最需要精準的地方。用碼查表，跟現在的 15 個一樣。
- 相關但不同：`/search` 的供應商徽章印的是 200 回應裡的繁中欄位，不經過這個處理器，
  已經另外修掉，見 [[2026-09-06-search-provider-badge-chinese]]。
- `FIELD_LABELS` 與 `_localized_issue`（422 的欄位驗證訊息）也是繁中的，同一個家族，
  但它們有自己的組句邏輯，建議在上面那 146 個做完之後再單獨處理。
