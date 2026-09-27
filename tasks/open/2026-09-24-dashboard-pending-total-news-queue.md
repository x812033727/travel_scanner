---
id: 2026-09-24-dashboard-pending-total-news-queue
title: 後台總覽的「待處理」算進新聞待審，卻只連到景點審核佇列
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-24T04:51:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-dashboard.tsx
  - apps/web/components/admin-dashboard.test.tsx
  - apps/web/components/admin-partial-payload.test.tsx
  - apps/web/lib/admin-domains-messages
---

# 後台總覽的「待處理」算進新聞待審，卻只連到景點審核佇列

## Why

`/admin` 總覽第一排有一張「待處理」卡（`apps/web/components/admin-dashboard.tsx:44`）。它顯示 `pending_total`，點下去會到 `/admin/hotspots?tab=review&section=manual&status=pending`，也就是景點人工審核佇列。

`pending_total` 在 `apps/api/app/admin/operations_service.py:184-194` 加總六項。PR #694（2142f228）在 `:192` 加進了 `news_review_pending`，算的是狀態為 `manual_review`、`shadow_review` 或 `failed` 的 `NewsCandidate`（`:168-171`）。可是景點佇列只列 `TravelHotspot`，新聞候選不會出現在那裡。總覽下方的「內容目錄」（`admin-dashboard.tsx:48-60`）也只有景點、美食、飯店三張卡。所以算進總數的新聞候選，在總覽上沒有任何一條路點得到，只剩側欄「AI 自動新聞」的徽章（`operations_service.py:61-64`）。#694 改了 `operations_service.py` 和側欄，但沒有改 `admin-dashboard.tsx`。

同一張卡從 #377（59c86438）起就把料理、店家、文章（`guides_pending`）、飯店的待審也加進總數，再連到景點佇列。這個不一致一直都在，只是那四項在下方各有自己的佇列連結（`admin-dashboard.tsx:50-58`），總覽上還找得到。新聞是唯一沒有入口的一項。

有一個容易被誤導的地方：`/admin/dashboard` 回傳的 `quick_actions`（`apps/api/app/admin/dashboard_router.py:108-140`）裡也沒有新聞，但網頁根本不讀這個欄位（`admin-dashboard.tsx:14` 的型別只有 `counts` 與 `can_deploy`）。總覽上的數字來自 bootstrap 的 `pending_counts`，它在 `:29-30` 蓋過 `/admin/dashboard` 的 counts，本來就帶著 `news_review_pending`。所以這張票不用改 API。

影響：新聞影子期（`min_shadow_days` 預設 14 天）裡每小時掃一次。通過的候選停在 `shadow_review`，失敗的停在 `failed`，只有人工處理才會離開，所以 `news_review_pending` 會一直累積，很快就會變成「待處理」裡最大的一塊。管理者看到「待處理 N」，點進去卻只有幾筆景點，會以為數字錯了，或以為佇列壞了。

決定：`pending_total` 繼續當跨領域的總數，它回答的是「還有多少事等人處理」。但算進去的每一項，都要在總覽上有一個點一下就到的佇列連結，「待處理」卡也不要再裝成景點佇列。否決的做法：

- 把 `news_review_pending` 從 `pending_total` 拿掉：這只是把新聞藏起來，料理、飯店也不在景點佇列的老問題還是在。
- 把卡改名成「景點待審」：會和下方景點卡重複，總數也就沒了。

## Definition of done

- [ ] `/admin` 總覽上，`pending_total` 的每一個組成（景點、文章、料理、店家、飯店、新聞）都有自己的佇列連結，顯示自己的數字，連到自己的工作區。新聞連到 `/admin/news`，數字是 `news_review_pending`。
- [ ] 「待處理」卡不再帶人到只有景點的佇列。它要嘛連到總覽上列出全部組成的佇列區，要嘛不是連結、直接列出組成。卡上的數字等於畫面上各組成佇列數字的和，沒有 bootstrap 時也一樣，不再退回只顯示 `hotspots_pending`。
- [ ] 導覽裡沒有 `/admin/news` 的角色看不到新聞佇列（沿用 `canVisit`），頁面上也不會因此出現壞連結。
- [ ] `admin-dashboard.test.tsx` 有測試釘住上面三點；`admin-partial-payload.test.tsx` 的「每一個待審數字都有自己的佇列」清單也包含新聞。

## Steps

- [ ] 在 `admin-dashboard.tsx` 的 `domains`（`:48-60`）加入新聞，做成一張卡或一列佇列都可以：`count: "news_review_pending"`、href 用 `/admin/news`，並用 `canVisit` 過濾。數字直接用 bootstrap 的 `pending_counts`（`:29-30` 已經合進 `counts`），不必改 API，也不要去改 `quick_actions`。
  - 「內容目錄」的格線是 `xl:grid-cols-3`（`:71`），加第四張卡要一起調版面。
  - 新聞沒有「總數」。`count(domain.total)` 遇到沒有的 key 會顯示「總數 · —」，所以 `total` 要改成可省略，不要硬塞一個假的。
  - 卡片標題可以直接用 `adminNewsCopy(locale).nav`（`apps/web/lib/admin-news-copy.ts`，側欄已經在用）。
- [ ] 新佇列的標籤（例如「新聞待審」）加進 `apps/web/lib/admin-domains-messages/` 的五個語系檔。五個檔的 key 是否一致，由 `apps/web/lib/admin-workspace-navigation.test.ts:113-120` 和 typecheck 檢查（`check:i18n` 不讀這個目錄）。
- [ ] 「待處理」卡（`:44`）的 href 改成總覽上佇列區的錨點，佇列區要補一個 id；另一個做法是這張卡不做連結，改在旁邊列出組成。
  - `:65` 的可見性過濾要改成「任一組成佇列看得到就顯示」，不能再拿景點網址來判斷。
  - 用 next-intl 的 `Link` 包錨點時，要確認渲染出來的 href 真的是錨點，沒有被加上語系前綴。
- [ ] 卡上的值改成畫面上可見佇列數字的和；或者繼續用 `pending_total`，但把 `:44` 的 `aliases: ["hotspots_pending"]` 拿掉。二選一，並在 Notes 寫下選了哪個。
- [ ] 補測試（`admin-dashboard.test.tsx`）：
  - bootstrap 帶 `pending_counts: { pending_total: 9, hotspots_pending: 2, news_review_pending: 7 }`，navigation 裡有 news 項。斷言「新聞待審 7」連到 `/admin/news`，「待處理」卡的 href 不是 `/admin/hotspots?...`，卡上數字是 9。
  - navigation 裡沒有 news 的角色看不到新聞佇列。
- [ ] 在 `admin-partial-payload.test.tsx:32-70` 那張清單加上新聞一列，mock 的 counts 補上 `news_review_pending`。

## How to verify

先在現在的 main 上重現：

```bash
grep -n "news_review_pending" apps/api/app/admin/operations_service.py   # 63 側欄徽章；171、192 算進 pending_total
grep -n "pending_total" apps/web/components/admin-dashboard.tsx          # 44：連到景點人工審核佇列
grep -c "news" apps/web/components/admin-dashboard.tsx                   # 目前是 0，總覽上沒有新聞入口
```

修好之後：

```bash
npm run test:web -- admin-dashboard admin-partial-payload admin-workspace-navigation
npm run lint:web && npm run check:i18n && npm run typecheck:web
```

點擊流程（本機，或部署後用管理者帳號）：

1. 確認至少有一筆新聞候選停在 `manual_review`、`shadow_review` 或 `failed`。
2. 開 `/zh-TW/admin`。「待處理」的數字要等於下方各佇列數字的和。
3. 點「待處理」：要看到全部組成的佇列，不是跳到 `/admin/hotspots`。
4. 點「新聞待審」：要到 `/zh-TW/admin/news` 的人工審查頁。

## Notes

- 2026-09-23 看 PR #694 時發現，2026-09-24 在 main（692dcf5a）上重新確認還在。
- 這張和 `2026-09-24-keep-every-news-review-item-reachable` 有關，但沒有重疊。那張修的是 `/admin/news` 清單只取最新 100 筆（`admin-news-workspace.tsx:101`、`:122`），這張修的是總覽沒有入口。那張落地之前，從總覽點進 `/admin/news`，還是可能看不到較舊的待審項。那張加上網址篩選之後，把這裡的新聞連結改指向審查篩選。
- `/admin/news` 的「待審」只算 `manual_review` 加 `shadow_review`，「失敗」另外算（`apps/api/app/news_automation/service.py:827-828`）。`news_review_pending` 則把三種加在一起。所以總覽的標籤要寫清楚包含失敗，不然就拆成兩個數字。實作時決定，並把決定寫在這裡。
- `tools/e2e-runtime-api.mjs` 的假導覽（`:83-105`）沒有 news 項，假 `pending`（`:131`）也沒有 `news_review_pending` 和 `pending_total`。所以在 e2e 裡，新聞佇列會被 `canVisit` 藏起來。要在 e2e 驗這張，得先補那邊，但那不在本票 scope。那個檔案在 `2026-09-09-site-experience-settings` 的 scope 裡，要補就另開票，或在那張票寫明。
- `apps/web/e2e/readability.spec.ts:377-387` 逐一檢查總覽各佇列連結的對比度，目前沒有新聞。要補也不在本票 scope：那個檔案在 `2026-09-09-site-experience-settings` 和 `2026-09-07-mokaair-community-web` 的 scope 裡。
- 如果實作時還是決定把新聞從 `pending_total` 拿掉，就要改 `apps/api/app/admin/operations_service.py` 和 `apps/api/tests/test_admin_operations.py`。這是 scope 變更，要先在這裡寫理由；而且 `2026-09-09-site-experience-settings` 的 scope 也含 `operations_service.py`，動手前確認那張沒有人在做。
- 2026-09-24（task 2026-09-24-make-the-news-review-queue-actionable）：`news_review_pending` 已經不算 `failed`，只算 `manual_review`＋`shadow_review`，和 `/admin/news` 的「待審查」清單、頁首「等你判斷」卡一致；失敗的候選移到新的「需重寫」清單。上面 Notes 說的「總覽標籤要寫清楚包含失敗」因此不用了。「待審查」的連結是 `/admin/news?queue=review`（預設就是它）。
