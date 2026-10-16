# B14 免費分鏡準備

[完整分鏡](storyboard.md)｜[機器格式](storyboard.json)｜[原段對照](paragraph-table.md)｜[來源範圍](source-map.json)｜[原文差異](adaptation-manifest.json)｜[離線檢查](checks.json)

48 段／2161 字／83 鏡；75 插畫、8 卡，最多 2 連卡。六章旁白正文 body 估 518.64–563.74 秒；開場後五章另估 472.56–513.65 秒（僅分析分段，不是正式 body 門檻）。片頭 5 秒＋片尾 21 秒另計，總估 544.64–589.74 秒。尚未實錄，不補停頓充長。

六章完整旁白正文 body 字數估算在八分鐘以上，但仍未有配音實測，不能視為長度關卡通過。

原始全文與 active worker row／review／整合 manifest／修正字數各自 pin hash；原正文按明確 H2 範圍及六章取得，再逐段比對 corrected metrics 的 text hash。來源 URL 取 active row，不把舊入口冒充現行來源。

本包僅 Temp 編輯準備，沒有 repo、主機、模型、付費、TTS、產圖或 worker 收據操作。先 A01／B18；本集正式 chapter、來源／聽稿／敘事審查、實錄、整片報價、圖片評審與站主看片都還待做。

`offline-shot-reading-input.json` 的 diag IDs 只供官方讀法測試，工具自帶時間間隔不可用來冒充本片實測。`build-prep.mjs --prepare` 產建議剪點，`visual-design.mjs` 是逐鏡人工設計；正常 build 組裝輸出並檢查。
