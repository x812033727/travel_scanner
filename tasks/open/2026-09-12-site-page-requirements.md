---
id: 2026-09-12-site-page-requirements
title: 填入擁有者確認資訊，解鎖四個網站資訊頁
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-guides
claimed_at: 2026-09-12T01:56:04Z
created_at: 2026-09-12T01:55:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/site_pages/drafts
  - apps/api/tests/test_site_pages_drafts.py
  - apps/api/tests/test_site_pages.py
---

# 填入擁有者確認資訊，解鎖四個網站資訊頁

## Why

`/privacy`、`/terms`、`/about`、`/contact` 四頁的本體五語系都已經寫好（13／14／6／4 段），
但 `pending_requirements()`（`app/site_pages/service.py:61-70`）擋著發布，因為
`operator`、`location`、`contact`、`retention`、`legal` 與 `effective_date` 是空的。

`2026-09-11-privacy-data-map` 做完了可以從程式碼查的那一半（`docs/privacy-data-map.md`），
並把五個問題提給站主。站主已於 2026-09-12 全部答覆，這張票把答覆填進去。

## Definition of done

- [x] 五個欄位填入四個 slug × 五個語系，`about`／`contact` 只填它們宣告的三欄。
- [x] `effective_date` 維持空白，由站主在後台按發布的當天填。
- [x] 測試擋住三種回歸。

## 站主的決定（2026-09-12）

| 欄位 | 決定 |
| --- | --- |
| `operator` | 「Mokaair 站長（個人營運，非公司法人）」，不具名 |
| `location` | 台灣 |
| `contact` | support@mokaair.com |
| `retention` | 照程式現況據實寫，不另訂期限 |
| `legal` | 只寫適用中華民國法律，不指定管轄法院 |
| 生效日期 | 留空 |

三處是依站主決定推導、而非他逐字指定的，已在提交前逐一告知並由他保留：
`location` 的跨境傳輸句（選台灣＝適用個資法，§8 把利用地區列為應告知事項，而
MiniMax 在 `api.minimaxi.com`、S3 在 `us-east-1`）、`contact` 的防詐提醒、
`retention` 第三段「刪除後仍留存什麼」。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && \
  uv run pytest tests/test_site_pages.py tests/test_site_pages_drafts.py -q
```

填完後 `pending_requirements()` 對全部 20 份文件應該只回 `["effective_date"]`。

## Notes

**測試的前提被反轉了，不是刪掉。** `test_site_pages_drafts.py` 原本有
`test_no_locale_ships_a_filled_requirement`（我在 #410 寫的），前提是「站主還沒給」。
站主給了之後改成兩個更強的：每頁只帶它宣告的欄位（`about` 帶 `retention` 會失敗），
以及 `effective_date` 絕不進版控且閘門只剩它。

`tests/test_site_pages.py` 既有的 `test_all_twenty_initial_documents_...` 也編碼了同一個
前提，包含 `assert "@" not in document.model_dump_json()`——那是防止 email 意外混進草稿的
守門。現在刻意公開一個地址，所以改成「只允許 support@mokaair.com 這一個」，守門的意圖
保留。三種回歸都先植入確認會失敗才留下。

**這只對還沒初始化的環境生效。** `initialize_pages()` 用 `on_conflict_do_nothing`
（`service.py:201-230`），正式站若已初始化，要在後台逐語系編輯並發布。四頁 × 五語系＝
20 次發布操作，每次都要填生效日期、打勾確認並寫原因。

**頁尾那三個 message 鍵還不能刪。** `2026-09-06-legal-content-from-owner` 的 DoD 要求刪掉
`footerPendingTitle`／`footerPendingBody`／`footerContactBody`，但那要等四頁在正式站真的
發布之後——未發布的頁面仍靠它們顯示說明，先刪會變空白。
