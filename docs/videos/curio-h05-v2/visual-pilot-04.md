# H05 v2｜`open-note` 單張小樣人工退件

**後續處置：** 已以 c04 原生示意卡取代這張退件 shot 的候選主稿；新雜湊與離線檢查見 [open-note-diagram-revision-20261014.md](open-note-diagram-revision-20261014.md)。本頁及付費檔案仍保留原始退件收據，沒有把舊圖改成通過。

日期：2026-10-14。站主只授權 H05 一張 MiniMax 代表小樣；本輪僅對 `open-note` 執行一張生成與一次正常判圖，**不擴批、不重抽**。`video.json` SHA-256 `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3`，主稿的旁白、場景、look 與該鏡 prompt 未改；manifest 記 `look_hash=38b9efa0cb47553f`、`pictures_hash=6b3167e632a73379`。

| 項目 | 收據 |
| --- | --- |
| 鏡頭 | `open-note`，要求一隻成人手遞小張折起、外側無字的紙條，空服員只露袖口，臉全部出框 |
| MiniMax 請求 | `image-01`，seed 1，request key `61d0956a4a12d46c`，job ID `9ab14dde-209c-4989-9d9f-292df52059f0` |
| 圖檔 | `keyframes/open-note-1.jpg`；SHA-256 `9b25c3efd1178629ad7ccbf0cd89e400a82fcb2c6786f7ac9aeb268f27d4c266` |
| 自動判圖 | 總分 9.29，`passed=true`、`needs_review=false`；但 `details=7`，判圖文字明記多張乘客臉與機艙排椅超出 close-up 指示 |
| 費用 | MiniMax 圖像 US$0.0035，加 Gemini 判圖 US$0.0100，這一張合計 **US$0.0135**；帳本此時累計 US$0.1350，10 張圖、10 次判圖 |

人工打開完整 1280×720 JPEG 檢查：紙面沒有假字、2D 編輯插畫感也維持住，但前景紙張變成巨大的未折整張，機艙內出現多名有清楚五官的乘客，左側還有未要求的墨鏡人物；鏡頭被排椅和人物佔滿，觀眾讀不到原定「單手遞小張折紙給空服員袖口」的動作。此構圖會讓虛構乘客被誤認成案件中的目擊人物。**人工結論：`needs_revision`／退件；不可進正片、縮圖或當作美術通過樣張。** 自動總分不覆蓋其自身列出的關鍵偏差。

原始 JPEG、`keyframes/manifest.json`、`keyframes/contact-sheet.png`、`media/ledger.json`、當時 `video.json` 已逐檔複製並驗 SHA 到外部 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/visual-pilot-04-20261014/`。複本 manifest SHA-256 `aa89f3830cf9fb3343bd46aea3f4755ac8a93d7e4aca82f7d3ef04609ab006ba`，contact sheet SHA-256 `5c426e46592236c5aaac93f28703860e6d54f1050873a1340988bdd6c6d43d28`，ledger SHA-256 `7ed7e0157abb0553c714aef1293d6b4752bd83fa80850f5f511e7cb67b16b2eb`。保留原 manifest 及 judge 原話，不把 `passed=true` 改成假的退件收據；本人工決定另記在此文件。

這是三輪開場九張失敗後的第四輪單張代表小樣；它能局部證明 MiniMax 可輸出無假字的 2D 色調，卻再次未按案件敘事要求控制人物和道具。維持 **stop / no batch**。若後續改場景版型或提示詞，先評估已核准敘事、時間軸和 50% 插圖占比的重新綁定，不用此圖或這次自動 PASS 跳過 storyboard、全片實速審看與最終 QA。
