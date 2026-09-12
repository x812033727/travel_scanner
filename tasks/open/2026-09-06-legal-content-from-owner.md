---
id: 2026-09-06-legal-content-from-owner
title: 隱私權政策、服務條款與聯絡方式的內容要由擁有者提供
status: review
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-12T04:59:05Z
created_at: 2026-09-06T19:44:10Z
completed_at:
branch: claude/legal-content-handling-71d3a2
depends_on: []
scope:
  - apps/web/app/[locale]/privacy/page.tsx
  - apps/web/app/[locale]/terms/page.tsx
  - apps/web/app/[locale]/contact/page.tsx
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
- [x] 三個頁面都不再顯示 `footerPendingTitle` / `footerPendingBody` / `footerContactBody`，
      而且那三個 message 鍵被刪掉（留著就會爛掉）。

前三格要等正式站發布才能打勾；條文本身已經寫好並經站主批准，見下一節。

## Steps

- [x] **先問擁有者這四件事**，其他都做不了：
      1. 對外的法律主體名稱（公司或個人）與所在地，決定適用哪一國的法規。
      2. 可以公開的聯絡方式（email 或表單收件處）。
      3. 資料保存期限與刪除帳號的處理方式。
      4. 是否已經有法務或範本要沿用。
      → 2026-09-12 在 [[2026-09-11-privacy-data-map]] 問完、[[2026-09-12-site-page-requirements]]
      填入五語系草稿（#410、#412）。
- [x] 依答覆撰寫兩份文件，**由人審過**才上線。
      → 五語系條文在 #380 寫好、#410 逐條對照程式碼修正三處、#412 填入確認資訊並經站主
      逐字批准（「文字沒問題」）。上線動作見下一節。
- [x] 把三個頁面的 placeholder 換掉，刪掉那三個 message 鍵，`check:i18n` 會確認五個語系同步。
      → placeholder 在 #380 改成後台管理的資料庫文件；三個鍵連同同樣已無引用的
      `footerAboutBody`／`footerAboutLocales` 在這張票刪掉。

## 剩下的一步：正式站發布（2026-09-12 盤點，claude-fable-5-1）

查到的事實：

- 正式站 2026-09-12 03:32 部署到 `3230a339`，包含 #410 與 #412，API 容器裡的
  `drafts/*.json` 就是站主批准的版本。
- `site_pages` 表是**空的**（唯讀 psql 查過）：四頁從未初始化。所以後台「建立缺少的五語系
  初稿」一鍵就會用批准版建立 20 筆，不需要手動貼；前一張票擔心的「已初始化要逐語系貼」
  不會發生。
- 三個頁尾鍵在 #380 之後沒有任何程式引用（含動態組鍵）；未發布狀態的文案來自
  `admin.json` 的 `sitePages.unpublished`，刪鍵不會讓頁面變空白。
- 20 份草稿結構一致（privacy 13 / terms 14 / about 6 / contact 4 個區塊，五語系相同），
  `pending_requirements()` 只剩 `effective_date`。
- mokaair.com 的 MX 指向 Hostinger（mx1／mx2.hostinger.com）。**support@mokaair.com 這個
  信箱是否已建立，程式碼與 DNS 都看不出來**，發布前站主要確認它收得到信。

後台操作（`/zh-TW/admin/site-pages`，需要 `settings.manage`）：

1. 按一次「建立缺少的五語系初稿」。
2. 每個「資訊頁 × 文件語言」：填「生效日期」→「儲存草稿」→「發布」→ 填「異動原因」、
   勾「我已核對內容與營運資料」→「確認發布」。發布鈕在有未儲存變更或尚待確認欄位非空時
   是停用的，順序不能反。
3. 隱私權政策與服務條款各五語系共 10 次；關於 Mokaair 與聯絡我們再 10 次。
4. 發布後開 `/zh-TW/privacy`、`/en/terms`、`/ja/contact` 確認不再是「內容準備中」，
   再把這張票 `done`。

模型做不到的部分：auto mode 擋掉正式站的 psql `UPDATE`／`INSERT`、把腳本送進 api 容器、
以及從瀏覽器頁面對 admin API 發 `fetch`；唯一開放的路是站主登入後由模型驅動後台表單，
而 2026-09-12 Claude in Chrome 沒有連線。所以這 20 次要嘛站主自己按，要嘛登入後再叫模型按。

## How to verify

```bash
npm run check:i18n && npm run test:web -- site-footer
```

開 `/zh-TW/privacy`、`/en/terms`、`/ja/contact`，確認顯示的是真的內容而不是待補說明。

## Notes

- 已經知道的事實：整個 repo 目前沒有任何 email、法律主體名稱或對外聯絡方式，
  所以這四個問題不能從程式碼裡查，只能問人。（2026-09-12 已問完，答覆見上。）
- 頁尾與四個頁面的版位已經做好，這張任務只換內容，不動版面。
- **不要請模型代寫這兩份文件然後直接上線。** 那正是上一張任務刻意沒做的事。
- 這張票的 `scope` 是 09-06 寫的；自 #380 起 `/privacy` 等 `page.tsx` 只是薄薄一層讀資料庫，
  真正的文字在 `apps/api/app/site_pages/drafts/`，改文字要走那個目錄（和它自己的票）。

2026-09-12 窄幅釋放（五語系 navigation-only）：這張票的 navigation.json 步驟已在 `fc274a1d`（#426）合併並打勾，
剩下的工作全在後台與站主手上，不再需要這五個檔案。依 `2026-09-07-merchant-style-discovery` 的先例，
只把 `apps/web/messages/{en,ja,ko,zh-CN,zh-TW}/navigation.json` 五個精確 scope 釋放給
`2026-09-12-lifestyle-section-and-guides-relabel`（同一個 owner 身分 `claude-fable-5-1`）；其餘三個 page.tsx 仍歸這張票。
