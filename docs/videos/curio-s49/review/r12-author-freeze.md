# S49 R12｜敘事盲讀失分的作者修稿與精確凍結

2026-10-20 UTC。[R11 官方雙盲](r11-official-panel.md)兩名新讀者一致判 `payoffs`、`no_recap` **FAIL（11/13）**。本版只修他們指出的問題；作者自檢不算獨立來源或敘事通過。

| 問題 | R12 處理 |
| --- | --- |
| `moon006→118` 問第二份獨立觀測，原回收只限單一選錄段落 | 開場明說核對範圍是重印本與後出的 Jacoby 評論；`moon118` 回扣同一範圍，說這兩份文字沒有交出第二份獨立月面觀測。`claims.md` 同列 L 選錄及 J「引句取自重印本」錨點。不推論所有館藏都沒有獨立證物。 |
| `moon104→106` 問何時持續觀測，卻只答「當月不行」 | 重讀 L [1619–1626](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1619-L1626)：**虛構報導後段**說直到三月新月天氣才適合持續月面觀測。`moon104` 明問「持續」而非「下一次」，因原文 L1626 還提到中間少數晴夜的觀測。`moon106` 直接給出三月，`moon107–108` 回到等待期間先談土星的文章順序。`research.md` P12 和企劃章表同步明示這只是紙上時間線。沒有說真實天文台在三月拍到月球居民。 |
| `moon010/011` 南天目的重說 | `moon011` 改為 Jacoby 記載的 1833 年 11 月出航及與 1835 報導相隔將近兩年；鏡頭改為一人在碼頭持無字儀器箱登船。`moon012` 只保留實際雙星／星雲成果，接 `moon013` 的月球假目標。 |
| `moon019/112` 1859 重印書再介紹 | `moon112` 改成翻開先前那本書的後段，讓同年背景成為明確回呼，章首也接上 `moon111` 的編輯反應問題。 |
| `moon119–122` 連續重判反諷 | 先讓《晚郵報》引文把有翼人與 Peter Wilkins 的遊記並列，再指出「最可信的旅行家」的語氣，問 Jacoby 怎樣讀，最後才用他「沒有受騙」的評論判這不是支持票。L [2100–2114](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2100-L2114)、J [4177–4215](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4177-L4215) 已列在逐句主張表。 |

改動旁白行 ID：`moon006`, `moon011`, `moon012`, `moon104`, `moon106`, `moon107`, `moon108`, `moon112`, `moon118`, `moon119`, `moon120`, `moon121`, `moon122`。`moon011` 提示詞一景改動；其餘提示詞、字卡、loop 端點、頻道及來源連結、配樂、片頭片尾規格沿用。所有變動行在 `claims.md` 同步並保留直接錨點。固定 L、J 全文 SHA 仍分別是 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 與 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。

| R12 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9` |
| `research.md` | `c3b9fff8a4656536438137fb1b9e2403bc84f50dd9a36dbb797f85204f99649e` |
| `claims.md` | `e87359c6f7e53f6567fb82697cebbdf39e171dda423483b8ace117a5c9561658` |
| `script.md` | `ab8e840e2c74b283b60e65e62d62e41d79d6eea0ded323e4888a3940de80ab7e` |
| `video.json` | `bfff58fdda9eb5501fb46d5211222cb135dff30a4c0a25223e7a10884d6a4c06` |

`script --slug curio-s49` 重生逐字稿，narrative 短碼 `a67a707c4db0fd6b`、speech 短碼 `395bf279bc159bb1`。130/130 編號景與 claims 同 ID、同序、同文；133/133 `script.md` 旁白與 JSON 同序同字；124 shot、6 big、11 loop 全端點存在。`lint --slug curio-s49 --json` 為 **0 errors／0 warnings**；工具預估全片 13.87 分鐘，第一章結束 00:50。`npm run test:docs-videos` **236/236**、`npm run check:tasks` **2124 票驗證成功**，`git diff --check` 通過。正文仍待新版 TTS 實測至少八分鐘及逐句零旗標。

**R12 待辦：**另一位工作者按這五檔 SHA 重讀固定來源和書面畫面；兩位全新、只讀 R12 `narration` 的讀者各答正式 13 題，合併並保存 CLI 回條。R11 的獨立來源 PASS 與敘事 FAIL 均不移轉到此版；舊音檔也不是 R12 新稿。本輪未做新 TTS、插圖、配樂或成片。
