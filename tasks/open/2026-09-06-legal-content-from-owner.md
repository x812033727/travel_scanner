---
id: 2026-09-06-legal-content-from-owner
title: 隱私權政策、服務條款與聯絡方式的內容要由擁有者提供
status: review
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-10T16:59:30Z
created_at: 2026-09-06T19:44:10Z
completed_at:
branch: claude/mokaair-privacy-terms-ji8492
depends_on: []
scope:
  - apps/api/app/site_pages/drafts
  - apps/api/tests/test_site_pages.py
  - docs/contact-channels.md
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

- [x] `/privacy` 有真的隱私權政策，五個語系。
- [x] `/terms` 有真的服務條款，五個語系。
- [x] `/contact` 有一個真的可以聯絡到人的方式。
- [x] 三個頁面都不再顯示 `footerPendingTitle` / `footerPendingBody` / `footerContactBody`，
      而且那三個 message 鍵被刪掉（留著就會爛掉）。
- [ ] **擁有者在 `/admin/site-pages` 逐語系讀過、填生效日期並發布**。這一步只有人能做，
      程式碼不會替他按下去。

## Steps

- [x] **先問擁有者這四件事**，其他都做不了：
      1. 對外的法律主體名稱（公司或個人）與所在地，決定適用哪一國的法規。
      2. 可以公開的聯絡方式（email 或表單收件處）。
      3. 資料保存期限與刪除帳號的處理方式。
      4. 是否已經有法務或範本要沿用。
- [x] 依答覆把確認事實寫進五個語系的草稿，生效日期留空（發布時才由人填）。
- [x] 刪掉死掉的 message 鍵，`check:i18n` 確認五個語系同步。
- [ ] 擁有者（必要時含法務）逐語系審閱後發布；發布步驟見
      [`docs/contact-channels.md`](../../docs/contact-channels.md)。

## How to verify

```bash
npm run check:i18n && npm run test:web -- site-footer
cd apps/api && uv run pytest tests/test_site_pages.py -q
```

`/zh-TW/privacy`、`/en/terms`、`/ja/contact` 在發布前仍然顯示「內容準備中」，
那是對的：草稿有內容不等於已發布。發布後才應該看到正式內容與頁尾的確認資訊。

## Notes

2026-09-10，擁有者回答了那四個問題（四個答案原文記在這裡，之後不要再重新猜）：

1. 營運者對外寫 **Mokaair（個人經營者）**，不公開本名。
2. 所在地與準據法：**台灣，中華民國法律**。
3. 保存期限：用**依程式現況整理的版本**（所以文件裡的每個數字都對得上程式：
   分析原始事件 90 天、彙總 25 個月、備份保留最近 7 份、Email 連結 30 分鐘一次有效、
   登入最長 30 天；來源見 `config.py` 與 `database_admin/schemas.py`）。
4. 聯絡方式：**`support@mokaair.com` 對外、`support-noreply@mokaair.com` 寄系統信**。
   兩個信箱的分工與設定寫在 [`docs/contact-channels.md`](../../docs/contact-channels.md)。

這張任務建立時，四個頁面的內容還寫在 `page.tsx` 的 placeholder 裡；
`2026-09-09-site-experience-settings` 之後把它們換成 API 管理的文件，
所以 scope 改成實際存放內容的 `apps/api/app/site_pages/drafts`，頁面檔案不必動。

條文本身（blocks）是那張任務寫好的，這裡只補上五個 `requirements` 欄位，
並在 `/privacy` 與 `/contact` 各加一個 `mailto:` 連結。原本刻意留空的
「不要讓模型編造營運者事實」那條規則沒有被打破：填進去的五件事都是擁有者答覆的，
唯一還空著的 `effective_date` 正是發布閘門，initialize 之後仍然無法發布。

`send_mail` 只設 `From`，使用者回信會寄到不讀信的 `support-noreply@`。
修法另開 [[2026-09-10-account-mail-reply-to]]，因為當時 `apps/api/app/config.py`
被 `2026-09-09-configurable-catalog-review-run-call-limit` 佔著。

順手刪掉 `footerAboutBody` / `footerAboutLocales`：它們和那三個鍵一樣已經沒有任何
程式引用，關於頁的內容現在由 API 文件提供。
