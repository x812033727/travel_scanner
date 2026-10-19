# S08 旁白重錄及音訊審核待決

2026-10-19 21:56 UTC。劇本保持獨立盲讀 13／13 的確切 SHA-256 `54974b5cb36c0f3ecbc889fe4bc84c185a4bcd53f75964a47d684e1d307c4113`；`video.json` SHA-256 `721671fbce11eb96d6d3d502505a7ab83a2e100d5f06db5deff12e1fdf1e63d4`。93 句 Gemini Sulafat 旁白合成完成，實測長 **591.633 秒（09:51.633）**，`narration.wav` SHA-256 `5f6361d54dd652b33c74e8b9bbedaa1b3f0bab9d4e2462ee5def601651610abd`。首次現稿音檔複查標出 10 句，已依 `/workspace/.video-work/curio-s08/review/check-flags.json` **只重錄那 10 句**，另 83 句沿用；此次 TTS 233 個計費字元。

重錄後 `check-audio` 完整檢查 **93／93**：57 句逐字相符、24 句只差同音字或語助詞、5 句由 Jev 判為可接受，**7 句仍被標記，指令退出碼 1**。確切機器報告在 `/workspace/.video-work/curio-s08/review/check.json`（SHA-256 `5eb15ff1951d8ceac0052bbfd8d370e037ed0be1397f3d2e81f5e1b530e65e2c`），標記清單在 `review/check-flags.json`（SHA-256 `4167e52df98113019e8d5bb4763f13e693a9f9b9aac5f12b4bf3397c875cdc02`），輸出在 `check-audio-redo.log`。未把退出碼 1 說成合格。

| 句號 | 原稿／轉寫差異 | 尚不能排除的風險 |
| --- | --- | --- |
| `ox009` | 運糧／月亮 | 同音近音；短句孤立轉寫不穩 |
| `ox012` | 始以木牛運／時以木牛運 | 原文首字聲調不同，須核實是否唸「始」 |
| `ox017` | 糧盡退軍／梁敬退軍 | 原文四字被辨為近音人名 |
| `ox077` | 流馬／劉滿 | 專名被辨為近音人名；前輪曾辨為羅馬 |
| `ox079` | 流馬、接點／流碼、節點 | 同音及聲調差；前輪無法轉寫，此輪可轉寫 |
| `ox107` | 疑神鬼／疑神疑鬼 | 常見成語補字，可能是辨識正規化或實際多唸一字 |
| `ox087` | 三年的運糧句子／三言兩語的句子 | 文意可能變，不能只按同音字放行 |

7 句皆已歷經既有重錄及此次定向重錄；再次以同稿盲目重錄沒有可靠的改善依據。此雲端沒有可用的 Whisper 模型權重，外部模型來源曾被代理拒絕；代理的音訊輸入也無法播放本機 WAV，因此**沒有獨立第二轉寫或人工實聽**。不能因轉寫像同音字就宣稱聲音正確，也不應只為迎合 ASR 而修改已通過的劇本。已 `review-push --gate audio` 將本次旁白及 7 句標記送至站台 `/admin/videos`，回覆為 **pending、由站主決定**。本機 `status` 仍顯示 `narration approved: not approved yet`；尚未代站主批准這個有未解標記的音檔，亦未啟動 S08 付費插圖。
