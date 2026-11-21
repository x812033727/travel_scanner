# curio-s38 rate-limit停止之原生圖獨立checkpoint

審閱者 `/root/s38_pf021_last_paper`。逐本輪settled PASS完整原圖及selected裁切，按curio內容相關插圖，僅重大史實／年代矛盾與畫風漂移拒收；不要求chibi年齡、普通道具或匿名幫手族裔精密重建。遵循整批完成再修政策，此票沒有因個別REJECT另觸STOP。

| 景／ledger實際累計 | 原圖與selected SHA-256 | Jev | 判斷 |
| --- | --- | --- | --- |
| pf061／2 | `pf061-1.jpg`: `612ac4db33bda9cc25310dc4c2f594dbbe6ad733f124b7015113043803fd3036` | 9.29 PASS | KEEP：本人扛木箱在木製碼頭，木船水面背景不再有現代橋船。 |
| pf062／3 | `pf062-3.jpg`: `f9d179ac90aea0bb77a7a427c124d6d1313718ae1c818342a1977aa75e4a99df` | 10 PASS | KEEP：夜間辦公室鋪大被，符合D3暫睡；不要求夫妻同框。 |
| pf063／1 | `pf063-1.jpg`: `8250e2881e928aeaabf3d81baa9336ea4ec6267a34ba3ede67a6b2ea5a9e332d` | 9.29 PASS | REJECT：周圍紙箱具四片折蓋與印刷標記，明確現代紙箱；餐桌多碗盤亦直接違背D3 L65987–65988 no fire nor dishes，非一般盤型小細節。 |
| pf064／1 | `pf064-1.jpg`: `af2a68b7a738bdc2ee303566d4c78b192f69f1f4c16030548b9907adc526f4d6`<br>`pf064-1-trim.jpg`: `c5eb821251948ed63be1ea0c301f8edec124aa69dd90eec660fc6af1a2e9516b` | 9.29 PASS | KEEP：夜間酒容器與搬運雜物，符合難搬財物的提問插圖，沒有新增歷史結果。 |
| pf065／1 | `pf065-1.jpg`: `b4eda65ed2a4309f318cc3fb11f40e3febbedb01858adf924751ca055c3afc0d`<br>`pf065-1-trim.jpg`: `cbe00bf9428e94d31f47397acd7aa7df270d132bb4d3bf279cb7bdac3fd80277` | 9.29 PASS | REJECT：中央背景明確現代拖船輪廓、矩形白色駕駛艙與近代航行設備；1666場景重大年代矛盾。 |
| pf067／1 | `pf067-1.jpg`: `f928ecdb222b9990b424265ab9194acb89fab1d412fcb2203d2c3fa64ca4afb6` | 9.29 PASS | KEEP：酒桶、土坑與思索人物，符合Batten酒難搬後想辦法，無新增結果。 |

PF061本輪檔名seed1實為跨修正累計第2actual，尚餘1；PF062本輪第3actual已PASS，不能第四次。PF063/065各1actual，未採用，餘最多2次。PF066三次machineFAIL耗盡保留needs_review，不能第四次。PF064/067各1actual。舊45KEEP不因本票而修改；上述REJECT不得入最終組片。

STOP已存在，media/jobs.json讀為空，批次因rate_limit_exceeded停止，沒有待排空job。本票只寫checkpoint，未改creative、媒體、manifest、ledger、STOP或git，未購圖。

凍結video SHA-256：`db454c5df93c692f6ba336532089692d86b82fb9eb62d352ac6643aa6faec106`。
