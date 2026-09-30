# Batch040 正式站 zh-TW 來源核對（2026-09-30）

票：`2026-09-28-batch040-live-source-reconciliation`。3 篇、4 個誤連到 AI 詞彙表的內文連結，
在正式站改成純文字（repo 早已改好，正式站 zh-TW 一直停在修正前的版本）。

## 核對（唯讀，2026-09-30 寫入前）

在 api 容器裡用唯讀腳本，把每篇 zh-TW 的草稿與已發布版本跟修正前的內容包（`88cfde04d`）比對：
全部**完全相同**，草稿與發布都是 v4，沒有任何後台編輯。修正前後的內容包只差下表的區塊，
差異僅是 `article` 連結節點換成同文字的 `text` 節點，沒有其他字元或欄位改變。

| 文章 | 修正 PR | 區塊 | 移除的連結目標 | 修正後 zh-TW 文件雜湊 |
| --- | --- | --- | --- | --- |
| `affiliate-marketing-basics` | #930 | 17 | `ai-term-token` | `c893c8eafcb6…` |
| `ecommerce-product-seo` | #930 | 1, 12 | `ai-term-token`, `ai-term-model-parameters` | `25fe33ce82ac…` |
| `zero-click-search-strategy` | #930 | 11 | `ai-term-token` | `2c0660c39def…` |

## 寫入（2026-09-30 00:13–00:14 UTC）

站主在對話中同意推上正式站並接手本票，同時接受「同映像隔離演練」為已知情放棄（沒有非正式環境）。
另一個 session 的部署 `cb4d0b44` 00:13:35 結束、api 健康 200 之後，在部署鎖下一次處理三批共 8 篇：

1. dry-run（只帶 8 個 slug、`--locale zh-TW`）：8 個 `update`、`publish: true`，taxonomy 全 `unchanged`。
2. `pg_dump -Fc`：`/root/travel_scanner_preimport_zhtwlinks_20260930T001344Z.dump`（168,764,941 bytes，TOC 1,216 項）。
3. `--publish`：updated 8、published 8、failed 無。
4. 重跑 dry-run：zh-TW、en、ja、ko、zh-CN 全部 `unchanged`，譯文沒有被動到。
5. `guides-links-rebuild`：materialized 2,570、dropped 0、unavailable 0。

## 讀回

- 資料庫：每篇 zh-TW 的草稿與已發布版本都等於 repo 目前的內容包（v4 → v6），顯示狀態沒有改變。
- 公開頁（未登入）：文章內容裡指向上表目標的連結數都是 0；`verify_public.py --locale zh-TW --sitemap`
  八篇 `RESULT PASS (0 problems, 8 pages)`。
