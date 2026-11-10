# S61 R7｜獨立史料與書面畫面覆核

2026-10-22 UTC。**HOLD：`s61031` 把來源的「general alarm」寫成「全城警報」，固定原文未證警報傳達全城。** 我不是 R7 作者；本次只覆核凍結文字，未修改作者檔案，未呼叫 TTS、圖片、音樂、評審或其他媒體。此結論僅適用下列雜湊，不是敘事雙盲、原生圖或站主核准。

| 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `ef67f56b4d384015edc9eeaea3640946ff0c4c9b778a2a587adb190c43004a65` |
| `research.md` | `3da127b6e386cfc1e67808688102124931715e75d3f5db18b38cdfda4fcc3203` |
| `video.json` | `1916964aeb68e2586c697eff5cedd61999a9c3088890f4f0ba78c1c1d694fb8e` |
| `script.md` | `9ac6972f9c3e27dd67ba11e3eb7f621da71a2c72d58b81d3c9f4dddbaa9ee4d5` |
| `claims.md` | `33283abb5ac43f98947deed544e41c730d5cbe1a1f717390a761cdcd38c65d8d` |
| `r7-author-delta.json` | `da5b1897f118184d4664fdc92b98d9d6c179a0bff1e89ea9f53a15f72e6abffd` |

固定原文是 Samuel Henry Prince，*Catastrophe and Social Change*（1920），GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`；本機 `/tmp/s61-halifax-prince.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。下述 L 行號指該轉錄檔，不是印本頁碼。Prince 親自參與救援，但碰撞、人群行動和砲兵隊細節在書中兼有轉述及研究歸因，不可都說成他親眼看見。

## 唯一 HOLD 與精確修法

`s61031` 的旁白「普林斯寫，消防員在首爆後很快回應**全城警報**，這支隊伍一時還保有組織」及 `research.md` P09 的「全城警報」多了地理覆蓋範圍。Prince [L1963–1968](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1963-L1968) 寫的是消防員「largely remained organized, and responded to the **general alarm** soon after the explosion」，然後另述**第二次爆炸警報**擴散時消防員留守。他沒有說首爆後這道警報已傳到全城；「全城」也可能使兩道警報混淆。`brief.md` 已用較精確的「消防員很快回應警報」。建議作者在下一版把 `video.json`、`script.md`、`claims.md` 的 `s61031` 和 `research.md` P09 改為「回應警報」，並同步修正任務及交接敘述、重產雜湊與差分後重新送審。R7 原檔保持凍結。

## 本版已通過的史料與畫面項目

我逐一比對 R7 變動的十個台詞／引文列、相關 `brief.md` 與 `research.md` 改文及對應書面畫面；`s61031` 除上述一詞外，其消防員迅速回應、暫保組織及畫面中的匿名消防員均符合 L1963–1968。

| R7 變動 | 固定原文與核對結果 |
| --- | --- |
| `s61005` 開場的搜救疑問、匿名搜救者 | [L924–960](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L924-L960) 記瓦礫下的傷者與火藥庫警報；[L2016–2023](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L2016-L2023) 記初期搜救。開場保留「能否等到」為問題，沒有先說救援結果。 |
| `s61008` 參與救援直連 | [L90–110](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L90-L110) 說明研究，[L766–773](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L766-L773) 直述 Prince 參與 1917 年救援；1920 年出版，符合「三年後」。未把整本書寫成親歷。 |
| `s61026` 木板直連 | [L842–873](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L842-L873) 支持玻璃及建物受損，[L1363–1370](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1363-L1370) 直述車越過「splintered boards」。新連結補足木板。 |
| `s61034` 北區多種建物起火 | [L924–937](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L924-L937) 直列「church and school, factory and home」。插圖為各類建物與匿名消防員，不畫傷亡。 |
| `s61113` 公地後如何避寒 | [L951–960](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L951-L960) 點到老人病弱者，[L1373–1398](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1373-L1398) 記徒步、寒冷與公地，[L2051–2069](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L2051-L2069) 記白帳及清出的教堂大廳；`s61081` 回收此問題，未強訂帳棚搭設在五小時分區之後。 |
| `s61054–57` 志願隊伍、身分與灌水 | [L1832–1834](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1832-L1834) 直寫整支 battery 自願灌水海軍造船廠的火藥庫。分句依序揭示行動、砲兵隊身分與灌水；沒有補造軍種、下令者、水管或精確距離。匿名隊伍及無可見軍徽／輸水裝備的畫面符合此界線。 |
| `s61059` 瓦礫下待救者卡 | [L931–937](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L931-L937) 直述消防員知道有人受傷困於瓦礫、無法自行脫困；資訊卡「北區火場／瓦礫下仍有人待救／Prince 1920 年研究」未畫可辨傷者。 |

機械核對：103／103 非片尾 scene 各有且只有一列 `claims.md`；每列旁白逐字對上 `video.json` 與 `script.md`，每列有固定來源錨點，127 個連結皆指固定 commit 且行號在 6,215 行 raw 內。96／96 `shot` 提示詞及 7／7 `big` 卡文字和主張列相同；96 幅提示詞互不重複，最多連續一張卡；`look` 是 `cute-mystery`，共有 20 組 `loops`。其餘未改行承接 R6 的逐句獨立來源覆核，這次又核了完整映射及變動上下文；本版 103／103 **有來源覆蓋**，但 `s61031` 的「全城」未獲來源支持，因此**史實尚未全過**。

獨立重放 `r7-author-delta.json`：以 `/tmp/s61-r6-pr-frozen/` 六檔為 R6 基準，逐塊確認舊／新行及零起算座標，正向得到本版六檔，逆向逐位元還原；`brief.md`、`research.md`、`video.json`、`script.md`、`claims.md`、任務票分別 5／3／16／9／8／4 塊，全數通過。這只證明差分可逆，不替代上面的史料判斷。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json` exit 0，**0 errors／0 warnings**，106 句（103 正文加 3 句品牌片尾）、六章。用 `estimateTimeline(doc, 325)` 獨立量得濃縮開場 **48.23 秒**、開場後至片尾前正文 **486.57 秒（8:06.57）**；250 CPM 時分別 59.53 秒與 604.00 秒。這是合成前估時，沒有實際旁白音檔可量。

書面畫面沒有要求可讀的原始命令、官方地圖、新聞或血腥重建；本輪改動的匿名搜救者、消防員、北區建物、志願隊伍和資訊卡與相鄰台詞及來源相容。**96 幅插圖及 7 張卡的書面畫面 PASS**，不等於生成圖 KEEP；原生圖仍須按系列規則逐張檢查人物群組、年代、文字、畫風及黑邊。R7 的獨立史料結論維持上述一處 HOLD，修復後須按新雜湊重新覆核。
