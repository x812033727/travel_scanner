# 2026-09-24 desk-cable 四語上線

`desk-cable-charging-organization` 的 en、ja、ko、zh-CN 已在正式站發布。內容來自 PR #723（`4e618566`），翻譯與審稿紀錄在 `tasks/done/2026-09-24-localize-desk-cable-guide.md`。發布票：`tasks/done/2026-09-24-release-localized-desk-cable-guide.md`。

## 做了什麼

1. **不必部署**：正式站 10:24 UTC 已由另一次部署跑到 `1b4b42f2`，包含 #723；部署腳本的 `--dry-run` 回報 up to date。預檢：沒有暫停檔、鎖空著、沒有被規則 1 標記的發布；執行中的 api 映像裡，內容包已有五個語系；slug 不在 `publish_holds.json`。
2. **dry-run**：`guides-import --slug desk-cable-charging-organization --locale en --locale ja --locale ko --locale zh-CN --dry-run`，四個 `create`、`publish: true`，taxonomy `unchanged`。另跑一次 zh-TW 的 dry-run，是 `unchanged`。
3. **站主同意**：在對話中選了「先 pg_dump 再發布 4 個語系」。整庫 `pg_dump -Fc` 143,453,584 bytes，TOC 可讀。
4. **發布**：同一指令帶 `--publish`，`created` 與 `published` 都只有這四個語系，`failed: null`。
5. **連結**：`guides-links-rebuild` 從 2,032 筆變 2,036 筆，多的四筆是新語系文末連到 `gadget-purchase-needs-checklist`；dropped 0。五個語系的 `guides-links-check` 在本篇都是 0 筆發現；每個語系 exit 1，是因為其他文章原本就有的發現。
6. **發布後**：五個語系一起跑 dry-run，全部 `unchanged`、`publish: false`。

## 結果（本機未登入從外部查）

`verify_public.py --kind life --sitemap`，五個語系：`RESULT PASS (0 problems, 5 pages)`（200、h1、canonical、沒有 noindex、圖片 200、在 sitemap 裡）。

| 語系 | 公開版本 | 正規化文件雜湊（正式站＝內容包） |
| --- | --- | --- |
| zh-TW | 8（這次沒動） | `b67d107a9413dbf5…` |
| en | 2 | `29300977c879cb73…` |
| ja | 2 | `99b3444a19f729aa…` |
| ko | 2 | `796d07ab7e0402e0…` |
| zh-CN | 2 | `a55af5580b4ff6a4…` |

每個語系的 `article_links` 都含 `gadget-purchase-needs-checklist`，都不含 `ai-term-token`；`published_locales` 五個都在。公開 API 的原始回應存成 `published-<locale>.json`，完整雜湊與數字在 `evidence.json`。正規化方式同 `../2026-09-24-cable-source-correction/README.md`。
