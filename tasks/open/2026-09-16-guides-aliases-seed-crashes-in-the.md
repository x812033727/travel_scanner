---
id: 2026-09-16-guides-aliases-seed-crashes-in-the
title: guides-aliases-seed crashes in the production image
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:32:15Z
created_at: 2026-09-16T05:39:18Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/aliases.py
  - apps/api/tests/test_guides_aliases.py
---

# guides-aliases-seed crashes in the production image

## Why

`docs/article-architecture.md` 與 #531 的部署順序都要求部署後跑
`python -m app.cli guides-aliases-seed --dry-run` → 正式跑。2026-09-16 部署 #531 後在正式站執行，
不帶參數就直接崩：

```
File "/app/app/guides/aliases.py", line 35, in default_terms_file
  return Path(__file__).resolve().parents[4] / "docs" / "ai-terms-series" / "aliases.json"
IndexError: 4
```

`parents[4]` 是照 repo 版面推 repo 根目錄（`repo/apps/api/app/guides/aliases.py` → `parents[4]` 是 repo 根）。
正式映像把套件放在 `/app/app/guides/aliases.py`，往上只有 `/app/app/guides`、`/app/app`、`/app`、`/`
四層，`parents[4]` 必定 `IndexError`。

這和 `default_terms_file` 自己的 docstring 互相矛盾：它寫「a container without `docs/` seeds the
series keywords only」，`term_aliases` 也備好了 `if not path.is_file(): return []` 的優雅路徑 ——
但那行永遠到不了，因為算路徑當下就炸了。`default_keywords_file`（`aliases.py:86`）是同一個寫法，
同樣的問題。

測試看不到：本機 repo 版面下 `parents[4]` 正常，`test_guides_aliases.py` 不是 monkeypatch 掉
`default_keywords_file`，就是在檔案不存在時 `pytest.skip`，`test_guides_search.py:549` 也是 monkeypatch。
沒有一個測試在「路徑算不出來」的版面下呼叫過這兩個函式。

## Definition of done

- [x] 在正式映像裡 `python -m app.cli guides-aliases-seed --dry-run` 不帶檔案參數也能跑完，
      沒有 `docs/` 時照 docstring 說的只種系列關鍵字，不丟例外。
- [x] 操作者自己指定、但指錯的路徑仍然是錯誤（`FileNotFoundError`），這個行為不能被一起改掉。

## Steps

- [x] `default_terms_file` 與 `default_keywords_file` 改成算不出 repo 根時回一個必定不存在的路徑
      （或讓呼叫端接住），而不是讓 `parents[4]` 自己丟 `IndexError`。
- [x] 加一個測試，在套件被放到淺層目錄的情況下（例如 monkeypatch `aliases.__file__` 或直接
      驗 `default_terms_file()` 不丟例外）證明兩個函式都不炸。

## How to verify

正式站上，不帶 `--terms-file`／`--keywords-file`：

```
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-aliases-seed --dry-run
```

應該回 JSON 而不是 traceback。指錯路徑仍要報錯：

```
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  guides-aliases-seed --terms-file /tmp/does-not-exist.json --dry-run
```

## Notes

2026-09-16 部署 #531 時的繞法：把 repo 的兩個檔案 `docker cp` 進 api 容器再用參數指定，
種子有跑成功（`inserted` 307、`reindexed` 142、`unknown_slugs` 158 篇是還沒發布的內容包）。
繞法只是當次可用 —— 容器一重建就沒了，所以下一次部署如果照文件跑，還是會踩到同一個 traceback。

### 2026-09-19 修法（claude-fable-5-1）

- `aliases.repository_file(*parts)`：有 repo 根（parents 超過四層）就用 `parents[4]`，沒有就錨在
  檔案系統根目錄，所以 `/app/app/guides/aliases.py` 算出來的是 `/docs/ai-terms-series/aliases.json`
  ——不存在的檔，`term_aliases` 與 `keyword_aliases` 走既有的「預設檔不在就回空」路徑；操作者指定
  的錯路徑仍是 `FileNotFoundError`（那段沒動）。`default_terms_file` 與 `default_keywords_file` 都改用它。
- 測試 `test_default_files_resolve_to_the_checkout_and_never_raise_in_the_image`：checkout 版面指到
  repo 的 docs、monkeypatch `__file__` 成 `/app/app/guides/aliases.py` 後兩個預設都算得出且不是檔案、
  兩個 loader 回空、指錯路徑仍丟例外。
- 部署後在正式站跑票上 How to verify 的兩條確認（第一條回 JSON、第二條報錯）即可 done。
