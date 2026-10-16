# A29 LEGO — 免費分鏡準備

閱讀 [完整分鏡](storyboard.md)，機器可讀版為 [storyboard.json](storyboard.json)。來源範圍見 [source-map.json](source-map.json)，原段逐字對照見 [paragraph-table.md](paragraph-table.md)。

- 65 段／2,201 字；83 畫面＝72 插畫＋11 數字來源卡，86.75% 插畫，最多 2 連卡。
- 正文估 487.68–530.09 秒，全旁白估 528.24–574.17 秒。5＋21 秒首尾另計，總估 554.24–600.17 秒。尚無實錄。
- 字數只取原稿第二節。舊表誤把 loops 中的 8 行也算進正文；這包不改原文 bytes，也不改 repo 舊指標，已交 root 作獨立修正。
- 所有原段 ID／文字／順序重建一致；shot_reading 72 張插畫、0 traps；純結構檢查見 [checks.json](checks.json)。
- [offline-shot-reading-input.json](offline-shot-reading-input.json) 只供免費鏡頭讀法；diag001 等 ID 非正式台詞 ID。其估時含工具預設間隔，不可當實際片長或套進正式稿。
- `prepare.mjs` 只產初始剪點；83 鏡畫面由 `visual-design.mjs` 逐鏡人工設計，`assemble-storyboard.mjs` 負責來源、還原、統計與文件組裝。
- 此包不是 formal chapters、worker PASS、製作／付費／匯入／上架核准。只寫 Temp，未呼叫主機、模型、TTS、產圖或媒體工具。

正式章稿、實際 verifier/listener/narrative、全片報價、實錄估時、圖片評審、成片與站主驗收仍待後續；A01／B18 優先。
