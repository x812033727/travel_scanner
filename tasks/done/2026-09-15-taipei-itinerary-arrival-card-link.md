---
id: 2026-09-15-taipei-itinerary-arrival-card-link
title: 台北四日行程的英日韓簡中版把台灣入境卡文章連成錯的類別
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-15T12:14:34Z
created_at: 2026-09-15T12:14:34Z
completed_at: 2026-09-15T12:20:32Z
branch: claude/fix-taipei-arrival-card-link
depends_on: []
scope:
  - apps/api/app/guides/content/taipei-4-day-itinerary.json
  - apps/api/tests/test_guides_content_links.py
---

# 台北四日行程的英日韓簡中版把台灣入境卡文章連成錯的類別

## Why

`taipei-4-day-itinerary` 的 en、ja、ko、zh-CN 四個語系都有一個連結指到入境卡文章
`taiwan-entry-2026-arrival-card`，網址寫成 `/<locale>/guides/howto/taiwan-entry-2026-arrival-card`。
但那篇是 `intel`。一篇文章只在自己 kind 的網址上渲染，換成別的 kind，頁面就是 noindex 的
「This guide is not available here」。
2026-09-15 在正式站實測：`/en/guides/howto/...` 回的是那個頁面，`/en/guides/intel/...` 才是文章本身。

內容包 schema 只驗網址格式，`pack_cli lint` 也只在「完全沒有站內連結」時才警告，
沒有任何檢查會發現連結的 kind 和目標文章對不上。

## Definition of done

- [x] 四個語系的連結都指到 `/guides/intel/taiwan-entry-2026-arrival-card`。
- [x] 有測試在任何內容包把站內連結寫錯 kind 時變紅（完整網址的連結與 `{"type":"article"}` 行內引用都算）。

## Steps

- [x] 改內容包四處網址（只改路徑中的 `howto` → `intel`，其餘不動）。
- [x] 新增 `apps/api/tests/test_guides_content_links.py`：
  - 掃所有內容包的站內完整網址與 article 行內引用，只檢查有內容包的目標 slug（只存在資料庫的文章無從得知 kind）。
  - 附兩個合成案例：錯 kind 會被抓到；沒有內容包的目標不會誤報。

## 合併後步驟（正式站）

內容包改了不會自己上線。部署之後在主機跑，限定這一篇：

```bash
python -m app.cli guides-import --actor-email <admin> --slug taipei-4-day-itinerary --publish --dry-run
python -m app.cli guides-import --actor-email <admin> --slug taipei-4-day-itinerary --publish
```

dry-run 應該是 en、ja、ko、zh-CN 四個 `update`。不要省略 `--slug`：正式站還積著數百篇已合併但未發布的內容包。

## How to verify

```bash
cd apps/api
uv run pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
uv run ruff check tests/test_guides_content_links.py
uv run python -m app.guides.pack_cli lint --slug taipei-4-day-itinerary
```

正式站匯入後：打開 `https://mokaair.com/en/guides/howto/taipei-4-day-itinerary`（以及 ja、ko、zh-CN），
確認入境卡連結指向 `/guides/intel/taiwan-entry-2026-arrival-card` 並開得出文章。

## Notes

- 2026-09-15 本機（Windows、`uv sync --frozen` 的 venv）：
  - 新測試 3 passed。
  - 把內容包換回 main 的版本時，全庫掃描那條測試變紅，正好列出這四個連結；還原後又綠。
  - `test_guides_content_pack.py`＋`test_guide_partner_links.py`＋新檔：66 passed、28 skipped。
  - ruff 與 mypy 對新檔都乾淨。
  - `pack_cli lint --slug` 的 exit 0，只剩兩個既有警告（en 本文 7,960 字超過 howto 建議上限、全站 sitemap 列數），與本次修改無關。
- 修正前掃過全部 943 個內容包，錯 kind 的連結只有這四個。
- 這是站主要求「其他文章哪邊有問題」時做的站內連結分析發現的；同一份分析另外找到 189 個連到未發布文章的連結，
  那屬於發布順序，不在本票範圍。
