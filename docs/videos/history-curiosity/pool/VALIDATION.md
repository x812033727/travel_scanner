# 驗證（2026-11-01，revision `2026-11-01-curio-pool-97`）

## 機械檢查（本機，Node v22.23.4）

| 檢查 | 結果 |
| --- | --- |
| `node --test tools/video/curio/pool/pool.test.mjs` | 16 通過、0 失敗、0 略過 |
| `python -X utf8 tools/video/curio/pool/semantic_test.py`（numpy 2.5.4、onnxruntime 1.31.1、tokenizers 0.23.3） | 2 通過 |
| `node tools/video/curio/pool/cli.mjs build` | 入選 97、題庫內高相似未處置 0、跨系列未處置 0 |
| `node tools/video/curio/pool/cli.mjs check` | PASS：重建後 pool.json、四份 md、index.html 與 manifest 雜湊都一致 |
| `cli.mjs index` 跑兩次 | 第一次 IMPORTED，第二次 UNCHANGED、0 writes |
| `cli.mjs source https://www.gutenberg.org/ebooks/25645` | 反查到 H02（已製作）與它的定位 |
| `node tools/tasks.mjs check` | 通過 |
| `npm run test:tools` | 1040 通過、101 失敗；失敗的 101 個在拿掉本 PR 的檔後一樣失敗（本機沒有 `npm ci` 的依賴），與本 PR 無關 |

## 測試鎖住的規則（`pool.test.mjs`）

- topic-check 一題一檔整檔讀：表格裡的每個網址都留下，非 200 的連結檢查記成限制。
- 沒有來源的題目卡只能是候補，不能選入。
- 已製作的題鎖定：能吸收重複題，不能被併掉、淘汰或轉 Shorts；分支草稿與 W 軸也算。
- 淘汰要寫重新收錄條件，轉出要寫去哪，Shorts 要寫理由。
- 別名保留自己的 ID 與來源；只有完全相同的題目會自動合併。
- 同一案件鍵的配對沒處置前不能 build；有來源的題不是入選就是暫緩，要有理由。
- 跨系列（原來如此事務所）高相似的配對沒處置前不能 build；轉出要同時是轉出處置。
- 片長估計：能當一集主幹的題至少要撐到 8 分鐘，否則標章節。
- 題案 8–13 分鐘、章節秒數剛好加總、每章至少 30 秒；一題只進一個題案；不排已製作的題；撐不起一集的入選新題不能單獨存在。
- 網址解析、私有位址拒絕、追蹤參數清除；基線快照的原始紀錄變動要寫理由；SQLite 索引重跑 0 writes；頁面跳脫 `</script>`。
- 已提交的輸出：manifest 雜湊、題案定義雜湊、未處置配對為 0、沒有任何題標 production_ready。

## 頁面實看

`index.html` 用 Playwright（Chromium）開桌面 1280px 與手機 390px：

| 項目 | 結果 |
| --- | --- |
| 初始 | 355 筆（淘汰與轉出不顯示） |
| 搜尋「1947」 | 4 筆 |
| 篩「候補」 | 142 筆 |
| 篩題案 T01 | 3 筆 |
| 篩 U 軸並展開第一張卡 | 紀錄、範圍、來源清單都有內容 |
| 橫向溢出 | 0 px |
| console 錯誤 | 0 |

兩張截圖都實際看過。

## 編輯與覆核

- 舊題處置：作者第一輪 114 條，一位非作者覆核者逐條判讀。結果是 92 同意、7 不同意、15 建議修改，另有 25 項漏處置，全部照覆核改判（[收據](reviews/legacy-review-20261101.json)）。
- 新題：六個研究代理，各自一個題組。兩位非作者覆核者分批逐題重開關鍵來源（[收據](reviews/wave1-review-20261101.json)）。
- 語意近鄰：本機跑釘版 MiniLM，輸入是 `.cache/draft.json`。每題讀 top-10，另對原來如此的核心題讀 top-3。這個近鄰只用來找比較對象，不是合併判定，也沒有評估召回率。

## 限制

- 舊查核檔與集數研究檔的 4,800 多個網址本輪沒有重讀；入選舊題的可讀性要在製作前重查。
- 新題研究時打不開或只讀到鏡像的頁（web.archive.org、FBI、NSA、JSTOR、部分 Nature、ADS 等），寫在各題 notes 與來源的 limitations。
- 詞面相似對中文標題幾乎抓不到真重複；語意近鄰也不保證找全。人工比對的範圍是全部題目卡，但這不是獨立的抽樣品質評估。
- 原來如此事務所的排程（`so-thats-why/schedule.csv`）有不在核心題快照裡的題，例如 B03 可口可樂配方。L20 製作前要跟它錯開。
- 沒有呼叫付費媒體、沒有部署、沒有改 `topics.json`，也沒有任何劇本核准。
