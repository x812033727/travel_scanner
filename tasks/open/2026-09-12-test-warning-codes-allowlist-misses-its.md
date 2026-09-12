---
id: 2026-09-12-test-warning-codes-allowlist-misses-its
title: test_warning_codes allowlist misses its own files on Windows path separators
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T06:10:44Z
completed_at:
branch:
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

- [ ] Windows 上 `pytest tests/test_warning_codes.py` 全綠，且白名單的豁免仍然有效。
- [ ] Linux 上行為完全不變——真的把中文句子寫進 warnings 還是要被抓到。

## Steps

- [ ] 比對時用 `path.as_posix()`（或把白名單換成 `Path(...)`），不要比字串。
- [ ] 加一條斷言證明白名單至少命中一個檔，這樣以後路徑寫錯會被測試自己抓到。

## How to verify

`cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_warning_codes.py -q`
在 Windows 上跑；Linux 那一側由 CI 的 `api` job 覆蓋。

## Notes

2026-09-12 在修 2026-09-07-community-read-metric-concurrency 時撞到。確認是既有問題而不是
那次改動造成的：被指名的兩個檔（`app/crawlers/back_to_back.py`、
`app/providers/live_back_to_back.py`）一行都沒動過，而同一時間 main 的 `api` job 是綠的。
