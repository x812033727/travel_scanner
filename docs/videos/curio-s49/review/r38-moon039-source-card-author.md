# S49 R38｜`moon039` 虛構顯微鏡比方來源卡作者候選

2026-10-22 UTC。**只提出書面來源卡；固定來源與版面仍待非作者紙審。**[R36 首張](r36-moon039-native-stop.md)把虛構比方畫成童貌人物、口鼻前的鏡筒與書上的藍色水窪；[R37 第二張](r37-moon039-second-native-stop.md)修好成年面貌，卻有三隻手、未對上目鏡，前景大透明杯取代玻片單滴。兩張均 HUMAN REJECT；本輪不買第三張。

本輪只把 `moon039` 從 `shot` 改成 `big`，三行如下：

| 位置 | 字樣 |
| --- | --- |
| 上標 | **1835 年報導的虛構顯微鏡比方** |
| 主文 | **一滴水，蚊幼蟲放大到幾英尺** |
| 下標 | **1859 重印本所載，非實驗紀錄** |

固定 Locke 名下 [1859《The Moon Hoax》重印本 P05](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 的 L428–434 在**假設語氣**裡拿一滴水中的 *larvæ of a gnat* 經顯微鏡放大到 *many feet* 作比方，再推想望遠鏡焦像；不是已做的水滴測試。固定 [Jacoby 1902 評論](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` 稱整段為 *imaginary conversation*。卡片和 claims 同列只轉述故事中的概念，沒有宣稱赫歇爾／布魯斯特真的做實驗、量測幼蟲、在月上發現幼蟲，或保存了標本／1835 原報影像；「蚊幼蟲」沿用已核准的口播翻譯，不再細分物種。既有旁白及 P05 來源錨點不變。

[逐字可逆結構差分](r38-moon039-source-card-structured-diff.json) SHA-256 **`b4c268c3c3d0352f6e721cefa68c4ac781e40a8903ddcb9a99f6d10f58651e59`** 唯一記 `scenes[35]` 的 `template/data` 與 claims `moon039` 畫面列。將新 scene 區塊與 claims 新行反填舊值，逐位元還原 Git `8e285ae64` 的 `video.json` SHA `b46cba46a708b1f8c2a9e36ed4fd26d94d03532b2594f06c6f6de4f5b27b0535`、`claims.md` SHA `9f856f9cccfba14180b5834cf0f6ea00a63e8cd9f5af579070ee77894097efc3`。現 `video.json` SHA **`5d899f4e40c792761e9935345191af3f1f4637532a85c82b6f90e6be776c8d4c`**、`claims.md` **`5bda4ed9c7b7242ae5b3ae3b34c94ed6f70f4b00b3dc6cc08c7a15dfaf9287bc`**；其餘 128 個 scene、全部 131 句口播、`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 均未變。

工具重算 R38 `visual_hash=c2f2beaa8befb76d`，`look_hash=98a370ae40badbaf` 不變；`renderPlan` 證明 `moon039` 是一個 `stills` 大字卡，三行文字都進入畫面。正文 **117 shot／11 卡＝117／128＝91.41% 插圖**，最長 **2** 張連卡，符合系列至少 70% 插圖／最多 3 連卡。使用同一主題、字型與本機 Chromium 離線繪製 1920×1080 卡面，所有文字在畫面內，layout/refused-resource 問題 **0**；私人截圖 SHA `0accdbf12dbbb9834e0827ad0b2f564745194f6c0894caf1a1c6209d7fc81fc2`。`lint --json` exit 0、**0 errors／0 warnings／131 lines**，`npm run test:docs-videos` **236／236 PASS**，沒有 image、judge、TTS 或其他付費請求。

私人 active manifest **仍綁 R37** `visual_hash=d6bf4ef8a3456363`，SHA `faff6b0cc2f8e150b5e38c4ebc483be61411d070fd30350947265183cc058e83`；31 張既收圖及所選實檔 SHA 全相符，沒有 `moon039` 退圖入選。ledger SHA `b022285fdfdc39149d90579e612265235263893d6f5f3cca6321483df6f0b059`，**US$1.2015／89 image／89 judge／0 預約**，低於整集 US$5.30；STOP 在位、jobs 空。**先交非作者核固定來源、條件語氣、卡片文字、可逆差分、版面與 31 KEEP；PASS 後才能在 STOP 下只換 manifest `visual_hash`。**`moon040` 不因本作者候選放行付費；完整 storyboard／站主卡／人耳及成片仍 HOLD。
