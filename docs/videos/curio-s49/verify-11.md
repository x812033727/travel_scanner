# S49 R8｜完整旁白音檢、兩輪定點補錄與停手

2026-10-20 UTC。R8 固定稿的[獨立史料／書面畫面](review/r8-source-independent.md)、[正式雙盲](review/r8-official-panel.md)及[政策](review/r8-policy.md)均 PASS；本站大綱與劇本卡仍為 **pending**。本輪只處理已生成的繁中旁白：保存首次完整音檢，依其 flags 做**兩輪**定點 `tts --redo`，每輪後均執行不抽樣的 `check-audio --slug curio-s49`。未修改劇本、主張、分鏡、字典或插畫，也沒有送出音訊核准。

| R8 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `a010434fbbb2e498f6d064557b58e11cea338ccf93fc6300ab5960444f9e25e1` |
| `script.md` | `f40259db7e16da37652689f0e2d703b8e03b8364d1738d0b4c2f848043618c8b` |
| `video.json` | `1eaec3a24e656fe86e0cc5f48e5d61fa3a690b18aa7f4621960aa85f14f60baa` |

私有原件與每輪快照在 `/workspace/.video-work/curio-s49/review/r8-audio-archive/round{0,1,2}/`。每輪 `manifest.json` 記 WAV、時間軸、完整 check、flags 及當輪被標／補錄單句 WAV 的逐檔 SHA-256 與大小，複製後均逐檔比對原件。首次 `review/narration-r8-first.wav`、`review/timeline-r8-first.json` 與 round0 完全同 SHA。原始音檔及 136 句逐字轉錄只留私有工作目錄。

| 音訊輪次 | 重新合成／用字量 | 完整音檢（exact／同音或語助／Jev 放行／旗標） | 旁白實長（開場／正文／片尾／全部） | WAV／timeline／check／flags SHA-256 |
| --- | --- | --- | --- | --- |
| 首次 R8 | 136 句、3,288 billable characters | 136/136；84／26／5／**21** | 47.200／748.700／15.567／811.467 秒 | `f684eaad53b0633b266a75efc0bd6414c1027abad93c7e9c5004746d136daafc`／`7e1d11cac03775d5e23de88b1999118d9d9d2a1ba5d83e7a29b920f7cda3d3a1`／`8cdde38af4c449a637980b05fca2c57592029a29e90e80764bb78746f19f55f3`／`66a67f48c7adf13fc846f7c56ee77ac99891b8bc0771c9c692891d1bddd1a0df` |
| 定點補錄 1 | 21 句、509 billable characters；115 句重用 | 136/136；92／30／6／**8** | 47.200／752.133／15.567／814.900 秒 | `d4eb21a047b6af5144a4e7e79a9577061559971f6b206f87a29aaeaf515120e5`／`527f8b9f5cc906034762e2a98dfa138c02185e9d7a9cc35feeed4c00b753977d`／`4e53050492bae6f4e04834185d25e71c8e7b79d80622b8269b72f45265f9b34d`／`487e25754dbf04e48804a267cc6a967e97d7a4912ded87e2246127f9e0b14913` |
| 定點補錄 2 | 8 句、191 billable characters；128 句重用 | 136/136；94／30／6／**6** | 47.200／753.367／15.567／816.133 秒 | `fadfb143202762ee3fe4ae30c33caa19bde15a369f97b742980ca7e68f996ea0`／`df4f414ea98f5a6dbaa553d2e80842a843c41ebe2bf080b5af79ae9439616739`／`529ea2266e7ab8e75151ebd2c75e2e50f8e004a347e82c4b258aaa0090abd119`／`6cef34a935370d4ca645e542a5e7e59e33db5f8116effc236ee23782b8b8614a` |

逐輪 manifest SHA-256：round0 `2d86912186dfa23ba12b82b9279c9a0c1349f516ce7cb930f8ece33a67c48c77`；round1 `9aeba3f6637fa397f3e0164165fc7a8ece3393be48025c8da3eb3ddafe2fd488`；round2 `146aca7372499fd20031e7379466ba0edc356d850f0b1e367810d26d00efae61`。兩次時間軸各恰有 21、8 個單句音檔 SHA 改變，與各自 redo 的 ID 完全相同；其他 115、128 句的音檔 SHA 未變。三次音檢新轉錄數為 136／21／8，Jev 各呼叫一次，未檢句數皆 0。兩次補錄及音檢的原始 CLI log 亦在相應私有快照。

固定稿共 **2,928 spoken units**（開場 176、正文 2,693、片尾 59）；CLI 的完整一次語音報價是 3,288 billable characters。TTS 累計 **3,988 billable characters**（首次 3,288＋509＋191），165 次單句合成請求。按各輪實際單句 WAV 合計，合成語音為 673.99＋105.68＋41.40＝**821.07 秒**；倉庫目前記載的 Gemini 3.8 Flash TTS 公開價為音訊輸出每百萬 token US$9、每秒約 25 token，因此**僅輸出音訊約 US$0.185**。站台未向本機回傳各請求實際輸入／輸出 token 或美元帳單；輸入 token、轉錄與 Jev 不在這個美元估算內，不能將它當實收總額。

第二輪後仍有六句旗標：`moon011`（遠行／遠航）、`moon012`（「報紙借走」被轉作「伴著節奏」）、`moon015`（真名／聲明）、`moon026`（增刊與助手連在一起）、`moon030`（鏡筒／鏡頭）、`moon100`（早晨聚住／造成聚焦）。這是轉錄與 Jev 的疑慮，不等於已證實每句都唸錯；其中 `moon012/015/026/100` 的轉錄差異尤其可能改變意思。六句精確原文、聽寫、分數及單句 WAV 都在 round2 私有快照。

**音訊關 HOLD。** 兩輪 redo 上限已用盡，不再重錄相同稿。下一關先由作者對六句做獨立實聽／第二轉錄，針對證實含混的詞窄修旁白和相應 `claims.md`、重生劇本；有新稿須以新 SHA 重核受影響史料／畫面、正式敘事與其後政策、網站卡，再重做受影響音訊及 136/136 完整音檢。未達零旗標及必要核准前，不進入付費插畫、配樂或成片。
