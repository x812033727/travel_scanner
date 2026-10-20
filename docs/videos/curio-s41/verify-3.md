# S41｜R12 劇本、政策與實測語音關卡

2026-10-20。精確現稿：`video.json` SHA-256 `5dcfa734204a998fb252d5aadad7b13fa36a24ffe5e26b845127b5c700e589a9`、`script.md` `cede86bee6c52e0827079ac80606e5ad6b3ecc2198ab6b6bac43eacab18e1c30`、`claims.md` `f3eaa619db47210656825b222fc025040ca5ae6bbd1ac571be16ceb307e8f808`。R12 只改 R11 片尾一句；[作者差分](reviews/source-visual-r12-delta.md)及[獨立史料／書面畫面覆核](reviews/source-visual-r12-independent.md)均 PASS，不是實際影像或音訊驗收。

**敘事與政策。**兩位真正全新的 R12 讀者在同一組 hash 上分別判 13/13 與 12/13，B 唯一 No 是 `no_recap`；依 `mergePanelVerdicts` 的雙讀者規則，沒有共同必答 No，正式 [narrative-r12.json](reviews/narrative-r12.json) PASS，工作樹 `review/narrative.json` 同版。一次精確 `policyRequest`／Jev 判斷 PASS：stance 0.78、advice 0.01、sponsored 0.01、demo 不適用；請求 SHA-256 `fc84129240552754748f056ef2c9f71b865e5c3aa0f65af7aee045afe0114929`，詳 [policy-r12.json](reviews/policy-r12.json)。`lint` 0 errors，1 個既有片尾「未口播訂閱」警告；視覺片尾卡有「訂閱奇聞檔案局」。

**站台真實狀態。**R12 以手動影片 `review-push --gate script` 送站台，回覆 `pending`；緊接 `review-pull` 回「script: waiting for the owner」。因此這不是站主在站台核准。依使用者「採推薦方案、不要逐項問、繼續完成影片」的常設委任，本機另核准 `script.md` 精確 hash 供補錄，`approvals.json` 注記與站台 pending 分開；若稿子再改，該本機核准也失效。大綱 A 仍有較早真正的站台核准，見 [R7 收據](verify-2.md)。

**語音與時長。**沿用 77 條 R7 可驗 WAV，另合成 19 條 R12 句子，Gemini `Sulafat` 記 489 billable characters。一次定點 `qb006` 同稿重錄另記 31 characters；本輪合計 **520 billable characters／20 新請求**，未出任何付費插圖。重錄後時間軸 SHA-256 `4fdacf521cf7e9c6b828bea33329d977798207d6fc3660fd57caf471f3daeffe`，語音 `speech_hash` `4f2eed0775738845`；全音檔 SHA-256 `9c3bf955b7726967ff7cea1c8178940c9a9991ddf3389522d409b47b9b3a73de`。實測開場 `qb001→qb009` **59.07 秒**；開場後至片尾前 `qb009→qb999` 正文 **542.70 秒（9:02.70）**；全片片尾前 601.77 秒、總旁白 624.13 秒（10:24.13），七章時長檢查無問題。`brief.md` 尚述 108 句與更早稿的估時，**不能作 R12 證據**；現版為 96 句、94 景、88 張插圖鏡頭、5 張史料卡與 1 張片尾卡。

**音訊關卡未過。**首輪 `check-audio` 96/96 有 16 flags；只重錄新稿中轉寫具實質歧義的 `qb006` 一次，再查仍是 16 flags，該句 Jev 0.03→0.04。完整 [音檢與停損報告](reviews/audio-r12-gate.md)保留兩輪逐句轉寫、旗標、舊新 WAV hash、同音與風險分流。本環境無可靠原音接收或獨立本機 ASR，不能把轉寫文字視為已聽見的字，也不能宣稱聆聽 PASS。現階段不送 `review-push --gate audio`、不本機核准音訊、**不開付費插圖**；待真正獨立聆聽／轉寫或有來源安全的新稿、重新走必要關卡。
