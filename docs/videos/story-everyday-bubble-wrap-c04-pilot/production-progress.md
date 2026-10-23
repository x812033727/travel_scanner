# C04 Bubble Wrap｜本機試片製作進度

本頁接續 [站主核准收據](approval.md)，記錄已執行的關卡及暫停原因。影像、音訊與影片素材放在本機 `<home>\mokaair-work\videos\story-everyday-bubble-wrap-c04`，不進 Git。原稿 PR #1670 仍為草稿。

## 2026-10-22 03:41 UTC：旁白供應商 429 暫停

- 起點：本片媒體工作目錄原先不存在；基底與本片均無 `STOP`。`media-status` 顯示本片 US$0.00、0 張圖、0 首配樂、0 次評審；網站媒體月額可用。`tts --dry-run` 顯示 94 個請求、3,086 計費字元、`Sulafat` 當時為 ready，本月字元尚餘 7,887,491。
- 核准：依站主 2026-10-22 對**定稿三份檔案**及本機試片的明確授權，已以本機 CLI 記錄 `outline`、`script` gate；`status` 讀回企劃、獨立查核、腳本均有效。這不等於音訊、圖片或成片驗收。
- 首次正式執行 `node tools/video/cli.mjs tts --slug story-everyday-bubble-wrap-c04 --workdir <home>\mokaair-work\videos`，約 38 秒後結束，訊息為「Gemini 語音暫時忙碌或達到用量上限，請稍後重試」；原始服務分類在程式中為 `video_speech_upstream_busy`，屬 provider 429。
- 結束後唯讀查核：本片工作目錄只有 `approvals.json` 與空的 `audio/speech-journal/`；沒有 `cache.json`、WAV、`timeline.json`、`narration.wav`、影像／配樂目錄或媒體台帳，也沒有基底／本片 `STOP`。目前可確認**零個成功 TTS take**、**零個未知結果的 journal 項目**；無影像或配樂購買。
- 此非本月字元預算不足的 `video_speech_budget_exhausted`。現行 client 對帶回的 429 視為已結清拒絕，speech journal 會移除該請求；網站 API 對本片這種非 pilot slug 的 Gemini provider 429 會釋回保留的月字元。未持有網站供應商帳單逐筆明細，故不把美元費用寫成零；本機沒有可計入的成功 take。
- 依 `curio-episode` 對此 429 的規則，**HOLD，不連續手動重送**。若是當日額度，太平洋午夜夏令時間約為 **2026-10-22 07:00 UTC／15:00 台北**；下次可在重置後先做一輪狀態／journal／STOP 讀回，再受控續跑。此為時間推定，不是供應商已確認的恢復承諾。

## 續跑前與停線

1. 讀回 `approval.md` 綁定的三份 SHA-256、空 journal、既有 take、STOP、網站媒體台帳與本片 US$25 餘額；若有新未知項目先停。
2. 只續跑**同一 slug／同一 workdir／同一腳本**的 `tts`；不使用 `--force`，讓 cache／journal 保留已成功素材。若再次是 provider 429，維持 HOLD 並記下新時間，不買圖。
3. TTS 全數完成後，以同資料夾的 `measure-body.mjs <本片媒體工作目錄>` 分開計算第 02–06 章所有 WAV 的**解碼後純語音長度總和**，以及該章在實測 `timeline.json` 中的起迄；它還核對定稿語音雜湊、每句 WAV/cache 雜湊與時間軸樣本數。純語音必須至少 **480 秒**，時間軸不能代替純旁白。若不足，先做有來源的腳本修訂及覆核，重新確認站主腳本關卡，再考慮圖像。
4. `check-audio`、84 張上限與每鏡累計三次、配樂一首與**實際可解碼音檔時長**、本機合成和 QA 逐關紀錄。音樂的請求秒數或快取命中不能代替實際交付長度；不得為短音檔自動重買。全片任何已花、保留或未知費用都按 US$25 硬停線保守處理。
