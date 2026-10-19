# A01 2026-10-18 正式機唯讀讀回：HOLD

這是 `story-rolling-suitcase-v2` 的唯讀擷取與離線核對紀錄，並非採用新章稿、簽發審稿收據或啟動付費製作的授權。原始擷取保存在本機私有路徑 `<home>\.codex\captures\A01-20261018-1523-104`；該處的 `capture-manifest.json` 列出七份檔案的位元組數與 SHA-256。正式機沒有因本次檢查而寫入。

## 擷取與主機狀態

- 15:23 UTC，經已授權的 `hostinger2` PuTTY root 唯讀連線，在主機以 stdout 串流 A01 的六章、合稿、稽核 JSON、安裝收據和釘選發音表；本機 tar 為 8,140,800 bytes，SHA-256 `13fedb2bcdb44bd2dd1bf484ea5557c2d217a0ddf71e6c1b57e33b2ba46912ed`。清單為 254 個一般檔案、108 個目錄，沒有符號連結或特殊項目。
- 主機 Git HEAD `498b1dbfc78f44dfa79926b0c979cb26d3b5202f`（#1568）；worker `story.mjs` SHA-256 `4ea58f881f5b81e96b75b91a420f7deef86eaa6bb454ed9de3f03607baaad4e7`；現行敘事 panel 指示 SHA-256 `3fb840dee13468f0133f9001d1d16f2930dfec29075145ddc6bc1e8a609bd4b3`。
- 全域 `STOP` 不存在；A01 `STOP` 存在，SHA-256 `f7bea3b50620f35ef3575662d1032a72dad9755dfa3c035ac373c002e137352a`，理由是發音表採用後仍須獨立讀回及審稿；A01 `LEASE` 不存在。沒有解除 STOP。
- 15:23 與 15:32 UTC，兩次只讀 SQL 投影逐位元組相同，SHA-256 `7fbb745093afef035f7e076eb2c9eca30383ce92526074e51566436bdb6ff9dd`：系列 active、A01 集 started、project blocked；A01 寫稿工作 131 succeeded、1 failed、1 uncertain，媒體工作 0。
- 兩次 A01 預算 CLI 唯讀輸出也逐位元組相同，SHA-256 `65b8f04cf07ac9d44956195653fe1028b97dc5dbb363fac6ac4c38a41e621141`：上限與剩餘皆 US$25，操作 0、保留 0、結算 0。
- 15:36 UTC 前檢：部署 hold 不存在、部署鎖空、主機 checkout 乾淨，但全站有 1 筆 running 和 3 筆 queued 的付費 AI 階段工作；這份前檢沒有列出它們的 slug 或階段種類。A01 在 15:32 的 SQL 讀回沒有 running／queued 工作，但兩次讀取並非同一交易。部署會重啟 worker 並使當時 running 工作的結果不確定，因此此時不能部署。

## 離線核對結論

最新 254 檔和先前已獨立驗證的 `snapshot-104` 逐檔比較：253 檔相同，唯一差異是共用 `docs/videos/lexicon.json`。A01 六章、合稿、企劃、釘選 `story-lexicon` 和稽核事件沒有漂移。以 80／81／82 筆不可變基線及 `inspect-review-progress.mjs` 重算，兩份快照均為 `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`：104 筆連續事件、82 筆後另有 22 筆，來源 SHA-256 `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`，104-index manifest SHA-256 `eb22c3ef4bb0254618d7a3f06c1840ec2c6564a0baec02930e1b46b25f7d4ccd`，tip index SHA-256 `f2628d894d6907f64733325581e0116c1d7b297b45fec0d9d63c4aff82d09288`。這證明本次擷取的舊鏈完整，**不代表新稿已被採用或審查通過**。

目前正式稿仍為 79 鏡、目標 `[9,11]` 分鐘；`review/narrative.json` 的 `one_line`、`no_recap` 未過，且舊 panel 指示雜湊不同於現行規則。`story/reviews/script-review.json` 不存在；此次 A01 工作與預算讀回未見付費媒體，已列的 A01 工作目錄也未見成片。這不是全域媒體資產或 YouTube 的完整盤點。r12／後續 r13 新稿須在來源索引與章稿修正後，以正式保存的精確位元組重新跑 verifier、listener、兩位獨立敘事讀者和審稿收據；真實 TTS、插畫與成片驗收另計。任何正式機寫入都須新的指定範圍核准與無漂移前檢。
