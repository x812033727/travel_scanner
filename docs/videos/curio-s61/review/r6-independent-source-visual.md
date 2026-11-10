# S61 R6｜獨立史料、差異與書面畫面覆核

2026-10-22 UTC。**固定史料與書面畫面 PASS；原生圖、正式敘事雙盲、語音與成片均未放行。**我不是 R6 作者，沒有修改劇本、主張、分鏡或來源，也未呼叫付費媒體。本結論只對以下凍結檔案有效。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `bd52f1b3fa5d36135939435a6599b3eee181109e4d6720afbfdb8845b2f126d0` |
| `research.md` | `c67653b6b71955de68bc9f82e0a17d1837ec96c4885dbe6282a7a648ddf05457` |
| `video.json` | `f7a68ab0582ea4060bf144da4266d676478c8aff5d33f9bcfece4f11b2c3f637` |
| `script.md` | `3fbc7c935bcb1e12f20ce78e68387606061cdb1086930e288f7a973205b11a32` |
| `claims.md` | `05629423c2d96a8b82ef52a5b23ea9a78befd6fab0efe540406ad6746c1943b1` |
| `r6-author-delta.json` | `2278cb95a666488f9e629579fe9045ab1483f2b241b57e2c9505f5ce591e809d` |

重新核對固定 Samuel Henry Prince，[*Catastrophe and Social Change*（1920）](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt)，commit `befb706982ba1be631a52d4f686be301c2de7f34`；本機 raw `/tmp/s61-halifax-prince.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。行號指這份固定轉錄檔，不是原版頁碼。Prince 親自參與救援，但對碰撞、群眾與砲兵隊的文字有引述與研究歸因，影片已標清這些層級。

## 雙向差分與機械對齊

獨立逐塊重放 `r6-author-delta.json`，不是只信作者自述。以 `/tmp/s61-r5-frozen/` 六檔作基準，每塊舊／新行及零起算座標均對上，正向得到表列 R6 SHA，再逆向逐位元還原 R5 SHA；`brief.md`、`research.md`、`video.json`、`script.md`、`claims.md`、任務票分別 **4／3／72／115／23／5 塊，六檔全 PASS**。其中 `brief.md`、`research.md` 的 R5 凍結基準比本 PR 的前一提交多了作者於 R5 查核後寫入的狀態說明；差分自身的基準 SHA 與凍結檔相符，沒有拿 PR 前一提交冒充該基準。

`video.json` 有 **103／103** 非片尾台詞 ID 與 `claims.md` 一對一逐字相同，主張表沒有缺列或多列；96／96 `shot` 提示詞逐字列於同一主張列且互不重複，另有 7 張 `big` 字卡；3 句品牌片尾不作史實主張。主張表 129 個來源連結均指固定 commit，代碼 P01–P14 的實際使用者都有定義，行號在 raw 範圍內。全部 106 句旁白亦出現在 `script.md`。CLI `lint --slug curio-s61 --json` exit 0，**0 errors／0 warnings**。獨立用 `estimateTimeline(doc, 325)` 量得首章 **48.03 秒**，片頭後至片尾前正文 **484.70 秒（8:04.70）**；250 CPM 時正文 601.57 秒。這些是合成前估算，實際 TTS 時長仍須另量。

## 原文重新核對

- Prince [L789–841](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L789-L841) 明記戰時船隊、爆裂物進出總量未公開確數、蒙布朗號從紐約進港等待船隊及船貨、伊莫號空載出港與平日為比利時運糧。法國船原為法國戰場運軍需，畫面僅作無標示貨船與貨物示意，不給船長虛構對白或碰撞責任。
- [L1282–1303](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1282-L1303) 有船員離船、約二十分鐘後首爆、Prince 認為可利用間隔示警，並附他轉引的調查對船長與領港員示警不足的批評。`s61021–22` 的問題與回答對準這個來源，沒有把調查轉引說成已另查完整判決。
- [L924–960](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L924-L960) 支持北區多處房火、瓦礫下有人無法脫困且消防員知道、首爆不到一小時火勢逼近海軍造船廠火藥庫；[L902–948](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L902-L948) 支持城堡震動、煤灰油水、海水進街後留下小艇、列車停止與車輛扭曲。`s61142` 只說書裡沒寫火已入庫，不畫庫房起爆。
- [L1363–1398](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1363-L1398) 原文「*Some ran to their shops. Those in the shops ran home.*」確為兩群；R6 `s61130`「有人跑向店鋪；店裡的人則趕回家」及兩間不同店鋪、兩名成人的提示詞沒有再拼成同一人的去返路線。Prince 轉引 Johnstone 手稿記士兵南移警告、帶孩子與包袱、徒步者、望家與望天、公地／山坡的人潮和騎馬者解除消息；影片有指出這是**轉引**，沒有變成 Prince 逐戶目擊。
- [L1824–1836](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1824-L1836) 說一整支砲兵隊自願為火藥庫灌水，Prince 將第二次沒有爆炸歸於此。`s61095–97` 清楚標示是 1920 年研究的歸因及未另核軍方卷宗；畫面不發明軍種、命令、灌水器具或精確火距。[L1963–1968](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1963-L1968) 支持消防正副長遇難、市政官員接手與消防員在警報後仍守崗。
- [L1990–2023](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1990-L2023) 支持軍人救援、居民先找家人而沒有家屬牽掛的訪客較早投入、醫療船一刻鐘內派兩支外科醫師上岸隊、北區車站乘客急救、蒙特婁旅客至少協助五十人、初期同一廢墟重搜兩三次與約五小時後分區記錄。[L2051–2069](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L2051-L2069) 支持公地白帳與教堂收容；`s61081` 用「那一天」回指，沒有指定帳棚一定在五小時分區之後才搭。

## 紙面畫面與後續原圖界線

96 個插圖提示與 7 張字卡沒有要求可讀軍方命令、原始新聞／地圖、可辨認傷者或血腥重建；`look` 僅 `cute-mystery`，音樂採系列固定配方。`s61130` 的兩個店鋪、`s61144` 的兩處分開室內、`s61049` 的 1917 年車輛與徒步人潮、`s61057` 的砲兵隊、`s61139` 的列車與車輛都要在**原生圖**逐張看人物群組、年代、畫風和黑邊。書面 PASS 不是原圖 KEEP，也不代表整集分鏡、語音或影片完成。

**兩處直連行號可在出稿前精修，無須改旁白事實：**`claims.md` 的 `s61008` 引 P01 L90–110 支持研究自述，參與 1917 救援的直述實在同一固定 raw [L766–773](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L766-L773)；`s61026` 直連 P04 L842–873 有玻璃與建物受損，而「碎木板」見 [L1363–1370](https://github.com/GITenberg/Catastrophe-and-Social-ChangeBased-Upon-a-Sociological-Study-of-the-Halifax-Disaster_37580/blob/befb706982ba1be631a52d4f686be301c2de7f34/37580.txt#L1363-L1370)。兩個事實都已在相同固定來源中核到，屬引用範圍精度，非新增無據情節；若修 `claims.md`，須更新其 SHA 與對應回條，不得把本次 SHA 的結論直接冒用到新檔。
