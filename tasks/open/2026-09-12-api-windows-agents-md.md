---
id: 2026-09-12-api-windows-agents-md
title: 三個 API 測試在 Windows 開發機上必紅，AGENTS.md 叫大家推送前跑的就是這套
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-12T18:05:00Z
completed_at:
branch:
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
- [ ] 修的是測試本身的可攜性，不是放寬它要守的規則——`test_warning_codes` 那條規則仍然抓得到
      新寫進 `warnings` 的中文句子。

## Steps

- [ ] `test_warning_codes.py`：比對路徑改用 `as_posix()`（或把白名單改成 `Path`）。
- [ ] 加一筆驗證：故意在某個 `warnings.append` 寫中文，確認測試仍然會紅。
- [ ] `test_guides.py`：查 `old-deal` 在 sqlite 下為何算成 draft，多半在到期判斷的時間比較。

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
