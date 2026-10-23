# H11 分鏡插畫 QA：70 鏡

日期：2026-10-16（Asia/Taipei）。本收據綁定 H11 `video.json` SHA-256 `FE86AE2B1795834CA23FC2E032A3DD8AD5C2DF72840AA13116898319C2FB3624`、`script.md` SHA-256 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108`。只改了三鏡的畫面提示詞；已核准的 75 句劇本文字與旁白時間軸未改。`lint --slug curio-h11` 為 0 errors／0 warnings；`status` 讀回 script approved、narration approved、keyframes drawn，storyboard 尚未核准。

MiniMax image-01 1K 產圖、Gemini 九題逐圖評審。第一輪 `keyframes --takes 3` 製作 70／70 鏡，103 次圖片與 103 次評審，67 鏡通過；三鏡完成三 take 後仍失敗：`strange-writing` 出現可辨漢字，`paper-published` 出現標誌或數字，`story-removed` 出現未連接的手或漂浮紙張。依失敗原因只重寫這三鏡提示詞，閉合手稿與期刊不露可辨文字，撤稿改為編輯把單張空白新聞稿收進抽屜。定向執行 `keyframes --shot strange-writing,paper-published,story-removed --takes 3`，無 `--force`；工具讀回 **67／70 原有鏡頭保留評審結果**。新圖分別於 take 1、take 1、take 3 通過，分數 9.29／10、10／10、9.29／10。

最終 `keyframes/manifest.json` SHA-256 `30B7D6CEB8CD441A1D85DC8BDA684C90E959753B954ECD1216FE362C96EFFC99`：70／70 鏡有圖、70／70 評審通過、0 `needs_review`。本機媒體帳本 `<home>/mokaair-work/videos/curio-h11/media/ledger.json` 合計 **US$1.458 工具估算、108 圖片、108 評審**，`reserved=0`，無 held／unknown／failed 請求；不是供應商最終美元帳單。首輪與定向修圖均在預留的 H11 插畫額度內；主代理已把共用停手帳本的修圖預留 US$0.13 結算為實際估算 US$0.0675，與旁白及音訊 QA 的保守估算 US$0.70 合計 **US$2.158**、無未結預留，低於本集 US$6 停手上限。

逐頁目視最終聯絡表，三個原先的文字／漂浮物件問題已消除。其餘鏡頭維持已通過評審的可愛插畫，沒有看到與旁白相反的史實畫面；少量道具或景別偏差按 `curio-episode` 驗收規則保留，交站主看分鏡時可逐鏡提出調整。聯絡表：

| 頁 | 本機檔案 | SHA-256 |
| --- | --- | --- |
| 1 | `<home>/mokaair-work/videos/curio-h11/keyframes/contact-sheet-01.png` | `0DEDAE3452A410EF7BEE8A1C5562D40356174252A8F5DB50C620AC33ED0B9374` |
| 2 | `<home>/mokaair-work/videos/curio-h11/keyframes/contact-sheet-02.png` | `5BD441E59204D9ED28FA72E3335F5751708F943510E1BD29F083E51313E3DC45` |
| 3 | `<home>/mokaair-work/videos/curio-h11/keyframes/contact-sheet-03.png` | `3CBC4928D44E9FFFF677184B006BC064CD595A8FFE948B5C192678CEF7264A0B` |

已執行 `review-push --slug curio-h11 --gate storyboard`，工具回報 `storyboard submitted for review (pending)`；隨即 `review-pull --slug curio-h11 --gate storyboard` 現場讀回 `storyboard: waiting for the owner`。站主看三頁聯絡表核准後才能製作成片。尚未製作成片或上傳。
