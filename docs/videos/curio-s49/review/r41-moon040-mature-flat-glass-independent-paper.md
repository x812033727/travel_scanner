# S49 R41｜`moon040` 成年人與平板玻璃非作者紙審

2026-10-22 UTC。**固定史料及書面畫面 PAPER PASS，僅限凍結 R41 的 `moon040` 窄修。**我不是 R41 作者；本結論沒有核准新原圖、整章 storyboard 或成片，也沒有改動作者文稿、私人 manifest、帳本、任務或 PR，沒有付費媒體呼叫。

## 來源與可畫性

我重新讀 Locke 名下 1859 年《The Moon Hoax》重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 的 [P05 L435–443](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L443)：虛構報導說幾週試驗後，取珠寶商 Desanges 的櫥窗 **plate glass** 作為焦像承接媒介。它不是赫歇爾實際器材、實驗紀錄或留存圖像；Jacoby 1902 年評論 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` 只把相關光學對話辨作荒謬的想像對話，沒有核證器材。原旁白「**又寫**兩人試了幾週，挑一片珠寶店櫥窗玻璃來承接影像」與 claims 的「虛構報導的想像畫面」維持此界線。

[R40 首張原圖退件](r40-moon040-first-native-stop.md)所封存的 1280×720 原圖 SHA-256 `efd3a31f315a17a9096acbc76c98e171304835de08fbe2afdf32b6b7568f20ad` 我另行完整檢視：兩個童貌人物，一個巨大圓形金框放大鏡對著左方人臉；沒有平面櫥窗玻璃與獨立鏡片。R41 新提示明確收窄為**一位灰鬢、面紋、寬肩的成熟成人**，只做**手持平坦透明長方形玻璃片**這一動作，四條直邊可見；另一枚小型簡單鏡片在桌上的木座，非手持放大鏡。1830 年代英國工場、樸素年代工作衣、柔和窗光以及排除第二人、孩童、臉部反射和現代設備，正面對準 R40 的人物、物件及光學作用錯誤。小片尺寸和木座是**概念插畫的構圖安排**，不宣稱來源記下玻璃尺寸或真實裝置；不能把新畫面介紹為存世照片、原報插圖或成功實驗。

紙審 **PASS** 表示此提示可以接受一次受守衛的原圖測試，**不預判模型必能畫出四邊、成年外貌或分離的鏡片**。原尺寸驗收須再核人物不童貌、玻璃確實為直邊平片、沒有放大人臉，以及畫風／年代和來源界線；若重複 R40 的人物或玻璃錯誤，應 HUMAN REJECT 並停下，不連續購圖。

## 精確差異與私人守衛

- 凍結 `video.json` SHA-256 **`36d9ddcc442a686f6f88ddadd10e9f8dfc37d58400a07b716979993d0f379461`**、`claims.md` **`fc4b77a6fe7929903d7492eb4afef0c1f0c566ea6116739934e7e927f8787b80`**、[R41 可逆結構差分](r41-moon040-mature-flat-glass-structured-diff.json) **`f698c9852f6179c5cb8593491245dea88c8c08467ddb59a329815720a0484097`**。我獨立把差分的 `after→before` 原始位元組各替換一次，兩檔精確還原 Git `04b58276b`：R40 video SHA `7c793e461696644e78e9723e0a2103e40746bf5e0e51c7c587da080d427f5f75`、claims SHA `93945e1368d357cd4baa178b156a46735f9de0d9b4ac6386c46f81eb60a023c4`。129 景只 `scenes[36].data.prompt` 改，其餘 128 景完整物件、所有 131 句台詞、`camera` 與 `visual` 均相同；claims 只 `moon040` 一行的畫面欄改。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 不變。
- 我獨立跑 `node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0：**0 errors／0 warnings／131 lines**；`keyframes --shot moon040 --takes 1 --dry-run` exit 0、提示 **516／1069** 字元、MiniMax `image-01` ready。這是只讀 dry-run，工具印的通用 US$200 cap **不是**本集授權上限。畫面仍 129 景（117 shot、11 big、1 outro），正文插圖 **117／128＝91.40625%**、卡片連續上限沿用 R40 兩張。新 `visual_hash=540e3ad9a6188297`；系列 `look` 未變。
- 私人 active manifest `/workspace/.video-work/curio-s49/keyframes/manifest.json` SHA-256 **`fdad71a266cdbe3c7fc7d2387fc3ebd39ff42918320b13504a0d992b5c89059c`** 仍綁 R40 `visual_hash=12f2aee4595df518`，不能直接用它畫 R41。31／31 張 selected KEEP 實檔 SHA 均相符，沒有 `moon040` 入選、其他圖單問題為 0，86 景仍未畫。私人 ledger SHA-256 **`792656daede23b96c2665b6975bfb8dc4db8430f61d9a1d651f4666fc600c122`**：**US$1.2150／90 image／90 judge／0 預約**，距本集 US$5.30 上限餘 US$4.0850。`STOP` 在位，`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 jobs 空。

**結論：R41 `moon040` 書面候選 PAPER PASS。**下一步須在 STOP 下驗精確文稿／本紙審雜湊、31 KEEP 實檔、帳本及 jobs，僅離線重綁新 `visual_hash`；之後重新檢查即時媒體額度與整集 US$5.30 上限，才可買**至多一張**第二次 `moon040` 原圖及 judge。必須完整原尺寸人工驗收，失敗即恢復 31 KEEP／STOP，`moon041` 不跟著購買。這張紙審不取代分鏡、網站、聽音或成片關卡。
