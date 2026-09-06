---
id: 2026-09-06-legal-content-from-owner
title: 隱私權政策、服務條款與聯絡方式的內容要由擁有者提供
status: blocked
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-06T20:59:55Z
created_at: 2026-09-06T19:44:10Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/[locale]/privacy/page.tsx
  - apps/web/app/[locale]/terms/page.tsx
  - apps/web/app/[locale]/contact/page.tsx
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/navigation.json
---

# 隱私權政策、服務條款與聯絡方式的內容要由擁有者提供

## Why

`2026-09-06-no-footer-legal-links` 把頁尾與四個頁面做出來了，但那張任務的 Notes 寫得很清楚：
「政策內容本身要人來定，不是模型能編的。」所以 `/privacy` 與 `/terms` 現在只寫一句
「這份文件還沒有公開」，`/contact` 只說對外管道還在建立中。**這是刻意的**：生出來的隱私權
條文會被讀者當成承諾，而那個承諾沒有任何人做過，比沒有那一頁更糟。

`/about` 不一樣，它寫的是這個產品實際在做什麼，內容是真的，不需要等。

擋著的東西：

- Google 與 Apple 登入的送審都要求可公開存取的隱私權政策網址。
  相關任務 [[2026-09-06-social-login]] 目前程式做完了但沒開通。
- 未來要接金流一定會要服務條款。
- 讀者現在找不到「這家是誰、資料怎麼用、出事找誰」。

## Definition of done

- [ ] `/privacy` 有真的隱私權政策，五個語系。
- [ ] `/terms` 有真的服務條款，五個語系。
- [ ] `/contact` 有一個真的可以聯絡到人的方式。
- [ ] 三個頁面都不再顯示 `footerPendingTitle` / `footerPendingBody` / `footerContactBody`，
      而且那三個 message 鍵被刪掉（留著就會爛掉）。

## Steps

- [ ] **先問擁有者這四件事**，其他都做不了：
      1. 對外的法律主體名稱（公司或個人）與所在地，決定適用哪一國的法規。
      2. 可以公開的聯絡方式（email 或表單收件處）。
      3. 資料保存期限與刪除帳號的處理方式。
      4. 是否已經有法務或範本要沿用。
- [ ] 依答覆撰寫兩份文件，**由人審過**才上線。
- [ ] 把三個頁面的 placeholder 換掉，刪掉那三個 message 鍵，`check:i18n` 會確認五個語系同步。

## How to verify

```bash
npm run check:i18n && npm run test:web -- site-footer
```

開 `/zh-TW/privacy`、`/en/terms`、`/ja/contact`，確認顯示的是真的內容而不是待補說明。

## Notes

- 已經知道的事實：整個 repo 目前沒有任何 email、法律主體名稱或對外聯絡方式，
  所以這四個問題不能從程式碼裡查，只能問人。
- 頁尾與四個頁面的版位已經做好，這張任務只換內容，不動版面。
- **不要請模型代寫這兩份文件然後直接上線。** 那正是上一張任務刻意沒做的事。
