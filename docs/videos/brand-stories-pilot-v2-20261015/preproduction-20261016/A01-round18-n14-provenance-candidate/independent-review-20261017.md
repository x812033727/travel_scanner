# A01 round18 `n14` 來源歸屬獨立複核 — 局部 PASS／整片 HOLD

日期：2026-10-17（台北）。本覆核只判定 round17 → round18 的一筆來源中繼資料修補。它不重新審核 108 句整稿、實際圖片或正式主機稿，也不是 `story/reviews/script-review.json`。

## 精確版本與機械檢查

| 檔案 | 本機重算 SHA-256 |
| --- | --- |
| round17 基底 `manifest.json` | `fb664ada083dbd09529edfc4462d16bbb0d23d406126c5e7d76fde8622729a81` |
| round18 `delta.json` | `d7b0c3a4bd677b514c36d5682f99275ea10ebff0f471c5b2f4700a52f8e86ccf` |
| round18 `source-map.json` | `5d7a88c91f4ef0ba5348e1d4484776f7f3ca64c1749c266951e016df0b9d25c1` |
| round18 `manifest.json` | `df5908caec1b88147b19a50b42ea992f88388750eecf4ffd681cb394707d60da` |

`node build.mjs --check` 退出碼 0，回報 79 景／108 句、旁白改動 0、active 來源表行改動 0、現行 `n14.source=null`、歷史來源索引 6。這只是候選產物的位元組與規則檢查；沿用的 `validation.json` 並非新一輪整片審核。

## 獨立差異核對

我另外直接逐位元組比較 round17 與 round18：六章 `candidate/chapters/*.json`、`candidate/series.json`、`validation.json` 全相同，round18 manifest 對應的六章、series、validation 與 narration SHA 也維持 round17 值。解析兩份 `source-map.json` 後，27 條 active `lines` 的內容與順序相同，其他四筆 `inherited_claim_reconciliation` 亦相同。

獨立遞迴差異只落在 `inherited_claim_reconciliation[4]`（`id=n14`）的八處：頂層 `source`／`source_url`／`pin`／`note`，`current.source`／`current.source_url`／`current.note`，以及新增 `prior_source`。沒有動 `active: true`、現行 claim 文字與 `PENDING` 判定；舊 `historical` 物件逐欄相同，`NOT FOUND` 判定原封保留。

新語意也一致：現行 `now-06/tszs` 的「輪子能幫忙移動，卻不會減掉重量。」是未引外部來源的一般物理敘述，章稿 `n14.source`、active `tszs.source_index`、對照表頂層和 `current.source` 都是 `null`。舊索引 6、[ABC 2010 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) URL 與舊 pin 完整保存在 `prior_source`，只記錄已刪空服員歸屬的歷史，不能再拿來證明重量敘述。本次修正消除了 round17 審查所指出的「active 卻仍指 ABC」歧義。

## 結論

**PASS_METADATA_DELTA_ONLY**：round18 的唯一來源歸屬修補、27 條 active 行不變、舊 `NOT FOUND` 歷史保留、檔案雜湊與 `--check` 均已獨立核對。round18 仍是 `HOLD_UNREVIEWED_OFFLINE_CANDIDATE`；round9 三項敘事 FAIL 沒被新整片 panel 取代。正式 verifier／listener／敘事審核、真實 TTS 片長、MiniMax 圖像與成片播放仍未完成。此局部 PASS 不授權正式審稿收據、主機寫入、付費製作或上架。
