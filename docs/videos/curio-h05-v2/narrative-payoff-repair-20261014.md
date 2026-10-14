# H05 v2｜圖卡後的敘事回扣與正式語音

`open-note` 改用原生示意卡後，第一次獨立盲審對新版稿的 `payoffs` 回答否：`h5v028→h5v029` 的再起飛答案和 `h5v098→h5v103` 的浸水順序答案，雖然有回答，卻沒有明確點名各自先前的問題。只改兩句答案：`h5v029` 加「再起飛，是因為……」，`h5v103` 加「剛才問的先後順序……」。沒有更改日期、數值、來源主張或其他句子。第二位只讀新稿的獨立審稿者回答 **11/11 是**，`review/narrative.json` 綁定 `narrative_hash=31f279e4aaa020c5`、無 failed 或 advisory。答案保存在外部 `review/native-card-audio-refresh-20261014/h05-blind-answers-round2.json`。

這兩句變動讓旁白快取出現 2 筆待合成，dry-run 估 **53 計費字元**；正式 TTS 實際只合成 `h5v029`、`h5v103`，沿用其餘 100 段，沒有重買其他句子。送出前把舊 `timeline.json`、整段 `narration.wav`、核准與逐句檢查逐檔複製並驗 SHA 到外部 `review/native-card-audio-refresh-20261014/before/`。新版 speech hash `0b7b642f114d257f`，正式 `timeline.json` SHA-256 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee`，整段 WAV SHA-256 `f0ce6fff529dfb60a72c0e7b4479938d48f6f476ca5961b7ea2190ba15f6feac`。108 個 line ID 順序與場景起訖連續；只有上述兩句的音檔 SHA 與樣本數變更。

正式 `check-audio` 覆蓋 **108/108**：只新增 2 次轉錄、0 次新 Jev 判斷；`h5v029` 與 `h5v103` 均是 exact match，原有 12 個旗標完全一致。`review/check.json` SHA-256 `096b37442681dd5331121573ffb76470a75edd43e18f966734a844e27362fe3f`。實際正文 **16,204 幀／30 fps＝540.133 秒**，61 個 `shot` 佔 9,490 幀／**58.5658%**；108 個畫面狀態最長 235 幀／7.833 秒，`cadenceProblems=[]`。這些數字是音訊與分鏡檢查，尚非完成畫面或播放器字幕驗收。

舊音訊核准只綁 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`。新版已 `review-push --gate audio` 到 `/admin/videos`，回報 **pending**；須由站主聽審並 `review-pull --gate audio` 讀回新版雜湊，不能把舊核准轉用。其餘 61 個插圖鏡頭、縮圖、完整 render、成片 QA、正式繁中 CC、上傳包與播放驗收仍待完成。
