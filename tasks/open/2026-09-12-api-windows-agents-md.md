---
id: 2026-09-12-api-windows-agents-md
title: 三個 API 測試在 Windows 開發機上必紅，AGENTS.md 叫大家推送前跑的就是這套
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:34:56Z
created_at: 2026-09-12T18:05:00Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/tests/test_warning_codes.py
  - apps/api/tests/test_guides.py
---

# 三個 API 測試在 Windows 開發機上必紅，AGENTS.md 叫大家推送前跑的就是這套

## Why

CI 是綠的，但在 Windows 開發機上 `uv run pytest` 一定看到三筆紅的。AGENTS.md 要求推送前先跑
這套檢查，所以每個在 Windows 上工作的人都得先自己判斷「這三筆是不是我弄壞的」，判斷錯就會去
改沒壞的東西。2026-09-13 在 `13f654ad`（當時的 main）上量到的，與當時進行中的變更無關：把變更
stash 掉重跑，同樣三筆失敗。

**`test_warning_codes.py::test_no_new_warning_is_written_as_a_finished_sentence` 的原因已經查到**：
白名單寫的是 POSIX 路徑

```python
allowed = {
    ("app/crawlers/back_to_back.py", "stale rate"),
    ...
}
...
unexpected = [row for row in sorted(found) if row[0] not in {path for path, _ in allowed}]
```

而 `found` 裡的 `str(path)` 在 Windows 上是 `app\crawlers\back_to_back.py`，所以白名單永遠對不
上，三個刻意保留的例外每次都被當成新違規報出來。用 `path.as_posix()` 就好。

`test_guides.py` 兩筆（`test_an_expired_notice_keeps_its_page_but_leaves_the_listings[sqlite]`、
`test_the_admin_listing_filters_by_status_and_reports_facets[sqlite]`）原因**尚未查明**，症狀是
`old-deal` 這筆的狀態算成 `draft` 而不是 `expired`。只有 sqlite 參數化那組會紅，CI 是綠的，所以
先懷疑時區或 naive datetime 比較（這台機器是 UTC+8）。

## Definition of done

- [ ] 在 Windows 開發機上 `pytest tests/test_warning_codes.py tests/test_guides.py` 全綠。
- [x] 修的是測試本身的可攜性，不是放寬它要守的規則——`test_warning_codes` 那條規則仍然抓得到
      新寫進 `warnings` 的中文句子。（2026-09-19 用 scratch 複本驗過，見筆記）

## Steps

- [x] `test_warning_codes.py`：比對路徑改用 `as_posix()`（或把白名單改成 `Path`）。（本分支已改）
- [x] 加一筆驗證：故意在某個 `warnings.append` 寫中文，確認測試仍然會紅。（一次性驗證，結果在筆記）
- [x] `test_guides.py`：查 `old-deal` 在 sqlite 下為何算成 draft，多半在到期判斷的時間比較。（查明了，而且 #442 已修）

## How to verify

```bash
cd apps/api
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m pytest tests/test_warning_codes.py tests/test_guides.py -q
```

Linux/CI 也要照跑一次，確認修完沒有反過來把 CI 弄紅。

## Notes

在 Windows 上跑整套的指令（另有三個檔在 Windows 上連收集都不行，
`test_deployment_center.py` 用了 `socketserver.UnixStreamServer`，另兩個要真的
PostgreSQL／Redis）：

```bash
cd apps/api && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m pytest -q \
  --ignore=tests/test_deployment_center.py \
  --ignore=tests/test_integration_postgres_redis.py \
  --ignore=tests/test_deployments_integration.py
```

2026-09-13 的結果：3511 passed、193 skipped、3 failed（就是本票這三筆）。

### 2026-09-19 done in repo (claude-fable-5-1)

**`test_warning_codes.py`**：本分支已經是 `path.as_posix()`（測試裡有註解說明 Windows 的反斜線）。
規則沒被放寬：把 `apps/api/app` 複製到 scratch 目錄、在複本的 `app/warnings.py` 末尾加一行
`warnings.append("路線服務尚未啟用")`、以該目錄為 cwd 跑同一支測試，
`test_no_new_warning_is_written_as_a_finished_sentence` 如預期紅掉並點名 `app/warnings.py:58`。
repo 裡沒有動任何 `app/` 檔案，所以沒有留下永久的反向測試；既有的第二個 assert
（`found` 的檔案集合必須恰好等於三個白名單檔案）本來就會在掃描器「什麼都看不到」時失敗，
Windows 那次也是它連同第一個 assert 一起紅的。

**`test_guides.py` 兩筆的原因（已查明）**：票裡量到的 `13f654ad` 上，
`tests/test_guides.py` 第 357／377／536 行用的是 `date.today()`（**本機**日期）算 `valid_until`，
而 `app/guides/publication.py` 的 `today()` 從那時起就是 `datetime.now(UTC).date()`，
`article_is_live`／`article_status`／`admin_status_expression` 的 cutoff 都是它。UTC+8 的機器在本地
00:00–08:00 之間，本地日期比 UTC 多一天：`date.today() - 1 天` 剛好等於 UTC 的今天，
`valid_until < cutoff` 不成立、`expired` 落空；`old-deal` 從沒發布過，就掉進 CASE 的 `else_="draft"`，
第一筆則是 `expired` 回 `False`、文章沒有離開列表。這張票是 2026-09-12T18:05Z 開的，
也就是台北 02:05，正好在那個窗口裡。`test_publishing_an_already_expired_article_is_refused` 用的是
`days=2`，UTC 今天減一仍然小於 cutoff，所以它一直是綠的——這就是為什麼只紅兩筆。
跟 sqlite 的日期存法或 naive／aware datetime 無關，PostgreSQL 一樣會紅；「只有 sqlite 那組紅」是因為
Windows 上沒有 `RUN_INTEGRATION_TESTS=1`，postgresql 參數化那組被 skip 了。

**已經修好，不需要再改檔案**：`d3e474ab`（#442，2026-09-13 03:04Z 合併，就在量到失敗之後幾小時）
順手把三處改成 `from app.guides.publication import today`（commit 訊息：「tests/test_guides.py 的
兩個過期測試改用 UTC 的 today()，本地 00:00–08:00 不再 flake」）。本分支 HEAD 的 `tests/test_guides.py`
第 40 行 import、第 405／425／584 行都已是 `today()`；檔案裡沒有剩下的 `date.today()`，也沒有
`valid_until=today()`（今天到期）這種會跨 UTC 午夜 flake 的案例，測試與程式現在共用同一個時鐘。
`tests/` 裡其他 `date.today()`（trips、flights、planner 的「未來 30–90 天」）只需要「在未來」，
不跟 UTC 日期比大小，與這個問題無關。

**驗證（Linux；現在是 09:3x Z，`Asia/Taipei` 與 UTC 同一天，所以另外用 POSIX 字串把
「本地日期 ≠ UTC 日期」兩個方向都跑過）**：

```
cd apps/api
uv run pytest tests/test_warning_codes.py tests/test_guides.py -q                # 97 passed, 86 skipped
TZ=Asia/Taipei uv run pytest tests/test_warning_codes.py tests/test_guides.py -q # 97 passed, 86 skipped
TZ=Etc/GMT+12  uv run pytest tests/test_warning_codes.py tests/test_guides.py -q # 97 passed, 86 skipped（本地日期落後 UTC 一天）
TZ=XXX-20 uv run pytest tests/test_guides.py -q \
  -k "sqlite and (expired_notice or filters_by_status)"                           # 2 passed（本地日期超前 UTC 一天，即台北 02:00 的情境）
uv run ruff check tests/test_warning_codes.py tests/test_guides.py               # All checks passed!
```

**用重現確認原因**：把 HEAD 的 `tests/test_guides.py` 複製到 scratch 目錄、只把那三處 `today()` 改回
`date.today()`（等於 `13f654ad` 的寫法），在 `TZ=XXX-20`（本地日期超前 UTC 一天）下跑同兩筆：
恰好就是這兩筆紅，訊息與票裡一樣——`{'old-deal': 'draft'} != {'old-deal': 'expired'}`、
`assert article.json()["expired"] is True` 得到 `False`；HEAD 的檔案在同一個 TZ 下 2 passed。

Definition of done 第一條要在 Windows 開發機上跑才能打勾，這裡沒有 Windows，狀態先放 `review`；
Windows 上照「How to verify」跑一次綠了就 `done`。
