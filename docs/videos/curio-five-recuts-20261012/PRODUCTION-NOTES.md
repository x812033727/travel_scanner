# 旁白製作收據

2026-10-12 從現用檔與完整修訂歷史唯讀核對，外部收據為
`C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/speech-production-summary.json`，
SHA256 `d8160b00107b8544ec00ed5b32943a98032d4de0290686715819846b036188be`。
本次稽核沒有呼叫語音服務，也沒有修改音訊或歷史。

| 合成階段 | 已保存回應 | 收據回報計費字元 |
| --- | ---: | ---: |
| 初次五片四語片頭 | 144 | 6,017 |
| 同稿限定重錄 | 5 | 193 |
| H03 日文兩句發音修訂 | 2 | 69 |
| L08 繁中一句措辭修訂 | 1 | 25 |
| 合計 | 152 | 6,304 |

以 slug、語系、句 ID、請求 SHA、音訊 SHA 及 `saved_at` 去除歷史複本，
保留每筆收據來源與可驗證 WAV：共 152 個不同音訊 SHA、147 個不同請求 SHA。
所有合成回應都有計費字元；此數字不包含轉錄／評判費用，不換算金額，
也不推測服務帳戶餘額。較早估算不能取代上述實際回應。

現用共 20 軌、144 句，待合成請求為零；全部沿用原來源的 Gemini Sulafat
及各來源 voice 設定與雜湊。136 句通過原轉錄檢查，另外 8 句在 6 軌中由
精確 WAV 綁定的第二意見解除：H02 繁中 intro01、英文 intro06；H03 英文
intro04；U02 日文 intro02／05／06；L08 日文 intro05、韓文 intro07。
原始旗標保持留存。14 軌原檢查直接通過，全部 20 軌通過片頭自動音訊關卡。

已核對四語共用時間軸、原速播放、48 kHz 樣本長度與格數、字幕／旁白／收據
雜湊及無過長語言留白：H01 45.267 秒、H02 41.567 秒、H03 43.367 秒、
U02 47.833 秒、L08 44.700 秒。五片 intro 與 intro-revisions 的語音 journal
沒有留存中的 sent／held／waiting 項目；這是本批本機證據範圍的結論。

H01 沿用正文的日文配音保留原有資格：`117/118 native clear + 1 exact
owner-accepted mtua audio flag`。不得把它改稱完整原生語言 PASS；新片頭
通過也不代表重審全部既有正文。此收據不宣稱站主已聽驗、成片完整核准、
已上傳或已發布。

重跑同一唯讀稽核（會更新收據時間與 SHA）：

```powershell
node docs/videos/curio-five-recuts-20261012/speech-production-summary.mjs
```

H03 使用 `h03-pronunciation-specs.json`、L08 使用 `l08-wording-specs.json`。
U02 的 `u02-visual-specs.json` 只把比較卡取樣指定為完整顯示的第 316 格，
旁白內容與語音收據未變；H01、H02 使用原始 `intro-specs.json`。
所有舊稿、舊 WAV、重錄與修訂歷史皆保留。
