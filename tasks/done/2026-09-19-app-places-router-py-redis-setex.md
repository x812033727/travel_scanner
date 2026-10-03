---
id: 2026-09-19-app-places-router-py-redis-setex
title: app/places/router.py 的 redis.setex 在 redis-py 8.1 已標 deprecated，改成 set(..., ex=)
status: done
priority: P3
area: api
owner: claude-opus-5-5-redis-set
claimed_at: 2026-10-02T14:30:09Z
created_at: 2026-09-19T11:33:47Z
completed_at: 2026-10-02T15:11:34Z
branch: claude/places-redis-set-ex
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

- [x] `app/places/router.py` 不再呼叫 `setex`，改成 `set(key, value, ex=seconds)`，語意相同（TTL 以秒計）。
- [x] `uv run pytest tests/test_google_places.py -q -W error::DeprecationWarning` 綠；全套 pytest 的 warnings 少一個。
- [x] 全 repo `grep -rn "\.setex(" apps/api/app` 沒有其他呼叫（有的話一併改，先把檔案加進 scope）。

## Steps

- [x] 改那一行；確認 key／TTL／值沒變。
- [x] 跑上面的測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_google_places.py -q -W error::DeprecationWarning
cd apps/api && uv run ruff check . && uv run mypy app
```

## Notes

- 2026-09-19 由 claude-fable-5-1 在 redis-py 8 升級時發現並開票；那次沒動這個檔。
- 2026-10-02 claude-opus-5-5-redis-set：認領時被 `2026-09-14-redis-py-8-migration` 與
  `2026-09-19-api-keys-in-logged-urls` 的 scope 擋下。兩張都掛在分支
  `claude/travel-scanner-pr-552-rpq36m`，那條分支的 PR（#561、#565 等）都已 MERGED，沒有開著的 PR
  用它，屬於過期認領，所以用 `--force` 接手。
- 改法：`redis.setex(cache_key, ttl, photo_uri)` → `redis.set(cache_key, photo_uri, ex=ttl)`。
  key（`places:photo-uri:<sha256>`）、值、TTL（`place_photo_cache_ttl_seconds`，秒）都沒變；
  `RedisError` 一樣吞掉。redis-py 8.1 的 `setex` 帶 `@deprecated_function`，每次呼叫發
  `DeprecationWarning`。
- 原本沒有任何測試在 `test_google_places.py` 裡走到照片快取的寫入；只有
  `test_public_provider_auth.py::test_authenticated_photo_miss_calls_google_once_then_uses_cache`
  走到，那條就是全套多出來的那個 warning。新增
  `test_photo_uri_cache_is_written_with_set_ex_and_the_configured_ttl`：TTL 用 900（不是預設
  3,600，寫死的 TTL 會露出來），記下 `set` 的呼叫並斷言恰好是 `set(key, uri, ex=900)`，再用
  fakeredis 的 `ttl()` 確認 Redis 真的收到 895–900 秒的期限；加上
  `filterwarnings("error::DeprecationWarning")`。改之前跑這條是紅的（`setex` 的
  DeprecationWarning 變成錯誤），改之後綠。
- 驗證：`pytest tests/test_google_places.py -q -W error::DeprecationWarning` 11 passed；
  `test_google_places.py`＋`test_public_provider_auth.py` 改前 15 passed、3 warnings（其一是
  `router.py:198` 的 setex），改後連同 `test_provider_request_limits.py`、
  `test_places_discover_contract.py`、`test_hotspot_places.py` 共 37 passed、2 warnings（剩下兩個是
  `<frozen importlib._bootstrap>` 的 `~` on bool，跟這張票無關）。全套 pytest 沒在本機跑（機器滿載，
  15 條測試要 7 分鐘），warnings 少一個以上述同一條測試的前後對照為證，CI 會跑全套。
- 其他 `setex`：整個 repo 的 Python（排除 `.venv`、`node_modules`）只有這一處，`apps/api/app`
  沒有別的呼叫，scope 不用加檔。
