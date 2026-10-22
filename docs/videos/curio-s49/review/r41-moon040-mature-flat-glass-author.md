# S49 R41｜`moon040` 成年人物與平板玻璃作者窄修

2026-10-22 UTC。這是 [R40 `moon040` 首張原圖退件](r40-moon040-first-native-stop.md)後的**單景書面候選**，待非作者重新核來源、畫面及精確差分。沒有圖單重綁、第二張原圖、judge、TTS 或配樂費用。

固定 Locke 名下 [1859 年重印本 P05 L435–443](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L443) 說明**虛構報導中**，數週試驗後選用珠寶商櫥窗的純淨平板玻璃作焦像接收媒介；不是存世赫歇爾裝置或已做成的史實實驗。來源固定檔 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。R40 原圖 SHA `efd3a31f315a17a9096acbc76c98e171304835de08fbe2afdf32b6b7568f20ad` 同時被機器 9／10 FAIL 與兩次獨立原尺寸 HUMAN REJECT：畫成兩位童貌人物，用圓放大鏡放大左側人的臉，沒有平坦玻璃作影像接收媒介。

本輪只將 `scenes[36].data.prompt` 明寫為**一位灰鬢、成人面紋與寬肩的 1830 年代工匠**，拿著一片**四條直邊清晰可辨的平坦透明長方形玻璃**；桌上另有一枚小鏡片和簡單木托，兩個物件彼此分開。柔和窗光、想像中的年代工場；不畫第二人、孩童、人物臉反射、手持圓放大鏡、現代裝備或可讀字。同步只改 claims `moon040` 畫面欄，保留「又寫兩人試了幾週」的**旁白文字**、1859 重印本連結與虛構報導限制。鏡片與玻璃的相對擺法僅是概念插畫，不主張文獻有這一張器材圖。

[逐字可逆結構差分](r41-moon040-mature-flat-glass-structured-diff.json) SHA-256 **`f698c9852f6179c5cb8593491245dea88c8c08467ddb59a329815720a0484097`** 記錄 `scenes[36].data.prompt` 和 claims `moon040` 整行的舊／新位元；`after→before` 可精確還原 Git `04b58276b` 的 R40 `video.json` SHA `7c793e461696644e78e9723e0a2103e40746bf5e0e51c7c587da080d427f5f75`、`claims.md` SHA `93945e1368d357cd4baa178b156a46735f9de0d9b4ac6386c46f81eb60a023c4`。現 `video.json` SHA **`36d9ddcc442a686f6f88ddadd10e9f8dfc37d58400a07b716979993d0f379461`**、`claims.md` SHA **`fc4b77a6fe7929903d7492eb4afef0c1f0c566ea6116739934e7e927f8787b80`**；其他 **128 景**完整物件、全部 **131 句**台詞、`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 都不變。新 `visual_hash=540e3ad9a6188297`，`look_hash=98a370ae40badbaf` 不變。

CLI lint exit 0、**0 errors／0 warnings／131 lines**。單景只讀 `keyframes --shot moon040 --takes 1 --dry-run` exit 0、MiniMax `image-01` ready、提示 **516／1069** 字元；沒有生成圖片。正文仍 128 景＝117 shot＋11 big，插圖占 **91.41%**、最長連卡 2。私人 manifest **仍綁 R40** `visual_hash=12f2aee4595df518`、SHA `fdad71a266cdbe3c7fc7d2387fc3ebd39ff42918320b13504a0d992b5c89059c`，31 KEEP 實檔 SHA 全部核對；ledger SHA `792656daede23b96c2665b6975bfb8dc4db8430f61d9a1d651f4666fc600c122`，US$1.2150／90 image／90 judge／0 預約。STOP 在位、jobs 空。

**下一步先由非作者紙審 R41 凍結文字與來源。**通過後才可在 STOP 下精確重核 31 KEEP、離線重綁新 visualHash，做新鮮 MiniMax／US$5.30 整集上限預檢；至多一張第二次 `moon040` 原圖並看 1280×720 全尺寸。若又把人或玻璃畫錯，停止重試，改有來源註記的字卡並另做紙審。`moon041` 與完整 storyboard／成片仍 HOLD。
