---
id: 2026-09-07-generator-rewrites-categories
title: 產生器每次執行都會重寫既有列的分類，重跑一次就還原剛修好的資料
status: done
priority: P2
area: tools
owner: claude-opus-5
claimed_at: 2026-09-07T00:31:10Z
created_at: 2026-09-07T00:29:54Z
completed_at: 2026-09-07T00:31:13Z
branch: claude/generator-keeps-categories
depends_on: []
scope:
  - tools/generate_secondary_hotspots.py
---

# 產生器每次執行都會重寫既有列的分類，重跑一次就還原剛修好的資料

## Why

`2026-09-06-seed-categories-assigned-by-quota` 把 `secondary_bootstrap.json` 裡按配額亂發的
分類逐筆修好了（34 筆，對照 Wikidata P31）。那張票已經 done。

但**產生那份資料的工具沒有改**。`tools/generate_secondary_hotspots.py` 的 `main()` 開頭是：

```python
for row in output:                     # output = 讀進來的既有 secondary_bootstrap.json
    offset = city_offsets.get(row["city_code"], 0)
    row["category"] = FALLBACK_CATEGORIES[offset % len(FALLBACK_CATEGORIES)]
```

它把**已經在檔案裡的每一列**的分類都覆寫成輪流發的值，然後才去收集新城市。

**損害什麼時候落地**：寫檔（`OUTPUT.write_text`）在城市迴圈裡面，所以全部城市都收集完的
情況下重跑只會在記憶體裡改、不落地。但只要有人為了加一個新目的地而執行它，那次就會把
既有 180 列的分類全部寫回輪流發的值——剛修好的 34 筆連同其他都沒了，而且輸出訊息只會說
「wrote 180 reviewed secondary-city hotspots」，看不出剛剛毀掉什麼。

第 459 行對**新**列也一樣是 `FALLBACK_CATEGORIES[index % 5]`，那是位置不是判斷。

## Definition of done

- [x] 既有列的分類不再被工具覆寫。
- [x] 新列的分類仍會給一個值（工具要能跑完），但在程式裡標明那是佔位、不是判斷。
- [x] 執行結束時列出哪些新列需要人工分類，不要靜靜混進去。

## Steps

- [x] 刪掉 `main()` 開頭那個重寫既有列的迴圈。
- [x] 第 459 行加註解說明它是位置不是判斷，並把新列的 slug 收進 `needs_category`。
- [x] 結尾印出需要分類的清單與「Wikidata P31 是上次用的來源」。

## How to verify

工具會連 Wikipedia 且耗時，沒有測試框架涵蓋 `tools/*.py`（`npm run test:tools` 只掃
`tools/*.test.mjs`，pytest 的 `testpaths` 只有 `apps/api/tests`）。所以驗證是靜態的：
`ast.parse` 通過，且 `row["category"] = FALLBACK_CATEGORIES` 這個字串已經不在檔案裡。

真正要跑的時候：先另外備份一份 `secondary_bootstrap.json`，跑完 `git diff` 確認既有列的
`category` 一行都沒動。

## Notes

- **沒有把新列的分類改成從 P31 推**，那是另一件事：要嘛在工具裡加 Wikidata 查詢，要嘛沿用
  `2026-09-06-seed-categories-assigned-by-quota` 的人工流程。這張票只負責「不要毀掉已經正確
  的資料」，範圍刻意收窄。
- `tools/` 沒有測試框架。要替這類工具加保護，得先決定放哪。
- 發現方式：另一個 session 傳訊息提到那張配額票時，我去看產生器有沒有一起修——沒有。
  那張票的內文與 Result 都沒有提到這個工具。
