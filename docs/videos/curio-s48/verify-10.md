# S48 R8｜兩輪限縮重錄後仍有三句音檢旗標

2026-10-20 UTC。精確 R8 `script.md` SHA `52d9f1e7b3fce7805f928e72754481e79836cf35fde5aa9098929f88086e29b1` 經[獨立來源／書面畫面](review/r8-source-independent.md)、[兩名新讀者合併](review/r8-official-panel.md)、[全稿政策](review/r8-policy.md) PASS；本站精確劇本卡仍 `hand_pushed pending`，本機另記使用者推薦偏好下的委派同版選擇。

R8 `tts` 在 102 件中重用 89 件、合成 13 件／414 billable characters。首輪完整官方 `check-audio` **102/102**，標 `atl038,atl040,atl058,atl095` 四句；原樣 `check-r8-first.json` SHA `a1fc76514553f70099ae82d84d3a8e0c90ec1047b56155314ca4b41b30518e89`。依旗標限縮重錄四句／135 字元後全句重查，`atl040` 過，其餘三句仍標；`check-r8-redo1.json` SHA `3834e9e87ff797a857414d68827f64f7a75fb520807576be842f952e1880d32f`。再只重錄三句／111 字元後全句重查，仍是 `atl038,atl058,atl095` 三句；`check-r8-redo2.json` SHA `a1b2a11daf1ef9ad5f1000341d25504b37cc3a2760d93d2a9d615a65e090a80a`。每輪完整 WAV、時間線、檢查原樣、旗標與受標單句 WAV 都保留在私有 `/workspace/.video-work/curio-s48/review/`。

末輪轉寫把 `atl038` 的「船首」聽成「船索」（Jev 0.06）；把 `atl058` 的「這使」聽成「這是」（0.22）；`atl095` 的「菲爾德」聽成同音「費爾德」，另省書名號（0.25）。末輪 WAV SHA `3368bc0ee869f4467abc84545ef9ce6c684cb34b37740e5f0d0ac3907cd8216b`、時間線 SHA `af2d4d20faf32fa2faf7345d36b40be71ac253b0d9eaf520abbacba8fccee459`；30 fps 實測濃縮開場 **54.77 秒**、正文至片尾前 **10:58.40**、全旁白 **12:07.30**。這些時長不是音訊 PASS。

依預先限縮的兩輪上限，**R8 音訊 HOLD**；不送音訊核准、插畫、配樂或成片。下一版可定點改 `atl038/058/095` 的易混口播，守住 Russell／Field 來源與伏筆，再以新檔 SHA 重做獨立來源／畫面、兩位新讀者、全稿政策、網站卡與改句 TTS／全句零旗標音檢；舊政策或 R8 WAV 不可移作新版證據。
