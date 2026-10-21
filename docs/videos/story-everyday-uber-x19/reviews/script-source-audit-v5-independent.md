# X19 Uber v5｜獨立 SEC 原件與修稿查核

**稿件事實 PASS；敘事雙盲與正式媒體另驗。** 本票只綁定 `video.json` SHA-256 `c6c442fdf02e65a86be1eaf7115a91a8962a1231a394956e9fca61187110768b`、`shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`、`source-matrix.md` `16a660e71ea51f1a9a288aee8c6598550a0c96f45e271888cf9130a6d8f4ce70`、`drafts/narration.md` `062e791a246b0654ee8a831d2c724f9d3142957721b42a9a1851d00bc2fc1ee9`、`visual-plan.md` `612240b892ff1407cc07c70b0a7ca46cecc7ff53d274fa84955bc851514c372a`。任何受審檔案改動需重查。

2026-10-21 審稿者從來源矩陣列出的 SEC 發行人原件 URL **重新 GET 十份 HTML**，S1–S8 與兩份日期封面 S3a/S5a 均 HTTP 200。當日原始回應比矩陣 2026-10-20 快照**每份多 9 bytes、原始 SHA-256 全部不同**；不能聲稱新回應的 raw hash 仍相符。逐 byte 比對此前已保存、其原始長度與 SHA 與矩陣相符的十份快照後，十份差異都只在頁尾一個 SEC 注入的 `<script type="text/javascript"  src="/... "></script>` 路徑。舊新檔各只有一個這種 tag；把**這個 tag 而非整段文件**替換成同一固定字串後，十組完整檔案均 byte-for-byte 相同。內容、表格、日期與申報事實未隨尾端安全腳本輪換。下表保留當日 raw 快照及固定替換後的 SHA-256，便於重驗：

| 原件 | 2026-10-20 bytes | 2026-10-21 bytes | 10/21 raw SHA-256 | 兩日相同的固定替換 SHA-256 |
| --- | ---: | ---: | --- | --- |
| S1 | 548,307 | 548,316 | `4aef7703ea764828bc5f93a9b1792c66653df195514aea77206b07e27f272512` | `99d99273be98a5f813d026be04794c9edebf43e80d9b72e90923d97645a9c358` |
| S2 | 829,739 | 829,748 | `7b0c4bd318d0cd35899157b6027c21966225833a5590d0d973721b85e49c6780` | `4e62ad72dbddf4d6254becab21272d91ec00893def82163f192ce8874b9c9d89` |
| S3 | 53,755 | 53,764 | `f1d55c4ff0cc805b5182fb4762691bb47af7ff8e571513480523329af8cac5b5` | `dafac50758e77c772d588d168a9fa8ed8327b2e0ae2305205d7c162ef8ffaac4` |
| S3a | 37,477 | 37,486 | `1c93dbf8e1d25f0ea3d1876b10672e1aa61107b68b51c104f87db728e074a461` | `b973246f29ed45322a163df0bd5cffb3473dafddf14acba42b7a61c472b1997b` |
| S4 | 512,044 | 512,053 | `ab2391b5d58283794e266c2d2ae664b2a13a02ec796af7df2ea3af388ec71eef` | `a6f29aac5e8a8ec052e5e58625c6285946311fac242f0bace305030546a9131f` |
| S5 | 8,683 | 8,692 | `efa0a6afb043dd3009cbe0c514b59b2ca0424b4475d9097b3b5608dac3156d30` | `a7ed0f5fb9a0bff9bd9fca2c4348ee58254d93f02b930244a6cc85c96b8d2914` |
| S5a | 33,735 | 33,744 | `66201fcd39ff41e2f4b5d6589de0cae6bedfcccebfc70fa789d084b35e8419f0` | `fe2a02c353023f5cd71d4fd251f93efdada02665e08e2eb297a1a483a7f2c8ff` |
| S6 | 499,870 | 499,879 | `a61d34a9ad1be17ab40692314e3ebedceb4d988a44b3b3ec8e2ef93241abddfc` | `297dea7648f8d514f790ffde085c99eae983dbfce3add7233737ea28bc53db11` |
| S7 | 520,384 | 520,393 | `55891e3d97914c0b699734703265da8ce3387f2c891329c188e7dcbebe181b40` | `9013ac94b8b72f7d0892222b257f54ff2eee8e25b668026c44ba93c126fbc440` |
| S8 | 583,069 | 583,078 | `9270b2d4aa90a0225e510c8666eed917b6c96fb98ca73f427ccc8e667fcc6d82` | `dc66d664d8e183187184562b71f3064cb87cd8745079e8cc2ad21f62b6cad81a` |

固定替換規則：對 raw bytes 中**恰好一處**符合 `b'<script type="text/javascript"  src="/[^"]+"></script>'` 的尾端 tag，換成 `b'<SEC-DYNAMIC-SCRIPT>'`；其餘 bytes 不動。這只用於核實原件正文未變；矩陣保留真實 10/20 raw hash，當日 10/21 raw hash 另列於本票，沒有把正規化 digest 冒稱 raw hash。

v5 逐項對照：S1 的第一季司機端轉接、五月初退出八個虧損 Eats 市場，以及某些市場免新餐廳啟用費／加快加入，支持 `x190210–218` 的「司機能轉接，也需要餐廳可加入」因果鋪墊；旁白沒有說八市退出造成六月反超。S4 的 Q3 Mobility／Delivery Gross Bookings 與 Delivery +134% 支持 `x190409–412`，S5／S5a 證明 Postmates **12/1 才完成收購**，因此 `x190412` 沒把七月簽約倒灌為 Q3 成長原因。S5 的完成與開始整合、S6 的「大致整合」及近五百萬消費者／十六萬配送員／逾兩萬五千商家遷移，支持 `x190501–510`；「遷入不是留存」是避免把清單推作實際留存率，沒有捏造數字。S8 的 2022 Q4 Mobility US$14.894bn、Delivery US$14.315bn、同比 +31%／+6%，以及同季各部門 Segment Adjusted EBITDA US$1.012bn／US$241m，支持 `x190610–625`；這些不是公司 GAAP 年度淨利，也不證明最早反超季度。保留 S4 雜貨服務「九月年化交易額」與十一月公告時十多國的兩個時點，沒有把年化交易額說成實收營收。兩支 Shorts 的新 source hash／主片 shot 引用已同步，不新增獨立事實主張。其餘 v4 查過的數值、時點與分母未改且新抓內容相同。

第一鏡司機、手機和餐袋仍明示為匿名概念插畫，不是司機口述史或真 App 截圖。此票只核**稿件與完整原件**；兩名新讀者的敘事 PASS、TTS 正文 ≥8:00 實測、MiniMax 插畫、正式 5 秒／21 秒動畫、字幕、Shorts 手機觀看、US$25 實際支出、MP4 與真實 YouTube 連結仍待各自驗收。
