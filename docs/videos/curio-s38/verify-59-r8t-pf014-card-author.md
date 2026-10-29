# S38 R8t｜PF014 日記引句卡退路，作者凍結

2026-10-22 UTC。R8s `pf014` 依獨立書面 PASS 單景試畫後，[未裁切 1280×720 原圖](verify-57-r8s-pf014-native-stop.md)因上下黑色 letterbox 寬帶 **REJECT**；機器 9.71/10 仍 FAIL，裁邊版不能取代原圖驗收。此景已有三次原生生成紀錄（首輪退件、R8q 舊運鏡 KEEP、R8s 新運鏡退件）及兩輪提示詞／運鏡修訂。舊 KEEP 圖與 R8s 新 request key 不符。**R8t 停止為 PF014 購買第四張圖片，只把 PF014 改為來源引句卡；不改其他景、旁白、章節、系列畫風或已收圖。**

## 來源界線與卡片內容

[1666 年 9 月 2 日佩皮斯日記 L65807–65819](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65807-L65819)先說他在倫敦塔高處看見橋端房屋起火，`which, among other people, did trouble me for poor little Michell and our Sarah on the bridge`；**下塔、搭船之後**，才寫 `Poor Michell's house ... already burned`。卡片保留一個署明日期與出處的中文譯文：「我為橋上的米切爾和莎拉擔心」。它對應旁白「橋上的火，讓他掛念那裡一戶熟人的家」，只表達當時的擔憂，不說他已在塔上確認那棟房子燒毀，也不推定米切爾與莎拉的親屬關係。PF019 的「到了船上才看見熟人家已燒」仍是首次確認。

R8s 的 PF013 已是同日記「橋那端的房屋全在火中」引句卡；兩張連續卡先交代**所見火勢**，再交代**心中所掛念的人**，不重複同一主張。PF015 隨後恢復塔上插圖。卡片用既有 `big` 模板，只含譯文引句、來源及日期；不把模型生成的錯橋或有黑邊圖片帶入成片。

## 精確差分、檢查與停點

[兩欄可逆結構化差分](verify-59-r8t-pf014-card-structured-diff.json)只改 `scenes[13].template`（`shot`→`big`）及 `scenes[13].data`（原 prompt／camera／visual→引句／來源／日期）。R8s 基準 `video.json` SHA-256 `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`；R8t 作者稿 `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532`。把新兩欄換回舊值，已實際逐位元組重建 R8s SHA。`script.md`／`claims.md` SHA 仍為 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。

正文 111 景中 **106 景 `shot` = 95.5%**，最長連卡 **2 景**（PF006／007、PF013／014），符合至少 70% 插圖與最多 3 張連卡。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json` 為 **0 errors／0 warnings**；112 句、10.016 分鐘不變。PF011／PF012 雖都屬 `drift`，下一張 `pf015` 是 `push in`，無連三鏡運動錯誤。沒有跑付費 `keyframes`、judge 或 render。

私有 `STOP` 在位，ledger SHA-256 `660db85effcba9197da0b1b3802ca05cab2a54a4950103f848139498c4df35ea`，仍 **US$0.5830／38 image／37 judge／1 music**，另有舊 PF003 US$0.0035 reservation，低於本集 US$4.58 上限。舊 keyframe manifest SHA-256 `3da69280990b2639f2efdc657f55b3a3239f5fbab64cb478412379fc554f118d` 綁 R8s，包含一張已退 PF014，**不是 R8t 通過圖單**；後續須按新 `pictures_hash` 重綁並查九張其餘 KEEP 的 request key、judge stamp、選圖 SHA。PF001–005、PF008、PF010–012 九張 KEEP 內容未改；PF009、PF013 的獨立書面 PASS 引句卡未改。此頁只凍結作者候選，**待另一位獨立書面覆核**兩欄差分與日記親見／擔憂／搭船後確認的順序，才往 PF015–022 繼續；第一章與全片尚未完成。
