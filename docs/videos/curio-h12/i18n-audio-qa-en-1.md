# H12 英語配音首輪 QA

日期：2026-10-17（Asia/Taipei）。本收據是首輪機械辨識與離線複核，**不代表英語旁白已經站主試聽核准**。

- 93／93 句 Gemini 配音已落盤，5237 計費字元，0 句沿用舊音；`dubs/en.m4a` SHA-256 `8CA592CB0E7D62593A39606DC3DC79B3DA95380F23B13C299049203468DB72AD`。合成預檢曾遇網站連線失敗，但失敗發生在服務狀態 GET，當時無付費 POST；連線恢復後才逐句合成，完成時無未決 speech journal。US$0.15 為保守估算結算，供應商最終帳單未提供。
- `check-audio --locale en` 對 93 句重新轉寫，1 次 TypeSafe Jev 差異判讀；77 句逐字吻合、4 句 Jev 接受、12 句旗標。`review/check.en.json` SHA-256 `69DC670595CBF0A7E21831C6B7510BAADFE3F00510504F9372EBB79967F1C95C`；`review/check-flags.en.json` SHA-256 `692DDFA20BC72D367BD2940A4B803FFE3465BEEBF0134C1050CA6AD1EDCAF05D`。QA 保守估算 US$0.50 已結算，實際供應商帳單未提供。指令因 12 句旗標而以 1 結束；不等於音軌通過。
- 用本機 faster-whisper small 對 12 句各做獨立盲轉寫，不另送供應商；文字檔 SHA-256 `7BC65C0DA193CF60AB5D6387A978BF61ECCEF10B230DC30B3BB9AC0E464BE555`。逐句試聽頁 `review/dub-en.html` SHA-256 `8DE41C86DC5D7386E9D256119B68F3E1EDFEF7B5AC354041EF5C82B426BFF10A`，先列旗標、可切換全部 93 句。

| 句 ID | 兩套轉寫與判定 |
| --- | --- |
| `9jra` | Gemini 與 Whisper 都聽成單數 **him**；核准英文稿是複數 **them**。這會改變指涉對象，優先請站主試聽。 |
| `anms` | 兩套都轉成 `Ducot(t)` 一類拼寫；核准稿為 `Ducat`。拼寫無法單靠轉寫判定人名讀音，請站主聽。 |
| `tbuz` | Gemini 聽 `Do`，Whisper 聽 `Did`；兩套對助動詞不同。 |
| `h8mk`、`5udf` | Gemini 把 Moore 轉成 `Nora`／`Maura`，Whisper 都聽成 Moore。 |
| `ds8v`、`s7g4` | Gemini 把 Muirhead 分成 `Muir had`，Whisper 分別為 Muirhead／Mirhead；需以音檔核對人名。 |
| `jjr5`、`phjr`、`yt2k`、`efzu`、`2d4b` | 日期序數、Moore／more、light-out／lights out、site／sight、tonne／ton 等聽寫差異；文字仍保留旗標供人工判定。 |

目前未依轉寫自行修改英文稿、重錄或宣布核准。站主試聽結果回來後只修有依據的句子，再更新音訊 QA、字幕與上傳包。

## 站主試聽結果

站主於 2026-10-17 對 `9jra` 的實際聽感回覆原文「聽到 them，英語旁白可以」。據此把現有英文音軌記為**站主聽感接受**；`9jra` 不重錄，其餘 11 句自動旗標、兩套轉寫與本收據原始判讀仍保留。這項回覆不等於 `publish`／`languages` 後台審核或 YouTube Studio 上傳。
