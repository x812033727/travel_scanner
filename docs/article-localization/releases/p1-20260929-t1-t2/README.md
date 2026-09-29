# T1／T2 候選凍結與本機驗證

這是[逐批發布方案](../../../work-status-2026-09-29-article-release-plan.md)的候選準備紀錄，
不是正式發布收據。內容、圖片與原審稿收據保留在私人候選包；本目錄只保存可公開的
[驗證摘要與雜湊](evidence.json)。沒有重新翻譯、修改正文、正式連線、生成素材或發布。

## 固定範圍

| 波次 | slug | 目標語系 | 目標文件／語系圖片 |
| --- | --- | --- | --- |
| T1 | `marketing-mix-models`、`brand-tone-vibe-marketing` | en、ja、ko、zh-CN | 8／24 |
| T2 | `seo-keyword-research`、`seo-title-writing` | en、ja、ko、zh-CN | 8／24 |

合計4個完整五語內容包、16份目標文件與48張語系圖片；另保留4份繁中原文及12張原圖
作前後比對。`marketing-plan-small-business`、`paid-vs-organic-marketing` 不在範圍內。
文章、語系、文件雜湊、圖片位元組或審稿證據有變，都需要新的候選與驗證紀錄。

內容與圖片取自 `086e006cdfd5a982da9f412d28939ebb8eb4b453` 的 Git blob，
來源／目標核對表固定於方案提交 `2fda1163d974e75cbe0f6ac68018380c7b06e92d`。
原文、文章屬性與原圖另對照翻譯前提交；T1 審稿的 raw canonical JSON 雜湊與
T2／方案的 GuideDocument normalized 雜湊分別核對，不混用兩種定義。

正式狀態只引用 **2026-09-29 10:14:43（台灣）**的歷史唯讀快照：當時4篇皆為
article v2、繁中 draft/published v4，指定的16個語系列不存在。它不能代替新的
正式 preflight，也不是目前仍可寫入或已獲准發布的證明。

## 私人包與重驗

私人包的 `candidate-manifest.json` 固定內容、圖片、原收據、歷史快照投影與檢查工具；
`content/`、`assets/`、`reviews/` 不進公開倉庫。公開摘要保存 manifest SHA-256，
驗證時必須從摘要取得這個外部固定值，不能只相信待驗檔案自己填的雜湊。

```text
<API_PYTHON> -B <CANDIDATE_ROOT>/_tools/freeze_candidate.py validate
  --repo <REPO_ROOT> --manifest-sha256 <evidence.json 的 candidate_manifest_sha256>
```

在同一行執行上列參數。私人包 README 與 `_review/` 保存本機重驗方式、原始結果及
受控修改檢查。實際通過項目、數量與工具雜湊以 `evidence.json` 為準。

SQLite 驗證使用合成的本機資料列、ID 與修訂號，原文字內容對到固定雜湊。
它可核對既有匯入邏輯的範圍、內容保留及重跑行為，不能證明正式 PostgreSQL
交易鎖、指定 API 映像、備份回復或公網狀態。

## 本機驗證結果

完整性與五種受控竄改檢查共 **6 passed、0 skipped**；另外的 SQLite 匯入測試
**1 passed、0 skipped**。T1、T2 各建立並模擬發布8份目標文件，原文、文章屬性、
既有語系列、修訂及範圍外資料均保留；每波重跑皆無新增、更新或發布操作。
四包 lint 為0錯誤，仍有20個缺 summary、2個英文長度及8個站內連結提醒，
因此不能將 lint 成功當作完整編輯驗收。

## 發布前仍需完成

1. T2 的[原文 summary 審查](../../../../tasks/open/2026-09-28-review-batch041-keyword-and-title-summary.md)
   仍未完成。候選位元組與原審稿證據一致，不表示這項編輯門檻已通過。
2. 路線B仍需經獨立審查及排演的交易內來源／版本／可見性 guard 與 durable receipt。
   原生 `guides-import` 每個管理操作各自提交，不能用外層 dry-run 充當這個 guard。
   路線A publisher 的通用測試也不能代替本批路線B實際排演，不建立假的產線收據。
3. 選定包含內容與必要修正的 API 映像，完成同映像、隔離 PostgreSQL 的成功／衝突／
   中斷續跑／回復排演。本機沒有 Docker，這項仍未執行。
4. 按原方案取得逐步正式操作同意，重新核對版本、雜湊、缺列、可見性、holds、備份及
   actor；發布後才驗五語頁面、圖片、連結與索引並結案原發布票。

T1 的既有翻譯審稿 GO 保留；它也仍受上述執行門檻約束。這次只結案候選準備票，
不結案原文章發布票，不解除任何正式發布 hold。
