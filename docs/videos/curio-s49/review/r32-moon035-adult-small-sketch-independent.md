# S49 R32｜`moon035` 成年讀者／小型示意紙獨立紙審

2026-10-22 UTC。**固定史料與逐句主張 PASS；R32 單景書面畫面 PASS；原生圖與整集 storyboard 仍 HOLD。**本審沒有修改創作稿、私人圖單或帳本，也沒有圖片、judge 或其他付費呼叫。

## 固定來源與修補範圍

重新讀取 Locke 名下 **1859 重印本** `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L413–418](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L413-L418)確實由光量不足轉向「人工光能否穿過焦點裡的影像」的提問。Jacoby **1902 評論** `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4092–4109](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4092-L4109)稱其為 *absurd imaginary conversation*。`moon035` 旁白「紙上的赫歇爾忽然問：能不能讓人工光穿過焦點裡的影像？」只講報導內虛構提問，不宣稱真正的赫歇爾做過此試驗；來源也沒有一張可核驗的焦點草圖。

[R31 退件原圖](r31-moon035-native-stop.md)把成年讀者畫得像少年，並把兩條抽象光線畫成巨幅放射海報。R32 將主體限為**一名可辨中年的讀者**，加灰白鬢角、鬍子、額紋、成年肩型和 1830 年代高領禮服；紙被限為**手掌大小、平放木桌**的空白紙片，僅有細小中心點和兩條短而無字的鬆散墨線。疑問手勢、自然光和明寫「概念示意，不是存世圖紙」均吻合該句旁白的敘事視角。讀者作為觀眾理解虛構對話的示意人物，沒有冒充赫歇爾肖像；文字也沒有要求真實儀器、原始報紙版面或可讀公式。**書面 PASS** 只放行有界原圖試驗：若生成的臉仍偏少年、紙又變直立巨幅海報或具體設計圖、出現現代燈具／儀器／可讀文字／黑邊，仍須人工 REJECT，不能靠機器分數收圖。

## 可逆差分與私人證據

現行 `video.json` SHA-256 **`33c5340f8c84888851fe4e968a7ec316431e8d721e95ef1e2390ff639dce15f5`**、`claims.md` **`27ac2780c03c2aa7f2fccc041f18dcfbf007187eeec8015402c6532a67c48463`**，與[作者可逆差分](r32-moon035-adult-small-sketch-structured-diff.json) SHA-256 `993b528d730e3d5a29e716f66b287c7e16a33ab0fc441a740cbbe0d1277e50bd`的 `after` 一致。獨立以唯一 `scenes[31].data.prompt` 及 claims `moon035` 畫面列 `after→before` 倒填，精確還原 R31／Git `cf9e18ef0` 的 `video.json` `df908e395da02b427bea4f6ae03c3ca69c834058cff90f881c0ac2139f05dc7b` 和 `claims.md` `c7278022364e16210ac5fbb6d85c4498b0e5a534e3db35ea62736b3d666a64c9`。解析比較只有 `moon035` 提示詞變動，該景 `lines`／`chapter`／`camera`／`visual` 與其餘 scene、全域設定完全相同；`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 位元不變。

工具獨立重算 `visual_hash=5ab1ae1e3c7bcfa1`、`look_hash=98a370ae40badbaf`；正文 119 張 `shot`、9 張 `big`。`lint --json` exit 0、**0 errors／0 warnings／131 句**；只讀 `keyframes --shot moon035 --takes 1 --dry-run` exit 0、MiniMax `image-01` ready、提示詞 577／1070 字元，沒有付費生成。`git diff --check` 通過。

私人 manifest `/workspace/.video-work/curio-s49/keyframes/manifest.json` SHA-256 **`5e660a3839c5a51923dfe4f8b36c3e8e988aaf10919a76d19e07bc3ebac3e77b`** 仍綁 R30 `visual_hash=0ec110a386fb0098`，含 **28／28** 人工 KEEP；逐張所選實檔 SHA 與 manifest 相符，無 `moon035` 退件選圖。`STOP` 在位、jobs 為 `{ "jobs": {} }`；ledger SHA-256 **`a2c44d8e8b053d5a0a0dac91eeb421c720a56f6b335ba968b3fc38e459f4da91`**，累計 **US$1.0935／81 image／81 judge／0 預約**，低於整集 US$5.30。**下一步先在 STOP 下備份並離線重綁 `visual_hash=5ab1ae1e3c7bcfa1`，保留 28 張完整項目和實檔 SHA；重綁成功後才可只試 `moon035` 一張原生圖並逐張看 1280×720 選圖。**本審不放行 `moon036–039` 批次、完整 storyboard、站主網站卡或成片。
