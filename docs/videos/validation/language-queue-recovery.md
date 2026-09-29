# 影片語言佇列恢復：正式站驗收（2026-09-29）

票：`2026-09-29-verify-video-language-queue-recovery`。修正：PR #964（`eddcc3ee`），上層票
`tasks/done/2026-09-29-video-language-summary-stalls-worker.md`。

## 部署

- 站主在對話中要求重新部署。預檢：沒有暫停檔、鎖空著、沒有被規則 1 標記的發布、磁碟 59%。
- 正式站從 `717e1628` 部署到 `716bd5dc81cb2ebef51e338be5a2e6a201314226`（含 #964），部署腳本
  3/3 健康檢查通過，`DEPLOY_EXIT=0`，10:08:40 UTC 完成。沒有 migration；alembic `0113_video_flat_explainer (head)`。
- video-worker 在 10:08:14 UTC 以新映像啟動，之後 restart 0 次。

## 部署前（引用上層票的唯讀診斷）

`openai-academy-learning-paths` 的語言批次摘要有 673 字，API 上限 500 字，每五分鐘被
`summary：內容太長` 拒絕一次。worker 把它當成暫時故障而停下整輪，所以排在後面的六支影片
從 2026-09-28 16:21:52 到至少 2026-09-29 00:44:23 UTC 都沒有前進。部署重建了容器，舊容器的
log 跟著消失，所以部署前的證據只剩上層票的紀錄。

## 部署後（2026-09-29 10:08–10:57 UTC，唯讀：worker log、`video_reviews`、`video_projects`、`auto.json`）

worker log（時間為 UTC）：

| 時間 | 事件 |
| --- | --- |
| 10:08:32 | `API 服務目前無法回應`／`the Shorts knock failed`：api 容器還在重啟的那幾秒，下一步就恢復 |
| 10:08:34 | `openai-academy-learning-paths: language batch sent`（en、ja、ko 各含說明、字幕、配音；zh-CN 含說明、字幕） |
| 10:08:36–10:09:55 | `enisa-threat-landscape-2026-denominator`：旁白合成、Jev 逐句通過、影片組好、上傳包確認 |
| 10:55:28 | ENISA 的語言批次送出 |
| 10:55:30–10:56:46 | `gpt-6-sol-luna-where-to-use`：旁白合成、Jev 通過、影片組好 |

部署後 log 裡 `內容太長` 出現 0 次。

`video_reviews` 裡 gate 為 `languages`、2026-09-28 之後建立的列：

| 影片 | 狀態 | 摘要長度 | payload 裡各語系配音原因的長度 |
| --- | --- | --- | --- |
| `openai-academy-learning-paths` | approved | 74 | en 264、ja 65、ko 264、zh-CN 0 |
| `enisa-threat-landscape-2026-denominator` | approved | 74 | en 165、ja 284、ko 284、zh-CN 0 |

摘要已縮短到 500 字以內，完整的放棄配音原因仍留在 `payload.locales[locale].dub.reason`，
長度跟上層票診斷時一樣（264／65／264）。這兩列在建立的同一刻就是 approved，是既有的「依設定自動核准」語言批次，不是有人代為核准。

Academy 的其他審查（outline、audio、final、publish）決定時間都在 2026-09-26 到 09-28 之間，
部署後沒有新增或改動。`youtube_video_id` 仍有值，但部署前的值沒有留下紀錄，所以只能證明
「還在」，不能證明「沒變」；worker 的語言回報不寫這個欄位。

`video_projects`（部署後有更新的列）：

| 影片 | stage | 有 YouTube ID | 重試請求已確認 |
| --- | --- | --- | --- |
| `openai-academy-learning-paths` | languages sent | 是 | 是 |
| `enisa-threat-landscape-2026-denominator` | languages sent | 否 | 是 |
| `gpt-6-sol-luna-where-to-use` | video assembled | 是 | 是 |

上層票記下「四列停在 `retrying`、重試請求已確認」；這三列現在都已確認，而且 stage 往前走了。

`auto.json` 還是 `active` 的：`claude-opus-5-5-three-numbers`、`google-vids-omni-free-quota`、
`openai-cursor-wind-down-nov-12`、`wordpress-7-1-2-version-check`，排在 GPT-6 後面，照順序處理。

## 結論

- Academy 的語言批次已經送出，摘要在上限內，完整原因仍在 payload 裡。
- 原本被擋住的影片開始前進：ENISA 跑完到語言批次，GPT-6 已組好影片。
- 部署後沒有任何一支影片因語言送出驗證失敗而被標成 blocked，所以「驗證失敗的影片標成 blocked、
  不擋其他影片」這條路徑沒有在正式站實際發生過，只有 #964 的回歸測試涵蓋。

## 另外看到、不屬於這張票的

- ENISA 的 en 配音「retake failed」，ja、ko 配音「Jev still hears lines wrong after 2 retakes」，
  三個語系的配音都放棄，影片沒有配音照樣繼續。log 裡已經寫了下一步（修字典或譯文後 `dub --redo`），
  需要站主或內容線決定要不要重做。
- 上層票列的其他積壓（15 支 Shorts 的 QA、11 個停在 outline approved 的專案、6 支匯入的長片）
  都有各自的內容票，這次部署不會處理到它們。
