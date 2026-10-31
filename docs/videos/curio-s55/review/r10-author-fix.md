# S55 R10｜十二英尺重述的單句作者修訂

2026-10-20 UTC。R9 已通過[獨立史料與書面畫面覆核](r9-source-independent.md)，但兩位真正無先前對話脈絡的讀者在[正式 OR 合併](r9-clean-merge.md)均判 `no_recap` 否，指出 `s55018` 和 `s55038` 各說一次查爾斯氣球的「十二英尺」。本檔是 **R10 作者候選**，不是新一輪來源、敘事或語音核准。

## 五檔凍結雜湊

| 檔案 | R10 SHA-256 |
| --- | --- |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `claims.md` | `9e65b7a2aeb55a749ba20397a589d840ae0b6b0cbda196026daf55f76781522c` |
| `video.json` | `cc86ecf2165f658417d81235d432cc00429e0f6cc853e3011d8b74d15177d6ed` |
| `script.md` | `5e231cb244bf28075f64df92d64d5a529d9b6d5e954fd093cdf42f13c80799f9` |

## 精確改動與原文界線

只改 `s55038` 口播，從「那顆新球直徑約三十八英尺，比查爾斯那顆十二英尺的小球大得多」改為「那顆新球直徑約三十八英尺，比先前查爾斯放飛的無人小球大出許多」。`s55018` 的第一次十二英尺仍在；後段保留新的三十八英尺尺寸、兩種球的大小對比，以及「先前查爾斯」的明示回呼，但不再重唸十二英尺。書面畫面原本就是一大一小兩個無可讀測量字樣的示意球，無須改提示詞。

同一文字同步在 `video.json` 一句與 `claims.md` 一列；主張列另補 [富蘭克林記查爾斯小球直徑及無人升空的原文 F 122–151](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L122-L151)，並保留 [準備中的孟格菲大球 F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179)。原文分別是十二與三十八英尺，尺寸比較由兩個原文數字得出。沒有把準備中的球說成已經載人飛行。

在現版 `video.json` 將新句逆換為 R9 舊句，所得 SHA-256 恰為 R9 `525ba099fc70de1c03d49327ac854348b001808d3c8580ad558ee487d8ccf669`；在 `claims.md` 同時逆換一句及補入的來源連結，所得 SHA-256 恰為 R9 `f069c516d79c16ef7091d1f4cda72927cbc3da583625f8d9b096c7a9ca64dff0`。除這一景口播／來源欄外沒有其他手改；`script.md` 由 CLI 重生。

## 作者機械檢查與後續

`VIDEO_WORKDIR=/tmp/curio-s55-r10-author NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s55 --json`：**0 errors／0 warnings**、140 句含片尾。正文仍有 138 句與 `claims.md` 的 138 列同文同序；濃縮開場 175 漢字，後續正文 2,626 漢字，以每分鐘 325 漢字的最快估算法為 **8.08 分鐘**。這是文字下界，尚未合成或實測語音。

下一關須另找未參與修稿者，以這版五檔 SHA 獨立覆核單句史料／畫面差分，再請兩位 `fork_turns:none` 的無背景讀者各自盲評 R10 官方 13 題，正式 OR 合併通過後才可進 TTS。R9 的讀者答卷及來源 PASS 都不直接充當 R10 核准。未做付費旁白、插圖、配樂或成片。
