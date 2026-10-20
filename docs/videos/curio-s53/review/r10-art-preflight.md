# S53 R10｜音訊送審與插圖非付費預檢

2026-10-20 UTC。本收據不作網站核准或插圖放行；沒有呼叫付費插圖、評審、配樂或影片生成。

## 網站音訊卡

依 [R10 語音驗證](../verify-10.md)，現有 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`，126／126 官方音檢零旗標；`audioEvidenceProblems` 為空。工作目錄沒有 `auto.json`。執行 `review-push --slug curio-s53 --gate audio` 後，網站讀回音訊卡 ID `09dbb49f-a0a4-4f02-b886-d1e4e7a0531d`，`content_sha256` 正是上述 timeline SHA，`hand_pushed=true`、`status=pending`。企劃及 R10 劇本卡也仍 `hand_pushed`、`pending`。先前本機以站主常設「用推薦的決定」記錄的 R10 劇本委派編輯選擇，與這三張網站待審卡分開；沒有記入任何網站核准。

## 插圖報價與現有來源審查

非付費指令：

```sh
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s53 --dry-run
```

工具列出 **116 個 `shot`、0 個 end frame、每景最多三次 take**，伺服器 `minimax image-01` 為 1K，**每景一次約 US$1.57，全景最多三次約 US$4.70**。隨後 `media-status --slug curio-s53 --json` 讀回單片 `max_usd_per_video=US$200`，本片已花 **US$0.00**、0 張圖、0 個 judge call、0 個預留額度。這些是估價和額度快照，未形成實際圖檔或花費。

網站全域額度同一快照為：圖片 **18,682／20,000 已用，餘 1,318**；judge calls **19,985／20,000 已用，餘 15**；音樂 **60／60 已用，餘 0**。額度會隨其他集數變動；插圖開始前應重查，尤其 15 次剩餘 judge call 不能覆蓋 116 景的逐張評審，音樂也須有可用額度才可製作。依協調者的 S51／S49 生成順序，本次停在預檢，未呼叫付費 `keyframes`。

現有 **116 個書面插圖提示詞**已有逐版獨立來源及視覺核對：R3 全量讀過 120 個當時 `shot` 與七張數字卡，書面畫面 PASS；[R5 獨立審查](r5-source-independent.md)修復中間版本的畫面 HOLD 後來源／畫面均 PASS；R6–R9 各輪來源差分審查承接未改提示詞並核改動；[R10 獨立審查](r10-source-independent.md)核對最後六個改過的提示詞 `s53083/099/100/101/103/104` 與目前五檔精確 SHA，書面畫面 PASS。只要五檔不變，付費前無須再重做**書面**提示詞來源審查。日後每張實際生成圖仍須依系列規則過圖像評審及內容／畫風驗收，再走 `storyboard` 站主關卡。
