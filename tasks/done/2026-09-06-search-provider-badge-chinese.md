---
id: 2026-09-06-search-provider-badge-chinese
title: 搜尋頁的供應商徽章在五個語系都印出 API 的繁中句子
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T20:30:00Z
created_at: 2026-09-06T20:30:00Z
completed_at: 2026-09-06T20:31:05Z
branch: claude/provider-status-i18n
depends_on: []
scope:
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-experience.test.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 搜尋頁的供應商徽章在五個語系都印出 API 的繁中句子

## Why

2026-09-07 用 Playwright 走過 `/en`、`/ja`、`/ko` 的九個公開頁，只有 `/search` 的主要內容
留著整句繁中：

```
目前沒有可用的航班查價供應商。；目前沒有可用的飯店查價供應商。；正式環境禁止使用模擬報價。
```

三個語系一字不差。來源是 `search-experience.tsx` 直接把 API 的 `providerStatus.message`
印出來，而那個字串是 `apps/api/app/providers/registry.py` 在伺服器端用繁中組出來的
（`ready_message` / `missing_message`，全檔共 12 句）。這些不是 `AppError`，是 200 回應
裡的欄位，所以 `problems.py` 的錯誤訊息翻譯機制根本碰不到它。

那句話說的每一件事，旁邊的結構化欄位都已經有了：`status`、`mode`、`selected_provider`，
以及 `module_statuses` 裡每個模組的 `available`。

## Definition of done

- [x] `/en`、`/ja`、`/ko`、`/zh-CN` 的搜尋頁徽章都是該語系的句子。
- [x] zh-TW 讀者看到的資訊量不減少（哪一個模組停了，仍然逐項列出）。
- [x] API 不必改：只要不再印 `message`，`registry.py` 的繁中字串就只剩後台在讀。

## Steps

- [x] 徽章改成由 `status`／`mode`／`module_statuses` 組出來，一個停用的模組一顆徽章。
- [x] 五個語系各加八個鍵（兩句就緒、一句停用、一句全停、四個模組名）。
- [x] 測試釘住：停用時看得到「航班查價暫停」「住宿查價暫停」且 API 的繁中句子沒有出現在
      畫面上；就緒時看得到「即時報價 · skyscanner」。

## How to verify

```bash
curl -s https://mokaair.com/api/travel/providers/status | head -c 300
```

開 `https://mokaair.com/en/search?origin=TPE&destination=NRT&departure_date=2026-11-10`，
標題旁的徽章應該是英文。

## Notes

- 順帶量到的正式站狀態：**航班與飯店查價供應商目前都沒有設定**（Skyscanner／Duffel／
  Amadeus 都沒有金鑰，Booking 也沒有），所以 `/search` 本來就查不到價。那是設定問題不是
  程式問題，但值得讓擁有者知道，因為站上最主要的功能因此停著。
- API 那一邊還有更大的一塊：263 個錯誤碼裡只有 15 個有翻譯，見
  [[2026-09-06-api-error-details-untranslated]]。那個的表現方式不同——非繁中讀者拿到的是
  一句通用的「The request could not be completed」，不是中文——所以是另一張票。
- 未來 API 若新增模組（目前是 flight／hotel／activities／transport），前端會退回「即時查價暫停」
  而不是印出未翻譯的鍵。
