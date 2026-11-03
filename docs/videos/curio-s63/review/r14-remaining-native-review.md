# curio-s63 原生圖獨立驗收

審閱者 `/root/s38_pf021_last_paper`。逐完整原圖／selected crop按curio插圖標準，僅重大史實年代矛盾與畫風漂移拒收，不因chibi或普通小物件精密重建加嚴。

起始15KEEP完整記錄canonical SHA-256：`809f6619f6b81ad13e4ade51a4b1b33dcaae53b45497e9ff6e9b29842b9ba966`。

| 景／actual | 原圖與selected SHA-256 | Jev | 判斷 |
| --- | --- | --- | --- |

| s63020／2 | `s63020-2.jpg`: `475ec8eeea4a15d7195a1629b5907fa352192af8a44a6f56f76c5203b3805b80`<br>`s63020-2-trim.jpg`: `da7d1226f4e9ec82b7d0db74b9442f34251989ac165b0574e508020791e6cac8` | 10 PASS | KEEP：棕膚男子在門口傾聽，符合Nancy主人承諾段落的聆聽示意；裁切消除黑邊，無實質現代物件。 |

| s63021／2 | 原圖＝selected `s63021-2.jpg`: `0bb184ee2d550bbe85c84bdcbaaf3e759ffa47c0ddaf2a073c7319bde43add70` | 9.29 PASS | REJECT：右側明確多輛現代汽車及現代道路，與1840s現場矛盾；不是因chibi、牌匾塗鴉或手勢。已touch STOP。 |

已STOP，等待結算；未列者未驗收。

## 停止結算

日誌已確認stopped after6 new keyframes，media/jobs.json為空。ledger本輪20=2、21=2、22=2，共6個ready；s63022第二張已ready未judge，key `9e306bde755d4a09`，原圖SHA-256 `4bbf79ebf97892116b4cec7539e9f386c9fbe5d87944fc75d8fb6baaf43baefe`，因此22已2actual僅剩1次，不能漏算第二張。21亦已2actual僅餘1，20本票KEEP。未改創作、媒體、manifest、ledger或git；僅本票與STOP。
