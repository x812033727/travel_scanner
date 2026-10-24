# S49 R8｜敘事三處窄修與作者凍結

2026-10-20 UTC。這是**作者修稿與機械自查**，不算 R8 獨立來源／書面畫面覆核，也不算全新雙盲敘事 PASS。[R7 獨立來源覆核](review/r7-source-independent.md)對 R7 精確雜湊為 PASS；[R7 A](review/r7-fresh-panel-a.md) 12/13、[B](review/r7-fresh-panel-b.md) 11/13，兩人共同在必答 `no_recap` 判 No，B 另在 `no_toc` 判 No。[正式合併](review/r7-official-panel-merged.json)因此是 **FAIL**。R7 核對票不移作 R8 核准。

R8 保留 `brief.md`、`research.md`、全部 133 個編號景、136 句、11 組 `loops`、七張字卡及其文字。只改 `moon005/013/122` 三句，讓 `moon048` 的月面小物聲稱只在正文首次完整提出；`moon122` 的一張書面提示詞隨台詞更換；三句的 `claims.md` 同步，並由 CLI 重生 `script.md`。其餘場景與提示詞不動。

| R7 盲讀發現 | R8 作者改動及固定錨點 |
| --- | --- |
| A：開場 `moon005` 已說可看清月面細小東西，`moon048` 又說一次 | `moon005` 現只問虛構報導的望遠鏡光線難題；`moon034–041` 逐步提出並解釋光學問題，`moon048` 才第一次給四萬兩千倍與細小物件聲稱。仍把數字限定為**報導聲稱**，錨定 [P05：L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)與 [J 光學評論](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。`moon005` 的望遠鏡草圖提示詞可沿用。 |
| B：`moon013` 的「真實工作說到這裡」像宣告段落切換 | `moon013` 改成《太陽報》把赫歇爾的觀測目標從南天星空寫成月球，接 `moon012` 的真實工作與 `moon014` 的標題署名；沒有旁白自述章節。這是**假報導的寫法**，不聲稱真赫歇爾改了研究方向。[P06：J4050–4080](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4050-L4080)區分真旅程與捏造發現，[P03：L168–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L168-L254)是重印本虛構開篇；原讀者比較無字星圖和報紙的示意提示詞仍合用。 |
| B：`moon122` 重列 `moon113/115/119` 的稱讚、質疑與反諷 | `moon122` 直接回答 `moon121` 的「能算相信票嗎」：把這則反話算成支持會誤讀重印本選錄；不再概括三類反應。錨定 [P13：L2055–2193](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2055-L2193)與 [J 反應分析](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4177-L4215)。畫面由三張剪報改成一位史料讀者把**無字紙片示意**從重印本旁移開，沒有冒充原報剪報或真的插在書裡。 |

| R8 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md`（未改） | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md`（未改） | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `a010434fbbb2e498f6d064557b58e11cea338ccf93fc6300ab5960444f9e25e1` |
| `script.md`（CLI 重生） | `f40259db7e16da37652689f0e2d703b8e03b8364d1738d0b4c2f848043618c8b` |
| `video.json` | `1eaec3a24e656fe86e0cc5f48e5d61fa3a690b18aa7f4621960aa85f14f60baa` |

`script --slug curio-s49` 的 narrative 短碼是 `14e10ff9b09866b8`。`lint --slug curio-s49 --json` 為 **0 errors／0 warnings、136 lines**。CLI 劇本與 JSON 136/136 台詞逐字同序；claims 的 133/133 景 ID 與台詞、126/126 shot 提示詞、7/7 big 卡片三欄均同序一致，台詞 ID 唯一，11 組 loop ID 均存在。開場前八景 **176 spoken units＝32.49 秒**；正文 **2,693 units＝497.17 秒（8:17.17）**，以偏快的 325 units／分鐘保守估時，**尚非 TTS 實長**。`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` 驗證 2,123 票成功，倉庫其他票的既有 stale／scope overlap 警告不影響成功；`git diff --check -- docs/videos/curio-s49` 通過。

下一關由未參與 R8 修稿者重讀固定 L／J、三句及 `moon122` 書面提示詞並核對上述精確 SHA；另由**兩名全新、彼此隔離、只讀 R8 `script.md` 和固定十三題**的讀者重新盲評。R8 未取得這些獨立裁決，也未做新政策檢查、站台劇本卡、TTS、付費圖、配樂或成片。
