# S56 R12｜獨立史料與書面畫面覆核

2026-10-20 UTC。**此精確 R12 五檔版本的史料、逐句主張、引註與書面畫面 PASS。** 我未參與 R12 修稿；以固定版原文核對兩句新口播，逐句核對主張表與分鏡／劇本，並以 R11 精確雜湊確認其餘場景未變。本票只涵蓋文字和未生成的畫面提示詞；不是新讀者敘事、政策、R12 音訊、實際插圖或成片的判票。R11 音檢剩下的兩個旗標不能沿用或清空。沒有修改作者五檔，也沒有呼叫付費媒體。

## 凍結輸入

| 檔案 | 重算 SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `ca09512c0398c94578f2acaa748cdc13c4b5ebff79ac80b6107ca600d65f6b11` |
| `video.json` | `f54a4c830fb876e949f4f4910d025cb8f68331e40d27dc87ab9edf26f05bd479` |
| `script.md` | `65ae866c1761da1c83d0941a92569c7b85ec0fddda0de17adc157bbc8d046f4f` |

五值均等於 [R12 作者交接](r12-author-oral-repair.md)；審查結尾重算仍相同。`brief.md`、`research.md` 亦與 [R11 獨立審查](r11-source-independent.md) 的凍結值相同。

## 固定來源與兩句裁決

我重開 `/tmp/s56-chicago-foster/66472-0.txt` 與 `/tmp/s56-chicago-loesch/66433-0.txt`：前者 checkout 為 `60c777551301c30942acf749d4bb37ca32752353`，`HEAD:66472-0.txt` Git blob `565a1a465fb84a2c9035ea82d312ae80b70b52e8`，全文 SHA-256 `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee`；後者 checkout 為 `08931a6f2629fd4b8be37b1ec548857d48d17eb9`，`HEAD:66433-0.txt` Git blob `3370a705ac376a115010a8480e3874ab10a6cb5b`，全文 SHA-256 `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`。兩份工作樹乾淨，與 [research.md](../research.md) 的釘選相符。F 是 1871-10-31 家書的 **1923 年家族抄本印刷版**，編者在 [F161–171](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L161-L171) 說原信下落不明；L 是 **1925 年**晚年回憶。電子行號不是原版頁碼，私人見聞也不是官方火因調查。

| ID | R12 口播及逐句主張 | 固定原文、來源邊界與書面畫面 |
| --- | --- | --- |
| `s56096` | 「福斯特仍不放心，回旅館打包行李。」 | [F376–414](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L376-L414)，特別是 F379–386：他自認磚石區不會被火穿透，卻寫「still to make my mind easy, I went to the Brigg’s House, and commenced packing」。F223–229、F268 亦稱 Brigg’s House 為自己住的旅館。故「仍不放心／回旅館／打包」有直接依據；`claims.md` 的 L245–269 是石造市政廳補充，**不**作福斯特收箱的證據。同景 `s56095` 的石牆提示詞承接磚石區判斷，後景 `s56097` 的旅館窗口、`s56099` 的大箱子接續收箱；提示詞沒有可讀家書、現代設備或與原文相反的已裝箱時序。**PASS。** |
| `s56174` | 「西岸大火隨後越河，跟東岸那片火勢連在一起。」 | [F349–383](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L349-L383)，特別是 F357–370：他從 West Side 過河到 South Side，先見自己這岸約四百碼外有新火，消防車被分走，接著寫原火「it soon jumped the river too, and joined the new one」。前句 `s56173` 已交代另起的火；「那片火勢」有明確指向。原文沒有他逐格目擊某一塊火屑走完整個河面，稿子也未如此聲稱。`s56173` 提示詞畫東岸木屋另起火，`s56174` 只畫兩岸火勢與橋，沒有畫火焰穿水或精確飛火軌跡。**PASS。** |

## R11 差分與全稿對齊

把 R12 `video.json` 中上述 **兩處口播文字各還原一次**，所得 SHA-256 精確等於 R11 凍結的 `297b576499068e12fb937bc6032394cf9408f8543065b762a95c6b26ef89cd72`。對 `script.md` 還原同兩句及尾端由口播重算的 `narrative`／`speech` 雜湊，所得 SHA-256 精確等於 R11 的 `38ef6dfdbb71bd0b59a441a4d41fc4a89b2b3aed288899a28ec902193b792d2c`。故 R12 沒有別的 JSON 場景、prompt、章節、卡片、伏筆或書面劇本內容改動；R11 書面畫面獨立 PASS 的其餘部分仍適用。

我另逐列解析現稿：`video.json` 有 **121 景（118 `shot`、3 `big`）**、**154 個唯一旁白 ID**、**18** 個 loops；`claims.md` 有 **154** 列，與 JSON 逐 ID、逐字、逐序一致；`script.md` 的 **154** 句亦與 JSON 逐字逐序一致。以 R10 作者保留的逐句表原樣副本交叉檢查，R10→R12 只見 `s56079`、`s56112`（R11 已審的改句）及本次兩句口播四列不同；**154 列的引文欄與畫面界線欄全無變動**。`claims.md` 的 R12 導言更新屬版本說明。全部 **234** 個逐句來源連結（**30** 種固定行段）都指向 F 或 L 上述固定 commit，行段無倒置、越界或錯提交。逐景讀取 prompt 和相鄰旁白後，本次變更所及兩景沒有新的書面矛盾；對未生成畫面仍僅裁文字。

`node tools/video/cli.mjs lint --slug curio-s56 --json`：**0 errors、0 warnings**；154 句、2,604 估算口播單位、約 12.65 分鐘的文字估計。`npm run test:docs-videos`：**236/236 通過**。`npm run check:tasks`：退出碼 0，驗證 2,283 張任務票；輸出含既有其他票的過期／重疊警告，未影響本票。這些檢查不構成 R12 真實語音時長或音檢。對新報告與新任務票各跑 `git diff --no-index --check /dev/null <file>`，無空白錯誤診斷；退出碼 1 僅代表檔案有新增內容。

**結論：R12 這五個 SHA 的來源與書面畫面 PASS。** 後續須對 **R12** 另做兩位無前情讀者的正式盲評合併、政策與全新 154／154 句音檢；R11 已合成音訊及仍留兩旗標的 HOLD 不轉作新版 PASS。本審查沒有核准付費語音、插圖、配樂、成片或發布。
