# X05 Meta｜v16 九景提示詞套用與媒體橋接作者收據

**獨立套用後差異審查 PASS；零付費呼叫，主工作區 `STOP` 保留。** 2026-10-20。先前[離線九景候選](prompt-proposal-after-v15-batch.md) SHA-256 `dd964048b45e7a8341c421b11ccc497a50d23d0afb7507a6b75f2a1bfe383fb7` 有[獨立語義 PASS](visual-v16-proposal-independent.md)，實際套用及橋接另有[獨立覆核 PASS](visual-v16-postapply-independent.md)；這些尚不表示新圖合格。

基準 v15 `video.json` SHA-256 `077a5a6b541cb9e5a181786b8ed2d3d00816263dc68a71db625a1a0c0520b12a`；套用後 v16 SHA-256 **`a412c6b2e9a78f8eda90238336d7ccb87521dff8f87d8ae31842b508bce0b40d`**。`drafts/lines.tsv` 新 SHA-256 `4ea1b301dd03216e271fe52f2df8a964e20c5ed1f1efbe5dcfcd23955a1197bc`，Shorts 不變 SHA-256 `52e2812e2bbf409b3edab3e935dcf65f3768e79b0e9c0522a898e0b9d024dfd2`；新全片 `visual_hash` `a933997a39265cd9`。

只改下列九個 `shot.data.prompt`，對應 TSV 各一筆 `visual` 欄：

| 鏡頭 | TSV 句 ID | 理由 |
| --- | --- | --- |
| `x05-b02-s06` | `m050206` | 封住兩分部與合計，取代秤盤浮頭。 |
| `x05-b03-s12` | `m050310` | 三組成本改為物件抽屜，結果仍封閉。 |
| `x05-b04-s03` | `m050402` | 保持收入問句的容器全遮蓋。 |
| `x05-b01-s06` | `m050106` | 兩裝置／分岔路徑及被遮住的結果同框。 |
| `x05-b02-s03` | `m050203` | 更名動作與兩報表抽屜隔開，不添文字。 |
| `x05-b02-s04` | `m050204` | 用無字手機背面示意 FoA 服務歸欄。 |
| `x05-b03-s08` | `m050308` | 已公告與年末名冊同框，費用箱仍關閉。 |
| `x05-b04-s05` | `m050403` | 只在揭曉後呈現收入銅幣總堆上升。 |
| `x05-b04-s06` | `m050418` | 三封公告信代表計畫，年末人數仍藏住。 |

程式按鎖定候選逐字抽取九項，先比對 v15 基準雜湊，再各將 `video.json` 的舊 prompt 和 TSV 的舊 `visual` 各替換一次。將新 JSON 的這九欄還原為 v15 後，整份物件深度相等；TSV 的章、句 ID、旁白、來源欄逐列相等，場景與卡片順序、`cute-mystery` look、語音、來源數值、Shorts 均未變。`compose-video.mjs` 仍有既有 CARD-row assert 問題，本次沒有聲稱從 TSV 全量重生。

已付費 v15 33 景 manifest 先封存於 repo 外 `review/local-preview/v15-art-batch-archive-2026-10-20`，舊檔 SHA-256 `f4092657d38f3394989a2c09977bd7e80d9104d61d5fe26011893cd3e9d28130`；影像、失敗評審及舊 HOLD 都保留。新主 manifest 只橋接 24 景**提示詞未變且已評審 PASS、人工暫可用**的選圖；每張引用影像逐一核 SHA，九景舊選圖／失敗圖不帶到 v16 可用集合。新 manifest 的 `visual_hash` 是 `a933997a39265cd9`、檔案 SHA-256 `6472a5881826813a139f98f4a6b3ad5c89a6381d161a79bc9211f1639258b02f`。ledger 與 cache 位元組未改，帳本仍 **US$0.9485、71 圖／70 評審、預留 0**；那張已付費但尚未評審的 `x05-b04-s06` 第二 take 原檔仍在。主 `STOP` 保留。九景仍是未驗收畫面，另有 31 景未試，不能製成成片或宣稱 64 景完成。

獨立審查已核：九個新提示詞與離線候選完全一致，剝除九欄後 v16/v15 JSON 深比相等；Shorts SHA 未變；24 景橋接的 prompt、模型、look、檔案 SHA 及 judge PASS 照舊，九景舊圖未混入；ledger/cache/STOP 未被改動。配對工具的九景 `keyframes --dry-run --takes 3` 顯示九句皆低於 MiniMax 提示詞上限（384–491／1,070–1,074 字），當時一輪報價約 US$0.12、三輪上限約 US$0.36；這是未付款估價。共享額度與整支 US$25 最壞預留允許時才可做付費小試。

驗證：影片 lint **0 errors／3 warnings**（v16 多一項 `smooth` 在 64 景中出現 23 次的視覺重複提醒，另兩項既有年份提醒）；`npm run test:docs-videos` **248/248 PASS**；`npm run check:tasks` 驗證 2,077 份任務文件、exit 0（既有跨任務提醒）；`git diff --check` PASS。重複詞提醒不等於圖像合格，待後續逐景出圖時按實際畫面重看多樣性；本次不改已獨立鎖定的九項字句。
