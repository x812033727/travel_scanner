# 九語旁白參考字幕句內對時：實際交付

本輪已在[本片後台](https://mokaair.com/zh-TW/admin/videos?video=kimi-k31-3d-delivery)更新實際變更的en、es、pt、id、vi、th字幕，並保留每份被替換的舊字幕。現在35個附件已正常完整下載並逐檔核對。九語仍為1364cue，當前字幕速度提醒由47減為23，剩餘提醒照實保留。

| 語言 | cue數 | 原速度提醒 | 當前速度提醒 |
| --- | ---: | ---: | ---: |
| zh-TW | 119 | 0 | 0 |
| en | 134 | 2 | 1 |
| ja | 185 | 3 | 3 |
| ko | 182 | 0 | 0 |
| es | 165 | 15 | 6 |
| pt | 158 | 10 | 4 |
| id | 164 | 13 | 8 |
| vi | 141 | 3 | 1 |
| th | 116 | 1 | 0 |

[新版九語SRT／VTT](../../../captions/reading-balanced/README.md)保留完整文字、切句、cue數、順序與每句首尾時間；只重分配本來有足夠時間的句內邊界，沒有改稿、拉長時間窗、合成或重新轉寫。[原生完整九語複核](root-nine-locale-caption-review.json)、[當前完整元件報告](actual-component-report.txt)及[實際原生流程](native-caption-lifecycle.json)記錄結果。

這些仍是繁中旁白時序的外語參考字幕，不是外語dub對時。繁中原聲、正式片頭片尾、114句原文、912句翻譯與全部逐句WAV不變；114句仍待實際聽校，八語合格M4A仍0/8。原全片QA維持10/11整體false，47項字幕速度及3項歷史縮圖提醒、R4false、未知ASR與全域保留槽皆原樣。[原47項元件紀錄](original-caption-findings47.json)、[原字幕manifest](original-caption-manifest.json)、[原整片QA](original-whole-QA.json)與[更新前完整進度](before-caption-pacing-progress.json)保存日期與原始結果。

[原生程式與全部單元測試歷史](code-and-unit-evidence.json)和[最終55項測試原始輸出](unit-tests-final.stdout.txt)分開記錄。第二次測試因錯誤EN浮點案例而實際失敗，原stdout／stderr及描述符保留；後改為真實Thai浮點案例，再完成原繼承邏輯不變的最終版本。沒有把失敗改成PASS，也沒有降低字幕門檻。

[後台實際更新摘要](actual-backend-caption-delivery.json)、[正常完整附件清單](normal-caption-review-files.json)、[Root逐檔實體驗核](root-final-binary-readback.json)及[本輪里程碑](actual-caption-pacing-milestone.json)記錄唯一交付。舊公開收據與先前字幕不覆蓋，原始媒體／privateproject／auth／profile／release不複製進Git。父票仍blocked，來源／旁白／成片核准、上架包及語言批次未完成；沒有合併、部署或YouTube上傳。
