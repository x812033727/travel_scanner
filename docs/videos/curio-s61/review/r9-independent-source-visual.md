# S61 R9｜獨立史料與書面畫面覆核

2026-10-22 UTC。**固定史料與書面畫面 PASS。** 此結論只對下列 R9 凍結檔案有效，不是敘事雙盲、原生圖、旁白、成片或站主核准。我不是 R9 作者，沒有改作者文字、主張或畫面，也沒有呼叫付費媒體。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `75205d400dc05994097133ee45800161f816949e8d5658048909a2b8191a91f6` |
| `research.md` | `8fc6c82f22c352e5e4d336b2704eda9a9419dccf2896dbd970c5d16ffcaefdcf` |
| `video.json` | `005cc35734535c8a01ee46f7ee5dc1a3555d3b543d0fc3b42c0beda2812d97ce` |
| `script.md` | `e3f27c9da2b951fd744e9de48b2c64d665ef4f76cd6abaa4e323b43c5ebb9eb9` |
| `claims.md` | `37eb7bf2a039692d583e15b1e2e2aab477096ba47ee526fe8876a26e995df11c` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `72c65406eb82552b0f4ec3bd7fadec7fc12fb12e6cbe7a4bb140cad5203626e9` |
| `r9-author-delta.json` | `d8de5784ea82872d1ac128a7f0400c7520c099eb7a42893d4bb94a83a05495e9` |

固定原文仍是 Samuel Henry Prince，*Catastrophe and Social Change*（1920），GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`；本機 `/tmp/s61-halifax-prince.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。以下行號屬固定轉錄檔，不是原版頁碼。

## R8→R9 的兩個事實與畫面

- `s61123` 現說「北面的天空已被火光染紅，大片街區像一座還在轟鳴的火爐」。Prince [L924–930](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L924-L930) 寫北面「a roaring furnace」，上方天空「crimson」，且有多處建物起火。這是有明確歸屬的原文意象，沒有新增火距、個案或傷亡數。既有 wide shot 的北區多處遠火、紅色煙光天空及匿名遠望者與新旁白吻合，不畫具體死傷。
- `s61113` 現說老人與病弱者在寒風中更難趕路，接著問**公地上的人**在哪暫避寒風。Prince [L951–960](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L951-L960) 點到老人與病弱者的撤離困難；其轉引的同時代記述 [L1373–1398](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1373-L1398) 說多數人徒步、人們在公地與山坡上挨冷；[L2048–2069](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L2048-L2069) 記軍方在公地搭白帳，教堂大廳也被整理作收容。`s61081` 白帳、`s61149` 教堂大廳提供來源支持的處所；新問句沒有聲稱特定老人或病弱者實際進了哪頂帳棚。既有匿名年長者獲成人攙扶、朝公地走的提示詞對上前半句，不冒充可指認個案。

R9 `video.json` 只有上述兩句旁白改動；`brief.md` 的階段與計時、`research.md` 的階段、`claims.md` 的對應兩列及 `script.md` 的對應兩句／生成雜湊同步更新。R8 [獨立覆核](r8-independent-source-visual.md) 已在相同固定原文下 PASS 其餘 101 句與書面畫面；我再核對 R9 全套對應，沒有發現新的史料或書面畫面矛盾。Prince 對火藥庫灌水和第二次未爆炸的說法仍被片中標為他的 1920 年研究歸因，沒有冒充另核軍方卷宗。

機械核對：103／103 非片尾台詞各有且只有一列 `claims.md`，旁白逐字對上 `video.json` 與 `script.md`；每列有來源，127 個連結均指固定 commit 且行號在 6,215 行 raw 範圍內。96／96 `shot` 提示詞及 7／7 `big` 卡文字和主張列一致；scene 順序、96 個提示詞、7 卡內容、六章及 20 組 `loops` 與 R8 相同，最多連續一張卡。3 句品牌片尾不作史實主張。畫面仍標為原創示意，不要求可讀原始命令、官方地圖、新聞或血腥重建。**書面畫面 PASS**；生成原圖仍須按系列規則另驗。

獨立重放 `r9-author-delta.json`：以 `/tmp/s61-r8-pr-frozen/` 六檔比對每塊舊／新行與零起算座標，正向得到 R9 雜湊、逆向逐位元還原 R8。`brief.md`、`research.md`、`video.json`、`script.md`、`claims.md`、任務票分別 **2／1／2／3／3／4 塊，全 PASS**。差分可逆性不替代上面的史料判斷。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` exit 0，**0 errors／0 warnings**，106 句（含 3 句品牌片尾）、六章。獨立用 `estimateTimeline(doc, 325)` 得濃縮開場 **48.23 秒**、開場後至品牌片尾前正文 **487.13 秒（8:07.13）**；250 CPM 時分別 59.53 秒與 604.73 秒。這是合成前估時，沒有實際 TTS 可量。R9 敘事雙盲仍須對這組新雜湊獨立進行；本紙審 PASS 不移轉 R8 敘事票。
