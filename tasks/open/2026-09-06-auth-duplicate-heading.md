---
id: 2026-09-06-auth-duplicate-heading
title: 註冊關閉頁的小標與 H1 是同一句話
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:53:43Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/messages/en/auth.json
  - apps/web/messages/ja/auth.json
  - apps/web/messages/ko/auth.json
  - apps/web/messages/zh-CN/auth.json
  - apps/web/messages/zh-TW/auth.json
---

# 註冊關閉頁的小標與 H1 是同一句話

## Why

`messages/*/auth.json` 裡這兩個鍵的值一模一樣：

```
registrationPaused      = "目前暫停開放註冊"
registrationPausedTitle = "目前暫停開放註冊"
```

`registrationUnavailable` / `registrationUnavailableTitle` 同樣重複（「暫時無法確認註冊狀態」）。
一個當 eyebrow、一個當 H1，畫面上同一句話上下印兩次，看起來像模板沒填完。

小問題，但這是**沒有帳號的人看到的第一個畫面**，第一印象的成本比修它的成本高。

## Definition of done

- [ ] 註冊關閉時，eyebrow 與 H1 是兩句不同的話，且合起來讀得通。
- [ ] 五語系都改，鍵集合不變（只改值）。
- [ ] `CI=1 npm run check:i18n` 通過。

## Steps

- [ ] 決定文案分工。建議 eyebrow 當狀態標籤、H1 說人話，例如
      eyebrow「註冊狀態」／H1「目前暫停開放註冊」，
      或 eyebrow「暫停中」／H1「現在還不能建立新帳號」。
- [ ] 五語系一起改，不要只改繁中。
- [ ] `registrationUnavailable` / `registrationUnavailableTitle` 一併處理。

## How to verify

```bash
cd .. && CI=1 node tools/check-i18n.mjs
```

把後台的註冊開關關掉，開 `/zh-TW/register` 與 `/en/register` 各看一次。
（後台開關在 `/admin/system-settings`。）

## Notes

只改 `messages/*/auth.json` 的**值**就夠，元件不用動 —— 所以 scope 只有那五個檔案，
不會擋到任何人改 `auth-form.tsx`。

`check:i18n` 只驗鍵集合與 ICU 參數一致，不會驗「兩個鍵的值不可以相同」，
所以這種重複不會被自動擋下，得靠人看。
