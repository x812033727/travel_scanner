---
id: 2026-09-14-life-finance-series-catalogue
title: 財經系列：編輯總表與撰稿指令
status: done
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-14T11:50:31Z
created_at: 2026-09-14T11:45:18Z
completed_at: 2026-09-14T11:50:32Z
branch: claude/beautiful-fermat-0klj9k
depends_on: []
scope:
  - docs/life-finance-series.md
  - docs/life-finance-series-brief.md
---

# 財經系列：編輯總表與撰稿指令

## Why

站主要在生活分享專區做第二個垂直領域：約 120 篇財經文章與教學，分六批。
批次票的 `scope` 要精確到檔案才能讓六批同時開工，所以每一篇的 slug、標題、topics、配圖方式
必須先在一份總表裡定死；撰稿代理也需要一份可以重複使用的指令。

這兩份文件就是那個前提。AI 系列的對應檔案是 `docs/life-ai-series.md` 與
`docs/life-ai-series-brief.md`，形狀照抄，**但財經多了一層法遵限制**，那是 AI 系列沒有的。

## Definition of done

- [x] `docs/life-finance-series.md`：120 篇的編輯總表，六個批次各一張表格，
      欄位 `| # | slug | 標題 | topics | 圖 | 合作 | 易變 |`，slug 在第二欄的反引號裡
      （`pack_ingest.catalogue_slugs` 解析的就是這個形狀）。
- [x] 總表含「政策」「不能寫的東西」「可連的旅遊攻略」「產製流程」「經驗記錄」各節。
- [x] `docs/life-finance-series-brief.md`：每篇原文重用的撰稿指令，含免責 callout 的樣板。
- [x] 120 個 slug 互不重複，也不和站上既有的 378 個內容包相撞。
- [x] 總表列出的旅遊攻略網址全部存在、`kind` 正確、而且有 zh-TW。

## Steps

- [x] 寫總表與撰稿指令。
- [x] 用 `catalogue_slugs` 的正規表示式驗證 120 列都解析得出來。
- [x] 驗證 slug 沒有重複、沒有和既有內容包相撞。
- [x] 驗證每個旅遊銜接網址都指到存在、`kind` 正確且有 zh-TW 的文章。

## How to verify

```bash
# 總表解析得出 120 個 slug（全部都還沒寫，所以全是 catalogue_missing_pack 警告，exit 0）
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life \
  --catalogue ../../docs/life-finance-series.md
npm run check:tasks
```

## Notes

- `lint --catalogue` 同時會把 AI 系列的內容包列成「總表沒有」的警告，那是既有行為
  （`lint_all` 拿總表比對的是全部內容包，不是 `--kind` 篩過的），
  `tasks/open/2026-09-14-guides-pack-lint-catalogue-life.md` 已經在處理，不要在這裡順手改。
- 警告不影響離開碼；沒有加 `--warnings` 就是 exit 0。

## Outcome

總表與撰稿指令已寫好，六張批次票的 scope 直接從總表產生。三個在寫的過程中才發現的限制，
已經寫進文件與相關票裡：

1. **站上有一批 `taiwan-` 開頭的旅遊攻略沒有 zh-TW**（`taiwan-payment-easycard-cash-cards`、
   `taiwan-tax-refund-shopping-2026` 等，只有 en／ja／ko／zh-CN，因為那是寫給境外旅客的）。
   從 zh-TW 的財經文連過去是壞連結。總表因此改成給一張**驗證過的完整網址白名單**，
   撰稿代理不准自己組網址。
2. **`kind` 是旅遊攻略網址的一部分**（`/guides/howto/…` 或 `/guides/intel/…`），
   所以白名單給的是完整網址而不是 slug。
3. **免責 callout 的標記字串必須和 lint 規則逐字一致**（「不是投資建議」）。
   brief 的樣板已經寫死，並註明不可改字。
