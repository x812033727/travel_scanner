---
id: 2026-09-11-social-login-buttons-use-official-brand
title: Social login buttons use official brand marks
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T09:07:24Z
created_at: 2026-09-11T09:07:21Z
completed_at: 2026-09-11T09:16:26Z
branch: claude/google-apple-line-login-0fmfi5
depends_on: []
scope:
  - apps/web/components/social-login-buttons.tsx
  - apps/web/components/brand-marks.tsx
  - apps/web/components/social-login-buttons.test.tsx
---

# Social login buttons use official brand marks

## Why

`social-login-buttons.tsx:11-15` 用文字當第三方登入的識別：Google 是一個字母
`"G"`、LINE 是文字 `"LINE"`、Apple 是 `""` 字元。

三家的登入按鈕規範都要求使用官方圖形，不是自己排版的近似物。`""` 還有實際
故障：在沒有安裝 Apple 字型的平台上會變成缺字方塊。

另外按鈕要等 `/auth/oauth/providers` 這個 client-side 請求回來才出現。
Email 表單就在正下方，所以按鈕抵達時會把表單往下推——讀者的指標正停在那裡。

## Definition of done

- [x] 三顆按鈕使用官方圖形與官方指定的按鈕配色。
- [x] Apple 標誌在沒有 Apple 字型的平台上也正確顯示。
- [x] 供應商清單還不知道時，版面高度不會塌陷再彈開。
- [x] 這個元件有測試（先前完全沒有）。

## Steps

- [x] 新增 `apps/web/components/brand-marks.tsx`：`GoogleMark` / `LineMark` /
      `AppleMark` 三個 inline SVG 元件。
- [x] `social-login-buttons.tsx` 的 `mark: string` 改成
      `Mark: ComponentType<{ className?: string }>`。
- [x] 補載入佔位；請求成功或失敗都要收掉，不能留下永久空白。
- [x] 新增 `social-login-buttons.test.tsx`。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run check:i18n
cd apps/web && npx vitest run components/social-login-buttons.test.tsx
```

圖形本身用瀏覽器實際渲染確認過（三個 SVG 抽出來放進一張 HTML，
用 `/opt/pw-browsers/chromium-1194` 截圖檢查），不是只看程式碼通過。
手寫的路徑資料光看 diff 看不出來畫出來是什麼。

## Notes

### 沒有新增任何 i18n key

`auth.continueWith.{google,line,apple}` 與 `auth.orUseEmail` 五個語系本來就齊全
（en / ja / ko / zh-TW / zh-CN 逐一確認過），`npm run check:i18n` 通過。

### 為什麼用 inline SVG 而不是 public/ 的檔案

按鈕在 client component 裡、要跟著讀者的文字大小縮放，而且第一次繪製時不該再多
一次網路請求——圖形晚於按鈕抵達會是另一種閃動。

### 品牌色是固定值，不是主題變數

Google 的淺色按鈕是白底深字、LINE 是 #06C755、Apple 是黑底。這三組是品牌資產，
規範不允許改色，所以它們**刻意**不跟著站上的 CSS 變數走，在淺色與深色主題下都一樣。
Google 的邊框順手從 `var(--line)` 改成規範的 `#747775`，文字從 `#3c4043` 改成
現行規範的 `#1f1f1f`。只有 LINE 與 Apple 的圖形用 `currentColor`，因為規範本來就
允許它們是按鈕前景色的挖空。

### 先前沒有被測到的行為

新測試釘住了四件事：只渲染回報為已設定的供應商、`start` URL 帶對
`intent`/`locale`/`next`、供應商查詢失敗時不擋住 Email 表單、
以及未知的 `oauth_error` 會落到 `oauth_token_invalid` 而不是把原始字串顯示給使用者。
