# S38 R8y｜PF012 私人圖單離線重綁

2026-10-22 UTC。R8y [作者單一提示詞窄修](verify-79-r8y-pf012-final-prompt-author.md)及[非作者紙審](verify-80-r8y-pf012-final-prompt-independent.md)通過後，在 STOP 在位、jobs 空、沒有媒體呼叫的狀態，將私人圖單從 R8x 重綁到 R8y。這只證明 10 張既有合格圖可保全，**不等於** PF012 新圖或完整分鏡已驗收。

R8y `video.json` SHA-256 `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`；工具計算新 `visual_hash=099da572e40ba916`、不變 `look_hash=98a370ae40badbaf`。舊 manifest SHA-256 `e7e5b8f1977110b2fc3bb09d4c25a19dcfe49cab4030698292536d6bf403b49d`，備份在私人 `rebind-backups/r8x-manifest-before-r8y-pf012-final.json`。離線原子寫入後、付費試畫之前的新 manifest SHA-256 `3eeaeb1d31a60e982c843dc95bb1fc89ca17ab5bd1acb50680cb43c0736b5621`：只改 `visual_hash`、移除人眼退件的 `shots.pf012`，並清空含舊圖的 contact sheet 引用；縮圖來源仍是合格 `pf002`。兩張先前 PF012 原圖與裁圖另備份在私人 `rebind-backups/r8x-pf012-seed-images/`，四檔 SHA 與[退件審核](verify-78-r8x-pf012-seed2-human-reject.md)相符，避免新 seed 1 同名檔覆寫舊證據。

另外 10 個 KEEP 的完整 JSON 條目逐項與舊圖單相等；10 張實際所選檔案的 SHA-256 全部符合 manifest，見[逐張清單](verify-81-r8y-pf012-offline-manifest-inventory.json)（SHA-256 `45b8b341531e2a0b2d04e3536cd89568207bd94997c9ff01f4853481a057dbc5`）。正式 `keyframeProblems` 對 10 張 retained 圖為 0；對全片仍有 95 張缺圖，包括 PF012，而 PF015 仍是 `big` 來源卡。ledger 前後 SHA-256 `368cd9664468db66de264216fe5bc591d9086768150af028109fb057c5259b9e`，累計 US$0.7415／49 images／49 judges／1 music，另有舊 US$0.0035 reservation；低於 US$4.58 上限。STOP 在位、jobs 空。

重綁後才允許 PF012 **最後一張**實際原生圖與一次 judge；即使新 prompt 的種子重新從 1 編號，累計實際原圖仍按先前兩張加一張計，不能再補第四張。必須目視新原圖；機器分數不代替歷史畫面覆核。
