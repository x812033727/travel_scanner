---
id: 2026-09-19-app-places-router-py-redis-setex
title: app/places/router.py 的 redis.setex 在 redis-py 8.1 已標 deprecated，改成 set(..., ex=)
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-19T11:33:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/places/router.py
  - apps/api/tests/test_google_places.py
---

# app/places/router.py 的 redis.setex 在 redis-py 8.1 已標 deprecated，改成 set(..., ex=)

## Why

`2026-09-14-redis-py-8-migration` 把 redis-py 升到 8.1 之後，`uv run pytest` 多了一個 DeprecationWarning：
`app/places/router.py:198` 用的 `redis.setex(...)` 在 8.1 標了 deprecated，下一個大版會拿掉。
現在只是警告，不影響行為，但升級票的 scope 沒有這個檔，所以另開一張。

## Definition of done

- [ ] `app/places/router.py` 不再呼叫 `setex`，改成 `set(key, value, ex=seconds)`，語意相同（TTL 以秒計）。
- [ ] `uv run pytest tests/test_google_places.py -q -W error::DeprecationWarning` 綠；全套 pytest 的 warnings 少一個。
- [ ] 全 repo `grep -rn "\.setex(" apps/api/app` 沒有其他呼叫（有的話一併改，先把檔案加進 scope）。

## Steps

- [ ] 改那一行；確認 key／TTL／值沒變。
- [ ] 跑上面的測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_google_places.py -q -W error::DeprecationWarning
cd apps/api && uv run ruff check . && uv run mypy app
```

## Notes

- 2026-09-19 由 claude-fable-5-1 在 redis-py 8 升級時發現並開票；那次沒動這個檔。
