---
id: 2026-09-13-klook-clickout-locale
title: Klook clickout ignores the visitor locale
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-13T15:07:10Z
created_at: 2026-09-13T15:06:14Z
completed_at:
branch: claude/klook-clickout-locale
depends_on: []
scope:
  - apps/api/app/i18n.py
  - apps/api/app/travel_services/channels.py
  - apps/api/tests/test_klook_affiliates.py
---

# Klook clickout ignores the visitor locale

## Why

每一個 Klook 外連最後都會經過 `klook_affiliate_target`，而它把 offer 裡存的網址原樣帶走。
店家資料是用 zh-TW 審的（`docs/klook-integration.md:75` 的範例就是 `/zh-TW/hotels/...`），
所以日文、韓文、英文讀者按下去也是開繁體中文的 Klook 頁面。
`active_locale()` 早就在同一條路徑上（`affiliates/service.py:218` 拿它組 `sub_id`），
只是從來沒有拿來決定連結本身。

## Definition of done

- [x] 五個語系的讀者按下 Klook 按鈕，開到的是同一個商品的對應語言版本。

## Steps

- [x] `i18n.py` 的 `PROVIDER_LOCALES` 加 `klook`（沿用 booking／skyscanner 的既有機制）。
- [x] `channels.py` 加 `klook_locale_target`，在 `klook_affiliate_target` 裡呼叫。
- [x] 測試：五語系各驗一次、樣板網址沒有語系段時要插入、冪等、以及改寫不能救回被拒絕的網址。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_klook_affiliates.py tests/test_i18n.py -q
./.venv/Scripts/python.exe -m ruff check .
```

部署後：用不同語言開站，按任一個 Klook 按鈕，看落地網址的語系段是否跟著變
（例如日文版應該是 `https://www.klook.com/ja/...`）。

## Notes

- 對照表不是猜的：Klook 商品頁自己的 hreflang 就列了 `/ja/`、`/ko/`、`/zh-TW/`、`/zh-CN/`、
  `/en-US/` 搭配**同一個 slug**，實測 `https://www.klook.com/ja/hotels/detail/285841-hotel-gracery-shinjuku/`
  （zh-TW 的 slug 配 ja 前綴）回傳日文頁且 canonical 就是它本身——Klook 是用數字 id 認頁面，slug 只是裝飾。
  `en` 沒有無地區的英文版，所以用 `en-US`。
- 改寫刻意放在 `klook_canonical_target` **之後**：那道閘擋掉 redirect 路徑與外來 AID，
  先改寫等於讓語系段有機會把被擋的網址變成過得了的網址。測試有一條專門守這件事。
- 三個呼叫點（`affiliates/router.py:458`、`affiliates/service.py:246`、`channels.py:217`）
  全都收斂到 `klook_affiliate_target`，所以只要改那一個函式。前端與文章內容包裡沒有任何
  硬編碼的 klook.com 連結（已 grep 確認），不需要動 web。
- 點擊當下語系拿得到：表單 POST 帶不了自訂標頭，但 BFF 會用查詢字串的 `locale` 或
  `travel_locale` cookie 補出 `X-Travel-Locale`（`apps/web/app/api/travel/[...path]/route.ts:79,97`）。
- `--force` 認領：`2026-09-12-food-merchant-enrichment` 的 scope 也圈了 `i18n.py`，但那張票
  claim 於 2026-09-12 已過期，分支沒推上 origin，且只動 837 行之後的 `ERROR_DETAILS`，
  與這裡改的 `PROVIDER_LOCALES`（17 行）不重疊。
- 若某個 Klook 商品是透過 Travelpayouts 通路（而非 `klook_direct`）出去的，最終網址由
  Travelpayouts 的 Links API 產生，這裡改不到，是已知的邊界。
