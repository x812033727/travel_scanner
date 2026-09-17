---
id: 2026-09-16-land-the-batch-4-authoring-tooling
title: Land the batch-4 authoring tooling in docs/news-2026-batch-4
status: done
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T21:49:48Z
created_at: 2026-09-16T21:49:44Z
completed_at: 2026-09-16T22:11:54Z
branch:
depends_on: []
scope:
  - docs/news-2026-batch-4/verticals.py
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/merge_locale.py
  - docs/news-2026-batch-4/apply_corrections.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/PORT-NOTES.md
  - docs/news-2026-batch-4/.gitignore
  - docs/crypto-news-2026/README.md
  - docs/tech-news-2026/README.md
  - docs/ai-news-2026-09-late/README.md
---

# Land the batch-4 authoring tooling in docs/news-2026-batch-4

## Why

批次 4 的六個腳本（`verticals.py`、`check_article.py`、`build_assets.py`、`merge_locale.py`、
`apply_corrections.py`、`update_index.py`）是從批次 3 的 `docs/ai-news-2026-09-mid/` 移植的，
移植後經過兩輪審查。第一輪 22 個問題修掉 20 個，第二輪重測後還有 11 個沒關，另有 6 個是
修理的代理刻意不動的（其中三個只是因為 `PORT-NOTES.md` 是共用檔，不想跟別人對撞）。

腳本一直放在 scratchpad 裡，不在 repo。三個垂直的工作區目錄也還不存在，
而 4.1／4.2／4.3 三張票的 `scope` 都指著它們。

## Definition of done

- [x] 六個 `.py` 與 `PORT-NOTES.md` 進 `docs/news-2026-batch-4/`，`__pycache__` 不進。
- [x] `docs/news-2026-batch-4/.gitignore` 與批次 3 的一字不差（`renders/`、`__pycache__/`）。
- [x] 第二輪 `still_broken` 的 11 項全部關掉，每一項都用它自己的 EVIDENCE 指令重跑證明，
      並附一個「壞輸入仍然要被擋下」的反面案例。
- [x] `PORT-NOTES.md` 與程式碼一致：垂直表不再有 callout 數、`COUNT` 那段重寫、
      build_assets 那句照建議改寫並補上瀏覽器延後解析、hero 改成警告、`.gitignore`。
- [x] 三個工作區目錄各有一份 README，指向 `BRIEF.md`、垂直規格與對應的修正清單。

## Steps

- [x] 複製六個檔案與 `PORT-NOTES.md`，寫 `.gitignore`。
- [x] `update_index.py`：`_PIECES` 補簡體 `则`；`EDITS` 的區塊索引與 `TABLE` 的欄索引補範圍檢查。
- [x] `merge_locale.py`：壞 JSON、不存在的 slug、沒有 `sources` 鍵、沒有 zh-TW 都改成 `REFUSED`。
- [x] `apply_corrections.py`：檔案不是 JSON／不是陣列、缺鍵、指名 zh-TW（原本是裸 `assert`）
      都改成 `SKIPPED` 並繼續跑後面的條目。
- [x] `check_article.py`：`body_without_summary` 改用 `_body_parts`；`HERO_SIZE` 與
      summary／faq 上下限改成從 schema 讀；hero 位元數改成 `pack_ingest` 的兩級；
      研究紀錄的 `translations[locale].diagram.title`／`caption` 補進檢查。
- [x] `build_assets.py`：工作區 `.gitignore` 補 `__pycache__/`；hero 超過編輯準則改成警告。
- [x] `ai.md` 與 B8 的矛盾另開一張票，程式註解改成指向那張票。

## How to verify

```bash
cd apps/api
# 讀取路徑（不寫任何東西）
uv run python ../../docs/news-2026-batch-4/check_article.py <slug> --full --assets
# 寫入路徑一律在沙箱根目錄下跑，apps/api/app 是複本：
MOKAAIR_ROOT=<sandbox> uv run python .../merge_locale.py <slug> ja <document.json>
MOKAAIR_ROOT=<sandbox> uv run python .../apply_corrections.py <corrections.json>
MOKAAIR_ROOT=<sandbox> uv run python .../build_assets.py ai [--svg-only]
```

實測輸出在這張票的工作紀錄裡；重點是：批次 3 的 `ai-news-siri-ai-ios-27-20260914` 加上
`summary`／`faq` 之後，`--full --assets` 是 `OK`，而每一條規則都有對應的反面案例會 `FAIL`。

## Notes

- **正式內容一個位元組都沒動。** `apps/api/app/guides/content` 當時被
  `2026-09-15-content-summary-howto-and-life` 持有，所有會寫檔的測試都在
  `MOKAAIR_ROOT` 指定的沙箱根目錄下跑，那裡的 `apps/api/app` 是複本而不是符號連結。
- **hero 位元數的兩級是站上自己的分級。** `pack_ingest` 超過 `IMAGE_HARD_CAP`（300 KB）
  才是 error，超過 `HERO_MAX_BYTES`（200 KB）是 warning。檢查器與產圖器現在都照這個分級，
  所以產圖器寫得出來的東西，檢查器不可能擋下。
- **`--full` 在翻譯併入後就不是選配。** 沒有 `--full` 時 locales 必須剛好只有 zh-TW，
  這是批次 3 的規則，保留未改；已完成的文章不帶 `--full` 會回
  `locales ['zh-TW', 'en', …] != ['zh-TW']`。
- **`RELATED`、`NEW`、`CITED`、`TABLE`、`CAPTION` 仍然是空的**，`drawing()` 也還沒有任何一篇的
  分支。這些是各垂直那三張票的內容，不是移植的一部分。
- `ruff` 在這些檔案上報 5 個 `B905` 與一批 `E501`；`docs/` 不在設定的 lint 範圍內，
  批次 3 的原檔報得更多。細節見 `PORT-NOTES.md`。
