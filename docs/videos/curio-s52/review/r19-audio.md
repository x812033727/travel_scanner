# S52 R19｜Gemini Sulafat 旁白及全篇音檢

2026-10-20 UTC。R19 的五檔雜湊見 [政策回條](r19-policy.json)；`script.md` SHA-256 `5c51bcff8ed8540059f6a0c456562e04223fd591cbedec0349b72ad5a29fe067` 在 TTS 與兩次音檢後保持相同。獨立來源／書面畫面 PASS、無歷史脈絡雙盲 OR 13／13 PASS、Jev 當前解說政策 PASS。沒有拿 R16 的舊語音檢查當 R19 結果。

`tts --dry-run` 預報 113 個語音請求，其中 **13 個新請求／330 計費字元**，其餘 **100 個同文同聲快取**；全片 2,584 個語音計費字元，網站 Gemini Sulafat 當時月餘量 8,536,732 字元。正式 TTS 完成上述 13 個新請求，沒有 429。初輪 `check-audio` 正式全檢 **115／115**：88 句逐字、22 句同音字或填充詞、3 句 Jev 判可接受、2 句旗標。初輪原樣[旗標](r19-audio-flags-round0.json) SHA-256 `abcdad172fba65fb66a2ba0c6a9c70814c519c5ddac60bd8b9c8da8a650b4ee5`；`check.json` SHA-256 `c28a99e4523e192b93bf2294ab7d0045abb80687b831c13fbeebb2f032f7d9de`。

| ID | 初輪 ASR／官方判定 | 處置 |
| --- | --- | --- |
| `s52005` | 「這一刻」→「傑克」；Jev 0.03 | 只重配本句 |
| `s52090` | 「第一格」→「第一個」；Jev 0.11 | 只重配本句 |

以初輪原樣旗標作 `tts --redo`，只新合成這 **2 個 ID／33 計費字元**，其餘 111 個語音請求重用，未改劇本或發音辭典。第一次定點重配後再跑**全篇**官方 `check-audio`，退出碼 0：**115／115**、90 句逐字、22 句同音字或填充詞、3 句 Jev 判可接受、**0 旗標**。末輪原樣[旗標](r19-audio-flags-round1.json) SHA-256 `34e6429b568cfd596fd6c5c977ae8a44b99e05d2d4021b8da02640f5beaa8984`；`check.json` SHA-256 `fcec3867f5baead98156e67e9ead5d6f7ed1901be00439a9f4cf8211ee75375e`。兩輪完整原始 `check.json` 與 `check-flags.json` 另保留於私有工作目錄 `review/r19-audio-round0/`、`review/r19-audio-round1/`。`check.json` 保有四個前版已刪 ID 的轉寫快取；以上統計只計當前 `video.json` 唯一 **115** 個 ID。

最終旁白 WAV SHA-256 `c3adbbbb97de3287ac54151edc3c76ef4422c8f7176789a379e02931c4dc4bfc`；時間軸 SHA-256 `378ba91e98893c8f6445594f169c4657f4cc70122c777c695f7b7ec426e10add`，語音版本 `speech_hash=2af0a08f6e592b5d`。30 fps 共 20,609 幀、WAV 686.966667 秒：第一章開場 **1,324 幀＝44.13 秒**，第二章起至片尾前正文 **18,751 幀＝10:25.03**，片尾場景 **534 幀＝17.80 秒**，全段 **11:26.97**。正文達到至少八分鐘的實測門檻。

**機器音檢 PASS；人耳聽審與網站音訊卡未取得核准。** Jev 的三句可接受是文字轉寫與判斷，不是人工聲學聽辨；未聲稱有人聽過成品。圖片評審、配樂仍受本月額度限制，尚無生成圖、動畫開頭／片尾或完成影片。
