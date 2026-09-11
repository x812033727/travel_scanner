---
id: 2026-09-11-affiliate-panel-i18n-and-disclosure
title: 合作平台面板繁中且漏用在地化佣金揭露
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/affiliate-partner-options.tsx
  - apps/api/app/trips/stay_router.py
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

- [ ] 合作平台面板在五語系都正確顯示。
- [ ] `stay_router.py` 改用 `DISCLOSURES[locale]`。
- [ ] 全 repo 沒有其他地方 import 裸的 `DISCLOSURE`。

## Steps

- [ ] `moduleLabels` 與 `:37` 的說明搬進 `messages/*/travelServices.json`。
- [ ] `:19` 的預設 `title = "合作平台"` 也處理掉（目前三個呼叫端都有傳翻譯過的 title，但預設值不該是中文）。
- [ ] `stay_router.py:21,491` 改用 `DISCLOSURES[locale]`；grep 確認沒有其他裸引用。
- [ ] 加一個測試釘住：非 zh-TW locale 的 stay 回應，`disclosure` 不得含中文字元。

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
