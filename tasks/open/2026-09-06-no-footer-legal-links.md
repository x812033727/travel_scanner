---
id: 2026-09-06-no-footer-legal-links
title: 後台以外的公開頁沒有頁尾，也沒有隱私權、條款、關於或聯絡的連結
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-06T17:32:55Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/app/[locale]/layout.tsx
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/navigation.json
---

# 後台以外的公開頁沒有頁尾，也沒有隱私權、條款、關於或聯絡的連結

## Why

2026-09-07 上線後的獨立查核：13 個公開頁 `document.querySelector("footer")` 全部是
null，把所有 `<a href>` 用 `/privacy|terms|legal|about|contact|policy|隱私|條款/i`
掃過去，全站一個都沒有（只有 /foods 上兩個店家自己的外部連結）。

一個會員站沒有隱私權政策與服務條款，除了讓讀者找不到「這家是誰、資料怎麼用」之外，
Google／Apple 登入的服務條款、以及未來要接的金流都會要求這兩頁。對長輩來說，頁尾
還是他們找「聯絡我們」的第一個地方。

## Definition of done

- [ ] 每個公開頁底部都有頁尾：隱私權政策、服務條款、關於、聯絡方式、語言與版權。
- [ ] 手機上頁尾不會被底部導覽列蓋住。
- [ ] 五個語系都有翻譯。

## Notes

政策內容本身要人來定，不是模型能編的：先把版位與連結做出來，內容跟使用者確認。
