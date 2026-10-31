# S53 R22｜`s53018` 第三／最後原生圖獨立退件與停線

2026-10-22 UTC。**HUMAN REJECT FINAL；不買第四張 `s53018`，亦不買第四張 `s53010`。**本回獨立看了 1280×720 未裁原圖及工具所選裁圖，對照已 [紙審 PASS 的 R22 提示詞](r22-s53010-card-s53018-prompt-independent-paper.md)、固定史料與 R21 退件原因。圖像及帳本仍在私人工作區；沒有追加 image、judge、音樂或其他付費呼叫。[逐圖與 14 張 KEEP 清單](r22-s53018-final-native-inventory.json)綁定以下 SHA。

## 原圖判定

固定 1913 年 *San Francisco Relief Survey* 原檔 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，[L4848–4853](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4853)只支持 South Park 面積不足以放分開的小屋，**不記實際帳棚間距**。R22 將畫面明標為概念示意；提示詞要求一名灰髮成年工作者胸肩近景、側身擠過兩道相鄰帳棚牆，外套擦過兩牆、側臉、帆布填框。這是讓「空間不足」可讀的核心動作。

| 畫面 | SHA-256／機器結果 | 人工所見 |
| --- | --- | --- |
| 未裁原圖 `keyframes/s53018-1.jpg` | `17f2e4e9803fa0a5136b58c2db5b093a2cd0a40611ca2ed3785fa1c3c849225a`；1280×720 | 成年灰髮與 2D 系列畫風大致成立，沒有 R21 的照片式背景；但人物正面站立、軀幹幾乎全見，兩側帆布像打開的寬帳門，外套未貼牆，也沒有側身擠過的動作。 |
| 所選裁圖 `keyframes/s53018-1-trim.jpg` | `cfc3f5c7215a61c1935ebd0102e776da314298e618e537e396bfa72e8dac74a5`；1280×720 | 裁掉左側紙邊但未改視線方向或可見寬度；仍是正面立在開口中，沒有狹縫中的物理擠壓。 |

正式 judge **9.29／10 PASS**，但 `details` 本身寫「character faces forward instead of seen in profile squeezing between canvas walls」。R22 是 R20 實圖、R21 第二實圖失敗後的**第三／最後實圖**；這次解了照片式背景，卻重複了寬通道／未側身的主要失配。這不是從史料推出確切帳棚距離的要求，而是已簽核的概念畫面未呈現「放不下」；若作本句分鏡會給出寬敞營地的反向視覺訊號。故機器 PASS 不能代替本輪人工 KEEP，**此圖 REJECT FINAL**。

## 私人圖單、既收圖與費用

凍結 `video.json` SHA `49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`、`claims.md` SHA `34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`；正文／口播未改。試畫前安全 [R22 離線重綁](r22-s53010-card-s53018-offline-manifest-rebind.md) manifest SHA `96ef6a6d67c03fd37f86963f819f5bdbafce8c72fbb9f04d0bb983b371a04ef5`、`visual_hash=133eba68d1a96469`，14 張人工 KEEP。最後一次原生及 judge 後 manifest SHA `71276a573a6f7a8901151a37000ccc571b120b10e4540bc095c8bf984b5bb2cd`，暫含機器 PASS／人工 REJECT 的 `s53018` 選圖、key `acccb8d34754f6a4` 與舊 contact sheet；已備份到 `/workspace/.video-work/curio-s53/rebind-backups/r22-s53018-final-native-before-human-reject.json`，備份 SHA 相同。原圖／裁圖保留私人工作區作證據。

在 `STOP` 在位且 jobs 空的條件下，將唯一退件 `shots.s53018` 刪除、contact sheet 引用清回 `null`／`[]`，並恢復原先 `generated_at`；以 mode `600` 原子寫入，**逐位元組還原試畫前安全 manifest SHA `96ef6a6d67c03fd37f86963f819f5bdbafce8c72fbb9f04d0bb983b371a04ef5`**。14 張舊 KEEP 的完整條目、request key、所選路徑及實際檔案 SHA 與試畫前逐項一致；縮圖仍為 `s53005`。工具 `keyframeProblems` 對這 14 張得 0 問題；整集 114 張 `shot` 中仍有 100 張缺合格圖，`s53018` 列為缺圖，`s53010` 正確為來源卡。退件圖與舊 contact sheet 不在目前圖單。

帳本由 **US$0.4590／35 image／34 judge** 增至 **US$0.4725／36 image／35 judge／0 預約**，新增 US$0.0135，仍低於整集 US$4.78 上限；現 ledger SHA `dc7aaf8ca062b7680113bde534ce7d1cbdc218ab5567626f0365f6fa39dfc01f`，jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`、jobs 空、`STOP` 在位。下一步由作者比較同章已收圖重用或來源卡，另人紙審後才處理圖單；本回不核准 `s53018`、第二章分鏡或完整成片。
