# H12 日語配音 QA 暫停與復原收據

日期：2026-10-17（Asia/Taipei）。前五項保留連線失敗時的歷史狀態；文末記錄後續復原。此收據不得當作整語站主核准。

- 日語成音 `dubs/ja.m4a` SHA-256 `9115BCF7624D6FC0B8192C8E1445AC965345F76AE49AC3DEDB471DB27B81F197`；93 句時間槽均可容納。`check-audio --locale ja` 只快取前 33／93 句，`review/check.ja.json` 仍缺第 34–36 句及後續 57 句，尚無完整 `check-flags.ja.json` 或正式逐句試聽頁。
- 第 34 句 `s4hn` 的轉寫請求 SHA-256 `552bce02d80b66c963533c7ef75d6c4291c1a0a3c6fa737eafe0099ba65503fe`、音訊酬載 SHA-256 `d0b822703a3f7074ec66ae0b48ac76176de20d222623d4b6ceaad73a1da3e6e5`、186924 bytes。首次於 2026-10-17 02:35:38 UTC 送出，speech journal 記 `held`，原因為 `no usable answer came back (other side closed)`；原 journal 已封存於 `<VIDEO_WORKDIR>/curio-h12/review/held-ja-s4hn-552bce02…json`，封存檔 SHA-256 `386D30B724393CA9FC66C4C45C2D9E1A15595E2BE97916534917CB83E1AA58F3`。
- 站主其後只授權這一筆再送一次並接受可能重複計費。清除該筆 held 後工具確實送出同 SHA 一次，但沒有取得可用 `s4hn` 轉寫；接著第 35 句 `fgbf`、第 36 句 `ey9a` 也屬 service 類失敗，連續三句後工具停跑。這輪 stdout 沒有另存，無法從目前檔案確認後兩句的確切 HTTP code；journal 目前沒有 pending／held 項，供應商帳單仍不可見。之後 Jev 階段亦因 `cannot reach https://mokaair.com: fetch failed` 結束。不能把離線辨識算成完整機械 QA。
- 本機 faster-whisper small 對三句的免費複聽見 `<VIDEO_WORKDIR>/curio-h12/review/whisper-small-ja-unchecked-20261017.txt`，SHA-256 `2C43F4EA2C7FE098CF7459F77AF808290D50FD573D4A42945B1D4B095AE0FAF3`。`fgbf`、`ey9a` 支持稿文；`s4hn` 將「記す」誤轉近音「知るす」，其餘意義吻合。這只能協助人工試聽，不能替代未完成的 Gemini／Jev 關卡。
- 外部五集帳本把本語 QA US$0.50 和一次可能重複計費 US$0.05 全額保守計入。當時 H12 US$5.785／8.50，五集合計 US$27.7795／41.50。站主後續另同意在站台穩定後，`s4hn` 再試一次、`fgbf` 與 `ey9a` 各受控試一次，三句合計另保守預留 US$0.15；此項在暫停當下尚未預留或送出。當時本站只讀 HTTPS GET 連線逾時，因此未啟動日語或韓語付費 QA。

## 連線恢復後的結果

- 站台只讀檢查穩定後，先完成獨立韓語 QA 並結清其預留；再將上述三句可能重複計費風險 US$0.15 計入帳本。此金額包含 `s4hn` US$0.05、`fgbf`／`ey9a` 各 US$0.05，供應商帳單仍不可見。
- 僅執行一次標準 `check-audio --locale ja` 續跑，未使用 `--force`、自製快取或額外的單句重送。工具沿用原先 33 句快取；`s4hn`、`fgbf`、`ey9a` 依序各取得一筆可用轉寫，接著完成其餘首次轉寫。`s4hn` 逐字吻合，`fgbf` 的「石版／石板」屬字形差異，`ey9a` 逐字吻合。完整 stdout 保存為 `<VIDEO_WORKDIR>/curio-h12/review/check-ja-resume-run-20261017.log`，SHA-256 `1B4F45A59712D9AF6D4CB20E90DFD6EEDA73F831F68B504639F953D4EA4960D0`；完成時沒有未決 speech journal。
- 日語機械 QA 現為 93／93 句：43 句逐字吻合、23 句由 TypeSafe Jev 接受、27 句留旗標。`review/check.ja.json` SHA-256 `39682043F0DE598B6B33F9BC5E07D81E23A6E4B0B0F80072CC590667DA370DD5`；`review/check-flags.ja.json` SHA-256 `CAD29E0BD9B49DC2C0E2C0659877E03DB46EC4773044C376A5117E5543AB1C4F`。指令因旗標以 1 結束，尚須站主試聽，不能記為音訊核准。
- 日語 QA US$0.50 與三句風險 US$0.15 已在外部共享帳本保守結清；截至此步 H12 估算 US$6.435／8.50，五集合計 US$28.4295／41.50。這些是停手用估值，不是供應商美元帳單。
