# S31 文稿與來源核對（一）

2026-10-19。最終盲讀文稿 `script.md` SHA-256：`72eb00f5f0f05268dc9125705c3e75eaea98b8b933e2471fb42cf6e28762826c`；`video.json` 旁白標識 `98ab3b7c8cd5ce07`。這份核對只涵蓋文稿、古籍轉錄與分鏡提示詞；音訊、插圖成品、配樂與成片尚未製作。

## 來源核對

- 固定全文共同來自 GitHub `garychowcmu/daizhigev20` commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620`。杜牧《樊川文集》、白居易《白氏長慶集》、《新唐書》、《舊唐書》四個下載全文的 SHA-256 和各引句見 [research.md](research.md)。研究筆記內 7 個固定連結的路徑均在該 commit 的 tree 中，四個全文 hash 與下載檔一致。
- 杜牧第一首的「一騎紅塵妃子笑」是詩中的一個瞬間；後兩首的探使與歌舞提供它的諷刺脈絡，沒有驛站或果園名。S31 用它開場，不把「一騎」數成全程馬匹。
- 《新唐書·楊貴妃傳》原句「妃嗜荔支，必欲生致之，乃置騎傳送，走數千里，味未變已至京師」。S31 稱為後出史書的記載；不把「數千里」當精確測量，不推定站數、天數、速度、保鮮器具或華清宮簽收。
- 《新唐書·禮樂志》另說生日新曲適逢「南方進荔枝」；地理志廣州「土貢……荔支」、戎州「土貢……荔枝煎」均未將某批果與楊貴妃騎傳連到同一張貨單。畫面不用特定南方果園或畫好的驛路。
- 白居易《荔枝圖序》談巴峽果，「一日而色變，二日而香變，三日而味變」。後出的《舊唐書·白居易傳》轉引這句，不構成第二個獨立的運貨測量。S31 沒用三日倒算馬速，沒把巴峽說成那批果的已證產地。
- [claims.md](claims.md) 逐句列 `ly001`–`ly097` 來源；多個代號代表比較或推論，並非多個互不依賴的目擊者。片尾訂閱句標明 `EDITORIAL`。

## 結構與工具檢查

| 項目 | 結果 |
| --- | --- |
| 靜圖分鏡 | 正文 96/96 `shot`，加一景片尾；正文插圖占比 100%，`cute-mystery`，固定系列配樂設定，無具體路線示意。 |
| 長度 | `lint` 預估全片 9.4 分鐘；開場 46 秒；正文約 8 分 35 秒，超過 8 分鐘下限。 |
| 鉤子 | `video.json` 18 條 setup→payoff；`lint` 無 45 秒以上未掛問題的警告。 |
| 系列 lint | `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`：0 errors、0 warnings。 |
| 稿本 | `node tools/video/cli.mjs script --slug curio-s31` 重生 `script.md`；SHA-256 如頁首。 |
| 文檔測試 | `npm run test:docs-videos`：236 tests passed、0 failed。 |
| 任務票 | `npm run check:tasks`：exit 0；其他既存票有 stale／scope warnings，無 S31 結構錯誤。 |
| 獨立盲讀 | 第五位新讀者先只看 `script.md` 和 narrative 題目，核對本頁首 SHA，逐題給證據；`narrative --answers` 結果 13/13 全過，無失敗或提醒。逐題原始輸出見 [narrative-review.json](narrative-review.json)。先前獨立讀者指出的開場像目錄、重述數字與來源、終章重複回顧，已重寫並以新 SHA 重測。 |
| 音訊及付費媒體 | 未執行 TTS、音檢、MiniMax 生圖、配樂、合成；本集媒體費用 US$0。音訊完成並核對後，才安排後續付費媒體階段。 |
