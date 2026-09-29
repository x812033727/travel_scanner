# batch041-pair-b 語系發布收據（2026-09-29）

票：`2026-09-28-release-reviewed-batch041-on-page-and`。內容 PR #941。正式站部署在 `716bd5dc`（2026-09-29 10:08 UTC），之後才匯入。

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
| `on-page-seo-workflow` | en | 已發布 | ok |
| `on-page-seo-workflow` | ja | 已發布 | ok |
| `on-page-seo-workflow` | ko | 已發布 | ok |
| `on-page-seo-workflow` | zh-CN | 已發布 | ok |
| `image-seo-workflow` | en | 已發布 | ok |
| `image-seo-workflow` | ja | 已發布 | ok |
| `image-seo-workflow` | ko | 已發布 | ok |
| `image-seo-workflow` | zh-CN | 已發布 | ok |

「ok」是 200、h1 等於內容包標題、canonical 正確、沒有 noindex、引用 `/guides/<slug>/` 的圖、在 sitemap 裡。

內容包 SHA-256（部署時的 `716bd5dc` 與合併時一致，之後沒有改動）：

- `on-page-seo-workflow.json`：`4efc110daa4f755fc82e02fd5a71c9f0b791642fb6fdfc0e9d71f94cdfc8aabd`
- `image-seo-workflow.json`：`9b07710a4b4918cec10f22f141c6b8f85de2a6d8e765fec15d31a4eecbe98193`

## 還沒做完的

- **正式站 zh-TW 仍是舊版**：`image-seo-workflow` 的 zh-TW dry-run 是 `update`（repo 移除了誤連 AI 詞彙表的連結）。這次刻意沒動，留給 live-source reconciliation 票用版本化的修正處理。新語系是依修正後的來源翻的，所以跟正式站 zh-TW 差那幾個連結。
- **跳過的關卡**：票上要求的「同映像隔離 Docker 演練」沒有做（沒有非正式環境）。站主在對話中知情後選了「先 pg_dump 再只發新語系」。手機與桌機的實際畫面沒有逐頁看過，只做了下面的未登入 HTTP 檢查。
- **站內連結**：`guides-links-check --locale en` 在這 16 篇有 17 筆 `unpublished`，指向還沒有英文版的 13 篇 life 文章（例如 `utm-link-conventions`、`canonical-url-guide`）；其他三個語系同型。等那些文章翻好就會生效。

## 手機與桌機實看（2026-09-29 11:30 UTC 前後）

Playwright 驅動本機的 Chrome，未登入，桌機 1366×900、手機 Pixel 7（412×839），每頁往下捲到底讓延遲載入的圖片出現：
16 次載入全是 200，`lang` 與語系一致、沒有 noindex、h1 是該語系的標題；文章圖 80 張，沒有破圖、全部有 alt；
兩種寬度都沒有水平溢出。逐頁數字在 `browser-check.json`。另外親眼看過日文手機版與韓文桌機版的截圖（圖解是該語系的文字）。

console 裡的錯誤跟翻譯無關：桌機版的 `emrldtp.cc` 跨網域錯誤是 Travelpayouts Drive 腳本，zh-TW 原頁一樣會出；
連續掃頁觸發的 429 只打在子資源、單頁重開時一筆也沒有；一次 `int64` 例外單頁重開兩次沒有重現。

站主在 2026-09-29 的對話中接受「同映像隔離演練」為已知情放棄。
