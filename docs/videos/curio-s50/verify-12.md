# S50 R7｜119 句真實配音與完整零旗標音檢

2026-10-20 UTC。精確 R7 劇本 SHA `5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b` 的[獨立史料／書面畫面](review/r7-source-independent.md)、[兩位新讀者合併](review/r7-official-panel.md)、[全稿解說政策](review/r7-policy.md)均 PASS。網站劇本卡已 `hand_pushed pending`；本機 `approvals.json` 另記使用者常設推薦偏好下的同版委派選擇，非網站核准。

`tts --slug curio-s50 --dry-run` 顯示 119 件中僅 **8 件**須重新合成、約 **190 billable characters**，Gemini Sulafat 可用且免費額度足夠。實際合成 `fire015/019/020/032/039/062/078/099` 八件，另 **111 件**沿用已封存 R5 音檔；沒有重送原稿或非改句。完整官方 `check-audio` 查 **119/119**，93 句逐字相符、19 句只有同音或語助詞差異、7 句 Jev 判可接受、**0 flagged**，不需再重錄。原樣 `check-r7-first.json` SHA `49b12743862236f8b314fa332eaa53e48053e0b5d3736e5c3cd18e161584dd83`、空旗標表 SHA `8251b01658db9fe4fee3c6ca414af5f8b832d57e5e5bf8c13e8c7a72e6218dd6` 留在私有 `/workspace/.video-work/curio-s50/review/`。

現用 WAV SHA `ddb70999e36d21632714ac09f374e27148d039e10f2f2d63aff5e183c70dc33f`，時間線 SHA `1955529a671a5743be06056f1b993980c9e272ef6d90bf73bb2a8049e72b600b`；30 fps 實測濃縮開場 **47.03 秒**，其後正文至片尾 `fire999a` 前 **10:55.37**，旁白總長 **11:56.00**。R5 音檢原有 30→11→7 旗標並未被宣稱成過關；**R7 音訊零旗標 PASS** 綁定上述精確版本與私有音檔。

下一關：站台精確音訊卡與整集插圖／配樂上限，先定點試畫並逐張原生圖驗收；本站卡的待審狀態不可當作站主批准。插圖、片頭片尾合成、分鏡、成片與上傳尚未完成。
