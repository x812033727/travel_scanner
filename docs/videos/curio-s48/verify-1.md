# S48｜前製候選與交接（R1）

2026-10-20 UTC。本檔記錄作者靜態檢查；**不是獨立史料查核、敘事盲讀通過、站台選案／核稿、成片或付費媒體驗收**。

| 固定稿 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `5a6f3e107bb21f7104d9a132d11bd4f38eb259e82f2448f44ff6a7fbd60f8680` |
| [research.md](research.md) | `da0be70bbba324df9bf84f87e88fbf061dfea935c9cbe5d662172aff502ce927` |
| [video.json](video.json) | `72ec6a1cfbd0c767a0e087ed53bc7b48ac293485bcd79a1b22b58c328da54608` |
| [script.md](script.md) | `9955e0fbd9f023e31926c3de2036b4091acbd6c38ee8d723f861bb6944f017de` |
| [claims.md](claims.md) | `7083fe431b7c7d69ef56fcebb112430ec781d8bd47f495a730f9000099d530ed` |

1865 年船上記者 Russell [固定文字檔](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt)的原始位元組 SHA-256 是 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`。Henry M. Field 後出的 [固定文字檔](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt)原始位元組 SHA-256 是 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。完整行段及見證層次在 `research.md` 的 P01–P16；`claims.md` 每句直連該固定版行段。作者程式比對 `video.json` 的 103 句與 `claims.md` 103 列，文字完全一致，**尚須另一人逐句讀原文與畫面提示**。

本機重生：`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s48`。同環境 `lint --slug curio-s48 --json` 結果 **0 errors／0 warnings**。稿含 11 個事件章（第一章為濃縮開場）、100 張預定 `shot`、18 個前後對應 `loops`，片尾另有 3 句；正文預定插圖占比 100%，但還沒有任何原生插圖。`look.preset` 是 `cute-mystery`；鏡頭只描述畫面內容，沒有讓模型畫可讀文件、指針數值、照片或海底攝影。

按 `estimateTimeline` 推算（每句有預設停頓，**不是 TTS 實測**）：

| 語速（單位／分鐘） | 濃縮開場 `atl001`–`atl008` | 正文 `atl009`–`atl100` | 片尾 3 句 | 含旁白的全部估時 |
| --- | ---: | ---: | ---: | ---: |
| 250 | 55.4 秒 | 10:45.1 | 16.3 秒 | 11:56.8 |
| 300 | 47.4 秒 | 9:11.8 | 14.0 秒 | 10:13.2 |
| 325 | 44.5 秒 | 8:37.6 | 13.2 秒 | 9:35.3 |

即使以 325 估，正文仍比八分鐘多約 38 秒；真正是否達標以合成後的正文音訊為準。30–60 秒濃縮後才安排系列原創 5 秒片頭；正片後預定共用 21 秒 `v4-endscreen`，最後約 16 秒留兩個推薦框和訂閱圈。動畫、片尾、音樂、字幕及影片**尚未生成或組裝**。可點推薦與訂閱連結須在私人上傳後進 YouTube Studio 指定並點測，本機框位不可點。

## 下一位查核者要核的具體邊界

1. 以原文 SHA 重抓固定版，逐句核 1865 年 Russell 的親見、船上測試及推論：`atl043`–`atl045` 不把船首斷線歸咎單一零件；`atl049`–`atl054` 的張力**不能**說成有人目睹海底端頭；`atl032`–`atl035` 不把船上破壞猜疑升成裁定。1858 已傳訊但停止可理解訊號，1866 不是首次跨洋通信。
2. 1866 年依後出 Field 書及其內引的日記、證詞復核 `atl069`–`atl098`：7 月 27 日是**新線先抵岸**；8 月 17 日舊線海面可見但五分鐘後斷；8 月底的殘片不是完整舊線；9 月 2 日舊線固定上船再驗電；9 月 7 日才有第二條抵岸。Field 本人不是全程隨船的 1866 第一手見證者。
3. 讓兩名未見本檔及彼此判讀的新讀者，依 `curio-episode` 官方題目各自盲讀此 SHA 定稿；如有修改，重生腳本、主張表、hash 與讀者結論。靜態 `lint` 不能代替他們的敘事判斷。
4. 站台 `hand_pushed` 仍要走 A 案／劇本審核及後續音畫門檻；沒有網站核准。先實測 Gemini 語音與 `check-audio`，按費用政策處理；MiniMax 試畫前三張需人工看原生畫面是否為 1860 年代的卡通器物。完成後再做品牌片頭、`v4-endscreen`、YouTube 私人上傳與連結點測，以及 `from-episode` Short。

選案 A 是依站主的持續推薦偏好作的**本地編輯選擇**。S48 尚非已完成影片，也未消耗圖像或語音費用。
