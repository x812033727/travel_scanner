---
id: 2026-09-06-no-footer-legal-links
title: 後台以外的公開頁沒有頁尾，也沒有隱私權、條款、關於或聯絡的連結
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T19:26:50Z
created_at: 2026-09-06T17:32:55Z
completed_at: 2026-09-06T19:46:59Z
branch: claude/site-footer
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
  - apps/web/app/[locale]/privacy/page.tsx
  - apps/web/app/[locale]/terms/page.tsx
  - apps/web/app/[locale]/about/page.tsx
  - apps/web/app/[locale]/contact/page.tsx
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/metadata.json
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

- [x] 每個公開頁底部都有頁尾：隱私權政策、服務條款、關於、聯絡方式、語言與版權。
- [x] 手機上頁尾不會被底部導覽列蓋住。
- [x] 五個語系都有翻譯。

## Notes

政策內容本身要人來定，不是模型能編的：先把版位與連結做出來，內容跟使用者確認。

## Result（2026-09-07 完成版位，內容待擁有者）

頁尾做好並掛進 `[locale]/layout.tsx`，五個語系齊全。四個連結各自有落腳的頁面。

**手機不被底部導覽列蓋住，靠的是既有的 CSS 不是新的。** `.public-app-shell` 本來就有
`padding-bottom: calc(5rem + env(safe-area-inset-bottom))` 幫固定的 `.app-bottom-nav` 讓位，
所以把頁尾放進那個 shell 裡面（在 `{children}` 之後）就落在保留區之上，不需要另外加間距。

**兩個地方不顯示頁尾**：`/admin` 不是公開頁、有自己的外框；`/trips/<id>` 的行程編輯器是
全螢幕 shell，本來就把底部導覽列藏起來，再加一段頁尾會把行程擠出手機第一屏。判斷用
`usePathname()`，跟 `app-bottom-nav.tsx` 同一套。

`year` 是從 layout（伺服器端）當 prop 傳進去的，不在 client 元件裡呼叫 `new Date()`，
否則跨年那一刻會 hydration mismatch。

### 內容刻意沒有寫

任務 Notes 說「政策內容本身要人來定，不是模型能編的」，這點我照做，而且它比看起來重要：
生出來的隱私權條文會被讀者當成承諾，而那個承諾沒有任何人做過——那比沒有那一頁更糟。

- `/privacy`、`/terms`：只寫「這份文件還沒有公開」與為什麼，明確聲明在公開前不代表任何承諾。
- `/contact`：說明對外管道還在建立中。查過了，整個 repo 沒有任何 email、法律主體名稱或
  聯絡方式，所以這不是我沒找，是真的不存在。
- `/about`：**這一頁有真的內容**，因為它寫的是產品實際在做什麼，不需要等誰決定。

要換成真內容的四個問題（法律主體、聯絡方式、資料保存期限、有無現成範本）寫在
[[2026-09-06-legal-content-from-owner]]，P1，並且註明不要請模型代寫後直接上線。

### 順帶被自己的測試擋一次

四個新頁面一建好，前一張任務加的 `metadata.test.ts` 就要求它們也要有自己的
`generateMetadata`，所以 `metadata.json` 多了 8 組鍵。那個測試按預期在做事。

檢查：`lint:web`、`typecheck:web`、`check:i18n`、完整 `vitest run`（110 檔 564 測試）全綠，
其中頁尾自己 14 個、metadata 守門 27 個。
