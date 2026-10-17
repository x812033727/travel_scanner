# A01 round18 `n14` 來源歸屬中繼資料候選 — HOLD

此資料夾由 [round17](../A01-round17-source-bound-candidate/README.md) 凍結 manifest 衍生，只處理其[獨立複核](../A01-round17-source-bound-candidate/independent-review-20261017.md)指出的唯一 metadata 矛盾。六章 JSON、79 景／108 句旁白與畫面、`series.json`、`validation.json` 及來源矩陣的 **27 條 active `lines`** 都和 round17 逐位元組相同；round14–17 原檔不變。

`source-map.json` 只改 `inherited_claim_reconciliation[n14]`：保留 `active: true` 和原 `historical.verdict: NOT FOUND`，將頂層與 `current` 的現行 `source`／`source_url` 設為 `null`，明寫 `now-06/tszs` 是未附外部來源的一般物理敘述，仍為 `PENDING`。原 ABC 2010 的來源索引 6、URL 與舊 pin 移入 `prior_source`，僅作已刪空服員歸屬的歷史脈絡，不能作「輪子不減重量」的證據。`now` 章稿中的 `n14.source` 及 active `tszs` 行原已是 `null`，本輪沒有改它們，也沒有重寫舊審核結果。

`node build.mjs --write` 與 `node build.mjs --check` 都已通過：builder 核 round17 manifest 及每個檔案的 SHA-256，要求只對 `n14` 歷史／現行歸屬做上述變動，並逐條比對 27 個 active rows 和其他 reconciliation 紀錄。`node --check build.mjs` 亦通過。既有 round17 的 compose／lint／cute-story 檢查結果是 0 lint error、41 warning、0 cute-story error；本輪沒有改任何接受該檢查的輸入，不把這份中繼資料修正說成新的整稿審核。

round18 `manifest.json` SHA-256：`df5908caec1b88147b19a50b42ea992f88388750eecf4ffd681cb394707d60da`；`delta.json` SHA-256：`d7b0c3a4bd677b514c36d5682f99275ea10ebff0f471c5b2f4700a52f8e86ccf`；來源矩陣 SHA-256：`5d7a88c91f4ef0ba5348e1d4484776f7f3ca64c1749c266951e016df0b9d25c1`。基底 round17 manifest SHA-256：`fb664ada083dbd09529edfc4462d16bbb0d23d406126c5e7d76fde8622729a81`。`manifest.json` 另釘選六章、series、validation 和旁白全文雜湊。

**仍 HOLD：** 這只是離線來源表的單筆中繼資料修正。第 18 輪精確整稿尚待獨立事實與聽感複核、正式 verifier／listener／整片 narrative panel、實際 TTS 片長、MiniMax 真圖及成片播放；不得據此建立 `story/reviews/script-review.json`、寫正式主機稿、啟動付費製作、匯入 B18／後五集或上傳 YouTube。第九輪的三項敘事 FAIL 保留為歷史紀錄。
