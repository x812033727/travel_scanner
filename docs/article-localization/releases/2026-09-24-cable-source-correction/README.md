# 2026-09-24 desk-cable 原文修正上線

`desk-cable-charging-organization`（zh-TW）第一個 rich_paragraph 的「標記」原本連到 AI 詞彙文章 `ai-term-token`，意思不對。PR #690（`b626f310`）在 repo 把它改成純文字；這份紀錄是把同一個修正發布到正式站的過程與結果。票：`tasks/done/2026-09-24-publish-cable-labeling-source-correction.md`。

## 做了什麼

1. 預檢（唯讀）：沒有部署暫停檔、部署鎖空著、沒有被規則 1 標記的分階段發布；正式站跑 `b6dcfb81`，已包含 `b626f310`；主機上的內容包 `blocks[2].inlines[1]` 已是純文字；這個 slug 不在 `publish_holds.json`。
2. 發布前比對：正式站 v6 的公開文件與 repo 內容包正規化後只差 `/blocks/2/inlines/1`，所以匯入不會蓋掉任何後台編輯。
3. `guides-import --slug desk-cable-charging-organization --locale zh-TW --dry-run`：taxonomy `unchanged`，zh-TW `update`、`publish: true`，沒有別的項目。
4. 站主在對話中選擇「先 pg_dump 再發布 1 篇」。整庫 `pg_dump -Fc` 143,274,356 bytes，TOC 可讀。
5. 同一指令帶 `--publish`：`updated` 與 `published` 都只有 `desk-cable-charging-organization:zh-TW`，`failed: null`。走的是後台同一條寫入路徑（`save_draft` 帶 `expected_version`、`publish_locale`），產生新版本，舊的 v6 留在歷史裡。
6. `guides-links-rebuild`：materialized 2,032、dropped 0、unresolved 0。`guides-links-check --locale zh-TW` 只有一筆與本篇無關、早已存在的發現（`gemini-guide` 的 `raw_url`）。
7. 再跑一次 dry-run：zh-TW `unchanged`、`publish: false`，也就是草稿、正式版與 repo 內容包三者相同。

## 結果（2026-09-24 06:20 UTC，未登入從外部查）

- 公開 API 的 `document.blocks[2].inlines[1]` 是 `{"type":"text","text":"標記"}`，版本 8；另一個內連 `gadget-purchase-needs-checklist` 仍在。
- `article_links` 沒有 `ai-term-token`；`ai-term-token` 那篇的 backlinks 不再列出本篇。
- `/zh-TW/life/desk-cable-charging-organization` 回 200，HTML 裡沒有 `/life/ai-term-token`。

## 翻譯基準

之後翻這篇的四個語系，從 `published-zh-TW.json` 開始，不要用舊的 v6。

| 項目 | 值 |
| --- | --- |
| 檔案 `published-zh-TW.json` 的 SHA-256 | `cb167ca844dbe7dd3b3bce75f8224b9fe319c9dd8a15c6e924af5e611628ceb8` |
| 正規化後文件雜湊（正式站） | `b67d107a9413dbf52e5729d0c543cbb9698524feeb332f67c6df8b0de8e3619c` |
| 正規化後文件雜湊（repo 內容包） | 同上 |
| zh-TW 公開版本 | 8 |

正規化：拿掉公開文件的 `version`、`published_at`、`modified_at`，經 `GuideDocument.model_validate(...).model_dump(mode="json")`，再用 `app.guides.service.document_hash`。這個雜湊和舊票 Notes 裡記錄的「修正後原文模型」`b67d107a…` 相同，兩邊獨立算出同一個值。

完整數字在 `evidence.json`。
