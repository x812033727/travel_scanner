---
id: 2026-09-11-affiliate-panel-i18n-and-disclosure
title: 合作平台面板繁中且漏用在地化佣金揭露
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T16:30:48Z
created_at: 2026-09-11T03:20:59Z
completed_at: 2026-09-11T17:18:14Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/affiliate-partner-options.tsx
  - apps/web/components/affiliate-partner-options.test.tsx
  - apps/api/app/trips/stay_router.py
  - apps/api/tests/test_trip_stay_router.py
  - apps/web/messages/en/travelServices.json
  - apps/web/messages/ja/travelServices.json
  - apps/web/messages/ko/travelServices.json
  - apps/web/messages/zh-CN/travelServices.json
  - apps/web/messages/zh-TW/travelServices.json
---

# 合作平台面板繁中且漏用在地化佣金揭露

## Why

**一、模組標籤寫死繁中。** `affiliate-partner-options.tsx:11-17` 的 `moduleLabels` 是一個寫死的 zh-TW record（「航班合作平台」「住宿合作平台」「活動與票券」「交通與接送」「eSIM 上網」），`:38` 對所有語系原樣渲染。`:37` 的說明文字「以下為外部合作平台，切換或前往查看不扣使用次數。」也是 inline。

這個元件同時出現在 `/search`（`search-experience.tsx:1636,1689`）**和**行程編輯器（`trip-editor.tsx:2000`）——是變現介面，卻對英日韓使用者顯示繁中。

**二、漏用在地化揭露。** `apps/api/app/affiliates/router.py:58` 定義了 zh-TW 的 `DISCLOSURE`，`:59-64` 定義了五語系的 `DISCLOSURES` map，`:239` 與 `:419` 正確使用 `DISCLOSURES[locale]`。但 `apps/api/app/trips/stay_router.py:21` import 的是那個**裸常數**，`:491` 原樣回傳成 `"disclosure"`，由 `stay-area-flow.tsx:396` 渲染。非中文使用者在住宿區域「尚未就緒／無結果」的路徑上，拿到繁中的佣金揭露。

佣金揭露是法遵相關文字，不只是翻譯問題。

## Definition of done

- [x] 合作平台面板在五語系都正確顯示。
- [x] `stay_router.py` 改用 `DISCLOSURES[locale]`。
- [x] 全 repo 沒有其他地方 import 裸的 `DISCLOSURE`。

## Steps

- [x] `moduleLabels` 與 `:37` 的說明搬進 `messages/*/travelServices.json`。
- [x] `:19` 的預設 `title = "合作平台"` 也處理掉（目前三個呼叫端都有傳翻譯過的 title，但預設值不該是中文）。
- [x] `stay_router.py:21,491` 改用 `DISCLOSURES[locale]`；grep 確認沒有其他裸引用。
- [x] 加一個測試釘住：非 zh-TW locale 的 stay 回應，`disclosure` 不得含中文字元。

## How to verify

```bash
cd apps/api && uv run pytest tests -k "stay or affiliate" -q
cd apps/web && npm run check:i18n && npm run test:web -- affiliate
```

## Notes

- `docs/affiliate-configuration.md:170-173` 把「佣金揭露只有繁中」列為已知缺口，並標示為大致已修——`stay_router.py` 是唯一漏掉的呼叫端，文件可以順手更新。
- **認領會被擋，這是正常的。** `2026-09-11-hotel-operation-rakuten-clickout`（owner `codex-hotel-guard`，目前 `review`）的 scope 含同樣五個
  `apps/web/messages/*/travelServices.json`，所以在它離開 review 之前，`claim` 會拒絕這張任務。
  等它結束再認領，不要為了繞過而把 scope 改窄成不誠實的範圍。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器對 `en` / `ja` / `ko` 共 12 條路由，搜尋第一輪點名的 27 個寫死繁中字串，**零命中**。

**這不代表本任務的問題不存在，而是那些程式路徑在唯讀環境下走不到**：刪除確認框需要帳號裡有行程（測試帳號 0 筆）、機票與飯店卡需要完成一次搜尋（環境只轉讀取，不送寫入）、行程時間軸需要行程裡有項目。

所以本任務的狀態是**未驗證**，不是**已推翻**。接手的人請自己建一筆有內容的行程再確認，不要因為「掃描沒掃到」就把它關掉。

順帶澄清一個第二輪用過的無效指標：曾以「頁面漢字佔比」推估洩漏程度，但**日文本來就使用漢字**（實測 `ja` 頁面漢字 28–37%，同時有大量假名，是真正的日文），該指標對日文無效，不可採信。英文頁實測漢字僅 0.2–5.2%，且經逐一檢查後確認全部來自語言切換器的語言名稱（繁體中文／简体中文／日本語），屬正確做法。

## claim 用了 --force，理由寫在這裡（claude-opus-5, 2026-09-11）

`messages/*/travelServices.json` 五個檔在 `2026-09-11-hotel-operation-rakuten-clickout`（codex-hotel-guard）的 scope 裡。它的 claim 只有 13 小時，**還沒到 24 小時的 stale 門檻**，所以我先查了它到底還在不在動：

- 它的工作已經合併進 main：`5e3168e Guard hotel operating dates, Rakuten Japan links and booking handoffs (#389)`，正是最後一次動到 `travelServices.json` 的 commit。
- 它的遠端分支 `codex/hotel-operation-rakuten-clickout` 已經不存在（`git ls-remote --heads` 沒有回傳）。

也就是說沒有正在進行中的工作需要被保護，只是任務檔沒標 `done`。24 小時那條規則是為了避免兩個人同時改同一個檔，這裡沒有那個風險。重疊的部分只是往 JSON 加一個新的 top-level key。

沒有去改它的任務檔。

## 完成紀錄（claude-opus-5, 2026-09-11）

**一、模組標籤。** 不必新增翻譯——`travelServices.json` 早就有 `affiliateFlight` / `affiliateHotel` / `affiliateActivities` / `affiliateTransport` / `affiliateConnectivity`，五語系齊全。元件裡那份 `moduleLabels` 是第二套、只有繁中的死抄本，直接刪掉改讀 catalog。

只新增一個 key：`affiliatePanelHint`（「以下為外部合作平台，切換或前往查看不扣使用次數。」）。

預設 `title = "合作平台"` 改成 `title ?? t("title")`。三個呼叫端目前都有傳自己的 title，所以這個預設值一直沒被看見——但它在那裡等著第一個不傳 title 的呼叫端。

**二、佣金揭露。** `stay_router.py:21` import 的是裸的 `DISCLOSURE`（繁中），`:491` 原樣回傳。同一個函式的簽章裡就有 `locale: RequestLocale`，改成 `DISCLOSURES[locale]` 一行就好。

`grep -rn "\bDISCLOSURE\b" apps/api --include=*.py` 現在只剩 `affiliates/router.py` 自己定義它、以及 `DISCLOSURES["zh-TW"]` 引用它。

### 驗證

`test_trip_stay_router.py` 加兩個案例。第一版我寫的是「非 zh-TW 的 disclosure 不得含漢字」，**跑起來就錯了**——日文和簡中本來就有漢字。改成釘住每個語系該拿到的那一句：

```python
assert payload["disclosure"] == DISCLOSURES[locale]
assert payload["disclosure"] != DISCLOSURES["zh-TW"]
```

把 `DISCLOSURES[locale]` 還原成 `DISCLOSURES["zh-TW"]` 之後 en/ja/ko/zh-CN 四個 parametrize 全紅，復原後 13 passed。
