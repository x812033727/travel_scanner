# 原來如此事務所：目前採用規格

2026-11-01，依站主「用奇聞檔案局的新規則來優化、整理並剔除不好的題目、補更好的題目，可參考十萬個為什麼」。

**新選題從 [30 支逐集規劃](refresh-20261101/EPISODES.md) 開始，完整規格在 [新版製作規格](refresh-20261101/SPEC.md)。素材池擴充到十萬筆以上的方向見 [素材池規劃](refresh-20261101/POOL-STRATEGY.md)。**

**2026-11-14 畫風、語音與成片觀眾評分現行定案**（站主拍板「以後用這種的」「把觀眾評分加入流程，修完後才推後台跟備份」）：雙人對話版（所長＋小問）停用 MiniMax 生圖，全面改由代理內建 `generate_image`（`16:9` 滿版＋系列角色設定圖鎖臉）生成**「劇場級動畫光影 × 厚塗水粉質感」**後以 `keyframes import --provider external --usd 0` 匯入；中文語音（`zh-TW`）固定用 Gemini（`Sulafat`＋`Leda`），八語配音（`en,ja,ko,es,pt,id,vi,th`）固定用 MiniMax（`dub --provider minimax`）；成片組裝與 `qa`（11/11）通過後，**必先由未參與製作的獨立子代理完成一般觀眾視角評分（`review/audience-review.md`），把縮圖、畫面、節奏或包裝瑕疵全數修完並重過 `qa`，最後才執行 Google Drive 完整備份與 `review-push --gate final`**。開拍前必讀 [`look.md`](look.md)、[`thumbnails.md`](thumbnails.md)、[`dialogue-pilot-20261103/README.md`](dialogue-pilot-20261103/README.md) 與 [`../lessons/sothatswhy.md`](../lessons/sothatswhy.md)。

站主後續要求按片長與內容厚度篩選，相關題目可合成一個主題。現有 313 筆來源先篩出 100 題素材，再以其中 44 題組成 30 支候選；其餘 25 題短片、26 題補強後重評、5 題暫緩。十萬筆是後續目標，目前未建成；100 題也不再等於 100 支固定 13 分鐘影片。
三季原始題庫、查核包、五語文案、排程與既有影片是歷史來源；新版以逐題處置決定是否仍適合開新長片，不刪原稿、不沿用舊核准。

這次完成的是編輯規格、題庫取捨與本機查詢入口。共用主機工人的提示詞、後台題庫與已上架影片不會因這份文件自動改變；正式同步見新版交接。

```powershell
node tools/video/so-thats-why/cli.mjs check
node tools/video/so-thats-why/cli.mjs list
node tools/video/so-thats-why/cli.mjs brief P01
```

`list` 列單集企劃，`topics` 列初篩素材。`brief` 以整支企劃帶出每題來源、主線、片長估計、刪減條件與最新規格；不是可直接匯入的已審劇本，也不呼叫付費服務。用入選素材 ID 會導向其母企劃，退下長片清單的題目拒絕輸出 brief，須用 `show <id>` 查兩輪取捨理由。
