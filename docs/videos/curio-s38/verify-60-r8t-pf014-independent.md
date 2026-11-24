# S38 R8t｜PF014 日記譯文卡獨立書面覆核

2026-10-22 UTC。**書面 PASS：PF014 的來源引句卡可作作者候選，無須再為本景購買原生圖。** 此票只認日記譯文、精確差分與版面／狀態檢查；不宣稱第一章或全片畫面已完成。R8s PF014 新原圖因上下黑帶退件，本輪沒有重試圖片、judge 或 render。

## 1666 年 9 月 2 日的所見、擔憂、後來確認

直接核固定 `/tmp/curio-s38-pepys-4200.txt`，SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，L65807–65819。佩皮斯先在倫敦塔高處看見橋端房屋起火，接著寫 `which, among other people, did trouble me for poor little Michell and our Sarah on the bridge`；**之後下塔、到河邊搭船穿橋，才**記 `Poor Michell's house ... already burned`。PF014 卡片「我為橋上的米切爾和莎拉擔心」是前一段關於人物的中文節譯，保留的是**擔憂**，沒有把後一段的房屋燒毀提前當成塔上親見，也沒有推測兩人的親屬關係。`kicker=佩皮斯日記・中文譯文`、`sub=1666．09．02` 正確標明譯文與日期。PF013 緊前一張卡講「橋端房屋在火中」的所見；PF014 改講所掛念的人；PF019 仍是上船後首次確認熟人房屋損失。旁白及相鄰景沒有被改寫。

## 精確反向檢查與版面

現行 `video.json` SHA-256 `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532`，與 `verify-59-r8t-pf014-card-structured-diff.json` 新值一致。逐一核 `scenes[13].template` 為 `shot`→`big`、`scenes[13].data` 為舊 prompt／camera／visual→日記譯文卡，ID 仍 `pf014`。只復舊這兩欄後，原檔相同格式的位元組 SHA 精確回到 R8s `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`。其他 `video.json` 欄位沒有隱性變動。`script.md`／`claims.md` SHA-256 仍為 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。

正文 111 景中 `shot` **106／111 = 95.5%**，其餘五張 `big` 卡；最長連卡 **2 張**（PF006／007、PF013／014），符合至少 70% 插圖、最多 3 張連卡。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json` 實測 **0 errors／0 warnings**，112 句、約 10.016 分鐘。PF011、PF012 的 drift 運鏡後，PF015 為 push in，沒有新增三連同運鏡問題。

## 私有圖單與停點

STOP 在位；ledger SHA-256 `660db85effcba9197da0b1b3802ca05cab2a54a4950103f848139498c4df35ea`，仍為 **US$0.5830／38 image／37 judge／1 music**，舊 PF003 US$0.0035 reservation 未動，低於全片 US$4.58 硬限。舊 manifest SHA-256 `3da69280990b2639f2efdc657f55b3a3239f5fbab64cb478412379fc554f118d` 仍含 R8s 退件 PF014（`needs_review=true`），**不是 R8t 的可用圖單**。另外九張已收 PF001–005、PF008、PF010–012 的現行 manifest entries 與 R8s 批後備份逐項相同，九個所選檔案 SHA 各符合 entry。R8t 的 PF009、PF013、PF014 是文字卡，不得從舊 manifest 取其退件圖片。

**下一步：**依 [R8t 後續任務](verify-61-r8t-next-task.md)先書面審查 PF015–022 未畫提示詞與新圖單失效範圍，再決定單景有界原生抽樣；本票沒有放行付費或更大批次。
