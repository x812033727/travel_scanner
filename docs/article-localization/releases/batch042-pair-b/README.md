# batch042-pair-b 語系發布收據（2026-09-29）

票：`2026-09-28-batch042-pair-b-release-reviewed-locales`。內容 PR #955。正式站部署在 `716bd5dc`（2026-09-29 10:08 UTC），之後才匯入。

## 做了什麼

1. **預檢**：沒有暫停檔、部署鎖空著、沒有被規則 1 標記的發布目錄；這批 slug 不在 `publish_holds.json`。
2. **dry-run**：16 篇 × en/ja/ko/zh-CN 全是 `create`、`publish: true`，taxonomy `unchanged`；zh-TW 為 8 篇 `update`、8 篇 `unchanged`。
3. **站主同意**：在對話中選了「只發新語系」：先備份、只 create 四個新語系、完全不動 zh-TW、Batch043 Pair A 的 zh-CN 先不發。
4. **備份**：整庫 `pg_dump -Fc` 存 `/root/travel_scanner_preimport_seo_20260929T101450Z.dump`（163,017,944 bytes），`pg_restore --list` 讀得出 1,216 個項目。匯入全程持有 `/var/lock/travel-scanner-deploy.lock`。
5. **發布**：每個語系一次 `guides-import --slug … --locale <L> --publish`，只帶這批的 slug。
6. **發布後**：同一清單再跑 dry-run，每個語系全 `unchanged`；zh-TW 仍是 8 `update`／8 `unchanged`，證明沒被動到。`guides-links-rebuild`：materialized 2,453、dropped 0、unresolved 0。

## 結果（本機未登入，`verify_public.py --kind life --sitemap`）

| 文章 | 語系 | 狀態 | 公開頁檢查 |
| --- | --- | --- | --- |
| `technical-seo-checklist` | en | 已發布 | ok |
| `technical-seo-checklist` | ja | 已發布 | ok |
| `technical-seo-checklist` | ko | 已發布 | ok |
| `technical-seo-checklist` | zh-CN | 已發布 | ok |
| `seo-learning-roadmap` | en | 已發布 | ok |
| `seo-learning-roadmap` | ja | 已發布 | ok |
| `seo-learning-roadmap` | ko | 已發布 | ok |
| `seo-learning-roadmap` | zh-CN | 已發布 | ok |

「ok」是 200、h1 等於內容包標題、canonical 正確、沒有 noindex、引用 `/guides/<slug>/` 的圖、在 sitemap 裡。

內容包 SHA-256（部署時的 `716bd5dc` 與合併時一致，之後沒有改動）：

- `technical-seo-checklist.json`：`55f4a7ae7f33fd4b4b6d95fb1e95eb08e881984038ba5f1b45f311dd5bb53f48`
- `seo-learning-roadmap.json`：`71f1033c6067eba0289ce7e7959100e84086e6c3b1504ef6cc2e582763b11ad4`

## 還沒做完的

- **正式站 zh-TW 仍是舊版**：`technical-seo-checklist`、`seo-learning-roadmap` 的 zh-TW dry-run 是 `update`（repo 移除了誤連 AI 詞彙表的連結）。這次刻意沒動，留給 live-source reconciliation 票用版本化的修正處理。新語系是依修正後的來源翻的，所以跟正式站 zh-TW 差那幾個連結。
- **跳過的關卡**：票上要求的「同映像隔離 Docker 演練」沒有做（沒有非正式環境）。站主在對話中知情後選了「先 pg_dump 再只發新語系」。手機與桌機的實際畫面沒有逐頁看過，只做了下面的未登入 HTTP 檢查。
- **站內連結**：`guides-links-check --locale en` 在這 16 篇有 17 筆 `unpublished`，指向還沒有英文版的 13 篇 life 文章（例如 `utm-link-conventions`、`canonical-url-guide`）；其他三個語系同型。等那些文章翻好就會生效。
