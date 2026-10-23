# H11 繁中旁白 QA：第一次合成

日期：2026-10-16（Asia/Taipei）。本收據只對應 `video.json` SHA-256 `FC9B6B1FF2F94AB75EA1AA2D4E6753AD1D001B0DE82CE693A1D3FD89F8E801A4` 與站主核准的 `script.md` SHA-256 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108`。劇本文字未改。

Gemini Sulafat 產生 73 個請求／75 句 WAV、2,346 計費字元；時間軸 16,446 影格、30 fps，即 09:08.2。音訊 journal 無 hold。`check-audio` 完成 75/75 句轉寫、1 次 TypeSafe Jev 判讀：48 句逐字相符、13 句同音字或語助詞、4 句 Jev 接受、10 句旗標。檢查原件在 `<home>/mokaair-work/videos/curio-h11/review/check.json`（SHA-256 `63191ECAB630A61BFB69F3E0DD7A47AECEAA0A4A6F5952CE055B738B1654A934`）；旗標檔 SHA-256 `D117BF513E2CE6B309359DEC26A006B76037A7EF91349BC7BF2C4F0CD0A94FA6`。

用本機 faster-whisper small、CPU int8、beam size 5、無劇本文字提示，重新轉寫該 10 句。原始結果 `<home>/mokaair-work/videos/curio-h11/review/whisper-small-flags-20261016.txt`，SHA-256 `40CA879021478B7376093E953B1F6A9129B6B251FDF3A2135F9060058E15639F`。這是第二套自動辨識，不等於人工試聽。

| 句 ID | 核准稿關鍵字 | Gemini 聽成 | 離線 Whisper 聽成 | 判定 |
| --- | --- | --- | --- | --- |
| `v2405e28` | 葉數／頁數 | 頁碼／頁數 | 葉樹／葉樹（同音） | 兩套不支持「頁碼」錯讀，屬 Gemini 辨識漂移。 |
| `v0e564e3` | 從四頁取下四份樣本 | 從絲頁取下四份 | 從事業取下四份 | 兩套都把短語猜成不同字；保留原音，請站主試聽「四頁」。 |
| `v16d9e2d` | 轉寫好的版本、字形 | 撰寫好的版本 | 轉寫好的版本、字型（同音） | 離線轉寫支持核准稿，不重錄。 |
| `va919cc7` | 一部分、又換成 | 一部份、欸又換成 | 一部分、又換成 | 離線轉寫支持核准稿；Gemini 的字形與語助詞不支持重錄。 |
| `v470a2c5` | 開場那則新聞 | 該則新聞 | 開場內則新聞 | 離線保留「開場…則」聲音輪廓，不支持 Gemini 的換詞；不重錄。 |
| `v1df5834` | 影像反轉、同一葉 | 影像翻轉、同一頁 | 影像反轉、同頁 | 關鍵動詞與核准稿一致；「同一葉」是否完整仍請站主試聽。 |
| `v439465f` | 她、馬爾奇字、頁邊、筆畫 | 他、某二字、阿扁、筆劃 | 他、馬爾奇字、頁邊、筆劃 | 專名與頁邊被離線轉寫辨出；他／她同音，筆畫／筆劃同義，不重錄。 |
| `v2ebbd0d` | 格雷什科、奈貝、方向試 | 格雷舍科、奈貝、方向試 | 格雷社科、奈貝、方向式 | 兩套都把專名中間音節記成近似「舍／社」；請站主試聽讀音，未確認前不改稿。 |
| `vd56bdd7` | 模型有已知輸入、仍待找到讀法 | 模型由已知輸入、仍得找到讀法 | 模型有已知輸入、仍在找到讀法 | 前半與核准稿一致；「仍待」被兩套記成不同字，請站主試聽。 |
| `v75e1ebb` | 如果先查一樣 | 如果懸差一樣 | 如果先查一樣 | 離線轉寫支持核准稿，不重錄。 |

結論：**0 句有足夠證據立刻重錄；4 句交站主優先試聽**（`v0e564e3`、`v1df5834`、`v2ebbd0d`、`vd56bdd7`）。其餘 6 句的自動旗標沒有形成可確認的錯字。試聽頁：`<home>/mokaair-work/videos/curio-h11/review/audio.html`。站主已回覆試聽並在後台核准；`review-pull --gate audio` 現場讀回 `audio: approval recorded`，`status` 同時顯示 `narration approved`。未對旗標自行核准，也未重錄。

`timeline.json` SHA-256 `FF66A71BAC562CAE9A3013BFC7F72DD50A5F06107D4843F6A8421BD062AEFCA4`。已執行 `review-push --gate audio`，後台先讀回等待站主；站主試聽並核准後，重新 `review-pull` 讀回 `audio: approval recorded`。後台仍列完整 10 句自動旗標；上表的 4 句是當時的人工試聽優先項，最終決定來自站主。

費用停手帳本：`<home>/mokaair-work/videos/curio-next-five-20261016/review/spend-ledger.json`，本集 TTS US$0.20、轉寫與 Jev QA US$0.50，合計 US$0.70，都是保守估算；工具沒有提供最終美元帳單。
