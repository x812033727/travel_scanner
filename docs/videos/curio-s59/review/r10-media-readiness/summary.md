# S59 R10｜站台稿件與有限額語音前置紀錄

2026-10-21 UTC。承接 [R10 正式文字關卡](../r10-merge-policy/summary.md)：來源、110 句／124 引註、100 張書面分鏡／10 張卡與雙讀者固定 OR 13／13 均 PASS。本紀錄綁定 `research.md` `39a48f08…`、`brief.md` `9d68d7b4…`、`claims.md` `5f3066ba…`、`video.json` `70487214…`、`script.md` `94acc30b…`，完整 SHA 見[首輪語音計畫](tts-run-plan.json)。

`review-push --report-only` 將 S59 列入 `/admin/videos`，未送審。`review-push --gate outline` 提交 R10 `brief.md`；Jev 選推薦 A（符合立場 0.86，選案信心 1.00），但因本片不是網站 worker 自製，網站卡仍為 **pending**。`review-push --gate script` 提交 R10 `script.md`，網站卡也是 **pending**。各自 `review-pull` 回 `waiting for the owner`、exit 3；原始輸出與結束碼保存在此資料夾。

使用者已持續委託「用推薦的決定就好不用問我」及持續製作。因此本地 CLI 依 Jev 推薦選 A，並依 R10 獨立來源、書面畫面與正式雙盲結果採用此版劇本，兩筆決定均綁定精確 SHA。[本地決定快照](local-approvals.snapshot.json) SHA-256 `df66cfa4ad9d00cc918dbc2153ed4d07f5a3f20a83affd061dcc3c5dac3126e9`；註記明說**站主未親自審讀此版，網站卡仍待站主決定**。這兩筆本地決定僅用於授權後續有限額製作。

[完整口播政策請求](policy-request-body.json) SHA-256 `5fb30b09f718efb96da7c490440bb113f7416516a00985af0aba2dc4bf96a3a0`，單次 Jev 呼叫的[原始回覆](policy-response.raw.json)與[判讀收據](policy-receipt.json)均已封存；**PASS**，符合立場 0.80、示範不適用於解說、建議 0.01、業配 0.06。程式在送出前鎖定五檔並落盤一次送出標記，禁止自動重送。

`tts --dry-run` 回 110 次、全需合成、3,182 計費字元；`gemini:Sulafat` ready，當時網站剩餘 8,484,681 字元。先寫[首輪語音計畫](tts-run-plan.json)：一次原稿、最多 110 個成功請求與 3,182 字元、保守 US$0.25 上限、零重配。

首輪 `tts` 結束碼 **0**，110 次成功、實際 **3,182 計費字元**、0 重用、0 重配；工具報旁白 **12:31**。110 份逐句 WAV 齊全，`ffprobe` 驗 `narration.wav` 為 751.866667 秒；檔案 SHA-256 `7de1b9fa1b9a7eb8def3f26ca05684f1a8bed3a4698e7f3cf8166c4961d7bd38`，`timeline.json` SHA-256 `8c0763b7f90537227390e966d4fa8ff2fba1c0ad05af46914007d408b80f2952`，時間軸含 110 句、六章。[逐句音檔清冊](audio-manifest.json) SHA-256 `63e9b9699bfab9d3a42bbd22a72603cff3e87428ae6a389f3f4424803b1cf77c`，驗每一 ID、音檔 SHA 與 48 kHz／單聲道／16 位格式。按系列估價約 US$0.81／小時，這段長度約 US$0.17，低於本輪 US$0.25 保守上限；網站實際帳單要以網站為準。合成後第二次乾跑顯示 0 待補、0 計費字元。五份創意檔 SHA 均與 R10 凍結值相同。逐句音檢正在執行；音訊／網站音訊卡與生成圖皆另需驗收。

方便後續聽審的本地壓縮檔為 `/workspace/.video-work/curio-s59/narration-preview.mp3`，9,023,084 bytes，SHA-256 `d41c335f0478111b0899219f9c2f234c879ada6c2c44d91fe90ae5486b7fa3af`；它尚未得到音訊核准，且未納入版本庫。
