# S49 R42｜`moon041` 蠟燭桌面概念圖非作者紙審

2026-10-22 UTC。**固定來源與書面畫面 PAPER PASS，只限本次凍結的 `moon041` 提示／claims 畫面欄。**我是非作者；沒有改作者文稿、私人 manifest、帳本、任務或 PR，也沒有付費影像／judge 呼叫。本結論只允許後續受守衛的單張原圖測試，不預判模型能畫對蠟燭、成人或固定系列畫風，也不核准全章 storyboard／成片。

## 來源與畫面判斷

我重讀 Locke 名下 1859 年重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 的 [P05 L420–443](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L420-L443)：人工光如何照亮焦像是**1835 年虛構報導中的對話**。Jacoby 1902 評論 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` 的 [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 稱這段為荒謬的想像光學對話，沒有證實器材。旁白原句「問題是，照亮桌上的影像，不會替月亮送回更多細節」是讀者的概念性質疑，不是可由桌上照明增強實際月球資訊的實驗結論。

我完整查看 [R41 首張退件](r41-moon041-first-native-stop.md)封存的 1280×720 原圖 SHA `b75188f16ad55c8d5144b4ad9b7964d292412c2be59e9f8bd5acad8304cda147`：巨大的有線現代聚光燈、白色大圓盤和半寫實 3D 偶戲畫風，確實超出年代與固定 `cute-mystery` 畫風；裁圖只能去掉黑邊。R42 新提示把光源**正面限定成一支短蠟燭、外露火焰、樸素黃銅座**，小光暈只在木桌上的**小型無細節圓斑**附近；成年灰鬢讀者只指桌面，窗外月亮仍暗，普通粉牆且不畫光學器材或可讀字。這保留單人單一動作，避免把前圖的電燈、劇場光束或假赫歇爾器材寫回畫面，也把大白盤縮成小型概念斑。

**蠟燭與黃銅座是想像插畫的年代照明選擇，並非 Locke 或 Jacoby 證實的實驗裝置。**claims 同列仍明說「虛構報導的桌上影像與遠月對照示意」、「燭光只照桌面」以及不畫真實赫歇爾器材或現存實驗；來源和旁白均未變。沒有把抽象的桌面圓斑稱作留存焦像圖。若實際原圖再畫現代燈、光束通往月球、過大圓盤、3D／照片質感或假文獻版面，仍應 HUMAN REJECT 並停止下一景；紙審本身不能代替原尺寸視覺驗收。

## 可逆性與守衛

- 凍結 `video.json` SHA-256 **`07ca48195b04696375564fdde0295ecf35532e75c2b09db09b61a19ba0038f75`**、`claims.md` **`5aa04589f6ad859c9178247003c2c56caeaf40dc03fab003c5e15f73b4020953`**、[R42 逐字可逆結構差分](r42-moon041-candle-tabletop-structured-diff.json) SHA-256 **`2e41f25dd49ed25a596a5d418d01405b497c232be50f9e153f88c9ea708d815e`**。我獨立用差分原始位元組 `after→before` 各替換一次，精確還原 Git `b554efe53` 的 R41 video SHA `36d9ddcc442a686f6f88ddadd10e9f8dfc37d58400a07b716979993d0f379461`、claims SHA `fc4b77a6fe7929903d7492eb4afef0c1f0c566ea6116739934e7e927f8787b80`。129 景只 `scenes[37].data.prompt` 改，其他 **128 景完整物件**、`moon041` camera／visual、全部 **131 句台詞**不變；claims 只 `moon041` 一行畫面欄改，旁白與 P05／J 來源欄不變。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 不變。
- 我獨立跑 `node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0：**0 errors／0 warnings／131 lines**；`keyframes --shot moon041 --takes 1 --dry-run` exit 0、提示 **489／1070** 字元、MiniMax `image-01` ready。只讀 dry-run 沒有影像或費用；工具所列通用 US$200 cap 不取代本集 **US$5.30** 上限。重算 `visual_hash=d43f3c8a95c29e22`、`look_hash=98a370ae40badbaf`。正文 **117／128 shot＝91.40625%**，最長連續字卡 **2**。
- 私人 active manifest `/workspace/.video-work/curio-s49/keyframes/manifest.json` SHA-256 **`a28a741c18e0760a2545c3b224f1f5e8c75943dd281a5108063a9c36cd1c8c2d`** 仍綁 R41 `visual_hash=540e3ad9a6188297`，不能直接畫 R42；32／32 張 selected KEEP 實檔 SHA 均相符，沒有 `moon041` 入選。ledger SHA-256 **`3d7a25ca6c2f15ba2dafeaafe6eeb03268d805aaecb3a0f270f76f58eabec92a`**：**US$1.2420／92 image／92 judge／0 預約**，距本集上限餘 US$4.0580。`STOP` 在位，jobs 空；本輪零新增媒體費用。

**結論：R42 `moon041` 書面候選 PAPER PASS。**下一步須在 STOP 下核精確凍結文稿／本紙審 SHA、32 KEEP 入選實檔、ledger、jobs，僅離線重綁新 `visual_hash`；再重新查即時 MiniMax 額度、每張價格與 US$5.30 整集上限，才可買**至多一張**第二次 `moon041` 原圖＋judge。原圖與裁圖都要完整 1280×720 人工驗收；退件即恢復 32 KEEP／STOP，`moon042` 不跟著購圖。
