# S42 劇本與語音關卡接續（2026-10-20）

現行 `video.json` SHA-256 `fa187588a94836e994205a500e1a673fa83473b404c54672071316fb27ccbf4e`；`script.md` SHA-256 `3a0f9748ae41cfebf9853a9fcf3413dd6937b464bdb6b8210e1b335d72db0677`；`claims.md` SHA-256 `b25ef409a2c2bfd9e3662d43eb7001e52337464c888759bd32cfafd1b8d745a9`。`verify-1.md` 接上既有獨立固定來源、全幕與 R11 差分查核；新稿只改片尾 `md999c` 的無史實口播，其餘 85 句、83 幕正文畫面與來源未動。`script --slug` 更新的另兩行是生成性校驗字串。

站台在 `2026-10-20T09:43:20Z` 對 `brief.md` SHA-256 `29beb1e0307a117470445b2aa23a120073e27f101ec6fa2a32dfdb9f58ba4bb7` 正式選 **A 案**，本機 `review-pull` 於 10:36:26Z 記錄。新稿獨立無歷史盲讀在上述 `script.md` SHA 下對 13 題各附原句，官方 `narrative --answers` **13/13 PASS**；正式 verdict SHA-256 `9db85356aa3b528f9158a63424394220d6ba39fc310a9a0529a07e4bd57e40f4`、回答 SHA-256 `2d79838eb4e90c9e271852295338727bde1c83fb1e24ae0d81481fdb05087bdb`。`lint` 0 errors、1 個片尾未**口播**訂閱的提醒；動畫片尾的訂閱位置仍在。

政策預檢對原稿最後的口播「訂閱奇聞檔案局」評業配 `0.46`，只移除這句的診斷為 `0.02`；現行中性收束句完整旁白再評 `0.02`，符合門檻（立場 `0.79`、建議 `0.01`）。這是合成前的現行旁白評估，正式成片仍須重跑 `qa`。`review-push --gate script` 將精確稿送站台，`review-pull` 回覆 **pending**；依站主「用推薦的決定，不用問我」的持續製作委託，CLI 在 10:43:57Z 記錄了**本機代理**精確劇本核准，與站台站主審核分開。

語音首輪 `tts --dry-run` 為 86 requests、約 2270 Gemini 計費字元，頻道聲音可用。實際 `tts` 合成 **86/86** 句、2270 計費字元，0 舊 take 重用。首輪逐句辨識 86/86，49 句逐字一致、21 句僅同音字或語助詞不同、2 句經 Jev 判可接受、14 句 flagged。針對 14 句執行 `--redo`，其中 **13 句已保存新 WAV 和快取**，預估再計 330 字元；最後 `md083` 的 33 字元 Gemini 請求回 HTTP 502，無可用回應，是否實際計費不明。語音 journal 將精確請求 SHA-256 `ac8ad4385d8f2a5fde8e24640f53eb41d75dd83e11417b8ae09f2417d6de5e52` 保持 `held`。**不得忘記 journal 或重送這個相同請求，須先查明供應商使用量。**首輪 `md083` WAV 仍在且快取有效。

為了核對已確認完成的重錄，無 `--redo` 的 `tts --dry-run` 回報 **86 requests、0 to synthesize**；接著普通 `tts` 完全重用 86 句、0 新計費字元，從 13 句新 take 加上舊 `md083` 安全重建 `narration.wav` 和 `timeline.json`。現行 `timeline.json` SHA-256 `01dfbbee707ba72dc406d565a8c02b0089530604f98667e37913b02257866a30`、`narration.wav` SHA-256 `55a94207ce5d073019c3838920936e78ef231e7c926f0989b9458ee267bbb37a`；86 行都綁定當前 WAV 的 SHA，`status` 顯示 narration synthesized。時間軸共 17,219 格／30 fps，約 **9:33.97**；片尾從第 16,701 格開始，正文 **9:16.70**；濃縮開場至第二章第 1,278 格，約 **42.60 秒**，之後正文 **8:34.10**，不靠片頭片尾湊足八分鐘。

重錄後 `check-audio` 只重辨 13 句，86/86 已查：55 句逐字一致、21 句同音字或語助詞、2 句 Jev 通過，仍有 **8 句 flagged**（`md043`、`md053`、`md065`、`md068`、`md069`、`md070`、`md072`、`md083`）。部分是實際漏字或改詞，例如 `md053` 把「日期」讀成「日記」，`md072` 將「帝多雷」讀成「維多利」。精確查核檔 `/workspace/.video-work/curio-s42/review/check.json` SHA-256 `8cb2486a81686f617b012ffd28d0c3ec708373410398f057d128ff700cc798a8`，flags SHA-256 `d98265bbcbcbf7ec9fab8e5ec8e4960ffb37fcd99d746d4ecc8174d53d171540`。**語音關卡未通過；沒有送出 audio review 或宣稱站台核准。** S42 插圖、配樂和影片製作繼續暫停，也沒有 YouTube ID。
