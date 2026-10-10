# AI 引用查核影片：2026-10-07 備份盤點

本次只讀盤點沒有找到可綁定 `ai-citation-check` 原始媒體的匹配封存，因此沒有可供採用的 archive 路徑／SHA-256、143 筆 raw 音訊、原始 take cache、舊音訊 QA、五語 CC 或 final 的還原證據。這是下列明確範圍的查找結果，不能推論所有磁碟、其他備份批次或正式站都沒有這些檔案。

此文件保留已完成盤點的結果；它不是持續更新的媒體狀態。後續製作、正式站與 provider journal 狀態由各自的實際收據記錄。

## 來源與歷史完成紀錄

凍結的 `docs/videos/ai-citation-check/video.json` 來源 SHA-256 為：

`a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2`

此 pin 也存在於下列本機 renewed-finals source inventories 的九份 citation 文件描述中；那些描述涵蓋 brief、claims、demo-log、verify-1、video 與四語翻譯，沒有 citation 音訊、cache、字幕或 final 的媒體路徑：

- `<home>/mokaair-work/handoff/renewed-finals-20261007/r3-runtime-inventory-readonly-snapshot-20261007T0814Z.json`
- `<home>/mokaair-work/handoff/renewed-finals-20261007/r6-host-prepared-20261007T0826Z/operator-runtime-r6-receipt.json`

任務票的 2026-09-28 記錄曾描述五語 SRT、143/143 音訊檢查零標記，以及 18,749 影格、約 10:24、-14 LUFS 的新版成片。這些是歷史製作紀錄；本次沒有找到可還原並重新驗證的匹配媒體，不能把那段紀錄當成當前檔案存在、當前 QA 通過或交付完成的證明。此盤點也沒有否認歷史製作曾發生。

## G 槽查找範圍與實際讀取

僅列目錄、讀小型索引與收據、讀 ZIP central directory，並在記憶體內解析媒體 ZIP 的 `__manifest__.json`；沒有抽取或還原 blob。

| 實際批次 | ZIP 目錄讀取數 | 媒體 manifest 數 | manifest logical file records | `ai-citation-check` 原路徑／slug 命中 |
| --- | ---: | ---: | ---: | ---: |
| `G:/我的雲端硬碟/Backup/Mokaair/ai-series-continuation-20261004/20261004T172900751Z-llm-d6e2ea2352cb43b6954f38d46dcf182f` | 2 | 2 | 1,250 | 0 |
| `G:/我的雲端硬碟/Backup/Mokaair/video-upgrade-20261001/delivered-20261003-2010` | 30 | 29 | 34,341 | 0 |
| 合計 | 32 | 31 | 35,591 | 0 |

第二批的第 30 個 ZIP 是 `verification-and-cleanup-records.zip`，只讀其 central directory；不計入 29 份媒體 manifest。媒體 ZIP 採 `blobs/<sha256>` 命名，因此判斷 citation 是否在批次內，依據是 manifest 內的原路徑／slug，而非僅搜尋 ZIP member 檔名。

20261004 批次的媒體 manifest 只綁定 `ai-term-large-language-model`。20261003 批次的 `completed-roots.json` 列 24 個來源 root，`delivered-candidates.json` 列其他 11 支交付候選；兩者均沒有 citation。已讀的 `PUBLISHED-RECEIPT.json`、`BACKUP-INDEX.json`、`BACKUP-PUBLICATION.json`、`completed-roots.json`、`delivered-candidates.json` 與媒體 manifest 也沒有匹配 citation 的來源描述。

下列小型索引在本次實際讀取時計算 SHA-256，與同批 `BACKUP-PUBLICATION.json` 的預期 pin 一致；不是 GB 級 ZIP 的新雜湊或新的雲端同步證明。三檔皆位於上述 `delivered-20261003-2010` 批次。

| 檔案 | 實際 bytes | 實際／預期 SHA-256（相同） |
| --- | ---: | --- |
| `BACKUP-INDEX.json` | 55,227 | `308ae9f8b38ea1596aff3a61e35c5bb51dd8ec01dcf566cc59533472243d125e` |
| `completed-roots.json` | 16,844 | `35a78fb7ff9a10ab6b3cb853ceb26566fcee2aa9ea7e35feba8cfeb2e38f56ad` |
| `delivered-candidates.json` | 33,056 | `48223e47c1973b1e0496810422864a630a553b05cbca6a673cc34b1de6a19243` |

## C 槽查找範圍與限制

- 指定的 `<home>/mokaair-work/ai-series-continuation-20261004` metadata／收據中，citation 命中屬於 queue、backend 舊快照或來源描述，沒有 citation 專屬 archive、restore、delete 或媒體 pin 收據。`<home>/mokaair-work/video-upgrade-20261001` 在盤點時不存在。
- 擴大列出 `<home>/mokaair-work` 一至兩層資料夾，並對 handoff、renewed-finals、ai-teaching-continuation、ai-terms-resume 與 diagnostics 的 JSON／Markdown／文字／log 做 citation 路徑與收據查找，沒有找到匹配媒體或可還原的封存。
- 直接檢查 `<home>/mokaair-work/videos/ai-citation-check`，該目錄在盤點時不存在。唯一新的 citation 媒體資料夾是當次 continuation workspace 的 `<home>/mokaair-work/ai-teaching-continuation-20261007/media/ai-citation-check`，當時可列的檔案為 `approvals.json`；它不能證明舊 143 筆音訊或舊成片已恢復。
- `VALIDATION.json` 與 runbook 指向 20261003 的歷史批次，含舊 DriveFS size／MD5／pending-operations 紀錄，但沒有 citation member 綁定；歷史雲端檢查不能取代本次媒體還原驗證。

上述限制不等同於 provider 未送出、沒有未知付費 request、production 沒有媒體，或可以忽略其他製作工作。那些條件需要另以當前 runtime 與 journal 證據核對。本次沒有執行 API、native 製作命令、provider 呼叫、抽取、同步、刪除或媒體寫入，也未改動 Embedding HOLD、lease 或未知 reservation。所有本次讀取程序均已結束。
