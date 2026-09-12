---
id: 2026-09-11-privacy-data-map
title: 從程式碼盤點個資處理，供擁有者填寫隱私權頁的確認資訊
status: done
priority: P1
area: docs
owner: claude-opus-5-guides
claimed_at: 2026-09-11T23:32:27Z
created_at: 2026-09-11T23:32:27Z
completed_at: 2026-09-12T01:55:42Z
branch: claude/privacy-data-map
depends_on: []
scope:
  - docs/privacy-data-map.md
  - apps/api/app/site_pages/drafts
  - apps/api/tests/test_site_pages_drafts.py
---

# 從程式碼盤點個資處理，供擁有者填寫隱私權頁的確認資訊

## Why

`/privacy` 的本體其實已經寫好了——五個語系各 13 個區塊，而且寫得很克制，通篇只描述
機制，把每一個承諾都推給「本頁的確認資訊」。卡住發布的是
`pending_requirements()`（`apps/api/app/site_pages/service.py:61-70`）要求的五個欄位
與 `effective_date`。

那五個欄位裡，`retention` 有一半不是法律判斷，是「這套程式實際上做了什麼」，而那個
答案散在 repo 裡沒有人整理過。`2026-09-06-legal-content-from-owner` 說「這四個問題不能
從程式碼裡查，只能問人」——對 operator／location／contact／legal 是對的，但對
retention 只對了一半：期限是承諾要人定，**現況是事實，可以查**。

這張票做可以查的那一半，好讓擁有者回答時是在確認事實而不是猜。

## Definition of done

- [x] `docs/privacy-data-map.md`：蒐集什麼、存哪裡、留多久、刪帳號實際做什麼、
      哪些第三方拿得到，每一條標到檔案與行號。
- [x] 現有五語系草稿與程式不符的地方修掉。
- [x] 補測試擋住兩種回歸。
- [x] 五個只有擁有者能回答的問題整理給站主。**這張票到此為止，不代寫政策條文。**

## Steps

- [x] 盤點並逐條核對（有一條初稿的主張核對後撤回，見文件第二節）
- [x] 修正草稿三處事實錯誤
- [x] 測試：五語系 `privacy` 草稿的區塊結構一致
- [x] 測試：稽核紀錄若把使用者識別碼寫在非 `user:` target 底下，清除時會漏掉

## How to verify

```bash
cd apps/api && uv run pytest tests/ -k "site_pages or privacy" && uv run ruff check . && uv run mypy app
npm run check:i18n
```

## Notes

**不代寫政策條文是刻意的**，沿用 `2026-09-06-legal-content-from-owner` 的立場：
生出來的條文會被讀者當成承諾，而那個承諾沒有人做過。這張票只提供事實。

**初稿有一條主張核對後是錯的。** 自動盤點說稽核紀錄只做了部分去識別化、政策該加但書；
掃過全部 95 個 `AdminAuditLog(...)` 寫入點之後，每一個寫入 email 或使用者識別碼的都用
`target=f"user:{user.id}"`，清除時都會被涵蓋。照抄的話，政策會對讀者**少**承諾一件它
其實做到的事。留下的是另一回事：那靠慣例維持、沒有機制，所以補一個測試。

**一件超出這張票、需要產品決定的事**：`affiliates/router.py:376-381` 把
`uuid5(NAMESPACE_URL, f"...:{user.id}:...")` 當 `sub_id` 送給聯盟夥伴做跨站歸因。
`service.py:231-234` 只對 Klook 做了防護（「never expose a member/trip-derived ID」），
KKday／Agoda／Trip.com／Airalo／Booking／Skyscanner 只要後台樣板含 `{sub_id}` 都會拿到。
要嘛在政策裡揭露，要嘛把 Klook 那條防護套用到全部——後者是另一張票。

**改 `drafts/*.json` 只對還沒初始化的環境生效**：`initialize_pages()` 用
`on_conflict_do_nothing`（`service.py:201-230`）。已初始化的環境要在後台逐語系編輯。

**三處修正的內容**（`tests/test_site_pages_drafts.py` 擋住其中兩處回歸）：

1. **刪除帳號後留下什麼。** 英文版原本寫「Retained historical accounting links and delivered
   conversations use a **de-identified identity**」——帳本那半是**錯的**：`erase_account()`
   完全沒碰 `usage_accounts`／`usage_ledger`／`usage_reservations`，它們仍帶著 `user_id`。
   改成據實說明：帳號紀錄本身保留、Email 換成無法聯繫的代碼，為核對帳務保留的紀錄仍帶
   該帳號的關聯。
2. **未存檔的草稿會留在瀏覽器。** 新增一則說明，指出共用裝置上要留意。
3. **「雜湊識別」其實是以網站金鑰計算的 HMAC。** 一併補上原始 IP 只作為計算輸入、
   不會被保存，且該值逐日更換——這幾件對讀者是有利的事實，原本沒講。

兩個測試都**先植入回歸確認會失敗**才留下：抽掉 ko 的一則項目、把一筆帶 email 的稽核
寫入改成非 `user:` target，各自都會失敗並指出確切的檔案與行號。

**收尾（#410 已合併，commit c488bc0）。** 五個問題已於 2026-09-12 提給站主並全部得到答覆：

| 欄位 | 站主的決定 |
| --- | --- |
| `operator` | 「Mokaair 站長（個人營運）」，不具名 |
| `location` | 台灣 |
| `contact` | support@mokaair.com |
| `retention` | 照程式現況據實寫，不另訂期限 |
| `legal` | 只寫適用中華民國法律，不指定管轄法院 |
| 生效日期 | 留空，由站主在後台按發布的當天填 |

站主另外決定**不開啟 Google／Apple 社群登入**（`auth_*_enabled` 三個本來就預設 False，
`social-login-buttons.tsx:47,65` 在沒有可用供應商時整塊不渲染，所以不需要任何程式變更）。
那並不免除 `operator` 欄位——發布閘門與個資法 §8 各自要求它，與登入方式無關。

填入的工作另開 `2026-09-12-site-page-requirements`，因為它動的是同一個 drafts 目錄，
而這張票的 scope 押著它。
