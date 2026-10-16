# H06 v2｜片尾答案前的 DNA 母系線索窄修

日期：2026-10-14。本補記接續[兩句 DNA 回扣修稿](dna-payoff-two-lines-20261014.md)。該稿的獨立 11 題盲審為 **10 YES／1 NO**，唯一未過 `no_recap`：`[v226]` 已說比對能排除公主身分，片尾 `[d7um] 她不是安娜塔西亞。` 再說同一排除結論。正式 `review/narrative.json` round 16 FAIL 紀錄與盲審原答已先複製到本輪快照，不修改原件或把該輪結果當作新版通過。

站主指定**只換 `v226` 一句文字**：由「回到開場那兩份檢體：比對能排除公主身分，卻不能獨自鎖定另一個本名。」改為「**回到開場那兩份檢體：它們提供母系線索，卻不能獨自鎖定另一個本名。**」`fa8j` 仍明說兩份檢體與皇后已知母系參照未對上；`d7um` 保留片尾才說出人物答案。`v226.pause_after_ms=0` 仍沿用前稿，場景交界原有 700 ms 停頓不變。其餘 100 句、82 景、來源標註、模板、chapter 及畫面資料均不變。這只把正文的結論退回**母系線索及個人識別界線**；c09、c19–c20 的史料及推論限制見 [claims.md](claims.md)。`fa8j` 的明確皇后參照仍可能讓觀眾推知結果，因此需要新版獨立盲審判定實際敘事節奏。

| 綁定 | 本次值 |
| --- | --- |
| 正式 `video.json` SHA-256 | `c0e4c948b9f1fd3cb628992ab325700eae9dff716ff65c7163ab5de194e9e21b` |
| 正式 `script.md` SHA-256 | `8f3346092033557cec8b806eaba9459b38dabc152a1743077bec73f4e32ba794` |
| narrative／speech／visual hash | `12dccbe87d74918d`／`a13d326e1afeca70`／`373e3953f50e6b1c` |
| 純盲審 `blind-payload.json` SHA-256 | `fe453ab0a743850a145b531b45f55dbc3a527e45ad43251df2c41deaf71471c8`；只有 narration 與 11 問，沒有答案 |
| 未核准 `timeline-projected-unapproved.json` SHA-256 | `3a3edcae7e3c4a8171282b29daa0db17d3c07b2b9d9e2986dea7f557f5d4ca9e` |

這次**沒有新 TTS**。投影用其他 99 句現有 WAV 的精確樣本數，加上 `fa8j`／`v226` 新文按預設語速估出的 264,960／334,080 樣本，因此 14,670 格／30 fps＝**489 秒（8:09.00）**仍非正式時間軸。planned `shot` **7,464／14,670 格＝50.8793%**，比 50% 整格門檻多 129 格；98 畫面狀態、最長 8.0 秒、平均 5.0 秒，`cadenceProblems=[]`、敘事機械檢查 0 errors／0 warnings。`v226` 第二個原生卡狀態估計 **7.7 秒**；在 `pause_after_ms=0` 加 700 ms scene gap 下，若嚴格不超過 240 格／8 秒，實際 `v226` WAV 至多 **350,400 樣本（7.30 秒）**。真正 TTS 的語速可能不同；合成後必須依新 WAV 重算此狀態、全片時窗與 shot 占比，八秒與 50% 成片門檻均以實測為準。正文估時超過八分鐘不等於正式音訊驗收。

外部隔離目錄：`<home>/mokaair-work/videos/curio-h06-v2/review/dna-payoff-last-line-20261014T054614Z/`。`before/`、`before-receipt.json` 在動稿前保存正式稿、上一版 payload／投影／收據、當時 canonical timeline／approval／manifest／ledger 雜湊、round 16 FAIL 原答與正式紀錄。前收據 SHA-256 `2bef3381cce69509c9b115a3e4c607ceece531d7e20e81dd0948b1600c9b7ef2`；原答 SHA-256 `e9240f54db87afc1e00093c9836ab3bf1a96b67da768bafc673382ec49fea511`，正式 FAIL 紀錄 SHA-256 `a58750a2e82bbe7e505a20fb5a8e78218a5fa7cd0598b6790fe678f95613039b`。同目錄的 `postflight-receipt.json` 記錄後狀態與免費檢查。新版純 payload 只供 fresh blind；兩句各一次 TTS、正式時間軸重綁、音訊核准與圖片／成片關卡，須按後續結果執行。本輪未呼叫 TTS、judge、付費圖片或後台，未 commit／push。
