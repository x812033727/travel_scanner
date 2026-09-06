---
id: 2026-09-06-api-error-details-untranslated
title: 出錯時，非繁中讀者拿到的是同一句通用訊息
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T20:39:35Z
created_at: 2026-09-06T20:35:00Z
completed_at: 2026-09-06T20:44:50Z
branch: claude/api-error-i18n
depends_on: []
scope:
  - apps/api/app/i18n.py
  - apps/api/tests/test_error_localization.py
---

# 出錯時，非繁中讀者拿到的是同一句通用訊息

## Why

`app/problems.py` 的 `app_error_handler` 這樣決定 `detail`：

```python
detail = exc.detail if locale == "zh-TW" else ERROR_DETAILS[locale].get(
    exc.code, GENERIC_DETAILS[locale]
)
```

機制是對的——非繁中讀者不會拿到中文。問題是覆蓋率：**API 會 raise 的 263 個錯誤碼裡，
`ERROR_DETAILS` 只認得 82 個**。其餘的一律退回 `GENERIC_DETAILS`：

> The request could not be completed. Please try again.

所以一個英文讀者不管撞到什麼——航班已存在、日期超出旅程、次數不足、旅程被別人改過、
LINE 還沒綁定——看到的都是同一句。繁中讀者則拿到 263 句寫得很具體的訊息。

這是這個站在多語系上最後一塊明顯的落差：畫面上的字都翻好了，出錯時的字沒有。

### 訂正：這張票原本寫「只有 15 個有翻譯」

那個數字是錯的，來自一個把 `ERROR_DETAILS["en"]` 的區塊切錯的正規表示式——多行括號寫法的
值讓它提早結束。實際 import 這個模組數出來是 **82** 個。分母 263 是對的。

## Definition of done

- [x] 使用者真的會撞到的錯誤碼（公開端點，非後台）四個語系都有具體訊息。
- [x] 有一個測試會在新增錯誤碼卻沒補翻譯時失敗——不然這張票會再長回來。
- [x] 繁中的訊息一字不改（`exc.detail` 仍是繁中的唯一來源）。

## Steps

- [x] 分類 263 個碼：路徑含 `admin`／`deployments` 的算後台，其餘算公開。
      公開 192、只在後台出現的 71。
- [x] 公開的 192 個逐一補上 en／ja／ko／zh-CN，照 `OAUTH_ERROR_DETAILS` 的體例寫進
      `ERROR_DETAILS`。本次新增 131 句 × 4 語系（82 + 131 = 213，另有 18 個後台碼本來就有）。
- [x] 加守門測試 `tests/test_error_localization.py`：掃描 `app/` 收集所有 `AppError` 的碼，
      斷言公開的碼四個語系都有、四個語系的鍵集合一致、沒有空字串也沒有殘留的 `{}` 佔位符。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_error_localization.py
```

正式站（部署後）：

```bash
curl -s -H 'X-Travel-Locale: en' https://mokaair.com/api/travel/trips/00000000-0000-0000-0000-000000000000
```

`detail` 應該是「This trip could not be found」，不是通用那句。

## Notes

- 表格沒有插值能力（`dict[str, str]`，用碼查表），所以原文帶 f-string 的那幾句在譯文裡
  改成不帶數字的說法：`route_items_limit`（原文「每次最多 N 個」）、`trip_ledger_full`、
  `trip_date_range_too_long`、`trip_places_too_many_lines`、`itinerary_optimization_limit`、
  `trip_shrink_confirmation_required`、`usage_operation_unknown`、`holiday_country_unknown`。
  繁中讀者仍然看得到數字，因為繁中走的是 `exc.detail`。守門測試會擋住任何殘留的 `{`。
- **後台的 71 個碼刻意不翻**：後台面板本身就是繁中優先，操作者看碼比看句子多。測試把
  「路徑含 admin／deployments」當成豁免規則寫在檔案註解裡，不是一份會腐爛的清單。
  其中 18 個本來就有譯文，留著不動。
- `FIELD_LABELS` 與 `_localized_issue`（422 的欄位驗證訊息）也是繁中的，同一個家族，
  但它們有自己的組句邏輯（把 pydantic 的英文訊息換成中文），要另外處理。
- 相關但不同：`/search` 的供應商徽章印的是 200 回應裡的繁中欄位，不經過這個處理器，
  已經另外修掉，見 [[2026-09-06-search-provider-badge-chinese]]。
