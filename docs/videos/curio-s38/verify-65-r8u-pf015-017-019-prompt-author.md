# S38 R8u｜第一章四景提示詞窄修，作者候選

2026-10-22 UTC。**R8u 只有作者稿，待另一位工作者獨立書面覆核；尚無新原生圖 KEEP，也沒有放行付費重畫。** 經 [R8t 書面預檢](verify-62-r8t-pf015-022-independent.md) 與 [三張原圖停止回條](verify-63-r8t-pf015-017-native-stop.md)，PF015–017 各一張原生 1280×720 圖皆 REJECT：PF015 有現代道路、汽車和黑邊，PF016 有童貌東亞制服、偽字地圖和室內電燈感，PF017 多個童貌人物使成年佩皮斯失焦。PF019 原稿 `near city Bridge` 有已發生過的 1894 Tower Bridge 誤畫風險，維持不購圖直到新稿獨立核對。

## 固定來源與四景改動

[1666 年 9 月 2 日佩皮斯日記 L65807–65834](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65807-L65834)，固定原文 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，明確區分：塔上親見橋端房屋起火、下塔後**聽**官員說火源、再搭船才看到 Michell 家已燒。四個旁白及 `claims.md`、`script.md` 一字未動，原圖失敗只在畫面指令。

| 景 | R8u 畫面指令意圖與仍須原圖檢查的風險 |
| --- | --- |
| `pf015` | 改成 1666 年塔內石瞭望口的**單一成年書記官**抓石欄；窄窗只露低屋頂和一束遠煙，不要求看整條街，降低現代汽車／道路及黑邊風險。仍須檢查原圖是否成年、17 世紀、無車、無黑帶。 |
| `pf016` | **單一成年塔官**在石室對畫框外聽者開口，桌子全空；不再要求兩人互動、地圖、文字或制服。這只能表示口頭轉述，不能畫成佩皮斯目擊烘焙屋起火。仍須原圖查角色成年與英國 1666 年服飾。 |
| `pf017` | **單一成年佩皮斯**在塔內側身傾聽，窄窗與石牆只是背景；不再畫火源或多人圍窗。仍須原圖查其他臉是否被模型加進來。 |
| `pf019` | 保留**搭船後**的時間位置；框內只見木船、成年書記官、燒黑屋牆／下垂屋頂和煙，不要求橋體、精確街圖或現代城市全景。這是 Michell 家損失的原創示意，不是可考證的該屋立面。仍須原圖查模型是否擅自加入 Tower Bridge。 |

上述新 prompt 皆只描述畫面，不加 `look.style`／`negative`，沿用固定 `cute-mystery`；相機路徑、鏡位次序、逐句史實、日期、章節、片頭片尾與音檔不變。PF018／PF020–022 先前只得書面 PASS，沒有原生圖，不在本輪改稿與付費範圍。PF009／PF013／PF014 仍是來源引句卡，不回選先前退件圖。

## 精確差分、檢查與停點

[可逆結構化差分](verify-65-r8u-pf015-017-019-prompt-structured-diff.json) SHA-256 `265196678f04ba45f09fdefe9979bbbbdc89de3a4ced66afe7d6dd85f3f1bcd4`，以 #1641 乾淨工作樹 R8t `video.json` SHA-256 `35a23a36a8503988bdb70ff2dc2c6e3bd2f02c226891a5119f3b9756b86d2532` 為基準，只變 `scenes[14/15/16/18].data.prompt`，正向與反向 JSON 重建皆逐位元組等於檔案。R8u `video.json` SHA-256 `2d04002c0c4642d7cbac9cf541d03fdfb09a0c39e2dacca1b1be21371ebe23e9`；未改 `script.md`／`claims.md` SHA-256 分別 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json`：**0 errors／0 warnings**，112 句，估算 10.016 分鐘；正文 111 景仍有 106 張 `shot`（95.5%），最長連續字卡 2 景。首輪新 prompt 的 `London`／`linen` 使用頻率曾觸發兩條視覺重複警告，已改為不失時間地點的 `Tower`／`Thames` 與多種樸素領口詞；最終 lint 零警告。沒有換成卡片、增加橋畫面或改故事。

私有 `STOP` 仍在位；`media/ledger.json` SHA-256 `86bf09c92238cfc7ff44001955c19bf6cd5e580e64bc52e342ea91f0c1bca6c4`，**US$0.6235／41 image／40 judge／1 music**；`keyframes/manifest.json` SHA-256 `121fa94cb357ee891b1c8c4b01df909753a536f9b58bc6b69d1decd39c81fcfa`，九張舊 KEEP 的 entry／檔案未動，PF015–017 的舊機器結果仍是**人工 REJECT**。整集硬上限 US$4.58 未變；本次沒有 MiniMax、judge、配樂、render 或任何其他付費呼叫。後續請另一位先在 R8u 雜湊上核對精確差分、日記親見／聽聞／搭船時序、提示詞及 STOP／九張 KEEP，才決定哪些 ID 能在剩餘預算內各試一張；每張仍需看完整未裁切原圖，三張同類錯誤即停。
