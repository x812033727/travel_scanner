# S57 R12｜技術音訊關卡

2026-10-21 UTC。此回條綁定 [R12 媒體前置政策與本地決定](../r12-media-readiness/summary.md)所列五個 SHA-256；原始旁白音檔已完成，**159／159** 句。機器音檢進行中；站主沒有親自聆聽或核准音訊。沒有生成圖片、片段、配樂、成片或上架。

`tts --dry-run` 報 Gemini `Sulafat` 準備好、159 個新請求、3,121 計費字元，月剩餘 8,488,450 字元。啟動前的[範圍及上限](tts-run-plan.json)限定本輪一個正式 `tts` 呼叫、159 個原句、3,121 字元、0 次 `--redo`，以約 US$0.81／小時的系列語音報價，13.8 分鐘預估時長的保守金額停手線為 **US$0.25**。每一景只有一句，故沒有多句拆音的付費回退路徑。`tts` 正式退出碼 0；[原樣 stdout](tts.stdout.txt)末尾記 **159 請求、3,121 計費字元、0 重用、12:56**。stderr 空白；沒有額外重錄。

[原始音訊清單](tts-artifacts.json)保存五檔創作 SHA、159 個逐句 WAV SHA、原樣工具日誌及總檔／時間軸 SHA。`narration.wav` SHA-256 `5c1865d898d4dd49999ff81a9fae5adcf3dd7b624717bf644ddb5447fa0a0f8a`；[初始時間軸](timeline.initial.json) SHA-256 `fffd18e940ea7d10cfecd91757753884cfc5b8d20c64d0ccacf0b3e22f298e3f`，30 fps、23,308 格，即 **776.93 秒＝12:56.93**。本機工作檔在 `/workspace/.video-work/curio-s57/`，不在 repo；回條保留其逐檔雜湊供後續核對。

依[一次音檢範圍](check-run-plan.json)，正式 `check-audio` 只跑一輪：最多 159 句初始轉寫，文字不符時 Jev 每批最多 40 句、全不符最多四批，沒有第二轉寫工具，也沒有本輪重錄。待完成後再記實際逐句結果及網站 audio 卡片狀態；此時不判音檢 PASS，也不把本地大綱／劇本續作決定當成站主音訊核准。
