---
id: 2026-09-11-fare-lab-warnings-and-copy
title: 航班票價實驗室三個畫面的多語系與警告代碼
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-11T20:41:05Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/back-to-back-fare-search.tsx
  - apps/web/components/live-back-to-back-search.tsx
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
---

# 航班票價實驗室三個畫面的多語系與警告代碼

## Why

`2026-09-11-remaining-api-warning-literals` 把後端所有送給前端的警告都改成代碼，讓讀者自己的
catalog 去說。**只留了三處沒改**，並在 `apps/api/tests/test_warning_codes.py` 的 allow-list
裡寫明理由：

| 位置 | 內容 |
| --- | --- |
| `crawlers/back_to_back.py:810` | 「{currency} 使用七日內的舊匯率估算 TWD。」 |
| `crawlers/back_to_back.py:812` | 「{currency}：目前無法取得 TWD 估算匯率。」 |
| `providers/live_back_to_back.py:274` | 「{role}：沒有可用即時票價」 |

理由是渲染端：`airline-fare-lab.tsx:337`、`back-to-back-fare-search.tsx:651`、
`live-back-to-back-search.tsx:183` 都是 `result.warnings.map((warning) => …{warning})`——
原樣印出，沒有 catalog 可查。送代碼過去只會把識別字印在畫面上，比現在更糟。

而那三個畫面本來就整頁寫死繁中（標題、空狀態、每一張比較卡），所以這不是補三個 key 就好，
是那三頁還沒做多語系。`airline_fares` 是站主刻意關閉的四個功能之一，目前線上回「尚未開放」，
所以不急——但要做就是一起做。

## Definition of done

- [ ] 三個畫面改用 message catalog（五語系），不再有寫死的使用者可見中文。
- [ ] 三處後端警告改用 `app.warnings.warning_code`，帶 `currency` / `role` 參數。
- [ ] 三個渲染端改用 `apps/web/lib/warnings.ts` 的 `translateWarnings`。
- [ ] `apps/api/tests/test_warning_codes.py` 的 allow-list 清空，那條 ratchet 變成無例外。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_warning_codes.py -q
cd apps/web && npm run check:i18n && npm run test:web -- airline-fare back-to-back live-back
```

## Notes

- 參數化警告的寫法已經有了：`code?name=value`，值做 percent-encode。
  後端 `app/warnings.py`，前端 `apps/web/lib/warnings.ts`，兩邊都有測試。
- 這三頁的漢字量不小，做之前先估一下 key 數；`lib/itinerary-messages/` 那種功能專屬的側
  catalog 是另一個選項，可以避開多人同時編輯 `messages/*/search.json` 的衝突。
