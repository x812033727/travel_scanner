# S49 R34｜`moon036` 成年讀者與小 V 角獨立書面覆核

2026-10-22 UTC。審者為 `/root/s53_r22_author`，未撰寫 S49 R34 修稿、未操作 S49 付費圖。**PASS，僅限精確 R34 來源與書面畫面候選。**本輪只讀來源、R33 原圖、兩版稿件和 S49 私有狀態，沒有修改影片、圖單、語音或付費媒體；書面 PASS 不等於下一張原生圖 KEEP，也不放行 storyboard 或成片。

## 固定來源及概念畫界線

我重開固定 1859 年《The Moon Hoax》重印本 `/tmp/s49-moon-hoax-62779.txt`，SHA-256 **`3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`**。[P05 L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520) 中虛構的 Brewster 在對話裡確實 *hesitatingly referred to the refrangibility of rays, and the angle of incidence*（本機 L417–422）；`moon036` 口播「布魯斯特在文中遲疑，先提折射和入射角該怎麼辦」是歸屬於**文中**的概述。另重開固定 Jacoby《Practical Talks by an Astronomer》`/tmp/s49-jacoby-53396.txt`，SHA-256 **`f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`**；[J L4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)引述同一虛構對話，明說這是沒有可理解科學意義的光學術語拼貼。來源不支持真實實驗、存世角度圖或 Brewster 實際畫過 V 角。

R34 畫面改成**一名**中年、灰髮鬢角、額有紋的匿名讀者，在明標 *plainly imagined* 的 1830 年代英國書房，以羽毛筆筆尖接觸小紙上的一個簡單無字 V 角。這個紙上 V 僅為折射／入射角話題的**原創概念符號**，不是聲稱報導留下的圖、真實光學實驗或 Herschel 器材；`claims.md` 亦逐字標明虛構討論、非真實月面或器材。口播沒有要求同框兩人，因此拿掉 R33 童貌聽者不改述事實。我直接看 R33 未裁 1280×720 `moon036-1.jpg`，SHA-256 **`aaf3051acddcb5557185537611304d5bf7aff9877eca28a26fa09f9be071dd7e`**：左側童貌、右側筆離紙、紙上長交叉曲線。R34 的一人成年、年代外套、筆尖貼紙與小 V 角文字逐項針對這些失配；實際生成能否做到仍須下一張原圖判斷。

## 版次、可逆差分與停線

從 R33 Git `4fed9510e` 讀取 `video.json`、`claims.md` 原始位元組，再核 [R34 結構差分](r34-moon036-adult-angle-structured-diff.json) SHA-256 **`aeb2e1eb533e4344d04d0b4b16741f04ce09797bbcca1f39a448621f23dcb42c`**。`scenes[32].data.prompt` 和 `claims.md` 的 `moon036` 完整行各是唯一替換；把 `after` 反填 `before`，兩檔各逐位元組重現 R33 Git：`video.json` SHA `33c5340f8c84888851fe4e968a7ec316431e8d721e95ef1e2390ff639dce15f5`，`claims.md` SHA `27ac2780c03c2aa7f2fccc041f18dcfbf007187eeec8015402c6532a67c48463`。R34 現檔分別 SHA **`c3c87e4a4a29627f596bb4108320c1f33b3694b6699cc9acd62dfd07b2c7fba4`**、**`2718f55cdf7501a847a1cab51c88a07dfef0b1ed34209206a87a97442ad90313`**。解析比較 129 景：只有 `moon036` 提示詞不同，其餘 128 景完整相同；131 句口播、同景 `camera=push in`／`visual=still` 和全域設定不變。`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 未變。

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json`，exit 0、**0 errors／0 warnings／131 lines**。R34 `visualHash=1c3c268eca8111e4`；私有有效 `keyframes/manifest.json` SHA **`c4e11b2f9080b2d998d813a4cb70b4c99f945eef378658c19f120dcd5af7de86`**，仍綁舊 `5ab1ae1e3c7bcfa1`，只有 29 KEEP、沒有退件 `moon036`；我逐檔重算 29 個所選圖 SHA，全部吻合，且對 29 景的 `keyframeProblems` 為 0。私有 ledger SHA `03726e2755a995b16f809393d44dd8f3c8ab07833b38f3200554d200695dc7c6`，**US$1.1205／83 image／83 judge／0 預約**，低於 US$5.30；jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且空、STOP 在位。

**結論：R34 紙審 PASS。**待操作者先在 STOP 下安全備份並只重綁圖單 `visual_hash`、確認 29 KEEP 完整項目與實檔不變，再做即時 image-01／額度預檢，僅 `moon036` 一張原生圖、一個 judge，直接核未裁原尺寸。新圖若再畫出童貌、年代不合的服裝、筆離紙或長交叉線而非小 V，立即停，不順畫 `moon037–039`。本報告沒有執行這些後續操作。
