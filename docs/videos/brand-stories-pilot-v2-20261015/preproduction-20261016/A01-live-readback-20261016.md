# A01 正式機唯讀讀回（2026-10-16）— HOLD

本紀錄只涵蓋 `story-rolling-suitcase-v2` 在 **2026-10-16 06:19:37–06:26:30 UTC** 的主機讀取與本機離線檢查。沒有修改正式機或儲存庫既有檔案，沒有啟動模型、媒體供應商、影片重試或部署。離線匯出適配器因來源鏈未通過而**沒有執行**；以下數值不能當成安裝、付費製作或上架許可。

## 主機來源與可重現檔案

- PuTTY `hostinger2` 的正式機 checkout 為 `3cdbbd68b667ea202d10b8fd3c611a97cd809217`，`git status --porcelain` 為空。執行中的 `video-worker` 可讀 `/opt/mokaair/docs/videos/` 與 `/var/lib/mokaair/video-work/`。
- 工人 `/opt/mokaair/tools/video/automation/story.mjs` SHA-256：`f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3`；實際匯出的 `PANEL_INSTRUCTIONS` 文字 SHA-256：`3fb840dee13468f0133f9001d1d16f2930dfec29075145ddc6bc1e8a609bd4b3`。這兩項與 Git SHA 一起辨識讀回環境，不代替完整映像來源查證。
- 以二進位安全的 PuTTY stdout 串流保存 allowlist tar 到本機 Temp：`C:\Users\x8120\AppData\Local\Temp\a01-prod-snapshot-20261016-0624.tar`，**6,144,000 bytes**，SHA-256 `3ec1f7d2ade117456f875dab1b2eae8fa3f2d2d6372020bc49f1f50806b12676`。PuTTY 與 `tar -tf` 均 exit 0；280 成員為 199 個一般檔、81 個目錄，路徑均落在核准的 A01 文件、工作 JSON／Markdown、80 事件稽核目錄和安裝收據範圍，沒有媒體 bytes 或符號連結。`story/recheck-audit` 為 80 個事件目錄、80 個 `index.json`，沒有非 JSON 檔或符號連結；另有 13 份 `installation-receipt.json`。
- 本機檢查報告：`C:\Users\x8120\AppData\Local\Temp\a01-snapshot-inspection-20261016-0624.json`，SHA-256 `19b7a86171d466b8b8cc8a38f4c0d2c93e49be7e8aa4da0ab87a027c88eead27`。`inspect.mjs` exit 1，`integrity=REJECTED`，錯誤為 `SOURCE_DRIFT_FROM_TIP`。這是明確失敗，不是快照完整通過。

## 唯一來源差異：共用 lexicon 增加兩個空詞條

80 筆事件的鏈、安裝錨點與索引清單已走到鏈尾；鏈尾索引 SHA-256 為 `c7ddb6b5796605c08b3c47c305864eddf28e5246ee6ad8426c3601637ecdc9a4`，80 索引清單 SHA-256 為 `ada7ff1859788310fcda7ca35da052a2c4f1009b2c9058454b0e1b4d74d3614f`，均與先前固定釘選相同。鏈尾要求的來源組合雜湊為 `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`；實際快照為 `2a54ed212c1d876664e17f73fc39f8a20b1ddddccb6c877de54c694c5634501a`。逐欄比較後，**只有共用 `docs/videos/lexicon.json` 不同**；A01 的 `video.json`、`series.json`、`claims.md`、`script.md`、`auto.json`、六章、敘事審核與 `verify-1.md` 的來源雜湊仍吻合鏈尾。

| 來源 | SHA-256 | 說明 |
| --- | --- | --- |
| 鏈尾期望 | `ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9` | 對應舊版 bytes 保存在 `A01-round10-candidate/evidence/round9-lexicon.json`，不是推測重建。 |
| 工人掛載的現行 lexicon | `835e09df378d0c1b542b89c3fc44b2583b201217679267bce1146c638187d9c1` | 6,047 bytes；主機檔案 mtime 為 2026-10-16 03:26:39 UTC。 |
| 主機 Git checkout 中的 lexicon | `5ca9dda9f0672175d79627dbd8b86cdaac0b9afad48ea780c6a2242c30fe0a87` | 與工人掛載的持久化檔案不同；checkout 檔案 mtime 為 2026-10-12 04:14:56 UTC。 |

舊版與工人現行版逐行及 JSON 詞條比較：**295 → 297 詞條**，只在末尾新增 `"pull": null`、`"request": null`；沒有刪除或改值。工人掛載檔的 mtime 早於本次約 05:42 UTC 的部署，且與主機 checkout 檔位元組不同，所以不能把漂移直接歸為這次部署帶入的 repo 文件更新。是哪個流程寫入共用持久化 lexicon，這次唯讀讀回**未證實**。A01 來源正文與章稿沒有改動，是上述逐欄雜湊的結論。

對現行 `video.json`（含 YouTube 標題／說明）、六章 JSON 的所有字串欄位，以及本機 `A01-round12-candidate/candidate/series.json` 和六章 JSON 做不分大小寫的完整詞比對，另查現行 `claims.md`、`script.md`：`request` 沒有出現；`pull` 在現行影片只出現於 13 個 `data.camera`（`pull out`）與 1 個插畫 `data.prompt`，新版候選六章只出現於 17 個 `data.camera` 與 3 個插畫 `data.prompt`。旁白、標題／說明、主張表與口播稿沒有這兩個詞。這支持「新增空詞條不影響本次檢查所見的 A01 口播」的**有限推論**，不取代來源鏈重新綁定與獨立審查。

## 兩次資料庫、預算及工作目錄讀回

固定 slug 的 `readback.sql` 在唯讀交易中查詢；第一次與第二次的原始輸出逐位元相同，SHA-256 均為 `e5ec6ece0108b8e083b477915a8a08f0f4cd7f3af6eab40b22c706cfe91c3838`：

| 讀回 | 本機 Temp 檔案 | 結果 |
| --- | --- | --- |
| 第一筆 SQL（約 06:21 UTC） | `C:\Users\x8120\AppData\Local\Temp\a01-readback-20261016-0621.jsonl` | PuTTY exit 0；series `active`、episode 1 `started`、project `blocked`，retry ID 均為 null；110 筆 stage job（109 `succeeded`、1 `uncertain`），0 筆 media job。 |
| 第二筆 SQL（06:26:30 UTC） | `C:\Users\x8120\AppData\Local\Temp\a01-readback-20261016-0626.jsonl` | PuTTY exit 0；與第一筆原始 bytes 相同。唯一 `uncertain` stage job ID 為 `a4232619-a9a0-4488-9964-c66d2287b22a`。 |
| 第一筆預算帳本（約 06:22 UTC） | `C:\Users\x8120\AppData\Local\Temp\a01-budget-readback-20261016-0622.json` | PuTTY exit 0，SHA-256 `65b8f04cf07ac9d44956195653fe1028b97dc5dbb363fac6ac4c38a41e621141`。US$25 上限，reserved／settled 均 0，0 筆 operation。 |
| 第二筆預算與工作目錄（06:25:52 UTC） | `C:\Users\x8120\AppData\Local\Temp\a01-host-readonly-closeout-20261016.txt` | PuTTY exit 0，SHA-256 `b10eaf8af9c7a401941b66099a8127012bf45f65acbae4b3e720cd0ad58a38c4`；預算欄位仍相同。 |

兩次工作目錄觀察均未見全域 `STOP`、A01 `STOP` 或 A01 `LEASE`。`run-receipts` 只有 1 份 archived JSON（60,621 bytes，SHA-256 `e4baf4ed638d4d8ce66738f40791e1cdf9c21e86d3638320a62e0b7c378efa3d`），沒有未封存的 run journal；A01 工作目錄內所查的圖片、音訊與影片副檔名檔案數均為 0。`story/reviews/script-review.json` **不存在**。第一份目錄清單另存於本機 Temp：`a01-host-readonly-inventory-20261016.txt` SHA-256 `1e6e7de75385c01f77bd15d4bfaefa8611ce33985833425bb2fb5718cbd5a65e`；來源／媒體路徑核對清單 `a01-host-readonly-files-20261016.txt` SHA-256 `2d34fcbc1c7f8c5e829781a6fc904d041649224bdfbf1b9fd9915c4d71abc2b2`。

預算 CLI 只證明這個 A01 試作帳本當時沒有已列的 operation；**不能據此推論 110 筆歷史寫稿工作沒有供應商費用**。SQL 與預算 CLI 不是同一筆原子交易，兩次讀回相同也不保證之後不會變動。

## HOLD 與恢復前提

1. 保留 80 事件歷史、原釘選與這次失敗快照。由獨立審查者確認新增兩個空詞條的來源、A01 口播與工具語義影響，正式記錄共用 lexicon 的前後 SHA；不要直接改舊釘選或跳過 `SOURCE_DRIFT_FROM_TIP`。
2. 若採追加稽核事件重新綁定，先設計精確的新事件及來源雜湊、獨立審查與測試；目前檢查器硬性要求 80 事件，須經 PR 審查將新事件數與釘選正規更新。任何正式機的 lexicon／稽核／審稿收據寫入，須按既有任務與主機規則取得對應的限縮授權；本次未執行。
3. 變更落地後，重新擷取不可變 allowlist 快照、兩次 SQL／預算／STOP／LEASE／收據／媒體讀回，嚴格執行離線鏈與匯出適配器。只有新的確切檔案實稿通過獨立審查，才能另依已核准的窄範圍寫入 `story/reviews/script-review.json`；目前尚無此收據。
4. 正式機部署期間打斷其他影片工作之競態仍未修好；在獨立部署關卡修復與複核前，A01 維持 HOLD。這份文件不授權新增付費 A01 呼叫、B18／後五集或 YouTube 上傳。
