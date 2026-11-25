# 原來如此事務所：目前採用規格

2026-11-01，依站主「用奇聞檔案局的新規則來優化、整理並剔除不好的題目、補更好的題目，可參考十萬個為什麼」。

**新選題從 [30 支逐集規劃](refresh-20261101/EPISODES.md) 開始，完整規格在 [新版製作規格](refresh-20261101/SPEC.md)。素材池擴充到十萬筆以上的方向見 [素材池規劃](refresh-20261101/POOL-STRATEGY.md)。**

**2026-11-25 Google Flow 動畫化長片與去 GitHub 化新規則**（首支試作 P02 `sothatswhy-p02-cloud-rain-flow` 定案）：完整規格見 [`../explainer-series/FLOW-PRODUCTION-RULES.md`](../explainer-series/FLOW-PRODUCTION-RULES.md)（方案 B 動靜混剪 35–40 支 Flow ≤ 500 點、開拍前全片三視角盲審 ≥ 8.5、先 0 點數 `Nano Banana 2.1` 生圖 QA 才進 `Omni 1.2 Flash`、長鏡多鏡位防卡頓、逐句 CPS 巡檢、雙引擎 `-14 LUFS`、`heimao-left` 本機字體鎖定，以及**成片盲審通過後定稿腳本／`i18n`／審片報告一律直存雲端 `製作檔/<slug>/腳本定稿/`、0 GitHub Commit**）。

**2026-11-14 畫風、雙系列人物分家、無人機制鏡比例、語音與成片觀眾評分現行定案**（站主拍板「以後用這種的」「把觀眾評分加入流程，修完後才推後台跟備份」「不一定每一個畫面要都有人；原來如此跟奇聞兩系列人物造型不同」）：雙人對話版停用 MiniMax 生圖，全面改由代理內建 `generate_image`（`16:9` 滿版）生成**「劇場級動畫光影 × 厚塗水粉質感」**後以 `keyframes import --provider external --usd 0` 匯入；有角色鏡 `ImagePaths` **必傳 Repo 內正式 2.5 頭身 Q 版設定圖**（[`series-sheets/characters/chief/chief-canon-v2.png`](series-sheets/characters/chief/chief-canon-v2.png) 與 [`series-sheets/characters/kid/kid-canon-v2.png`](series-sheets/characters/kid/kid-canon-v2.png)，與《奇聞檔案局》3.5 頭身修長比例研究員 `Ada` 嚴格區隔，禁用舊版 MiniMax 失敗設定圖）；**全集不必每鏡都有人**，約 **45%–65%** 鏡頭應設為 `"nobody": true` 直接畫純機制剖面、物件微距與數量對照，角色鏡頭約 **35%–55%** 留給提問、反應、轉折與首尾；中文語音（`zh-TW`）固定用 Gemini（`Sulafat`＋`Leda`），八語配音（`en,ja,ko,es,pt,id,vi,th`）固定用 MiniMax（`dub --provider minimax`）；成片組裝與 `qa`（11/11）通過後，**必先由未參與製作的獨立子代理完成一般觀眾視角評分（`review/audience-review.md`），把縮圖、畫面、節奏或包裝瑕疵全數修完並重過 `qa`，最後才執行 Google Drive 完整備份與 `review-push --gate final`**。開拍前必讀 [`look.md`](look.md)、[`series-sheets/README.md`](series-sheets/README.md)、[`thumbnails.md`](thumbnails.md)、[`dialogue-pilot-20261103/README.md`](dialogue-pilot-20261103/README.md) 與 [`../lessons/sothatswhy.md`](../lessons/sothatswhy.md)。

站主後續要求按片長與內容厚度篩選，相關題目可合成一個主題。現有 313 筆來源先篩出 100 題素材，再以其中 44 題組成 30 支候選；其餘 25 題短片、26 題補強後重評、5 題暫緩。十萬筆是後續目標，目前未建成；100 題也不再等於 100 支固定 13 分鐘影片。
三季原始題庫、查核包、五語文案、排程與既有影片是歷史來源；新版以逐題處置決定是否仍適合開新長片，不刪原稿、不沿用舊核准。

這次完成的是編輯規格、題庫取捨與本機查詢入口。共用主機工人的提示詞、後台題庫與已上架影片不會因這份文件自動改變；正式同步見新版交接。

```powershell
node tools/video/so-thats-why/cli.mjs check
node tools/video/so-thats-why/cli.mjs list
node tools/video/so-thats-why/cli.mjs brief P01
```

`list` 列單集企劃，`topics` 列初篩素材。`brief` 以整支企劃帶出每題來源、主線、片長估計、刪減條件與最新規格；不是可直接匯入的已審劇本，也不呼叫付費服務。用入選素材 ID 會導向其母企劃，退下長片清單的題目拒絕輸出 brief，須用 `show <id>` 查兩輪取捨理由。
