# S61 R8｜獨立史料與書面畫面覆核

2026-10-22 UTC。**固定史料與書面畫面 PASS。** R7 唯一 HOLD 的 `s61031` 過強地理範圍已修正；此結論只對下列 R8 凍結雜湊有效。我不是 R8 作者，沒有修改作者稿、主張、畫面或來源，也沒有做盲讀或呼叫 TTS、圖片、音樂、評審及其他媒體。PASS 不等於原生圖、語音、成片或站主核准。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `ef67f56b4d384015edc9eeaea3640946ff0c4c9b778a2a587adb190c43004a65` |
| `research.md` | `4ccf2c0aae5aa5f3bb27ee56641f6092aa79bc6d2165d6cbfdecbb582a48ddba` |
| `video.json` | `47860fcf1347bc549dcabeb2630f5a9e63bbbcd7a40c629ceafb16570f96ccb5` |
| `script.md` | `00f9734108f68b0093a3c7791fe4b0974a376cb963cbc772c1ed92cc61c11b04` |
| `claims.md` | `1e632d8f0884ca20829b49cc443610633fca028c20cc521232f6dffb86ccc4d8` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `290b00655a4c8ffbef5f9be91e8ab33df4c1bb061d3eb1c2495f188be87e708e` |
| `r8-author-delta.json` | `2fa82207d665d87c86f4e27f895c7f58ceb1be381edbf73a826ba1719e8cebef` |

固定原文仍是 Samuel Henry Prince，*Catastrophe and Social Change*（1920），GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`；本機 raw `/tmp/s61-halifax-prince.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。Prince [L1963–1968](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1963-L1968) 說消防員「largely remained organized, and responded to the general alarm soon after the explosion」；接著另說第二次爆炸警報傳開時，他們仍留守。R8 的 `s61031` 及 `research.md` P09 只說「首爆後很快回應警報，隊伍一時還保有組織」，不再聲稱警報遍及全城，也保留兩道警報的區別。這直接解決 [R7 獨立覆核](r7-independent-source-visual.md) 的唯一 HOLD。

逐檔比對 R7 與 R8：`video.json` 只有 `s61031` 一句的「全城」刪除；`claims.md` 同句與 `research.md` P09 同步，`script.md` 同句及生成的 narrative／speech 短雜湊同步，任務票改現況並記審核，`brief.md` 未改。全部 scene 順序、96 個 `shot` 提示詞、7 張 `big` 卡內容、章節和 20 組 `loops` 都與 R7 逐位元相同。R7 [獨立覆核](r7-independent-source-visual.md) 已逐項核對其餘改文與固定原文，96 幅及 7 卡紙審 PASS；本輪重新核對修訂句、相鄰的消防指揮與第二次警報語境，以及全部當前來源與畫面映射，未發現其他新問題。

機械核對：103／103 非片尾台詞各有且只有一列 `claims.md`，旁白逐字對上 `video.json` 和 `script.md`；每列有來源，127 個錨點皆指固定 commit 且行號在 6,215 行 raw 範圍內。96／96 插圖提示與 7／7 卡片文字和主張列一致，最多連續一張卡；另有 3 句品牌片尾，不作史實主張。所有畫面仍標為原創示意，未要求可讀原始命令、官方地圖、新聞或血腥重建。這是**書面畫面 PASS**，生成原圖仍須另驗。

獨立重放 `r8-author-delta.json`：用 `/tmp/s61-r7-frozen/` 六檔比對每塊舊／新行與零起算座標，正向得到 R8 雜湊、逆向逐位元還原 R7。`brief.md`、`research.md`、`video.json`、`script.md`、`claims.md`、任務票分別 **0／1／1／2／1／1 塊，全 PASS**。此差分檢查不代替史料判斷。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` exit 0，**0 errors／0 warnings**；106 句、六章。獨立用 `estimateTimeline(doc, 325)` 得濃縮開場 **48.23 秒**、開場後至品牌片尾前正文 **486.20 秒（8:06.20）**；250 CPM 時分別 59.53 秒與 603.53 秒。正文在較快估速下仍超過八分鐘。這些是合成前估算，未量實際 TTS。
