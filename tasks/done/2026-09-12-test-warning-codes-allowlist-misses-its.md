---
id: 2026-09-12-test-warning-codes-allowlist-misses-its
title: test_warning_codes allowlist misses its own files on Windows path separators
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:32:16Z
created_at: 2026-09-12T06:10:44Z
completed_at: 2026-09-19T08:39:41Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/tests/test_warning_codes.py
---

# test_warning_codes allowlist misses its own files on Windows path separators

## Why

`test_no_new_warning_is_written_as_a_finished_sentence` 掃 `Path("app").rglob("*.py")`，
再用 `row[0] not in {path for path, _ in allowed}` 濾掉白名單。白名單寫的是
`app/crawlers/back_to_back.py` 這種正斜線字串，而 Windows 上 `str(path)` 給的是
`app\crawlers\back_to_back.py`，比不中，於是三個**刻意被豁免**的費率實驗室檔案在 Windows
上全被當成違規、測試必紅。Linux CI 不受影響。

代價是每個在 Windows 上驗 API 的人都要先判斷一次「這條紅是不是我弄的」：本機跑整套時它是
唯一的紅（2026-09-12：3335 passed / 180 skipped / 1 failed）。

## Definition of done

- [x] Windows 上 `pytest tests/test_warning_codes.py` 全綠，且白名單的豁免仍然有效。
- [x] Linux 上行為完全不變——真的把中文句子寫進 warnings 還是要被抓到。

## Steps

- [x] 比對時用 `path.as_posix()`（或把白名單換成 `Path(...)`），不要比字串。
- [x] 加一條斷言證明白名單至少命中一個檔，這樣以後路徑寫錯會被測試自己抓到。

## How to verify

`cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_warning_codes.py -q`
在 Windows 上跑；Linux 那一側由 CI 的 `api` job 覆蓋。

## Notes

2026-09-12 在修 2026-09-07-community-read-metric-concurrency 時撞到。確認是既有問題而不是
那次改動造成的：被指名的兩個檔（`app/crawlers/back_to_back.py`、
`app/providers/live_back_to_back.py`）一行都沒動過，而同一時間 main 的 `api` job 是綠的。

### 2026-09-19 修法（claude-fable-5-1）

`found.add((path.as_posix(), …))`：比對用的字串永遠是正斜線，和白名單一致；Linux 上結果不變
（測試綠），Windows 上三個豁免檔會被正確濾掉。沒有 Windows 機器可以親自跑，但 `as_posix()` 在兩個
平台上的輸出都是 `app/crawlers/back_to_back.py` 這種形式，這正是白名單寫的字串。
