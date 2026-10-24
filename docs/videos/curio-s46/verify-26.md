# S46 R14｜實配音全句零旗標與精確音訊決定

2026-10-20 UTC。先核對 R14 [獨立來源／書面畫面](review/r14-source-independent.md)、[兩名新讀者合併](review/r14-official-panel.md)與[全稿 Jev 政策](review/r14-policy.md)均 PASS，精確 `script.md` SHA-256 `d5d01d3c96327060df9e7531aba796af45bedeaa25b8124c5993de528f7a8e40`。本站劇本卡同 SHA 為 `hand_pushed pending`；本機腳本核准明載使用者推薦偏好下的委派選擇，不冒稱網站核准。

`tts --slug curio-s46 --dry-run` 顯示 118 件中 6 件待合成、約 178 billable characters，Sulafat 可用且免費額度充足。實際合成 6 件、其餘 112 件重用；第一次 R14 `check-audio` 查完 **118/118**，只有 `bkw016` 的布萊克威爾讀音被標 0.39。首輪 `check.json`、flags、該句 WAV 及整段 WAV／時間線均封存在私有 `/workspace/.video-work/curio-s46/review/`，其中 `check-r14-first.json` SHA `0420e9807517dd74f068ae758d79297f9a6da02855cc4219e344ec25acf47cc8`。

只按首輪 flags 重錄 `bkw016` 一句（40 字元），其餘 117 件重用。第二次正式 `check-audio` **118/118，零旗標**：41 句字面相同、75 句同音／語助詞差異、2 句 Jev 判可接受。`bkw016` 新轉寫為「布萊克韋爾」，Jev 0.90；`bkw044` 的「她／他」為同音轉寫，工具分類 `sound`。最終 `check-r14-final.json` SHA `ca4769b57ecf16bc9ea73834fdb71fd57cdf75b4962779063029a558ab1b164b`，完整最終 WAV SHA `f705fd6052dca8bdd00e441d4a9cf1730e7efc9a90b5f7609b10a7685e027c5a`，時間線 SHA `60331fbdcd8f30b37facafe65c9ded9b619eaf43ada9e576f01653d2adf7f67c`。30 fps 實測濃縮開場 **43.93 秒**、其後正文到片尾前 **10:42.17**、全部旁白 **11:45.77**。

`review-push --gate audio` 已送精確時間線，站台讀回 `content_sha256=60331fbd…`、`hand_pushed pending`、`decided_at=null`。本機 `approve --gate audio` 只記使用者常設推薦偏好下的**委派精確音訊選擇**，不是網站或站主親耳核准。舊 R11 `bkw044` 轉寫 HTTP 504 的 uncertain-use journal 仍 HOLD 且未重送；R14 用的是已成功轉寫的另一段音訊。下一關只可在事先記整集媒體預算與三景原尺寸試畫門檻後進圖，並須依生成圖逐張作原生畫面驗收；尚無插畫、配樂、分鏡核准或成片。
